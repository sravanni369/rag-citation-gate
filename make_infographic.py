"""Build LinkedIn-infographic-v2.html from the real rag.py (all 50 lines, lines 17-18 highlighted)
and the numbers in results/summary.json. Render with headless Edge at 1080x1350."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).parent
src = (ROOT / 'rag.py').read_text(encoding='utf-8').splitlines()
assert len(src) == 50, len(src)
s = json.loads((ROOT / 'results/summary.json').read_text(encoding='utf-8'))
m = s['methods']
sha = s['frozen_core_sha256'][:8]

KW = re.compile(r'\b(def|if|not|or|and|return|import|as|with|for|in|try|except|raise|any|isinstance|else)\b')
STR = re.compile(r"('(?:[^'\\]|\\.)*')")
CMT = re.compile(r'(#.*)$')
FN = re.compile(r'\b(api|verify|run)\b(?=\()')


def hl(line):
    e = html.escape(line, quote=False)  # keep apostrophes literal so the string regex sees them
    e = STR.sub(r'<span class="st">\1</span>', e)
    e = CMT.sub(r'<span class="cm">\1</span>', e)
    e = KW.sub(r'<span class="kw">\1</span>', e)
    e = FN.sub(r'<span class="nm">\1</span>', e)
    return e


rows = []
for i, l in enumerate(src, 1):
    cls = ' class="fix"' if i in (17, 18) else ''
    rows.append(f'<tr{cls}><td class="n">{i:02d}</td><td>{hl(l)}</td></tr>')
code = '\n'.join(rows)

em = ' · '.join(str(m[k]['exact_match_count']) for k in ('always_refuse', 'baseline', 'gated', 'entail_gated'))
uns = ' → '.join(str(m[k]['unsupported_answers']) for k in ('baseline', 'gated', 'entail_gated'))
ref = ' → '.join(str(m[k]['answerable_refusals']) for k in ('baseline', 'gated', 'entail_gated'))
cp = s['citation_precision']
p_span = s['paired_vs_baseline']['gated']['mcnemar_exact_p']
p_ent = s['paired_vs_baseline']['entail_gated']['mcnemar_exact_p']

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>RAG in 50 lines: a citation is not proof</title>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden;background:#0f62d6}}
body{{font-family:'EB Garamond',Georgia,serif;color:#37425c}}
.frame{{position:absolute;inset:14px;background:#fff;padding:26px 36px 22px}}
.kicker{{font-family:'JetBrains Mono',monospace;font-size:15px;letter-spacing:3px;text-transform:uppercase;color:#0f62d6;font-weight:600}}
h1{{font-size:46px;line-height:1.04;color:#0d1b2a;font-weight:700;margin-top:6px}}
h1 b{{color:#0f62d6}}
.sub{{font-size:19px;color:#44506b;margin-top:6px;line-height:1.28}}
.sub b{{color:#0d1b2a}}
.term{{margin-top:12px;background:#0d1b2a;border:1px solid #1c3355;border-radius:12px;overflow:hidden;font-family:'JetBrains Mono',monospace}}
.bar{{background:#0a1424;padding:7px 12px;display:flex;align-items:center;gap:6px;font-size:12px;color:#7d90ad}}
.dot{{width:10px;height:10px;border-radius:50%}}.r{{background:#ff5f56}}.y{{background:#ffbd2e}}.g{{background:#27c93f}}
.bar .f{{margin-left:8px}}.bar .rt{{margin-left:auto;color:#7d90ad}}
table.code{{border-collapse:collapse;width:100%;font-size:11.6px;line-height:1.28;color:#d6e2f2;font-variant-ligatures:none}}
table.code td{{padding:0 8px;white-space:pre;vertical-align:top}}
table.code td.n{{color:#6b7c96;text-align:right;width:34px;padding-right:10px}}
table.code tr.fix td{{background:rgba(255,204,77,.13)}}
table.code tr.fix td.n{{color:#ffcc4d;font-weight:600}}
.kw{{color:#6fa8ff}}.st{{color:#4fd18b}}.nm{{color:#ffcc4d}}.cm{{color:#6b7c96}}
.fixnote{{font-family:'JetBrains Mono',monospace;font-size:12px;color:#ffcc4d;padding:6px 14px 10px;border-top:1px solid #1c3355}}
.row{{display:flex;gap:18px;margin-top:14px;align-items:stretch}}
.card{{flex:1;border:1px solid;border-radius:14px;padding:12px 16px}}
.c1{{border-color:#0f62d6;background:rgba(15,98,214,.07)}}.c2{{border-color:#12915a;background:rgba(18,145,90,.09)}}.c3{{border-color:#e0a800;background:rgba(224,168,0,.14)}}
.card h2{{font-size:18px;font-weight:700;line-height:1.1;margin-bottom:4px}}
.c1 h2{{color:#0b4bb3}}.c2 h2{{color:#0e7a4b}}.c3 h2{{color:#8a6a00}}
.big{{font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:600;color:#0d1b2a;line-height:1.1}}
.card p{{font-size:15px;line-height:1.25;color:#37425c;margin-top:4px}}
.card p b{{color:#0d1b2a}}
.punch{{margin-top:12px;border-top:1px solid #d7e0ee;padding-top:8px;font-size:19px;line-height:1.22;color:#37425c}}
.punch b{{color:#0e7a4b}}
.foot{{position:absolute;left:36px;right:36px;bottom:14px;border-top:1px solid #d7e0ee;padding-top:7px;display:flex;justify-content:space-between;font-size:14px;color:#5a6472}}
.credit{{font-size:12.5px;color:#5a6472;margin-top:5px;line-height:1.25}}
</style></head><body><div class="frame">
<div class="kicker">Book to business · RAG · Negative result · v2 after audit</div>
<h1>RAG in 50 lines: a <b>citation</b> is not proof</h1>
<div class="sub">The complete <b>rag.py</b>, local Ollama + NumPy, no cloud calls. <b>Lines 17–18 are the fix</b>: v1 compared raw strings while the scorer lowercased, and one "over-refusal" was a capital C.</div>
<div class="term"><div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="f">rag.py · 50 lines · single file · runnable</span><span class="rt">sha256 {sha}…</span></div>
<table class="code">{code}</table>
<div class="fixnote">lines 17–18: case-folded containment — the gate now uses the same normalisation as the scorer that grades it</div></div>
<div class="row">
  <div class="card c1"><h2>Exact match / 24</h2><div class="big">{em}</div><p><b>always refuse</b> · baseline · span gate · entailment gate. The do-nothing policy wins on aggregate; the gates tie or edge the baseline (McNemar p = {p_span:.2f} and {p_ent:.3f}).</p></div>
  <div class="card c2"><h2>Unsupported answers / 12</h2><div class="big">{uns}</div><p>baseline → span gate → <b>entailment gate</b> (book ch. 46). Only <b>{cp['supporting_quotes']} of {cp['quotes']}</b> quoted sentences contain the gold span: a verbatim quote is not evidence.</p></div>
  <div class="card c3"><h2>Refused answerable / 12</h2><div class="big">{ref}</div><p>v1 reported <b>2</b> for the span gate; case-folded it is <b>{m['gated']['answerable_refusals']}</b>, a right answer with the wrong sentence cited. The entailment gate refuses {m['entail_gated']['answerable_refusals']}, one already wrong.</p></div>
</div>
<div class="punch"><b>A copied quote is not proof of support.</b> Neither gate is fit for autonomous answering. Small balanced pilot, correct parent paragraph supplied, n = 24: none of the gaps is significant. The v1 numbers stay in the repo next to these.</div>
<div class="credit">Adapted from Sanjay N T, RAG and Vector Databases (2026), pp. 9, 25, 27, 31. Dataset: SQuAD 2.0, Rajpurkar, Jia and Liang (2018), CC BY-SA 4.0. Code, logs, audit: github.com/sravanni369/rag-citation-gate</div>
<div class="foot"><span>Follow Lakshmi Sravani Putta on LinkedIn</span><span>Book code, run against today's libraries, published with the log</span></div>
</div></body></html>'''
(ROOT / 'LinkedIn-infographic-v2.html').write_text(page, encoding='utf-8')
print('LinkedIn-infographic-v2.html written from rag.py (50 lines) and results/summary.json')
