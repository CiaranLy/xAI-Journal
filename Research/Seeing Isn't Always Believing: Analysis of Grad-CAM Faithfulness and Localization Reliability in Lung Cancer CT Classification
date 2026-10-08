# Seeing Isn't Always Believing: Analysis of Grad-CAM Faithfulness and Localization Reliability in Lung Cancer CT Classification

**Author:** Teerapong Panboonyuen (Chulalongkorn University)

**Link:** https://arxiv.org/abs/2601.12826 (v1, January 2026)

---

## How it fits our topic

I picked this because it separates two parts of our topic: whether a model gets the diagnosis right, and whether its heatmap gives a reliable explanation. It is useful as a case study of how explanations are tested, although I would be cautious about relying on its conclusions.

It adds another comparison to the papers already collected:
- McGonagle et al. combine explanation methods and judge example images.
- Wen et al. include a fidelity score whose meaning needs closer checking.
- This paper proposes three explanation measures, but does not clearly report their numerical results.

For me, the useful question is whether the evidence supplied actually supports the claim about explanation quality.

## What it is

A Grad-CAM comparison across five lung CT classifiers. Grad-CAM uses gradients to weight feature maps and produce a heatmap for a class.

## Data and setup

- **Dataset:** IQ-OTH/NCCD; 1,190 slices, 110 patients.
- **Classes:** normal, benign, malignant.
- **Split:** 60/20/20 training/validation/test.
- **Preprocessing:** 224 × 224 resizing and intensity normalisation.
- **Training:** 50 epochs.

## How the explanation checks work

| Proposed check | Measurement |
|---|---|
| Tumour coverage | Overlap with annotated tumour regions |
| Effect on predictions | Score change after masking highlighted pixels |
| Stability | Heatmap overlap across random initialisations |

Section II-C defines these checks. **Tumour coverage and faithfulness are different:** highlighting the expected area does not establish how much the prediction depends on it.

## Results

### Classification performance

Table I reports:

| Model | Accuracy | F1 |
|---|---|---|
| ResNet-50 | 85% | 0.79 |
| ResNet-101 | 87% | 0.83 |
| DenseNet-161 | 88% | 0.85 |
| EfficientNet-B0 | 83% | 0.78 |
| ViT-Base-Patch16-224 | 89% | 0.86 |

### Heatmap examples

The descriptions in section V vary by model:

| Model family | What the author describes |
|---|---|
| ResNet | Broad or scattered highlights |
| DenseNet | Highlights near image edges |
| EfficientNet | Inconsistent tumour localisation |
| ViT | Mostly precise examples, with occasional errors |

**The classification table does not rank explanation quality.** I would want to compare the effect of removing highlighted pixels with removing an equally sized control region before treating a heatmap as reliable.

## Weaknesses

- **The account of ViT is difficult to follow.** The abstract criticises its faithfulness, while sections IV–V praise its localisation. These are different properties, so both could be true, but the numerical evidence needed to explain the distinction is missing.
- **Proposed measures are not clearly backed by results.** The paper defines three explanation checks without clearly reporting their scores. I would keep the proposed evaluation separate from what was actually demonstrated.
- **Patient separation is unclear.** The split does not say whether all slices from one patient stay in the same set. Similar slices in training and testing could make the test easier. This is a concern to check, not proof of leakage.
- **No external validation is reported.** I would want testing on a separate dataset before applying the conclusions more broadly.
- **Localisation is not the whole explanation.** A heatmap lining up with a tumour does not by itself establish that it accurately describes the model's decision. Equally, an unexpected highlight needs further testing before it is called a shortcut.

These notes refer to arXiv v1. I would use the paper to discuss gaps in evaluation, rather than as our main evidence that one model produces better explanations.
