# Saliency sanity checks on brain MRI

Supporting experiment for the paper (issues #5 and #6). It asks whether four common saliency methods on a medical imaging classifier
(1) depend on what the model learned, (2) highlight the tumour, and (3) point at pixels the model actually relies on.

## Setup

```bash
python3 -m venv ~/.venvs/xai
~/.venvs/xai/bin/pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
~/.venvs/xai/bin/pip install -r requirements.txt
```

The dataset ([LGG MRI Segmentation](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation), Buda et al. 2019)
downloads without a Kaggle account:

```bash
~/.venvs/xai/bin/python -c "import kagglehub; print(kagglehub.dataset_download('mateuszbuda/lgg-mri-segmentation'))"
```

Data and checkpoints live outside the repo (`~/data`). Override the paths with `LGG_ROOT` and `RUN_DIR` if needed.

## Run

```bash
cd experiment
~/.venvs/xai/bin/python train.py         # ~5 min on an RTX 4060 Ti
~/.venvs/xai/bin/python sanity.py        # cascading randomisation
~/.venvs/xai/bin/python localisation.py  # tumour overlap + deletion
~/.venvs/xai/bin/python figures.py
```

## Design

| Component | Choice |
|---|---|
| Data | 110 patients, 3,929 slices (pre-contrast / FLAIR / post-contrast as RGB, 256×256). A slice is "tumour" if its mask has any tumour pixel. |
| Split | By patient, 77 / 16 / 17 (`results/split.json`), so no patient appears in more than one set |
| Model | ImageNet ResNet-18, 2-class head, 12 epochs Adam 1e-4, class-weighted CE, flip + shift augmentation; best val AUC kept |
| Explained slices | The 169 test tumour slices that the model classifies correctly |
| Methods | Gradient, Guided Backprop, Integrated Gradients (32 steps, black baseline), Grad-CAM (`layer4`); all explain the tumour logit |
| Randomisation | Cascading re-initialisation from `fc` down to `conv1`/`bn1` (PyTorch default init, batch-norm statistics reset), 3 seeds. Similarity to the trained model's maps measured with Spearman rank correlation (absolute maps) and SSIM (maps scaled to [0, 1]) |
| Localisation | Pointing game (is the peak inside the mask?) and the share of map mass inside the mask. Compared across the trained model, the fully randomised model, and two model-free maps (Sobel edges of FLAIR; raw input intensity) |
| Deletion | Black out the top 1–20% of pixels, or of 16×16 patches, and measure the drop in tumour probability. Controls: random brain pixels/patches, and the annotated tumour itself |

## Results

**Classifier** (17 unseen test patients, 674 slices): accuracy 0.942, AUC 0.976, sensitivity 0.837, specificity 0.987.

**1. Cascading randomisation** (`results/sanity_*.csv`, 169 slices × 3 seeds). Brain-pixel Spearman correlation with the trained model's maps:

| Randomised down to | Gradient | Guided Backprop | Integrated Gradients | Grad-CAM |
|---|---|---|---|---|
| Logits | 0.48 | **0.99** | 0.75 | 0.29 |
| Layer 4 | 0.16 | 0.76 | 0.61 | 0.12 |
| Layer 2 | 0.09 | 0.39 | 0.56 | −0.01 |
| Conv 1 (whole network) | 0.01 | 0.12 | **0.54** | −0.13 |

- Gradient and Grad-CAM pass: their maps lose their structure once the top layers are randomised.
- Guided Backprop is almost unchanged when the output layer is randomised (0.99), so it is insensitive to the class the model learned, matching Adebayo et al.
- Integrated Gradients keeps 0.54 correlation with a **fully random network**. Its maps correlate about 0.67 with raw input brightness for both the trained (0.66) and the random (0.67) model, so a large share of each IG map reflects the image, not the model.
- Whole-image Spearman overstates IG's similarity (0.82 vs 0.54), because IG is exactly zero on the black background for any model. Similarity metrics need to exclude regions where the method is fixed by construction.

**2. Localisation** (`results/localisation.csv`). The tumour covers on average 2.8% of a slice.

| Map | Pointing game | Mass in tumour |
|---|---|---|
| Integrated Gradients, trained | 0.91 | 0.24 |
| Gradient, trained | 0.73 | 0.13 |
| Grad-CAM, trained | 0.56 | 0.13 |
| Guided Backprop, trained | 0.47 | 0.23 |
| Any method, fully randomised | ≤ 0.012 | 0.02–0.07 |
| Edge detector / input intensity (no model) | 0.012 / 0.000 | 0.03 / 0.07 |

The best-localising method (IG) is also the one that fails the randomisation test most clearly. Agreeing with the annotated tumour and depending on the model are separate properties, and each needs its own test.

**3. Deletion** (`results/deletion.csv`, baseline tumour probability 0.967)

| Deleted | Mean drop in tumour prob. | Predictions flipped |
|---|---|---|
| Top 1% **pixels** (Gradient, Guided Backprop, IG) | 0.83–0.86 | 93–96% |
| 1% **random** brain pixels | 0.83 | 89% |
| Top 1% of **16×16 patches** by saliency | 0.37–0.49 | 42–56% |
| 1% random brain patches | 0.04 | 5% |
| Annotated tumour (2.8% of pixels) | 0.81 | 89% |

Pixel-level deletion cannot tell a saliency method from random: scattered black pixels break the model whatever chooses them (the out-of-distribution problem identified by Hooker et al.). Deleting contiguous patches shows that every method's top regions matter far more than random regions.

**Figures:** `results/figures/randomisation_curves.pdf` and `results/figures/example_maps.pdf` are sized for one IEEE column.

## Limitations

- One dataset, one architecture (ResNet-18), one training run; the 169 explained slices come from 17 patients.
- Deletion uses black replacement; other replacements (blur, inpainting, retraining as in ROAR) could change the size of the effects.
- Batch-norm statistics are reset during randomisation, so the randomised networks' activations differ in scale as well as in weights.
- Integrated Gradients is evaluated with a single (black) baseline; its dependence on input brightness is partly a consequence of that choice.
