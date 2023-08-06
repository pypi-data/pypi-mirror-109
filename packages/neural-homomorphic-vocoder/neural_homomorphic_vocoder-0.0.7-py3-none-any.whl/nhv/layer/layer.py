#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2021 Kazuhiro KOBAYASHI <root.4mac@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class Conv1d(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size=3,
        dilation_size=1,
        group_size=1,
        use_causal=False,
        look_ahead=0,
    ):
        super().__init__()
        self.use_causal = use_causal
        self.look_ahead = look_ahead
        self.kernel_size = kernel_size
        self.padding = (kernel_size - 1) * dilation_size

        self.conv1d = nn.Conv1d(
            in_channels,
            out_channels,
            kernel_size,
            padding=self.padding,
            dilation=dilation_size,
            groups=group_size,
        )
        nn.init.kaiming_normal_(self.conv1d.weight)

        if use_causal and self.kernel_size != 1:
            assert look_ahead >= 0, "look_ahead must be > 0."
            assert look_ahead < self.padding, "look_ahead must be < self.padding."

    def forward(self, x):
        """
        x: (B, T, D)
        y: (B, T, D)
        """
        x = x.transpose(1, 2)
        y = self.conv1d(x)
        # NOTE(k2kobayashi): kernel_size=1 does not discard padding
        if self.kernel_size != 1:
            if self.use_causal:
                y = y[..., self.look_ahead : -self.padding + self.look_ahead]
            else:
                y = y[..., self.padding // 2 : -self.padding // 2]
        return y.transpose(1, 2)


class ConvLayers(nn.Module):
    def __init__(
        self,
        in_channels,
        conv_channels=256,
        out_channels=222,
        kernel_size=3,
        dilation_size=1,
        group_size=8,
        look_ahead=0,
        use_causal=False,
        use_ddsconv=False,
        use_quefrency_norm=True,
    ):
        super().__init__()
        self.in_channels = in_channels
        self.conv_channels = conv_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.dilation_size = dilation_size
        self.group_size = group_size
        self.use_causal = use_causal
        self.use_quefrency_norm = use_quefrency_norm
        self.look_ahead = look_ahead
        self.use_ddsconv = use_ddsconv

        if not use_ddsconv:
            self.net = self.original_conv()
        else:
            self.net = self.dds_conv()

        if self.use_quefrency_norm:
            idx = torch.arange(1, out_channels // 2 + 1).float()
            self.quef_norm = torch.cat([torch.flip(idx, dims=[-1]), idx], dim=-1)

    def forward(self, x):
        """
        x: (B, T, in_channels)
        y_comp: (B, T, out_channels)
        """
        y = self.net(x)
        if self.use_quefrency_norm:
            y = y / self.quef_norm.to(y.device)
        return y

    def original_conv(self):
        return nn.Sequential(
            Conv1d(
                self.in_channels,
                self.conv_channels,
                self.kernel_size,
                self.dilation_size,
                1,
                self.use_causal,
            ),
            nn.ReLU(),
            Conv1d(
                self.conv_channels,
                self.conv_channels,
                self.kernel_size,
                self.dilation_size,
                self.group_size,
                self.use_causal,
            ),
            nn.ReLU(),
            Conv1d(
                self.conv_channels,
                self.conv_channels,
                self.kernel_size,
                self.dilation_size,
                self.group_size,
                self.use_causal,
            ),
            nn.ReLU(),
            Conv1d(
                self.conv_channels,
                self.out_channels,
                self.kernel_size,
                self.dilation_size,
                1,
                self.use_causal,
            ),
        )

    def dds_conv(self):
        modules = []
        modules += [
            Conv1d(
                in_channels=self.in_channels,
                out_channels=self.conv_channels,
                kernel_size=1,
                dilation_size=1,
                group_size=1,
                use_causal=self.use_causal,
            )
        ]
        for i in range(3):
            if self.dilation_size == 1:
                dilation_size = self.kernel_size ** i
            else:
                dilation_size = self.dilation_size ** i
            modules += [
                DepthSeparableConvBlock(
                    channels=self.conv_channels,
                    kernel_size=self.kernel_size,
                    dilation_size=dilation_size,
                    use_causal=self.use_causal,
                )
            ]
        modules += [
            Conv1d(
                in_channels=self.conv_channels,
                out_channels=self.out_channels,
                kernel_size=1,
                dilation_size=1,
                group_size=1,
                use_causal=self.use_causal,
                look_ahead=self.look_ahead,
            )
        ]
        return nn.Sequential(*modules)


class DepthSeparableConvBlock(nn.Module):
    def __init__(self, channels, kernel_size, dilation_size, use_causal=False):
        super().__init__()
        self.sep_conv = Conv1d(
            channels,
            channels,
            kernel_size,
            dilation_size,
            group_size=channels,
            use_causal=use_causal,
        )
        self.conv1d = Conv1d(
            channels,
            channels,
            kernel_size=1,
            dilation_size=1,
            group_size=1,
            use_causal=use_causal,
        )
        self.ln1 = nn.LayerNorm(channels)
        self.ln2 = nn.LayerNorm(channels)

    def forward(self, x):
        y = self.sep_conv(x)
        y = self.ln1(y)
        y = F.gelu(y)
        y = self.conv1d(y)
        y = self.ln2(y)
        y = F.gelu(y)
        return x + y


class ConvLTVFilterGenerator(nn.Module):
    def __init__(
        self,
        in_channels,
        conv_channels=256,
        ltv_out_channels=222,
        kernel_size=3,
        dilation_size=1,
        group_size=8,
        fft_size=1024,
        hop_size=256,
        look_ahead=256,
        mel2spc_fn=None,
        use_causal=False,
        use_ddsconv=False,
        use_ltv_conv_postfilter=False,
        use_quefrency_norm=True,
    ):
        super().__init__()
        self.fft_size = fft_size
        self.hop_size = hop_size
        # TODO(k2kobayashi): support overlap size not only 50%
        self.window_size = hop_size * 2
        self.ltv_out_channels = ltv_out_channels
        self.mel2spc_fn = mel2spc_fn
        self.use_ltv_conv_postfilter = use_ltv_conv_postfilter

        win_norm = self.window_size // (hop_size * 2)  # only for hanning window
        self.win = torch.hann_window(self.window_size) / win_norm
        self.conv = ConvLayers(
            in_channels,
            conv_channels,
            ltv_out_channels,
            kernel_size=kernel_size,
            dilation_size=dilation_size,
            group_size=group_size,
            use_causal=use_causal,
            use_ddsconv=use_ddsconv,
            use_quefrency_norm=use_quefrency_norm,
        )

        if self.use_ltv_conv_postfilter:
            self.conv_pf = Conv1d(
                in_channels=1,
                out_channels=1,
                kernel_size=hop_size,
                use_causal=True,
                look_ahead=look_ahead,
            )

    def forward(self, x, z):
        """
        x: B, T, D
        z: B, 1, T * hop_size
        """
        ccep = self.conv(x)
        if self.mel2spc_fn is not None:
            log_mag = self.mel2spc_fn(x)
        else:
            log_mag = None

        y = self._ccep2impulse(ccep, ref=log_mag)
        z = self._conv_impulse(z, y)
        z = self._ola(z)
        if self.use_ltv_conv_postfilter:
            z = self.conv_pf(z.transpose(1, 2)).transpose(1, 2)

        z = torch.clamp(z, -1, 1)
        return z

    def _ccep2impulse(self, ccep, ref=None):
        padding = (self.fft_size - self.ltv_out_channels) // 2
        ccep = F.pad(ccep, (padding, padding))
        y = torch.fft.fft(ccep, n=self.fft_size, dim=-1)
        if ref is not None:
            # TODO(k2kobayashi): it requires to consider following line.
            # this mask eliminates very small amplitude values (-100).
            # ref = ref * (ref > -100)
            y.real[..., : self.fft_size // 2 + 1] += ref
            y.real[..., self.fft_size // 2 :] += torch.flip(ref[..., 1:], dims=[-1])

        # NOTE(k2kobayashi): we assume intermidiate log amplitude as 10log10|mag|
        mag, phase = torch.pow(10, y.real / 10), y.imag
        real, imag = mag * torch.cos(phase), mag * torch.sin(phase)
        y = torch.fft.ifft(torch.complex(real, imag), n=self.fft_size, dim=-1)
        return y.real

    def _conv_impulse(self, z, y):
        z = z.reshape(z.size(0), 1, -1)  # (B, 1, T x hop_size)
        z = F.pad(z, (self.window_size // 2 - 1, self.window_size // 2))
        z = z.unfold(-1, self.window_size, step=self.hop_size)  # (B, 1, T, window_size)

        z = F.pad(z, (self.fft_size // 2 - 1, self.fft_size // 2))
        z = z.unfold(-1, self.fft_size, step=1)  # (B, 1, T, window_size, fft_size)

        # z = matmul(z, y) -> (B, 1, T, window_size) where
        # z: (B, 1, T, window_size, fft_size)
        # y: (B, T, fft_size) -> (B, 1, T, fft_size, 1)
        z = torch.matmul(z, y.unsqueeze(1).unsqueeze(-1)).squeeze(-1)
        return z

    def _ola(self, z):
        z = z * self.win.to(z.device)
        l, r = torch.chunk(z, 2, dim=-1)  # (B, 1, T, window_size // 2)
        z = l + torch.roll(r, 1, dims=2)  # roll a frame of right side
        z = z.reshape(z.size(0), 1, -1)
        return z


class SinusoidsGenerator(nn.Module):
    def __init__(
        self,
        hop_size,
        fs=24000,
        excit_amp=0.1,
        noise_std=0.03,
        n_harmonics=200,
        use_uvmask=True,
    ):
        super().__init__()
        self.fs = fs
        self.excit_amp = excit_amp
        self.noise_std = noise_std
        self.upsample = nn.Upsample(scale_factor=hop_size, mode="nearest")
        self.use_uvmask = True

        self.n_harmonics = n_harmonics
        self.harmonics = torch.arange(1, self.n_harmonics + 1).unsqueeze(-1)

    def forward(self, cf0, uv):
        device = cf0.device
        f0, uv = self.upsample(cf0.transpose(1, 2)), self.upsample(uv.transpose(1, 2))
        excit = self.generate_sinusoids(f0, uv).reshape(cf0.size(0), 1, -1)
        noise = torch.normal(0, self.noise_std, size=excit.size()).to(device)
        return excit, noise

    def generate_sinusoids(self, f0, uv):
        harmonics = self.harmonics.to(f0.device)
        mask = self.anti_aliacing_mask(f0 * harmonics)
        rads = f0.cumsum(dim=-1) * 2.0 * math.pi / self.fs * harmonics
        excit = torch.sum(torch.cos(rads) * mask, dim=1, keepdim=True)
        if self.use_uvmask:
            excit = uv * excit
        return self.excit_amp * excit

    def anti_aliacing_mask(self, f0_with_harmonics, use_soft_mask=False):
        if use_soft_mask:
            return torch.sigmoid(-(f0_with_harmonics - self.fs / 2.0))
        else:
            return (f0_with_harmonics < self.fs / 2.0).float()
