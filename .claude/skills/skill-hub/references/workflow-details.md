# Workflow Implementation Details

This file contains detailed implementation steps for Workflows C and D.

## Workflow C: Direct Installation

### Step-by-Step Installation Process

#### Step 1: Confirm Installation

Show user what will be installed:

```
📦 准备安装：

Skill名称：xlsx
评分：89/100 ✅ 建议安装
来源：https://github.com/anthropics/skills/tree/main/skills/xlsx

安装位置：~/.claude/skills/xlsx

确认安装吗？(yes/no)
```

#### Step 2: Execute Installation

Run the installation script:

```bash
python3 scripts/install_skill.py <github_url> [--skill-name <name>]
```

**Examples:**
```bash
# Install from GitHub URL
python3 scripts/install_skill.py https://github.com/anthropics/skills/tree/main/skills/xlsx

# Install with custom name
python3 scripts/install_skill.py https://github.com/user/repo/my-skill --skill-name custom-name

# Install from local path
python3 scripts/install_skill.py /path/to/local/skill
```

#### Step 3: Report Results

The script will:
1. Clone/copy Skill files to `~/.claude/skills/<skill-name>`
2. Verify SKILL.md exists and is valid
3. Output installation status

**Success output:**
```json
{
  "success": true,
  "skill_name": "xlsx",
  "install_path": "~/.claude/skills/xlsx",
  "message": "✅ Skill 'xlsx' installed successfully"
}

🎉 Installation complete! Restart Claude Code to use the new skill.
```

**Failure output:**
```json
{
  "success": false,
  "skill_name": "xlsx",
  "error": "SKILL.md not found or invalid"
}
```

#### Step 4: Post-Installation

Remind user to restart Claude Code:

```
✅ Skill已成功安装到 ~/.claude/skills/xlsx

⚠️ 重要：请重启Claude Code以使Skill生效

重启后，您可以：
- 使用 /xlsx 触发Skill
- 在对话中描述需求，系统会自动激活
```

---

## Workflow D: Construction Guidance

### Step-by-Step Analysis Process

#### Step 1: Analyze Skill Patterns

Run the analysis script:

```bash
python3 scripts/analyze_skill_patterns.py <github_url_or_local_path>
```

The script will extract:
- Architecture patterns
- Implementation techniques
- Reusable components
- Construction steps

#### Step 2: Present Construction Guide

Show a structured guide with 7 key sections:

**1. Skill Type Classification**
```
📋 这是一个：API Integration Skill

类似的Skills：
- safe-skill-copy (GitHub API integration)
- mcp-builder (API server creation)
```

**2. Architecture Overview**
```
🏗️ 架构设计：

- Uses step-by-step workflow structure
- Employs progressive disclosure with 3 reference files
- Includes executable scripts in: Python
```

**3. Key Components**
```
🔧 核心组件：

1. SKILL.md frontmatter
   目的：Metadata and triggering information
   详情：Contains: name, description

2. Executable scripts
   目的：Perform deterministic operations
   详情：Languages: Python, Complexity: moderate

3. Reference files
   目的：Extended documentation for progressive disclosure
   详情：Files: scoring-criteria.md, installation-guide.md
```

**4. Implementation Steps**
```
📝 实现步骤：

Step 1: Initialize Skill structure
操作：Use skill-creator's init_skill.py
命令：python scripts/init_skill.py <skill-name>

Step 2: Define SKILL.md frontmatter
操作：Write clear name and comprehensive description
提示：
  - Include 'Use when' scenarios in description
  - Add example trigger phrases in quotes
  - Be specific about what the Skill does

Step 3: Implement scripts
操作：Write executable scripts in Python
提示：
  - Keep scripts focused on single responsibility
  - Return JSON for easy parsing
  - Handle errors gracefully with clear messages
  - Install dependencies: urllib, json, pathlib

Step 4: Test and validate
操作：Use skill-creator's package_skill.py to validate
命令：python scripts/package_skill.py <path/to/skill>
```

**5. Reusable Patterns**
```
♻️ 可复用模式：

1. Progressive disclosure
   说明：Keep SKILL.md concise, move details to reference files
   示例：See [REFERENCE.md](references/REFERENCE.md) for details

2. JSON output format
   说明：Scripts return structured JSON for easy parsing
   示例：print(json.dumps(result, ensure_ascii=False, indent=2))

3. Multi-step workflow
   说明：Break complex tasks into sequential steps
   示例：Step 1: ... Step 2: ... Step 3: ...
```

**6. Similar Examples**
```
💡 参考示例：

- Anthropic official Skills (github.com/anthropics/skills)
- awesome-claude-skills community Skills
- skill-creator (Skill creation workflow)
```

**7. Construction Tips**
```
💡 构建建议：

✅ Start with concrete examples of how the Skill will be used
✅ Keep SKILL.md under 500 lines for better context efficiency
✅ Test scripts independently before integrating
✅ Use descriptive names for scripts (fetch_X.py, analyze_Y.py)
✅ Show example outputs after each workflow step
✅ Add explicit trigger patterns to description
```

#### Step 3: Offer Next Steps

```
🎯 接下来您可以：

1. 🚀 直接开始构建
   - 使用 /skill-creator 初始化一个新Skill
   - 参考上面的架构设计和实现步骤

2. 📚 深入学习
   - 查看参考示例的源代码
   - 研究类似Skills的实现方式

3. 💬 继续交流
   - 告诉我您想构建什么类型的Skill
   - 我可以提供更具体的指导
```

---

## Common Installation Issues

### URL 无法访问
**问题**：GitHub 仓库无法访问

**解决方案**：
- 检查仓库是否公开
- 确认网络连接
- 尝试使用 VPN

### 脚本执行失败
**问题**：Python 脚本无法运行

**解决方案**：
- 确保已安装 Python 3.6+
- 使用 `python3` 而非 `python`
- 检查脚本权限（`chmod +x`）

### 安装失败回滚
**问题**：安装过程中出错

**特性**：install_skill.py 会自动清理失败的安装

**无需手动操作**：失败的文件会被自动删除

### Skill 已存在
**问题**：目标位置已有同名 Skill

**解决方案**：
- 删除旧版本：`rm -rf ~/.claude/skills/<skill-name>`
- 或使用 `--skill-name` 指定新名称

---

## Performance Tips

### 搜索优化
- 使用具体的关键词（"数据分析和CSV处理"而非"数据分析"）
- 中英文混合查询效果更好
- 避免过于宽泛的查询

### 评估优化
- 批量评估多个 Skills 时，使用 auto_evaluate_skills.py
- 对于已知高质量 Skill，可跳过详细评估

### 安装优化
- 从本地路径安装比 GitHub 克隆更快
- 使用 `--skill-name` 避免名称冲突
