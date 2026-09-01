#!/usr/bin/env python3
"""Validate the structural and repository-local invariants of a README.

The validator deliberately does not execute commands or check network reachability.
Exit status is 0 for a pass, 1 for validation failures, and 2 for an invalid target.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Sequence
from urllib.parse import unquote, urlparse


PROFILES = ("auto", "library", "cli", "application", "service", "template", "monorepo")

PROFILE_ALIASES = {
    # These are the smallest structural gates. Configuration, support, and
    # policy sections remain conditional on facts found in the repository.
    "library": (),
    "cli": ("usage",),
    "application": ("prerequisites",),
    "service": ("prerequisites",),
    "template": ("prerequisites", "usage"),
    "monorepo": ("development",),
}

SECTION_ALIASES = {
    "installation": ("install", "installation", "setup", "getting started"),
    "quick start": ("quick start", "quickstart", "first use", "success path", "example"),
    "usage": ("usage", "use", "using", "commands", "api", "how to use"),
    "prerequisites": ("prerequisites", "requirements", "before you begin"),
    "configuration": ("configuration", "config", "environment variables", "options"),
    "development": ("development", "developing", "contributing", "testing", "tests"),
}

URL_RE = re.compile(r"https?://[^\s)>`]*")
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
PLACEHOLDER_RE = re.compile(
    r"(?:\b(?:TODO|FIXME|TBD)\b|\{\{[^\n{}]+\}\}|\$\{[^\n{}]+\}|"
    r"\[YOUR_[^\]]+\]|<\s*(?:placeholder|your[-_ ]\w+|project[-_ ]\w+|todo)\s*>)",
    re.IGNORECASE,
)
SECRET_RE = re.compile(
    r"(?:sk-[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|"
    r"AIza[0-9A-Za-z_-]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
)
ABSOLUTE_PATH_RE = re.compile(
    r"(?:^|[ `])/(?:Users|home|private|tmp|var|opt|workspace|mnt)/[^\s`]+|"
    r"(?:^|[ `])[A-Za-z]:[\\/](?:Users|home|tmp|workspace)[\\/][^\s`]+",
    re.I,
)
PATH_TOKEN_RE = re.compile(
    r"(?<![\w./-])((?:(?:\.\./)+|\.\/)?(?:scripts|bin|src|docs|examples|test|tests)/[\w./-]+|"
    r"(?:Makefile|Dockerfile|docker-compose\.ya?ml|package\.json|pyproject\.toml|"
    r"Cargo\.toml|go\.mod|pnpm-workspace\.yaml|yarn\.lock|package-lock\.json))"
)
INSTALL_COMMAND_RE = re.compile(
    r"\b(?:python(?:3)?\s+-m\s+pip|pip(?:3)?|npm|pnpm|yarn|cargo)\s+"
    r"(?:install|i|add)\s+(?:(?:-\S+|--\S+)\s+)*([^\s`]+)",
    re.IGNORECASE,
)


def normalize(value: str) -> str:
    value = re.sub(r"[`*_~]", "", value).strip().lower()
    value = re.sub(r"\s+", " ", value)
    return value


def _outside_fences(text: str) -> list[tuple[int, str]]:
    """Return (line number, line) pairs outside fenced code blocks."""
    result: list[tuple[int, str]] = []
    marker: str | None = None
    length = 0
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if match:
            token = match.group(1)
            if marker is None:
                marker, length = token[0], len(token)
            elif token[0] == marker and len(token) >= length and not match.group(2).strip():
                marker, length = None, 0
            continue
        if marker is None:
            result.append((number, line))
    return result


def headings(text: str) -> list[tuple[int, int, str]]:
    return [
        (line_number, len(match.group(1)), normalize(match.group(2)))
        for line_number, line in _outside_fences(text)
        if (match := HEADING_RE.match(line))
    ]


def _section_body(text: str, heading_line: int, next_heading_line: int | None) -> str:
    lines = text.splitlines()
    start = heading_line
    end = next_heading_line - 1 if next_heading_line is not None else len(lines)
    return "\n".join(lines[start:end])


def _has_alias(section_names: set[str], canonical: str) -> bool:
    aliases = SECTION_ALIASES.get(canonical, (canonical,))

    def matches(name: str, alias: str) -> bool:
        if name == alias or name.startswith(alias + ":") or name.startswith(alias + " "):
            return True
        return alias in name.split()

    return any(
        matches(name, alias)
        for name in section_names
        for alias in aliases
    )


def _section_names_and_bodies(text: str) -> tuple[set[str], dict[str, str]]:
    found = headings(text)
    names = {name for _, level, name in found if level >= 2}
    bodies: dict[str, str] = {}
    for index, (line, level, name) in enumerate(found):
        if level < 2:
            continue
        next_line: int | None = None
        for later_line, later_level, _later_name in found[index + 1 :]:
            if later_level <= level:
                next_line = later_line
                break
        bodies[name] = _section_body(text, line, next_line)
    return names, bodies


def _meaningful(body: str) -> bool:
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return bool(body.strip())


def _repo_root(target: Path) -> Path:
    return target if target.is_dir() else target.parent


def _nearest_project_root(target: Path) -> Path:
    """Find the nearest useful project root for profile and manifest detection."""
    start = target if target.is_dir() else target.parent
    markers = {
        ".git",
        "package.json",
        "pyproject.toml",
        "Cargo.toml",
        "go.mod",
        "pnpm-workspace.yaml",
        "lerna.json",
        "turbo.json",
        "nx.json",
        "rush.json",
        "cookiecutter.json",
        "copier.yml",
    }
    non_git_markers = markers - {".git"}
    current = start.resolve()
    git_root: Path | None = None
    for candidate in (current, *current.parents):
        if any((candidate / marker).exists() for marker in non_git_markers):
            return candidate
        if git_root is None and (candidate / ".git").exists():
            git_root = candidate
    return git_root or current


def _repository_root(target: Path) -> Path:
    """Find the repository boundary used to contain nested README references."""
    start = (target if target.is_dir() else target.parent).resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return _nearest_project_root(target)


def detect_profile(target: Path | str, text: str | None = None) -> str:
    """Infer a README profile from repository files and, secondarily, its text."""
    path = Path(target)
    root = _nearest_project_root(path)
    if text is None and path.is_file():
        text = path.read_text(encoding="utf-8")
    text_lower = (text or "").lower()

    workspace_markers = (
        "pnpm-workspace.yaml",
        "lerna.json",
        "turbo.json",
        "nx.json",
        "rush.json",
    )
    if any((root / marker).exists() for marker in workspace_markers):
        return "monorepo"
    for manifest_name in ("package.json", "pyproject.toml", "Cargo.toml"):
        manifest = root / manifest_name
        if manifest.exists():
            try:
                raw_content = manifest.read_text(encoding="utf-8")
            except OSError:
                raw_content = ""
            content = raw_content.lower()
            workspace_manifest = False
            if manifest_name == "package.json":
                try:
                    package_data = json.loads(raw_content)
                except (json.JSONDecodeError, TypeError):
                    package_data = None
                workspace_manifest = isinstance(package_data, dict) and bool(
                    package_data.get("workspaces")
                )
            elif manifest_name == "Cargo.toml":
                workspace_manifest = bool(re.search(r"(?m)^\s*\[workspace(?:\.|\])", content))
            elif manifest_name == "pyproject.toml":
                workspace_manifest = bool(
                    re.search(r"(?m)^\s*(?:workspace|members)\s*[=:]", content)
                )
            if workspace_manifest:
                return "monorepo"
            if (
                '"bin"' in content
                or "console_scripts" in content
                or "[[bin]]" in content
                or "entry_points" in content
                or "project.scripts" in content
                or "poetry.scripts" in content
            ):
                return "cli"
    if (root / "cookiecutter.json").exists() or (root / "copier.yml").exists() or "cookiecutter" in text_lower:
        return "template"
    if any((root / marker).exists() for marker in ("Dockerfile", "docker-compose.yml", "docker-compose.yaml")):
        if any(token in text_lower for token in ("health", "readiness", "endpoint", "service")):
            return "service"
        dockerfile = root / "Dockerfile"
        if dockerfile.is_file():
            try:
                docker_text = dockerfile.read_text(encoding="utf-8").lower()
            except (OSError, UnicodeError):
                docker_text = ""
            if "expose " in docker_text or "healthcheck" in docker_text:
                return "service"
    if any((root / marker).exists() for marker in ("vite.config.js", "vite.config.ts", "next.config.js", "src/App.tsx", "src/App.jsx")):
        return "application"
    if any(token in text_lower for token in ("argparse", "click", "typer", "commander", "clap", "--help")):
        return "cli"
    if any(token in text_lower for token in ("health check", "readiness", "docker compose", "localhost:")):
        return "service"
    return "library"


def _check_fences(text: str, errors: list[str]) -> None:
    marker: str | None = None
    length = 0
    for _number, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        token = match.group(1)
        if marker is None:
            marker, length = token[0], len(token)
        elif token[0] == marker and len(token) >= length and not match.group(2).strip():
            marker, length = None, 0
    if marker is not None:
        errors.append("unclosed fenced code block")


def _check_headings(text: str, errors: list[str]) -> None:
    found = headings(text)
    h1 = [item for item in found if item[1] == 1]
    if len(h1) != 1:
        errors.append(f"README must contain exactly one H1 (found {len(h1)})")
    elif not h1[0][2]:
        errors.append("README H1 is empty")
    for line_number, level, _name in found:
        if level > 1 and not any(
            previous_level == level - 1
            for previous_line, previous_level, _previous_name in found
            if previous_line < line_number
        ):
            # A skipped level is a warning only when it skips directly from H1 to H3+.
            if level > 2:
                errors.append(f"heading level jumps to H{level} at line {line_number}")


def _check_opening(text: str, errors: list[str]) -> None:
    lines = text.splitlines()
    found = headings(text)
    h1_index = next((index for index, (_line, level, _name) in enumerate(found) if level == 1), None)
    if h1_index is None:
        return
    h1_line = found[h1_index][0]
    next_heading_line = found[h1_index + 1][0] if h1_index + 1 < len(found) else None
    opening: list[str] = []
    end = next_heading_line - 1 if next_heading_line is not None else len(lines)
    for line in lines[h1_line:end]:
        if line.strip() and not line.lstrip().startswith(("<!--", "![", "[")):
            opening.append(line.strip())
    if not opening:
        errors.append("README needs a non-empty opening description after the H1")


def _check_sections(text: str, profile: str, errors: list[str]) -> None:
    names, bodies = _section_names_and_bodies(text)
    required = list(dict.fromkeys(("installation", "quick start") + PROFILE_ALIASES.get(profile, ())))
    # Keep order while de-duplicating aliases.
    seen: set[str] = set()
    for canonical in required:
        if canonical in seen:
            continue
        seen.add(canonical)
        if not _has_alias(names, canonical):
            errors.append(f"missing required section for {profile}: {canonical}")
            continue
        matching = [name for name in bodies if _has_alias({name}, canonical)]
        if matching and not any(_meaningful(bodies[name]) for name in matching):
            errors.append(f"empty required section: {canonical}")


def _check_placeholders_and_secrets(text: str, errors: list[str]) -> None:
    outside = "\n".join(line for _, line in _outside_fences(text))
    for match in PLACEHOLDER_RE.finditer(outside):
        errors.append(f"unresolved placeholder {match.group(0)!r}")
    for match in SECRET_RE.finditer(text):
        errors.append(f"possible credential material {match.group(0)[:12]!r}")
    if ABSOLUTE_PATH_RE.search(outside):
        errors.append("machine-specific absolute path found")


def _check_links(
    text: str,
    base_dir: Path,
    errors: list[str],
    containment_root: Path | None = None,
) -> None:
    containment_root = (containment_root or base_dir).resolve()
    visible_text = "\n".join(line for _, line in _outside_fences(text))
    for url in URL_RE.findall(visible_text):
        parsed = urlparse(url.rstrip(".,;"))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"malformed URL {url!r}")
    link_targets = list(INLINE_LINK_RE.findall(visible_text))
    link_targets.extend(
        target_a or target_b
        for target_a, target_b in re.findall(
            r"(?m)^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))", visible_text
        )
    )
    for raw_target in link_targets:
        target = raw_target.strip().split()[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target_path = unquote(target.split("#", 1)[0])
        if not target_path:
            continue
        candidate = (base_dir / target_path).resolve()
        try:
            candidate.relative_to(containment_root)
        except ValueError:
            errors.append(f"relative link escapes repository: {target!r}")
            continue
        if not candidate.exists():
            errors.append(f"missing local link target {target!r}")


def _check_repo_references(
    text: str,
    base_dir: Path,
    strict: bool,
    errors: list[str],
    containment_root: Path | None = None,
) -> None:
    if not strict:
        return
    containment_root = (containment_root or base_dir).resolve()
    for token in PATH_TOKEN_RE.findall(text):
        candidate = (base_dir / token).resolve()
        try:
            candidate.relative_to(containment_root)
        except ValueError:
            errors.append(f"repository reference escapes root {token!r}")
            continue
        if not candidate.exists():
            errors.append(f"missing repository reference {token!r}")


def _manifest_names(base_dir: Path) -> set[str]:
    names: set[str] = set()
    package_json = base_dir / "package.json"
    if package_json.is_file():
        try:
            value = json.loads(package_json.read_text(encoding="utf-8"))
            if isinstance(value, dict) and isinstance(value.get("name"), str):
                names.add(value["name"])
        except (OSError, UnicodeError, json.JSONDecodeError):
            pass
    for manifest, section in (("pyproject.toml", "project"), ("Cargo.toml", "package")):
        path = base_dir / manifest
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        in_section = False
        for line in content.splitlines():
            section_match = re.match(r"^\s*\[([^\]]+)\]\s*$", line)
            if section_match:
                in_section = section_match.group(1).strip().lower() == section
                continue
            if in_section:
                name_match = re.match(r"^\s*name\s*=\s*[\"']([^\"']+)[\"']", line)
                if name_match:
                    names.add(name_match.group(1))
                    break
    return names


def _check_install_package_names(text: str, base_dir: Path, strict: bool, errors: list[str]) -> None:
    if not strict:
        return
    names = _manifest_names(base_dir)
    if not names:
        return
    normalized_names = {name.lower().replace("_", "-") for name in names}
    for match in INSTALL_COMMAND_RE.finditer(text):
        package = match.group(1).split("[", 1)[0].split("=", 1)[0]
        if package in {".", "-e", "--editable"}:
            continue
        normalized_package = package.lower().replace("_", "-")
        if normalized_package not in normalized_names:
            errors.append(
                f"install command package {package!r} does not match manifest name(s): "
                + ", ".join(sorted(names))
            )


def validate_readme(
    text: str,
    base_dir: Path | str | None = None,
    profile: str = "auto",
    strict: bool = False,
    target: Path | str | None = None,
) -> list[str]:
    """Return human-readable validation failures for README text."""
    errors: list[str] = []
    if profile not in PROFILES:
        return [f"unsupported profile {profile!r}"]
    root = Path(base_dir or ".").resolve()
    if target is not None and profile == "auto":
        profile = detect_profile(Path(target), text)
    elif profile == "auto":
        profile = detect_profile(root, text)
    _check_fences(text, errors)
    _check_headings(text, errors)
    _check_opening(text, errors)
    _check_sections(text, profile, errors)
    _check_placeholders_and_secrets(text, errors)
    containment_root = _repository_root(Path(target)) if target is not None else root
    _check_links(text, root, errors, containment_root)
    _check_repo_references(text, root, strict, errors, containment_root)
    _check_install_package_names(text, root, strict, errors)
    return errors


def _readme_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    ignored = {".git", ".hg", ".svn", "node_modules", ".venv", "venv", "dist", "build"}
    candidates: list[Path] = []
    for candidate in path.rglob("*"):
        if not candidate.is_file() or candidate.name.lower() != "readme.md":
            continue
        if any(part in ignored for part in candidate.relative_to(path).parts):
            continue
        candidates.append(candidate)
    return sorted(candidates, key=lambda item: (len(item.relative_to(path).parts), str(item)))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="README.md or repository directory")
    parser.add_argument("--profile", choices=PROFILES, default="auto")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--quiet", action="store_true", help="print only failures")
    args = parser.parse_args(argv)

    if not args.target.exists():
        print(f"target does not exist: {args.target}")
        return 2
    files = _readme_files(args.target)
    if not files:
        print(f"no README.md found at: {args.target}")
        return 2
    failed = False
    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            print(f"FAIL {file_path}: cannot read ({exc})")
            failed = True
            continue
        errors = validate_readme(
            text,
            base_dir=_repo_root(file_path),
            profile=args.profile,
            strict=args.strict,
            target=file_path,
        )
        if errors:
            failed = True
            print(f"FAIL {file_path}")
            for error in errors:
                print(f"  - {error}")
        elif not args.quiet:
            actual_profile = detect_profile(file_path, text) if args.profile == "auto" else args.profile
            print(f"PASS {file_path} (profile: {actual_profile})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
