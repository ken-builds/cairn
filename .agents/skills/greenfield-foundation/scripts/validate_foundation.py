#!/usr/bin/env python3
"""Validate greenfield Foundation Brief and ADR Markdown.

The validator checks the foundation artifact contract, not whether an architecture is
technically correct. It intentionally reports missing thresholds, ownership, evidence, or
handoff details instead of inferring them.

Usage:

    validate_foundation.py docs/architecture/briefs
    validate_foundation.py foundation.md --kind brief
    validate_foundation.py ADR-0001-choice.md --kind adr
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
RECORD_STATE = {"confirmed", "inferred", "unknown", "not-run", "blocked"}

BRIEF_SECTIONS = (
    "objective",
    "non-goals",
    "mandate and baseline",
    "constraints and assumptions",
    "context map",
    "glossary",
    "drivers and scenarios",
    "candidates",
    "foundation blueprint",
    "evidence",
    "probes",
    "decision",
    "bootstrap plan and gates",
    "walking skeleton / first vertical slice",
    "sensors and definition of done",
    "evolution and rollback",
    "open questions",
)

BRIEF_SECTION_ALIASES = {
    "mandate and baseline": ("mandate and baseline",),
    "constraints and assumptions": (
        "constraints and assumptions",
        "assumptions and constraints",
    ),
    "context map": ("context map", "context/map"),
    "foundation blueprint": ("foundation blueprint", "blueprint"),
    "bootstrap plan and gates": ("bootstrap plan and gates", "bootstrap plan"),
    "walking skeleton / first vertical slice": (
        "walking skeleton / first vertical slice",
        "walking skeleton/first vertical slice",
        "walking skeleton",
        "first vertical slice",
    ),
    "sensors and definition of done": (
        "sensors and definition of done",
        "sensors and definition of done (dod)",
    ),
    "evolution and rollback": (
        "evolution and rollback",
        "migration and rollback",
    ),
}

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
    r"<\s*(?:\.\.\.|placeholder|slug|number|four-digit|id|term|claim|option|owner|question|"
    r"invariant|path(?:\s+or\s+url)?|url(?:/path/command)?|version(?:\s+or\s+sha)?|"
    r"person(?:\s+or\s+team)?|team|decision(?:\s+title)?|short\s+name|"
    r"YYYY-MM-DD|stimulus|context|response|metric|threshold|priority|result|"
    r"hypothesis|baseline|environment|scope|action|impact|meaning|aliases?/?relations?|"
    r"input|source|fit|trade-offs?|reversibility|target\s+shape|concern|state|"
    r"deliverables|exit\s+criterion|boundary|check|step|acceptance|path|"
    r"decision(?:\s+and\s+)?title)\s*>",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://[^\s)>`]+")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^\s*([A-Za-z][A-Za-z /_-]+):\s*(.*?)\s*$", re.MULTILINE)
STATE_FIELD_RE = re.compile(r"\bstate\s*:\s*([A-Za-z][A-Za-z-]*)\b", re.IGNORECASE)


def normalize(value: str) -> str:
    """Normalize a heading, label, or table cell for tolerant comparison."""

    value = value.strip().lower().replace("—", "-").replace("–", "-")
    value = re.sub(r"[`*_]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value


def heading_matches(value: str, canonical: str) -> bool:
    normalized = normalize(value)
    aliases = BRIEF_SECTION_ALIASES.get(canonical, (canonical,))
    return any(normalized == normalize(alias) for alias in aliases)


def find_heading(text: str, section: str) -> re.Match[str] | None:
    for match in HEADING_RE.finditer(text):
        if heading_matches(match.group(2), section):
            return match
    return None


def section_body(text: str, section: str) -> str:
    """Return the body following a heading until the next peer or parent heading."""

    match = find_heading(text, section)
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
    cleaned = re.sub(
        r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$",
        "",
        cleaned,
        flags=re.MULTILINE,
    )
    cleaned = re.sub(r"^\s*[|:-]+\s*$", "", cleaned, flags=re.MULTILINE)
    return bool(cleaned.strip())


def has_none_reason(body: str) -> bool:
    """Whether the whole section is an explicit, intentional None statement."""

    return bool(
        re.fullmatch(
            r"\s*(?:[-*+]\s*)?none\s*(?:-|—|:)\s*[^\r\n]+\s*",
            body,
            re.IGNORECASE,
        )
    )


def split_table_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [cell.strip() for cell in cells]


def is_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def table_blocks(body: str) -> list[tuple[list[str], list[list[str]]]]:
    """Return Markdown tables as (normalized headers, data rows)."""

    lines = body.splitlines()
    blocks: list[tuple[list[str], list[list[str]]]] = []
    index = 0
    while index < len(lines) - 1:
        if "|" not in lines[index] or "|" not in lines[index + 1] or not is_separator(lines[index + 1]):
            index += 1
            continue
        headers = [normalize(cell) for cell in split_table_row(lines[index])]
        rows: list[list[str]] = []
        index += 2
        while index < len(lines) and "|" in lines[index]:
            if not is_separator(lines[index]):
                rows.append(split_table_row(lines[index]))
            index += 1
        blocks.append((headers, rows))
    return blocks


def first_table(body: str) -> tuple[list[str], list[list[str]]] | None:
    blocks = table_blocks(body)
    return blocks[0] if blocks else None


def table_has(body: str, *terms: str) -> bool:
    table = first_table(body)
    if table is None:
        return False
    headers, _ = table
    return all(any(normalize(term) in header for header in headers) for term in terms)


def row_count(body: str) -> int:
    table = first_table(body)
    return len(table[1]) if table else 0


def column_index(headers: list[str], *terms: str) -> int | None:
    """Return the first header index containing all requested terms."""

    wanted = [normalize(term) for term in terms]
    for index, header in enumerate(headers):
        if all(term in header for term in wanted):
            return index
    return None


def require_nonempty_cells(
    body: str, label: str, *header_groups: tuple[str, ...]
) -> list[str]:
    """Report blank cells for the requested columns in the first table."""

    table = first_table(body)
    if table is None:
        return []
    headers, rows = table
    columns = [(group, column_index(headers, *group)) for group in header_groups]
    errors: list[str] = []
    for row_number, row in enumerate(rows, 1):
        for group, index in columns:
            if index is None:
                continue
            if index >= len(row) or not row[index].strip():
                errors.append(
                    f"{label} row {row_number} has an empty {'/'.join(group)} cell"
                )
    return errors


def extract_state_token(value: str) -> str | None:
    """Extract a state at the start of a cell, allowing a short annotation."""

    value = re.sub(r"[`*_]", "", value).strip().lower()
    value = re.sub(r"^\[([^]]+)\]", r"\1", value).strip()
    allowed = sorted(RECORD_STATE | BRIEF_STATUS | ADR_STATUS, key=len, reverse=True)
    pattern = r"^(?:" + "|".join(re.escape(item) for item in allowed) + r")"
    match = re.match(pattern + r"(?=$|\s|[;,:()\[\]—–-])", value)
    return match.group(0) if match else None


def check_placeholders(text: str, errors: list[str]) -> None:
    for match in PLACEHOLDER_RE.finditer(text):
        errors.append(f"unresolved placeholder {match.group(0)!r}")


def check_field_states(text: str, errors: list[str]) -> None:
    for match in STATE_FIELD_RE.finditer(text):
        value = match.group(1).lower()
        if value not in RECORD_STATE:
            errors.append(
                f"unsupported State value {value!r}; expected one of {sorted(RECORD_STATE)}"
            )


def check_table_states(text: str, errors: list[str]) -> None:
    """Validate values in Markdown columns whose header names State or Status."""

    for body in (text,):
        for headers, rows in table_blocks(body):
            state_columns = [
                index
                for index, header in enumerate(headers)
                if "state" in header or header == "status"
            ]
            if not state_columns:
                continue
            for row in rows:
                for column in state_columns:
                    if column >= len(row) or not row[column].strip():
                        continue
                    value = extract_state_token(row[column])
                    if value is None:
                        errors.append(
                            f"unsupported table state/status {row[column]!r}; expected a known lifecycle or evidence state"
                        )


def check_links(text: str, errors: list[str], base_dir: Path | None = None) -> None:
    """Check URL syntax and local relative-link targets, never network reachability."""

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
        if not target or target.startswith("//") or ":" in target.split("/", 1)[0]:
            continue
        if not (base_dir / target).exists():
            errors.append(f"missing local link target {target!r} (from {base_dir})")


def require_sections(text: str, sections: Iterable[str], errors: list[str]) -> None:
    for section in sections:
        if find_heading(text, section) is None:
            errors.append(f"missing required section '## {section}'")
            continue
        body = section_body(text, section)
        if not meaningful(body):
            errors.append(f"section '{section}' is empty")


def require_metadata(text: str, fields: Iterable[str], errors: list[str]) -> None:
    for field in fields:
        value = first_field(text, field)
        if value is None or not value.strip():
            errors.append(f"missing {field} field")


def validate_brief(text: str, base_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    require_sections(text, BRIEF_SECTIONS, errors)
    require_metadata(text, ("status", "date", "owner"), errors)

    status = first_field(text, "status")
    if status and status.lower() not in BRIEF_STATUS:
        errors.append(f"unsupported Brief status {status!r}; expected one of {sorted(BRIEF_STATUS)}")

    assumptions = section_body(text, "constraints and assumptions")
    if meaningful(assumptions) and not has_none_reason(assumptions):
        if not table_has(assumptions, "id", "assumption", "impact", "validation", "owner", "state"):
            errors.append(
                "Constraints and assumptions table must include ID, assumption/constraint, impact, validation/owner, and State columns"
            )
        elif row_count(assumptions) < 1:
            errors.append("Constraints and assumptions must contain a data row")
        else:
            errors.extend(
                require_nonempty_cells(
                    assumptions,
                    "Constraints and assumptions",
                    ("id",),
                    ("assumption",),
                    ("impact",),
                    ("validation",),
                    ("state",),
                )
            )

    glossary = section_body(text, "glossary")
    if not has_none_reason(glossary):
        if not table_has(glossary, "term", "scope", "canonical meaning", "source", "aliases"):
            errors.append(
                "Glossary table must include Term, Scope, Canonical meaning, Source, and Aliases/relations columns"
            )
        elif row_count(glossary) < 1:
            errors.append("Glossary must contain a data row")
        else:
            errors.extend(
                require_nonempty_cells(
                    glossary,
                    "Glossary",
                    ("term",),
                    ("scope",),
                    ("canonical", "meaning"),
                    ("source",),
                )
            )

    scenarios = section_body(text, "drivers and scenarios")
    if not table_has(scenarios, "id", "stimulus", "context", "response", "metric", "threshold", "priority"):
        errors.append(
            "Drivers and scenarios table must include ID, Stimulus, Context, Response, Metric, Threshold, and Priority columns"
        )
    elif row_count(scenarios) < 1:
        errors.append("Drivers and scenarios must contain a data row")
    else:
        errors.extend(
            require_nonempty_cells(
                scenarios,
                "Drivers and scenarios",
                ("id",),
                ("stimulus",),
                ("context",),
                ("response",),
                ("metric",),
                ("threshold",),
                ("priority",),
            )
        )

    candidates = section_body(text, "candidates")
    if not table_has(candidates, "id", "option", "fit", "trade-offs", "reversibility", "state"):
        errors.append(
            "Candidates table must include ID, Option, Fit, Trade-offs, Reversibility, and State columns"
        )
    elif row_count(candidates) < 1:
        errors.append("Candidates must contain a data row")
    else:
        errors.extend(
            require_nonempty_cells(
                candidates,
                "Candidates",
                ("id",),
                ("option",),
                ("fit",),
                ("trade-offs",),
                ("reversibility",),
                ("state",),
            )
        )
    if not re.search(r"\bC0\b", candidates, re.IGNORECASE):
        errors.append("Candidates must include C0, the smallest reversible foundation")
    candidate_table = first_table(candidates)
    candidate_ids: set[str] = set()
    if candidate_table is not None:
        id_column = column_index(candidate_table[0], "id")
        if id_column is not None:
            candidate_ids = {
                re.sub(r"[`*_]", "", row[id_column]).strip().upper()
                for row in candidate_table[1]
                if id_column < len(row)
            }

    blueprint = section_body(text, "foundation blueprint")
    if not table_has(blueprint, "concern", "target shape", "owner") or not (
        table_has(blueprint, "evidence/state") or table_has(blueprint, "state")
    ):
        errors.append(
            "Foundation Blueprint table must include Concern, Target shape, Owner, and Evidence/state columns"
        )
    elif row_count(blueprint) < 1:
        errors.append("Foundation Blueprint must contain a data row")
    else:
        errors.extend(
            require_nonempty_cells(
                blueprint,
                "Foundation Blueprint",
                ("concern",),
                ("target", "shape"),
                ("owner",),
                ("state",),
            )
        )
    blueprint_terms = (
        "boundar",
        "dependenc",
        "interface",
        "data",
        "runtime",
        "security",
        "observab",
        "delivery",
        "cost",
    )
    blueprint_lower = blueprint.lower()
    for term in blueprint_terms:
        if term not in blueprint_lower:
            errors.append(f"Foundation Blueprint is missing a concern covering {term}")

    evidence = section_body(text, "evidence")
    if not has_none_reason(evidence):
        if not table_has(evidence, "id", "claim", "source", "version", "accessed", "state", "applicability"):
            errors.append(
                "Evidence table must include ID, Claim, Source, Version/commit, Accessed/measured, State, and Applicability columns"
            )
        elif row_count(evidence) < 1:
            errors.append("Evidence must contain a data row")
        else:
            errors.extend(
                require_nonempty_cells(
                    evidence,
                    "Evidence",
                    ("id",),
                    ("claim",),
                    ("source",),
                    ("state",),
                    ("applicability",),
                )
            )

    probes = section_body(text, "probes")
    if not has_none_reason(probes):
        if not table_has(probes, "id", "question", "hypothesis", "workload", "environment", "baseline", "method", "threshold", "result", "state"):
            errors.append(
                "Probes table must include ID, Question, Hypothesis, Workload/input, Environment, Baseline, Method/budget, Threshold, Result, and State columns"
            )
        elif row_count(probes) < 1:
            errors.append("Probes must contain a data row")
        else:
            errors.extend(
                require_nonempty_cells(
                    probes,
                    "Probes",
                    ("id",),
                    ("question",),
                    ("hypothesis",),
                    ("workload",),
                    ("environment",),
                    ("baseline",),
                    ("method",),
                    ("threshold",),
                    ("result",),
                    ("state",),
                )
            )

    decision = section_body(text, "decision")
    if not re.search(r"(?im)^\s*[`*_ ]*selected candidate[`*_ ]*\s*:", decision):
        errors.append("Decision must identify a Selected candidate")
    if not re.search(r"(?im)^\s*[`*_ ]*rationale[`*_ ]*\s*:", decision):
        errors.append("Decision must include a Rationale")
    if not re.search(r"\bC\d+\b", decision, re.IGNORECASE):
        errors.append("Decision must reference a candidate ID")
    selected_match = re.search(r"(?im)^\s*[`*_ ]*selected candidate[`*_ ]*\s*:\s*([^\s,;]+)", decision)
    if selected_match and candidate_ids:
        selected_id = re.sub(r"[`*_]", "", selected_match.group(1)).upper()
        if selected_id not in candidate_ids:
            errors.append(f"Decision selects {selected_id!r}, which is not present in Candidates")

    gates = section_body(text, "bootstrap plan and gates")
    if not table_has(gates, "gate", "entry", "deliverables", "exit criterion", "owner", "state"):
        errors.append(
            "Bootstrap plan and gates table must include Gate, Entry, Deliverables, Exit criterion, Owner, and State columns"
        )
    elif row_count(gates) < 5:
        errors.append("Bootstrap plan and gates must contain G0 through G4 data rows")
    else:
        errors.extend(
            require_nonempty_cells(
                gates,
                "Bootstrap plan and gates",
                ("gate",),
                ("entry",),
                ("deliverables",),
                ("exit", "criterion"),
                ("owner",),
                ("state",),
            )
        )
        gate_table = first_table(gates)
        if gate_table is not None:
            gate_column = column_index(gate_table[0], "gate")
            gate_values = (
                [row[gate_column] for row in gate_table[1] if gate_column < len(row)]
                if gate_column is not None
                else []
            )
            positions: list[int] = []
            for gate in ("G0", "G1", "G2", "G3", "G4"):
                matches = [
                    index
                    for index, value in enumerate(gate_values)
                    if re.match(rf"^\s*{gate}\b", value, re.IGNORECASE)
                ]
                if len(matches) != 1:
                    errors.append(f"Bootstrap plan and gates must contain exactly one {gate} row")
                else:
                    positions.append(matches[0])
            if len(positions) == 5 and positions != sorted(positions):
                errors.append("Bootstrap plan and gates must list G0 through G4 in order")
    for gate in ("G0", "G1", "G2", "G3", "G4"):
        if not re.search(rf"(?m)^\s*\|\s*{gate}\b", gates, re.IGNORECASE):
            errors.append(f"Bootstrap plan and gates is missing {gate}")

    skeleton = section_body(text, "walking skeleton / first vertical slice")
    if not table_has(skeleton, "step", "boundary", "test", "deploy", "rollback", "acceptance"):
        errors.append(
            "Walking skeleton table must include Step, Boundary crossed, Test/observation, Deploy/rollback, and Acceptance columns"
        )
    elif row_count(skeleton) < 1:
        errors.append("Walking skeleton must contain a data row")
    else:
        errors.extend(
            require_nonempty_cells(
                skeleton,
                "Walking skeleton",
                ("step",),
                ("boundary",),
                ("test",),
                ("deploy",),
                ("acceptance",),
            )
        )
    if not re.search(r"(?i)end[- ]to[- ]end", skeleton):
        errors.append("Walking skeleton must state an end-to-end path")
    for term in ("contract", "data", "test", "deploy", "observ", "rollback"):
        if term not in skeleton.lower():
            errors.append(f"Walking skeleton is missing a {term} path")

    sensors = section_body(text, "sensors and definition of done")
    if not table_has(sensors, "id", "invariant", "check", "when", "owner", "state", "failure"):
        errors.append(
            "Sensors table must include ID, Invariant, Check or signal, When, Owner, State, and Failure action columns"
        )
    elif row_count(sensors) < 1:
        errors.append("Sensors must contain a data row")
    else:
        errors.extend(
            require_nonempty_cells(
                sensors,
                "Sensors",
                ("id",),
                ("invariant",),
                ("check",),
                ("when",),
                ("owner",),
                ("state",),
                ("failure",),
            )
        )
    if not re.search(r"(?i)definition\s+of\s+done(?:\s*[:#]|\s*$)", sensors, re.MULTILINE):
        errors.append("Sensors section must include a Definition of Done")

    evolution = section_body(text, "evolution and rollback")
    if not re.search(r"(?i)rollback|release|evolution|not applicable", evolution):
        errors.append("Evolution and rollback must describe release evolution/rollback or an explicit None reason")

    questions = section_body(text, "open questions")
    if not has_none_reason(questions):
        question_table = first_table(questions)
        if question_table is not None:
            headers, rows = question_table
            if not table_has(questions, "question", "owner", "next", "state"):
                errors.append(
                    "Open questions table must include Question, Owner, Next check, and State columns"
                )
            else:
                errors.extend(
                    require_nonempty_cells(
                        questions,
                        "Open questions",
                        ("question",),
                        ("owner",),
                        ("next",),
                        ("state",),
                    )
                )
        else:
            question_lines = [
                line.strip()
                for line in questions.splitlines()
                if re.match(r"^\s*(?:[-*+] |\d+[.)]\s+)", line)
            ]
            if not question_lines:
                errors.append(
                    "Open questions must contain a question with owner, next check, and state, or an explicit None reason"
                )
            for number, line in enumerate(question_lines, 1):
                if not re.search(r"(?i)\bowner\b\s*:", line):
                    errors.append(f"Open question {number} is missing an owner")
                if not re.search(r"(?i)\bnext\s+check\b\s*:", line):
                    errors.append(f"Open question {number} is missing a next check")
                if not re.search(r"(?i)\bstate\b\s*:", line):
                    errors.append(f"Open question {number} is missing a state")

    check_field_states(text, errors)
    check_table_states(text, errors)
    check_placeholders(text, errors)
    check_links(text, errors, base_dir)
    return errors


def validate_adr(text: str, base_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    require_sections(text, ADR_SECTIONS, errors)
    require_metadata(text, ("status", "date", "deciders"), errors)

    status = first_field(text, "status")
    if status and status.lower() not in ADR_STATUS:
        errors.append(f"unsupported ADR status {status!r}; expected one of {sorted(ADR_STATUS)}")

    alternatives = section_body(text, "alternatives")
    if not table_has(alternatives, "option", "why considered", "why not selected"):
        errors.append("Alternatives table must include Option, Why considered, and Why not selected columns")
    elif row_count(alternatives) < 1:
        errors.append("Alternatives must contain a data row")

    evidence = section_body(text, "evidence")
    if not re.search(r"\bE\d+\b", evidence, re.IGNORECASE) and not has_none_reason(evidence):
        errors.append("Evidence must reference an Evidence ID or give an explicit None reason")

    confidence = section_body(text, "confidence")
    if not re.search(r"(?i)\b(?:high|medium|low)\b", confidence) or re.search(
        r"(?i)\b(?:tbd|todo)\b", confidence
    ):
        errors.append("Confidence must state high, medium, or low and its supporting assumptions")

    revisit = section_body(text, "revisit trigger")
    if re.search(r"(?i)\b(?:tbd|todo|none)\b", revisit):
        errors.append("Revisit Trigger must name an observable event, threshold, date, version, or assumption")

    check_field_states(text, errors)
    check_table_states(text, errors)
    check_placeholders(text, errors)
    check_links(text, errors, base_dir)
    return errors


def detect_kind(path: Path, text: str) -> str | None:
    first_lines = "\n".join(text.splitlines()[:20])
    if re.search(r"^\s*#\s+Foundation Brief\b", first_lines, re.IGNORECASE | re.MULTILINE):
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
            if args.kind == "auto":
                continue
            print(f"FAIL {artifact}: cannot decode UTF-8 ({exc})")
            failed += 1
            selected += 1
            continue

        kind = args.kind if args.kind != "auto" else detect_kind(artifact, text)
        if kind is None:
            if not args.quiet:
                print(f"SKIP {artifact}: no Foundation Brief or ADR heading")
            continue
        selected += 1
        errors = validate_brief(text, artifact.parent) if kind == "brief" else validate_adr(text, artifact.parent)
        if errors:
            failed += 1
            print(f"FAIL {artifact} ({kind})")
            for error in errors:
                print(f"  - {error}")
        elif not args.quiet:
            print(f"PASS {artifact} ({kind})")

    if selected == 0:
        print("error: no Foundation Brief or ADR artifacts found", file=sys.stderr)
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
