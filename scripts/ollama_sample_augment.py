import csv
import json
import os
import requests
from pathlib import Path

BASE = os.environ.get('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
MODEL = os.environ.get('OLLAMA_MODEL', 'qwen3.5')

INPUT = Path('..') / 'DupliQuest' / 'ques' / 'ques_pairs.csv'
OUTPUT = Path('data') / 'processed' / 'augmented_sample_qwen3.5.csv'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

def stream_generate(prompt: str, model: str = MODEL, timeout: int = 120) -> str:
    url = f"{BASE}/api/generate"
    payload = {"model": model, "prompt": prompt}
    try:
        with requests.post(url, json=payload, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            collected = []
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                line = line.strip()
                # lines may be raw JSON objects per line
                try:
                    obj = json.loads(line)
                except Exception:
                    # sometimes servers prefix 'data:'
                    if line.startswith('data:'):
                        try:
                            obj = json.loads(line[len('data:'):].strip())
                        except Exception:
                            continue
                    else:
                        continue
                # prefer 'response' then 'thinking' payloads
                if isinstance(obj, dict):
                    if obj.get('response'):
                        collected.append(obj['response'])
                    elif obj.get('thinking'):
                        collected.append(obj['thinking'])
                    elif obj.get('payload') and isinstance(obj['payload'], dict):
                        txt = obj['payload'].get('text') or obj['payload'].get('content')
                        if txt:
                            collected.append(txt)
            return ''.join(collected).strip()
    except Exception as e:
        raise


def main(sample_size: int = 5):
    rows = []
    with INPUT.open('r', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for i, r in enumerate(reader):
            if i >= sample_size:
                break
            rows.append(r)

    out_rows = []
    for r in rows:
        q1 = r.get('question1', '')
        prompt = (
            "Generate 1 high-quality paraphrase for the following question, keeping the meaning unchanged.\n\n"
            f"Question: {q1}\n\nParaphrase:"
        )
        try:
            text = stream_generate(prompt)
            if not text:
                text = q1
        except Exception as e:
            text = q1
        out_rows.append({
            'id': f"aug-{r.get('id','')}",
            'question1': text,
            'question2': r.get('question2',''),
            'is_duplicate': r.get('is_duplicate','0'),
            'semantic_label': 'paraphrase',
            'label_reason': 'ollama_qwen3.5_sample',
            'source_dataset': INPUT.name,
            'split': r.get('split','train'),
        })

    fieldnames = ['id','question1','question2','is_duplicate','semantic_label','label_reason','source_dataset','split']
    with OUTPUT.open('w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in out_rows:
            writer.writerow(row)
    print('Wrote sample augmented file:', OUTPUT)

if __name__ == '__main__':
    main()
