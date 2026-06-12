from typing import Any

from pydantic import BaseModel, Field, field_validator


class SummaryRequest(BaseModel):
    bundle: dict[str, Any] = Field(..., description="FHIR Bundle JSON")

    @field_validator("bundle")
    @classmethod
    def validate_bundle(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("FHIR Bundle cannot be empty")
        if value.get("resourceType") != "Bundle":
            raise ValueError("Invalid FHIR bundle: resourceType must be 'Bundle'")
        if "entry" not in value or not isinstance(value["entry"], list):
            raise ValueError("Invalid FHIR bundle: entry must be a list")
        return value
