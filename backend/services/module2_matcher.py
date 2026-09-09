"""
Module 2: Product-to-Standard Attribute Matching
Performs deterministic attribute extraction across 4 categories:
- Category (product type)
- Material (stainless steel, plastic, gold, etc.)
- Intended user / context (children, food-contact, industrial, household)
- Activity (manufacture, import, sell, test)
Boosts directory candidate ranking and handles single clarifying questions for ambiguous QCO status.
"""

import re
from typing import Dict, Any, List, Optional
from difflib import SequenceMatcher
from backend.services.module1_directory import search_directory

# Curated Attribute Dictionaries per §6.1
CATEGORY_DICT = {
    "bottle": ["bottle", "flask", "thermos", "sipper", "container", "tumbler"],
    "toy": ["toy", "toys", "doll", "teddy", "game", "rattle", "plaything", "puzzle"],
    "helmet": ["helmet", "helmets", "headgear", "head protection"],
    "battery": ["battery", "batteries", "cell", "power bank", "powerbank", "accumulator"],
    "lighting": ["led", "bulb", "lamp", "light", "luminaire", "tube light"],
    "water": ["water", "mineral water", "drinking water", "packaged water"],
    "jewellery": ["jewellery", "jewelry", "gold", "bangle", "necklace", "ring", "chain"],
    "cement": ["cement", "concrete", "mortar", "ppc", "opc"],
    "steel": ["steel", "rebar", "saria", "tmt", "structural steel", "iron rod"],
    "cable": ["wire", "cable", "cord", "wiring", "conductor"],
    "footwear": ["shoe", "shoes", "footwear", "sneakers", "boots", "sandals"],
    "appliance": ["iron", "press", "heater", "geyser", "toaster", "blender"],
    "electronics": ["electronics", "electronic", "it equipment", "computer", "laptop", "tablet", "mobile", "gadget", "router", "server", "crs", "information technology", "electronic goods"]
}

MATERIAL_DICT = {
    "stainless steel": ["stainless steel", "steel", "ss304", "ss316", "metallic"],
    "plastic": ["plastic", "polymer", "pvc", "polypropylene", "synthetic"],
    "gold": ["gold", "22k", "18k", "916", "750", "yellow gold"],
    "copper": ["copper", "cu"],
    "rubber": ["rubber", "elastomer", "latex"],
    "glass": ["glass", "borosilicate"],
    "lithium": ["lithium", "li-ion", "lithium-ion", "lfp", "nmc"]
}

USER_CONTEXT_DICT = {
    "children": ["children", "child", "kids", "kid", "baby", "infant", "toddler", "school"],
    "food-contact": ["food-contact", "food", "drinking", "potable", "beverage", "kitchen", "cooking"],
    "industrial": ["industrial", "factory", "construction", "commercial", "heavy duty"],
    "household": ["household", "domestic", "home", "personal"],
    "automotive": ["two-wheeler", "motorcycle", "bike", "rider", "vehicle", "automotive"]
}

ACTIVITY_DICT = {
    "manufacture": ["manufacture", "manufacturing", "making", "produce", "producer", "factory", "assemble"],
    "import": ["import", "importer", "importing", "customs", "foreign", "overseas"],
    "sell": ["sell", "selling", "retail", "distribution", "distributor", "shop", "ecommerce"],
    "test": ["test", "testing", "lab", "certification", "compliance"]
}

def extract_attributes(query: str) -> Dict[str, Optional[str]]:
    """Extracts 4 attributes from natural language query deterministically using regex word boundaries."""
    lower_query = query.lower()
    extracted = {
        "category": None,
        "material": None,
        "user_context": None,
        "activity": None
    }

    # 1. Category extraction (exact word boundary + fuzzy typo tolerance)
    for cat_name, synonyms in CATEGORY_DICT.items():
        if any(re.search(rf'\b{re.escape(syn)}s?\b', lower_query) for syn in synonyms):
            extracted["category"] = cat_name
            break
        # Fuzzy fallback for typos like 'electrnoics', 'hemlt', 'botle', 'batry'
        matched = False
        for token in lower_query.split():
            if len(token) >= 4:
                for syn in synonyms:
                    if len(syn) >= 4 and SequenceMatcher(None, token, syn).ratio() >= 0.78:
                        extracted["category"] = cat_name
                        matched = True
                        break
            if matched:
                break
        if extracted["category"]:
            break

    # 2. Material extraction (exact word boundary + fuzzy typo tolerance)
    for mat_name, synonyms in MATERIAL_DICT.items():
        if any(re.search(rf'\b{re.escape(syn)}\b', lower_query) for syn in synonyms):
            extracted["material"] = mat_name
            break
        matched = False
        for token in lower_query.split():
            if len(token) >= 4:
                for syn in synonyms:
                    if len(syn) >= 4 and SequenceMatcher(None, token, syn).ratio() >= 0.78:
                        extracted["material"] = mat_name
                        matched = True
                        break
            if matched:
                break
        if extracted["material"]:
            break

    # 3. User context extraction (exact word boundary)
    for ctx_name, synonyms in USER_CONTEXT_DICT.items():
        if any(re.search(rf'\b{re.escape(syn)}\b', lower_query) for syn in synonyms):
            extracted["user_context"] = ctx_name
            break

    # 4. Activity extraction (exact word boundary)
    for act_name, synonyms in ACTIVITY_DICT.items():
        if any(re.search(rf'\b{re.escape(syn)}\b', lower_query) for syn in synonyms):
            extracted["activity"] = act_name
            break

    return extracted

def match_product_to_standard(query: str) -> Dict[str, Any]:
    """
    Combines attribute extraction with directory search to recommend standards.
    Applies scoring boosts and enforces confidence threshold gate before declaring local match.
    """
    attributes = extract_attributes(query)
    candidates = search_directory(query)

    if not candidates:
        # Fallback: search using ONLY extracted category + material keywords if direct search gave no hits
        # (DO NOT search generic user_context like 'household' or activity like 'manufacture' as product queries)
        product_terms = [attributes[k] for k in ("category", "material") if attributes.get(k)]
        if product_terms:
            candidates = search_directory(" ".join(product_terms))

    # Apply attribute boosts to candidate scores
    for cand in candidates:
        boost = 0.0
        title_lower = cand["title"].lower()
        synonyms_lower = cand["synonyms"].lower()

        if attributes["category"] and (attributes["category"] in title_lower or attributes["category"] in synonyms_lower):
            boost += 10.0

        if attributes["material"] and (attributes["material"] in title_lower or attributes["material"] in synonyms_lower):
            boost += 8.0

        if attributes["user_context"] and (attributes["user_context"] in title_lower or attributes["user_context"] in synonyms_lower):
            boost += 6.0

        cand["score"] += boost
        cand["attribute_boost"] = boost

    candidates.sort(key=lambda x: x["score"], reverse=True)

    # Check for ambiguity requiring clarifying question (§6.2 point 3)
    clarifying_question = None
    if len(candidates) >= 2:
        top1 = candidates[0]
        top2 = candidates[1]
        score_diff = abs(top1["score"] - top2["score"])
        
        # If scores are close and QCO status differs or context distinguishes them
        if score_diff < 5.0 and top1["qco_status"] != top2["qco_status"]:
            if not attributes["user_context"]:
                clarifying_question = f"Is this product intended specifically for children/infants or for general adult/household use?"
            elif not attributes["material"]:
                clarifying_question = f"What is the primary material composition of this product (e.g., stainless steel, plastic, or composite)?"

    # Confidence Threshold Gate:
    # A candidate must have at least 15.0 points (strong match), OR have an explicit category match (attribute_boost from category >= 10.0).
    # Weak accidental overlaps (e.g. stopword overlap or context-only boost)
    # are NOT accepted as valid local standards, allowing clean fallback to Tier-2 Web Search.
    primary_candidate = None
    if candidates:
        top_cand = candidates[0]
        has_category_match = bool(attributes["category"] and (
            attributes["category"] in top_cand["title"].lower() or 
            attributes["category"] in top_cand["synonyms"].lower()
        ))
        if top_cand["score"] >= 15.0 or has_category_match:
            primary_candidate = top_cand

    return {
        "attributes": attributes,
        "primary_match": primary_candidate,
        "all_candidates": candidates[:5],
        "clarifying_question": clarifying_question,
        "evidence_summary": {
            "matched_category": attributes["category"],
            "matched_material": attributes["material"],
            "matched_context": attributes["user_context"],
            "target_activity": attributes["activity"]
        }
    }
