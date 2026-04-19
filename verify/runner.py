from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class TestResult:
    id: str
    requirement_ids: list[str]
    passed: bool
    stdout: str
    exit_code: int
    expected_stdout: str
    expected_exit_code: int


def load_manifest(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def run_case(executable: str, case: dict) -> TestResult:
    proc = subprocess.run(
        [executable, *map(str, case["args"])],
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = proc.stdout.strip()
    passed = stdout == case["expected_stdout"] and proc.returncode == case["expected_exit_code"]
    return TestResult(
        id=case["id"],
        requirement_ids=case["requirement_ids"],
        passed=passed,
        stdout=stdout,
        exit_code=proc.returncode,
        expected_stdout=case["expected_stdout"],
        expected_exit_code=case["expected_exit_code"],
    )


def execute(manifest_path: str | Path) -> dict:
    manifest = load_manifest(manifest_path)
    executable = manifest["executable"]
    results = [run_case(executable, case) for case in manifest["tests"]]

    total = len(results)
    passed = sum(1 for result in results if result.passed)
    coverage = {
        req["id"]: [case["id"] for case in manifest["tests"] if req["id"] in case["requirement_ids"]]
        for req in manifest["requirements"]
    }

    return {
        "manifest": manifest,
        "results": [asdict(result) for result in results],
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": round((passed / total) * 100, 1) if total else 0.0,
        },
        "coverage": coverage,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Verification Report",
        "",
        f"- Total tests: {report['summary']['total']}",
        f"- Passed: {report['summary']['passed']}",
        f"- Failed: {report['summary']['failed']}",
        f"- Pass rate: {report['summary']['pass_rate']}%",
        "",
        "## Results",
    ]
    for result in report["results"]:
        lines.append(
            f"- {result['id']}: {'PASS' if result['passed'] else 'FAIL'} "
            f"(stdout={result['stdout']!r}, exit={result['exit_code']})"
        )
    lines.append("")
    lines.append("## Requirement Coverage")
    for req_id, cases in report["coverage"].items():
        lines.append(f"- {req_id}: {', '.join(cases) if cases else 'uncovered'}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", default="reports/latest_report.md")
    args = parser.parse_args()

    report = execute(args.manifest)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
