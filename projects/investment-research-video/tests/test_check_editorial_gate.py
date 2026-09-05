import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_editorial_gate.py"


def card(question: str, status: str = "approved") -> dict:
    return {
        "topic_id": "TOPIC-7",
        "title": "技术实力验证",
        "subject_type": "company",
        "audience_question": question,
        "click_reason": "市场把发布会当成商业化，但客户采用才是门槛。",
        "content_promise": "看懂技术优势如何变成客户采用。",
        "interaction_value": "讨论哪项采用证据最关键。",
        "follow_reason": "持续跟踪产品从验证到收入的变化。",
        "core_tension": "技术领先不等于规模收入。",
        "evidence": [{"source": "official", "id": "E7"}],
        "status": status,
    }


def write_inputs(root: Path, question: str, *, status: str = "approved", decision: str = "accepted", treatment: bool = False) -> tuple[Path, Path]:
    upstream = root / "topic-forward.json"
    upstream.write_text(json.dumps({
        "status": status,
        "approved_topic_id": "TOPIC-7" if status == "approved" else "",
        "approved_at": "2026-09-05T12:00:00+08:00" if status == "approved" else "",
        "cards": [card(question, status)],
    }, ensure_ascii=False), encoding="utf-8")
    brief = root / "research-brief.md"
    brief.write_text(
        f"# Topic Research Brief: TOPIC-7\n\n## Approved Question\n\n{question}\n\n"
        f"## Current Answer\n\n客户采用是当前更关键的验证。\n\n"
        f"## Scope Decision\n\n{decision}\n",
        encoding="utf-8",
    )
    if treatment:
        editorial = root / "editorial"
        editorial.mkdir()
        for filename in ("director-treatment.md", "opening-selection.json", "scene-intent.json", "director-execution.md"):
            (editorial / filename).write_text("approved treatment", encoding="utf-8")
        (editorial / "topic-order.json").write_text(json.dumps({"topics": [
            {"topic_id": "T01", "audience_payoff": "理解采用门槛", "primary_mechanism": "客户验证"},
            {"topic_id": "T02", "audience_payoff": "理解收入兑现", "primary_mechanism": "规模交付"},
        ]}, ensure_ascii=False), encoding="utf-8")
    return upstream, brief


def run_gate(root: Path, upstream: Path, brief: Path, require_approved: bool = False) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable, str(SCRIPT), "--run-root", str(root),
        "--upstream-topic-card", str(upstream), "--research-brief", str(brief),
    ]
    if require_approved:
        command.append("--require-approved")
    return subprocess.run(command, text=True, capture_output=True, check=False)


class EditorialGateTest(unittest.TestCase):
    def test_upstream_approval_is_reused_without_local_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upstream, brief = write_inputs(root, "这项技术优势能否转成客户采用？")
            result = run_gate(root, upstream, brief)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertFalse((root / "editorial/topic-approval.md").exists())

    def test_pending_topic_blocks_production(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upstream, brief = write_inputs(root, "这项技术优势能否转成客户采用？", status="pending", treatment=True)
            result = run_gate(root, upstream, brief, True)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("must be approved", result.stdout)

    def test_approved_treatment_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upstream, brief = write_inputs(root, "这项技术优势能否转成客户采用？", treatment=True)
            result = run_gate(root, upstream, brief, True)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_changed_research_question_requires_scope_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upstream, brief = write_inputs(root, "原批准问题")
            brief.write_text(
                "# Topic Research Brief: TOPIC-7\n\n## Approved Question\n\n已经改过的问题\n\n"
                "## Scope Decision\n\naccepted\n",
                encoding="utf-8",
            )
            result = run_gate(root, upstream, brief)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("differs from the approved", result.stdout)

    def test_scope_change_blocks_production(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upstream, brief = write_inputs(root, "原批准问题", decision="scope_change_required")
            result = run_gate(root, upstream, brief)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("must be accepted", result.stdout)


if __name__ == "__main__":
    unittest.main()
