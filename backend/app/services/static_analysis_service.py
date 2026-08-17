"""Safe static malware analysis service."""

import json
import re
from pathlib import Path

from app.utils.file_hash import calculate_file_hashes


# Common indicators found in suspicious files.
URL_PATTERN = re.compile(
    rb"https?://[^\s\"'<>]+",
    re.IGNORECASE,
)

IP_PATTERN = re.compile(
    rb"\b(?:\d{1,3}\.){3}\d{1,3}\b",
)

DOMAIN_PATTERN = re.compile(
    rb"\b(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|io|co|in|biz|info|xyz|ru|uk|de|fr|cn|top|site|online)\b",
    re.IGNORECASE,
)

SUSPICIOUS_KEYWORDS = {
    "powershell": 15,
    "cmd.exe": 10,
    "wscript": 10,
    "cscript": 10,
    "rundll32": 10,
    "regsvr32": 10,
    "mshta": 15,
    "schtasks": 10,
    "wmic": 10,
    "downloadstring": 15,
    "invoke-expression": 15,
    "base64": 10,
    "mimikatz": 20,
    "keylogger": 20,
    "ransomware": 25,
    "cryptojacking": 20,
}


def _extract_strings(data: bytes, minimum_length: int = 4) -> list[str]:
    """Extract printable ASCII strings from binary data."""

    pattern = rb"[\x20-\x7e]{%d,}" % minimum_length

    strings = re.findall(pattern, data)

    decoded = []

    for value in strings:
        try:
            decoded.append(value.decode("ascii", errors="ignore"))
        except UnicodeDecodeError:
            continue

    return decoded


def _valid_ip(value: str) -> bool:
    """Check whether an extracted IPv4 address is valid."""

    parts = value.split(".")

    if len(parts) != 4:
        return False

    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def analyze_file(file_path: str) -> dict:
    """
    Perform safe static analysis on a file.

    The file is read only and is never executed.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    data = path.read_bytes()

    sha256, md5 = calculate_file_hashes(str(path))

    strings = _extract_strings(data)

    urls = sorted(
        {
            value.decode("utf-8", errors="ignore")
            for value in URL_PATTERN.findall(data)
        }
    )

    ips = sorted(
        {
            value.decode("ascii", errors="ignore")
            for value in IP_PATTERN.findall(data)
            if _valid_ip(value.decode("ascii", errors="ignore"))
        }
    )

    domains = sorted(
        {
            value.decode("ascii", errors="ignore").lower()
            for value in DOMAIN_PATTERN.findall(data)
        }
    )

    # Remove domains that are actually part of URLs.
    for url in urls:
        domain_match = re.search(
            rb"https?://([^/\s\"'<>]+)",
            url.encode("utf-8"),
            re.IGNORECASE,
        )

        if domain_match:
            domain = domain_match.group(1).decode(
                "utf-8",
                errors="ignore",
            ).lower()

            domains = [
                item
                for item in domains
                if item != domain
            ]

    combined_text = "\n".join(strings).lower()

    suspicious_matches = []

    for keyword, weight in SUSPICIOUS_KEYWORDS.items():
        if keyword in combined_text:
            suspicious_matches.append(
                {
                    "indicator": keyword,
                    "weight": weight,
                }
            )

    risk_score = min(
        100,
        sum(item["weight"] for item in suspicious_matches)
        + min(len(urls) * 5, 15)
        + min(len(ips) * 5, 15)
        + min(len(domains) * 2, 10),
    )

    if risk_score >= 80:
        severity = "critical"
        classification = "highly_suspicious"
    elif risk_score >= 60:
        severity = "high"
        classification = "suspicious"
    elif risk_score >= 30:
        severity = "medium"
        classification = "potentially_unwanted"
    elif risk_score > 0:
        severity = "low"
        classification = "low_risk"
    else:
        severity = "unknown"
        classification = "undetermined"

    result = {
        "file": {
            "name": path.name,
            "size": len(data),
            "extension": path.suffix.lower(),
        },
        "hashes": {
            "sha256": sha256,
            "md5": md5,
        },
        "strings": {
            "count": len(strings),
            "samples": strings[:100],
        },
        "indicators": {
            "urls": urls,
            "ips": ips,
            "domains": domains,
        },
        "suspicious_indicators": suspicious_matches,
        "risk": {
            "score": risk_score,
            "severity": severity,
            "classification": classification,
        },
    }

    return result


def analyze_file_json(file_path: str) -> str:
    """Run static analysis and return JSON."""

    result = analyze_file(file_path)

    return json.dumps(
        result,
        indent=2,
        ensure_ascii=False,
    )
