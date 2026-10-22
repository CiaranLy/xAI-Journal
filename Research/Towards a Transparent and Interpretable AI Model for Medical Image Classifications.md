# Towards a Transparent and Interpretable AI Model for Medical Image Classifications

**Authors:** Binbin Wen, Yihang Wu, Ahmad Chaddad (Guilin University of Electronic Technology; Chaddad also at ÉTS Montréal), Tareef Daqqaq (Taibah University / Prince Mohammed Bin Abdulaziz Hospital, Madinah)

**Link:** https://arxiv.org/abs/2509.16685

---

## How it fits our topic

This is a broad survey of XAI in medicine with a small benchmark attached. It runs three post-hoc methods across five datasets and four CNNs. Unlike most papers of this kind, it tries to add a number (a "fidelity score") rather than relying only on looking at heatmaps. However, the metric is so loosely defined that it doesn't settle whether the heatmaps reflect what the model actually uses.

That makes it a useful counterpoint to McGonagle et al.: wide (many datasets) where they are deep (one dataset, combined methods), but with the same core weakness.

## What it is

The paper has two parts.

1. **Survey.** It sorts XAI methods along three axes: ante-hoc vs. post-hoc, global vs. local, and model-specific vs. model-agnostic. It reviews nine techniques: decision trees, Grad-CAM, activation maximization, KNN, SHAP, LIME, saliency maps, ICE and LRP. It also covers:
   - human-centred XAI (different explanations for developers, clinicians and lay users)
   - XAI in computer-aided diagnosis and EHRs
   - a table of 2023 studies
   - open challenges
2. **Experiments.** Four standard CNNs are trained on five public medical image datasets. Their predictions are then explained with Integrated Gradients (IG), Grad-CAM and SHAP.

## Data and setup

### Datasets (all public Kaggle sets)

| Dataset | Modality | Classes | Images (train / val / test) |
|---|---|---|---|
| Brain tumour | MRI | Glioma, meningioma, pituitary, no tumour | 7,022 (4,571 / 1,141 / 1,311) |
| Lung cancer | Chest CT | Adenocarcinoma, large cell, squamous cell, normal | 1,000 (581 / 94 / 315) |
| Colon disease | Capsule endoscopy | Normal, ulcerative colitis, polyps, oesophagitis | 6,000 (4,160 / 1,040 / 800) |
| Eye disease | Retinal images | Cataract, diabetic retinopathy, glaucoma, normal | 4,217 (2,698 / 673 / 846) |
| COVID-19 | Described as CT | COVID-19, normal, pneumonia | 6,432 (4,116 / 1,028 / 1,288) |

### Splits

- **Brain tumour and COVID-19:** 20% of the training set held out as validation.
- **Lung cancer and colon disease:** original validation sets merged into training, then 20% re-split off.
- **Eye disease:** split 70 / 10 / 20.
- Splits are by image. **No patient-level split is mentioned.**

### Models and training

- **Models:** ResNet50, DenseNet121, EfficientNetB3, EfficientNetB0
- **Loss:** cross-entropy
- **Optimiser:** Adam, learning rate 0.001
- **Batch size:** 32
- **Epochs:** 100
- **Hardware:** RTX 4090
- Not stated whether the models were pretrained.

## Results

### Best accuracy per dataset

| Dataset | Best model | Accuracy | Weakest model |
|---|---|---|---|
| Brain tumour | EfficientNetB0 | 98.78% | ResNet50 (96.57%) |
| Lung cancer | EfficientNetB3 | 88.25% | ResNet50 (78.73%) |
| Colon disease | DenseNet121 | 99.62% | ResNet50 (99.00%) |
| Eye disease | EfficientNetB0 | 93.62% | DenseNet121 (89.72%) |
| COVID-19 | EfficientNetB3 | 94.41% | ResNet50 (91.85%) |

The authors blame the weak lung results on the small, imbalanced dataset.

### Explanations (judged by eye)

- IG and SHAP usually agreed and highlighted the lesion, for example a meningioma.
- Grad-CAM often marked regions that were too large or too scattered, especially on lung CT and eye images.
- On the "easy" colon dataset, all three methods mostly agreed.
- The authors claim explanation quality tracks model accuracy: tight, focused maps on high-accuracy datasets and diffuse, unreliable ones on lung cancer.

### Quantitative analysis

| | Grad-CAM | IG | SHAP |
|---|---|---|---|
| Time per image (ResNet50) | ~0.04 s | Fast (similar to Grad-CAM) | ~5.5 s |
| Fidelity | Most stable across models | Moderate | Varies by model; highest on COVID-19 with EfficientNets (> 0.856) |

**Conclusion:** Grad-CAM and IG give workable interpretability at low cost, which suits low-resource devices.

## The "fidelity score" (main quantitative contribution)

The score compares the model's top-class confidence on the original image with its confidence after an adversarial perturbation:

$$F = \frac{C_a}{C_o}, \quad 0 \le F \le 1$$

- **C_o:** original confidence
- **C_a:** adversarial confidence

A score near 1 is meant to show that the explanation is faithful and robust.

## Weaknesses (useful for our review)

- **The fidelity score doesn't clearly test the explanation.**
  - As described, it measures how much the model's confidence drops under perturbation. The paper never says how the explanation is used: does the perturbation target the highlighted pixels?
  - It never specifies the attack or its strength.
  - The printed formula even reads C_a / C_a, presumably a typo.
  - It is therefore not equivalent to deletion/insertion tests or pointing-game scores.
  - There is also an internal tension: Grad-CAM looks worst by eye yet scores most stable on fidelity, which suggests the metric isn't capturing localisation quality.
- **Visual judgement only for localisation.** Some datasets have masks or bounding regions available, but there is no overlap with lesion masks, no clinician rating and no user study. The authors acknowledge that applying user-centred and other evaluation approaches was beyond the paper's scope.
- **"Accuracy correlates with explanation quality" is asserted, not measured.** No statistic backs it, only example images.
- **Possible data leakage.** Splits are by image on Kaggle datasets, with no patient-level separation stated. This may inflate the near-perfect scores, such as 99.6% on colon. There is also no external validation.
- **The survey and experiments don't line up.** The survey reviews nine methods, but the experiments use IG, which isn't among them, and skip LIME and LRP, which are.
- **Inconsistencies:**
  - The COVID-19 EfficientNetB3 F1 (95.52) is higher than both its precision (94.93) and recall (94.41), which is mathematically impossible.
  - The text says EfficientNetB3 was best on colon, but the table shows DenseNet121 was.
  - The COVID-19 data is called CT, but the cited dataset is chest X-ray.
  - The brain tumour reference is titled as a chest CT dataset.
  - The Grad-CAM weight equation (Eq. 1) is non-standard and looks garbled.
- **Overstated conclusion.** The paper says the work "validates the potential of XAI to enhance diagnostic accuracy." The XAI methods here explain predictions; they don't change accuracy.
