#!/usr/bin/env python3
"""Validate Implementation Record structure and repository-local references.

The validator checks the record contract, not whether a rationale is persuasive. Exit status is
0 for a pass, 1 for contract failures, and 2 for an invalid target or no detected records.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


RECORD_STATUS = {"draft", "complete", "superseded", "blocked"}
EVIDENCE_STATUS = {"confirmed", "inferred", "unknown", "not-run", "blocked"}
REQUIRED_FIELDS = ("date", "owner", "status", "baseline", "authorization")
SECTION_ALIASES = {
    "purpose": ("purpose",),
    "scope": ("scope",),
    "inputs": ("inputs", "design inputs"),
    "implementation sequence": ("implementation sequence",),
    "rationale ledger": ("rationale ledger",),
    "comment and sensor map": (
        "comment and sensor map",
        "comment/sensor map",
        "placement map",
    ),
    "verification": ("verification",),
    "drift and decisions": ("drift and decisions", "design drift"),
    "remaining boundaries": ("remaining boundaries",),
}
OPTIONAL_SECTION_ALIASES = {
    "public api coverage": (
        "public api coverage",
        "public surface coverage",
        "api coverage",
    ),
}
LEDGER_COLUMNS = {
    "id": ("id",),
    "finding": ("finding", "finding/observation", "observation"),
    "evidence": ("evidence",),
    "impact": ("impact", "impact if changed", "failure if changed"),
    "placement": ("placement", "primary placement"),
    "state": ("state", "status"),
}
MAP_COLUMNS = {
    "id": ("id",),
    "source": ("source", "source location", "location"),
    "role": ("role",),
    "link": ("link", "link or check", "reference", "sensor/check"),
    "state": ("state", "status"),
}
VERIFICATION_COLUMNS = {
    "check": ("check",),
    "command": ("command",),
    "environment": ("environment",),
    "result": ("result",),
    "state": ("state", "status"),
}
PUBLIC_API_COLUMNS = {
    "surface": ("surface", "api surface"),
    "kind": ("kind", "surface kind"),
    "scope": ("scope",),
    "documentation": ("documentation", "documentation location", "doc location"),
    "coverage": ("coverage", "coverage check", "check"),
    "state": ("state", "status"),
}

HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^\s*([A-Za-z][A-Za-z /_-]+):\s*(.*?)\s*$", re.MULTILINE)
TITLE_RE = re.compile(
    r"^\s*#\s+Implementation Record\s*:\s*\S.*$", re.IGNORECASE | re.MULTILINE
)
SEPARATOR_CELL_RE = re.compile(r"^:?-{3,}:?$")
RATIONALE_ID_RE = re.compile(r"^R[1-9][0-9]*$", re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
URL_RE = re.compile(r"https?://[^\s)>`]+")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
PLACEHOLDER_RE = re.compile(
    r"(?:\b(?:TODO|FIXME|TBD)\b|\{\{[^\n{}]+\}\}|\$\{[^\n{}]+\}|"
    r"<\s*(?:\.\.\.|slug|person|team|scope|branch|sha|finding|observation|"
    r"evidence|impact|placement|source|location|role|link|check|command|environment|"
    r"result|reason|placeholder|YYYY-MM-DD)[^>]*>)",
    re.IGNORECASE,
)


def normalize(value: str) -> str:
    value = re.sub(r"[`*_~]", "", value).strip().lower()
    value = value.replace("&", "and")
    value = re.sub(r"\s+", " ", value)
    return value


def headings(text: str) -> list[tuple[int, int, str]]:
    return [
        (match.start(), len(match.group(1)), normalize(match.group(2)))
        for match in HEADING_RE.finditer(text)
    ]


def section_body(text: str, canonical: str) -> str:
    aliases = SECTION_ALIASES.get(canonical, OPTIONAL_SECTION_ALIASES.get(canonical, ()))
    wanted = {normalize(alias) for alias in aliases}
    found = headings(text)
    for index, (start, level, name) in enumerate(found):
        if name not in wanted:
            continue
        heading_match = HEADING_RE.match(text, start)
        if heading_match is None:
            return ""
        end = len(text)
        for next_start, next_level, _next_name in found[index + 1 :]:
            if next_level <= level:
                end = next_start
                break
        return text[heading_match.end() : end].strip()
    return ""


def first_field(text: str, name: str) -> str | None:
    wanted = normalize(name)
    for match in FIELD_RE.finditer(text):
        if normalize(match.group(1)) == wanted:
            return match.group(2).strip()
    return None


def meaningful(body: str) -> bool:
    cleaned = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    cleaned = re.sub(r"^\s*[|:-]+\s*$", "", cleaned, flags=re.MULTILINE)
    return bool(cleaned.strip())


def split_table_row(line: str) -> list[str]:
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [cell.strip().replace(r"\|", "|") for cell in cells]


def first_table(body: str) -> tuple[list[str], list[list[str]]] | None:
    lines = body.splitlines()
    for index in range(len(lines) - 1):
        if "|" not in lines[index] or "|" not in lines[index + 1]:
            continue
        headers = split_table_row(lines[index])
        separators = split_table_row(lines[index + 1])
        if len(headers) != len(separators) or not all(
            SEPARATOR_CELL_RE.fullmatch(cell) for cell in separators
        ):
            continue
        rows: list[list[str]] = []
        for line in lines[index + 2 :]:
            if "|" not in line:
                break
            cells = split_table_row(line)
            if len(cells) < len(headers):
                cells.extend([""] * (len(headers) - len(cells)))
            rows.append(cells[: len(headers)])
        return headers, rows
    return None


def column_indexes(
    headers: list[str], required: dict[str, tuple[str, ...]], errors: list[str], label: str
) -> dict[str, int]:
    normalized = [normalize(header) for header in headers]
    indexes: dict[str, int] = {}
    for canonical, aliases in required.items():
        for index, header in enumerate(normalized):
            if header in {normalize(alias) for alias in aliases}:
                indexes[canonical] = index
                break
        else:
            errors.append(f"{label} table is missing the {canonical!r} column")
    return indexes


def clean_cell(value: str) -> str:
    value = re.sub(r"^\[([^]]+)\].*$", r"\1", value.strip())
    return re.sub(r"[`*_~]", "", value).strip()


def state_value(value: str) -> str:
    return clean_cell(value).split(";", 1)[0].strip().lower()


def validate_table_states(
    rows: list[list[str]], state_index: int | None, errors: list[str], label: str
) -> None:
    if state_index is None:
        return
    for row_number, row in enumerate(rows, 1):
        value = state_value(row[state_index])
        if value not in EVIDENCE_STATUS:
            errors.append(
                f"{label} row {row_number} has unsupported state {value!r}; "
                f"expected one of {sorted(EVIDENCE_STATUS)}"
            )


def validate_required_cells(
    rows: list[list[str]], indexes: dict[str, int], errors: list[str], label: str
) -> None:
    for row_number, row in enumerate(rows, 1):
        for canonical, index in indexes.items():
            if not clean_cell(row[index]):
                errors.append(
                    f"{label} row {row_number} has an empty {canonical!r} cell"
                )


def repository_root(base_dir: Path) -> Path:
    for candidate in (base_dir, *base_dir.parents):
        if (candidate / ".git").exists():
            return candidate
    return base_dir


def strip_line_anchor(value: str) -> str:
    return re.sub(r":(?:[1-9][0-9]*)(?::[1-9][0-9]*)?$", "", value)


def check_source_locations(
    rows: list[list[str]], source_index: int | None, base_dir: Path, errors: list[str]
) -> None:
    if source_index is None:
        return
    root = repository_root(base_dir)
    for row_number, row in enumerate(rows, 1):
        source = row[source_index]
        tokens = INLINE_CODE_RE.findall(source)
        for token in tokens:
            token = strip_line_anchor(token.strip())
            if not token or any(char.isspace() for char in token):
                continue
            if token.startswith(("http://", "https://")):
                continue
            if token.startswith(("./", "../")):
                target = base_dir / token
            elif "/" in token or Path(token).suffix:
                target = root / token
            else:
                continue
            if not target.exists():
                errors.append(
                    f"comment and sensor map row {row_number} references missing source "
                    f"location {token!r}"
                )


def check_links(text: str, base_dir: Path | None, errors: list[str]) -> None:
    for url in URL_RE.findall(text):
        if any(char in url for char in '<>"\''):
            errors.append(f"malformed URL {url!r}")
    if base_dir is None:
        return
    for target in MARKDOWN_LINK_RE.findall(text):
        target = unquote(target)
        if target.startswith(("http://", "https://", "mailto:", "#", "/")):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if target and not (base_dir / target).exists():
            errors.append(f"missing local link target {target!r} (from {base_dir})")


def check_placeholders(text: str, errors: list[str]) -> None:
    for match in PLACEHOLDER_RE.finditer(text):
        errors.append(f"unresolved placeholder {match.group(0)!r}")


def validate_record(
    text: str, base_dir: Path | None = None, require_complete: bool = False
) -> list[str]:
    errors: list[str] = []

    if not TITLE_RE.search("\n".join(text.splitlines()[:20])):
        errors.append("missing '# Implementation Record: <slug>' title")

    for field in REQUIRED_FIELDS:
        value = first_field(text, field)
        if value is None or not value:
            errors.append(f"missing {field.title()} field")

    status = first_field(text, "status")
    if status is not None and status.lower() not in RECORD_STATUS:
        errors.append(
            f"unsupported record status {status!r}; expected one of {sorted(RECORD_STATUS)}"
        )
    if require_complete and (status is None or status.lower() != "complete"):
        errors.append("record status must be 'complete' for this validation")

    date_value = first_field(text, "date")
    if date_value:
        try:
            parsed_date = date.fromisoformat(date_value)
        except ValueError:
            errors.append(f"Date must use YYYY-MM-DD, got {date_value!r}")
        else:
            if parsed_date.isoformat() != date_value:
                errors.append(f"Date must use YYYY-MM-DD, got {date_value!r}")

    found_headings = {name for _start, _level, name in headings(text)}
    for canonical, aliases in SECTION_ALIASES.items():
        if not any(normalize(alias) in found_headings for alias in aliases):
            errors.append(f"missing required section '## {canonical}'")
            continue
        body = section_body(text, canonical)
        if not meaningful(body):
            errors.append(f"section {canonical!r} is empty")

    public_api_body = section_body(text, "public api coverage")
    public_api_heading = any(
        normalize(alias) in found_headings
        for alias in OPTIONAL_SECTION_ALIASES["public api coverage"]
    )
    if public_api_heading and not meaningful(public_api_body):
        errors.append("section 'public api coverage' is empty")
    elif public_api_body:
        public_api = first_table(public_api_body)
        if public_api is None:
            errors.append("Public API coverage must contain a Markdown table")
        else:
            headers, rows = public_api
            indexes = column_indexes(
                headers, PUBLIC_API_COLUMNS, errors, "Public API coverage"
            )
            if not rows:
                errors.append("Public API coverage must contain at least one surface")
            validate_required_cells(rows, indexes, errors, "Public API coverage")
            validate_table_states(rows, indexes.get("state"), errors, "Public API coverage")

    ledger_ids: set[str] = set()
    ledger = first_table(section_body(text, "rationale ledger"))
    if ledger is None:
        errors.append("Rationale ledger must contain a Markdown table")
    else:
        headers, rows = ledger
        indexes = column_indexes(headers, LEDGER_COLUMNS, errors, "Rationale ledger")
        if not rows:
            errors.append("Rationale ledger must contain at least one finding")
        validate_required_cells(rows, indexes, errors, "Rationale ledger")
        if "id" in indexes:
            for row_number, row in enumerate(rows, 1):
                finding_id = clean_cell(row[indexes["id"]]).upper()
                if not RATIONALE_ID_RE.fullmatch(finding_id):
                    errors.append(
                        f"Rationale ledger row {row_number} has invalid ID {finding_id!r}; "
                        "expected R1, R2, ..."
                    )
                elif finding_id in ledger_ids:
                    errors.append(f"duplicate rationale ID {finding_id!r}")
                else:
                    ledger_ids.add(finding_id)
        validate_table_states(rows, indexes.get("state"), errors, "Rationale ledger")

    mapped_ids: set[str] = set()
    placement = first_table(section_body(text, "comment and sensor map"))
    if placement is None:
        errors.append("Comment and sensor map must contain a Markdown table")
    else:
        headers, rows = placement
        indexes = column_indexes(headers, MAP_COLUMNS, errors, "Comment and sensor map")
        if not rows:
            errors.append("Comment and sensor map must contain at least one placement")
        validate_required_cells(rows, indexes, errors, "Comment and sensor map")
        if "id" in indexes:
            for row_number, row in enumerate(rows, 1):
                finding_id = clean_cell(row[indexes["id"]]).upper()
                if not RATIONALE_ID_RE.fullmatch(finding_id):
                    errors.append(
                        f"Comment and sensor map row {row_number} has invalid ID "
                        f"{finding_id!r}"
                    )
                else:
                    mapped_ids.add(finding_id)
        validate_table_states(rows, indexes.get("state"), errors, "Comment and sensor map")
        if base_dir is not None:
            check_source_locations(rows, indexes.get("source"), base_dir, errors)

    for finding_id in sorted(ledger_ids - mapped_ids):
        errors.append(f"rationale ID {finding_id!r} has no comment or sensor placement")
    for finding_id in sorted(mapped_ids - ledger_ids):
        errors.append(f"placement references unknown rationale ID {finding_id!r}")

    verification = first_table(section_body(text, "verification"))
    if verification is None:
        errors.append("Verification must contain a Markdown table")
    else:
        headers, rows = verification
        indexes = column_indexes(headers, VERIFICATION_COLUMNS, errors, "Verification")
        if not rows:
            errors.append("Verification must contain at least one check")
        validate_required_cells(rows, indexes, errors, "Verification")
        validate_table_states(rows, indexes.get("state"), errors, "Verification")

    for optional in ("implementation sequence", "drift and decisions", "remaining boundaries"):
        body = section_body(text, optional)
        if body and normalize(body) in {"none", "n/a", "not applicable"}:
            errors.append(
                f"section {optional!r} must contain content or an explicit 'None - reason'"
            )

    check_placeholders(text, errors)
    check_links(text, base_dir, errors)
    return errors


def detect_record(text: str) -> bool:
    return bool(TITLE_RE.search("\n".join(text.splitlines()[:20])))


def iter_markdown(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
    elif path.is_dir():
        yield from sorted(candidate for candidate in path.rglob("*.md") if candidate.is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Implementation Record or directory to inspect")
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="fail unless every detected record has Status: complete",
    )
    parser.add_argument("--quiet", action="store_true", help="print only failures")
    args = parser.parse_args(argv)

    if not args.path.exists():
        print(f"error: path does not exist: {args.path}", file=sys.stderr)
        return 2
    if not args.path.is_file() and not args.path.is_dir():
        print(f"error: path is not a file or directory: {args.path}", file=sys.stderr)
        return 2

    selected = 0
    failed = 0
    for artifact in iter_markdown(args.path):
        try:
            text = artifact.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            print(f"FAIL {artifact}: cannot decode UTF-8 ({exc})")
            selected += 1
            failed += 1
            continue
        if not detect_record(text):
            if args.path.is_file():
                print(f"error: no Implementation Record found in {artifact}", file=sys.stderr)
                return 2
            continue

        selected += 1
        errors = validate_record(text, artifact.parent, args.require_complete)
        if errors:
            failed += 1
            print(f"FAIL {artifact}")
            for error in errors:
                print(f"  - {error}")
        elif not args.quiet:
            print(f"PASS {artifact}")

    if selected == 0:
        print("error: no Implementation Records found", file=sys.stderr)
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
