# Open Skill Finder｜开放 Skill 查找器

[English](README_EN.md) · 简体中文

一个面向通用 AI Agent 的开源 Skill：从本机、skills.sh、GitHub 和可配置目录中搜索 Agent Skills，并在推荐或安装前完成结构检查、安全审查、证据评分和来源核验。

它解决的不是“搜到最多”，而是“找到真正匹配、来源可追溯、风险可解释的 Skill”。

## 为什么做这个项目

常见的 Skill 查找工具往往依赖单一目录，主要按照关键词、安装量或 Star 排序。这样很快，但有几个问题：

- 一个目录失效，搜索能力也随之失效；
- 搜索排名和安装量不能证明安全或真实适用；
- 同名 Skill、合集中的不同路径容易被错误合并；
- 找到结果后直接安装，缺少对脚本、依赖、权限和外部链接的检查；
- 推荐理由通常不可复核，也很少说明信息缺口。

Open Skill Finder 把流程拆成四个独立阶段：

```text
多源发现 → 规范化去重 → 结构与安全门禁 → 可解释评分 → 用户确认后安装
```

安全门禁优先于分数。未经审查的候选可以展示，但不能被标记为可安装；高热度也不能抵消高风险问题。

## 主要能力

- 多源搜索：本机已安装 Skills、skills.sh、GitHub Code Search、自定义 JSON 目录；
- 可靠去重：按“仓库 + Skill 路径”识别，而不是只比较名称；
- 静态检查：检查 `SKILL.md`、全部脚本、引用、隐藏文件、符号链接、安装钩子、远程 URL 和可疑指令；
- 可解释评分：相关性、项目质量、来源、维护、使用量、社区证据、文档/测试/可移植性；
- 安全安装：明确来源和版本，先征得用户同意，安装后重新核验；
- 中英文输出：默认简体中文，可切换英文；
- 通用架构：遵循开放的 Agent Skills 目录结构，不绑定某一个 Agent 或某一家模型。

## 快速开始

### 作为 Skill 安装

```bash
npx skills add https://github.com/30bewater/open-skill-finder
```

也可以把本仓库复制到你的 Agent 所支持的 Skills 目录。不同客户端的目录和安装方式可能不同，请以对应客户端文档为准。

安装后可以直接表达需求，例如：

```text
帮我找一个能做视频、图片和音频格式转换的 Skill，比较来源和风险，先不要安装。
```

```text
找三个适合做 GitHub Issue 分类的通用 Skill，用中文给出证据卡。
```

### 独立使用脚本

这些脚本仅使用 Python 标准库，建议 Python 3.10+。

检查当前可用能力：

```bash
python scripts/probe_capabilities.py
```

搜索并保存候选：

```bash
python scripts/search_skills.py "media processing" --output candidates.json
```

审查一个已经下载到本机的候选：

```bash
python scripts/inspect_skill.py /path/to/example-skill --output audit.json
```

将审查报告放入候选的 `audit` 字段后进行评分：

```bash
python scripts/rank_skills.py --query "media processing" --input candidates.json --output ranked.json
```

渲染中文或英文推荐卡：

```bash
python scripts/render_cards.py --input ranked.json --lang zh
python scripts/render_cards.py --input ranked.json --lang en
```

每个脚本都支持 `--help`。

## 自定义搜索源

```bash
python scripts/search_skills.py "pdf" \
  --registry my-index=https://example.com/api/skills/search
```

接口接受 `q` 和 `limit` 参数，返回数组，或包含 `skills`、`results`、`items` 的对象。字段示例见 [references/providers.md](references/providers.md)。不要把访问令牌写进 URL。

## 评分规则

默认满分 100：

| 维度 | 分值 |
|---|---:|
| 需求相关性 | 30 |
| GitHub 项目质量 | 20 |
| 来源与可追溯性 | 15 |
| 维护情况 | 10 |
| 使用证据 | 10 |
| 独立社区证据 | 5 |
| 文档、测试与可移植性 | 10 |

完整解释见 [references/scoring.md](references/scoring.md)。Star、安装量和语义相似度都可能被操纵，因此它们只占有限权重。

## 安全边界

内置检查器是保守的静态扫描，不执行候选脚本。它会发现一部分高风险模式，但不能证明 Skill 绝对安全。重要环境建议同时使用独立扫描器并进行人工代码审查。

任何未解决的 `high` 或 `critical` 问题都会阻止安装建议。联网、安装软件包、访问凭据、修改全局配置等行为必须单独解释并征得同意。详见 [references/security.md](references/security.md)。

## 项目结构

```text
open-skill-finder/
├── SKILL.md                 # Agent 使用说明和工作流
├── agents/openai.yaml       # 可选的产品界面元数据
├── scripts/                 # 搜索、检查、评分和渲染工具
├── references/              # Provider、安全、评分、安装和输出规范
├── tests/                   # 标准库单元测试
└── README_EN.md             # English documentation
```

## 设计原则

- 搜索和信任分离；
- 实际文件优先于目录摘要；
- 证据优先于流行度；
- 缺失信息明确标注，不猜测；
- 安装是独立、需要确认的阶段；
- 默认输出简体中文，始终提供英文选项。

## 参考与致谢

本项目的设计参考了 Agent Skills 开放规范，以及 Vercel Skills、SkillX、oakoss/agent-skills、AgentBay Skills、Cisco AI Defense Skill Scanner、Sentry Skill Scanner、VoltAgent Awesome Agent Skills 等公开项目的思路。具体说明见 [NOTICE](NOTICE)。本项目为独立实现，不包含上述项目复制的源代码。

## 许可证

[MIT License](LICENSE)
