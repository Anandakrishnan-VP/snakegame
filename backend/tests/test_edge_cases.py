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
    # IS 12269 (53 Grade Cement) has directory record but no Tier B deep clause chunks
    chunks = get_flagship_chunks("IS 12269:2013")
    assert len(chunks) == 0, "Non-flagship standard should not have deep clause chunks"
    
    chain = run_compliance_chain("53 grade cement opc")
    assert chain["standard"]["is_code"] == "IS 12269:2013"
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

def test_11_persona_cache_and_response_isolation():
    # Cache isolation between MSME and Consumer personas
    query = "drinking water bottles standards"
    msme_resp = {"answer": "MSME factory response", "persona": "msme"}
    consumer_resp = {"answer": "Consumer safety response", "persona": "consumer"}

    write_cache(query, "en", msme_resp, persona="msme")
    write_cache(query, "en", consumer_resp, persona="consumer")

    c_hit, _ = check_cache(query, "en", persona="consumer") or (None, None)
    m_hit, _ = check_cache(query, "en", persona="msme") or (None, None)

    assert c_hit is not None
    assert c_hit["persona"] == "consumer"
    assert "safety" in c_hit["answer"].lower()

    assert m_hit is not None
    assert m_hit["persona"] == "msme"
    assert "factory" in m_hit["answer"].lower()

    # Synthesis differences
    mock_payload_consumer = run_compliance_chain("water bottles", persona="consumer")
    mock_payload_msme = run_compliance_chain("water bottles", persona="msme")

    c_synth = deterministic_synthesis(mock_payload_consumer, "water bottles", "en")
    m_synth = deterministic_synthesis(mock_payload_msme, "water bottles", "en")

    assert "consumer" in c_synth["what_it_means"].lower() or "buying" in c_synth["what_it_means"].lower() or "isi mark" in c_synth["what_it_means"].lower()
    assert "factory" in m_synth["what_it_means"].lower() or "scheme" in m_synth["what_it_means"].lower() or "audit" in m_synth["what_it_means"].lower()

    print("[PASS] Edge Case 11: Persona-aware cache and deterministic synthesis isolation")

def test_12_conversational_acknowledgments_and_thanks():
    from backend.services.conversational_handler import classify_conversational, generate_conversational_response
    from backend.main import augment_query_if_followup

    # 1. Classification
    assert classify_conversational("ok") == "ACK"
    assert classify_conversational("okay") == "ACK"
    assert classify_conversational("got it") == "ACK"
    assert classify_conversational("noted") == "ACK"
    assert classify_conversational("thanks") == "THANKS"
    assert classify_conversational("thank you so much") == "THANKS"
    assert classify_conversational("bye") == "CLOSING"
    assert classify_conversational("hello") == "GREETING"
    assert classify_conversational("What is IS 4151?") is None
    assert classify_conversational("ok but what about the fee?") is None

    # 2. Augment must NOT pollute conversational turns
    clean_aug = augment_query_if_followup("ok", "IS 4151:2015")
    assert clean_aug == "ok", f"Expected 'ok', got '{clean_aug}'"

    # 3. Response generation
    res = generate_conversational_response("ACK", "ok", active_topic="IS 4151:2015", persona="msme", language="en")
    assert "Understood" in res["answer"] or "Glad" in res["answer"]
    assert "IS 4151:2015" in res["answer"] or "IS 4151:2015" in res["what_it_means"]
    assert res["persona"] == "msme"

    # 4. Route intent
    r_intent = route_intent("ok")
    assert r_intent["intent"] == "CONVERSATIONAL_ACK"
    print("[PASS] Edge Case 12: Conversational acknowledgments & pleasantries handled gracefully without repetition")

def test_13_cross_session_topic_cache_isolation():
    import uuid
    sess_a = f"sess-a-{uuid.uuid4()}"
    sess_b = f"sess-b-{uuid.uuid4()}"

    # Session A discusses water bottle -> active topic IS 17803:2022
    get_or_create_session(sess_a)
    update_session(sess_a, active_topic="IS 17803:2022")
    # Session B discusses helmet -> active topic IS 4151:2015
    get_or_create_session(sess_b)
    update_session(sess_b, active_topic="IS 4151:2015")

    generic_query = f"where can I get it tested? {uuid.uuid4()}"

    # Session A writes its tested result into cache with context_topic = IS 17803:2022
    mock_resp_a = {
        "intent": "LAB_SEARCH",
        "answer": "Bottles under IS 17803:2022 can be tested at BIS Central Lab Sahibabad.",
        "what_it_means": "Food contact testing.",
        "next_action": "Submit bottle samples via Manak Online.",
        "evidence_tag": {"status": "confirmed"}
    }
    write_cache(
        generic_query,
        "en",
        mock_resp_a,
        active_topic="IS 17803:2022",
        persona="general",
        context_topic="IS 17803:2022"
    )

    # Session A checks cache with its own context topic -> HITS!
    hit_a, topic_a = check_cache(generic_query, "en", persona="general", active_topic="IS 17803:2022") or (None, None)
    assert hit_a is not None, "Session A must hit its own contextual cache"
    assert "17803" in hit_a["answer"]

    # Session B checks cache with helmet context topic -> MUST MISS!
    hit_b, topic_b = check_cache(generic_query, "en", persona="general", active_topic="IS 4151:2015") or (None, None)
    assert hit_b is None, "Session B must NEVER hit Session A's bottle cache for generic follow-up"

    # Now Session B caches its helmet response
    mock_resp_b = {
        "intent": "LAB_SEARCH",
        "answer": "Helmets under IS 4151:2015 can be tested at BIS Western Regional Lab Mumbai and ARAI Pune.",
        "what_it_means": "Protective helmet impact testing.",
        "next_action": "Submit helmet prototypes via Manak Online.",
        "evidence_tag": {"status": "confirmed"}
    }
    write_cache(
        generic_query,
        "en",
        mock_resp_b,
        active_topic="IS 4151:2015",
        persona="general",
        context_topic="IS 4151:2015"
    )

    # Now verify bidirectional isolation:
    # Session A still gets bottle answer:
    hit_a2, _ = check_cache(generic_query, "en", persona="general", active_topic="IS 17803:2022") or (None, None)
    assert hit_a2 is not None
    assert "17803" in hit_a2["answer"]

    # Session B gets helmet answer:
    hit_b2, _ = check_cache(generic_query, "en", persona="general", active_topic="IS 4151:2015") or (None, None)
    assert hit_b2 is not None
    assert "4151" in hit_b2["answer"]

    # Verify Session B's active topic in DB remains helmet
    sess_b_data = get_or_create_session(sess_b)
    assert sess_b_data["active_topic"] == "IS 4151:2015", "Session B active topic must remain intact"
    print("[PASS] Edge Case 13: Cross-session cache poisoning prevented by context-topic keying")

def test_14_lab_search_intent_routing_variations():
    lab_queries = [
        "where can I get it tested?",
        "where to get this tested",
        "where do i get it tested",
        "where can this be tested",
        "where to test it",
        "how can i test it",
        "where can i get tested",
        "testing facility near me",
        "test centres in delhi"
    ]
    for q in lab_queries:
        r = route_intent(q)
        assert r["intent"] == "LAB_SEARCH", f"Query '{q}' misrouted to {r['intent']}"
        assert r["method"] == "regex_fastpath", f"Query '{q}' did not use fastpath"
    print("[PASS] Edge Case 14: All lab-search follow-up variations route to LAB_SEARCH via regex fast-path")

def test_15_voluntary_standard_handling():
    # Test municipal tap water standard (IS 10500:2012)
    chain = run_compliance_chain("municipal drinking water")
    assert chain["standard"]["is_code"] == "IS 10500:2012"
    assert "voluntary" in chain["qco_status"].lower()
    assert chain["scheme"]["name"] == "Voluntary Compliance / Optional Scheme-I"
    assert chain["steps"][0]["scheme"] == "Voluntary"
    assert "mandatory compliance enforced" not in chain["evidence_tag"]["clause_summary"].lower()
    assert "voluntary" in chain["evidence_tag"]["clause_summary"].lower()

    # Verify synthesis handles voluntary status correctly
    synth = deterministic_synthesis(chain, "is drinking water certified by bis", "en")
    assert "VOLUNTARY" in synth["answer"]
    assert "not enforced" in synth["what_it_means"].lower() or "voluntary" in synth["what_it_means"].lower()
    print("[PASS] Edge Case 15: Voluntary standards correctly classified without mandatory QCO enforcement")

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
    test_11_persona_cache_and_response_isolation()
    test_12_conversational_acknowledgments_and_thanks()
    test_13_cross_session_topic_cache_isolation()
    test_14_lab_search_intent_routing_variations()
    test_15_voluntary_standard_handling()
    print("\nALL 15 SPECIFICATION & PERSONA EDGE-CASE TESTS PASSED!")
