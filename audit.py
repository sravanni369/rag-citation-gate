"""Independent checks of saved outputs; no model-quality pass threshold.

The audit recomputes the gate with its own case-folded containment (it must match the
scorer's normalisation, which is what the v1 audit failed to check) and reports every
stored v1 decision that differs, then recomputes every count in summary.json."""
import hashlib, json, re, string
from pathlib import Path
from rag import run, verify
ROOT = Path(__file__).parent
records = [json.loads(x) for x in (ROOT/'results/predictions.jsonl').read_text().splitlines()]
ent = {json.loads(l)['id']: json.loads(l) for l in (ROOT/'results/entailment.jsonl').read_text().splitlines()}
frozen = json.loads((ROOT/'results/frozen_protocol.json').read_text())
for name, digest in frozen.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
assert len(records) == 24 and len(ent) == 24
def normalize(s):
    s = ''.join(c for c in s.lower() if c not in string.punctuation)
    return ' '.join(re.sub(r'\b(a|an|the)\b', ' ', s).split())
checks, v1_diffs = [], []
for row in records:
    a, q = row['baseline'], row['quote']
    expected = isinstance(a, str) and isinstance(q, str) and bool(a.strip()) and bool(q.strip())
    expected = expected and a.strip().lower() in q.strip().lower()
    expected = expected and any(q.strip().lower() in p.lower() for p in row['evidence'])
    assert verify(a, q, row['evidence']) == bool(expected)
    if row['accepted'] != bool(expected):
        v1_diffs.append({'id': row['id'], 'stored_v1': row['accepted'], 'case_folded': bool(expected), 'answer': a, 'quote': q[:80]})
    assert all(p in row['context'] for p in row['evidence'])
checks.append('Independently recomputed every gate decision with case-folded containment and compared with rag.verify')
checks.append(f'{len(v1_diffs)} stored v1 (case-sensitive) decision(s) differ from the case-folded gate')
repeat = []
for row in (records[0], records[4]):
    rerun = run(row['question'], row['context'])
    same = all(rerun[k] == row[k] for k in ['baseline', 'quote', 'chunk_ids'])
    repeat.append({'id': row['id'], 'same': same})
checks.append('Repeated two preselected cases; see individual results')
summary = json.loads((ROOT/'results/summary.json').read_text())
preds = {'always_refuse': lambda r: '', 'baseline': lambda r: r['baseline'],
         'gated': lambda r: r['baseline'] if verify(r['baseline'], r['quote'], r['evidence']) else '',
         'entail_gated': lambda r: r['baseline'] if ent[r['id']]['supported'] else ''}
for method, metrics in summary['methods'].items():
    fn = preds[method]
    assert metrics['unsupported_answers'] == len([r for r in records if r['unanswerable'] and fn(r).strip()]), method
    assert metrics['answerable_refusals'] == len([r for r in records if not r['unanswerable'] and not fn(r).strip()]), method
    assert metrics['answered'] == len([r for r in records if fn(r).strip()]), method
    em = sum(max(float(normalize(fn(r)) == normalize(g)) for g in (r['answers'] or [''])) for r in records)
    assert metrics['exact_match_count'] == int(em), method
checks.append('Recomputed count-based and exact-match metrics for all four methods independently')
quotes = [r for r in records if isinstance(r['quote'], str) and r['quote'].strip()]
sup = [r for r in quotes if any(normalize(g) and normalize(g) in normalize(r['quote']) for g in r['answers'])]
assert summary['citation_precision']['supporting_quotes'] == len(sup) and summary['citation_precision']['quotes'] == len(quotes)
checks.append('Recomputed citation precision (book ch. 38) independently')
report = {'status': 'PASS', 'checks': checks, 'v1_decisions_changed_by_case_fold': v1_diffs, 'repeatability': repeat,
          'scope': 'Implementation and arithmetic verification. Does not certify model correctness.'}
(ROOT/'results/audit.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
