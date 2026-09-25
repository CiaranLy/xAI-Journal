# Topic 3: Is Chain-of-Thought a Reliable Explanation?

I think this topic would work well for a paper based on existing research. What interests
me is that a model can give an answer and explain it in a way which makes sense, while
leaving out information which affected that answer. When the steps are easy to follow,
it is tempting to treat them as a record of how the model reached its conclusion. The
research on this topic gives me a reason to question that assumption.

Chain-of-thought (CoT) is the series of reasoning steps a language model produces while
working through a question. The main issue I want to look at is faithfulness, which
means whether those steps reflect how the answer was actually produced. This is
different from whether the answer is correct. A model could give the right answer
without accurately explaining why it chose it.

My starting view is that CoT can be useful, but sounding convincing is not enough to
make it a reliable explanation. I would focus on where that usefulness holds and what
we can reasonably learn from the steps a model shows us.

---

## 1. Research behind the topic

### Turpin et al. 2023 — Language Models Don't Always Say What They Think

[Turpin et al. (2023)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ed3fea9033a80fea1376299fa7863f4a-Abstract.html)
is the main starting point for this topic. The paper looks at whether models mention
information which pushes them towards a particular answer. In one experiment, the
options in the sample questions included in the prompt were reordered so that the
correct answer was always A. These sample questions show the model how to respond.

The information could affect the model's answer without appearing in its explanation.
This is the part I find most relevant. The explanation can still make sense on its own,
even though it leaves out something which helped produce the result.

I would be careful about how I describe this experiment. The change was made to the
examples in the prompt, rather than simply moving the options in the question being
answered. I also do not think the result is enough to say that every explanation is
unfaithful. It shows a unique way an explanation can leave something important out.

### Lanham et al. 2023 — Measuring Faithfulness in Chain-of-Thought Reasoning

[Lanham et al. (2023)](https://arxiv.org/abs/2307.13702) looks at the reasoning steps
from another direction. The researchers changed the steps themselves, including adding
mistakes and rewording them, then checked what happened to the answer. How much the
models relied on those steps varied across models and tasks.

I would include this because it asks a different question from Turpin's paper. One
checks whether the explanation mentions information which affected the answer. The
other checks whether changing the explanation affects the answer. I initially saw
these as parts of the same issue, but separating them makes the comparison clearer.

The findings also leave room for CoT to be faithful in some situations. This matters
to my argument because I do not want to take evidence of a failure and apply it to
every use of the method.

### Chen et al. 2025 — Reasoning Models Don't Always Say What They Think

[Chen et al. (2025)](https://arxiv.org/abs/2505.05410) examines whether reasoning models
mention hints which affect their answers. The paper reports cases where the hints
influenced the answer but were left out of the explanation. It also looks at training
models through rewards and at reward hacking, where a model finds a shortcut to earn
a reward without properly completing the task.

I think this paper is needed because the topic should not depend entirely on the
2023 studies. Models trained to spend more time reasoning need to be considered
alongside models which are simply asked to show their steps.

The measurement still has limits. How often a model admits using a hint does not tell
me how truthful its whole explanation is. I would keep any results tied to the model,
the type of hint, and the cases included in the calculation.

### OpenAI 2025 — Evaluating chain-of-thought monitorability

[OpenAI (2025)](https://openai.com/index/evaluating-chain-of-thought-monitorability/)
looks at whether a checking system can identify particular behaviours by reading a
model's reasoning. The research describes situations where access to these steps helps,
while also noting limits around what was tested and whether the findings apply outside
the test setting.

This is the main reason I would not dismiss CoT entirely. An explanation may leave
out information and still reveal enough to identify a problem. I see this as a useful
distinction between having a complete explanation and having something worth checking.

It also changes the direction of the paper slightly. Rather than only asking whether
the explanation is faithful, I would consider what it is being used for. A trace used
to spot a particular behaviour may be useful even when it would not be enough to
explain the full decision.

### Lyu et al. 2023 — Faithful Chain-of-Thought Reasoning

[Lyu et al. (2023)](https://aclanthology.org/2023.ijcnlp-main.20/) takes a different
approach. The model turns the question into formal steps which a separate program
follows to produce the answer. This program uses fixed rules, so the answer comes
from the steps it is given.

I would include this as a possible improvement. It gives the intermediate steps a
clear role in producing the answer. However, I do not think it removes the whole
problem. The model could still turn the original question into the wrong steps, and
the method does not by itself explain why those steps were chosen.

This gives me a practical point to discuss without claiming that the issue has been
solved for every type of question.

### Wei et al. 2022 — Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

[Wei et al. (2022)](https://arxiv.org/abs/2201.11903) reports better results on maths,
commonsense, and tasks involving formal symbols when examples include reasoning steps.
I would use this to explain why CoT is worth considering in the first place.

Better performance is a real benefit. My concern is that it can be confused with a
better explanation. I would keep those two claims separate throughout the paper.

### Young 2026 — Measuring Faithfulness Depends on How You Measure

[Young (2026)](https://arxiv.org/abs/2603.20172v2) reports that different scoring systems
can disagree about whether a model admitted using a hint. This can change which model
appears most faithful, even when the same reasoning is being scored.

I think this could be useful when discussing how the studies measure their results.
Mentioning a hint and admitting that it affected the answer are not necessarily the
same thing. However, this source needs a closer look before I would rely on it. Its
data, code, and scoring method have not been checked here.

These sources give me a starting set of papers rather than a complete review of the
field. The source checks for this assessment were limited to abstracts, introductory
material, and research summaries: Turpin's abstract and PDF introduction, Chen's abstract
and HTML overview, OpenAI's research page, and the abstracts for Wei, Lanham, Lyu, and
Young. I would need to check the full methods before using detailed results. I have
left out numerical findings at this stage for that reason.

---

## 2. What this topic would add

The basic finding already exists. Showing that a model can leave important information
out of its explanation would repeat earlier work. I do not think a few more examples
would be enough to make this a new finding.

For me, the value would be in comparing what the different tests actually show. I
would look at whether the model mentions information which affected its answer,
whether its written steps affect the result, and whether those steps help identify
problems. These are related questions, but a good result on one does not settle the
others.

I would keep the scope to question answering, with multiple-choice tasks as the main
example. I would leave out a wider discussion of consciousness and hallucination.
Those are separate topics, and including them would make it harder to give this
question enough attention.

---

## 3. How I would frame the argument

The original topic idea says that convincing reasoning creates unearned trust. I
understand the concern, but I think that claim goes further than the evidence discussed
here. Showing that a model leaves information out does not tell me how a person reacts
to reading its explanation.

I would narrow the argument to whether the explanation gives us a reliable account
of how the answer was reached. My view is that CoT can provide useful information,
but it needs to be checked against what actually affects the answer. The fact that
it reads well is not enough on its own.

The three terms I would use are:

| Term | What I mean by it |
|---|---|
| Correctness | Whether the answer is right |
| Faithfulness | Whether the explanation reflects how the answer was reached |
| Monitorability | Whether the reasoning helps a person or checking system spot a particular behaviour |

I would still mention trust as a reason the topic matters. To make it a main conclusion,
I would need separate research on how explanations affect people's decisions. For now,
I think the technical question is enough to support a focused paper.

---

## 4. Issues I would need to account for

**1. Leaving something out does not mean it was hidden on purpose.** I would describe
what the model did without assuming why it did it. If a hint is missing from the
explanation, that is something I can record. Saying it was deliberately hidden would
need more evidence.

**2. One failure does not show how common the problem is.** A carefully tested example
can show that a method does not always work. It cannot tell me how often it fails.
That would need a clear way of choosing cases and an estimate of the uncertainty.

**3. The answer matters more than its letter.** If options are reordered, the same
answer can move from A to B. I would need to compare the selected content, otherwise
I could count a changed label as a changed answer.

**4. Different hints may have different effects.** Useful information, a suggested
answer, and a claim that an authority prefers an answer are different inputs. I would
keep these separate rather than treating every hint as the same kind of test.

**5. Models can change answers without a changed prompt.** I would need to ask the
unchanged question more than once. Otherwise, an ordinary difference between responses
could be mistaken for an effect caused by the hint.

**6. Mentioning a hint is different from admitting its use.** A model might mention
a hint only to reject it. I would need a clear scoring rule, with two people checking
the responses separately and recording where they disagree.

**7. Editing the reasoning does not explain the whole process.** If an answer changes
after an edit, that shows the edit affected it. If it stays the same, the model might
have corrected the mistake or used another approach. I would need to allow for both
possibilities when interpreting the result.

**8. Not every explanation is the same type of output.** Steps written before the
answer, a summary shown to the user, and an explanation requested afterwards are
different things. I would keep each finding tied to the output, model version, and
task which the study actually tested.

---

## 5. How I would approach the paper

I would base the paper on existing research rather than start with an experiment.
This would give me more time to compare the studies and explain where their findings
agree or differ.

Turpin, Lanham, and Chen would form the main part of the comparison. For each paper,
I would record the model, task, reasoning available, change made during the test,
measurement, result, and limits. I would then use the monitoring research to consider
where an incomplete explanation can still be useful. Lyu's approach would give me a
way to discuss possible improvements.

I think one comparison table and a diagram of the three types of test would be enough
to support the discussion. The main work would be explaining what we can learn from
each test, rather than writing a separate summary of every paper.

If I added an experiment, I would keep it small and repeat a hint-based test. I would
choose questions from a public source, save the selection rule, and compare an unchanged
prompt with one containing a misleading hint. The answer options and their order would
stay fixed. I would also repeat the unchanged prompt to see how often the model changes
its answer without the hint.

I would count changes towards the hinted answer separately from explanations which
admit using the hint. Among the changed answers, the share which admit using it would
give an acknowledgment rate. Both counts would need to be included. If no answers
changed towards the hint, that rate could not be calculated. This would still be an
estimate of influence, as repeated responses can vary for other reasons.

I would save the model version, date, settings, prompts, answers, errors, and any cases
left out. Two members would check the explanations independently. No experiment has
been run for this assessment, and I would treat this as a small repeat of existing
work rather than a basis for broad claims about a model.

---

## 6. Whether I would choose this topic

I think this is a suitable topic for a coursework paper. There is enough research to
support a comparison, and the question is narrow enough to discuss without needing
to train or run a model. Its value would come from explaining the differences between
the tests and what those differences mean for using CoT as an explanation.

Compared to topic 2, this would involve less implementation work. Topic 2 has a clearer
route to numerical results, while this topic depends more on the quality of the reading
and comparison. The main risk I see is taking a few failures and making a claim about
all reasoning models.

My preference would be to keep this as a focused review. I would include monitoring
as a main part of the discussion because it makes the conclusion more balanced. CoT
can leave out important information and still be useful. What I want to understand is
when that information is enough for the task, and when it needs further checks.

---

## Reading order

1. Turpin et al. 2023 — the starting example of an influence missing from an explanation.
2. Lanham et al. 2023 — what happens when the reasoning steps are changed.
3. Chen et al. 2025 — whether trained reasoning models show similar problems.
4. OpenAI 2025 — where reading the reasoning helps identify problems.
5. Lyu et al. 2023 — a different approach to connecting the steps with the answer.
6. Wei et al. 2022 — background on why CoT improves results.
7. Young 2026 — further checking of how mentions of hints are scored.
