import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'check_podcast_dialogue.py'


class DialogueGateTest(unittest.TestCase):
    def run_gate(self, valuation=None, text='我们偏多的是甲公司的技术优势。', entities=None, include_intro=True,
                 speaker=None, delivery=None, display_text=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first_turn = {'turn_id': 'COLD_OPEN-01', 'topic_id': 'COLD_OPEN', 'text': text}
            if speaker:
                first_turn['speaker'] = speaker
            if delivery:
                first_turn['delivery'] = delivery
            if display_text is not None:
                first_turn['display_text'] = display_text
            turns = [first_turn]
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
            (root / 'receipt.md').write_text('finance-content-engineering', encoding='utf-8')
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

    def test_male_monosyllable_backchannel_fails(self):
        code, report = self.run_gate()
        self.assertEqual(code, 0)
        # Exercise the production speaker-specific rule with a minimal edit.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            episode = {
                'turns': [
                    {'turn_id': 'COLD_OPEN-01', 'topic_id': 'COLD_OPEN', 'speaker': 'shenyan', 'text': '对。关键在利润。'},
                    {'turn_id': 'OUTRO-01', 'topic_id': 'OUTRO', 'speaker': 'zhiwei', 'text': '当前判断成立。'},
                ],
                'editorial_thesis': '结论',
                'growth_contract': {field: 'x' for field in ('click_reason', 'watch_promise', 'interaction_value', 'follow_reason')},
                'thesis_contract': {field: ['E1'] if field == 'evidence_ids' else 'x' for field in ('mechanism', 'time_horizon', 'affected_segment', 'strongest_counterargument', 'invalidation_condition', 'evidence_ids')},
            }
            (root / 'episode.json').write_text(json.dumps(episode, ensure_ascii=False), encoding='utf-8')
            (root / 'receipt.md').write_text('finance-content-engineering', encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), '--episode', str(root / 'episode.json'), '--phase2-execution', str(root / 'receipt.md'), '--feedback-constraints', str(root / 'receipt.md')], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('monosyllable backchannel', result.stdout)

    def test_numeric_turn_requires_display_text(self):
        code, report = self.run_gate(text='能繁母猪同比降了百分之六点五。')
        self.assertEqual(code, 1)
        self.assertTrue(any('missing display_text' in f for f in report['findings']))

    def test_numeric_turn_with_matching_display_text_passes(self):
        code, _ = self.run_gate(
            text='能繁母猪同比降了百分之六点五。',
            display_text='能繁母猪同比降了6.5%。')
        self.assertEqual(code, 0)

    def test_display_text_percent_mismatch_fails(self):
        code, report = self.run_gate(
            text='能繁母猪同比降了百分之六点五。',
            display_text='能繁母猪同比降了7.5%。')
        self.assertEqual(code, 1)
        self.assertTrue(any('differs from spoken numbers' in f for f in report['findings']))

    def test_question_without_particle_fails(self):
        code, report = self.run_gate(
            text='价格是回来了，这是不是反转了？',
            speaker='zhiwei', delivery='rising_question')
        self.assertEqual(code, 1)
        self.assertTrue(any('final particle' in f for f in report['findings']))

    def test_question_with_particle_passes(self):
        code, _ = self.run_gate(
            text='价格是回来了，这是不是已经反转了呢？',
            speaker='zhiwei', delivery='rising_question')
        self.assertEqual(code, 0)

    def test_analyst_question_requires_rising_delivery_too(self):
        code, report = self.run_gate(text='等等，那这个口径是不是也该重新核一遍？', speaker='shenyan')
        self.assertEqual(code, 1)
        self.assertTrue(any('rising_question' in f for f in report['findings']))

    def test_host_question_requires_rising_delivery(self):
        self.assertEqual(self.run_gate(text='这件事该怎么看？', speaker='zhiwei')[0], 1)
        self.assertEqual(self.run_gate(text='这件事该怎么看？', speaker='zhiwei', delivery='rising_question')[0], 0)


if __name__ == '__main__':
    unittest.main()
