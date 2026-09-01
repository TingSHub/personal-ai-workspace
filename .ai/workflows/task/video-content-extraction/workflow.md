# Workflow: video-content-extraction

> 位置: Global: .ai/workflows/task/video-content-extraction/workflow.md

## Mission

把视频文件解析为可消费的文本 + 视觉资产:音频转写(中文 ASR)、关键帧抽取、视觉版式分析、文档化。产出转写稿、帧目录、视觉特征报告——供蒸馏(cangjie-skill)、内容分析、版式参考等下游使用。

## Input

| 字段 | 必填 | 说明 |
|---|---|---|
| video_path | 是 | 视频文件路径(mp4/mov/mkv) |
| 输出目录 | 是 | 产物落盘位置(通常 {workdir}/extract/) |
| 语言 | 否 | ASR 语言(默认 zh) |
| 话题时间戳 | 否 | 若已知话题段落,按段抽帧;否则均匀抽帧 |

## Output

| 产物 | 格式 | 说明 |
|---|---|---|
| transcript.md | markdown | 带时间戳的转写稿(每段 [HH:MM:SS] 文本) |
| transcript.json | json | 结构化 segments(时间戳 + 文本) |
| frames/ | jpg 目录 | 关键帧(话题段或均匀抽帧) |
| visual-analysis.md | markdown | 像素级视觉分析:主色板/版式结构/内容带/共有元素 |
| extraction-execution.md | markdown | 资源 by-name、参数、产物清单、验收状态 |

## Principles

- 无文本不分析:转写是下游所有分析的前提
- 说话人无标注时,参考片段/内容归属需基频等客观验证,不凭句式猜测
- 视觉分析用像素级量化(色板/内容占比/行带),语义细节由人确认
- 真实执行留痕;by-name 引用资源

## Phase 1: 音频转写 — 中文 ASR

### Goal

提取视频音轨,用本地 ASR 转写为带时间戳的中文文本。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| faster-whisper | skill | 必选 | Systran · 项目 .venv-asr | 中文转写(medium 模型质量佳);CPU 可跑,22 分钟音频 ~13 分钟 |
| ffmpeg | 系统工具 | 必选 | 系统 | 音轨提取(16kHz mono wav) |

### Input

- video_path;语言(默认 zh)

### Output

- `transcript.md`(带时间戳分段)+ `transcript.json`

### Quality Criteria

- 转写覆盖全片(时长一致,无截断)
- 分段带时间戳,文本可追溯
- 转写质量:中文 medium 模型(实测 22 分钟音频质量可接受);敏感数字抽查核对

### Known Issues

- 转写稿无说话人标注:说话人归属需基频验证或其他来源,不凭文本句式推断
- 长视频分段处理;VAD 过滤静音

## Phase 2: 关键帧抽取

### Goal

按话题段落或均匀间隔抽取关键帧,覆盖内容变化点(数据页/图表页/纯文字页)。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| ffmpeg | 系统工具 | 必选 | 系统 | `-ss <t> -frames:v 1` 抽帧 |

### Input

- video_path;话题时间戳(或均匀间隔,每 60-90s 一帧)

### Output

- `frames/{label}-{t}.jpg`(每话题 1-2 帧 + 开场/结尾)

### Quality Criteria

- 每话题至少 1 帧;含数据对比帧与纯文字帧
- 帧可读(jpg 质量 q3)

### Known Issues

- 画面切换瞬间抽帧可能抓到过渡帧;按话题段落中段抽更稳

## Phase 3: 视觉版式分析

### Goal

对关键帧做像素级量化分析:主色板、内容密度、内容行带、跨帧共有元素,产出版式特征报告。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| python3 + PIL | 系统工具 | 必选 | 系统 | 像素分析(色板/内容占比/行带/共有元素) |

### Input

- Phase 2 帧目录

### Output

- `visual-analysis.md`:主色板/内容密度(对比像素%)/内容行带/跨帧共有元素(≥80% 帧出现的位置)

### Quality Criteria

- 覆盖全部帧;跨帧共有元素识别(顶部/底部固定带)
- 语义细节(元素含义)标记待人工确认,不臆断

### Known Issues

- 背景色判定受视频压缩影响(渐变/噪点),用主色板 + 内容像素双维度
- 视觉风格蒸馏(配色/版式定稿)需人工看帧确认,自动化只给量化特征

## Phase 4: 文档化

### Goal

汇总产物为执行记录,标注资源 by-name、参数与验收状态。

### Required Resources

无(汇总文档)

### Input

- Phase 1-3 产物

### Output

- `extraction-execution.md`:资源、参数、产物清单、验收状态、已知限制

### Quality Criteria

- 资源 by-name 可识别;参数可复现;验收状态如实

### Known Issues

- 大视频文件不复制,直接引用源路径
