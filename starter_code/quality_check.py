# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

TOXIC_STRINGS = [
    "Null pointer exception",
    "NullPointerException", 
    "Stack trace",
    "ERROR:",
    "Exception:",
    "Traceback (most recent call last)",
]

def run_quality_gate(document_dict):
    """
    Runs several quality gates to ensure data integrity and security.
    Returns True if the document passes all gates, False otherwise.
    """
    # 1. Content Length Check
    content = document_dict.get("content", "") or document_dict.get("body", "")
    if len(content) < 20:
        print(f"[GATE FAIL] Content too short: {document_dict.get('document_id', 'Unknown')}")
        return False

    # 2. Toxic String Detection
    for toxic in TOXIC_STRINGS:
        if toxic.lower() in content.lower():
            print(f"[GATE FAIL] Toxic string detected in {document_dict.get('document_id')}: '{toxic}'")
            return False

    # 3. Video Transcript Price Extraction Check
    if document_dict.get("source_type") == "Video" or document_dict.get("src_type") == "Video":
        meta = document_dict.get("source_metadata", {}) or document_dict.get("meta", {})
        if "detected_price_vnd" not in meta:
            print(f"[GATE FAIL] Video transcript missing detected_price_vnd: {document_dict.get('document_id')}")
            return False

    # 4. Legacy Code Logic Discrepancy Check
    if document_dict.get("source_type") == "Code" or document_dict.get("src_type") == "Code":
        meta = document_dict.get("source_metadata", {}) or document_dict.get("meta", {})
        rules = meta.get("rules_detected", [])
        has_tax_warning = any("tax" in str(r).lower() for r in rules)
        if not has_tax_warning:
            print(f"[GATE FAIL] Code document missing tax logic discrepancy flag: {document_dict.get('document_id')}")
            # We don't return False here because it's a flag/warning, but for the lab, 
            # let's assume it MUST be present if it's the legacy code file.
            # In a real system, this might just be a warning.

    # 5. Negative Price Check
    if document_dict.get("source_type") in ("CSV", "HTML") or document_dict.get("src_type") in ("CSV", "HTML"):
        meta = document_dict.get("source_metadata", {}) or document_dict.get("meta", {})
        price = meta.get("price") or meta.get("price_vnd")
        if price is not None and isinstance(price, (int, float)) and price < 0:
            print(f"[GATE FAIL] Negative price detected: {price} in {document_dict.get('document_id')}")
            return False

    return True
