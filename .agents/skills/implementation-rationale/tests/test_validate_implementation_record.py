from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPT_DIR))

import validate_implementation_record as validator  # noqa: E402


class ImplementationRecordValidatorTests(unittest.TestCase):
    def read(self, name: str = "valid-record.md") -> str:
        return (FIXTURE_DIR / name).read_text(encoding="utf-8")

    def validate(self, text: str, require_complete: bool = False) -> list[str]:
        return validator.validate_record(text, FIXTURE_DIR, require_complete)

    def test_valid_record(self) -> None:
        self.assertEqual(self.validate(self.read()), [])

    def test_public_api_coverage_is_optional(self) -> None:
        text = self.read()
        start = text.index("## Public API coverage\n")
        end = text.index("## Implementation sequence\n", start)
        text = text[:start] + text[end:]
        self.assertEqual(self.validate(text), [])

    def test_public_api_coverage_requires_a_complete_table(self) -> None:
        text = self.read().replace(
            "| Surface | Kind | Scope | Documentation | Coverage check | State |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| `ExampleApi` | exported type | one public result member | source declaration | `python3 -m unittest` | confirmed |\n",
            "Coverage was reviewed manually.\n",
            1,
        )
        errors = self.validate(text)
        self.assertIn("Public API coverage must contain a Markdown table", errors)

    def test_empty_public_api_coverage_section_is_rejected(self) -> None:
        text = self.read().replace(
            "## Public API coverage\n\n| Surface | Kind | Scope | Documentation | Coverage check | State |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| `ExampleApi` | exported type | one public result member | source declaration | `python3 -m unittest` | confirmed |\n",
            "## Public API coverage\n\n",
            1,
        )
        errors = self.validate(text)
        self.assertIn("section 'public api coverage' is empty", errors)

    def test_public_api_coverage_state_and_cells_are_checked(self) -> None:
        text = self.read().replace(
            "| confirmed |\n\n## Implementation sequence",
            "| pending |\n\n## Implementation sequence",
            1,
        )
        errors = self.validate(text)
        self.assertTrue(
            any(
                "Public API coverage row 1 has unsupported state 'pending'" in error
                for error in errors
            )
        )

        text = self.read().replace("| `ExampleApi` | exported type", "|  | exported type", 1)
        errors = self.validate(text)
        self.assertIn("Public API coverage row 1 has an empty 'surface' cell", errors)

    def test_complete_gate_accepts_complete_record(self) -> None:
        self.assertEqual(self.validate(self.read(), require_complete=True), [])

    def test_complete_gate_rejects_draft_record(self) -> None:
        text = self.read().replace("Status: complete", "Status: draft", 1)
        errors = self.validate(text, require_complete=True)
        self.assertIn("record status must be 'complete' for this validation", errors)

    def test_missing_field_and_section_are_reported(self) -> None:
        text = self.read().replace("Owner: Example team\n", "", 1)
        text = text.replace("## Inputs\n", "## Background\n", 1)
        errors = self.validate(text)
        self.assertIn("missing Owner field", errors)
        self.assertIn("missing required section '## inputs'", errors)

    def test_duplicate_ledger_ids_are_rejected(self) -> None:
        text = self.read().replace("| R2 | State is published", "| R1 | State is published", 1)
        errors = self.validate(text)
        self.assertTrue(any("duplicate rationale ID 'R1'" in error for error in errors))

    def test_every_finding_requires_a_placement(self) -> None:
        text = self.read().replace(
            "| R2 | [example decision](./decision.md) | decision and sensor | injected commit failure | inferred |\n",
            "",
            1,
        )
        errors = self.validate(text)
        self.assertIn("rationale ID 'R2' has no comment or sensor placement", errors)

    def test_placement_cannot_reference_an_unknown_finding(self) -> None:
        text = self.read().replace(
            "| R2 | [example decision]", "| R3 | [example decision]", 1
        )
        errors = self.validate(text)
        self.assertIn("rationale ID 'R2' has no comment or sensor placement", errors)
        self.assertIn("placement references unknown rationale ID 'R3'", errors)

    def test_missing_markdown_link_is_rejected(self) -> None:
        text = self.read().replace("./decision.md", "./missing-decision.md", 1)
        errors = self.validate(text)
        self.assertTrue(any("missing local link target" in error for error in errors))

    def test_missing_source_location_is_rejected(self) -> None:
        text = self.read().replace("`./sample.py:1`", "`./missing.py:1`", 1)
        errors = self.validate(text)
        self.assertTrue(any("missing source location" in error for error in errors))

    def test_table_states_are_validated(self) -> None:
        text = self.read().replace("| confirmed |", "| implemented |", 1)
        errors = self.validate(text)
        self.assertTrue(any("unsupported state 'implemented'" in error for error in errors))

    def test_required_table_cells_cannot_be_empty(self) -> None:
        text = self.read().replace(
            "| R1 | The adapter accepts a wider input shape than the public boundary. | focused negative test |",
            "| R1 | The adapter accepts a wider input shape than the public boundary. |  |",
            1,
        )
        errors = self.validate(text)
        self.assertIn("Rationale ledger row 1 has an empty 'evidence' cell", errors)

    def test_optional_none_sections_require_a_reason(self) -> None:
        text = self.read().replace(
            "None - the implementation follows the accepted example decision.",
            "None",
            1,
        )
        errors = self.validate(text)
        self.assertTrue(any("explicit 'None - reason'" in error for error in errors))

    def test_placeholders_are_rejected(self) -> None:
        text = self.read().replace("Example team", "<team>", 1)
        errors = self.validate(text)
        self.assertTrue(any("unresolved placeholder" in error for error in errors))

    def test_invalid_date_and_status_are_rejected(self) -> None:
        errors = self.validate(self.read("invalid-record.md"))
        self.assertTrue(any("Date must use YYYY-MM-DD" in error for error in errors))
        self.assertTrue(any("unsupported record status" in error for error in errors))

    def test_cli_validates_one_record(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "validate_implementation_record.py"),
                str(FIXTURE_DIR / "valid-record.md"),
                "--require-complete",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_cli_directory_reports_invalid_record(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "validate_implementation_record.py"),
                str(FIXTURE_DIR),
                "--quiet",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
