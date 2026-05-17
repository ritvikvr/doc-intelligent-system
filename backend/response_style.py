import re


def _as_bullets(items: list[str], fallback: str) -> list[str]:
    cleaned = []
    for item in items:
        text = (item or "").strip().lstrip("-").strip()
        if text:
            cleaned.append(f"- {text}")
    if not cleaned:
        cleaned = [f"- {fallback}"]
    return cleaned


def extract_points_from_groq_response(raw_text: str, max_points: int = 6) -> list[str]:
    text = (raw_text or "").strip()
    if not text:
        return []

    lines = []
    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        cleaned = re.sub(r"^#+\s*", "", cleaned)
        cleaned = re.sub(r"^[\-\*\u2022]\s*", "", cleaned)
        if len(cleaned.split()) < 5:
            continue
        lower = cleaned.lower()
        if lower in {
            "client-ready response",
            "executive summary",
            "key findings",
            "business impact",
            "risks and dependencies",
            "recommended next steps",
        }:
            continue
        lines.append(cleaned)

    unique = []
    seen = set()
    for item in lines:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
        if len(unique) >= max_points:
            break
    return unique


def format_client_ready_summary(
    processed_sources: int,
    extracted_pages: int,
    executive_points: list[str],
    findings: list[str],
) -> str:
    summary_points = _as_bullets(
        executive_points,
        "No material executive summary points were identified from the current indexed content.",
    )
    finding_points = _as_bullets(
        findings,
        "No additional high-confidence findings were detected in the indexed content.",
    )

    lines = [
        "Client-Ready Summary",
        "Document Overview",
        f"- Processed sources: {processed_sources}",
        f"- Extracted page coverage: {extracted_pages}",
        "",
        "Executive Summary",
        *summary_points,
        "",
        "Key Findings",
        *finding_points,
        "",
        "Business Impact",
        "- The document indicates actionable opportunities to improve delivery quality, decision speed, or stakeholder alignment.",
        "",
        "Risks and Dependencies",
        "- Important assumptions should be validated against source sections before external circulation.",
        "",
        "Recommended Next Steps",
        "- Convert the findings into a prioritized implementation backlog with clear owners and deadlines.",
        "- Confirm high-impact statements with referenced source pages in a review session.",
        "- Schedule a follow-up checkpoint after incorporating updates or new source files.",
    ]
    return "\n".join(lines)


def format_client_ready_answer(
    executive_points: list[str],
    findings: list[str],
    include_unknown_notice: bool = False,
) -> str:
    summary_points = _as_bullets(
        executive_points,
        "Insufficient context is available to provide a definitive executive-level answer.",
    )
    finding_points = _as_bullets(
        findings,
        "No additional high-confidence findings are available for this question.",
    )

    lines = [
        "Client-Ready Response",
        "Executive Summary",
        *summary_points,
        "",
        "Key Findings",
        *finding_points,
        "",
        "Business Impact",
        "- The retrieved evidence should be used to guide near-term technical and operational decisions.",
        "",
        "Risks and Dependencies",
        "- Some conclusions may rely on partial context and should be validated against full source material.",
        "",
        "Recommended Next Steps",
        "- Validate critical decisions with a source-backed review.",
        "- Convert confirmed findings into owned tasks with measurable outcomes.",
    ]
    if include_unknown_notice:
        lines.extend(["", "Confidence Note", "- The available context is limited; additional source data is recommended."])
    return "\n".join(lines)
