import json
import socket
import urllib.error
import urllib.request
from typing import Any

from app.core.config import settings


OPENROUTER_CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_SITE_URL = "http://localhost:8000"
OPENROUTER_APP_TITLE = "UWD Converter API"
REQUEST_TIMEOUT_SECONDS = 60

AI_SYSTEM_PROMPT = """You are an experienced healthcare data analyst specialized in wearable device monitoring and FHIR resources.

Analyze the provided FHIR Bundle and generate a concise physician-oriented clinical summary.

Instructions:
- Review all observations and resources.
- Identify trends and patterns.
- Highlight clinically relevant abnormalities.
- Summarize wearable monitoring results.
- Mention missing data if applicable.
- Do not invent diagnoses.
- Do not prescribe medications.
- Do not make treatment decisions.
- Only use information present in the bundle.

Output Format:
- Return a single short paragraph of 2-3 sentences maximum.
- Do not use headings, bullets, markdown, or repeated sections.
- Keep only the most clinically relevant points.
"""


class MissingOpenRouterKeyError(RuntimeError):
    pass


class OpenRouterAPIError(RuntimeError):
    pass


def bundle_to_text(bundle: dict[str, Any]) -> str:
    entries = bundle.get("entry", [])
    lines = []

    for entry in entries:
        resource = entry.get("resource", {}) if isinstance(entry, dict) else {}
        resource_type = resource.get("resourceType", "Unknown")

        if resource_type == "Observation":
            code_text = resource.get("code", {}).get("text", "Unknown observation")
            value = resource.get("valueQuantity", {}).get("value", "N/A")
            unit = resource.get("valueQuantity", {}).get("unit", "")
            timestamp = resource.get("effectiveDateTime", "No timestamp")
            lines.append(f"Observation: {code_text}; value={value} {unit}; time={timestamp}")
        elif resource_type in {"Patient", "Device"}:
            lines.append(json.dumps(resource, ensure_ascii=True))

    return "\n".join(lines) if lines else json.dumps(bundle, ensure_ascii=True, indent=2)


def build_prompt(bundle: dict[str, Any]) -> str:
    return f"FHIR Bundle data:\n{bundle_to_text(bundle)}"


def _extract_response_text(data: dict[str, Any]) -> str:
    if data.get("output_text"):
        return data["output_text"].strip()

    choices = data.get("choices", [])
    if choices:
        message = choices[0].get("message", {})
        content = message.get("content")
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") in {"output_text", "text"} and item.get("text"):
                    text_parts.append(item["text"])
            if text_parts:
                return "\n".join(text_parts).strip()

    text_parts = []
    for output in data.get("output", []):
        for content in output.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                text_parts.append(content["text"])

    return "\n".join(text_parts).strip()


def generate_summary(bundle: dict[str, Any]) -> str:
    api_key = settings.openrouter_api_key
    if not api_key:
        raise MissingOpenRouterKeyError("OPENROUTER_API_KEY environment variable is missing")

    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": AI_SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(bundle)},
        ],
        "max_tokens": 220,
    }

    request = urllib.request.Request(
        OPENROUTER_CHAT_COMPLETIONS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": OPENROUTER_SITE_URL,
            "X-Title": OPENROUTER_APP_TITLE,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise OpenRouterAPIError(f"OpenRouter API error ({exc.code}): {error_body}") from exc
    except urllib.error.URLError as exc:
        raise ConnectionError("Network failure while contacting OpenRouter API") from exc
    except socket.timeout as exc:
        raise TimeoutError("OpenRouter API request timed out") from exc

    summary = _extract_response_text(data)
    if not summary:
        raise OpenRouterAPIError("OpenRouter API returned an empty summary")

    return summary
