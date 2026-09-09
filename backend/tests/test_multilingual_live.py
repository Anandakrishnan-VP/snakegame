import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_chat(title, query, lang):
    url = 'http://127.0.0.1:8000/api/chat'
    data = json.dumps({'query': query, 'language': lang, 'persona': 'msme'}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            print(f"=== {title} ===")
            print(f"Input: '{query}' | Page Lang: {lang}")
            print(f"Intent: {res.get('intent')} | Active Topic: {res.get('active_topic')}")
            print(f"Answer:\n{res.get('answer', '')}")
            print("=" * 60)
    except Exception as e:
        print(f"Error for {query}: {e}")

if __name__ == "__main__":
    # Case 1: Tamil input, Page lang Tamil
    test_chat("Case 1: Tamil Input + Page Lang Tamil", "குழந்தைகளுக்கான பொம்மைகளுக்கான தரநிலை என்ன?", "ta")

    # Case 2: English input, Page lang Tamil
    test_chat("Case 2: English Input + Page Lang Tamil", "What is the standard for electric ceiling fans?", "ta")

    # Case 3: Telugu input, Page lang English
    test_chat("Case 3: Telugu Input + Page Lang English", "ప్యాక్ చేసిన తాగునీటి ప్రమాణం ఏమిటి?", "en")

    # Case 4: English input, Page lang Hindi
    test_chat("Case 4: English Input + Page Lang Hindi", "What is the standard for toys safety?", "hi")
