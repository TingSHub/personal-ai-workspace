import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'check_podcast_dialogue.py'


class DialogueGateTest(unittest.TestCase):
    def run_gate(self, valuation=None, text='我们偏多的是甲公司的技术优势。', entities=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            episode = {'turns': [
                {'turn_id': 'COLD_OPEN-01', 'topic_id': 'COLD_OPEN', 'text': text},
                {'turn_id': 'INTRO-01', 'topic_id': 'INTRO', 'text': '今天讲清楚原因。'},
            ], 'valuation_context': valuation or {}, 'comparison_entities': entities or []}
            (root / 'episode.json').write_text(json.dumps(episode), encoding='utf-8')
            (root / 'receipt.md').write_text('human-understanding humanizer-zh', encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), '--episode', str(root / 'episode.json'),
                '--phase2-execution', str(root / 'receipt.md'), '--feedback-constraints', str(root / 'receipt.md')],
                capture_output=True, text=True)
            return result.returncode, json.loads(result.stdout)

    def test_thesis_opening_without_question_passes(self):
        self.assertEqual(self.run_gate()[0], 0)

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
