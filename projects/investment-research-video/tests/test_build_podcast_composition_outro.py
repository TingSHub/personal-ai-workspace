import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'build_podcast_composition.py'


def load_module(module_name='build_podcast_composition'):
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OutroTitleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_fallback_is_current_conclusion(self):
        self.assertEqual(self.module.resolve_outro_title({}, {}), '本期结论')

    def test_episode_topic_title_wins_when_no_visual(self):
        self.assertEqual(
            self.module.resolve_outro_title({}, {'title': '猪周期能不能反转'}),
            '猪周期能不能反转')

    def test_visual_plan_title_wins(self):
        self.assertEqual(
            self.module.resolve_outro_title({'title': '本轮结论：产能还在调减'}, {'title': '旧标题'}),
            '本轮结论：产能还在调减')

    def test_no_production_meta_inside_composition_sources(self):
        source = SCRIPT.read_text(encoding='utf-8')
        for marker in ('双人总结', '主持人总结', '双方总结', '分析师回答'):
            self.assertNotIn(marker, source, f'{marker} leaked into composition writer')

    def test_range_band_renders_low_and_high_on_one_shared_scale(self):
        markup = self.module.chart_markup([{
            'chart_id': 'lag-range', 'type': 'range-band', 'claim': '滞后区间',
            'data': [
                {'label': '产能到价格', 'low': 3, 'high': 6},
                {'label': '事件到主升浪', 'low': 9, 'high': 12},
            ],
        }], 'editorial-paper')
        self.assertIn('3–6', markup)
        self.assertIn('9–12', markup)
        self.assertIn('chart-row-lag-range-1', markup)
        self.assertNotIn('width:100%', markup)

    def test_dumbbell_requires_two_endpoints(self):
        with self.assertRaises(SystemExit):
            self.module.chart_markup([{
                'chart_id': 'comparison', 'type': 'dumbbell',
                'data': [{'label': '公司 A', 'value': 12}],
            }])

    def test_range_band_rejects_reversed_bounds(self):
        with self.assertRaises(SystemExit):
            self.module.chart_markup([{
                'chart_id': 'bad-range', 'type': 'range-band',
                'data': [{'label': '错误区间', 'low': 12, 'high': 6}],
            }])

    def test_empty_chart_fails_instead_of_rendering_blank_zone(self):
        with self.assertRaises(SystemExit):
            self.module.chart_markup([{
                'chart_id': 'empty', 'type': 'horizontal-bar', 'data': [],
            }])

    def test_scene_manifest_drives_state_at_real_global_time(self):
        script = self.module.motion_script([], 10, {'scenes': [{
            'states': [{
                'state_id': 'S1', 'turn_id': 'T1', 'at': 4.25,
                'action': 'reveal', 'target_ids': ['chart-lag-range'],
            }],
        }]})
        self.assertIn('chart-lag-range', script)
        self.assertIn(',4.25)', script)

    def test_scene_actions_have_distinct_motion_grammar(self):
        script = self.module.motion_script([], 10, {'scenes': [{
            'start': 0, 'end': 10, 'topic_id': 'T1',
            'states': [
                {'at': 1, 'action': 'establish', 'target_ids': ['a']},
                {'at': 2, 'action': 'compare', 'target_ids': ['b', 'c']},
                {'at': 3, 'action': 'challenge', 'target_ids': ['d']},
                {'at': 4, 'action': 'resolve', 'target_ids': ['e']},
            ],
            'transition_out': {'type': 'push', 'duration': .4},
        }]})
        for action in ('establish', 'compare', 'challenge', 'resolve'):
            self.assertIn(f"action==='{action}'", script)
        self.assertIn("type==='push'", script)

    def test_multiline_uses_one_shared_vertical_scale(self):
        markup = self.module.chart_markup([{
            'chart_id': 'shared', 'type': 'multiline',
            'data': [
                {'label': '低位', 'values': [10, 20]},
                {'label': '高位', 'values': [100, 200]},
            ],
        }])
        self.assertIn('60.0,88.0 690.0,84.9', markup)
        self.assertIn('60.0,60.5 690.0,30.0', markup)

    def test_step_line_emits_horizontal_then_vertical_points(self):
        markup = self.module.chart_markup([{
            'chart_id': 'step', 'type': 'step-line',
            'data': [{'values': [10, 20, 15]}],
        }])
        points = markup.split('points="', 1)[1].split('"', 1)[0].split()
        self.assertEqual(len(points), 5)

    def test_flow_nodes_and_connectors_are_addressable(self):
        markup = self.module.chart_markup([{
            'chart_id': 'chain', 'type': 'flow',
            'data': [{'label': '供给'}, {'label': '价格'}, {'label': '利润'}],
        }])
        self.assertIn('chart-node-chain-0', markup)
        self.assertIn('chart-connector-chain-0', markup)


if __name__ == '__main__':
    unittest.main()
