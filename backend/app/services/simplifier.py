"""AI-Powered Document Simplification Service with Gemini API and Rule-Based Fallback."""
import os
import re
import json
import urllib.request
import urllib.error

# Extensive dictionary of complex legal, medical, financial, and technical terms with layman definitions
DOMAIN_GLOSSARY = {
    "indemnify": "To legally protect someone against loss, damage, or legal responsibility, typically by paying their costs.",
    "indemnification": "An agreement where one party pays for the potential legal costs, damages, or losses incurred by the other party.",
    "force majeure": "Unforeseeable external circumstances (such as natural disasters or wars) that prevent a party from fulfilling a contract without penalty.",
    "liquidated damages": "A predetermined sum of money agreed upon in a contract that a breaching party must pay if they violate specific terms.",
    "arbitration": "A private legal dispute resolution process outside of public courts where an independent arbitrator makes a legally binding decision.",
    "subrogation": "The right of an insurance company to step into your shoes and sue the party responsible for causing your loss.",
    "statute of limitations": "The maximum legal time window after an event within which legal proceedings may be initiated.",
    "severability": "A contract clause stating that if any single term is deemed invalid, the remainder of the contract remains legally enforceable.",
    "heretofore": "Before this time or prior to this document.",
    "hereinafter": "Further on in this document (used to introduce a shortened nickname for a party).",
    "notwithstanding": "In spite of, or despite whatever was stated elsewhere in the agreement.",
    "jurisdiction": "The official power of a specific court or government body to make legal decisions and judgments.",
    "confidentiality": "The duty to keep sensitive, non-public information private and not disclose it to third parties.",
    "intellectual property": "Creations of the human mind protected by law, such as inventions, trademarks, copyrights, and trade secrets.",
    "warranty": "A written guarantee or promise that goods or services will meet certain quality standards or be repaired/replaced.",
    "liability": "Legal responsibility for one's acts or omissions, especially when causing financial or physical harm.",
    "waiver": "Voluntarily giving up a known legal right, claim, or privilege.",
    "breach": "The violation or failure to perform any term or obligation specified in a contract.",
    "remedy": "The legal mechanism (such as compensation or an injunction) used to correct a wrong or enforce a right.",
    "termination": "The formal ending or cancellation of a contract or agreement.",
    "consideration": "Something of value exchanged between parties (such as money or services) that makes a contract legally binding.",
    "covenant": "A formal, solemn promise or obligation within an agreement.",
    "affidavit": "A written statement confirmed by oath or affirmation for use as evidence in court.",
    "tort": "A civil wrong or injury that causes harm to someone, resulting in legal liability.",
    "fiduciary": "A person or entity legally obligated to act strictly in the best financial and ethical interest of another.",
    "hypertension": "High blood pressure condition that can strain the heart and blood vessels.",
    "benign": "Non-cancerous or harmless condition that does not spread to surrounding tissues.",
    "malignant": "Cancerous or dangerous condition that can invade and destroy nearby tissue.",
    "prognosis": "The likely or expected medical outcome and recovery course of an illness.",
    "idiopathic": "A disease or condition that arises spontaneously without a known cause.",
    "asymptomatic": "Showing or causing no outward symptoms or signs of disease.",
    "contraindication": "A specific condition or factor that serves as a reason to withhold a medical treatment or medication due to potential harm.",
    "amortization": "Spreading out a loan into a series of equal periodic payments over time.",
    "depreciation": "The reduction in the financial value of an asset over time due to wear and tear or obsolescence.",
    "liquidity": "The ease with which an asset can be converted into ready cash without losing its market value.",
    "escrow": "Money or assets held by a neutral third party until specified contractual conditions are satisfied.",
    "default": "Failure to fulfill a financial or legal obligation, such as missing a required debt repayment.",
}

# Plain-language substitutions for dense bureaucratic phrases
PHRASE_SUBSTITUTIONS = [
    (r"\bin the event that\b", "if"),
    (r"\bfor the reason that\b", "because"),
    (r"\bprior to\b", "before"),
    (r"\bsubsequent to\b", "after"),
    (r"\bin accordance with\b", "following"),
    (r"\bshall be entitled to\b", "has the right to"),
    (r"\bshall be deemed to be\b", "is considered"),
    (r"\bshall have the right to\b", "may"),
    (r"\bit is incumbent upon\b", "must"),
    (r"\butilize\b", "use"),
    (r"\bcommence\b", "start"),
    (r"\bterminate\b", "end"),
    (r"\bheretofore\b", "previously"),
    (r"\bherein\b", "in this agreement"),
    (r"\bthereof\b", "of it"),
    (r"\bwhereas\b", "since"),
    (r"\bnotwithstanding anything to the contrary\b", "regardless of any other statement"),
    (r"\bsole discretion\b", "own judgment"),
    (r"\bcovenant and agree\b", "agree"),
    (r"\bnull and void\b", "invalid"),
    (r"\bterms and conditions\b", "terms"),
]


class SimplifierService:
    """Orchestrates document simplification using Google Gemini API or intelligent heuristic fallback."""

    @classmethod
    def get_api_key(cls) -> str:
        """Retrieves Gemini API key from environment."""
        key = os.getenv("GEMINI_API_KEY", "").strip()
        # Avoid treating template placeholder as real key
        if key in ("", "your_gemini_api_key_here", "None"):
            return ""
        return key

    @classmethod
    def call_gemini_api(cls, text: str, api_key: str, level: str = "plain_language") -> dict:
        """
        Sends extracted text to Google Gemini REST endpoint with structured JSON prompt.
        """
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

        system_instruction = (
            "You are DocuEase, an expert plain-language document translator. "
            "Your objective is to make complex legal, medical, academic, or technical text clear, direct, "
            "and easily understandable for everyday citizens without omitting critical obligations, numbers, or rights. "
            "Always respond strictly with a valid JSON object matching the requested schema."
        )

        prompt = f"""Analyze and simplify the following document text:

---
{text[:12000]}
---

Return a strictly valid JSON object with EXACTLY this structure:
{{
  "summary": "A concise 2-4 sentence executive summary highlighting key points, obligations, and critical dates/facts.",
  "simplified_text": "A full, clear, section-by-section plain-English rewrite of the document preserving all original meaning.",
  "key_takeaways": [
    "First main takeaway or obligation",
    "Second main takeaway or obligation",
    "Third main takeaway or obligation"
  ],
  "terminology": [
    {{"term": "technical or legal term", "definition": "simple plain English definition"}}
  ],
  "reading_level": "Grade 8 / Everyday Plain English"
}}
Do NOT wrap the output in markdown code blocks like ```json ... ```. Return raw JSON only."""

        payload = {
            "contents": [
                {
                    "parts": [{"text": f"{system_instruction}\n\n{prompt}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 3000,
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        # Parse Gemini response candidates
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError("Gemini API returned no response candidates.")

        raw_content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        # Clean potential markdown fences
        cleaned = re.sub(r"^```json\s*", "", raw_content.strip())
        cleaned = re.sub(r"\s*```$", "", cleaned.strip())

        parsed = json.loads(cleaned)
        return parsed

    @classmethod
    def rule_based_simplify(cls, text: str) -> dict:
        """
        Intelligent heuristic simplification engine used when Gemini API key is unset or unavailable.
        Detects domain jargon, simplifies sentences, generates summary, and builds glossary.
        """
        # 1. Substitute complex phrases
        simplified_paragraphs = []
        raw_paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if not raw_paragraphs:
            raw_paragraphs = [text.strip()]

        for para in raw_paragraphs:
            p_text = para
            for pattern, replacement in PHRASE_SUBSTITUTIONS:
                p_text = re.sub(pattern, replacement, p_text, flags=re.IGNORECASE)

            # Split run-on sentences where feasible
            p_text = re.sub(r";\s*provided,?\s*however,?\s*that\b", ". However,", p_text, flags=re.IGNORECASE)
            p_text = re.sub(r",\s*and furthermore\b", ". Furthermore,", p_text, flags=re.IGNORECASE)
            simplified_paragraphs.append(p_text)

        simplified_text = "\n\n".join(simplified_paragraphs)

        # 2. Extract terminology matches
        found_terms = []
        lower_text = text.lower()
        for term, definition in DOMAIN_GLOSSARY.items():
            if re.search(r"\b" + re.escape(term) + r"\b", lower_text):
                found_terms.append({
                    "term": term.title(),
                    "definition": definition,
                })

        # Sort terms alphabetically
        found_terms = sorted(found_terms, key=lambda x: x["term"])

        # 3. Formulate Executive Summary & Key Takeaways
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        first_few = [s.strip() for s in sentences if len(s.strip()) > 20][:3]
        summary_intro = (
            "This document outlines essential terms, obligations, and conditions. "
            if not first_few else " ".join(first_few)
        )
        # Apply plain phrasing to summary
        for pattern, replacement in PHRASE_SUBSTITUTIONS:
            summary_intro = re.sub(pattern, replacement, summary_intro, flags=re.IGNORECASE)

        # Key takeaways
        takeaways = [
            f"Contains {len(found_terms)} defined specialized term(s) requiring careful review." if found_terms else "Clear everyday document structure.",
            "Obligations and conditions have been translated into direct plain language.",
            "Verify all dates, figures, and named parties against the original document.",
        ]

        return {
            "summary": summary_intro[:450],
            "simplified_text": simplified_text,
            "key_takeaways": takeaways,
            "terminology": found_terms,
            "reading_level": "Grade 8 / Everyday Plain English",
        }

    @classmethod
    def simplify(cls, text: str, level: str = "plain_language") -> dict:
        """
        Main simplification entry point. Tries Gemini API first; falls back gracefully.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        original_clean = text.strip()
        orig_words = len(original_clean.split())
        orig_chars = len(original_clean)

        api_key = cls.get_api_key()
        provider = "gemini"
        error_notice = None

        result_data = None
        if api_key:
            try:
                result_data = cls.call_gemini_api(original_clean, api_key, level)
            except Exception as e:
                provider = "rule_based_fallback"
                error_notice = f"Gemini API unavailable ({str(e)}). Used intelligent fallback engine."
                result_data = cls.rule_based_simplify(original_clean)
        else:
            provider = "rule_based_engine"
            result_data = cls.rule_based_simplify(original_clean)

        simplified_body = result_data.get("simplified_text", original_clean)
        simp_words = len(simplified_body.split())
        simp_chars = len(simplified_body)

        reduction = max(0, round(((orig_words - simp_words) / orig_words) * 100)) if orig_words > 0 else 0

        response = {
            "status": "success",
            "original_text": original_clean,
            "simplified_text": simplified_body,
            "summary": result_data.get("summary", ""),
            "key_takeaways": result_data.get("key_takeaways", []),
            "terminology": result_data.get("terminology", []),
            "metrics": {
                "original_words": orig_words,
                "simplified_words": simp_words,
                "original_chars": orig_chars,
                "simplified_chars": simp_chars,
                "reduction_percent": reduction,
                "reading_level": result_data.get("reading_level", "Grade 8 Plain English"),
                "estimated_reading_time_mins": max(1, round(orig_words / 200)),
            },
            "ai_provider": provider,
        }

        if error_notice:
            response["notice"] = error_notice

        return response
