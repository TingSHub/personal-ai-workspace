from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PYTHON = sys.executable


def run_script(name: str, *arguments: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONUTF8"] = "1"
    completed = subprocess.run(
        [PYTHON, str(SCRIPTS / name), *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=environment,
    )
    if completed.returncode != expected:
        raise AssertionError(
            f"{name} returned {completed.returncode}, expected {expected}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


class WorkflowTests(unittest.TestCase):
    def create_skill(self, parent: Path, name: str = "sample-skill") -> Path:
        skill = parent / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            "description: Convert images and media files with a safe, reviewable workflow.\n"
            "---\n\n"
            "# Sample\n\nInspect the input, plan the conversion, and ask before writing output.\n",
            encoding="utf-8",
        )
        (skill / "LICENSE").write_text(
            "MIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy.\n",
            encoding="utf-8",
        )
        return skill

    def test_safe_skill_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.create_skill(Path(directory))
            completed = run_script("inspect_skill.py", str(skill))
            report = json.loads(completed.stdout)
            self.assertTrue(report["spec_valid"])
            self.assertTrue(report["install_allowed"])
            self.assertEqual(report["license"]["id"], "MIT")

    def test_dangerous_skill_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.create_skill(Path(directory), "dangerous-skill")
            scripts = skill / "scripts"
            scripts.mkdir()
            (scripts / "run.py").write_text("exec(input('command: '))\n", encoding="utf-8")
            completed = run_script("inspect_skill.py", str(skill), expected=2)
            report = json.loads(completed.stdout)
            self.assertFalse(report["install_allowed"])
            self.assertIn(report["risk_level"], {"high", "critical"})

    def test_local_search_rank_and_bilingual_cards(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "skills"
            skill = self.create_skill(root, "media-converter")
            candidates = base / "candidates.json"
            ranked = base / "ranked.json"
            audit = json.loads(run_script("inspect_skill.py", str(skill)).stdout)

            run_script(
                "search_skills.py", "media convert", "--local-root", str(root),
                "--no-skills-sh", "--no-github", "--output", str(candidates),
            )
            payload = json.loads(candidates.read_text(encoding="utf-8"))
            target = next(item for item in payload["candidates"] if item["name"] == "media-converter")
            target["audit"] = audit
            target["has_tests"] = True
            payload["candidates"] = [target]
            candidates.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            run_script("rank_skills.py", "--query", "media convert", "--input", str(candidates), "--output", str(ranked))
            ranked_payload = json.loads(ranked.read_text(encoding="utf-8"))
            self.assertEqual(ranked_payload["candidates"][0]["recommendation_status"], "eligible")

            zh = run_script("render_cards.py", "--input", str(ranked), "--lang", "zh").stdout
            en = run_script("render_cards.py", "--input", str(ranked), "--lang", "en").stdout
            self.assertIn("匹配度", zh)
            self.assertIn("Security", en)


if __name__ == "__main__":
    unittest.main()
