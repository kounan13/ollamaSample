import requests
import json

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama2",
    "prompt": "こんにちは！"
}
response = requests.post(url, json=payload)
for line in response.text.splitlines():
    try:
        print(json.loads(line))
    except Exception:
        print(line)
