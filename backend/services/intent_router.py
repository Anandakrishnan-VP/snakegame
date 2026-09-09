"""
Intent Router for BIS Saathi.
Classifies user queries into 7 distinct intents using regex fast-path and TF-IDF similarity fallback:
- STANDARD_SEARCH
- PRODUCT_TO_STANDARD
- CERTIFICATION_PROCESS
- VERIFICATION
- LAB_SEARCH
- GENERAL_FAQ
- OUT_OF_SCOPE
"""

import re
from typing import Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Pre-defined training utterances for semantic fallback (§15)
UTTERANCES = {
    "STANDARD_SEARCH": [
        "what is is 4151",
        "search standard for cement",
        "details of is 9873",
        "tell me about is 17803",
        "find indian standard for cables",
        "specifications for packaged drinking water standard",
        "is code for gold hallmarking",
        "download is 13252",
        "standard for toys",
        "toy safety standard",
        "packaged drinking water standard",
        "ceiling fan standard"
    ],
    "PRODUCT_TO_STANDARD": [
        "which standard applies to stainless steel water bottles",
        "i am manufacturing toys for kids what are the rules",
        "standard for electric vehicle batteries",
        "do led bulbs need bis certification",
        "what is the standard for two wheeler helmets",
        "making footwear for sports which standard",
        "i produce concrete rebars fe500d",
        "recommend standard for baby milk bottles",
        "children toys standard",
        "what is the standard for toys"
    ],
    "CERTIFICATION_PROCESS": [
        "how to get bis licence",
        "what are the steps for scheme 1",
        "explain crs registration process",
        "how can a foreign manufacturer get bis certificate fmcs",
        "what is form v on manak online",
        "licensing procedure for domestic manufacturers",
        "timeline and fees for bis marking",
        "how to apply for isi mark"
    ],
    "VERIFICATION": [
        "verify cml1234567",
        "check huid ab1234",
        "is this isi mark genuine",
        "verify bis licence number",
        "check gold hallmark number",
        "verify crs registration r-41001234",
        "authenticate this jewellery huid",
        "check if this manufacturer is licensed"
    ],
    "LAB_SEARCH": [
        "where is testing lab in mumbai",
        "testing laboratories for helmets",
        "find lab to test water bottles",
        "recognized testing labs in delhi or chennai",
        "where can i test lithium ion battery in india",
        "bis central laboratory contact",
        "nabl test house for toys"
    ],
    "GENERAL_FAQ": [
        "what are bis standards clubs in schools",
        "how can a consumer file complaint against fake isi",
        "tell me about nits training in noida",
        "what concessions are available for msme and startups",
        "consumer rights for sub-standard products",
        "who regulates hallmarking in india"
    ],
    "OUT_OF_SCOPE": [
        "who is the prime minister of india",
        "write a python script for binary search",
        "how to cook biryani recipe",
        "tell me a funny joke",
        "what is the weather in new york",
        "recommend a good movie on netflix",
        "write an essay on global warming"
    ]
}

# Compile corpus and TF-IDF matrix for fallback
_corpus = []
_labels = []
for intent, examples in UTTERANCES.items():
    for ex in examples:
        _corpus.append(ex)
        _labels.append(intent)

_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
_tfidf_matrix = _vectorizer.fit_transform(_corpus)

def route_intent(query: str) -> Dict[str, Any]:
    """
    Routes user query to the most appropriate intent.
    Uses regex/keyword rules first, then TF-IDF cosine similarity fallback.
    """
    from backend.services.conversational_handler import classify_conversational
    conv = classify_conversational(query)
    if conv:
        return {"intent": f"CONVERSATIONAL_{conv}", "confidence": 0.98, "method": "conversational_fastpath"}

    text = query.lower().strip()

    # 1. Verification Fast-Path
    if re.search(r'\b(?:cml|cm/l|huid|crs|r-\d{8})\b', text) or re.search(r'\bverify\b', text):
        return {"intent": "VERIFICATION", "confidence": 0.95, "method": "regex_fastpath"}

    # 2. Lab Search Fast-Path
    if re.search(r'\b(?:lab|testing lab|laborator(?:y|ies)|where can i test|nabl lab)\b', text):
        return {"intent": "LAB_SEARCH", "confidence": 0.92, "method": "regex_fastpath"}

    # 3. Certification Steps Fast-Path
    if re.search(r'\b(?:how to apply|how to get|procedure|certification step|process for|scheme-i|crs|fmcs|manak online|form v|timeline|licensing steps)\b', text):
        return {"intent": "CERTIFICATION_PROCESS", "confidence": 0.90, "method": "regex_fastpath"}

    # 4. Standard Search Fast-Path (Contains explicit "IS " followed by digits)
    if re.search(r'\bis\s*\d{3,5}\b', text):
        return {"intent": "STANDARD_SEARCH", "confidence": 0.92, "method": "regex_fastpath"}

    if re.search(r'\b(?:standard for|standards for|which standard|what is the standard|applicable standard|safety standard)\b', text):
        return {"intent": "PRODUCT_TO_STANDARD", "confidence": 0.92, "method": "regex_fastpath"}

    # 5. General FAQ Fast-Path
    if re.search(r'\b(?:standards? club|nits|grievance|complaint|bis care|concession|msme fee|udyam discount)\b', text):
        return {"intent": "GENERAL_FAQ", "confidence": 0.88, "method": "regex_fastpath"}

    # 6. Out of Scope Fast-Path
    if re.search(r'\b(?:recipe|poem|joke|weather|movie|cricket score|netflix|python code|algorithm)\b', text):
        return {"intent": "OUT_OF_SCOPE", "confidence": 0.95, "method": "regex_fastpath"}

    # 7. Semantic Fallback (TF-IDF Cosine Similarity)
    q_vec = _vectorizer.transform([text])
    similarities = cosine_similarity(q_vec, _tfidf_matrix)[0]
    best_idx = similarities.argmax()
    best_score = similarities[best_idx]
    best_intent = _labels[best_idx]

    if best_score < 0.12:
        # Default to PRODUCT_TO_STANDARD if product keywords or general inquiry
        return {"intent": "PRODUCT_TO_STANDARD", "confidence": 0.50, "method": "default_fallback"}

    return {
        "intent": best_intent,
        "confidence": float(best_score),
        "method": "semantic_tfidf"
    }
