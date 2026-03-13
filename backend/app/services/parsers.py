import csv
import io
import json
import xml.etree.ElementTree as ET
from typing import Any, Optional


def _safe_decode(content: bytes) -> str:
    return content.decode("utf-8", errors="replace")


def parse_json(text: str) -> Any:
    return json.loads(text)


def parse_csv(text: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(text))
    return [row for row in reader]


def _strip_ns(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _xml_records(root: ET.Element) -> list[dict]:
    records: list[dict] = []
    for node in root.iter():
        children = list(node)
        if not children and not node.attrib:
            continue
        record = {}
        has_text = False
        for child in children:
            key = _strip_ns(child.tag)
            value = child.text.strip() if child.text else ""
            if value:
                record[key] = value
                has_text = True
        if node.attrib:
            for key, value in node.attrib.items():
                if value:
                    record[_strip_ns(key)] = value
                    has_text = True
        if has_text and record:
            record["_tag"] = _strip_ns(node.tag)
            records.append(record)
    return records


def parse_xml(text: str) -> list[dict] | dict:
    root = ET.fromstring(text)
    records = _xml_records(root)
    if records:
        return records
    flat = {}
    for node in root.iter():
        key = _strip_ns(node.tag)
        value = node.text.strip() if node.text else ""
        if value:
            flat[key] = value
    return flat or {"root": _strip_ns(root.tag)}


def parse_any_bytes(content: bytes) -> tuple[Optional[str], Optional[Any], Optional[str]]:
    text = _safe_decode(content).strip()
    if not text:
        return None, None, "Empty file"

    try:
        if text.startswith("{") or text.startswith("["):
            return "json", parse_json(text), None
    except Exception as exc:
        return "json", None, f"JSON parse error: {exc}"

    try:
        csv_rows = parse_csv(text)
        if csv_rows:
            return "csv", csv_rows, None
    except Exception as exc:
        return "csv", None, f"CSV parse error: {exc}"

    try:
        if text.startswith("<"):
            return "xml", parse_xml(text), None
    except Exception as exc:
        return "xml", None, f"XML parse error: {exc}"

    return None, None, "Unsupported or unknown format"


def ensure_list(data: Any) -> list[dict]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        if "data" in data and isinstance(data["data"], list):
            return [item for item in data["data"] if isinstance(item, dict)]
        return [data]
    return []


def to_json_text(data: Any) -> str:
    return json.dumps(data, ensure_ascii=True, indent=2)
