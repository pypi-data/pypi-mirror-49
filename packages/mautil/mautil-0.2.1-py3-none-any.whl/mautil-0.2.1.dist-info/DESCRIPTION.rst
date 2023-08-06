# mautil
An deep learning util based on tensroflow.
- easy to build model and do experiments
- easy to debug
- support for colab tpu
- no need to transfer data to tf records(non tpu)

# requirements
tensorflow >= 1.11

# Install
`pip install mautil`

# Demo
## Text style transfer
- There are two text style transfer models. CA is an implementation of the  paper  [Style Transfer from Non-Parallel Text byCross-Alignment](https://papers.nips.cc/paper/7259-style-transfer-from-non-parallel-text-by-cross-alignment.pdf). CAR model just use reinforcement learning to bypass gumbel softmax
- run the text style transfer model in debug mode

  `python train.py -m CAR -dataset yelp -d`

## TPU
- see the [notebook](demo/colab/mautil_tfxl_colab_tpu.ipynb) about how to train a transformer-xl model for dataset wikitext103
- the demo is for colab cloud tpu, you need google cloud storage access to run the demo


