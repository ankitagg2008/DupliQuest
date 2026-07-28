import requests

url = 'http://localhost:11434'
for endpoint in ['/api/models', '/api/list', '/api/ping', '/api/version', '/api/v1/models']:
    try:
        r = requests.get(url + endpoint, timeout=5)
        print(endpoint, r.status_code, r.text[:400])
    except Exception as e:
        print(endpoint, 'ERROR', e)
