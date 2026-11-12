import requests

colis = {
    "entry": [{"changes": [{"value": {"messages": [
        {"from": "243000000000", "type": "text", "text": {"body": "bonjour"}},
        {"from": "243000000000", "type": "text", "text": {"body": "bonjour"}}
    ]}}]}]
}

r = requests.post("http://localhost:5000/webhook", json=colis)
print(r.status_code, r.text)