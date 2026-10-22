# Explainable AI: A Combined XAI Framework for Explaining Brain Tumour Detection Models

**Authors:** Patrick McGonagle, William Farrelly (Atlantic Technological University, Donegal), Kevin Curran (Ulster University)

**Link:** https://arxiv.org/abs/2602.05240

## How it fits our topic

A typical example of the post-hoc saliency-map approach in medical imaging: it combines several methods to make the explanation stronger, but only checks them by eye. It is a good case study for the question "do the heatmaps actually show what the AI is using, or do they just look convincing?"

## What it is

A custom CNN that classifies 2D brain MRI slices as tumour or no tumour. It is explained with **three post-hoc methods used together: Grad-CAM, LRP and SHAP.**

## Data and setup

- **Data:** BraTS 2021, FLAIR sequences only.
- **Slicing:** 3D volumes were cut into 2D slices, taking every 5th slice in each view. A slice counts as "tumour" if its mask has any tumour pixel.
- **Preprocessing:**
  - Slices without much brain tissue were removed.
  - Images were normalised to 0–1 and centre-cropped to 200×200.
  - Data was split 70/15/15 **by patient**, so no patient appears in more than one set.
  - Classes were balanced to 12,313 slices each (24,626 total).
- **Model:** 4 convolutional layers with growing kernel sizes (3×3 up to 9×9), max pooling, dense layers, dropout 0.5 and a sigmoid output. Trained with Adam and a learning rate scheduler; batch size 64.

## Results

Improved model compared with the baseline it builds on (Hafeez et al. 2023):

| Metric | Baseline | Improved |
|---|---|---|
| Accuracy | 84.76% | **91.24%** |
| Test loss | 0.3482 | 0.2355 |
| Precision | 0.919 | 0.961 |
| Recall | 0.762 | 0.862 |
| F1 | 0.833 | 0.909 |
| AUC | 0.92 | 0.96 |

**Error analysis:**
- **False negatives (376):** about one third came from poor image quality (blur, low contrast, motion artefacts); the rest were partial tumours that were barely visible.
- **False positives (~97):** about 39% came from poor image quality; about 61% were non-tumour abnormalities that look like tumours.

## How the three methods fit together (the main contribution)

| Method | Role |
|---|---|
| **Grad-CAM** (last conv layer) | Coarse view of *where* the model is looking. Focused on tumour slices, spread out on healthy slices. |
| **LRP** | Pixel-level detail inside that region. |
| **SHAP** | Puts numbers on it, e.g. 68.75% of SHAP values pushed towards "tumour" on a positive slice, and 86.27% pushed against it on a negative one. |

**Partial tumours** were the most interesting cases:
- Where Grad-CAM was spread out, LRP still pointed to the tumour.
- In one borderline case (predicted probability 0.507), all three methods showed the model was unsure. The authors use this to argue that combining methods exposes uncertainty that one method alone would miss.

The authors stress that the explanations should support clinicians, not replace them.

## Weaknesses (useful for our review)

- The explanations are judged **only by looking at example images**. There are no faithfulness metrics (such as deletion/insertion tests or pointing-game scores), no overlap with the segmentation masks, and no clinicians rating them. This is exactly the gap that [Self-eXplainable AI for Medical Image Analysis](Self-eXplainable%20AI%20for%20Medical%20Image%20Analysis.md) criticises in post-hoc methods.
- It uses 2D slices from a single sequence (FLAIR) and a single dataset, with no external validation.
- The authors say the loss is still high and that validation loss suggests mild overfitting.
- A few numbers don't match within the paper: false positives are given as 96 and as 97, and the false-negative breakdown appears as 123/376 and later as "44% of a 100-sample".
