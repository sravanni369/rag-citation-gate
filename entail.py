"""Claim verifier from the book's chapter 46: does the cited passage actually support the
answer, judged semantically rather than by string containment. The book leaves
`claim_supports` undefined; this is one deliberately small implementation of it using the
same local model as the generator, at temperature 0. It is a second opinion from the same
model family, not an independent NLI model, and that limit is stated in the README."""
import json
from rag import api

SYSTEM = ('You are a strict fact checker. You receive a question, a proposed answer and one quoted '
          'passage. Reply with JSON {"supported": true} only if the passage, read on its own, states '
          'that the proposed answer is the answer to the question. Paraphrase counts; inference '
          'beyond the passage does not. Otherwise reply {"supported": false}.')


def claim_supports(question, answer, quote):
    """Return (bool, raw_json). Empty answer or quote is never supported."""
    if not (isinstance(answer, str) and isinstance(quote, str) and answer.strip() and quote.strip()):
        return False, ''
    response = api('chat', {'model': 'qwen2.5-coder:3b', 'stream': False, 'format': 'json',
        'options': {'temperature': 0, 'seed': 42, 'num_predict': 40, 'num_ctx': 2048},
        'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user',
        'content': json.dumps({'question': question, 'answer': answer, 'passage': quote})}]})
    raw = response['message']['content']
    try:
        return bool(json.loads(raw).get('supported') is True), raw
    except (ValueError, AttributeError):
        return False, raw
