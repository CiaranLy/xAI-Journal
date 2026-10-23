These are the papers I read and why we ended up using them/not. 
Disclaimer: I assigned myself the first 3, the others we looked at in a group meeting. I forgot to actually upload the Research.
We went through them as a group to help decide if there was enough evidence to support our thesis. 

# Original notes:

## Explainable AI And Visual Reasoning: Insights From Radiology:

heatmaps/attention maps dont match how human experts build and communicate a diagnostic case. XAI should mirror the human process of justification. 

## Architecture-aware Robustness Evaluation of Explainable Deep Learning for Breast Cancer Diagnosis, by Balenthira Thanusanth, Selvarajah Thuseethan, Roshan G. Ragel, Bimali S. Weerakoon, Ayesh Jayasinghe and Ananthamoorthy Krishnamoorthy. It’s on arXiv as 2609.31692 (September 2026). 

Link: https://arxiv.org/abs/2609.31692 

claim: people don't usually pick the right XAI method for a specific model. It argues no method works best everywhere, so the model and explanation method should be chosen together. They built an evaluation protocol. They say selection is an optimisation problem: for a given model, pick the XAI method that maximises avg agreement (IoU,PG,MC) 

## Ranking XAI Methods for Head and Neck Cancer Outcome Prediction (Ma et al., April 2026) 

benchmarking study. authors note that most prior medical imaging papers just pick an XAI method (often Grad-CAM or SHAP) without justifying why 

Finding: picking an xai method by convention/popularity is dumb 
systematic evaluation needed (and an example was given ) 

## Sanity Checks for Saliency Maps (Adebayo et al., 2018).

Read: full text. Scrambled a model's weights and labels to see whether the heatmaps change; some methods (Guided Backprop, Guided Grad-CAM) barely changed and some maps looked like a plain edge detector, while Grad-CAM and plain gradients passed. Push back: it used mostly everyday images (one bone-age X-ray example), and passing the check doesn't prove a map shows what the model uses. 

## A Benchmark for Interpretability Methods in Deep Neural Networks (Hooker et al., 2019, "ROAR").

Read: abstract only. Removes the pixels a method calls important, retrains the model, and checks whether accuracy drops; many popular methods were no better than random. Push back: uses just everyday image, not medical paper. 

## In Defense of Post Hoc Explanations in Medical AI (Hatherley 

Argues that explanations which only approximate a model can still help doctors: they can improve understanding of how the AI behaves, and the risks critics raise (over-reliance, bias) also apply to human explanations and can be reduced.  
Basically- they argue post hoc methods are still useful, over reliance happens eitehr way. 

Push back: its main evidence is one study (Senoner) 

# Should we include? 

- **Radiology paper: YES.** Heatmaps don't match how radiologists reason or explain a diagnosis, so XAI should follow how humans justify decisions. 

- **Thanusanth et al. (2026): YES.** No XAI method works best on every model, so choose the method and model together. This supports why we need opapers to properly test faithfulness of heatmaps, because clinicians need to use this info to pick their xai model etc. 

- **Ma et al. (2026): YES.** Most medical papers pick Grad-CAM or SHAP by habit, and methods need proper systematic evaluation. It backs up Thanusanth on a different cancer. 

- **Adebayo et al. (2018): YES** Some popular methods barely changed when the model was scrambled, so a nice heatmap isn't automatically trustworthy. Issue- it uses mostly everyday images, and passing the test doesn't prove a map is right. 

- **Hooker et al. (2019): YES.** Many methods did no better than random at finding the pixels that matter. Caveat: it uses everyday images. 

- **Hatherley: YES-counterargument to heatmaps being useless-** Approximate explanations can still help doctors, and over-reliance happens with human explanations too. Caveat: it rests mainly on one study.
