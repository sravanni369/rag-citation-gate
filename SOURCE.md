# Book-to-project provenance

Source: **RAG & Vector Databases: Deep study and interview edition: formulas, techniques, failure diagnosis, system design, and runnable patterns**, by **Sanjay N T**, Production Handbook, 2026. Title page says research verified through August 2026. No publisher is named on the inspected title page.

Local source: `C:/nvidia notes/day17_drift_alarms/books/RAG and vector database.pdf`.

- Section 8, page 9: normalized embedding vectors and exact dot-product retrieval baseline.
- Section 46, page 31: grounded generation, structured output, extractive-first answers, abstention and citation verification. `entail.py` (v2) is one small implementation of the chapter's undefined `claim_supports`.
- Section 38, page 25: generation and citation metrics; `evaluate.py` (v2) reports the chapter's citation precision.
- Section 40, page 27: paired evaluations, separate failure slices, and honest release criteria.

Printed and PDF page numbers match for the inspected pages. Title page and page 31 were rendered and visually inspected locally. The book itself is not included in this project.

`rag.py` is an AI-assisted **adaptation**, not a verbatim reproduction. It replaces SentenceTransformers with an already-installed local Ollama embedding model, uses exact normalized dot products in NumPy, and replaces the book's undefined `claim_supports` placeholder with a deliberately limited exact-span check. This checks textual containment, NOT semantic entailment. That difference is the subject of the experiment, not a claim to have implemented a full verifier.

## Dataset

SQuAD 2.0, Rajpurkar, Jia and Liang (2018), public development data, CC BY-SA 4.0. See https://rajpurkar.github.io/SQuAD-explorer/ and https://creativecommons.org/licenses/by-sa/4.0/.

Questions and Wikipedia passages are retained in the downloaded dataset and the 24-case subset. Subsetting, reformatting and adding topic labels are the changes. Preserve the CC BY-SA attribution when sharing data or dataset-derived materials. `data/provenance.json` records download URL, checksum, subset checksum and exact selection rule.

The industrial motivation is evidence-grounded technical support. The data is a public reading-comprehension proxy, not real customer tickets, a production policy corpus, or a financial-impact study. Each question receives its original parent paragraph. Retrieval chooses two 2-sentence chunks inside that paragraph; this does not measure finding the correct document across a company corpus.

## Novelty check

Read-only GitHub API inventory: 65 public repositories on 2026-09-17. Relevant READMEs were fetched for `chat-with-your-documents`, `tiny-rag-pytorch`, `rag-conversational-ai`, and `ai-learning-repo`.

RAG itself is already represented. Existing projects cover document chat, retrieval implementation, citations and distance-based refusal. This project specifically tests **post-generation exact-span citation checks against adversarially unanswerable questions**, reporting wrong accepted answers and over-refusal in a paired comparison. We do not claim exhaustive inspection of all code or that this is the first RAG evidence-checking implementation.

Published to https://github.com/sravanni369/rag-citation-gate on 2026-09-17 after the evaluation audit described in README.md. No LinkedIn post has been published; LinkedIn-caption.md is a draft.
