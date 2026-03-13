from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.db.session import Base


class UploadRecord(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String(255), nullable=False)
    original_content_type = Column(String(120), nullable=True)
    original_bytes_base64 = Column(Text, nullable=False)
    parse_status = Column(String(32), nullable=False)
    parse_error = Column(Text, nullable=True)
    source_type = Column(String(20), nullable=True)
    parsed_raw_json = Column(Text, nullable=True)
    fhir_json = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
