# Topic 2 Viability Assessment: LIME/SHAP Disagreement

**Verdict: viable as a short paper, but the thesis needs rewording and the experiment
needs one addition or a reviewer kills it in a sentence.**

The core problem: the experiment as described has already been run and published.
Krishna et al. (2022), "The Disagreement Problem in Explainable Machine Learning: A
Practitioner's Perspective," is exactly this study — six methods (LIME, KernelSHAP,
Vanilla Gradient, Gradient x Input, Integrated Gradients, SmoothGrad), four datasets
(COMPAS, German Credit, AG News, ImageNet), eight models, six formal disagreement
metrics. It is the canonical reference and has been cited heavily since.

So this cannot be framed as a new finding. It can be framed as a replication with a
sharpened claim, which is a legitimate short-paper shape — but the framing has to be
honest from the first paragraph.

---

## 1. Prior art you must engage with

### Krishna et al. 2022 — arXiv:2202.01602
Defines the six metrics that are now standard. Use these rather than inventing your own:

| Metric | Definition |
|---|---|
| Feature agreement | fraction of shared features in the top-k |
| Rank agreement | shared top-k features at the *same* rank position |
| Sign agreement | shared top-k features with the same attribution sign |
| Signed rank agreement | same rank *and* same sign |
| Rank correlation | Spearman's rho over the ranked feature set |
| Pairwise rank agreement | fraction of feature pairs whose relative order matches |

Reported results (verify these numbers against the PDF yourself before citing — I read
them from an HTML conversion): on tabular data at k=5, feature agreement roughly
0.4–0.7 and rank agreement often below 0.4; text far worse (rank agreement <0.1);
images much better (LIME/KernelSHAP over superpixels, rank correlation ~0.90).
Their practitioner survey: 84% had hit disagreement in practice, 86% resolved it with
ad hoc heuristics, and KernelSHAP was picked ~67% of the time when methods conflicted
— largely on reputation rather than on any property of the output.

That survey finding is the most useful thing in the paper for your discussion section.

### Han, Srinivas & Lakkaraju 2022 (NeurIPS) — arXiv:2206.01254
**This is the paper that will be used against your thesis, so read it first.** It
unifies eight methods including LIME and KernelSHAP as *local function approximation*,
differing only in the neighbourhood and the loss used. It proves a no-free-lunch
theorem (no method is optimal across all neighbourhoods) **and gives a principled
selection rule: pick the method most faithful to the model in the neighbourhood you
actually care about.**

Consequence for you: "there is no fact of the matter about the explanation" is too
strong and is already refuted. Once you fix a neighbourhood, there *is* a fact of the
matter. Your defensible claim is narrower and better (see §3).

### Lundberg & Lee 2017 — the theoretical core of your "definitional" argument
Theorem 2 shows Shapley values are the solution to a weighted linear regression with a
*specific* kernel, loss and regulariser. LIME uses the same template but picks those
three heuristically, and with LIME's choices the solution **does not** recover Shapley
values. This is the cleanest citation for "they optimise different objectives by
construction" — same functional form, different weighting, therefore different answers
as a matter of definition, not tuning. Lead with this.

### Bilodeau, Jaques, Koh & Kim 2024 (PNAS) — arXiv:2212.11870
"Impossibility theorems for feature attribution." For moderately rich model classes,
any *complete and linear* attribution method — which includes Integrated Gradients and
SHAP — can provably fail to beat random guessing at inferring model behaviour, on end
tasks including identifying spurious features and algorithmic recourse. This is the
strongest theoretical backing available for the sceptical position. A short paper that
runs the disagreement experiment and lands on Bilodeau has a real spine.

### Chen, Janizek, Lundberg & Lee 2020 — arXiv:2006.16234
"True to the Model or True to the Data?" Interventional vs observational conditioning
changes SHAP's answers: the observational variant spreads credit across correlated
features the model may not even use, the interventional one only credits features that
actually move the output. There is no neutral choice. Directly relevant, because your
experiment silently makes this choice for you via the SHAP variant you call.

### ICLR 2026 — "Tackling the XAI Disagreement Problem with Adaptive Feature Grouping"
Argues the mathematical source of disagreement is **inter-group feature interactions**:
methods redistribute interaction terms differently. Their AGREED method merges
strongly-interacting features until the model is approximately groupwise-additive, at
which point the explainers converge.

This cuts against "not a tuning problem." Their result is that disagreement is
*partially remediable* by restructuring the feature space. You need a sentence
acknowledging it, or you are overclaiming.

### Rahnama, Butepage, Geurts & Bostrom 2021 — arXiv:2106.02488
"Evaluating Local Explanations using White-box Models." Gets around the no-ground-truth
problem by using models whose log-odds ratio decomposes additively (logistic
regression, naive Bayes), giving true per-instance importances to score methods
against. On Adult under logistic regression they report mean Spearman vs true
importance of **-0.075 for LIME and 0.372 for SHAP**. They also find performance
depends on the model, the dataset, which instance, the normalisation, and the
similarity metric.

This is the single best upgrade available to you — it turns "they disagree" into
"they disagree, and here is which one is wrong." See §4.

### OpenXAI (Agarwal et al., NeurIPS 2022 Datasets & Benchmarks)
github.com/AI4LIFE-GROUP/OpenXAI, MIT licensed. Datasets, pretrained models, method
implementations and 22 metrics for faithfulness/stability/fairness. Same lab as Krishna
et al. Using it saves you a day and makes the setup defensible by construction.

---

## 2. Novelty check

Near zero, as originally framed. Krishna et al. already covered German Credit; swapping
in Adult is not a contribution. There is a large low-quality literature of
"we compared SHAP and LIME on dataset X" papers — you do not want to be mistaken for
one of those.

The two things in your idea that are *not* already done:

1. **Separating within-method noise from between-method disagreement.** Krishna et al.
   report cross-method disagreement but do not isolate how much of it is just LIME's
   sampling variance. This is a real gap, it is cheap to fill, and it is the difference
   between a replication and a paper.
2. **The normative framing** — that the choice of neighbourhood and reference
   distribution is a value judgement that no deployment documents, which is where the
   recourse problem actually bites.

---

## 3. Fix the thesis

Your draft claim: *the disagreement is definitional, not a tuning problem, and it
undermines the idea that there's a fact of the matter about "the explanation."*

The second half is refuted by Han et al. and weakened by the ICLR 2026 interaction
result. Reword to something like:

> There is no *method-independent* fact of the matter about a feature's importance.
> There is a fact of the matter once a neighbourhood and a reference distribution are
> fixed — but those are normative choices, they are not determined by the model or the
> data, and deployed explanation systems do not disclose them. So the applicant is
> shown one answer from a family of equally defensible ones, with no record of which
> assumption produced it.

That version survives contact with the literature, is still a real claim, and the
recourse implication stays intact.

---

## 4. Methodological traps

Most "SHAP vs LIME" comparisons are invalid for at least one of these reasons.

**1. LIME discretises by default; SHAP does not.** `discretize_continuous=True` is the
default in `lime_tabular`, with quartile binning. LIME is then explaining binned
indicator features while SHAP explains raw ones — you would be comparing rankings over
two different feature spaces. Set it to `False`, or bin for both, and state the choice.
*This one invalidates a lot of published comparisons.*

**2. LIME's kernel width is arbitrary.** Default is `sqrt(n_features) * 0.75`. It
controls the size of the locality and therefore the answer. Sweeping it and plotting
rank correlation against it is a cheap, honest extra figure — and it directly tests
"tuning vs definitional," since if agreement moves a lot with kernel width then some of
the disagreement *is* tuning.

**3. LIME is unstable against its own seed.** Different perturbation samples give
different explanations for the same instance; this is well documented (Visani et al.'s
VSI/CSI stability indices, arXiv:2001.11757, plus S-LIME, OptiLIME, GLIME). **You must
report a within-method baseline: LIME(seed A) vs LIME(seed B) under the same metrics.**
If between-method disagreement is not clearly larger than within-LIME disagreement,
your definitional claim collapses into "LIME is noisy" and the paper has no result.
This is both the biggest risk and the main novelty — do not skip it.

**4. Which SHAP?** KernelSHAP, TreeSHAP, interventional vs observational, and the
background dataset (training median? a sample? how large?) all change the numbers.
Fix one, justify it, cite Chen et al. Do not use TreeSHAP for the tree and KernelSHAP
elsewhere and call both "SHAP."

**5. Correlated features inflate disagreement.** Adult has near-duplicates —
`education` vs `education-num`, and heavy overlap between `marital-status` and
`relationship`. Shapley splits credit across correlated features; LIME's surrogate does
not do so in the same way. Report a correlation-pruned variant so a reviewer cannot say
your effect is a redundant-encoding artefact.

**6. Ties near the top-k boundary.** If attributions ranked 4–8 have near-identical
magnitude, rank agreement at k=5 is measuring coin flips. Either bootstrap the
instance-level metrics or report the magnitude gap at the cut.

**7. Full-vector Spearman is misleading.** Over all features it is inflated by the long
tail of unimportant features agreeing that they are unimportant. Use top-k rank
agreement and pairwise rank agreement as primaries; report Spearman as secondary.

**8. Adult itself is a flagged dataset.** Ding et al. 2021, "Retiring Adult"
(arXiv:2108.04884): the $50k cut is 1994 dollars, the 76th percentile overall but the
88th in the Black population and 89th among women, and fairness conclusions are
sensitive to it. If you touch fairness or recourse framing at all — and your discussion
section does — either use folktables `ACSIncome` instead or cite the caveat explicitly.
FAccT-adjacent readers will know this.

---

## 5. Recommended design

Small enough to stay a short paper, large enough to have a defensible result.

- **Data:** folktables ACSIncome (one state, subsampled) or Adult with the Ding caveat
  stated. Optionally German Credit as a second dataset to connect to Krishna et al.
- **Models:** logistic regression plus one non-additive model (gradient-boosted tree or
  a small MLP). The logistic regression matters — see the ground-truth arm below.
- **Methods:** LIME (`discretize_continuous=False`) and KernelSHAP, same background
  distribution, matched sample budgets, single fixed variant each.
- **Instances:** 300–500 from the test set.
- **Metrics:** Krishna et al.'s six, at k = 3 and 5.
- **Arm A (the money result):** between-method vs within-method disagreement. LIME vs
  SHAP, against LIME vs LIME across seeds and KernelSHAP vs KernelSHAP across background
  samples. Plot all three distributions on one axis.
- **Arm B (cheap, strong):** the logistic-regression ground truth from Rahnama et al. —
  log-odds decomposes additively, so you get true per-instance importances and can say
  which method is *wrong*, not just that they differ. This is what lifts the paper above
  the "we compared two libraries" pile.
- **Arm C (optional):** rank correlation as a function of LIME kernel width, as the
  direct test of the tuning-vs-definitional question.

**Output:** one table (metrics x method pairs), and realistically two figures, not one —
Arm A's distribution plot and either Arm B or Arm C. Budget 1–2 days, not half a day.
KernelSHAP over 500 instances is slow, and Arm A means running LIME several times per
instance.

---

## 6. Where this can go

Not novel enough for a real venue as a contribution. Perfectly fine for coursework, a
student or departmental journal, or a workshop replication / negative-results track.
The honest pitch is "replication of Krishna et al. on a modern income dataset, plus a
within-vs-between-method decomposition they did not report, plus a ground-truth arm."

**Compared to the other topics in BasicTopics.md:** this is the strongest *empirical*
option, and Arm B is what makes it so. But note that #4 (plausibility vs faithfulness)
and #6 (explanations raise confidence more than accuracy) are cheaper and have sharper
theses, and #1 (Adebayo sanity checks) has the single cleanest narrative. If the goal is
the best short paper rather than the best experiment, #1 or #4 are less risky. If you
want to have run something, this one — with Arm A, which is non-negotiable.

---

## Reading order

1. Lundberg & Lee 2017, §4 and Theorem 2 — arXiv:1705.07874 (the definitional argument)
2. Krishna et al. 2022 — arXiv:2202.01602 (metrics + prior art you are replicating)
3. Han et al. 2022 — arXiv:2206.01254 (the counterargument; read before you write)
4. Rahnama et al. 2021 — arXiv:2106.02488 (Arm B)
5. Bilodeau et al. 2024 — arXiv:2212.11870 / PNAS (the spine of the discussion)
6. Chen et al. 2020 — arXiv:2006.16234 (SHAP variant choice)
7. Visani et al. 2020 — arXiv:2001.11757 (LIME instability, justifies Arm A)
8. Ding et al. 2021 — arXiv:2108.04884 (dataset caveat)
