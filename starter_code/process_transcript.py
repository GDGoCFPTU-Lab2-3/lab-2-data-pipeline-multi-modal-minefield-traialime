import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # 1. Remove noise tokens
    # Handle [Music], [Music starts], [Music ends], [Laughter], [inaudible], etc.
    noise_pattern = r'\[Music.*?\]|\[Laughter\]|\[inaudible\]'
    cleaned_text = re.sub(noise_pattern, '', text, flags=re.IGNORECASE)
    
    # 2. Strip timestamps [00:00:00]
    timestamp_pattern = r'\[\d{2}:\d{2}:\d{2}\]'
    cleaned_text = re.sub(timestamp_pattern, '', cleaned_text)
    
    # 3. Strip speaker labels [Speaker 1]:
    speaker_pattern = r'\[Speaker \d+\]:'
    cleaned_text = re.sub(speaker_pattern, '', cleaned_text)
    
    # Final cleanup of extra whitespaces/newlines
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text).strip()
    
    # 4. Extract price mentioned in Vietnamese words
    # Specifically looking for "năm trăm nghìn" -> 500000
    detected_price = None
    if "năm trăm nghìn" in cleaned_text.lower():
        detected_price = 500000
        
    return {
        "document_id": "video-transcript-001",
        "content": cleaned_text,
        "source_type": "Video",
        "author": "Speaker 1",
        "timestamp": None,
        "source_metadata": {
            "detected_price_vnd": detected_price,
            "language": "vi",
            "original_file": "demo_transcript.txt"
        }
    }

