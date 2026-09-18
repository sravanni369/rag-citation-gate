# RAG: a valid citation can still support a wrong answer

A 50-line, AI-assisted experiment motivated by technical-support knowledge bases. Can a post-generation citation gate prevent unsupported answers? Two gates were tested on the same 24 generated answers: an exact-span containment check (the book's placeholder made literal) and a semantic entailment check (the book's chapter 46 claim verifier). Neither is fit for autonomous deployment; the entailment gate is the better of the two and the difference is not statistically distinguishable at this sample size.

## Result

All four columns score the **same 24 generated answers**; only the accept/refuse decision differs.

| Metric | Always refuse | Baseline (ungated) | Exact-span gate | Entailment gate |
|---|---:|---:|---:|---:|
| Exact match, all 24 questions | **12/24** | 9/24 | 9/24 | 11/24 |
| Exact match, 12 answerable | 0/12 | 9/12 | 8/12 | 8/12 |
| Correct refusals, 12 unanswerable | 12/12 | 0/12 | 1/12 | 3/12 |
| Unsupported answers on unanswerable questions | 0/12 | 12/12 | 11/12 | 9/12 |
| Refusals on answerable questions | 12/12 | 0/12 | 1/12 | 2/12 |
| Answers returned | 0/24 | 24/24 | 22/24 | 19/24 |
| Wilson 95% CI on exact match | [0.31, 0.69] | [0.21, 0.57] | [0.21, 0.57] | [0.28, 0.65] |

- **The do-nothing policy wins on aggregate.** On a balanced 12/12 set, "always refuse" scores 12/24 exact match, higher than any model variant. Neither gate beats abstention on aggregate EM; the comparison that matters is the per-slice one, where the model answers 8–9 of 12 answerable questions and refuses 1–3 of 12 unanswerable ones.
- **The exact-span gate ties the baseline.** It removed one unsupported answer and refused one answerable question (a correct answer with the wrong sentence cited). McNemar exact p = 1.00 against the baseline: treat the EM row as a tie.
- **The entailment gate moves in the right direction and is not significant.** It removed three of twelve unsupported answers and refused two answerable questions, one of which was already wrong. Exact match 9 → 11; McNemar exact p = 0.625 on 24 paired cases. This is a first look on the same inspected pilot, not the fresh held-out test the protocol calls for, and the judge is the same 3B model as the generator, so it is a second opinion from one model family rather than an independent verifier.
- **Citation precision (book ch. 38) is 9/24 = 0.375.** Only nine of the twenty-four quoted sentences contain a gold answer span; all twelve quotes on unanswerable questions are decorative. A verbatim quote is not evidence that an answer follows from it.

Retain human review; do not use this experiment to approve autonomous support answers. No production savings were measured.

## What changed in v2 (2026-09-17, after an evaluation audit)

The first version (kept in `results/v1_case_sensitive/`) reported the span gate as 8/24 with two over-refusals. An audit found that `rag.py` checked `answer in quote` case-sensitively while the scorer lowercases, so one "over-refusal" (`computational complexity theory` against `Computational complexity theory…`) was a letter-case artefact, not a gate failure. The v1 `audit.py` reproduced the same case-sensitive semantics, so it passed the bug. Fixes:

1. `rag.py` now case-folds the containment check (still 50 lines). Gate decisions are recomputed from the cached model outputs; no answer was regenerated. One decision flipped, listed in `results/audit.json`.
2. `evaluate.py` reports the always-refuse trivial baseline, per-slice recall, Wilson intervals and McNemar exact p, and counts the classes instead of hardcoding 12/12.
3. `entail.py` adds the chapter-46 claim verifier as a second gate; `evaluate.py` reports citation precision from chapter 38.
4. A fresh independent rerun of the v1 pipeline on 2026-09-17 (Python 3.13.5, NumPy 2.2.6, versus the original 3.12.14 / 2.3.5) reproduced all 24 cached predictions exactly; log and summary in `results/v1_case_sensitive/`.

## Adaptation and data

Adapted from Sanjay N T, *RAG & Vector Databases* (2026), sections 8, 38, 40 and 46, pages 9, 25, 27 and 31. See SOURCE.md for attribution, substitutions and licence. The implementation is AI-assisted and does not reproduce an entire book listing.

SQuAD 2.0 public development data (CC BY-SA 4.0): 24 questions over 22 distinct paragraphs (two paragraphs each supply one answerable and one unanswerable question), balanced 12/12 across computational complexity, steam engines and packet switching. This is a reading-comprehension proxy for technical support, not customer tickets. Each question is given its correct parent paragraph; retrieval happens within that paragraph. Public-benchmark contamination is possible, and this sample does not establish general performance.

## Pipeline

Question → normalised local embeddings → top two 2-sentence chunks → local language model → answer and quote → gate.

- Exact-span gate (`rag.verify`): the answer occurs in the quote and the quote in a retrieved passage, case-folded. No semantic check.
- Entailment gate (`entail.claim_supports`): the same local model, at temperature 0, judges whether the quoted passage on its own states the answer to the question. One extra call per case, median 1.1 s.

There is no learned confidence score and no tuned rejection threshold in either gate.

## Reproduce

Requires Python 3.12 or 3.13, NumPy 2.x, and local Ollama with `nomic-embed-text:latest` and `qwen2.5-coder:3b` already pulled, listening on localhost:11434. Model digests are in `results/model_versions.json`. Generation uses temperature 0 and seed 42; hardware and runtime changes can still affect reproducibility.

```powershell
python -m pip install "numpy>=2,<3"
python evaluate.py
python audit.py
```

`evaluate.py` reuses the cached `results/predictions.jsonl` and `results/entailment.jsonl` and recomputes every summary from them; it does not silently regenerate. For a fresh independent run, copy the project to a new folder and move both cached files aside. `prepare.py` downloads and selects the public data; `data/provenance.json` holds the hashes. One-question interface: `python rag.py "your question" context.txt`.

## Validation and evidence

- `rag.py`: exactly 50 physical lines; preparation, entailment, evaluation and audit are separate files.
- `results/frozen_protocol.json`: SHA-256 of `rag.py`, `evaluate.py`, `entail.py` and the 24-case subset, frozen before the v2 evaluation. The v1 hashes are in `results/v1_case_sensitive/`.
- `results/predictions.jsonl`: the model's answers, quotes, selected passages, labels and timings for all 24 questions. `results/entailment.jsonl`: the judge's verdicts.
- `results/summary.json`: every number in the table above, with intervals and paired tests.
- `results/audit.json`: independent case-folded recomputation of every gate decision and every count, the one v1 decision that changed, and two repeated generations that matched.
- `screenshots/`: the fresh-run terminal log and the rendered report page.

Audit PASS means the checks and arithmetic passed. It does not mean the model answered correctly. Median generation latency 5.67 s, p95 9.27 s on this local run; not a service-level figure.

## Novelty and next experiment

The author's public GitHub already contains generic RAG and refusal projects. This project evaluates post-generation citation gates against adversarially unanswerable questions with a paired comparison, a trivial baseline and a negative result. The scoped repository review is in SOURCE.md. The next experiment is the one this pilot cannot be: the entailment gate on fresh held-out questions the author has not inspected, with an independent NLI model as judge.
