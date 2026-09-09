"""
End-to-end API integration tests using FastAPI TestClient.
Verifies all HTTP endpoints, JSON formats, and headers.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
    print("[PASS] GET /api/health")

def test_verify_endpoints():
    # 1. Valid CM/L
    res = client.post("/api/verify", json={"code": "CML1234567"})
    assert res.status_code == 200
    data = res.json()
    assert data["found"] is True
    assert "Milton" in data["licensee_name"]

    # 2. Valid HUID
    res = client.post("/api/verify", json={"code": "AB1234"})
    assert res.status_code == 200
    assert res.json()["found"] is True
    assert res.json()["code_type"] == "HUID"

    # 3. Invalid code
    res = client.post("/api/verify", json={"code": "XYZ99999"})
    assert res.status_code == 200
    assert res.json()["found"] is False
    print("[PASS] POST /api/verify")

def test_directory_endpoint():
    res = client.get("/api/directory?search=helmet")
    assert res.status_code == 200
    items = res.json()
    assert len(items) > 0
    assert any("4151" in item["is_code"] for item in items)
    print("[PASS] GET /api/directory")

def test_labs_endpoint():
    res = client.get("/api/labs?is_code=IS 17803:2022&city=Mumbai")
    assert res.status_code == 200
    labs = res.json()
    assert len(labs) > 0
    assert labs[0]["city"] == "Mumbai"
    print("[PASS] GET /api/labs")

def test_clause_inspector_endpoint():
    res = client.get("/api/clause/IS9873-P1-C4.2")
    assert res.status_code == 200
    clause = res.json()
    assert clause["chunk_id"] == "IS9873-P1-C4.2"
    assert "choking hazards" in clause["content"].lower()
    print("[PASS] GET /api/clause/{chunk_id}")

def test_chat_flow_and_pronoun():
    # Turn 1: Product description
    res1 = client.post("/api/chat", json={
        "query": "I am manufacturing stainless steel vacuum flasks for children",
        "session_id": "api-test-session-1",
        "persona": "msme"
    })
    assert res1.status_code == 200
    d1 = res1.json()
    assert "17803" in str(d1)
    assert d1["evidence_tag"]["status"] == "confirmed"
    assert d1["active_topic"] is not None

    # Turn 2: Followup with pronoun
    res2 = client.post("/api/chat", json={
        "query": "Where is the testing lab for it in Mumbai?",
        "session_id": "api-test-session-1",
        "city": "Mumbai"
    })
    assert res2.status_code == 200
    d2 = res2.json()
    assert "17803" in d2["active_topic"]

    # Turn 3: Cache hit
    res3 = client.post("/api/chat", json={
        "query": "I am manufacturing stainless steel vacuum flasks for children",
        "session_id": "api-test-session-1"
    })
    assert res3.status_code == 200
    assert res3.json().get("from_cache") is True
    print("[PASS] POST /api/chat with memory and cache")

def test_chat_hindi():
    res = client.post("/api/chat", json={
        "query": "खिलौनों के लिए क्या नियम हैं?",
        "language": "hi"
    })
    assert res.status_code == 200
    d = res.json()
    assert d["resolved_language"] == "hi"
    assert "9873" in str(d)
    print("[PASS] POST /api/chat Hindi support")

if __name__ == "__main__":
    test_health()
    test_verify_endpoints()
    test_directory_endpoint()
    test_labs_endpoint()
    test_clause_inspector_endpoint()
    test_chat_flow_and_pronoun()
    test_chat_hindi()
    print("\nALL API ENDPOINT INTEGRATION TESTS PASSED!")
