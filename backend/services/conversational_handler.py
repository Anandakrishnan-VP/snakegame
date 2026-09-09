"""
Conversational Handler for BIS Saathi.
Gracefully handles user conversational pleasantries, acknowledgments ("ok", "got it", "noted"),
gratitude ("thank you", "thanks"), closings ("bye", "that's all"), and greetings ("hi", "hello").
Prevents repeating technical standard answers or producing irrelevant responses when users simply acknowledge.
"""

import re
from typing import Dict, Any, Optional

ACK_PATTERNS = [
    r'^(?:ok|okay|okey|k|kk|okk|k+|alright|all\s+right|fine|cool|sure|sure\s+thing|done|noted|clear|all\s+clear|understood|makes\s+sense|perfect|great|nice|awesome|good|very\s+good|excellent|yes|yeah|yup|yep)(?:\s+(?:ok|okay|k|thanks|thank\s+you|got\s+it|understood|done|bro|sir|saathi))*[.!]?$',
    r'^(?:got\s+it|i\s+got\s+it|i\s+understand|understood|makes\s+sense|noted|duly\s+noted|sounds\s+good)[.!]?$',
    r'^(?:theek\s+hai|thik\s+hai|achha|accha|theek|thik|samajh\s+gaya|samajh\s+gaye|haan|ha|sahi\s+hai)[.!]?$',
    r'^(?:ठीक\s*है|अच्छा|समझ\s*गया|समझ\s*गए|हाँ|सही\s*है|சரி|புரிந்தது|సరే|అర్థమైంది|ঠিক\s*আছে|ઠીક\s*છે|ಸರಿ|ശരി)[.!]?$'
]

THANKS_PATTERNS = [
    r'^(?:thanks|thank\s+you|thank\s+you\s+so\s+much|thanks\s+a\s+lot|many\s+thanks|thx|tq|ty|appreciate\s+it|much\s+appreciated|thanks\s+for\s+the\s+(?:help|info|information))(?:\s+(?:so\s+much|saathi|bro|sir))*[.!]?$',
    r'^(?:dhanyawad|dhanyavad|shukriya|bahut\s+dhanyawad|bahut\s+shukriya)[.!]?$',
    r'^(?:धन्यवाद|शुक्रिया|बहुत\s*धन्यवाद|நன்றி|ధన్యవాదాలు|ಧನ್ಯವಾದಗಳು|നന്ദി|ধন্যবাদ|આભાર)[.!]?$'
]

CLOSING_PATTERNS = [
    r'^(?:bye|goodbye|good\s+bye|cya|see\s+you|that\'?s\s+all|that\s+is\s+all|that\'?s\s+it|nothing\s+else|no\s+more\s+questions|have\s+a\s+(?:good|nice)\s+day)[.!]?$',
    r'^(?:alvida|phir\s+milenge)[.!]?$',
    r'^(?:अलविदा|फिर\s*मिलेंगे)[.!]?$'
]

GREETING_PATTERNS = [
    r'^(?:hi|hello|hey|heya|hola|greetings|namaste|namaskar|good\s+(?:morning|afternoon|evening|day))(?:\s+(?:saathi|bis|there|sir))*[.!]?$',
    r'^(?:नमस्ते|नमस्कार|प्रणाम|வணக்கம்|నమస్కారం|ನಮಸ್ಕಾರ|നമസ്കാരം|নমস্কার|નમસ્તે)[.!]?$'
]

def classify_conversational(query: str) -> Optional[str]:
    """
    Returns 'ACK', 'THANKS', 'CLOSING', 'GREETING' if the query is a pure conversational turn,
    or None if it contains substantive domain questions.
    """
    if not query or not query.strip():
        return None
    text = query.strip().lower()

    for p in THANKS_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            return "THANKS"
    for p in CLOSING_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            return "CLOSING"
    for p in ACK_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            return "ACK"
    for p in GREETING_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            return "GREETING"

    return None

def generate_conversational_response(
    conv_type: str,
    raw_query: str,
    active_topic: Optional[str] = None,
    persona: str = "general",
    language: str = "en"
) -> Dict[str, Any]:
    """
    Generates an empathetic, proper, non-repetitive response adhering to the 4-part structure.
    Preserves active_topic so subsequent queries can still reference it.
    """
    topic_ref = f" **{active_topic}**" if active_topic else ""

    if language == "hi":
        return _generate_hindi_response(conv_type, active_topic, persona)

    # English & other languages default
    if conv_type == "ACK":
        if active_topic:
            if persona == "consumer":
                answer = f"Understood! Feel free to ask if you would like to verify another product's ISI mark, check gold hallmarking (HUID), or learn how to file a grievance on the BIS Care App."
                what_it_means = f"Your active session topic is currently set to{topic_ref}. You can ask more questions about its quality checks or switch to any other product."
                next_action = f"Ask any follow-up question regarding{topic_ref}, or type a new product name or licence number."
            else:
                answer = f"Understood! Let me know if you need further details on testing laboratories, fee concessions, or filing Form V on Manak Online for{topic_ref}."
                what_it_means = f"Your active inquiry remains focused on{topic_ref}. You can ask about lab testing, factory inspection, or explore another standard anytime."
                next_action = f"Type your next question, or click 'Start My Certification Journey' above to track your milestones for{topic_ref}."
        else:
            answer = "Understood! Feel free to ask about any product standard, mandatory Quality Control Order (QCO), laboratory testing, or licence verification."
            what_it_means = "BIS Saathi is ready for your next inquiry."
            next_action = "Type a product name (e.g. Helmets, Toys, Cement, Batteries) or an IS code (e.g. IS 17803) to begin."

    elif conv_type == "THANKS":
        answer = "You're very welcome! I'm glad I could help. Whenever you need guidance on Bureau of Indian Standards compliance, ISI licences, or lab testing, I'm here for you."
        what_it_means = f"You can return anytime with questions regarding industrial standards or consumer protection.{f' (Active standard: {active_topic})' if active_topic else ''}"
        next_action = "Ask another question or explore the 'Certification Journey' tab above to see step-by-step licensing roadmaps."

    elif conv_type == "CLOSING":
        answer = "You're all set! Have a wonderful day ahead. Whenever you have questions about Indian Standards, quality certifications, or BIS verification, BIS Saathi is here to assist you."
        what_it_means = f"Your session progress is preserved.{f' Active topic: {active_topic}.' if active_topic else ''}"
        next_action = "Revisit BIS Saathi whenever you need official standards and compliance intelligence."

    else:  # GREETING
        answer = "Hello! Welcome to **BIS Saathi**, your official intelligence assistant for Indian Standards, BIS certification schemes, testing laboratories, and hallmarking. How can I assist you today?"
        what_it_means = "You can ask about industrial licensing (Scheme-I, CRS, FMCS), MSME fee concessions, laboratory test centers, or consumer verification (CM/L, HUID)."
        next_action = "Enter a product name (e.g. Helmets, Toys, Drinking Water), an IS code (e.g. IS 4151), or a licence code to begin."

    return {
        "answer": answer,
        "what_it_means": what_it_means,
        "next_action": next_action,
        "evidence_tag": {
            "source_type": "faq",
            "reference": "BIS Saathi Conversational Assistant",
            "status": "confirmed",
            "clause_number": "Assistant Guidelines",
            "clause_summary": "Conversational reply acknowledging user communication.",
            "verbatim_excerpt": "Official BIS Saathi Conversational Intelligence.",
            "source_url": "https://www.bis.gov.in"
        },
        "persona": persona,
        "provider": "bis-saathi-assistant"
    }

def _generate_hindi_response(conv_type: str, active_topic: Optional[str], persona: str) -> Dict[str, Any]:
    """Generates localized Hindi conversational replies."""
    topic_ref = f" **{active_topic}**" if active_topic else ""

    if conv_type == "ACK":
        if active_topic:
            if persona == "consumer":
                answer = f"समझ गया! यदि आप किसी अन्य उत्पाद का ISI मार्क सत्यापित करना चाहते हैं, हॉलमार्क (HUID) जांचना चाहते हैं, या BIS Care App पर शिकायत दर्ज करने के बारे में जानना चाहते हैं, तो कृपया बताएं।"
                what_it_means = f"आपका वर्तमान विषय{topic_ref} पर केंद्रित है। आप इसके बारे में और पूछ सकते हैं या किसी अन्य उत्पाद का नाम दर्ज कर सकते हैं।"
                next_action = "अपना अगला प्रश्न पूछें या ऊपर दिए गए 'Verify Licence' टैब में जाकर सत्यापन करें।"
            else:
                answer = f"समझ गया! यदि आपको{topic_ref} के लिए परीक्षण प्रयोगशालाओं, शुल्क रियायतों, या माणक ऑनलाइन (Form V) आवेदन के बारे में कोई अन्य जानकारी चाहिए, तो कृपया बताएं।"
                what_it_means = f"आपका सक्रिय विषय अभी भी{topic_ref} है। आप संबंधित प्रक्रियाओं के बारे में पूछ सकते हैं या किसी अन्य मानक का विवरण ले सकते हैं।"
                next_action = "अपना अगला प्रश्न पूछें, या ऊपर 'Certification Journey' टैब में जाकर अपनी तैयारी का चरणबद्ध विवरण देखें।"
        else:
            answer = "समझ गया! भारतीय मानकों (Indian Standards), अनिवार्य गुणवत्ता नियंत्रण आदेशों (QCO), परीक्षण प्रयोगशालाओं, या लाइसेंस सत्यापन के बारे में किसी भी प्रश्न के लिए कृपया बताएं।"
            what_it_means = "बीआईएस साथी आपके अगले प्रश्न के लिए तैयार है।"
            next_action = "किसी उत्पाद का नाम (जैसे सीमेंट, खिलौने, हेलमेट, पानी) या आईएस कोड दर्ज करें।"

    elif conv_type == "THANKS":
        answer = "आपका बहुत-बहुत स्वागत है! सहायता करके अत्यंत प्रसन्नता हुई। भारतीय मानकों, बीआईएस लाइसेंसिंग और उत्पाद गुणवत्ता से संबंधित किसी भी सहायता के लिए बीआईएस साथी हमेशा उपलब्ध है।"
        what_it_means = "बीआईएस गुणवत्ता मानकों या प्रमाणन से जुड़े किसी भी सवाल के लिए आप कभी भी पूछ सकते हैं।"
        next_action = "अपना अगला प्रश्न पूछें या ऊपर दिए गए टैब देखें।"

    elif conv_type == "CLOSING":
        answer = "आपका दिन शुभ हो! जब भी आपको भारतीय मानकों, गुणवत्ता प्रमाणन या लाइसेंस सत्यापन में सहायता की आवश्यकता हो, बीआईएस साथी आपकी सेवा में तत्पर रहेगा।"
        what_it_means = "आपका सत्र सुरक्षित है। आप कभी भी पुनः प्रश्न पूछ सकते हैं।"
        next_action = "आवश्यकता पड़ने पर बीआईएस साथी पर पुनः पधारें।"

    else:  # GREETING
        answer = "नमस्ते! **बीआईएस साथी (BIS Saathi)** में आपका स्वागत है। मैं भारतीय मानकों, प्रमाणन योजनाओं (Scheme-I, CRS), परीक्षण प्रयोगशालाओं और हॉलमार्किंग से संबंधित आधिकारिक जानकारी के लिए आपका सहायक हूँ। आज मैं आपकी क्या सहायता कर सकता हूँ?"
        what_it_means = "आप एमएसएमई लाइसेंसिंग, परीक्षण प्रयोगशालाओं, या उपभोक्ता सत्यापन (CM/L, HUID) के बारे में पूछ सकते हैं।"
        next_action = "किसी उत्पाद का नाम (जैसे हेलमेट, खिलौने, बोतल) या आईएस कोड लिखकर शुरुआत करें।"

    return {
        "answer": answer,
        "what_it_means": what_it_means,
        "next_action": next_action,
        "evidence_tag": {
            "source_type": "faq",
            "reference": "BIS Saathi Conversational Assistant",
            "status": "confirmed",
            "clause_number": "Assistant Guidelines",
            "clause_summary": "बातचीत की पावती (Conversational Acknowledgment).",
            "verbatim_excerpt": "आधिकारिक बीआईएस साथी सहायक।",
            "source_url": "https://www.bis.gov.in"
        },
        "persona": persona,
        "provider": "bis-saathi-assistant"
    }
