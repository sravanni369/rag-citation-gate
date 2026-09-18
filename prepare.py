"""Freeze a small balanced technical benchmark before model evaluation."""
import hashlib, json, urllib.request
from pathlib import Path
ROOT = Path(__file__).parent
source = ROOT / 'data/dev-v2.0.json'
data = json.loads(source.read_text(encoding='utf-8'))
topics = ['Computational_complexity_theory', 'Packet_switching', 'Steam_engine']
rows = []
for article in data['data']:
    if article['title'] not in topics:
        continue
    for impossible in (False, True):
        candidates = []
        for p in article['paragraphs']:
            questions = [q for q in p['qas'] if q['is_impossible'] == impossible]
            if questions:
                q = sorted(questions, key=lambda x: hashlib.sha256(x['id'].encode()).hexdigest())[0]
                candidates.append({'id': q['id'], 'topic': article['title'], 'question': q['question'],
                    'context': p['context'], 'unanswerable': impossible,
                    'answers': [a['text'] for a in q['answers']]})
        candidates.sort(key=lambda x: hashlib.sha256(x['id'].encode()).hexdigest())
        rows += candidates[:4]
assert len(rows) == 24 and sum(r['unanswerable'] for r in rows) == 12
target = ROOT / 'data/evaluation.json'
target.write_text(json.dumps(rows, indent=2), encoding='utf-8')
manifest = {'source': 'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json',
    'license': 'CC BY-SA 4.0', 'dataset': 'SQuAD 2.0', 'downloaded': '2026-09-17',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'subset_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
    'sampling': '3 technical articles; 4 answerable and 4 impossible questions per article; hash-order selection',
    'scope': 'Oracle parent paragraph; dense retrieval over 2-sentence chunks within that paragraph.',
    'protocol': 'No tuning. One fixed prompt, one generator call per case; paired baseline and post-gate outputs.',
    'limitation': '24-case public-development-set pilot, not a hidden test or real support dataset. Model may have seen SQuAD.'}
(ROOT / 'data/provenance.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print('Frozen 24 cases: 12 answerable + 12 unanswerable.')
