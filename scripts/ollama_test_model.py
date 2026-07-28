import os
import requests

base = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
model = os.environ.get('OLLAMA_MODEL', 'qwen3.5')
print('Base URL:', base)
print('Model:', model)

endpoints = [
    '/api/generate',
    '/api/v1/generate',
    '/api/v1/completions',
    '/api/generate?model=' + model,
    '/api/generate?model=' + model + '&stream=false',
]

payloads = [
    {'prompt': 'Say hello in one sentence.'},
    {'model': model, 'prompt': 'Say hello in one sentence.'},
    {'model': model, 'messages': [{'role': 'user', 'content': 'Say hello in one sentence.'}]},
    {'model': model, 'text': 'Say hello in one sentence.'},
    {'model': model, 'input': 'Say hello in one sentence.'},
]

for endpoint in endpoints:
    for payload in payloads:
        url = base + endpoint
        try:
            r = requests.post(url, json=payload, timeout=10)
            print('URL:', url)
            print('Payload:', payload)
            print('Status:', r.status_code)
            print('Response:', r.text[:800])
        except Exception as e:
            print('URL:', url)
            print('Payload:', payload)
            print('ERROR:', repr(e))
        print('-' * 80)
