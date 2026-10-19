"""Cascading model-parameter randomisation test (Adebayo et al., 2018).

Starting from the trained classifier, re-initialise the network from the
logits downwards, one stage at a time, and compare each method's saliency
map on the randomised model with its map on the trained model. A method
whose maps stay similar after the weights are destroyed is not explaining
what the model learned.
"""
import copy
import os

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from scipy.stats import spearmanr
from skimage.metrics import structural_similarity

from common import DEVICE, RESULTS_DIR, RUN_DIR, load_patients, load_trained_model, patient_split, to_tensor
from explainers import METHODS, explain, normalise

STAGES = [
    ("Logits", ["fc"]),
    ("Layer 4", ["layer4"]),
    ("Layer 3", ["layer3"]),
    ("Layer 2", ["layer2"]),
    ("Layer 1", ["layer1"]),
    ("Conv 1", ["conv1", "bn1"]),
]
SEEDS = [0, 1, 2]


def randomise(model, module_names):
    """Re-initialise every parameter (and batch-norm running statistic) in the named modules."""
    for name in module_names:
        for module in model.get_submodule(name).modules():
            if hasattr(module, "reset_parameters"):
                module.reset_parameters()


def similarity(original, randomised):
    """Per-image Spearman rank correlation and SSIM between two stacks of maps."""
    rows = []
    a_norm, b_norm = normalise(original), normalise(randomised)
    for a, b, an, bn in zip(original, randomised, a_norm, b_norm):
        constant = np.ptp(b) == 0 or np.ptp(a) == 0
        rho = 0.0 if constant else spearmanr(a.ravel(), b.ravel())[0]
        rows.append({"spearman": rho, "ssim": structural_similarity(an, bn, data_range=1.0),
                     "constant_map": constant})
    return rows


def test_images():
    """Tumour-positive test slices that the trained model classifies correctly."""
    images, masks, labels, names = load_patients(patient_split()["test"])
    x = to_tensor(images)
    model = load_trained_model()
    with torch.no_grad():
        probs = torch.cat([F.softmax(model(x[i:i + 128].to(DEVICE)), 1)[:, 1].cpu()
                           for i in range(0, len(x), 128)]).numpy()
    keep = (labels == 1) & (probs >= 0.5)
    return x[keep], masks[keep], [n for n, k in zip(names, keep) if k]


def main():
    x, _, names = test_images()
    print(f"{len(x)} correctly classified tumour slices")
    trained = load_trained_model()
    original = {m: explain(m, trained, x) for m in METHODS}
    np.savez_compressed(os.path.join(RUN_DIR, "maps_trained.npz"), names=names, **original)

    rows, preds = [], []
    example_maps = {m: {"Trained": original[m][:4]} for m in METHODS}
    for seed in SEEDS:
        torch.manual_seed(seed)
        model = copy.deepcopy(trained)
        for stage, modules in STAGES:
            randomise(model, modules)
            model.eval()
            with torch.no_grad():
                p = torch.cat([F.softmax(model(x[i:i + 128].to(DEVICE)), 1)[:, 1].cpu()
                               for i in range(0, len(x), 128)]).numpy()
            preds.append({"seed": seed, "stage": stage, "frac_predicted_tumour": float((p >= 0.5).mean()),
                          "mean_tumour_prob": float(p.mean())})
            for method in METHODS:
                maps = explain(method, model, x)
                if seed == 0:
                    example_maps[method][stage] = maps[:4]
                for i, r in enumerate(similarity(original[method], maps)):
                    rows.append({"seed": seed, "stage": stage, "method": method, "image": names[i], **r})
            print(f"seed {seed} {stage} done")

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RESULTS_DIR, "sanity_randomisation.csv"), index=False)
    pd.DataFrame(preds).to_csv(os.path.join(RESULTS_DIR, "sanity_predictions.csv"), index=False)
    np.savez_compressed(os.path.join(RUN_DIR, "maps_examples.npz"),
                        images=x[:4].numpy(), names=names[:4],
                        **{f"{m}|{s}": v for m, d in example_maps.items() for s, v in d.items()})
    summary = (df.groupby(["method", "stage"], sort=False)[["spearman", "ssim", "constant_map"]]
               .agg(["mean", "std"]).round(3))
    print(summary)
    summary.to_csv(os.path.join(RESULTS_DIR, "sanity_summary.csv"))


if __name__ == "__main__":
    main()
