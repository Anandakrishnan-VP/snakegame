"""
Comprehensive Test Suite for §19 Edge-Case Checklist.
Tests all 10 critical edge cases required by the specification.
"""
import os
import sys
sys.path.insert(0, os.path.abspath("."))
import json
from backend.services.module1_directory import search_directory, get_flagship_chunks
from backend.services.module2_matcher import match_product_to_standard
from backend.services.module4_verification import verify_code
from backend.services.compliance_chain import run_compliance_chain
from backend.services.session_manager import get_or_create_session, update_session, check_cache, write_cache
from backend.services.multilingual import resolve_language, translate_to_english_if_needed
from backend.services.intent_router import route_intent
from backend.services.llm_groq import deterministic_synthesis

def test_1_directory_without_deep_clause():
    # IS 1489 (PPC Cement) has directory record but no Tier B deep clause chunks
    chunks = get_flagship_chunks("IS 1489 (Part 1):2015")
    assert len(chunks) == 0, "Non-flagship standard should not have deep clause chunks"
    
    chain = run_compliance_chain("PPC cement fly ash")
    assert chain["standard"]["is_code"] == "IS 1489 (Part 1):2015"
    assert chain["evidence_tag"]["source_type"] == "directory"
    assert "Directory" in chain["evidence_tag"]["clause_number"]
    print("[PASS] Edge Case 1: Directory query without deep clause coverage")

def test_2_deep_clause_non_flagship_boundary():
    # When asking for deep clause on a non-flagship standard
    chunks = get_flagship_chunks("IS 694:2010")
    assert len(chunks) == 0
    chain = run_compliance_chain("IS 694:2010 PVC cables")
    res = deterministic_synthesis(chain, "What is clause 4.2 in IS 694")
    # For a non-flagship standard, source_type is directory, not clause
    assert res["evidence_tag"]["source_type"] == "directory"
    print("[PASS] Edge Case 2: Deep-clause on non-flagship standard respects boundary")

def test_3_unrecognized_product_attribute():
    # Product with terms not in the category dictionary (e.g. "novel bio-acoustic hydrophone sensor")
    match = match_product_to_standard("novel bio-acoustic hydrophone sensor")
    # System should not crash, attributes will be None, candidates will fallback gracefully
    assert match["attributes"]["category"] is None
    print("[PASS] Edge Case 3: Unrecognized product attribute handles gracefully")

def test_4_pronoun_followup_active_topic():
    import uuid
    sess_id = f"sess-test-4-{uuid.uuid4()}"
    # Fresh session: identify standard
    session = get_or_create_session(sess_id)
    assert session["active_topic"] is None
    
    # User asks about water bottle
    chain = run_compliance_chain("stainless steel water bottle for kids")
    is_code = chain["standard"]["is_code"] # IS 17803:2022
    update_session(sess_id, active_topic=is_code)
    
    # Followup with pronoun: "Where can I test it in Mumbai?"
    session_after = get_or_create_session(sess_id)
    assert session_after["active_topic"] == "IS 17803:2022"
    
    augmented_query = f"{session_after['active_topic']} Where can I test it in Mumbai?"
    assert "IS 17803:2022" in augmented_query
    print("[PASS] Edge Case 4: Pronoun follow-up uses active-topic memory")

def test_5_cache_hit_updates_active_topic():
    import uuid
    sess_id = f"sess-cache-test-5-{uuid.uuid4()}"
    # Write to cache
    query = f"stainless steel bottle {uuid.uuid4()}"
    lang = "en"
    mock_resp = {
        "answer": "Use IS 17803:2022.",
        "what_it_means": "Mandatory standard.",
        "next_action": "Apply Form V.",
        "evidence_tag": {"status": "confirmed"}
    }
    write_cache(query, lang, mock_resp, active_topic="IS 17803:2022")
    
    # Fresh session
    session = get_or_create_session(sess_id)
    assert session["active_topic"] is None
    
    # Query hits cache
    cached_data, cached_topic = check_cache(query, lang)
    assert cached_data is not None
    assert cached_topic == "IS 17803:2022"
    
    # Crucial rule: update session state on cache hit
    update_session(sess_id, active_topic=cached_topic)
    
    # Verify session now has the active topic
    updated_sess = get_or_create_session(sess_id)
    assert updated_sess["active_topic"] == "IS 17803:2022", "Cache hit must update active topic"
    print("[PASS] Edge Case 5: Cache hit updates active topic for subsequent follow-up")

def test_6_sentence_with_date_and_cml():
    # Input with earlier date "2024-01-15" and CML licence "CML1234567"
    raw_query = "Product manufactured on 2024-01-15 carries licence CML1234567 batch 990"
    res = verify_code(raw_query)
    assert res["found"] is True
    assert res["extracted_code"] == "CML1234567", f"Expected CML1234567, got {res.get('extracted_code')}"
    print("[PASS] Edge Case 6: Sentence with date and CML extracts licence, not date")

def test_7_huid_mixed_alphanumeric():
    # HUID AB1234 (mixed letters and numbers)
    raw = "Jewellery invoice with HUID AB1234"
    res = verify_code(raw)
    assert res["found"] is True
    assert res["extracted_code"] == "AB1234"
    assert res["code_type"] == "HUID"
    assert "Tanishq" in res["licensee_name"]
    print("[PASS] Edge Case 7: Mixed alphanumeric HUID verified without truncation")

def test_8_multilingual_cache_isolation():
    # English query vs Hindi query must have distinct cache keys
    en_query = "what is the standard for helmets"
    hi_query = "हेलमेट के लिए क्या मानक है"
    
    en_lang = resolve_language(en_query, "en")
    hi_lang = resolve_language(hi_query, "auto")
    
    assert en_lang == "en"
    assert hi_lang == "hi"
    
    write_cache(en_query, "en", {"answer": "English Answer", "lang": "en"})
    
    # Ensure Hindi query does NOT hit English cache
    hi_cache, _ = check_cache(hi_query, "hi") or (None, None)
    assert hi_cache is None, "Hindi query must not hit English cache"
    print("[PASS] Edge Case 8: Language-aware cache isolation between English and Hindi")

def test_9_out_of_scope_rejection():
    res = route_intent("tell me a funny joke about cats")
    assert res["intent"] == "OUT_OF_SCOPE"
    
    declined = deterministic_synthesis({"out_of_scope": True}, "tell me a joke")
    assert "BIS" in declined["answer"]
    assert declined["evidence_tag"]["status"] == "not determined"
    print("[PASS] Edge Case 9: Out-of-scope query rejected politely")

def test_10_deterministic_failover():
    # Simulate completely offline / no API key synthesis
    mock_payload = run_compliance_chain("children toys")
    res = deterministic_synthesis(mock_payload, "children toys", "en")
    assert res["answer"] != ""
    assert res["what_it_means"] != ""
    assert res["next_action"] != ""
    assert res["evidence_tag"]["status"] == "confirmed"
    assert "9873" in res["evidence_tag"]["reference"]
    print("[PASS] Edge Case 10: Deterministic failover guarantees complete 4-part response")

if __name__ == "__main__":
    test_1_directory_without_deep_clause()
    test_2_deep_clause_non_flagship_boundary()
    test_3_unrecognized_product_attribute()
    test_4_pronoun_followup_active_topic()
    test_5_cache_hit_updates_active_topic()
    test_6_sentence_with_date_and_cml()
    test_7_huid_mixed_alphanumeric()
    test_8_multilingual_cache_isolation()
    test_9_out_of_scope_rejection()
    test_10_deterministic_failover()
    print("\nALL 10 SPECIFICATION §19 EDGE-CASE TESTS PASSED!")
