from datetime import datetime
from typing import Any
import uuid

from app.services.mapper import extract_metrics

FHIR_CODES = {
    "heart_rate": {"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"},
    "steps": {"system": "http://loinc.org", "code": "55423-8", "display": "Steps"},
    "sleep": {"system": "http://loinc.org", "code": "93832-4", "display": "Sleep duration"},
    "spo2": {"system": "http://loinc.org", "code": "59408-5", "display": "Oxygen saturation in Capillary blood"},
    "calories": {"system": "http://loinc.org", "code": "41981-2", "display": "Calories burned"},
    "activity": {"system": "http://loinc.org", "code": "55411-3", "display": "Physical activity"},
}

QUANTITY_CODES = {
    "heart_rate": "/min",
    "steps": "1",
    "sleep": "min",
    "spo2": "%",
    "calories": "kcal",
    "activity": "min",
}


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _bundle_entry(resource: dict, full_url: str) -> dict:
    return {"fullUrl": full_url, "resource": resource}


def _urn_uuid(seed: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, seed)}"


def _narrative(resource_type: str, summary: str) -> dict:
    return {
        "status": "generated",
        "div": f'<div xmlns="http://www.w3.org/1999/xhtml"><p>{resource_type}: {summary}</p></div>',
    }


def build_fhir_bundle(parsed_data: Any) -> dict:
    metrics = extract_metrics(parsed_data)

    patient_full_url = _urn_uuid("uwd:patient:1")
    device_full_url = _urn_uuid("uwd:device:1")

    patient = {
        "resourceType": "Patient",
        "id": "patient-1",
        "text": _narrative("Patient", "Synthetic patient record generated from UWD input."),
        "identifier": [{"system": "urn:uwd", "value": "patient-1"}],
    }

    device = {
        "resourceType": "Device",
        "id": "device-1",
        "text": _narrative("Device", "Synthetic source device generated from UWD input."),
        "manufacturer": metrics[0]["manufacturer"] if metrics else "unknown-manufacturer",
        "identifier": [{"system": "urn:uwd", "value": metrics[0]["device_id"] if metrics else "unknown-device"}],
    }

    observations = []
    for idx, metric in enumerate(metrics, start=1):
        code = FHIR_CODES.get(metric["metric"], {"system": "urn:uwd", "code": metric["metric"], "display": metric["metric"]})
        quantity_code = QUANTITY_CODES.get(metric["metric"], str(metric.get("unit") or "1"))
        observation_full_url = _urn_uuid(f"uwd:observation:{idx}")
        observations.append(
            _bundle_entry(
                {
                    "resourceType": "Observation",
                    "id": f"obs-{idx}",
                    "text": _narrative("Observation", f"{code['display']} observation generated from source data."),
                    "status": "final",
                    "category": [
                        {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                    "code": "vital-signs",
                                    "display": "Vital Signs",
                                }
                            ]
                        }
                    ],
                    "code": {"coding": [code], "text": code["display"]},
                    "subject": {"reference": patient_full_url},
                    "device": {"reference": device_full_url},
                    "performer": [{"reference": patient_full_url}],
                    "effectiveDateTime": metric["timestamp"] or _now_iso(),
                    "valueQuantity": {
                        "value": metric["value"],
                        "unit": metric["unit"],
                        "code": quantity_code,
                        "system": "http://unitsofmeasure.org",
                    },
                },
                observation_full_url,
            )
        )

    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "timestamp": _now_iso(),
        "entry": [
            _bundle_entry(patient, patient_full_url),
            _bundle_entry(device, device_full_url),
        ] + observations,
    }
    return bundle
