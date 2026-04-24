import json
import time
import os

# Robust path handling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "raw_data")


# Import role-specific modules
from schema import UnifiedDocument
from process_pdf import extract_pdf_data
from process_transcript import clean_transcript
from process_html import parse_html_catalog
from process_csv import process_sales_csv
from process_legacy_code import extract_logic_from_code
from quality_check import run_quality_gate

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================
# Task: Orchestrate the ingestion pipeline and handle errors/SLA.

def main():
    start_time = time.time()
    final_kb = []
    
    # --- FILE PATH SETUP (Handled for students) ---
    pdf_path = os.path.join(RAW_DATA_DIR, "lecture_notes.pdf")
    trans_path = os.path.join(RAW_DATA_DIR, "demo_transcript.txt")
    html_path = os.path.join(RAW_DATA_DIR, "product_catalog.html")
    csv_path = os.path.join(RAW_DATA_DIR, "sales_records.csv")
    code_path = os.path.join(RAW_DATA_DIR, "legacy_pipeline.py")
    
    output_path = os.path.join(os.path.dirname(SCRIPT_DIR), "processed_knowledge_base.json")
    # ----------------------------------------------

    # 1. PDF Processing (Gemini API)
    print("--- Processing PDF ---")
    doc = extract_pdf_data(pdf_path)
    if doc and run_quality_gate(doc):
        final_kb.append(doc)

    # 2. Transcript Processing
    print("--- Processing Transcript ---")
    doc = clean_transcript(trans_path)
    if doc and run_quality_gate(doc):
        final_kb.append(doc)

    # 3. HTML Catalog Processing
    print("--- Processing HTML Catalog ---")
    docs = parse_html_catalog(html_path)
    for doc in docs:
        if run_quality_gate(doc):
            final_kb.append(doc)

    # 4. CSV Sales Processing
    print("--- Processing CSV Sales ---")
    docs = process_sales_csv(csv_path)
    for doc in docs:
        if run_quality_gate(doc):
            final_kb.append(doc)

    # 5. Legacy Code Processing
    print("--- Processing Legacy Code ---")
    doc = extract_logic_from_code(code_path)
    if doc and run_quality_gate(doc):
        final_kb.append(doc)

    # 6. Save final_kb to output_path
    print(f"--- Saving output to {output_path} ---")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_kb, f, ensure_ascii=False, indent=2, default=str)

    # 7. SCHEMA MIGRATION (V2) - Mid-lab Incident requirement
    print("--- Migrating to Schema V2 ---")
    from schema import migrate_v1_to_v2
    final_kb_v2 = []
    for doc_dict in final_kb:
        # Convert dict to UnifiedDocument first
        from schema import UnifiedDocument
        v1_obj = UnifiedDocument(**doc_dict)
        v2_obj = migrate_v1_to_v2(v1_obj)
        final_kb_v2.append(v2_obj.model_dump())
        
    output_path_v2 = os.path.join(os.path.dirname(SCRIPT_DIR), "processed_knowledge_base_v2.json")
    with open(output_path_v2, "w", encoding="utf-8") as f:
        json.dump(final_kb_v2, f, ensure_ascii=False, indent=2, default=str)
    print(f"--- Schema V2 output saved to {output_path_v2} ---")

    end_time = time.time()
    print(f"Pipeline finished in {end_time - start_time:.2f} seconds.")
    print(f"Total valid documents stored: {len(final_kb)}")


if __name__ == "__main__":
    main()
