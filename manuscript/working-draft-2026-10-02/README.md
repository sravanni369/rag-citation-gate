# Working manuscript, 2 October 2026

*A Pilot Study of Citation Gating for Retrieval Augmented Question Answering*, Lakshmi Sravani Putta.

This is a **working draft for author review**. It has not been submitted anywhere.

| File | What it is |
|---|---|
| `rag_citation_gate_working_manuscript.pdf` | Reviewed PDF (7 pages), rendered from the DOCX |
| `rag_citation_gate_working_manuscript.docx` | Editable source of the PDF |
| `rag_citation_gate_latex_source.zip` | Standalone LaTeX version of the same text. Not yet compiled; needs a full TeX install and a layout pass |

## Numbers checked against this repository

Every figure in Table 1 and the results text was checked on 2 October 2026 against `results/summary.json` and `results/audit.json` at commit `5c0ce92`. They all match:

- Exact match: always-refuse 12/24, ungated 9/24, span gate 9/24, model-judged gate 11/24
- Answers returned: 0/24, 24/24, 22/24, 19/24
- Wilson 95% intervals; exact McNemar p = 1.000 (span gate) and 0.625 (model-judged gate)
- Gold-span-in-quote rate 9/24 (37.5%); median latency 5.67 s, p95 9.27 s, judge median 1.13 s

## Still open before any submission

- Confirm the handbook's attribution and redistribution permission (see `SOURCE.md`).
- Final author read-through and approval.
- Final AI-assistance disclosure (Appendix B).
- A stronger, independent evaluation: this is a 24-case exploratory pilot, and the cases were inspected during development.
