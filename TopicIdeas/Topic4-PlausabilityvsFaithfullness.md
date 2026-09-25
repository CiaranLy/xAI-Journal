# Topic 4: Plausibility versus faithfulness

I think this topic could work as a short paper, but not in the form the original idea puts it. The main argument has already been made. Jacovi and Goldberg (2020) separate plausibility from faithfulness, argue that people's judgements cannot tell us whether an explanation is faithful, and suggest treating faithfulness as a matter of degree. Their paper is the standard reference on this, so I could not present the distinction as a new idea.

The claim about the field also needs changing. The original idea says that human judgement is the field's main way of evaluating explanations. A review by Nauta et al. (2023) of more than 300 XAI papers found that only about one in five evaluated with users, while about one in three relied only on a few examples. Formal studies with people are not the main method. However, showing a handful of examples and treating them as convincing is still a judgement of plausibility, just an informal one made by the authors.

## 1. Definitions

Explainable AI (XAI) methods try to show why a model gave a particular output, usually by highlighting the parts of the input that mattered most or by giving a written reason. In this paper, plausibility means whether an explanation seems reasonable to a person, and faithfulness means whether it reflects what actually produced the output. I would also use usefulness to mean whether an explanation helps someone with a specific task, such as predicting what the model will do or finding a fault in it.

When a model behaves the way people expect, a faithful explanation will usually look reasonable as well. The two only separate when the model has learned something people would not expect.

## 2. Existing research

Adebayo et al. (2018) tested whether saliency maps changed when the model changed. They scrambled the model's weights, and separately trained models on random labels, then compared the maps. Some methods gave almost the same maps in every case, and the maps looked similar to the output of an edge detector. Since they followed the outline of the object, they looked believable, but a map that barely depends on the model cannot say much about it. This was true of some methods and not others.

Ribeiro et al. (2016), who introduced LIME, trained a classifier to tell wolves from huskies using photos where the wolves were standing in snow. The explanations showed that the model was using the snow. Judged on whether it was a sensible way to identify a wolf, the explanation would have failed, even though it was accurate and showed the problem with the model.

Lapuschkin et al. (2019) found a similar case in a real dataset. A model that appeared to recognise horses was relying heavily on a copyright tag found in many of the horse photos, and an explanation method showed this. Unlike the wolf example, nobody planted the shortcut.

Adebayo et al. (2022) trained models on data with planted shortcuts and tested whether explanation methods helped people find them. The methods they tested did poorly when the user did not already know what to look for, particularly when the shortcut was hard to see, such as a blurred background. They also found that some attribution methods pointed to a shortcut the model was not using. This means the wolf and horse examples show what can happen rather than what usually happens.

Doshi-Velez and Kim (2017) divide evaluation into three levels: people doing a real task, people doing a simplified task, and formal measures with no people involved. I would use this to avoid treating human evaluation as one method.

Hase and Bansal (2020) tested whether explanations helped people predict a model's output on new inputs. People's ratings of explanation quality did not reliably match how much the explanations helped them. This is a study with people, but it measures usefulness more than plausibility.

DeYoung et al. (2020) created the ERASER benchmark, which scores explanations on how closely they match the words people marked as important, and separately on how much the output changes when the highlighted words are removed. It keeps the two properties apart. It also shows that plausibility can be measured without asking anyone for ratings, since matching human-marked text is still a comparison with what people expect.

## 3. Argument

I would argue that plausibility can be measured, but should not be reported as evidence of faithfulness. The shortcut case is where this matters most, because it is when an explanation is most needed and also when a check based on plausibility is most likely to reject an accurate one.

I would change two parts of the original idea. Nauta et al. do not support the claim that human judgement is the dominant evaluation method, so I would focus on informal examples instead. I would also not describe the two properties as inversely related in general, since they only pull in opposite directions when a model relies on something unexpected.

The scope would be explanations of single predictions, mainly highlighted features in images and text. Written explanations from language models overlap with Topic 3, so I would only mention them briefly.

## 4. Problems to address

The biggest risk is that the paper turns into a summary of Jacovi and Goldberg. To avoid that, I would treat their paper as the starting point and spend most of the discussion on the shortcut case and on informal evaluation.

Faithfulness is also hard to measure. Most models have no record of the true reason for a prediction, and tests that remove parts of the input have their own weakness: the changed input may be unlike anything the model was trained on, so the output could change for unrelated reasons.

I would need to be fair to plausibility. If an explanation is meant for a user, it matters whether they can make sense of it. My objection is only to using it in place of faithfulness.

I would also keep different kinds of human study apart, since rating an explanation is not the same as using it to predict a model. The same goes for explanation types. Highlighted features, training examples and written reasons work differently, so each finding would stay tied to the method and model that was actually tested.

## 5. Possible experiment

The paper would not need an experiment, but a small one could illustrate the argument. I would train a simple text classifier on data where one planted word always appears with one label, then score an explanation method in two ways: how well it matches human-marked words, and how much the output changes when its highlighted words are removed. If the model uses the planted word, the removal test should pick it up while the match with human-marked text gets worse. I would also train a second model without the planted word, to check whether the method highlights it anyway. I would save the data, settings and scores, and run it several times. The results would only illustrate the argument and would not show anything general about the method.

## 6. Choosing this topic

I think it would suit a short paper. The argument is clear, the examples are well known, and it does not depend on a large experiment. The main risks are repeating Jacovi and Goldberg, and criticising a version of the field that no longer exists, since many papers already test faithfulness directly. It is more conceptual than Topic 3, but both topics deal with the same problem: an explanation that reads well is not necessarily an account of how the answer was produced.

## References

Adebayo, J., Gilmer, J., Muelly, M., Goodfellow, I., Hardt, M. and Kim, B. (2018) Sanity Checks for Saliency Maps. [arXiv:1810.03292](https://arxiv.org/abs/1810.03292)

Adebayo, J., Muelly, M., Abelson, H. and Kim, B. (2022) Post Hoc Explanations May Be Ineffective for Detecting Unknown Spurious Correlation. [arXiv:2212.04629](https://arxiv.org/abs/2212.04629)

DeYoung, J. et al. (2020) ERASER: A Benchmark to Evaluate Rationalized NLP Models. [arXiv:1911.03429](https://arxiv.org/abs/1911.03429)

Doshi-Velez, F. and Kim, B. (2017) Towards a Rigorous Science of Interpretable Machine Learning. [arXiv:1702.08608](https://arxiv.org/abs/1702.08608)

Hase, P. and Bansal, M. (2020) Evaluating Explainable AI: Which Algorithmic Explanations Help Users Predict Model Behavior? [arXiv:2005.01831](https://arxiv.org/abs/2005.01831)

Jacovi, A. and Goldberg, Y. (2020) Towards Faithfully Interpretable NLP Systems: How Should We Define and Evaluate Faithfulness? [arXiv:2004.03685](https://arxiv.org/abs/2004.03685)

Lapuschkin, S. et al. (2019) Unmasking Clever Hans Predictors and Assessing What Machines Really Learn. [Nature Communications](https://www.nature.com/articles/s41467-019-08987-4)

Nauta, M. et al. (2023) From Anecdotal Evidence to Quantitative Evaluation Methods: A Systematic Review on Evaluating Explainable AI. [arXiv:2201.08164](https://arxiv.org/abs/2201.08164)

Ribeiro, M. T., Singh, S. and Guestrin, C. (2016) "Why Should I Trust You?": Explaining the Predictions of Any Classifier. [arXiv:1602.04938](https://arxiv.org/abs/1602.04938)
