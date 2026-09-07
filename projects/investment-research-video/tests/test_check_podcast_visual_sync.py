import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_podcast_visual_sync.py"


class VisualSyncGateTest(unittest.TestCase):
    def run_gate(self, beats):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "episode.json").write_text(json.dumps({"turns": [
                {"turn_id": "T01-01", "topic_id": "T01", "text": "先看起点。"},
                {"turn_id": "T01-02", "topic_id": "T01", "text": "再看终点。"},
            ]}), encoding="utf-8")
            (root / "charts.json").write_text(json.dumps({"charts": [{
                "chart_id": "trend", "topic_id": "T01", "type": "line", "narration_beats": beats,
            }]}), encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), "--episode", str(root / "episode.json"), "--charts", str(root / "charts.json")], capture_output=True, text=True)

    def test_static_multi_step_chart_fails(self):
        self.assertEqual(self.run_gate([]).returncode, 1)

    def test_turn_bound_reveals_pass(self):
        result = self.run_gate([
            {"turn_id": "T01-01", "reveal": ["point-1"]},
            {"turn_id": "T01-02", "reveal": ["point-2"]},
        ])
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
