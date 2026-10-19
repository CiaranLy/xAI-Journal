"""Localisation and deletion tests for the saliency maps.

Localisation: do the maps put their mass on the annotated tumour? We score the
trained model, the fully randomised model, and a Sobel edge map of the input
that uses no model at all. If the randomised model or the edge map localise
the tumour too, then overlap with the tumour cannot be evidence that a map is
faithful to the trained model.

Deletion: black out the top-k% most salient pixels (or 16x16 patches) and
measure how much the trained model's tumour probability drops, against
deleting random brain pixels (or patches) and against deleting the annotated
tumour itself. Scattered single-pixel deletion pushes inputs off the training
distribution (Hooker et al., 2019), so the patch version is the fairer test.
"""
import copy
import os

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from skimage.filters import sobel

from common import DEVICE, IMAGENET_MEAN, IMAGENET_STD, RESULTS_DIR, black_baseline, load_trained_model
from explainers import METHODS, explain
from sanity import STAGES, randomise, test_images

DELETE_FRACTIONS = [0.01, 0.02, 0.05, 0.10, 0.20]
DELETE_PATCH_SIZES = [1, 16]  # per-pixel deletion, and contiguous 16x16 patches


def edge_maps(x_raw):
    """Model-free control: Sobel edges of the FLAIR channel."""
    return np.stack([sobel(img[..., 1].astype(float)) for img in x_raw])


def localisation(maps, masks):
    flat_maps = maps.reshape(len(maps), -1)
    flat_masks = masks.reshape(len(masks), -1)
    peak_inside = flat_masks[np.arange(len(maps)), flat_maps.argmax(axis=1)]
    mass = flat_maps.sum(axis=1)
    mass_inside = np.where(mass > 0, (flat_maps * flat_masks).sum(axis=1) / np.maximum(mass, 1e-12), 0.0)
    return {
        "pointing_game": float(peak_inside.mean()),
        "mass_in_tumour": float(mass_inside.mean()),
        "tumour_area_frac": float(flat_masks.mean(axis=1).mean()),
    }


@torch.no_grad()
def tumour_prob(model, x):
    return torch.cat([F.softmax(model(x[i:i + 128].to(DEVICE)), 1)[:, 1].cpu()
                      for i in range(0, len(x), 128)]).numpy()


def delete(x, remove):
    """Set pixels where `remove` (N, H, W) is True to black."""
    remove = torch.as_tensor(remove, dtype=torch.float32).unsqueeze(1)
    return x * (1 - remove) + black_baseline((1, 3, 1, 1)) * remove


def delete_top(x, scores, frac, patch=1):
    """Black out the top-`frac` of each image, ranked per pixel or per `patch` x `patch` square
    by mean score."""
    n, _, h, w = x.shape
    pooled = F.avg_pool2d(torch.from_numpy(scores.astype(np.float32)).unsqueeze(1), patch)
    flat = pooled.view(n, -1)
    remove = torch.zeros_like(flat)
    remove.scatter_(1, flat.topk(max(1, int(round(frac * flat.shape[1]))), dim=1).indices, 1.0)
    remove = F.interpolate(remove.view(pooled.shape), scale_factor=patch, mode="nearest")
    return delete(x, remove[:, 0])


def random_scores(brain, patch, rng):
    """Control ordering: random scores per pixel or patch, restricted to the brain."""
    n, h, w = brain.shape
    in_brain = F.avg_pool2d(torch.from_numpy(brain.astype(np.float32)).unsqueeze(1), patch)[:, 0].numpy() > 0.5
    r = np.where(in_brain, rng.random(in_brain.shape), -1.0)
    return r.repeat(patch, axis=1).repeat(patch, axis=2)


def main():
    x, masks, _ = test_images()
    x_raw = np.clip((x * IMAGENET_STD + IMAGENET_MEAN).permute(0, 2, 3, 1).numpy(), 0, 1)
    trained = load_trained_model()
    randomised = copy.deepcopy(trained)
    torch.manual_seed(0)
    for _, modules in STAGES:
        randomise(randomised, modules)
    randomised.eval()

    trained_maps = {m: explain(m, trained, x) for m in METHODS}
    edges = edge_maps(x_raw)

    loc_rows = [{"method": "Edge detector (no model)", "model": "none", **localisation(edges, masks)}]
    for method in METHODS:
        loc_rows.append({"method": method, "model": "trained", **localisation(trained_maps[method], masks)})
        loc_rows.append({"method": method, "model": "fully randomised",
                         **localisation(explain(method, randomised, x), masks)})
    loc = pd.DataFrame(loc_rows).round(3)
    loc.to_csv(os.path.join(RESULTS_DIR, "localisation.csv"), index=False)
    print(loc.to_string(index=False))

    rng = np.random.default_rng(0)
    brain = x_raw.max(axis=-1) > 0.02
    base = tumour_prob(trained, x)
    del_rows = []
    for patch in DELETE_PATCH_SIZES:
        orderings = {**trained_maps,
                     "Edge detector (no model)": edges,
                     "Random brain region": random_scores(brain, patch, rng)}
        for name, scores in orderings.items():
            for frac in DELETE_FRACTIONS:
                p = tumour_prob(trained, delete_top(x, scores, frac, patch))
                del_rows.append({"patch": patch, "ordering": name, "fraction": frac, "mean_prob": float(p.mean()),
                                 "mean_drop": float((base - p).mean()), "frac_flipped": float((p < 0.5).mean())})
    p_mask = tumour_prob(trained, delete(x, masks))
    del_rows.append({"patch": 0, "ordering": "Annotated tumour", "fraction": float(masks.mean()),
                     "mean_prob": float(p_mask.mean()),
                     "mean_drop": float((base - p_mask).mean()), "frac_flipped": float((p_mask < 0.5).mean())})
    dele = pd.DataFrame(del_rows).round(3)
    dele.to_csv(os.path.join(RESULTS_DIR, "deletion.csv"), index=False)
    print(f"baseline mean tumour prob: {base.mean():.3f}")
    print(dele.to_string(index=False))


if __name__ == "__main__":
    main()
