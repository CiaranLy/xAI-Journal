"""Shared data loading, model construction and paths for the sanity-check experiment."""
import glob
import json
import os

import numpy as np
import torch
import torch.nn as nn
from skimage import io
from torchvision import models

DATA_ROOT = os.environ.get(
    "LGG_ROOT",
    os.path.expanduser(
        "~/data/kagglehub/datasets/mateuszbuda/lgg-mri-segmentation/versions/2/kaggle_3m"
    ),
)
RUN_DIR = os.environ.get("RUN_DIR", os.path.expanduser("~/data/xai-runs"))
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
CHECKPOINT = os.path.join(RUN_DIR, "resnet18_lgg.pt")
SPLIT_FILE = os.path.join(RESULTS_DIR, "split.json")

SEED = 0
IMAGENET_MEAN = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
IMAGENET_STD = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def patient_split(seed=SEED, frac=(0.70, 0.15, 0.15)):
    """Split patient folders into train/val/test so no patient spans two sets."""
    if os.path.exists(SPLIT_FILE):
        with open(SPLIT_FILE) as f:
            return json.load(f)
    patients = sorted(os.path.basename(p) for p in glob.glob(os.path.join(DATA_ROOT, "*")) if os.path.isdir(p))
    rng = np.random.default_rng(seed)
    rng.shuffle(patients)
    n_train = round(frac[0] * len(patients))
    n_val = round(frac[1] * len(patients))
    split = {
        "train": sorted(patients[:n_train]),
        "val": sorted(patients[n_train:n_train + n_val]),
        "test": sorted(patients[n_train + n_val:]),
    }
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(SPLIT_FILE, "w") as f:
        json.dump(split, f, indent=2)
    return split


def load_patients(patients):
    """Load every slice for the given patients.

    Returns uint8 images (N, 256, 256, 3), boolean masks (N, 256, 256),
    labels (1 = any tumour pixel in the mask) and the slice file names.
    """
    images, masks, names = [], [], []
    for patient in patients:
        for mask_path in sorted(glob.glob(os.path.join(DATA_ROOT, patient, "*_mask.tif"))):
            images.append(io.imread(mask_path.replace("_mask.tif", ".tif")))
            masks.append(io.imread(mask_path) > 0)
            names.append(os.path.basename(mask_path).replace("_mask.tif", ""))
    images = np.stack(images)
    masks = np.stack(masks)
    labels = masks.reshape(len(masks), -1).any(axis=1).astype(np.int64)
    return images, masks, labels, names


def to_tensor(images):
    """uint8 (N, H, W, 3) -> ImageNet-normalised float tensor (N, 3, H, W)."""
    x = torch.from_numpy(images).permute(0, 3, 1, 2).float() / 255.0
    return (x - IMAGENET_MEAN) / IMAGENET_STD


def to_raw(x):
    """Normalised tensor (N, 3, H, W) -> float image in [0, 1], (N, H, W, 3)."""
    return np.clip((x * IMAGENET_STD + IMAGENET_MEAN).permute(0, 2, 3, 1).numpy(), 0, 1)


def brain_mask(x):
    """Pixels that are not black background."""
    return to_raw(x).max(axis=-1) > 0.02


def black_baseline(shape):
    """A normalised all-black image, the background value of these MRI slices."""
    return ((torch.zeros(shape) - IMAGENET_MEAN) / IMAGENET_STD).expand(shape).clone()


def build_model(pretrained=True):
    weights = models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None
    model = models.resnet18(weights=weights)
    model.fc = nn.Linear(model.fc.in_features, 2)
    return model


def load_trained_model():
    model = build_model(pretrained=False)
    model.load_state_dict(torch.load(CHECKPOINT, map_location="cpu"))
    return model.to(DEVICE).eval()
