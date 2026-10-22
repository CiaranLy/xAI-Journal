# Two viable formats:

## A focused position/review paper — take one specific controversy, present both sides, argue a position.

Saliency maps fail sanity checks — Adebayo et al. showed some methods produce near-identical maps for a trained network and a randomly initialized one. Four pages is perfect for explaining the test, summarizing which methods fail it, and arguing what this means for medical imaging deployments.
Plausibility vs. faithfulness — explanations that humans rate as good are often not the ones that reflect the model's computation. Clean, well-defined, plenty of literature, and you can state a real thesis.
Is chain-of-thought an explanation? — Turpin et al. showed models give reasoning that omits the actual cause of their answer (e.g. answer order bias). Very current, easy to motivate, and you can write it without compute.
The right to explanation is weaker than people think — legal/technical mismatch between GDPR Art. 22 and what post-hoc methods can actually deliver. Good if you want something less technical.

## A small empirical paper — one experiment, one or two figures. More impressive if you have time.

Run LIME and SHAP on the same tabular model (UCI Adult or German Credit) and quantify how often their top-5 feature rankings disagree. Rank correlation over a few hundred instances. Half a day of work, genuinely publishable-shaped finding.
Perturbation stability: add imperceptible noise to inputs, measure how much the explanation changes while the prediction doesn't.
Counterfactual recourse feasibility: generate counterfactuals with DiCE, then check what fraction recommend changing immutable features like age or race.

If I had to pick one for a short paper, the LIME/SHAP disagreement experiment is the best value — the setup is small, the result is concrete, and the discussion section writes itself because the implication (which explanation does the loan applicant get shown?) is obvious and important.