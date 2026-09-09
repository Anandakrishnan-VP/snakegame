"""
Core module unit tests verifying directory search, attribute matching, 
verification engine, and compliance chain functionality.
"""

from backend.services.module1_directory import search_directory, get_standard_by_code, get_flagship_chunks
from backend.services.module2_matcher import match_product_to_standard
from backend.services.module3_certification import get_certification_steps
from backend.services.module4_verification import verify_code
from backend.services.module5_labs import find_testing_labs
from backend.services.compliance_chain import run_compliance_chain
from backend.services.intent_router import route_intent
from backend.services.session_manager import get_or_create_session, check_cache, write_cache

def test_module1():
    # Test synonym search
    res = search_directory("led bulb")
    assert len(res) > 0, "LED bulb search should return candidate"
    assert "IS 16102" in res[0]["is_code"] or "16102" in res[0]["is_code"], f"Expected IS 16102, got {res[0]['is_code']}"

    # Test flagship chunks
    chunks = get_flagship_chunks("IS 17803:2022")
    assert len(chunks) > 0, "IS 17803 should have flagship deep clauses"
    print("[PASS] Module 1 Two-Tier Directory & Flagship Chunks")

def test_module2():
    # Test attribute extraction & scoring boost
    match = match_product_to_standard("stainless steel bottle for children")
    assert match["primary_match"] is not None
    assert "17803" in match["primary_match"]["is_code"]
    assert match["attributes"]["material"] == "stainless steel"
    assert match["attributes"]["user_context"] == "children"
    print("[PASS] Module 2 Product-to-Standard Attribute Matching")

def test_module3():
    steps = get_certification_steps("Scheme-I", "domestic")
    assert len(steps) >= 5, "Scheme-I should have at least 5 structured steps"
    assert steps[0]["step_number"] == 1
    print("[PASS] Module 3 Certification Steps")

def test_module4():
    # 1. Valid CM/L
    res_cml = verify_code("Check licence CML1234567")
    assert res_cml["found"] is True
    assert "Milton" in res_cml["licensee_name"]

    # 2. Mixed number + date test (strict prefix-first)
    res_date = verify_code("Manufactured on 2023-05-10 with licence CML7654321")
    assert res_date["found"] is True
    assert res_date["extracted_code"] == "CML7654321"

    # 3. Valid HUID (6 alphanumeric chars)
    res_huid = verify_code("HUID AB1234 purchased yesterday")
    assert res_huid["found"] is True
    assert "Tanishq" in res_huid["licensee_name"]

    # 4. Deliberate not found
    res_miss = verify_code("CML0000000")
    assert res_miss["found"] is False
    print("[PASS] Module 4 Deterministic Verification Engine")

def test_module5():
    labs = find_testing_labs(is_code="IS 17803:2022", city="Mumbai")
    assert len(labs) > 0
    # Top lab should be in Mumbai due to city prioritization
    assert labs[0]["city"] == "Mumbai"
    print("[PASS] Module 5 Testing Lab Suggester")

def test_compliance_chain():
    chain = run_compliance_chain("I want to manufacture stainless steel insulated water bottles for kids in Mumbai")
    assert chain["chain_completed"] is True
    assert "17803" in chain["standard"]["is_code"]
    assert chain["qco_status"] == "Mandatory"
    assert len(chain["steps"]) > 0
    assert len(chain["labs"]) > 0
    assert chain["evidence_tag"]["status"] == "confirmed"
    assert "17803" in chain["evidence_tag"]["reference"]
    print("[PASS] Compliance Chain Connected Intelligence")

def test_intent_router():
    assert route_intent("verify CML1234567")["intent"] == "VERIFICATION"
    assert route_intent("where is the testing lab in mumbai")["intent"] == "LAB_SEARCH"
    assert route_intent("how to apply for isi mark")["intent"] == "CERTIFICATION_PROCESS"
    assert route_intent("recipe for chocolate cake")["intent"] == "OUT_OF_SCOPE"
    print("[PASS] Intent Router Fast-Path & Fallback")

if __name__ == "__main__":
    test_module1()
    test_module2()
    test_module3()
    test_module4()
    test_module5()
    test_compliance_chain()
    test_intent_router()
    print("\nALL CORE BACKEND MODULE TESTS PASSED!")
