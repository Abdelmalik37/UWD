from datetime import datetime
from typing import Any

from app.services.mapper import extract_metrics

FHIR_CODES = {
    "heart_rate": {"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"},
    "steps": {"system": "http://loinc.org", "code": "55423-8", "display": "Steps"},
    "sleep": {"system": "http://loinc.org", "code": "93832-4", "display": "Sleep duration"},
    "spo2": {"system": "http://loinc.org", "code": "59408-5", "display": "Oxygen saturation in Capillary blood"},
    "calories": {"system": "http://loinc.org", "code": "41981-2", "display": "Calories burned"},
    "activity": {"system": "http://loinc.org", "code": "55411-3", "display": "Physical activity"},
}


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def build_fhir_bundle(parsed_data: Any) -> dict:
    metrics = extract_metrics(parsed_data)

    patient = {
        "resourceType": "Patient",
        "id": "patient-1",
        "identifier": [{"system": "urn:uwd", "value": "patient-1"}],
    }

    device = {
        "resourceType": "Device",
        "id": "device-1",
        "manufacturer": metrics[0]["manufacturer"] if metrics else "unknown-manufacturer",
        "identifier": [{"system": "urn:uwd", "value": metrics[0]["device_id"] if metrics else "unknown-device"}],
    }

    observations = []
    for idx, metric in enumerate(metrics, start=1):
        code = FHIR_CODES.get(metric["metric"], {"system": "urn:uwd", "code": metric["metric"], "display": metric["metric"]})
        observations.append(
            {
                "resourceType": "Observation",
                "id": f"obs-{idx}",
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
                "subject": {"reference": "Patient/patient-1"},
                "device": {"reference": "Device/device-1"},
                "effectiveDateTime": metric["timestamp"] or _now_iso(),
                "valueQuantity": {
                    "value": metric["value"],
                    "unit": metric["unit"],
                    "system": "http://unitsofmeasure.org",
                },
                "extension": [
                    {
                        "url": "urn:uwd:raw-field",
                        "valueString": metric["raw_field"],
                    }
                ],
            }
        )

    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "timestamp": _now_iso(),
        "entry": [{"resource": patient}, {"resource": device}] + [{"resource": obs} for obs in observations],
    }
    return bundle
