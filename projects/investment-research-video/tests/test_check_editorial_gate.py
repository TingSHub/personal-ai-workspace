import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_editorial_gate.py"
WORKFLOW = Path(__file__).parents[1] / "workflows" / "investagent-podcast-video-by-hyperframes" / "workflow.md"
GLOBAL_CONTRACT = WORKFLOW.parent / "references" / "global-contract.md"


def write_run(root: Path, approved: bool) -> None:
    editorial = root / "editorial"
    editorial.mkdir()
    candidates = []
    for index in range(3):
        candidates.append({
            "topic_id": f"TOPIC-{index + 1}",
            "title": f"候选 {index + 1}",
            "main_question": f"问题 {index + 1}",
            "audience_value": f"收益 {index + 1}",
            "opening_candidate": f"事实反差 {index + 1}？",
            "evidence_ids": [f"E{index + 1}"],
            "expansion_path": ["机制", "验证"],
            "max_risk": "证据不足",
            "content_angle": "company_led",
        })
    (editorial / "topic-options.json").write_text(json.dumps({"candidates": candidates}), encoding="utf-8")
    selected = "TOPIC-1" if approved else ""
    status = "approved" if approved else "pending"
    (editorial / "topic-approval.md").write_text(
        f"status: {status}\ntopic_id: {selected}\napproved_at: 2026-08-26T12:00:00+08:00\n",
        encoding="utf-8",
    )
    if approved:
        for filename in ("director-treatment.md", "opening-selection.json", "scene-intent.json", "director-execution.md"):
            (editorial / filename).write_text("approved treatment", encoding="utf-8")
        (editorial / "topic-order.json").write_text(json.dumps({"topics": [
            {"topic_id": "TOPIC-1", "audience_payoff": "收益 1", "primary_mechanism": "机制 1"},
            {"topic_id": "TOPIC-2", "audience_payoff": "收益 2", "primary_mechanism": "机制 2"},
        ]}), encoding="utf-8")


class EditorialGateTest(unittest.TestCase):
    def test_data_source_fallback_contract_is_documented(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        contract = GLOBAL_CONTRACT.read_text(encoding="utf-8")
        for text in (workflow, contract):
            self.assertIn("AkShare", text)
            self.assertIn("BaoStock", text)
            self.assertIn("data-source-ledger.json", text)
        self.assertIn("tushare-connector` | skill | conditional", workflow)
        self.assertIn("Tushare → AkShare → BaoStock", workflow)

    def run_gate(self, root: Path, require_approved: bool) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(SCRIPT), "--run-root", str(root)]
        if require_approved:
            command.append("--require-approved")
        return subprocess.run(command, text=True, capture_output=True, check=False)

    def test_pending_blocks_downstream(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_run(root, approved=False)
            result = self.run_gate(root, True)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("must be approved", result.stdout)

    def test_approved_treatment_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_run(root, approved=True)
            result = self.run_gate(root, True)
            self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
