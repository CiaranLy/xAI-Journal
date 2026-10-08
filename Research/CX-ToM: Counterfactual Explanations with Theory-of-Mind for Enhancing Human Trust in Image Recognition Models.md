# CX-ToM: Counterfactual Explanations with Theory-of-Mind for Enhancing Human Trust in Image Recognition Models

**Authors:** Arjun R. Akula, Keze Wang, Hongjing Lu (UCLA); Changsong Liu; Sari Saba-Sadiya (Michigan State University); Sinisa Todorovic (Oregon State University); Joyce Chai (University of Michigan); Song-Chun Zhu (BIGAI, Tsinghua University, Peking University)

**Link:** https://arxiv.org/abs/2109.01401 (v2, September 2021)

---

## How it fits our topic

This is not a medical paper. It uses ImageNet, and the paper only mentions clinical use in passing. It is useful because it tests the "do heatmaps actually help?" question from the human side. Instead of checking heatmaps by eye or with a fidelity number, it measures whether people who see an explanation can then **predict what the model will do**.

The headline finding is that attention/saliency maps (CAM, Grad-CAM, SmoothGrad) help people predict the model barely more than no explanation at all. Concept-based and counterfactual explanations do much better.

It makes a good contrast with the other two papers:
- McGonagle et al. judge heatmaps by eye.
- Wen et al. use a loosely defined fidelity score.
- Akula et al. measure human understanding directly.

One caveat: it measures *simulatability* (can a person predict the model?), not *faithfulness* (does the explanation reflect what the model actually computes?). Those are related but not the same.

## What it is

An interactive XAI framework with two parts:

1. **Fault-lines (counterfactual concept explanations).** For an image the model calls class A, a fault-line gives the smallest set of semantic concepts ("xconcepts") to add or remove to make the model say class B instead. For example, to turn a goat into a sheep: add *wool*, remove *beard* and *horns*.
   - **Positive fault-line:** concepts to add.
   - **Negative fault-line:** concepts to remove.
2. **Theory of Mind (ToM).** There are thousands of possible class pairs to explain. The system models what the user currently believes about the model and picks the class pair whose fault-line will help that user most. For example, if the user already trusts that the model recognises people but doubts it can tell man from woman, it explains Woman vs. Man rather than Woman vs. Deer.

The explanation is framed as a **dialogue** over several turns rather than a single heatmap.

## How fault-lines are built

1. **Mine concepts.** Take feature maps from the last conv layer and use **Grad-CAM** to find the most influential superpixels. Cluster them with K-means (number of clusters chosen by silhouette score) so that each cluster is one xconcept.
2. **Find class-specific concepts.** Use **TCAV** (concept activation vectors and directional derivatives) to decide which xconcepts matter for each class.
3. **Optimise the fault-line.** Perturb the *activations* in the last conv layer, not the image, adding concepts of class B and removing concepts of class A until the logits flip. L1 penalties keep the set of concepts small. The problem is solved with FISTA, following the CEM method.
4. **Select with ToM.** A 2-layer LSTM policy, trained by reinforcement learning (actor-critic with experience replay), picks which alternative class to explain next. The reward is positive when the user answers a check question correctly, with fewer dialogue turns rewarded more.

## Data and setup

### Preliminary ToM study (X-ToM game)

- **Task:** a collaborative game on 1,000 images from the Extended Leeds Sports Pose dataset, covering body parts, pose and action recognition.
- **How it works:** the user sees a blurred image and asks the machine questions. The machine reveals relevant regions ("bubbles").
- **Training:** the explainer was trained on Amazon Mechanical Turk with about 2,400 workers.
- **Evaluation:** 120 subjects, between-subject design, 3 groups:
  - answers only (QA)
  - answers + saliency maps
  - ToM explainer

### Main study (fault-lines)

- **Model:** VGG-16 on ImageNet (ILSVRC2012).
- **Classes and concepts:** 80 randomly chosen classes, 57 xconcepts mined.
- **Participants:**
  - 150 non-experts from a psychology subject pool, 12 per group
  - 60 experts with CV/CNN experience, 5 per group
- **Design:** between-subject, 11 groups:
  - no explanation (NO-X)
  - CAM, Grad-CAM, LIME, LRP, SmoothGrad, TCAV, CEM, CVE
  - fault-lines without ToM
  - CX-ToM (fault-lines with ToM)
  - SHAP was added later with 12 extra non-experts.
- **Procedure:**
  - **Familiarisation:** 25 images with the model's predictions and the group's explanations.
  - **Testing:** 8 images. Subjects see the image only and must predict the model's output.
- **ToM policy:** trained on interactions with 15 subjects.
- **Extra studies:** ResNet-50 and PACNet (15 and 18 xconcepts; 4 non-experts and 2 experts per group), a trust-over-time study, and a competency test (AlexNet vs. ResNet-50).

### Metrics

- **Justified trust (JT):** how well users predict the model. It combines the share of correctly classified images the user expects the model to get right with the share of misclassified images the user expects it to get wrong.
- **Explanation satisfaction (ES):** 0–9 Likert ratings of confidence, usefulness, appropriate detail, understandability and sufficiency.
- **X-ToM study only:** justified positive trust, justified negative trust and reliance, computed by comparing graphs of what the user thinks the model detects with what it actually detects.

## Results

### X-ToM game

- ToM explainer beat both baselines on justified positive trust, justified negative trust and reliance (p < 0.01).
- **Saliency maps did no better than giving answers with no explanation.**

### Main study: justified trust (VGG-16)

| Method | Non-experts | Experts |
|---|---|---|
| Random guessing | 6.6% | — |
| No explanation (NO-X) | 21.4% | 28.1% |
| CAM | 24.0% | 37.1% |
| Grad-CAM | 29.2% | 39.1% |
| SmoothGrad | 37.6% | 40.7% |
| LRP | 31.1% | 51.1% |
| SHAP | 40.9% | — |
| LIME | 46.1% | 42.1% |
| TCAV | 49.7% | 55.1% |
| CVE | 50.9% | 64.5% |
| CEM | 51.0% | 61.1% |
| Fault-lines without ToM | 69.1% | 70.5% |
| **CX-ToM** | **72.1%** | **74.5%** |

- The authors report that attention-map methods (CAM, Grad-CAM, SmoothGrad) did not differ significantly from no explanation.
- Concept-based (TCAV) and counterfactual (CEM, CVE) methods did significantly better.
- CX-ToM had the highest explanation-satisfaction ratings on almost every scale. For example, non-expert understandability was 7.7/9, against 4.2 for Grad-CAM.
- Experts preferred LRP over LIME (51.1% vs. 42.1%). Non-experts preferred LIME over LRP (46.1% vs. 31.1%).
- On self-reported trust, Grad-CAM, CAM and SmoothGrad scored *lower* than no explanation.

### Other experiments

- **ResNet-50:** CX-ToM 58.3% / 56.0% (non-expert / expert) vs. Grad-CAM 21.6% / 20.1%. TCAV was the best baseline.
- **PACNet:** CX-ToM 54.8% / 59.8% vs. Grad-CAM 15.2% / 16.8%.
- **Over time:** justified trust rose fastest with CX-ToM and stopped improving for all groups after about 5 sessions. Grad-CAM and CAM gave no significant gain over time.
- **Competency test (which model is more reliable, AlexNet or ResNet-50?):**
  - CX-ToM users picked ResNet-50 with confidence 7.7/9.
  - Grad-CAM (2.6), TCAV (4.9) and CEM (4.2) users also picked it, but with low confidence.
  - The other groups failed to identify it.
- **Response time:** no significant difference between groups.
- **Compute (one RTX 2080 Ti):**
  - Grad-CAM superpixel extraction: ~17 h
  - Clustering: ~3 h
  - TCAV: ~15 h, plus ~2 h for directional derivatives
  - Fault-line optimisation: ~40 s per image

## Weaknesses (useful for our review)

- **Measures understanding, not faithfulness.** Higher justified trust shows people can predict the model better. It doesn't show the explanation reflects the model's actual computation. No deletion/insertion tests or other faithfulness checks are run on the fault-lines themselves.
- **Manual curation.** In a footnote, the authors say they manually removed noisy xconcepts and fault-lines because they couldn't find an automatic filter. This means the explanations users saw were hand-picked, which favours CX-ToM against baselines shown uncurated.
- **Built on Grad-CAM.** The concepts are mined using Grad-CAM, the same attention method the paper argues is not a good explanation.
- **Counterfactuals are in activation space.** Concepts are added or removed by editing conv-layer activations, not images. The authors say producing realistic images was not the goal. So users never see what the "changed" image would look like, and there is no check that the edited activations correspond to anything real.
- **Small groups.**
  - Main study: 12 non-experts and 5 experts per group, with only 8 test images per person.
  - ResNet-50 and PACNet: 4 and 2 per group.
  - Several standard deviations are very large for a 0–9 scale (e.g., LRP confidence 3.2 ± 4.1).
- **ToM adds little over fault-lines alone.** On VGG-16, the ToM policy adds about 3–4 points (69.1% → 72.1%; 70.5% → 74.5%). Most of the gain comes from the fault-line format.
- **Group numbers don't add up.**
  - 150 non-experts split into 11 groups of 12 is 132.
  - 60 experts split into 11 groups of 5 is 55.
- **Generalises from NLP evidence.** The paper's "attention is not explanation" framing leans on Jain & Wallace (2019), which studied attention weights in NLP models, not saliency maps in vision.
- **Not medical.** It uses ImageNet animals and objects, with no clinicians or medical images, so transfer to radiology is untested.
- **Code availability.** The paper says data and code "will be made publicly available"; no link is given.
