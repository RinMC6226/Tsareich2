#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys
from typing import Iterable


LINE_PATTERN = re.compile(
    r"^\[(?P<time>[^\]]+)\]\[(?P<source>[^\]]+)\](?::\s*)?(?P<message>.*)$"
)
PATH_PATTERN = re.compile(
    r"([A-Za-z]:[\\/][^\s\"']+|(?:common|events|gfx|history|interface|localisation|map|music)[\\/][^\s\"']+)"
)

CATEGORY_RULES = [
    ("missing_file", re.compile(r"\b(could not find|not found|missing file|failed to open|does not exist)\b", re.I)),
    ("parse_error", re.compile(r"\b(parser error|unexpected token|malformed token|invalid syntax|error:)\b", re.I)),
    ("unknown_key", re.compile(r"\bunknown\b|\bunexpected\b|\bunrecognized\b", re.I)),
    ("duplicate", re.compile(r"\bduplicate\b|\balready exists\b", re.I)),
    ("localisation", re.compile(r"\blocali[sz]ation\b|\btranslation\b", re.I)),
    ("gfx_asset", re.compile(r"\b(texture|sprite|mesh|shader|dds|tga|gfx)\b", re.I)),
    ("map_data", re.compile(r"\bprovince\b|\bstate\b|\bstrategic region\b|\bterrain\b|\bbuilding\b", re.I)),
    ("script_logic", re.compile(r"\bevent\b|\bfocus\b|\btrigger\b|\beffect\b|\bidea\b|\bcharacter\b", re.I)),
]

SEVERITY_RULES = [
    ("error", re.compile(r"\berror\b", re.I)),
    ("warning", re.compile(r"\bwarning\b", re.I)),
    ("exception", re.compile(r"\bexception\b|\btraceback\b", re.I)),
]

NORMALIZE_PATTERNS = [
    (re.compile(r"\bline:\s*\d+\b", re.I), "line:N"),
    (re.compile(r"\bline \d+\b", re.I), "line N"),
    (re.compile(r"\bcolumn \d+\b", re.I), "column N"),
    (re.compile(r"\b0x[0-9a-f]+\b", re.I), "0xHEX"),
    (re.compile(r"\b\d+\b"), "N"),
    (re.compile(r'"[^"\n]*"'), '"STR"'),
    (re.compile(r"'[^'\n]*'"), "'STR'"),
]


def read_text(path: pathlib.Path) -> str:
    encodings = ("utf-8-sig", "utf-8", "cp932", "utf-16", "latin-1")
    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", b"", 0, 1, f"Could not decode {path}")


def normalize_message(message: str) -> str:
    normalized = " ".join(message.strip().split())
    for pattern, replacement in NORMALIZE_PATTERNS:
        normalized = pattern.sub(replacement, normalized)
    return normalized


def detect_severity(message: str) -> str:
    for name, pattern in SEVERITY_RULES:
        if pattern.search(message):
            return name
    return "other"


def detect_category(message: str) -> str:
    for name, pattern in CATEGORY_RULES:
        if pattern.search(message):
            return name
    return "other"


def shorten(text: str, limit: int = 140) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def iter_lines(text: str) -> Iterable[str]:
    for raw_line in text.splitlines():
        line = raw_line.strip("\ufeff")
        if line.strip():
            yield line


def summarize_log(text: str, top_n: int) -> str:
    severity_counts: collections.Counter[str] = collections.Counter()
    category_counts: collections.Counter[str] = collections.Counter()
    message_counts: collections.Counter[str] = collections.Counter()
    message_samples: dict[str, str] = {}
    source_counts: collections.Counter[str] = collections.Counter()
    path_counts: collections.Counter[str] = collections.Counter()

    total_lines = 0

    for line in iter_lines(text):
        total_lines += 1
        source = "unknown"
        message = line
        match = LINE_PATTERN.match(line)
        if match:
            source = match.group("source").strip()
            message = match.group("message").strip()

        severity = detect_severity(message)
        category = detect_category(message)
        normalized = normalize_message(message)

        severity_counts[severity] += 1
        category_counts[category] += 1
        source_counts[source] += 1
        message_counts[normalized] += 1
        message_samples.setdefault(normalized, shorten(message, 180))

        for path in PATH_PATTERN.findall(message):
            path_counts[path.replace("\\", "/")] += 1

    lines: list[str] = []
    lines.append("=== HOI4 Error Summary ===")
    lines.append(f"Total non-empty lines: {total_lines}")
    lines.append("")

    if total_lines == 0:
        lines.append("No log lines found.")
        return "\n".join(lines)

    lines.append("Severity counts:")
    for name, count in severity_counts.most_common():
        lines.append(f"- {name}: {count}")
    lines.append("")

    lines.append("Category counts:")
    for name, count in category_counts.most_common():
        lines.append(f"- {name}: {count}")
    lines.append("")

    lines.append(f"Top {top_n} repeated messages:")
    for normalized, count in message_counts.most_common(top_n):
        lines.append(f"- {count}x {message_samples[normalized]}")
    lines.append("")

    lines.append(f"Top {top_n} log sources:")
    for source, count in source_counts.most_common(top_n):
        lines.append(f"- {count}x {source}")
    lines.append("")

    if path_counts:
        lines.append(f"Top {top_n} referenced paths:")
        for path, count in path_counts.most_common(top_n):
            lines.append(f"- {count}x {path}")
        lines.append("")

    lines.append("Quick diagnosis:")
    biggest_categories = [name for name, _ in category_counts.most_common(3)]
    if "missing_file" in biggest_categories:
        lines.append("- Missing file errors are prominent. Check referenced file paths and descriptor/replace_path coverage first.")
    if "parse_error" in biggest_categories or "unknown_key" in biggest_categories:
        lines.append("- Parser or unknown-key issues are frequent. Fix one representative message, then rerun because many follow-on errors may disappear.")
    if "localisation" in biggest_categories:
        lines.append("- Localisation problems are common. Compare key names between script files and localisation yml files.")
    if "gfx_asset" in biggest_categories:
        lines.append("- GFX or asset loading issues are common. Verify sprite definitions, file extensions, and exact path casing/spelling.")
    if "map_data" in biggest_categories:
        lines.append("- Map/state/province issues are common. Validate IDs, region membership, and referenced assets.")
    if biggest_categories == ["other"] or not any(cat in biggest_categories for cat in ("missing_file", "parse_error", "unknown_key", "localisation", "gfx_asset", "map_data")):
        lines.append("- Errors are mixed. Start with the most repeated message and the busiest log source.")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarize HOI4 mod error logs into repeated issues and likely fix areas."
    )
    parser.add_argument("logfile", type=pathlib.Path, help="Path to error.log or another text log")
    parser.add_argument("--top", type=int, default=15, help="How many frequent items to show per section")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.logfile.exists():
        print(f"Log file not found: {args.logfile}", file=sys.stderr)
        return 1

    try:
        text = read_text(args.logfile)
    except UnicodeDecodeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(summarize_log(text, max(args.top, 1)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
