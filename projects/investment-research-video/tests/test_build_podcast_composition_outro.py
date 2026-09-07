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


if __name__ == '__main__':
    unittest.main()
