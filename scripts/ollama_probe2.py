import requests

url_base = 'http://localhost:11434'

for endpoint in ['/api/generate', '/api/v1/completions', '/api/v1/generate']:
    for payload in [
        {'model': 'qwen3.5', 'prompt': 'Hello'},
        {'model': 'qwen3.5', 'messages': [{'role': 'user', 'content': 'Hello'}]},
        {'model': 'qwen3.5', 'text': 'Hello'},
        {'model': 'qwen3.5', 'input': 'Hello'},
    ]:
        try:
            r = requests.post(url_base + endpoint, json=payload, timeout=10)
            print('endpoint', endpoint, 'payload', payload)
            print('status', r.status_code)
            print(r.text[:600])
        except Exception as e:
            print('endpoint', endpoint, 'payload', payload, 'ERROR', e)
