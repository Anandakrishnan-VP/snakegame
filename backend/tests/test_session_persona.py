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

if __name__ == "__main__":
    test_persona_and_turn_history_persistence()
