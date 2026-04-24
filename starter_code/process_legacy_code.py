import ast

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

import re

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # 1. Use 'ast' to find docstrings
    tree = ast.parse(source_code)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            functions.append({
                "name": node.name,
                "docstring": docstring if docstring else "No docstring provided"
            })
            
    # 2. Use regex to find business rules in comments
    # Look for "# Business Logic Rule XXX"
    rules_detected = []
    lines = source_code.split('\n')
    for line in lines:
        if "Business Logic Rule" in line:
            rules_detected.append(line.strip().replace('#', '').strip())
            
    # 3. Specifically look for the tax rate discrepancy
    # WARNING: This comment is misleading! ... code uses 10% ... 8%
    if "tax_rate = 0.10" in source_code and "8%" in source_code:
        rules_detected.append("WARNING: legacy_tax_calc comment says 8% but code uses 10%")
        
    # Aggregate content
    rules_text = ". ".join(rules_detected)
    content = f"Business Rules extracted from {file_path}: {rules_text}"
    
    return {
        "document_id": "code-legacy-001",
        "content": content,
        "source_type": "Code",
        "author": "Senior Dev (retired)",
        "timestamp": None,
        "source_metadata": {
            "filename": "legacy_pipeline.py",
            "functions": functions,
            "rules_detected": rules_detected
        }
    }

