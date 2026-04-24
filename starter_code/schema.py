from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    document_id: str           # Unique identifier, format: "<source>-<id>"
    content: str               # Cleaned main content
    source_type: str           # 'PDF' | 'Video' | 'HTML' | 'CSV' | 'Code'
    author: Optional[str] = "Unknown"
    timestamp: Optional[datetime] = None
    source_metadata: dict = Field(default_factory=dict)

# ==========================================
# SCHEMA MIGRATION (V2)
# ==========================================
class UnifiedDocumentV2(BaseModel):
    doc_id: str                    # was: document_id
    body: str                      # was: content
    src_type: str                  # was: source_type
    author: Optional[str] = "Unknown"
    timestamp: Optional[datetime] = None
    meta: dict = Field(default_factory=dict) # was: source_metadata
    processed_at: datetime = Field(default_factory=datetime.now)

def migrate_v1_to_v2(v1_doc: UnifiedDocument) -> UnifiedDocumentV2:
    """Migrates a V1 document to V2 schema."""
    return UnifiedDocumentV2(
        doc_id=v1_doc.document_id,
        body=v1_doc.content,
        src_type=v1_doc.source_type,
        author=v1_doc.author,
        timestamp=v1_doc.timestamp,
        meta=v1_doc.source_metadata,
        processed_at=datetime.now()
    )
