import os, logging
from collections import Counter
from . import util


class Vocabulary(object):
    fake = {'[PAD]': 0, '[SOS]': 1, '[EOS]': 2, '[UNK]': 3, '[SEP]': 4}

    def __init__(self, name, vocab_path, min_cnt=5, tokenizer=None):
        self.name = name
        self.vocab_path = vocab_path
        self.size = None
        self.vocab = None
        self.tokenizer = tokenizer
        self.min_cnt = min_cnt

        if os.path.isfile(self.vocab_path):
            self.restore()

    def restore(self):
        logging.info('load vocab from saved file: %s', self.vocab_path)
        self.vocab = util.load_json(self.vocab_path)
        self.size = len(self.vocab['word2id'])

    def _build_vocab(self, cnt):
        word2id = self.fake.copy()
        id2word = [k for k, v in sorted(word2id.items(), key=lambda x:x[1])]
        for word in cnt:
            if cnt[word] >= self.min_cnt:
                word2id[word] = len(word2id)
                id2word.append(word)
        self.size = len(word2id)
        self.vocab = {'word2id': word2id, 'id2word': id2word, 'word_cnt': dict(cnt)}

    def build_vocab(self, sents, save=True):
        if self.vocab is None:
            logging.info('building vocab')

            cnt = Counter()
            if self.tokenizer:
                for sent in sents:
                    for word in self.tokenizer(sent):
                        cnt.update([word])
            else:
                for sent in sents:
                    for word in sent:
                        cnt.update([word])
            self._build_vocab(cnt)
            if save:
                util.dump_json(self.vocab, self.vocab_path)
                logging.info('vocab saved to :%s', self.vocab_path)
        logging.info('vocab size:%s', self.size)

    def seq(self, sents, max_len=None, add_sos=True, add_eos=True):
        w2i = self.vocab['word2id']
        pad = w2i['[PAD]']
        add_len = 0
        if add_sos:
            add_len += 1
        if add_eos:
            add_len += 1
        seqs = []
        seq_lens = []
        for sent in sents:
            if self.tokenizer:
                tokens = self.tokenizer(sent)
            else:
                tokens = sent
            inds = [w2i[w] if w in w2i else w2i['[UNK]'] for w in tokens]
            if max_len is not None:
                inds = inds[0:max_len-add_len]
            if add_sos:
                inds = [w2i['[SOS]']] + inds
            if add_eos:
                inds += [w2i['[EOS]']]
            seq_lens.append(len(inds))
            if max_len is not None:
                inds += [pad] * (max_len - len(inds))
            seqs.append(inds)
        return seqs, seq_lens

    def deseq(self, seqs):
        id2w = self.vocab['id2word']
        sents = []
        for seq in seqs:
            sent = []
            for word_id in seq:
                sent.append(id2w[word_id])
            sents.append(sent)
        return sents



