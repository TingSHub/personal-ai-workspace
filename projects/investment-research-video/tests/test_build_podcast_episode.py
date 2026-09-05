import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_podcast_episode.py"
OPENING_SCRIPT = Path(__file__).parents[1] / "scripts" / "build_podcast_opening_test.py"


class BuildPodcastEpisodeTest(unittest.TestCase):
    def test_industry_subject_needs_no_company_fields_or_intro(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = {
                "episode": {
                    "episode_id": "industry-1", "subject_type": "industry",
                    "subject_id": "robotics", "subject_name": "人形机器人",
                    "research_date": "2026-09-06", "show_name": "账本两面",
                    "role_map": {"zhiwei": "host", "shenyan": "analyst"},
                    "speakers": {"zhiwei": {}, "shenyan": {}},
                },
                "opening": {"mode": "thesis", "cold_open": [{
                    "speaker": "zhiwei", "text": "决定机器人商业化速度的，是供应链里最慢的那一环。",
                    "interaction_type": "hook", "evidence_ids": ["E1"],
                }]},
                "growth_contract": {
                    "click_reason": "机器人热潮里，真正稀缺的环节可能不是整机。",
                    "watch_promise": "看懂商业化速度由哪一环决定。",
                    "interaction_value": "讨论最可能率先兑现收入的环节。",
                    "follow_reason": "持续跟踪瓶颈从技术验证走向量产的变化。",
                },
                "editorial_thesis": "执行器的稳定量产能力比整机发布数量更可能决定近期商业化速度。",
                "thesis_contract": {
                    "mechanism": "一致性和成本约束整机放量",
                    "time_horizon": "未来两到三年",
                    "affected_segment": "执行器与精密传动供应链",
                    "strongest_counterargument": "整机厂自研可能降低外部供应商价值",
                    "invalidation_condition": "关键执行器实现低成本规模化且不再影响交付",
                    "evidence_ids": ["E1"],
                },
                "topics": [{
                    "topic_id": "T01", "title": "瓶颈", "claim": "执行器仍是约束",
                    "metrics": [], "chart": {"evidence_ids": ["E1"]},
                    "turns": [{"speaker": "shenyan", "text": "先看执行器。", "evidence_ids": ["E1"]}],
                }],
                "outro": [{
                    "speaker": "zhiwei",
                    "text": "所以我们当前更看重执行器的一致性和降本速度；如果整机厂自研快速成熟，这个判断就要重做。",
                    "evidence_ids": ["E1"],
                }],
            }
            source = root / "episode-input.json"
            source.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(SCRIPT), "--input", str(source), "--run-root", str(root),
            ], text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            episode = json.loads((root / "podcast/script/episode.json").read_text(encoding="utf-8"))
            self.assertEqual(episode["subject_name"], "人形机器人")
            self.assertNotIn("INTRO", {turn["topic_id"] for turn in episode["turns"]})
            self.assertEqual(episode["outro_summary"], [])
            canary = root / "opening.json"
            opening_result = subprocess.run([
                sys.executable, str(OPENING_SCRIPT),
                "--episode", str(root / "podcast/script/episode.json"), "--out", str(canary),
            ], text=True, capture_output=True, check=False)
            self.assertEqual(opening_result.returncode, 0, opening_result.stderr)
            self.assertEqual(len(json.loads(canary.read_text(encoding="utf-8"))["turns"]), 1)

    def test_missing_growth_and_thesis_contracts_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "episode-input.json"
            source.write_text(json.dumps({
                "episode": {
                    "episode_id": "x", "subject_type": "event", "subject_id": "x",
                    "subject_name": "事件", "research_date": "2026-09-06", "show_name": "账本两面",
                    "role_map": {}, "speakers": {},
                },
                "opening": {"cold_open": [{"speaker": "zhiwei", "text": "先说结论。", "interaction_type": "hook"}]},
                "topics": [{"topic_id": "T01", "title": "原因", "claim": "有变化", "metrics": [], "chart": {}, "turns": [{"speaker": "shenyan", "text": "原因在这里。"}]}],
                "outro": [{"speaker": "zhiwei", "text": "持续关注。"}],
            }, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(SCRIPT), "--input", str(source), "--run-root", str(root),
            ], text=True, capture_output=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("editorial_thesis required", result.stderr)


if __name__ == "__main__":
    unittest.main()
