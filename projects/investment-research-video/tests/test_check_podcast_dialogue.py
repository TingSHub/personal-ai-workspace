import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'check_podcast_dialogue.py'


class DialogueGateTest(unittest.TestCase):
    def run_gate(self, valuation=None, text='我们偏多的是甲公司的技术优势。', entities=None, include_intro=True):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            turns = [{'turn_id': 'COLD_OPEN-01', 'topic_id': 'COLD_OPEN', 'text': text}]
            if include_intro:
                turns.append({'turn_id': 'INTRO-01', 'topic_id': 'INTRO', 'text': '今天讲清楚原因。'})
            turns.append({'turn_id': 'OUTRO-01', 'topic_id': 'OUTRO', 'text': '当前判断成立，条件变化时我们会重做结论。'})
            episode = {
                'turns': turns,
                'valuation_context': valuation or {},
                'comparison_entities': entities or [],
                'editorial_thesis': '技术优势能否转成收入，取决于交付能力。',
                'growth_contract': {
                    'click_reason': '同类公司兑现能力不同',
                    'watch_promise': '看懂差异来自哪里',
                    'interaction_value': '讨论哪项证据最关键',
                    'follow_reason': '持续跟踪兑现进度',
                },
                'thesis_contract': {
                    'mechanism': '交付决定收入确认',
                    'time_horizon': '未来一年',
                    'affected_segment': '技术供应商',
                    'strongest_counterargument': '需求可能不及预期',
                    'invalidation_condition': '交付未形成收入',
                    'evidence_ids': ['E1'],
                },
            }
            (root / 'episode.json').write_text(json.dumps(episode), encoding='utf-8')
            (root / 'receipt.md').write_text('human-understanding humanizer-zh', encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), '--episode', str(root / 'episode.json'),
                '--phase2-execution', str(root / 'receipt.md'), '--feedback-constraints', str(root / 'receipt.md')],
                capture_output=True, text=True)
            return result.returncode, json.loads(result.stdout)

    def test_thesis_opening_without_question_passes(self):
        self.assertEqual(self.run_gate()[0], 0)

    def test_intro_is_optional(self):
        self.assertEqual(self.run_gate(include_intro=False)[0], 0)

    def test_bearish_view_and_sourced_nonbrokerage_valuation_pass(self):
        self.assertEqual(self.run_gate({'enabled': True, 'source_class': 'official', 'source_refs': ['S1']},
            '我们对这份增长预期偏空，当前估值偏贵。')[0], 0)

    def test_unsourced_valuation_fails(self):
        self.assertEqual(self.run_gate({'enabled': True, 'source_class': 'official'})[0], 1)

    def test_brokerage_missing_directory_fails_cleanly(self):
        self.assertEqual(self.run_gate({'enabled': True, 'source_class': 'brokerage'})[0], 1)

    def test_direct_recommendation_still_fails_in_valuation(self):
        self.assertEqual(self.run_gate({'enabled': True, 'source_class': 'official', 'source_refs': ['S1']},
            '建议买入甲公司。')[0], 1)

    def test_direct_recommendation_fails_without_valuation(self):
        self.assertEqual(self.run_gate(text='这只股票可以买入。')[0], 1)

    def test_qualitative_peer_introduction_needs_no_financials(self):
        entities = [{'name': name, 'role': role, 'comparison_axis': '细分产品'}
                    for name, role in [('甲公司', '部件'), ('乙公司', '系统')]]
        self.assertEqual(self.run_gate(text='甲公司擅长部件，乙公司擅长系统交付。', entities=entities)[0], 0)

    def test_unnamed_peer_still_fails(self):
        self.assertEqual(self.run_gate(text='三家公司都有优势。')[0], 1)


if __name__ == '__main__':
    unittest.main()
