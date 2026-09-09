"""
Test Multilingual Answer Generation (§Post-Build Issue 6).
Verifies:
1. When asked in English: answers cleanly in English with exact IS code.
2. When asked in Hindi: answers directly in natural Hindi (Devanagari) using English-retrieved context.
3. IS codes (e.g. 'IS 9873 (Part 1):2019'), clause numbers, and numeric values remain untouched and uncorrupted.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_multilingual_direct_generation():
    # 1. English query
    en_query = "What is the standard for toys?"
    res_en = client.post("/api/chat", json={"query": en_query, "language": "en"})
    assert res_en.status_code == 200
    data_en = res_en.json()

    print("\n--- English Response ---")
    print(f"Answer: {data_en['answer']}")
    print(f"What it means: {data_en['what_it_means']}")
    print(f"Next action: {data_en['next_action']}")

    # 2. Hindi query for same product
    hi_query = "खिलौनों के लिए कौन सा भारतीय मानक लागू है?"
    res_hi = client.post("/api/chat", json={"query": hi_query, "language": "hi"})
    assert res_hi.status_code == 200
    data_hi = res_hi.json()

    print("\n--- Hindi Response ---")
    try:
        print(f"Answer: {data_hi['answer']}")
    except UnicodeEncodeError:
        print(f"Answer (UTF-8): {data_hi['answer'].encode('utf-8')}")

    # Verify IS code preservation
    is_code = "IS 9873 (Part 1):2019"
    assert is_code in data_en["answer"], f"Expected {is_code} in English answer"
    assert is_code in data_hi["answer"], f"Expected {is_code} untouched in Hindi answer"

    # Verify language resolution
    assert data_en["resolved_language"] == "en"
    assert data_hi["resolved_language"] == "hi"

    # Verify Hindi text is in Devanagari
    import re
    has_devanagari = bool(re.search(r'[\u0900-\u097F]', data_hi["answer"]))
    assert has_devanagari, "Expected Hindi answer to contain Devanagari characters"

    print("\nMultilingual direct generation test PASSED successfully!")

if __name__ == "__main__":
    test_multilingual_direct_generation()
