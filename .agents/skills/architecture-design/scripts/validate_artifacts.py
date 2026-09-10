#!/usr/bin/env python3
"""Validate Architecture Brief and ADR Markdown without third-party packages.

The validator checks the artifact contract, not architectural correctness.  It intentionally
reports missing evidence or thresholds instead of trying to infer them.  Usage:

    validate_artifacts.py docs/architecture
    validate_artifacts.py ADR-0001-choice.md --kind adr
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


BRIEF_STATUS = {"draft", "in-review", "accepted", "superseded", "blocked"}
ADR_STATUS = {"proposed", "accepted", "rejected", "superseded", "deprecated"}
EVIDENCE_STATUS = {"confirmed", "inferred", "unknown", "not-run", "blocked"}

BRIEF_SECTIONS = (
    "objective",
    "non-goals",
    "baseline",
    "map",
    "glossary",
    "drivers and scenarios",
    "candidates",
    "evidence",
    "probes",
    "decision",
    "sensors",
    "migration and rollback",
    "open questions",
)

ADR_SECTIONS = (
    "context",
    "decision",
    "alternatives",
    "evidence",
    "consequences",
    "confidence",
    "revisit trigger",
    "supersedes",
    "superseded by",
    "migration and rollback",
)

PLACEHOLDER_RE = re.compile(
    r"<\s*(?:\.\.\.|slug|number|id|term|claim|option|owner|question|invariant|"
    r"path(?:\s+or\s+url)?|url(?:/path/command)?|version(?:\s+or\s+sha)?|"
    r"person(?:\s+or\s+team)?|team|decision(?:\s+title)?|short\s+name|"
    r"YYYY-MM-DD|stimulus|context|response|metric|threshold|priority|result|"
    r"hypothesis|baseline|environment|scope|action|slug)\s*>",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://[^\s)>`]+")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^\s*([A-Za-z][A-Za-z /_-]+):\s*(.*?)\s*$", re.MULTILINE)
STATE_FIELD_RE = re.compile(
    r"\b(?:state|status)\s*:\s*([A-Za-z][A-Za-z-]*)\b", re.IGNORECASE
)


def normalize(value: str) -> str:
    """Normalize a heading or label for tolerant comparison."""

    value = value.strip().lower().replace("—", "-").replace("–", "-")
    value = re.sub(r"[`*_]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value


def headings(text: str) -> list[str]:
    return [normalize(match.group(2)) for match in HEADING_RE.finditer(text)]


def section_body(text: str, section: str) -> str:
    """Return the body following a heading until the next peer or parent heading."""

    wanted = normalize(section)
    match = None
    for candidate in HEADING_RE.finditer(text):
        if normalize(candidate.group(2)) == wanted:
            match = candidate
            break
    if match is None:
        return ""
    level = len(match.group(1))
    end = len(text)
    for next_heading in HEADING_RE.finditer(text, match.end()):
        if len(next_heading.group(1)) <= level:
            end = next_heading.start()
            break
    return text[match.end() : end].strip()


def first_field(text: str, name: str) -> str | None:
    wanted = normalize(name)
    for match in FIELD_RE.finditer(text):
        if normalize(match.group(1)) == wanted:
            return match.group(2).strip()
    return None


def meaningful(body: str) -> bool:
    """Whether a section has content beyond table separators and whitespace."""

    cleaned = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    cleaned = re.sub(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*[|:-]+\s*$", "", cleaned, flags=re.MULTILINE)
    return bool(cleaned.strip())


def has_none_reason(body: str) -> bool:
    return bool(re.match(r"(?is)^\s*none\s*(?:-|—|:)\s*.+", body.strip()))


def table_has(body: str, *terms: str) -> bool:
    """Check that a Markdown table header contains each requested term."""

    rows = [line for line in body.splitlines() if "|" in line]
    if not rows:
        return False
    header = normalize(rows[0])
    return all(normalize(term) in header for term in terms)


def row_count(body: str) -> int:
    rows = [line for line in body.splitlines() if "|" in line]
    return sum(1 for line in rows[1:] if not re.search(r"-{3,}", line))


def check_placeholders(text: str, errors: list[str]) -> None:
    for match in PLACEHOLDER_RE.finditer(text):
        errors.append(f"unresolved placeholder {match.group(0)!r}")


def check_states(text: str, errors: list[str], allowed: set[str]) -> None:
    for match in STATE_FIELD_RE.finditer(text):
        value = match.group(1).lower()
        if value not in allowed:
            errors.append(f"unsupported state/status {value!r}; expected one of {sorted(allowed)}")


def split_table_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [cell.strip() for cell in cells]


def check_table_states(text: str, errors: list[str], allowed: set[str]) -> None:
    """Validate values in Markdown columns named State or Status."""

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if "|" not in line:
            continue
        headers = [cell.lower() for cell in split_table_row(line)]
        state_columns = [
            column
            for column, header in enumerate(headers)
            if normalize(header) in {"state", "status"}
        ]
        if not state_columns:
            continue
        for row in lines[index + 1 :]:
            if "|" not in row:
                break
            cells = split_table_row(row)
            if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            for column in state_columns:
                if column >= len(cells) or not cells[column]:
                    continue
                value = re.sub(r"[`*_]", "", cells[column]).strip().lower()
                # Permit a linked status such as [confirmed](...) by checking its
                # first plain token; links remain a documentation concern.
                value = re.sub(r"^\[([^]]+)\].*$", r"\1", value)
                if value not in allowed:
                    errors.append(
                        f"unsupported table state/status {value!r}; expected one of {sorted(allowed)}"
                    )


def check_links(text: str, errors: list[str], base_dir: Path | None = None) -> None:
    # This is deliberately a syntax check. Network reachability belongs to the Evidence
    # gate and must not be made a hidden side effect of validating a document. Relative
    # links are checked locally when the artifact's directory is known.
    for url in URL_RE.findall(text):
        if any(char in url for char in "<>\"'"):
            errors.append(f"malformed URL {url!r}")
    if base_dir is None:
        return
    for target in MARKDOWN_LINK_RE.findall(text):
        target = unquote(target)
        if target.startswith(("http://", "https://", "mailto:", "#", "/")):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target or not target.startswith(("./", "../")):
            continue
        if not (base_dir / target).exists():
            errors.append(f"missing local link target {target!r} (from {base_dir})")


def validate_brief(text: str, base_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    found = set(headings(text))
    for section in BRIEF_SECTIONS:
        if normalize(section) not in found:
            errors.append(f"missing required section '## {section}'")
        elif not meaningful(section_body(text, section)):
            errors.append(f"section '{section}' is empty")
        elif section == "open questions" and not has_none_reason(section_body(text, section)):
            # An empty-looking questions section is easy to mistake for an omitted
            # review. Make the intentional absence explicit.
            body = section_body(text, section)
            if not body.strip() or body.strip().lower() in {"none", "n/a", "not applicable"}:
                errors.append("Open questions must contain a question or an explicit None reason")

    status = first_field(text, "status")
    if status is None:
        errors.append("missing Status field")
    elif status.lower() not in BRIEF_STATUS:
        errors.append(f"unsupported Brief status {status!r}; expected one of {sorted(BRIEF_STATUS)}")

    if not table_has(section_body(text, "glossary"), "term", "scope", "meaning"):
        errors.append("Glossary table must include Term, Scope, and canonical meaning columns")
    if row_count(section_body(text, "glossary")) < 1 and not has_none_reason(section_body(text, "glossary")):
        errors.append("Glossary must contain a data row or an explicit None reason")

    scenario = section_body(text, "drivers and scenarios")
    if not table_has(scenario, "stimulus", "context", "response", "metric", "threshold", "priority"):
        errors.append("Drivers and scenarios table must include stimulus, context, response, metric, threshold, and priority")
    elif row_count(scenario) < 1:
        errors.append("Drivers and scenarios must contain a data row")

    evidence = section_body(text, "evidence")
    if not table_has(evidence, "claim", "source", "version", "state"):
        errors.append("Evidence table must include Claim, Source, Version/commit, and State columns")
    if meaningful(evidence) and not has_none_reason(evidence) and row_count(evidence) < 1:
        errors.append("Evidence must contain a data row or an explicit None reason")

    probes = section_body(text, "probes")
    if not table_has(probes, "question", "hypothesis", "baseline", "threshold", "result", "state"):
        errors.append("Probes table must include Question, Hypothesis, Baseline, Threshold, Result, and State columns")
    elif row_count(probes) < 1 and not has_none_reason(probes):
        errors.append("Probes must contain a data row or an explicit None reason")
    sensors = section_body(text, "sensors")
    if not table_has(sensors, "invariant", "check", "owner", "state") and not table_has(sensors, "invariant", "signal", "owner", "state"):
        errors.append("Sensors table must include Invariant, Check/Signal, Owner, and State columns")
    elif row_count(sensors) < 1 and not has_none_reason(sensors):
        errors.append("Sensors must contain a data row or an explicit None reason")

    check_states(text, errors, EVIDENCE_STATUS | BRIEF_STATUS)
    check_table_states(text, errors, EVIDENCE_STATUS | BRIEF_STATUS)
    check_placeholders(text, errors)
    check_links(text, errors, base_dir)
    return errors


def validate_adr(text: str, base_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    found = set(headings(text))
    for section in ADR_SECTIONS:
        if normalize(section) not in found:
            errors.append(f"missing required section '## {section}'")
        elif not meaningful(section_body(text, section)):
            errors.append(f"section '{section}' is empty")

    status = first_field(text, "status")
    if status is None:
        errors.append("missing Status field")
    elif status.lower() not in ADR_STATUS:
        errors.append(f"unsupported ADR status {status!r}; expected one of {sorted(ADR_STATUS)}")

    alternatives = section_body(text, "alternatives")
    if not table_has(alternatives, "option", "considered", "selected"):
        errors.append("Alternatives table must include Option, considered, and selected rationale columns")
    evidence = section_body(text, "evidence")
    if not re.search(r"\bE\d+\b|none\s*(?:-|—|:)", evidence, re.IGNORECASE):
        errors.append("Evidence must reference an Evidence ID or give an explicit None reason")
    confidence = section_body(text, "confidence")
    if re.search(r"(?i)\b(?:tbd|todo|unknown)\b", confidence):
        errors.append("Confidence must state a level and its supporting assumptions")
    revisit = section_body(text, "revisit trigger")
    if re.search(r"(?i)\b(?:tbd|todo|none)\b", revisit):
        errors.append("Revisit Trigger must name an observable event, threshold, date, or version")

    check_states(text, errors, ADR_STATUS | EVIDENCE_STATUS)
    check_table_states(text, errors, ADR_STATUS | EVIDENCE_STATUS)
    check_placeholders(text, errors)
    check_links(text, errors, base_dir)
    return errors


def detect_kind(path: Path, text: str) -> str | None:
    first_lines = "\n".join(text.splitlines()[:20])
    if re.search(r"^\s*#\s+Architecture Brief\b", first_lines, re.IGNORECASE | re.MULTILINE):
        return "brief"
    if re.search(r"^\s*#\s+ADR(?:[-\s:#]|$)", first_lines, re.IGNORECASE | re.MULTILINE):
        return "adr"
    if re.match(r"(?i)^adr[-_\d]", path.name):
        return "adr"
    return None


def iter_markdown(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
    elif path.is_dir():
        yield from sorted(p for p in path.rglob("*.md") if p.is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Markdown artifact or directory to inspect")
    parser.add_argument("--kind", choices=("auto", "brief", "adr"), default="auto")
    parser.add_argument("--quiet", action="store_true", help="print only failures")
    parser.add_argument(
        "--fail-on-skip", action="store_true",
        help="fail when a Markdown target is not a supported artifact kind",
    )
    args = parser.parse_args(argv)

    if not args.path.exists():
        print(f"error: path does not exist: {args.path}", file=sys.stderr)
        return 2
    if not args.path.is_file() and not args.path.is_dir():
        print(f"error: path is not a file or directory: {args.path}", file=sys.stderr)
        return 2

    selected = 0
    failed = 0
    skipped = 0
    for artifact in iter_markdown(args.path):
        try:
            text = artifact.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            print(f"FAIL {artifact}: cannot decode UTF-8 ({exc})")
            failed += 1
            selected += 1
            continue

        kind = args.kind if args.kind != "auto" else detect_kind(artifact, text)
        if kind is None:
            skipped += 1
            if args.fail_on_skip:
                failed += 1
                print(f"FAIL {artifact}: unsupported artifact kind (--fail-on-skip)")
                continue
            if not args.quiet:
                print(f"SKIP {artifact}: no Architecture Brief or ADR heading")
            continue
        selected += 1
        errors = (
            validate_brief(text, artifact.parent)
            if kind == "brief"
            else validate_adr(text, artifact.parent)
        )
        if errors:
            failed += 1
            print(f"FAIL {artifact} ({kind})")
            for error in errors:
                print(f"  - {error}")
        elif not args.quiet:
            print(f"PASS {artifact} ({kind})")

    if not args.quiet:
        print(f"Coverage: selected={selected}, skipped={skipped}, failed={failed}")
    if selected == 0:
        print("error: no architecture artifacts found", file=sys.stderr)
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
