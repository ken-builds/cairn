from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPT_DIR))

import validate_foundation  # noqa: E402


class FoundationValidatorTests(unittest.TestCase):
    def read(self, name: str) -> str:
        return (FIXTURE_DIR / name).read_text(encoding="utf-8")

    def test_valid_foundation_brief(self) -> None:
        errors = validate_foundation.validate_brief(
            self.read("valid-foundation-brief.md"), FIXTURE_DIR
        )
        self.assertEqual(errors, [])

    def test_valid_adr(self) -> None:
        errors = validate_foundation.validate_adr(self.read("valid-adr.md"), FIXTURE_DIR)
        self.assertEqual(errors, [])

    def test_adr_accepts_an_explicit_none_evidence_section(self) -> None:
        text = self.read("valid-adr.md")
        start = text.index("## Evidence\n") + len("## Evidence\n")
        end = text.index("## Consequences\n", start)
        text = text[:start] + "None — no external evidence was needed.\n\n" + text[end:]
        self.assertEqual(validate_foundation.validate_adr(text, FIXTURE_DIR), [])

    def test_invalid_brief_reports_structural_failures(self) -> None:
        errors = validate_foundation.validate_brief(
            self.read("invalid-foundation-brief.md"), FIXTURE_DIR
        )
        self.assertTrue(any("unsupported Brief status" in error for error in errors))
        self.assertTrue(any("missing required section" in error for error in errors))
        self.assertTrue(any("Foundation Blueprint" in error for error in errors))

    def test_selected_candidate_must_exist(self) -> None:
        text = self.read("valid-foundation-brief.md").replace(
            "Selected candidate: C0", "Selected candidate: C9"
        )
        errors = validate_foundation.validate_brief(text, FIXTURE_DIR)
        self.assertTrue(any("not present in Candidates" in error for error in errors))

    def test_gate_rows_must_be_unique_and_ordered(self) -> None:
        text = self.read("valid-foundation-brief.md").replace(
            "| G4 Handoff |", "| G0 Handoff |"
        )
        errors = validate_foundation.validate_brief(text, FIXTURE_DIR)
        self.assertTrue(any("exactly one G0" in error for error in errors))

    def test_state_annotations_are_allowed_after_enum(self) -> None:
        text = self.read("valid-foundation-brief.md").replace(
            "| inferred |\n", "| inferred; owner will validate |\n", 1
        )
        self.assertNotIn(
            "unsupported table state/status",
            "\n".join(validate_foundation.validate_brief(text, FIXTURE_DIR)),
        )

    def test_none_reason_must_be_the_whole_optional_section(self) -> None:
        text = self.read("valid-foundation-brief.md").replace(
            "| E1 | The product brief requires transactional review decisions. | supplied product brief | not stated | 2026-08-30 | confirmed | review module |",
            "None — no decision-changing evidence.\nAn unowned claim remains.",
        )
        errors = validate_foundation.validate_brief(text, FIXTURE_DIR)
        self.assertTrue(any("Evidence must contain a data row" in error for error in errors))

    def test_bare_relative_links_are_checked(self) -> None:
        text = self.read("valid-foundation-brief.md").replace(
            "## Objective\n", "## Objective\nSee [missing record](missing-record.md).\n", 1
        )
        errors = validate_foundation.validate_brief(text, FIXTURE_DIR)
        self.assertTrue(any("missing local link target" in error for error in errors))

    def test_placeholder_values_are_rejected(self) -> None:
        text = self.read("valid-foundation-brief.md").replace(
            "Design a foundation for a document-collaboration product",
            "Design a foundation for <placeholder>",
            1,
        )
        errors = validate_foundation.validate_brief(text, FIXTURE_DIR)
        self.assertTrue(any("unresolved placeholder" in error for error in errors))

    def test_invalid_adr_reports_state_and_decision_failures(self) -> None:
        errors = validate_foundation.validate_adr(self.read("invalid-adr.md"), FIXTURE_DIR)
        self.assertTrue(any("unsupported ADR status" in error for error in errors))
        self.assertTrue(any("Confidence" in error for error in errors))
        self.assertTrue(any("Revisit Trigger" in error for error in errors))

    def test_auto_detection(self) -> None:
        brief = FIXTURE_DIR / "valid-foundation-brief.md"
        adr = FIXTURE_DIR / "valid-adr.md"
        self.assertEqual(
            validate_foundation.detect_kind(brief, self.read(brief.name)), "brief"
        )
        self.assertEqual(validate_foundation.detect_kind(adr, self.read(adr.name)), "adr")

    def test_cli_validates_a_directory(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "validate_foundation.py"),
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
