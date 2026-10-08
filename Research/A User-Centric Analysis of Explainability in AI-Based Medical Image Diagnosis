# A User-Centric Analysis of Explainability in AI-Based Medical Image Diagnosis

**Authors:** Julia Wagner, Tim Schlippe (IU International University of Applied Sciences, Germany)

**Link:** https://arxiv.org/abs/2605.02903 (v1)

**Publication:** XAI-Healthcare 2025 proceedings, Springer, published 2026.

---

## How it fits our topic

I picked this because it tests explanations from the user's side. The question I am interested in is whether an explanation helps someone challenge a wrong diagnosis, rather than just being easy to understand.

It makes a useful comparison with CX-ToM:
- CX-ToM tests whether people can predict the model's behaviour.
- This study asks medical participants to rate explanations and assess diagnoses.
- Neither result alone establishes whether the explanation reflects the model's actual calculation.

I would keep these differences clear when comparing the papers. An explanation can be preferred by users without protecting them from a wrong suggestion.

## What it is

A questionnaire comparing eight explanation formats and no explanation for chest X-ray diagnosis.

## Explanation formats

| Type | Formats tested |
|---|---|
| Visual | Heatmap; bounding box |
| Text | Written report; chatbot |
| Combined | Heatmap + report; heatmap + chatbot; box + report; box + chatbot |
| Comparison | No explanation |

## Data and setup

### Participants

- **Participants:** 33; 49% assistant physicians, 24% specialists, 12% senior physicians, 15% medical students.
- **Radiology:** 12% of the sample.

### Procedure

- **Task:** one correct and one incorrect AI diagnosis per method.
- **Ratings:** 1–5 for understandability, completeness, perceived speed, and applicability.

These details come from sections 3–4. The sample includes medical students, despite the abstract describing the participants as physicians.

## Results

### Explanation ratings

Selected mean ratings from sections 5.1–5.3, on a 1–5 scale:

| Format | Understandability | Completeness | Speed | Applicability |
|---|---|---|---|---|
| None | 3.24 | 1.85 | 2.64 | 2.64 |
| Heatmap | 2.73 | 2.03 | 2.06 | 2.42 |
| Box | 3.67 | 2.91 | 3.36 | 3.55 |
| Report | 3.70 | 3.24 | 3.06 | 3.36 |
| Chatbot | 3.67 | 2.76 | 2.73 | 2.76 |
| Box + report | 4.18 | 3.91 | 3.82 | 3.88 |

- **Box + report scored highest** across all four areas.
- Heatmaps scored below no explanation on understandability, perceived speed, and applicability.
- Reports scored above chatbots across the four areas shown.

These scores describe the participants' ratings. They are not measured diagnosis times or accuracy scores.

### Responses to incorrect AI suggestions

For box + report, section 5.4 reports:

| Outcome with an incorrect suggestion | Reported share |
|---|---|
| Wrong diagnosis | 32% |
| Partly wrong diagnosis | 20% |

These figures are from the arXiv version.

The highest-rated format still allowed incorrect suggestions to be accepted. I would want a comparison using equivalent cases without suggestions before concluding that the explanation caused the errors.

## Weaknesses

- **Small, mixed sample:** I would be cautious about applying the results to all clinicians. Experience with the image type could matter as much as the explanation format.
- **Few examples per method:** I would want more cases before deciding that one format consistently helps. An unusually easy or difficult image could affect the comparison.
- **Preference and performance:** a high rating tells us something about the participant's experience. It does not, by itself, show better decisions.
- **Cause of errors:** the reported mistakes need a suitable comparison before we can say explanations increased reliance on wrong answers.
- **Faithfulness remains a separate question:** even an accurate diagnosis with a well-liked explanation would not prove that the explanation reflects the model's actual calculation.
