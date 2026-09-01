import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / ".claude/skills/research-quality-gate/scripts/validate_research.py"


MASTER = """# 紫光股份 Research Master Document

## 公司投资摘要
紫光股份 2025 年收入为 800亿元，毛利率为 20%。E001
Bull Case：云计算需求改善。
Bear Case：价格竞争加剧。
核心跟踪指标：收入增速、毛利率、经营现金流。

## 行业研究
行业需求来自政企数字化，2025 年市场规模为 800亿元。E001

## 公司商业模式分析
公司围绕 ICT 设备与云服务交付，收入为 800亿元。E002

## 财务分析
毛利率为 20%，经营现金流为 50亿元。E002

## 投资逻辑
投资逻辑关注行业需求、公司渠道和现金流验证。E001

## 估值分析
可比公司估值为 20倍。E002

## 风险分析
风险包括竞争、需求和现金流波动。E002

## 证据链
| id | source |
| --- | --- |
| E001 | 行业资料 |
| E002 | 公司公告 |
"""


EVIDENCE = """# Evidence Ledger

| id | source |
| --- | --- |
| E001 | 行业资料 |
| E002 | 公司公告 |
"""


RESEARCH_INTELLIGENCE = """# 紫光股份 Full Research Intelligence Document

## 1. 公司概览
E001
## 2. 行业研究
E002
## 3. 产业竞争分析
E003
## 4. 公司业务分析
E004
## 5. 护城河分析
E005
## 6. 财务分析
E006
## 7. 投资逻辑
### 7.1 Bull Case
### 7.2 Base Case
### 7.3 Bear Case
## 8. 风险分析
E007
## 9. 估值分析
E008
## 10. 跟踪指标
E009
## Evidence Ledger
| ID | claim | source | date | confidence | notes |
|---|---|---|---|---|---|
| E001 | 主体 | 年报第1页 | 2025-12-31 | high | 法定披露 |
| E002 | 行业 | 官方数据 | 2026-08-13 | medium | 待更新 |
| E003 | 竞争 | 公司年报 | 2025-12-31 | medium | 管理层披露 |
| E004 | 业务 | 公司年报 | 2025-12-31 | high | 法定披露 |
| E005 | 护城河 | 公司年报 | 2025-12-31 | medium | 框架判断 |
| E006 | 财务 | 财务报表 | 2025-12-31 | high | 合并口径 |
| E007 | 风险 | 公司年报 | 2025-12-31 | medium | 风险章节 |
| E008 | 估值 | 市场数据 | 2026-08-13 | medium | 日频数据 |
| E009 | 跟踪 | 综合推导 | 2026-08-13 | medium | 研究判断 |
"""


LEGACY_SCRIPTS = """# 视频脚本

## 长视频
Hook：紫光股份为什么值得关注？
行业背景：2025 年市场规模为 800亿元。E001
公司优势：公司围绕 ICT 设备与云服务交付。E002
财务验证：毛利率为 20%，经营现金流为 50亿元。E002
投资逻辑：关注行业需求、公司渠道和现金流验证。E001
风险：竞争、需求和现金流波动。
总结：核心观点是增长需要财务继续验证。
跟踪指标：收入增速、毛利率、经营现金流。

## 短视频 1
标题：紫光股份的关键问题
Hook：为什么要看它？
内容：2025 年市场规模为 800亿元。
结尾：继续跟踪毛利率。

## 短视频 2
标题：财务怎么验证
Hook：看一个指标。
内容：毛利率为 20%。
结尾：继续跟踪现金流。

## 短视频 3
标题：风险在哪里
Hook：不是只看增长。
内容：风险包括竞争和需求波动。
结尾：等待数据验证。
"""


NARRATIVE = """# content-narrative-plan

## 用户定位
目标观众：关注 A 股科技公司的普通投资者。
用户痛点：研报太长，难判断为什么该关注。

## 核心冲突
为什么用户应该关注这个公司？行业需求改善，但财务验证仍需跟踪。

## 视频主题
- 角度一：行业需求能否传导到公司
- 角度二：毛利率能否验证竞争力
- 角度三：现金流能否支持逻辑

## Hook设计
前30秒开场：紫光股份的问题不是收入有多大，而是增长能不能被毛利率和现金流验证。

## 故事结构
8-15分钟视频结构：
1. 00:00-00:30 Hook
2. 00:30-02:00 行业背景
3. 02:00-04:00 公司优势
4. 04:00-06:00 财务验证
5. 06:00-08:00 投资逻辑
6. 08:00-10:00 风险与跟踪

## 标题方向
- 紫光股份真正要验证什么
- 一家公司从行业到财务的跟踪框架
"""


LONG_SCRIPT = """# video-script

## 开场
Hook：紫光股份为什么值得关注？
问题提出：行业需求改善，但财务是否验证，是这期视频的主线。

## 正文
行业背景：2025 年市场规模为 800亿元。E001
公司优势：公司围绕 ICT 设备与云服务交付。E002
财务验证：毛利率为 20%，经营现金流为 50亿元。E002
投资逻辑：关注行业需求、公司渠道和现金流验证。E001
风险：竞争、需求和现金流波动。

## 结尾
总结：核心观点是增长需要财务继续验证。
跟踪指标：收入增速、毛利率、经营现金流。
"""


SHORT_SCRIPTS = """# short-video-scripts

## 短视频 1
标题：紫光股份的关键问题
Hook：为什么要看它？
内容：2025 年市场规模为 800亿元。E001
结尾：继续跟踪毛利率。

## 短视频 2
标题：财务怎么验证
Hook：看一个指标。
内容：毛利率为 20%。E002
结尾：继续跟踪现金流。

## 短视频 3
标题：风险在哪里
Hook：不是只看增长。
内容：风险包括竞争和需求波动。E002
结尾：等待数据验证。
"""


SRT = """NOTE estimated

1
00:00:00,000 --> 00:00:04,000
紫光股份为什么值得关注？

2
00:00:04,000 --> 00:00:08,000
2025 年市场规模为 800亿元。

3
00:00:08,000 --> 00:00:12,000
毛利率为 20%，经营现金流为 50亿元。
"""


MATERIALS = """# material-plan

| 时间段 | 画面 | 数据图表 | 来源 |
| --- | --- | --- | --- |
| 00:00-00:30 | 公司与行业开场画面 | 行业规模趋势图 | E001 |
| 00:30-02:00 | 公司业务示意画面 | 收入与毛利率图 | E002 |
"""


RID = """# 紫光股份（000938.SZ）Research Intelligence Document

## 0. 研究范围、资源执行与证据边界

研究阶段不为内容生产压缩。

## 1. 公司概览

主体信息。E001

## 2. 行业研究

行业边界。E001

## 3. 产业竞争分析

竞争格局。E001

## 4. 公司业务分析

收入结构。E002

## 5. 护城河分析

客户粘性和技术壁垒。E001

## 6. 财务分析

收入 800亿元，毛利率 20%。E002

## 7. 投资逻辑

Bull Case：需求改善。
Base Case：收入增长但毛利仅企稳。
Bear Case：竞争加剧。

## 8. 风险分析

行业、财务、竞争、管理和估值风险。

## 9. 估值分析

PE 为 20倍。E002

## 10. 跟踪指标

收入、毛利率、经营现金流。

## Evidence Ledger

| claim | source | date | confidence | notes |
| --- | --- | --- | --- | --- |
| E001 主体和行业 | 年报 | 2026-04-15 | high | A级证据 |
| E002 财务和估值 | 一季报 | 2026-04-29 | high | A级证据 |
"""


def write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


class ValidateResearchCliTest(unittest.TestCase):
    def run_cli(self, args: list[str], cwd: Path) -> tuple[int, str, str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
        return result.returncode, result.stdout, result.stderr

    def test_research_intelligence_mode_accepts_ten_sections_and_ledger_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            output = base / "research-quality-report.md"
            code, stdout, stderr = self.run_cli(
                [
                    "--research-intelligence",
                    str(write(base / "research-intelligence-document.md", RESEARCH_INTELLIGENCE)),
                    "--output",
                    str(output),
                ],
                base,
            )
            self.assertEqual(code, 0, msg=stderr)
            self.assertIn("PASS", stdout)
            report = output.read_text(encoding="utf-8")
            self.assertIn("阻断项：0", report)
            self.assertIn("claim、source、date、confidence、notes齐全", report)

    def test_legacy_scripts_cli_still_accepts_aggregated_scripts(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            output = base / "quality-report.md"
            code, stdout, stderr = self.run_cli(
                [
                    "--master",
                    str(write(base / "master.md", MASTER)),
                    "--scripts",
                    str(write(base / "scripts.md", LEGACY_SCRIPTS)),
                    "--subtitles",
                    str(write(base / "subtitle.srt", SRT)),
                    "--materials",
                    str(write(base / "materials.md", MATERIALS)),
                    "--evidence",
                    str(write(base / "evidence.md", EVIDENCE)),
                    "--output",
                    str(output),
                ],
                base,
            )

            self.assertEqual(
                code,
                0,
                stdout + stderr + (output.read_text(encoding="utf-8") if output.exists() else ""),
            )
            self.assertIn("PASS WITH WARNINGS", stdout)
            report = output.read_text(encoding="utf-8")
            self.assertIn("- scripts:", report)
            self.assertIn("母稿→脚本数字", report)

    def test_content_layer_cli_validates_independent_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            output = base / "quality-report.md"
            code, stdout, stderr = self.run_cli(
                [
                    "--master",
                    str(write(base / "master.md", MASTER)),
                    "--narrative-plan",
                    str(write(base / "content-narrative-plan.md", NARRATIVE)),
                    "--long-script",
                    str(write(base / "video-script.md", LONG_SCRIPT)),
                    "--short-scripts",
                    str(write(base / "short-video-scripts.md", SHORT_SCRIPTS)),
                    "--subtitles",
                    str(write(base / "subtitle.srt", SRT)),
                    "--materials",
                    str(write(base / "material-plan.md", MATERIALS)),
                    "--evidence",
                    str(write(base / "evidence.md", EVIDENCE)),
                    "--output",
                    str(output),
                ],
                base,
            )

            self.assertEqual(
                code,
                0,
                stdout + stderr + (output.read_text(encoding="utf-8") if output.exists() else ""),
            )
            self.assertIn("PASS WITH WARNINGS", stdout)
            report = output.read_text(encoding="utf-8")
            self.assertIn("content-production", report)
            self.assertIn("quality-assurance", report)
            self.assertNotIn("content-narrative-design", report)
            self.assertNotIn("video-script-generation", report)
            self.assertIn("估算时间轴", report)
            self.assertIn("- narrative_plan:", report)
            self.assertIn("- long_script:", report)
            self.assertIn("- short_scripts:", report)

    def test_research_intelligence_cli_validates_ten_sections_and_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            output = base / "research-quality-report.md"
            code, stdout, stderr = self.run_cli(
                [
                    "--research-intelligence",
                    str(write(base / "research-intelligence-document.md", RID)),
                    "--output",
                    str(output),
                ],
                base,
            )

            self.assertEqual(
                code,
                0,
                stdout + stderr + (output.read_text(encoding="utf-8") if output.exists() else ""),
            )
            self.assertIn("PASS", stdout)
            report = output.read_text(encoding="utf-8")
            self.assertIn("RID章节：公司概览", report)
            self.assertIn("RID章节：跟踪指标", report)
            self.assertIn("Evidence Ledger字段", report)
            self.assertIn("investment-research", report)


if __name__ == "__main__":
    unittest.main()
