# XAI Group Project

**Paper:** *Plausible but Unverified: How Saliency Explanations Are Evaluated in Medical Imaging*

**Authors:** Aoibheann Mangan, Rosie McInerney, Ciarán Lynch, Cian McNamara

**Topic:** XAI in medical imaging, focusing on saliency maps

**Latest draft:** [`Paperv1.tex`](Paperv1.tex)

## What the paper does

Medical imaging papers often present saliency maps (heatmaps such as Grad-CAM) as evidence that a model reasons correctly. We ask whether those maps are ever tested for **faithfulness**, meaning whether they reflect what the model actually computes, or only for **plausibility**, meaning whether they look right to a clinician.

1. **Audit.** We check five recent medical imaging XAI papers against five criteria: model randomisation (R), attribution-guided perturbation (F), lesion-mask agreement (L), whether users can predict the model (S), and user ratings (U). Only one paper reports a faithfulness test, and none randomises the model or measures simulatability.
2. **Experiment.** We run the missing tests on a ResNet-18 brain tumour classifier (LGG MRI dataset) with four saliency methods. Integrated Gradients localises the tumour best, yet its maps stay correlated with those of a fully random network. Pixel-level deletion cannot tell most methods from random deletion.
3. **Recommendations.** A short checklist of what papers should report, mapped to the audit criteria.

## Repository layout

| Path | Contents |
|---|---|
| `Paperv1.tex` | The paper |
| `refs.bib` | References (IEEE numbered style, via `IEEEtranN`) |
| `experiment/` | Code, results and figures for the experiment. See [`experiment/README.md`](experiment/README.md) |
| `Research/` | Our notes on each paper we read |
| `Topic-Saliency maps.md`, `RoughConcepts.md` | Early topic notes and ideas |

## Building the paper

You need `Paperv1.tex`, `refs.bib` and `experiment/results/figures/example_maps.pdf`, kept in the same folder layout. The IEEEtran class and the `IEEEtranN` bibliography style come with Overleaf and standard TeX installations.

On **Overleaf**, upload those files and recompile. If citations show as `[?]`, use *Recompile from scratch*.

To build **locally**:

```bash
pdflatex Paperv1
bibtex Paperv1
pdflatex Paperv1
pdflatex Paperv1
```

## Running the experiment

Setup, dataset download and run commands are in [`experiment/README.md`](experiment/README.md). The results used in the paper are already saved in `experiment/results/`, so you don't need to rerun anything to build the paper.

ReadMe was made by Claude (Antrophic)
