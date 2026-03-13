from datetime import datetime
from typing import Any

from app.services.parsers import ensure_list

METRIC_ALIASES = {
    "heart_rate": ["heart_rate", "hr", "pulse", "bpm", "heartrate"],
    "steps": ["steps", "step_count", "step"],
    "sleep": ["sleep", "sleep_minutes", "minutesasleep", "sleepduration"],
    "spo2": ["spo2", "oxygen", "blood_oxygen", "oxygensaturation"],
    "calories": ["calories", "kcal", "energy"],
    "activity": ["activity", "workout", "exercise", "active_minutes", "distance"],
}

UNIT_BY_TYPE = {
    "heart_rate": "beats/min",
    "steps": "count",
    "sleep": "min",
    "spo2": "%",
    "calories": "kcal",
    "activity": "min",
}

TIME_KEYS = ["timestamp", "time", "datetime", "dateTime", "startTime", "wellnessStartTimeGmt", "startDate", "endDate"]
DEVICE_KEYS = ["device_id", "deviceId", "serial", "tracker", "sourceName"]
MANUFACTURER_KEYS = ["manufacturer", "brand", "sourceName"]


def _pick_first(item: dict, keys: list[str], default: str) -> str:
    for key in keys:
        if key in item and item[key] not in (None, ""):
            return str(item[key])
    return default


def _normalize_timestamp(item: dict) -> str:
    raw = _pick_first(item, TIME_KEYS, "")
    if raw:
        try:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            return parsed.isoformat()
        except ValueError:
            return str(raw)
    return datetime.utcnow().isoformat() + "Z"


def _coerce_float(value: Any) -> float | None:
    try:
        if isinstance(value, bool):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _detect_metric(field_name: str) -> str | None:
    key = field_name.lower().replace(" ", "").replace("-", "").replace("_", "")
    for metric, aliases in METRIC_ALIASES.items():
        for alias in aliases:
            if alias.replace("_", "") in key:
                return metric
    return None


def extract_metrics(data: Any) -> list[dict]:
    metrics: list[dict] = []
    entries = ensure_list(data)

    for item in entries:
        timestamp = _normalize_timestamp(item)
        device_id = _pick_first(item, DEVICE_KEYS, "unknown-device")
        manufacturer = _pick_first(item, MANUFACTURER_KEYS, "unknown-manufacturer")

        if "type" in item and "value" in item:
            inferred_metric = _detect_metric(str(item.get("type")))
            numeric_value = _coerce_float(item.get("value"))
            if inferred_metric and numeric_value is not None:
                metrics.append(
                    {
                        "metric": inferred_metric,
                        "value": numeric_value,
                        "unit": str(item.get("unit") or UNIT_BY_TYPE.get(inferred_metric, "unknown")),
                        "timestamp": timestamp,
                        "device_id": device_id,
                        "manufacturer": manufacturer,
                        "raw_field": "value",
                    }
                )

        for field_name, field_value in item.items():
            metric = _detect_metric(field_name)
            if not metric:
                continue
            numeric_value = _coerce_float(field_value)
            if numeric_value is None:
                continue
            metrics.append(
                {
                    "metric": metric,
                    "value": numeric_value,
                    "unit": UNIT_BY_TYPE.get(metric, "unknown"),
                    "timestamp": timestamp,
                    "device_id": device_id,
                    "manufacturer": manufacturer,
                    "raw_field": field_name,
                }
            )

    return metrics
