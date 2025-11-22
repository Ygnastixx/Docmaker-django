import requests
import json

url_render = "http://localhost:8000/api/documents/render/"
url_prefill = "http://localhost:8000/api/documents/prefill/"

params = {
        "context": json.dumps({"id": 4}),
        "business_code": "profile"
    }

response_prefill = requests.get(url_prefill, params=params)

print("Status:", response_prefill.status_code)
print("Response:", response_prefill.text)

payload = {field["name"]: field["value"] for field in response_prefill.json()["fields"]}

print("payload:", payload)

response_render = requests.post(url_render, json={"business_code": "profile", "context": payload})

print("Status:", response_render.status_code)
print("Response:", response_render.text)
