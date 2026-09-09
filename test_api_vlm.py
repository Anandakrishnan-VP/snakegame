import urllib.request
import json
import base64

with open(r'c:\Users\ABHISHEK\.gemini\antigravity-ide\scratch\snakegame\user_test_helmet.jpg', 'rb') as f:
    b64 = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

payload = {
    "image_base64": b64,
    "query": "Please inspect this product image, detect any visible ISI mark, CM/L number, Hallmark or HUID, and provide the compliance and quality details under Indian Standards.",
    "persona": "msme",
    "language": "en"
}

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/vision/analyze',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("DETECTED PRODUCT:", data.get("detected_product"))
        print("IS CODE:", data.get("is_code"))
        print("ANSWER:", data.get("answer"))
        print("WHAT IT MEANS:", data.get("what_it_means"))
        print("EVIDENCE TAG:", data.get("evidence_tag"))
except Exception as e:
    print("ERROR:", e)
