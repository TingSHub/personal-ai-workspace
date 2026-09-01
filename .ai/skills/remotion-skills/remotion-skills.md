# remotion-skills

> 管理资产：`.ai/skills/remotion-skills/remotion-skills.md`；安装实体：`.claude/skills/remotion-skills/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/remotion-dev/remotion（skills 在 packages/skills；文档 remotion.dev） |
| installed_ref | skills 快照 2026-08-14（npx skills add remotion-dev/skills 安装） |
| runtime | both |
| 调用入口 | npx skills add remotion-dev/skills；npx remotion <render|still|studio>；项目内 npm scripts |
| 要求 | Node 18+ / npm；google-chrome 系统浏览器（--browser-executable 指定）；中文字体文件（Noto Sans SC / Serif SC，OFL）；注意 License：≤3 人盈利组织免费且输出可商用；4+ 人需 Company License |
| 更新 | package-manager · 按 remotion.dev 官方升级指引更新 remotion 包与 skills；审查 changelog 后重跑样片验证；验证：npx remotion still 单帧 + npx remotion render 一条 10 秒含中文音频样片 |
| 辅助脚本 | — |
| 经验引用 | — |

## 作用

Remotion：React 网页逐帧渲染视频框架 + 官方 Agent Skills（12 个）。本实验 84.20s 中文财经视频 v1 一次成功渲染（2526 帧 1080p30，2m41s），零 Remotion API 幻觉（写码前对照类型定义核实）。

## 调用

- 官方 Skills（必须先读）：`npx skills add remotion-dev/skills`（remotion-create / remotion-markup / remotion-captions / remotion-render / remotion-studio 等）
- 常用：`npx remotion still --frame=N`（单帧检查，~1.7s/帧）、`npx remotion render`（MP4）、`remotion studio`（预览）
- 浏览器：`--browser-executable=/usr/bin/google-chrome` 复用系统 Chrome
- 中文字体：Noto Sans/Serif SC 变量字体（OFL）本地加载（@remotion/fonts），不依赖 Google Fonts 在线
- 本实验验证的参考实现：`projects/investment-research-system/experiments/listed-company-video-production/outputs/web/remotion/`（v1/v2 全源文件 16 个）

## 调用注意事项

- **License**：非 OSI 开源。≤3 人盈利组织免费且输出可商用；4+ 人需 Company License（Creators $25/座/月 或 Automators $0.01/渲染+$100/月最低）；@remotion/captions 包本身 MIT
- 官方规则：动画必须 useCurrentFrame/interpolate 帧号驱动，禁第三方计时动画（防闪烁）；图表用 SVG 自绘（pathLength 描线 + strokeDashoffset）
- 音频用 `<Audio>` 组件；TTS 出音 → getAudioDuration → 场景时长 → 渲染（Audio First）
- 推荐输入：冻结脚本 + Scene 划分 + 数据引用表 + 旁白音频

## 常见失败原因

- `fontVariantNumeric` 不能作 SVG `<text>` 属性（tsc 报错）；布局坐标手算易溢出（2 次修复经验：标签与数字面板间距）
- npm i 慢（实测 6m05s 网络瓶颈）；包体积数百 MB
- LLM 生成代码幻觉靠官方 skills 缓解：remotion-markup 规则文档在写码前必读
- 中文逐词卡拉OK字幕：Remotion 分组逻辑默认英文空格分词，中文需自写按 `。，？！` 分组转换层（本轮未做画面内字幕，待第二轮）

## 最佳实践

- script → TTS → alignment → scene timing → render（Audio First）
- 图表 SVG 自绘比接 ECharts 更顺：pathLength 描线零依赖零坑；2024 未披露的数据不要伪造插值（三点等距排布即可）
- 大数字动画：interpolate 区间集中一处管理，改 timing 极快（翻转 7s→6.5s 改 3 个区间）
- 修改成本分级：删装饰（药丸徽章→扁平文字）几行代码；"每幕一个核心观点"的信息重组最贵（布局几何重算）——首版就按 Scene 划分设计，避免 v2 大改
