A real citation can still accompany a wrong answer. And "always refuse" beat every version of my model.

For today's book-to-business RAG experiment, I adapted ideas from Sanjay N T's RAG & Vector Databases (2026), pages 9, 25, 27 and 31, into a 50-line Python core.

The business question: can a post-generation evidence gate make technical-support answers safer?

Same 24 generated answers (SQuAD 2.0, 12 answerable, 12 unanswerable), four accept/refuse policies:

• Always refuse: 12/24 exact match. The do-nothing policy wins on aggregate.
• Ungated model: 9/24. Answers all 12 unanswerable questions.
• Exact-span citation gate: 9/24. Removes 1 of 12 unsupported answers. Ties the baseline (McNemar p = 1.00).
• Entailment gate (book ch. 46): 11/24. Removes 3 of 12 unsupported answers, refuses 2 answerable ones. p = 0.625, not significant at n = 24.
• Citation precision: only 9 of 24 quoted sentences actually contain the answer.

What I got wrong first: my span gate was case-sensitive while my scorer lowercased, so one "over-refusal" was a capital C. An evaluation audit caught it; the v1 numbers stay in the repo next to the corrected ones.

A copied quote is not evidence that the answer follows from it. None of these gates is ready for autonomous answering. Next: the entailment gate on fresh held-out questions with an independent judge, not the same 3B model grading itself.

Book credit: Sanjay N T, RAG & Vector Databases (2026), sections 8, 38, 40, 46. Dataset: SQuAD 2.0, Rajpurkar, Jia and Liang (2018), CC BY-SA 4.0; https://rajpurkar.github.io/SQuAD-explorer/.

#RAG #LLMEvaluation #MachineLearning #AIEngineering
