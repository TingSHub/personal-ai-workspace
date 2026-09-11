import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_podcast_visual_sync.py"


class VisualSyncGateTest(unittest.TestCase):
    def run_manifest_gate(self, scene, *, turns=None, segments=None, charts=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            turns = turns or [
                {"turn_id": "T01-01", "topic_id": "T01", "text": "先看起点。"},
            ]
            segments = segments if segments is not None else [
                {"turn_id": "T01-01", "start": 1.0, "end": 3.0},
            ]
            (root / "episode.json").write_text(json.dumps({"turns": turns}), encoding="utf-8")
            (root / "segments.json").write_text(json.dumps({"segments": segments}), encoding="utf-8")
            scene_payload = [] if scene is None else ([scene] if isinstance(scene, dict) else scene)
            scene_payload = [{
                "purpose": "explain",
                "visual_pattern": f"pattern-{index}",
                "viewer_question": "观众需要理解什么？",
                "cognitive_change": "看清数据关系",
                "continuity_anchor": "none",
                **item,
            } for index, item in enumerate(scene_payload)]
            (root / "scene-manifest.json").write_text(json.dumps({
                "version": "v3",
                "visual_system": {"design_dials": {
                    "design_variance": 6, "motion_intensity": 6, "visual_density": 5,
                }},
                "scenes": scene_payload,
            }), encoding="utf-8")
            command = [
                sys.executable, str(SCRIPT),
                "--episode", str(root / "episode.json"),
                "--scene-manifest", str(root / "scene-manifest.json"),
                "--segments", str(root / "segments.json"),
            ]
            if charts is not None:
                (root / "charts.json").write_text(json.dumps({"charts": charts}), encoding="utf-8")
                command.extend(["--charts", str(root / "charts.json")])
            return subprocess.run(command, capture_output=True, text=True)

    def test_semantic_scene_state_passes(self):
        result = self.run_manifest_gate({
            "scene_id": "T01", "topic_id": "T01", "start": 1.0, "end": 3.0,
            "states": [{
                "state_id": "T01-S1", "turn_id": "T01-01", "at": 1.2,
                "action": "reveal", "target_ids": ["point-1"], "hold_until": 2.8,
            }],
            "transition_out": {"type": "crossfade", "duration": 0.5},
            "audio_cues": [],
        })
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_state_outside_real_turn_fails(self):
        result = self.run_manifest_gate({
            "scene_id": "T01", "topic_id": "T01", "start": 1.0, "end": 5.0,
            "states": [{
                "state_id": "T01-S1", "turn_id": "T01-01", "at": 4.0,
                "action": "reveal", "target_ids": ["point-1"], "hold_until": 4.5,
            }],
            "transition_out": {"type": "cut", "duration": 0},
        })
        self.assertEqual(result.returncode, 1)
        self.assertIn("outside narration turn", result.stdout)

    def test_empty_manifest_fails(self):
        result = self.run_manifest_gate(None)
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires at least one scene", result.stdout)

    def test_manifest_must_cover_every_episode_topic(self):
        result = self.run_manifest_gate({
            "scene_id": "T01", "topic_id": "T01", "start": 1.0, "end": 3.0,
            "states": [{
                "state_id": "T01-S1", "turn_id": "T01-01", "at": 1.2,
                "action": "reveal", "target_ids": ["point-1"], "hold_until": 2.8,
            }],
            "transition_out": {"type": "cut", "duration": 0},
        }, turns=[
            {"turn_id": "T01-01", "topic_id": "T01"},
            {"turn_id": "T02-01", "topic_id": "T02"},
        ])
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not cover episode topic: T02", result.stdout)

    def test_manifest_turn_must_exist_on_real_audio_timeline(self):
        result = self.run_manifest_gate({
            "scene_id": "T01", "topic_id": "T01", "start": 1.0, "end": 3.0,
            "states": [{
                "state_id": "T01-S1", "turn_id": "T01-01", "at": 1.2,
                "action": "reveal", "target_ids": ["point-1"], "hold_until": 2.8,
            }],
            "transition_out": {"type": "cut", "duration": 0},
        }, segments=[])
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing from segments", result.stdout)

    def test_three_states_need_more_than_one_motion_action(self):
        result = self.run_manifest_gate({
            "scene_id": "T01", "topic_id": "T01", "start": 1.0, "end": 3.0,
            "states": [
                {"state_id": f"T01-S{index}", "turn_id": "T01-01", "at": 1.0 + index * .2,
                 "action": "reveal", "target_ids": [f"point-{index}"], "hold_until": 2.8}
                for index in range(1, 4)
            ],
            "transition_out": {"type": "cut", "duration": 0},
        })
        self.assertEqual(result.returncode, 1)
        self.assertIn("repeats one motion action", result.stdout)

    def test_multistep_chart_uses_scene_states_as_production_contract(self):
        result = self.run_manifest_gate({
            "scene_id": "T01", "topic_id": "T01", "start": 1.0, "end": 3.0,
            "states": [
                {"state_id": "T01-S1", "turn_id": "T01-01", "at": 1.2,
                 "action": "establish", "target_ids": ["chart-trend"], "hold_until": 1.8},
                {"state_id": "T01-S2", "turn_id": "T01-01", "at": 2.0,
                 "action": "reveal", "target_ids": ["chart-series-trend-0"], "hold_until": 2.8},
            ],
            "transition_out": {"type": "cut", "duration": 0},
        }, charts=[{"chart_id": "trend", "topic_id": "T01", "type": "line"}])
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_state_cannot_animate_framework_owned_clip(self):
        result = self.run_manifest_gate({
            "scene_id": "T01", "topic_id": "T01", "start": 1.0, "end": 3.0,
            "states": [{
                "state_id": "T01-S1", "turn_id": "T01-01", "at": 1.2,
                "action": "reveal", "target_ids": ["chart-stage-T01-0"], "hold_until": 2.8,
            }],
            "transition_out": {"type": "cut", "duration": 0},
        })
        self.assertEqual(result.returncode, 1)
        self.assertIn("framework-owned clip", result.stdout)

if __name__ == "__main__":
    unittest.main()
