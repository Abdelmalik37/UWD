import base64
import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.upload_record import UploadRecord
from app.schemas.conversion import FhirResponse, UploadDetail, UploadResponse
from app.services.fhir_mapper import build_fhir_bundle
from app.services.parsers import parse_any_bytes, to_json_text

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    source_type, parsed, error = parse_any_bytes(content)

    parse_status = "parsed" if parsed is not None else "unsupported"
    if error and parsed is None:
        parse_status = "failed" if "error" in error.lower() else "unsupported"

    record = UploadRecord(
        original_filename=file.filename or "upload",
        original_content_type=file.content_type,
        original_bytes_base64=base64.b64encode(content).decode("ascii"),
        parse_status=parse_status,
        parse_error=error,
        source_type=source_type,
        parsed_raw_json=to_json_text(parsed) if parsed is not None else None,
        metadata_json=to_json_text(
            {
                "size_bytes": len(content),
                "content_type": file.content_type,
            }
        ),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return UploadResponse(
        id=record.id,
        filename=record.original_filename,
        parse_status=record.parse_status,
        parse_error=record.parse_error,
        source_type=record.source_type,
        created_at=record.created_at,
    )


@router.get("/upload/{upload_id}", response_model=UploadDetail)
def get_upload(upload_id: int, db: Session = Depends(get_db)):
    record = db.query(UploadRecord).filter(UploadRecord.id == upload_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Upload not found")
    return UploadDetail(
        id=record.id,
        filename=record.original_filename,
        parse_status=record.parse_status,
        parse_error=record.parse_error,
        source_type=record.source_type,
        parsed_raw_data=json.loads(record.parsed_raw_json) if record.parsed_raw_json else None,
        metadata=json.loads(record.metadata_json) if record.metadata_json else None,
        created_at=record.created_at,
    )


@router.post("/convert/{upload_id}", response_model=FhirResponse)
def convert_upload(upload_id: int, db: Session = Depends(get_db)):
    record = db.query(UploadRecord).filter(UploadRecord.id == upload_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Upload not found")
    if not record.parsed_raw_json:
        raise HTTPException(status_code=400, detail="No parsed data available for this upload")

    parsed = json.loads(record.parsed_raw_json)
    fhir_bundle = build_fhir_bundle(parsed)
    record.fhir_json = to_json_text(fhir_bundle)
    db.commit()

    return FhirResponse(id=record.id, fhir_bundle=fhir_bundle, created_at=record.created_at)


@router.get("/fhir/{upload_id}", response_model=FhirResponse)
def get_fhir(upload_id: int, db: Session = Depends(get_db)):
    record = db.query(UploadRecord).filter(UploadRecord.id == upload_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Upload not found")
    return FhirResponse(
        id=record.id,
        fhir_bundle=json.loads(record.fhir_json) if record.fhir_json else None,
        created_at=record.created_at,
    )


@router.get("/uploads")
def get_uploads(limit: int = 20, db: Session = Depends(get_db)):
    records = db.query(UploadRecord).order_by(UploadRecord.created_at.desc()).limit(limit).all()
    return [
        {
            "id": item.id,
            "filename": item.original_filename,
            "parse_status": item.parse_status,
            "source_type": item.source_type,
            "created_at": item.created_at,
        }
        for item in records
    ]
