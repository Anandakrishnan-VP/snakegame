"""
Test session_state persistence (§Post-Build Issue 4).
Verifies:
1. Setting persona to "Industry/MSME" persists in session_state table in SQLite.
2. Restarting / reloading session with the same session_id returns the persisted persona.
3. Turn history is recorded in session_state.turn_history JSON column.
"""

import uuid
from backend.services.session_manager import get_or_create_session, update_session
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_persona_and_turn_history_persistence():
    session_id = f"test-sess-{uuid.uuid4().hex[:8]}"

    # Step 1: Send a chat request setting persona to 'Industry/MSME'
    res1 = client.post("/api/chat", json={
        "query": "What is the certification process for toys?",
        "session_id": session_id,
        "persona": "Industry/MSME",
        "language": "en"
    })
    assert res1.status_code == 200, f"Chat failed: {res1.text}"

    # Step 2: Simulate session restart / retrieval using the same session_id
    # get_or_create_session without specifying persona defaults to 'general',
    # so it MUST retrieve the existing 'Industry/MSME' from SQLite!
    reloaded_session = get_or_create_session(session_id)
    
    print("\n[Session Reload Verification]")
    print(f"  Session ID: {reloaded_session['session_id']}")
    print(f"  Persona: {reloaded_session['persona']}")
    print(f"  Turn Count: {reloaded_session['turn_count']}")
    print(f"  Turn History: {reloaded_session['turn_history']}")

    assert reloaded_session["persona"] == "Industry/MSME", (
        f"Expected persona 'Industry/MSME' to persist, got '{reloaded_session['persona']}'"
    )
    assert reloaded_session["turn_count"] >= 1, "Turn count was not incremented"
    assert len(reloaded_session["turn_history"]) >= 1, "Turn history was not recorded"
    assert reloaded_session["turn_history"][0]["query"] == "What is the certification process for toys?"

    # Step 3: Test via the /api/session endpoint
    api_res = client.get(f"/api/session/{session_id}")
    assert api_res.status_code == 200
    api_data = api_res.json()
    assert api_data["persona"] == "Industry/MSME"
    assert len(api_data["turn_history"]) >= 1

    print("\nSession persistence test PASSED successfully!")

def test_cross_session_live_chat_isolation():
    sess_a = f"test-sess-a-{uuid.uuid4().hex[:8]}"
    sess_b = f"test-sess-b-{uuid.uuid4().hex[:8]}"

    # Turn 1: Session A asks about bottle
    res_a1 = client.post("/api/chat", json={
        "query": "stainless steel water bottle",
        "session_id": sess_a,
        "persona": "general",
        "language": "en"
    })
    assert res_a1.status_code == 200
    data_a1 = res_a1.json()
    assert "17803" in (data_a1.get("active_topic") or "") or "17803" in json.dumps(data_a1)

    # Turn 2: Session A asks generic follow-up "where can I get it tested?"
    res_a2 = client.post("/api/chat", json={
        "query": "where can I get it tested?",
        "session_id": sess_a,
        "persona": "general",
        "language": "en"
    })
    assert res_a2.status_code == 200
    data_a2 = res_a2.json()
    assert data_a2["intent"] == "LAB_SEARCH"
    assert data_a2.get("active_topic") == "IS 17803:2022"

    # Turn 1: Session B asks about helmets
    res_b1 = client.post("/api/chat", json={
        "query": "two wheeler helmet standards",
        "session_id": sess_b,
        "persona": "general",
        "language": "en"
    })
    assert res_b1.status_code == 200
    data_b1 = res_b1.json()
    assert "4151" in (data_b1.get("active_topic") or "") or "4151" in json.dumps(data_b1)

    # Turn 2: Session B asks the EXACT SAME generic follow-up "where can I get it tested?"
    res_b2 = client.post("/api/chat", json={
        "query": "where can I get it tested?",
        "session_id": sess_b,
        "persona": "general",
        "language": "en"
    })
    assert res_b2.status_code == 200
    data_b2 = res_b2.json()

    # Session B MUST NOT get Session A's cached bottle answer!
    assert data_b2["intent"] == "LAB_SEARCH", f"Expected LAB_SEARCH, got {data_b2['intent']}"
    assert "No registered Indian Standard found" not in json.dumps(data_b2), "Must not return 'No standard found' error"
    assert data_b2.get("active_topic") == "IS 4151:2015", f"Expected active_topic IS 4151:2015, got {data_b2.get('active_topic')}"
    
    # Session B state in SQLite must still be helmets
    sess_b_db = get_or_create_session(sess_b)
    assert sess_b_db["active_topic"] == "IS 4151:2015", f"Session B DB active_topic poisoned: {sess_b_db['active_topic']}"

    print("\nCross-session live chat isolation test PASSED successfully!")

if __name__ == "__main__":
    import json
    test_persona_and_turn_history_persistence()
    test_cross_session_live_chat_isolation()
