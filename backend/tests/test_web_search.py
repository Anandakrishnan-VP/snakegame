"""
Unit tests for Tier-2 Live BIS Web Intelligence Fallback.
Verifies domain whitelisting, query cleaning, and IS code regex extraction.
"""

import pytest
from backend.services.web_search import (
    clean_search_query,
    is_allowed_domain,
    IS_CODE_REGEX,
    search_bis_web
)

def test_clean_search_query():
    q1 = "What is the Indian Standard for manufacturing domestic LPG gas stoves?"
    cleaned1 = clean_search_query(q1)
    assert "domestic lpg gas stoves" in cleaned1
    assert "manufacturing" not in cleaned1
    assert "Indian Standard specification" in cleaned1

    q2 = "I am manufacturing solar panels for rooftop installations. What is the mandatory Indian Standard?"
    cleaned2 = clean_search_query(q2)
    assert "solar panels for rooftop installations" in cleaned2
    assert "Indian Standard specification" in cleaned2

def test_is_allowed_domain_whitelist():
    # Official government domains MUST be allowed
    assert is_allowed_domain("https://www.bis.gov.in/standards/lpg-stoves") is True
    assert is_allowed_domain("https://standards.bis.gov.in/website/") is True
    assert is_allowed_domain("https://manakonline.in/MANAK/productCertification") is True
    assert is_allowed_domain("https://services.bis.gov.in/php/BIS_2.0/bisconnect/") is True

    # Third-party blogs, consultants, and commercial sites MUST be rejected
    assert is_allowed_domain("https://taxguru.in/corporate-law/bis-certification.html") is False
    assert is_allowed_domain("https://corpbiz.io/bis-isi-certification") is False
    assert is_allowed_domain("https://google.com/search") is False
    assert is_allowed_domain("https://randomsite.com") is False

def test_is_code_regex_extraction():
    sample_text = "The mandatory standard notified in the Gazette is IS 4246:2002 for Domestic Gas Stoves."
    match = IS_CODE_REGEX.search(sample_text)
    assert match is not None
    assert match.group(1).upper() == "IS 4246:2002"

    sample_solar = "Quality Control Order for Crystalline Silicon Terrestrial Photovoltaic (PV) Modules specifies IS 14286:2010."
    match_solar = IS_CODE_REGEX.search(sample_solar)
    assert match_solar is not None
    assert match_solar.group(1).upper() == "IS 14286:2010"

def test_search_bis_web_graceful_without_api_key(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "")
    result = search_bis_web("domestic LPG gas stoves")
    assert result is None
