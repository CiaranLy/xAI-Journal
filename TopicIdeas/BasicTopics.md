# 1. Saliency maps don't survive sanity checks
Gradient-based methods produce heatmaps that look convincing, but when you randomize the model's weights layer by layer, some methods produce nearly identical maps — meaning they're responding to the input's edge structure, not what the model learned. Your claim: visual plausibility is a trap, and methods that fail randomization tests shouldn't be deployed in high-stakes imaging. Anchor reference: Adebayo et al., "Sanity Checks for Saliency Maps" (2018). Purely literature-based, very writable.

# 2. LIME and SHAP disagree on the same model
Both are the default answer to "how do I explain this classifier," but they optimize different objectives and routinely rank features differently on identical inputs. Your claim: the disagreement is not a tuning problem, it's a definitional one, and it undermines the idea that there's a fact of the matter about "the explanation." Best done as a tiny experiment — one model on UCI Adult, compare top-k feature rankings across a few hundred instances, report rank correlation. One table, one figure, done.

# 3. Chain-of-thought is not necessarily an explanation
LLMs produce step-by-step reasoning that reads as a justification, but experiments show the stated reasoning can omit the actual cause of the answer — e.g. reorder multiple-choice options and the model changes its answer while its written reasoning never mentions position. Your claim: fluent reasoning traces create unearned trust. Very current, easy to motivate, no compute needed. Anchor: Turpin et al., "Language Models Don't Always Say What They Think" (2023).

# 4. Plausibility versus faithfulness
Much of XAI evaluation asks humans whether an explanation seems reasonable. That measures agreement with human priors, not correspondence with the model's computation — and the two can be inversely related, because a faithful explanation of a model exploiting a spurious shortcut will look wrong. Your claim: the field's dominant evaluation metric is measuring the wrong thing. Conceptual, tight, good for a short paper.

# 5. Counterfactual explanations that can't be acted on
"You'd be approved if your income were $15k higher" is only useful if the change is achievable. Many generated counterfactuals recommend altering immutable or costly attributes. Your claim: actionability, not just proximity, should be the objective function. Can be literature-based, or a small experiment using DiCE on a credit dataset counting how many counterfactuals touch immutable features.

# 6. Explanations increase confidence more than accuracy
Several user studies find that showing people an explanation makes them more likely to accept the model's output — including when it's wrong. Your claim: XAI can worsen human-AI team performance by suppressing appropriate scepticism. Strong for a short paper because the finding is counterintuitive and the literature is compact.

# 7. Interpretable-by-design versus post-hoc
Rudin's argument is that for high-stakes decisions we should build models that are inherently interpretable rather than explaining black boxes after the fact, and that the accuracy cost is usually smaller than assumed. Your claim: pick a side and defend it. Good if you want a clear two-sided debate rather than a technical contribution. Anchor: Rudin, "Stop Explaining Black Box Machine Learning Models..." (2019).

# 8. The legal right to explanation exceeds what XAI can deliver
GDPR and the EU AI Act imply individuals should get meaningful information about automated decisions, but post-hoc attributions are unstable, method-dependent, and don't establish causation. Your claim: there's a gap between the legal standard and technical reality, and current methods wouldn't survive adversarial scrutiny. Least technical option — good if your background is more policy-leaning.