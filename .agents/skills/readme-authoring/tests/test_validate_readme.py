from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPT_DIR))

import validate_readme  # noqa: E402


class ReadmeValidatorTests(unittest.TestCase):
    def read(self, name: str) -> str:
        return (FIXTURE_DIR / name).read_text(encoding="utf-8")

    def test_valid_library(self) -> None:
        errors = validate_readme.validate_readme(
            self.read("valid-library.md"), FIXTURE_DIR, profile="library"
        )
        self.assertEqual(errors, [])

    def test_valid_cli(self) -> None:
        errors = validate_readme.validate_readme(
            self.read("valid-cli.md"), FIXTURE_DIR, profile="cli"
        )
        self.assertEqual(errors, [])

    def test_invalid_fixture_reports_multiple_failures(self) -> None:
        errors = validate_readme.validate_readme(
            self.read("invalid-readme.md"), FIXTURE_DIR, profile="library"
        )
        self.assertTrue(any("unclosed fenced" in error for error in errors))
        self.assertTrue(any("missing local link target" in error for error in errors))

    def test_missing_quick_start_is_reported(self) -> None:
        text = self.read("valid-library.md").replace("## Quick start\n", "## Walkthrough\n")
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("quick start" in error for error in errors))

    def test_missing_h1_is_reported(self) -> None:
        text = self.read("valid-library.md").replace("# Acme Parse\n\n", "", 1)
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("exactly one H1" in error for error in errors))

    def test_empty_required_section_is_reported(self) -> None:
        text = self.read("valid-library.md").replace(
            "## Quick start\n\n```python", "## Quick start\n\n## Usage\n\n```python", 1
        )
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("empty required section: quick start" in error for error in errors))

    def test_unclosed_fence_is_reported(self) -> None:
        text = self.read("valid-library.md") + "\n```sh\necho unfinished\n"
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("unclosed fenced" in error for error in errors))

    def test_missing_local_link_is_reported(self) -> None:
        text = self.read("valid-library.md").replace(
            "[API reference](docs/api.md)", "[API reference](docs/missing.md)"
        )
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("missing local link target" in error for error in errors))

    def test_reference_style_local_link_is_checked(self) -> None:
        text = self.read("valid-library.md") + "\n[missing]: docs/missing.md\n"
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("missing local link target" in error for error in errors))

    def test_nested_readme_can_link_to_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            package = root / "packages" / "parser"
            package.mkdir(parents=True)
            (package / "pyproject.toml").write_text(
                "[project]\nname = 'parser'\n", encoding="utf-8"
            )
            readme = package / "README.md"
            readme.write_text(
                self.read("valid-library.md").replace(
                    "docs/api.md", "../../docs/guide.md"
                ).replace("](LICENSE)", "](../../LICENSE)"),
                encoding="utf-8",
            )
            errors = validate_readme.validate_readme(
                readme.read_text(encoding="utf-8"),
                package,
                profile="library",
                target=readme,
            )
            self.assertEqual(errors, [])

    def test_strict_nested_repository_reference_can_reach_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            package = root / "packages" / "parser"
            package.mkdir(parents=True)
            readme = package / "README.md"
            readme.write_text(
                self.read("valid-library.md").replace(
                    "docs/api.md", "../../docs/guide.md"
                ).replace("](LICENSE)", "](../../LICENSE)"),
                encoding="utf-8",
            )
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            errors = validate_readme.validate_readme(
                readme.read_text(encoding="utf-8"),
                package,
                profile="library",
                strict=True,
                target=readme,
            )
            self.assertEqual(errors, [])

    def test_placeholder_is_reported_outside_fences(self) -> None:
        text = self.read("valid-library.md").replace("Acme Parse", "<placeholder>")
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("unresolved placeholder" in error for error in errors))

    def test_placeholder_inside_code_is_allowed(self) -> None:
        text = self.read("valid-library.md").replace(
            "acme_parse.parse(\"hello\")", "acme_parse.parse(\"<placeholder>\")"
        )
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertEqual(errors, [])

    def test_malformed_url_is_reported(self) -> None:
        text = self.read("valid-library.md") + "\nSee https:// for details.\n"
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("malformed URL" in error for error in errors))

    def test_possible_secret_is_reported(self) -> None:
        text = self.read("valid-library.md") + "\nToken: sk-1234567890abcdef1234567890.\n"
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("possible credential" in error for error in errors))

    def test_machine_path_is_reported(self) -> None:
        text = self.read("valid-library.md") + "\nRun it from `/Users/alice/project`.\n"
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("absolute path" in error for error in errors))

    def test_unix_temp_path_is_reported(self) -> None:
        text = self.read("valid-library.md") + "\nArtifacts are in `/tmp/acme-build`.\n"
        errors = validate_readme.validate_readme(text, FIXTURE_DIR, profile="library")
        self.assertTrue(any("absolute path" in error for error in errors))

    def test_strict_repository_reference_check(self) -> None:
        text = self.read("valid-library.md") + "\nSee `scripts/missing.py`.\n"
        errors = validate_readme.validate_readme(
            text, FIXTURE_DIR, profile="library", strict=True
        )
        self.assertTrue(any("missing repository reference" in error for error in errors))

    def test_strict_install_name_matches_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                self.read("valid-library.md").replace("acme-parse", "wrong-name"),
                encoding="utf-8",
            )
            (root / "pyproject.toml").write_text(
                "[project]\nname = 'acme-parse'\n", encoding="utf-8"
            )
            errors = validate_readme.validate_readme(
                (root / "README.md").read_text(encoding="utf-8"),
                root,
                profile="library",
                strict=True,
                target=root / "README.md",
            )
            self.assertTrue(any("does not match manifest" in error for error in errors))

    def test_auto_detection_for_cli_fixture(self) -> None:
        fixture = FIXTURE_DIR / "valid-cli.md"
        self.assertEqual(validate_readme.detect_profile(fixture), "cli")

    def test_auto_detection_prefers_nearest_package_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()
            package = root / "packages" / "parser"
            package.mkdir(parents=True)
            (root / "pnpm-workspace.yaml").write_text("packages: [packages/*]\n", encoding="utf-8")
            (package / "pyproject.toml").write_text(
                "[project]\nname = 'parser'\n", encoding="utf-8"
            )
            readme = package / "README.md"
            readme.write_text(self.read("valid-library.md"), encoding="utf-8")
            self.assertEqual(validate_readme.detect_profile(readme), "library")

    def test_auto_detection_recognizes_single_workspace_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "packages").mkdir()
            (root / "package.json").write_text(
                '{"name":"workspace-root","workspaces":["packages/*"]}\n',
                encoding="utf-8",
            )
            readme = root / "README.md"
            readme.write_text(self.read("valid-library.md"), encoding="utf-8")
            self.assertEqual(validate_readme.detect_profile(readme), "monorepo")

    def test_cli_validates_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(self.read("valid-library.md"), encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "api.md").write_text("# API\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "pyproject.toml").write_text(
                "[project]\nname='acme-parse'\n", encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / "validate_readme.py"), str(root), "--quiet"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_cli_validates_nested_readmes_and_skips_build_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(self.read("valid-library.md"), encoding="utf-8")
            nested = root / "packages" / "cli"
            nested.mkdir(parents=True)
            (nested / "README.md").write_text(self.read("valid-cli.md"), encoding="utf-8")
            generated = root / "dist"
            generated.mkdir()
            (generated / "README.md").write_text(self.read("invalid-readme.md"), encoding="utf-8")
            self.assertEqual(len(validate_readme._readme_files(root)), 2)

    def test_cli_invalid_target_exit_code(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "validate_readme.py"), "/no/such/readme"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
