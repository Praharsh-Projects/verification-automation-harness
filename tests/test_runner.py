from pathlib import Path
import subprocess
import unittest

from verify.runner import execute, render_markdown


class TestRunner(unittest.TestCase):
    def test_execute_generates_report(self):
        repo_root = Path(__file__).resolve().parents[1]
        (repo_root / "build").mkdir(exist_ok=True)

        subprocess.run(
            ["cc", "-Wall", "-Wextra", "-O2", "src/limit_checker.c", "-o", "build/limit_checker"],
            cwd=repo_root,
            check=True,
        )
        report = execute(repo_root / "data/manifest.yaml")
        self.assertEqual(report["summary"]["total"], 3)
        self.assertEqual(report["summary"]["passed"], 3)
        self.assertIn("SYS-001", report["coverage"])
        md = render_markdown(report)
        self.assertIn("Verification Report", md)
