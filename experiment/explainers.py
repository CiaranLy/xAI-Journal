"""Saliency methods, all returning non-negative maps of shape (N, H, W) as numpy arrays.

Gradient-based maps use the absolute attribution summed over colour channels,
following Adebayo et al. (2018). Grad-CAM is implemented directly so the
target layer and post-processing are explicit.
"""
import copy

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from captum.attr import IntegratedGradients

from common import DEVICE, black_baseline

TARGET = 1  # explain the "tumour" logit


def _to_map(attr):
    return attr.abs().sum(dim=1).detach().cpu().numpy()


def gradient(model, x):
    x = x.clone().to(DEVICE).requires_grad_(True)
    model(x)[:, TARGET].sum().backward()
    return _to_map(x.grad)


class _GuidedReLUFn(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return x.clamp(min=0)

    @staticmethod
    def backward(ctx, grad):
        (x,) = ctx.saved_tensors
        return grad * (x > 0) * (grad > 0)


class _GuidedReLU(nn.Module):
    def forward(self, x):
        return _GuidedReLUFn.apply(x)


def _guided_copy(model):
    guided = copy.deepcopy(model)
    for module in guided.modules():
        for name, child in module.named_children():
            if isinstance(child, nn.ReLU):
                setattr(module, name, _GuidedReLU())
    return guided


def guided_backprop(model, x):
    return gradient(_guided_copy(model), x)


def integrated_gradients(model, x, steps=32):
    ig = IntegratedGradients(model)
    x = x.to(DEVICE)
    attr = ig.attribute(x, baselines=black_baseline(x.shape).to(DEVICE), target=TARGET,
                        n_steps=steps, internal_batch_size=64)
    return _to_map(attr)


def grad_cam(model, x):
    store = {}
    layer = model.layer4

    def hook(_, __, output):
        output.retain_grad()
        store["act"] = output

    handle = layer.register_forward_hook(hook)
    try:
        x = x.to(DEVICE)
        model(x)[:, TARGET].sum().backward()
    finally:
        handle.remove()
    act = store["act"]
    weights = act.grad.mean(dim=(2, 3), keepdim=True)
    cam = F.relu((weights * act).sum(dim=1, keepdim=True))
    cam = F.interpolate(cam, size=x.shape[-2:], mode="bilinear", align_corners=False)
    return cam[:, 0].detach().cpu().numpy()


METHODS = {
    "Gradient": gradient,
    "Guided Backprop": guided_backprop,
    "Integrated Gradients": integrated_gradients,
    "Grad-CAM": grad_cam,
}


def explain(method, model, x, batch_size=16):
    model.eval()
    maps = []
    for i in range(0, len(x), batch_size):
        model.zero_grad(set_to_none=True)
        maps.append(METHODS[method](model, x[i:i + batch_size]))
    return np.concatenate(maps)


def normalise(maps):
    """Scale each map to [0, 1]; all-zero maps stay zero."""
    flat = maps.reshape(len(maps), -1)
    lo = flat.min(axis=1, keepdims=True)
    hi = flat.max(axis=1, keepdims=True)
    return ((flat - lo) / np.maximum(hi - lo, 1e-12)).reshape(maps.shape)
