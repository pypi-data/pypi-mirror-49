import json, os, logging, pprint
import numpy as np
from copy import deepcopy
from collections import namedtuple, defaultdict, OrderedDict
from . import util
from .text_process import Vocabulary

InputFeature = namedtuple('InputFeature', ['name', 'shape', 'dtype', 'sparse'])
InputFeature.__new__.__defaults__ = (None,) * len(InputFeature._fields)


def copy_dict(src, dst):
    dic = {}
    for w in dst:
        dic[w] = src[w]
    return dic

class BasicCFG(object):
    def update(self, cfg):
        for k, v in cfg.items():
            attr = getattr(self, k, None)
            if isinstance(attr, dict):
                attr.update(v)
            else:
                setattr(self, k, v)

    def save(self, fpath):
        with open(fpath, 'w') as f:
            json.dump(self.__dict__, f)

    def load(self, fpath):
        with open(fpath) as f:
            cfg = json.load(f)
        self.update(cfg)

    def copy(self):
        return deepcopy(self)

    def __str__(self):
        return pprint.pformat(self.__dict__, indent=4)


class CFG(BasicCFG):
    def __init__(self):
        self.seed = 9798
        self.lr = 1e-3
        self.min_lr_ratio = 0.001
        self.warmup_steps = 1000
        self.es = -0.001
        self.batch_size = 32
        self.val_batch_size = self.batch_size
        self.lr_decay_step = 1000000000
        self.save_step = 1000000000
        self.save_epoch = 1000000000
        self.epoch_step = 1000000000
        self.val_step = 1000000000
        self.val_batchs = 1000000000
        self.emb_dim = 8
        self.epochs = 10
        self.scoring = False
        self.min_cnt = 5 # minimum count for building vocabulary
        self.save_model = False  # if save model after fit
        self.only_validate = False
        self.no_validate = False
        self.debug = False
        self.dropout = None
        self.data_dir = 'data'
        self.vocab_file = None
        self.tokenizer = None
        self.copy_source = False  # if copy the model definition source file when save model


class LossHist(defaultdict):
    def __init__(self, decimal_digits=8, *args, **kwargs):
        self._fstr = "{}:{:." + str(8) + "f}"
        super(LossHist, self).__init__(list, *args, **kwargs)

    def append(self, losses):
        for name, loss in losses.items():
            self[name].append(loss)

    def get_avg(self):
        avg_loss = OrderedDict()
        keys = sorted(self.keys())
        for key in keys:
            avg_loss[key] = np.mean(self[key])
        return avg_loss

    def get_avg_sum(self):
        avg_loss = self.get_avg()
        return np.sum([v for k, v in avg_loss.items()])

    def avg_output(self):
        avg_loss = self.get_avg()
        #tot = np.sum(v for k, v in avg_loss.items())
        #avg_loss['tot'] = tot
        outstr = ', '.join(self._fstr.format(k, v) for k, v in avg_loss.items())
        return outstr


class CallBack(object):

    def __init__(self, itr=0):
        self.itr = itr

    def on_train_begin(self):
        pass

    def on_batch_start(self, batch):
        pass

    def on_batch_end(self, epoch):
        self.itr += 1


class BasicModel(object):
    cfg = CFG()
    vocab = None
       
    def __init__(self, name, cfg={}):
        self.name = name
        self.update_cfg = cfg
        self.cfg = deepcopy(self.cfg)
        self.cfg.update(self.update_cfg)

        if self.cfg.vocab_file is not None:
            if self.cfg.debug:
                self.cfg.vocab_file = self.cfg.vocab_file + '_debug'
#            self.vocab = Vocabulary('vocab', os.path.abspath(self.cfg.vocab_file))
            self.vocab = util.get_class(self.cfg.vocab)('vocab', self.cfg.vocab_file, min_cnt=self.cfg.min_cnt)
            self.cfg.vocab_size = self.vocab.size

#        if self.name is None:
#            self.name = self.__class__.__name__
        self._rs = np.random.RandomState(self.cfg.seed)

        self._model = None

        dirname = self.gen_fname('')
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        script_file = os.path.basename(__file__)
        if self.cfg.save_model:
            if not os.path.exists(self.cfg.data_dir):
                os.mkdir(self.cfg.data_dir)
            fpath = self.gen_fname('', script_file)
            dirname = os.path.dirname(fpath)
            if self.cfg.copy_source:
                shutil.copy2(script_file, dirname)
        if self.cfg.save_log:
            flog = self.gen_fname('', util.timestamp()+'.log')
            file_handler = logging.FileHandler(flog)
            log_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(threadName)s %(message)s')
            file_handler.setFormatter(log_formatter)
            logging.getLogger().addHandler(file_handler)

        logging.info('model cfg is: %s', self.cfg)

    def destroy(self):
        """
        release resource
        """
        pass

    def create_model(self):
        self._model = self

    def _process_data(self, data, data_type):
        """
        process data and update configuration like cfg.emb_size if needed
        :param data:
        :param data_type: 'train', 'validate', 'test'
        :return: processed_data, label
        """
        return data

    def process_data(self, data_dict):
        """
        :param data_dict: dictionary of data. keys:train, validate, test
        :return:
        """
        data = []
        for data_type in ['train', 'validate', 'test']:  # keep train first
            if data_type in data_dict:
                with util.timer('process data type {}'.format(data_type)):
                    processed_data = list(self._process_data(data_dict[data_type], data_type))
                for d in processed_data:
                    if d is not None:
                        for k in d:
                            if isinstance(d[k], list):
                                d[k] = np.array(d[k])
                data += processed_data
            else:
                data += [None, None]
        return data

    def fit(self, x, y, xV = None, yV = None, save=False, restore=False, xTest=None):
        if self._model is None:
            self.create_model()
        if restore:
            self.restore()

        best_val_loss = np.inf
        for i in range(self.cfg.epochs):
            logging.info("fit start")
            loss, val_loss = self._fit_epoch(x, y, xV, yV, epoch=i, xTest=xTest)
            if not self.cfg.no_validate:
                if self.cfg.scoring:
                    score = self.score(xV, yV)
                if not loss <np.inf:
                    logging.error('something is wrong loss is:%s, exit', loss)
                    raise Exception('loss:{} is abnormal'.format(loss))

                if self._should_stop(best_val_loss, val_loss):
                    break
                else:
                    if best_val_loss > val_loss:
                        best_val_loss = val_loss

        if save and self.cfg.save_epoch != 1:
            self.save()

        logging.info('***** end fit')
        return loss, best_val_loss

    def _should_stop(self, best_val_loss, val_loss):
        stop = False
        if (best_val_loss-val_loss) / val_loss < -self.cfg.es:
            logging.info("(best_val_loss %s - val_loss %s) / val_loss %s < minus early stop %s, train done", best_val_loss, val_loss, val_loss, self.cfg.es)
            stop = True
        return stop


    def gen_fname(self, postfix, *paras):
        name = self.name
        if self.cfg.debug:
            name = 'debug_' + name
        if postfix:
            name += '_' + postfix
        fname = os.path.join(self.cfg.data_dir, name, *paras)
        return fname
    
    def restore(self):
        fpath = self.gen_fname('', 'cfg.json')
        self.cfg.load(fpath)
        self.cfg.update(self.update_cfg)
        logging.info('model cfg after restore is: %s', self.cfg)


    def save(self):
        fpath = self.gen_fname('', 'cfg.json')
        dirname = os.path.dirname(fpath)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        self.cfg.save(fpath)


    def save_predict(self, pred, suffix=''):
        fpath = self.gen_fname('', 'pred' + suffix + '.dump')
        util.dump(pred, fpath)

        
    def predict(self, x):
        pred = self._model.predict(x)
        return pred

    def score(self, x, y):
        pass
