import base64
import json
import os
from backend.services.vlm_service import analyze_image_with_vlm

with open(r'c:\Users\ABHISHEK\.gemini\antigravity-ide\scratch\snakegame\user_test_helmet.jpg', 'rb') as f:
    b64 = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

res = analyze_image_with_vlm(b64, user_query='', persona='msme')
with open('helmet_result.json', 'w', encoding='utf-8') as out:
    json.dump(res, out, indent=2)
print("COMPLETED")
