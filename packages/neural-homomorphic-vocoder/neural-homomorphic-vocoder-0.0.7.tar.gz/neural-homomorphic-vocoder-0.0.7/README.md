[![CI](https://github.com/k2kobayashi/neural-homomorphic-vocoder/actions/workflows/ci.yaml/badge.svg)](https://github.com/k2kobayashi/neural-homomorphic-vocoder/actions/workflows/ci.yaml)
[![PyPI version](https://badge.fury.io/py/neural-homomorphic-vocoder.svg)](https://badge.fury.io/py/neural-homomorphic-vocoder)
[![Downloads](https://pepy.tech/badge/neural-homomorphic-vocoder)](https://pepy.tech/project/neural-homomorphic-vocoder)

# neural-homomorphic-vocoder

A neural vocoder based on source-filter model called neural homomorphic vocoder

# Install

```shell
pip install neural-homomorphic-vocoder
```

# Usage

Usage for NeuralHomomorphicVocoder class
- Input
    - x: mel-filterbank
    - cf0: continuous f0
    - uv: u/v symbol

```python
import torch
from nhv import NeuralHomomorphicVocoder

net = NeuralHomomorphicVocoder(
        fs=24000,             # sampling frequency
        fft_size=1024,        # size for impuluse responce of LTV
        hop_size=256,         # hop size in each mel-filterbank frame
        in_channels=80,       # input channels (i.e., dimension of mel-filterbank)
        conv_channels=256,    # channel size of LTV filter
        ltv_out_channels=222, # output size of LTV filter
        out_channels=1,       # output size of network
        kernel_size=3,        # kernel size of LTV filter
        group_size=8,         # group size of LTV filter
        dilation_size=1,      # dilation size of LTV filter
        fmin=80,              # min freq. of melspc calculation
        fmax=7600,            # max freq. of melspc calculation (recommend to use full-band)
        roll_size=24,         # frame size to get median to estimate logspc from melspc
        look_ahead=32,        # # of look_ahead samples (if use_causal=True)
        use_causal=False,     # use causal conv LTV filter
        use_ddsconv=False,    # use ddsconv instead of normal conv for LTV network
        use_tanh=False,       # apply tanh to output else linear
        use_conv_postfilter=False,     # use causal conv postfilter for NHV output
        use_ddsconv_pf=True,           # use ddsconv postfilter instead of conv1d
        use_ltv_conv_postfilter=False, # use causal conv postfilter for LTV output
        use_reference_mag=False,       # use reference logspc calculated from melspc
        use_quefrency_norm=True,       # enable ccep normalized by quefrency index
        use_weight_norm=False,         # apply weight norm to conv1d layer
        use_clip_grad_norm=False,      # use clip_grad_norm (norm_value=3)
        scaler_file=None      # path to .pkl for internal scaling of melspc
                              # (dict["mlfb"] = sklearn.preprocessing.StandardScaler)
)

B, T, D = 3, 100, in_channels   # batch_size, frame_size, n_mels
z = torch.randn(B, 1, T * hop_size)
x = torch.randn(B, T, D)
cf0 = torch.randn(B, T, 1)
uv = torch.randn(B, T, 1)
y = net(z, torch.cat([x, cf0, uv], dim=-1))   # z: (B, 1, T * hop_size), c: (B, D+2, T)
y = net._forward(z, cf0, uv)
```

# Features

- (2021/05/21): Train using [kan-bayashi/ParallelWaveGAN](https://github.com/kan-bayashi/ParallelWaveGAN) with continuous F1 and uv symbols
- (2021/05/24): Final FIR filter is implemented by 1D causal conv
- (2021/06/17): Implement depth-wise separable convolution

# References

```bibtex
@article{liu20,
  title={Neural Homomorphic Vocoder},
  author={Z.~Liu and K.~Chen and K.~Yu},
  journal={Proc. Interspeech 2020},
  pages={240--244},
  year={2020}
}
```
