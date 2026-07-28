import requests

url_base = 'http://localhost:11434'
print('Base URL:', url_base)
endpoints = [
    '/api/version',
    '/api/models',
    '/api/list',
    '/api/ping',
    '/api/v1/models',
    '/api/v1/list',
    '/api/v1/ping',
    '/api/model',
    '/api/llms',
]
for endpoint in endpoints:
    try:
        r = requests.get(url_base + endpoint, timeout=5)
        print(endpoint, 'GET', r.status_code, r.text[:500])
    except Exception as e:
        print(endpoint, 'GET ERROR', e)

for endpoint in ['/api/generate?model=qwen3.5', '/api/v1/generate?model=qwen3.5', '/api/v1/completions?model=qwen3.5']:
    try:
        r = requests.post(url_base + endpoint, json={'prompt': 'Hello'}, timeout=5)
        print(endpoint, 'POST', r.status_code, r.text[:500])
    except Exception as e:
        print(endpoint, 'POST ERROR', e)
