import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/design-ui-from-patterns"

def run(script, *args):
    return subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)

class PortableSkillTests(unittest.TestCase):
    def test_exports_have_all_patterns_and_resolvable_internal_links(self):
        for flag in ([], ["--include-source"]):
            with tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "portable.md"
                result = run(SKILL / "scripts/export_portable.py", "--output", target, *flag)
                self.assertEqual(result.returncode, 0, result.stderr)
                text = target.read_text()
                ids = set(re.findall(r'<a id="([^"]+)"></a>', text))
                links = re.findall(r"\]\(#([^)]+)\)", text)
                self.assertTrue(links)
                self.assertFalse(set(links) - ids, set(links) - ids)
                self.assertEqual(len(re.findall(r"^## P-[VIA]\d{2}$", text, re.M)), 24)
                self.assertIn("E-PERSONA", text)
                self.assertIn("E-WHEEL-PROPOSAL", text)
                self.assertEqual("~~~text" in text, bool(flag))

    def test_check_mode_detects_stale_export(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "portable.md"
            script = SKILL / "scripts/export_portable.py"
            self.assertEqual(run(script, "--output", target).returncode, 0)
            self.assertEqual(run(script, "--output", target, "--check").returncode, 0)
            target.write_text(target.read_text() + "stale change\n")
            self.assertNotEqual(run(script, "--output", target, "--check").returncode, 0)

    def test_validation_detects_a_missing_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "design-ui-from-patterns"
            shutil.copytree(SKILL, package)
            (package / "references/interaction.md").unlink()
            self.assertNotEqual(run(package / "scripts/validate_package.py").returncode, 0)

    def test_validation_detects_unlogged_source_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "design-ui-from-patterns"
            shutil.copytree(SKILL, package)
            path = package / "references/source-transcript.txt"
            lines = path.read_text().splitlines()
            lines[0] += " 未記録の変更"
            path.write_text("\n".join(lines) + "\n")
            result = run(package / "scripts/validate_package.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unlogged correction", result.stderr)

    def test_catalog_and_checked_in_exports_are_current(self):
        self.assertEqual(run(ROOT / "scripts/build_skill_catalog.py", "--check").returncode, 0)
        for name, flags in [
            ("design-ui-from-patterns.md", []),
            ("design-ui-from-patterns-with-source.md", ["--include-source"]),
        ]:
            result = run(SKILL / "scripts/export_portable.py", "--output", ROOT / "dist" / name, "--check", *flags)
            self.assertEqual(result.returncode, 0, result.stderr)

if __name__ == "__main__":
    unittest.main()
