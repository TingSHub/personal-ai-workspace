---
name: skill-hub
description: Complete Skill lifecycle assistant - SEARCH Skills (3-tier 16 official + 160+ curated + unlimited GitHub), EVALUATE with 6-dimensional scoring, INSTALL with one command, LEARN construction patterns. Triggers - Search:"帮我找Skill". Evaluate:"评估这个Skill". Install:"安装这个Skill". Learn:"怎么构建类似的Skill".
---

# Skill Hub v3.0

**Skill全链路助手：搜索 → 评估 → 安装 → 构建**

> 🎉 v3.0 Major Update: 完整Skill生命周期支持
> - 🔍 搜索：三层架构智能搜索（官方+精选+GitHub全平台）
> - ✅ 评估：六维安全评分
> - 📦 安装：一键直接安装
> - 🛠️ 构建：学习构建经验

## Core Features

### 🔍 Feature 1: Smart Skill Search

Automatically find Skills based on your requirements - no need to know specific Skill names or URLs.

**How it works:**
1. User describes their need in natural language (Chinese or English)
2. System expands keywords and searches 3-tier sources:
   - L1: Anthropic official (16 Skills, highest quality)
   - L2: awesome-claude-skills (160+ curated, community verified)
   - L3: GitHub code search (unlimited, real-time discovery, up to 200 results)
3. Results ranked by relevance (top 10 shown from 200+ candidates)
4. Top matches automatically evaluated for security

**Example queries:**
- "我需要一个数据分析的Skill"
- "Find me skills for project management"
- "有没有前端开发相关的Skill"
- "Search for testing and debugging tools"

### ✅ Feature 2: Security Evaluation

Evaluate specific Skills using a six-dimensional security scoring model.

### 📦 Feature 3: Direct Installation (NEW in v3.0)

Install Skills directly from GitHub or local paths with one command.

**How it works:**
1. After evaluation, system provides installation option
2. User confirms installation
3. System clones/copies Skill to ~/.claude/skills/
4. Verifies installation (SKILL.md exists and valid)
5. Prompts user to restart Claude Code

**Benefits:**
- No manual git clone or file copying
- Automatic validation
- Error handling and rollback on failure

### 🛠️ Feature 4: Construction Guidance (NEW in v3.0)

Learn how to build similar Skills by analyzing existing ones.

**How it works:**
1. System analyzes Skill structure and patterns
2. Extracts key components and implementation techniques
3. Provides step-by-step construction guide
4. Suggests reusable patterns and similar examples

**What you get:**
- Skill type classification
- Architecture overview
- Key components breakdown
- Implementation steps
- Reusable code patterns
- Similar Skills for reference
- Construction tips

## Workflows

### Workflow A: Search & Discover Skills

**Use when**: User describes a need without providing a specific Skill URL

**Trigger patterns:**
- "帮我找一个...的Skill"
- "有没有...相关的Skill"
- "search for skills about..."
- "I need a skill for..."

#### Step 1: Search for Skills

Run the search script with user's requirement:

```bash
python3 scripts/search_skills.py "<user requirement>"
```

**Examples:**
```bash
# Chinese query
python3 scripts/search_skills.py "数据分析和可视化"

# English query
python3 scripts/search_skills.py "project management and task tracking"

# Technical query
python3 scripts/search_skills.py "前端开发和React"
```

The script returns:
- Top 10 most relevant Skills
- Relevance score (0.0-1.0)
- Skill description and URL
- Source category (official/community)

#### Step 2: Present Search Results

Format results as a table:

```
🔍 找到 X 个相关 Skills：

| 排名 | Skill名称 | 相关度 | 类别 | 描述 |
|------|----------|--------|------|------|
| 1 | skill-name | 0.85 | 官方 | Description... |
| 2 | skill-name | 0.72 | 社区 | Description... |
| ... |

💡 自动评估前3个最相关的Skills...
```

#### Step 3: Auto-Evaluate Top Results

Automatically evaluate the top 3 most relevant Skills using Workflow B below.

Show brief scores for each:
```
📊 快速评分：

1. skill-name-1: 85/100 ✅ 建议安装
2. skill-name-2: 72/100 ✅ 建议安装
3. skill-name-3: 58/100 ⚠️ 谨慎安装
```

#### Step 4: Offer User Choices

After evaluation, present user with THREE options:

```
💡 您想要：
1. 📦 直接安装这个Skill（一键安装）
2. 🔍 查看详细评估报告
3. 🛠️ 学习如何构建类似的Skill
```

**If user chooses option 1** → Proceed to Workflow C (Direct Installation)
**If user chooses option 2** → Proceed to Workflow B (Detailed Evaluation)
**If user chooses option 3** → Proceed to Workflow D (Construction Guidance)

---

### Workflow B: Evaluate Specific Skill

**Use when**: User provides a specific GitHub URL or local path, OR after search results are presented

**Trigger patterns:**
- User provides a URL: "评估这个Skill https://github.com/..."
- After search: "给我详细评估第2个Skill"
- Direct evaluation: "check if this skill is safe"

#### Step 1: Fetch Skill Content

Run the fetch script to get SKILL.md and scripts content:

```bash
python3 scripts/fetch_skill.py <github_url_or_local_path>
```

The script handles:
- GitHub URLs (converts to raw.githubusercontent.com automatically)
- Local file paths (absolute or relative)
- SKILL.md + scripts/ directory content

**Edge cases:**
- If URL is inaccessible: Report "无法读取 Skill 内容，请确认 URL 是否正确或仓库是否公开"
- If user provides raw SKILL.md text: Skip script, evaluate directly
- If no scripts found: Note "无 Scripts 文件" in safety dimension

#### Step 2: Load Scoring Criteria

Read [scoring-criteria.md](references/scoring-criteria.md) for detailed evaluation rules.

#### Step 3: Evaluate Six Dimensions

Evaluate each dimension with score and brief reasoning:

1. **来源可信度 (Source Trust)** — /25
   - Anthropic official: 25
   - High-star repo (>1000): 20
   - Community user: 10-15
   - Unknown/new: 0-5

2. **社区热度 (Community Activity)** — /20
   - Star count + recent commits + documentation quality

3. **任务明确性 (Task Clarity)** — /20
   - Clear description + specific trigger scenarios

4. **可复用性 (Reusability)** — /15
   - No hardcoded paths + environment independence

5. **安全性 (Security)** — /10
   - No network requests + minimal tool permissions

6. **跨平台兼容 (Cross-platform)** — /10
   - POSIX paths + no platform-specific APIs

#### Step 4: Output Results

Format:

```
来源可信度：XX / 25 — [reasoning]
社区热度：  XX / 20 — [reasoning]
任务明确性：XX / 20 — [reasoning]
可复用性：  XX / 15 — [reasoning]
安全性：    XX / 10 — [reasoning]
跨平台兼容：XX / 10 — [reasoning]

总分：XX / 100
```

Then provide conclusion:

- **≥ 70**: ✅ **建议安装** + 提供简化安装命令（参考 installation-guide.md）
- **50-69**: ⚠️ **谨慎安装** + 列出具体风险点 + 由用户决定
- **< 50**: ❌ **不建议安装** + 说明主要失分维度 + 建议寻找替代方案

---

## Search Tips

### Effective Search Queries

**Good queries** (specific and descriptive):
- ✅ "数据分析和CSV处理"
- ✅ "project management with Linear integration"
- ✅ "前端开发和React组件"
- ✅ "security vulnerability scanning"

**Less effective queries** (too vague):
- ❌ "开发工具"
- ❌ "automation"
- ❌ "工作流"

### Keyword Expansion

The search automatically expands your query with related keywords:

| Your Query | Auto-Added Keywords |
|------------|-------------------|
| 数据分析 | data analysis, analytics, csv, excel, pandas, visualization |
| 项目管理 | project management, task, issue, kanban, linear, jira |
| 前端开发 | frontend, react, vue, web, ui |
| 安全 | security, vulnerability, audit, penetration |

### Search Sources

1. **Anthropic Official Skills** (16个)
   - Pre-vetted and high quality
   - Averaged 96/100 score
   - Source: https://github.com/anthropics/skills

2. **ComposioHQ/awesome-claude-skills** (160+个) ⭐ NEW
   - Curated community Skills collection (39K GitHub stars)
   - Includes 78+ app automation Skills (GitHub, Slack, Gmail, Notion, etc.)
   - Community-verified quality
   - Source: https://github.com/ComposioHQ/awesome-claude-skills

3. **GitHub Community Skills**
   - Wider variety but varies in quality
   - Auto-filtered by relevance

---

### Workflow C: Direct Installation (NEW in v3.0)

**Use when**: User wants to install a Skill immediately after evaluation

**Trigger patterns:**
- "安装这个Skill"
- "Install this skill"
- "帮我装上它"

**Quick steps:**
1. Confirm installation details with user
2. Run: `python3 scripts/install_skill.py <github_url>`
3. Verify installation and prompt user to restart Claude Code

**For detailed steps**, see [workflow-details.md](references/workflow-details.md#workflow-c-direct-installation)

---

### Workflow D: Construction Guidance (NEW in v3.0)

**Use when**: User wants to learn how to build a similar Skill

**Trigger patterns:**
- "怎么构建类似的Skill"
- "Show me how to build this"
- "教我怎么做"

**Quick steps:**
1. Run: `python3 scripts/analyze_skill_patterns.py <url>`
2. Present 7-section construction guide:
   - Skill type classification
   - Architecture overview
   - Key components
   - Implementation steps
   - Reusable patterns
   - Similar examples
   - Construction tips
3. Offer next steps (build/learn/discuss)

**For detailed output format**, see [workflow-details.md](references/workflow-details.md#workflow-d-construction-guidance)

---

## Real-World Examples

### Example 1: Complete Discovery Journey

```
User: "我需要一个Excel处理的Skill"

Claude: 🔍 搜索中...
找到 8 个相关 Skills

Top 3:
1. xlsx (0.92, 官方) - 电子表格处理
2. CSV Data Summarizer (0.78, 社区) - CSV分析
3. Google Sheets (0.65, 社区) - Google表格

📊 快速评分：
1. xlsx: 96/100 ✅ 强烈推荐
2. CSV Data Summarizer: 74/100 ✅ 建议安装
3. Google Sheets: 84/100 ✅ 推荐

💡 您想要：
1. 📦 直接安装xlsx
2. 🔍 查看详细评估
3. 🛠️ 学习如何构建

User: "1"

Claude: 📦 准备安装xlsx
评分：96/100 ✅
来源：https://github.com/anthropics/skills/.../xlsx

[执行安装...]

✅ xlsx已成功安装！
⚠️ 请重启Claude Code使Skill生效
```

### Example 2: Learn and Build

```
User: "帮我分析一下xlsx是怎么构建的"

Claude: 🛠️ 分析xlsx构建模式...

📋 Skill类型：File Processing Skill

🏗️ 架构：
- Step-by-step workflow structure
- Python scripts for Excel operations
- Progressive disclosure with references

🔧 核心组件：
1. SKILL.md (清晰的workflow指导)
2. Python scripts (openpyxl处理)
3. 错误处理和验证

📝 实现步骤：
Step 1: 初始化Skill结构
Step 2: 实现Excel读写脚本
Step 3: 编写workflow文档
Step 4: 测试和验证

💡 参考示例：docx, pdf, pptx

User: "好的，我想基于这个构建一个CSV处理的Skill"

Claude: 很好！基于xlsx的模式，CSV处理Skill可以：
1. 复用相似的workflow结构
2. 使用pandas而非openpyxl
3. 简化处理逻辑（CSV比Excel简单）

要我帮您开始构建吗？
```

---

## Common Issues

- **URL 无法访问**：检查 GitHub 仓库是否公开，或使用 VPN
- **脚本执行失败**：确保已安装 Python 3，路径使用 `python3`
- **评分过低但仍想安装**：可手动审查代码后决定，风险自负
- **安装失败回滚**：install_skill.py会自动清理失败的安装
- **Skill已存在**：删除旧版本或使用 --skill-name 指定新名称

## Tools Used

- **Bash**: Run search_skills.py, fetch_skill.py, install_skill.py, analyze_skill_patterns.py
- **Read**: Load scoring criteria and script outputs
- No Write/Edit needed (read-only evaluation)
