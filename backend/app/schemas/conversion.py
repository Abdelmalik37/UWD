from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: int
    filename: str
    parse_status: str
    parse_error: Optional[str] = None
    source_type: Optional[str] = None
    created_at: datetime


class UploadDetail(BaseModel):
    id: int
    filename: str
    parse_status: str
    parse_error: Optional[str] = None
    source_type: Optional[str] = None
    parsed_raw_data: Optional[Any] = None
    metadata: Optional[Any] = None
    created_at: datetime


class FhirResponse(BaseModel):
    id: int
    fhir_bundle: Optional[Any] = None
    created_at: datetime
