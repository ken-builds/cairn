from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import inventory_structure as inventory  # noqa: E402


class InventoryStructureTests(unittest.TestCase):
    def write(self, root: Path, relative: str, content: str = "x\n") -> Path:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def row(self, report: dict[str, object], path: str) -> dict[str, object]:
        rows = report["directories"]
        assert isinstance(rows, list)
        for row in rows:
            if row["path"] == path:
                return row
        self.fail(f"directory row not found: {path}")

    def test_small_cohesive_directory_is_retained(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "component/one.part", "one\n")
            self.write(root, "component/two.part", "two\n")
            self.write(root, "component/README.md", "# Component\n")

            report = inventory.inventory(root)
            component = self.row(report, "component")

            self.assertEqual(component["direct_production_files"], 2)
            self.assertEqual(component["disposition"], "retain")
            self.assertEqual(component["readme"], "component/README.md")
            self.assertIn("README.md", component["markers"])

    def test_source_extensions_are_not_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("a.c", "b.go", "c.rs", "d.py", "e.java", "f.rb"):
                self.write(root, f"component/{name}")

            report = inventory.inventory(root)
            component = self.row(report, "component")
            self.assertEqual(component["direct_production_files"], 6)
            self.assertEqual(component["recursive_roles"]["production"], 6)

    def test_roles_are_separated_from_production_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index in range(12):
                self.write(root, f"component/part-{index}.part")
            self.write(root, "component/tests/example.part")
            self.write(root, "component/generated/derived.part")
            self.write(root, "component/vendor/library.part")
            self.write(root, "component/scripts/tool.part")
            self.write(root, "component/agents/instructions.yaml")
            self.write(root, "component/docs/notes.yaml")
            self.write(root, "component/README.md", "# Component\n")

            report = inventory.inventory(root)
            component = self.row(report, "component")

            self.assertEqual(component["direct_production_files"], 12)
            self.assertEqual(component["disposition"], "review")
            self.assertEqual(component["recursive_files"], 19)
            self.assertEqual(component["roles"]["production"], 12)
            self.assertEqual(component["roles"]["documentation"], 1)
            self.assertEqual(component["recursive_roles"]["test"], 1)
            self.assertEqual(component["recursive_roles"]["generated"], 1)
            self.assertEqual(component["recursive_roles"]["vendor"], 1)
            self.assertEqual(component["recursive_roles"]["tooling"], 2)
            self.assertEqual(component["recursive_roles"]["documentation"], 2)

    def test_compare_candidate_band(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index in range(20):
                self.write(root, f"component/part-{index}.part")

            report = inventory.inventory(root)
            component = self.row(report, "component")
            self.assertEqual(component["disposition"], "compare-candidates")

    def test_nested_counts_and_child_fanout_are_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "component/root.part")
            self.write(root, "component/child/one.part")
            self.write(root, "component/child/two.part")
            self.write(root, "component/other/three.part")

            report = inventory.inventory(root)
            component = self.row(report, "component")
            child = self.row(report, "component/child")

            self.assertEqual(component["direct_files"], 1)
            self.assertEqual(component["recursive_files"], 4)
            self.assertEqual(component["child_directories"], 2)
            self.assertEqual(child["direct_production_files"], 2)
            self.assertEqual(child["recursive_files"], 2)

    def test_policy_thresholds_roles_excludes_and_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy_path = root / "policy.json"
            policy_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "thresholds": {
                            "observe_direct_production_files": 1,
                            "review_direct_production_files": 2,
                            "compare_direct_production_files": 3,
                        },
                        "exclude": ["ignored/**"],
                        "role_overrides": {"component/notes.part": "documentation"},
                        "boundary_paths": ["component"],
                    }
                ),
                encoding="utf-8",
            )
            self.write(root, "component/one.part")
            self.write(root, "component/notes.part")
            self.write(root, "ignored/should-not-count.part")

            report = inventory.inventory(root, policy=inventory.load_policy(policy_path))
            component = self.row(report, "component")

            self.assertEqual(component["direct_production_files"], 1)
            self.assertEqual(component["disposition"], "observe")
            self.assertTrue(component["boundary_candidate"])
            self.assertGreaterEqual(report["summary"]["excluded_paths"], 1)

    def test_binary_files_have_no_text_line_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / "component" / "image.part"
            binary.parent.mkdir(parents=True, exist_ok=True)
            binary.write_bytes(b"header\0binary\n")
            self.write(root, "component/source.part", "source\n")

            report = inventory.inventory(root)
            component = self.row(report, "component")
            self.assertEqual(component["direct_production_files"], 2)
            self.assertEqual(component["production_lines"], 1)

    def test_optional_default_excludes_and_line_count_modes_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "target/generated.part", "derived\n")

            default_report = inventory.inventory(root)
            default_target = self.row(default_report, ".")
            self.assertEqual(default_report["summary"]["files_scanned"], 0)
            self.assertEqual(default_target["recursive_files"], 0)

            expanded_report = inventory.inventory(
                root,
                use_default_excludes=False,
                count_lines=False,
            )
            expanded_target = self.row(expanded_report, "target")
            self.assertEqual(expanded_report["summary"]["files_scanned"], 1)
            self.assertEqual(expanded_report["summary"]["line_count_mode"], "skipped")
            self.assertEqual(expanded_target["recursive_roles"]["build_output"], 1)
            self.assertEqual(expanded_target["production_lines"], 0)

    def test_cli_json_output_is_machine_readable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "component/one.part")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "inventory_structure.py"),
                    str(root),
                    "--format",
                    "json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["schema_version"], 1)
            self.assertEqual(report["summary"]["files_scanned"], 1)

    def test_tracked_mode_uses_git_paths_and_respects_ignore_rules(self) -> None:
        if shutil.which("git") is None:
            self.skipTest("git is unavailable")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, ".gitignore", "ignored/\n")
            self.write(root, "component/tracked.part")
            self.write(root, "component/untracked.part")
            self.write(root, "ignored/ignored.part")
            subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
            subprocess.run(
                ["git", "-C", str(root), "add", ".gitignore", "component/tracked.part"],
                check=True,
            )

            report = inventory.inventory(root, tracked=True)
            self.assertEqual(report["path_source"], "git")
            self.assertEqual(report["summary"]["files_scanned"], 3)
            component = self.row(report, "component")
            self.assertEqual(component["direct_production_files"], 2)

    def test_invalid_policy_returns_usage_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy_path = root / "policy.json"
            policy_path.write_text(
                '{"thresholds": {"review_direct_production_files": 4, '
                '"compare_direct_production_files": 2}}',
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "inventory_structure.py"),
                    str(root),
                    "--policy",
                    str(policy_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("thresholds must be ordered", result.stderr)


if __name__ == "__main__":
    unittest.main()
