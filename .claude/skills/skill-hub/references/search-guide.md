# Skill搜索指南

## 什么是Skill搜索？

Skill搜索功能允许你通过描述需求来查找合适的Claude Skills，而不需要知道具体的Skill名称或GitHub URL。

## 工作原理

### 1. 关键词扩展

系统会自动将你的查询扩展为多个相关关键词：

| 你的查询 | 自动添加的关键词 |
|---------|-----------------|
| 数据分析 | data analysis, analytics, csv, excel, pandas, visualization |
| 项目管理 | project management, task, issue, kanban, linear, jira |
| 前端开发 | frontend, react, vue, web, ui |
| 测试 | test, testing, tdd, unit test, playwright |
| 文档 | documentation, doc, docx, pdf, markdown |

### 2. 多源搜索

- **Anthropic官方Skills** (优先)
  - 通过GitHub API获取
  - 平均评分96/100
  - 质量有保证

- **GitHub社区Skills**
  - 通过GitHub Code Search
  - 范围更广但质量参差
  - 自动过滤相关度

### 3. 相关度评分

每个Skill会根据以下因素计算相关度（0.0-1.0）：

- 关键词在Skill名称中的匹配
- 关键词在描述中的匹配
- 是否为官方Skill（+0.2加权）

### 4. 自动评估

搜索结果中Top 3最相关的Skills会自动进行快速评估，给出安全评分。

## 如何编写有效查询

### ✅ 好的查询（具体且描述性强）

```
数据分析和CSV处理
project management with Linear
前端开发和React组件
security vulnerability scanning
测试自动化和Playwright
PDF文档处理和表单填充
```

### ❌ 不太有效的查询（过于模糊）

```
开发工具
automation
工作流
代码
```

### 💡 查询技巧

1. **使用具体的技术名词**
   - ✅ "React前端开发"
   - ❌ "网页开发"

2. **组合多个关键词**
   - ✅ "数据分析和可视化"
   - ❌ "数据"

3. **包含你的使用场景**
   - ✅ "项目管理和任务追踪"
   - ❌ "管理"

4. **混合中英文也可以**
   - ✅ "前端开发React"
   - ✅ "project management项目管理"

## 搜索示例

### 场景1：数据分析需求

**查询**: `数据分析和可视化`

**可能找到的Skills**:
- csv-data-summarizer (CSV数据分析)
- xlsx (Excel处理)
- pdf (PDF表格提取)

### 场景2：项目管理需求

**查询**: `project management task tracking`

**可能找到的Skills**:
- Linear (Linear项目管理)
- kanban-skill (看板管理)
- task-observer (任务观察和改进)

### 场景3：前端开发需求

**查询**: `前端开发React组件`

**可能找到的Skills**:
- frontend-design (前端设计)
- web-artifacts-builder (React+shadcn/ui)
- webapp-testing (前端测试)

### 场景4：文档处理需求

**查询**: `文档编辑Word PDF`

**可能找到的Skills**:
- docx (Word文档)
- pptx (PowerPoint)
- pdf (PDF操作)
- doc-coauthoring (文档协作)

## 搜索结果解读

搜索会返回JSON格式的结果：

```json
{
  "query": "数据分析",
  "keywords": ["数据分析", "data analysis", "analytics", "csv", "excel"],
  "total_found": 8,
  "results": [
    {
      "name": "csv-data-summarizer",
      "url": "https://github.com/...",
      "description": "CSV数据分析工具...",
      "relevance_score": 0.85,
      "category": "community",
      "source": "username/repo"
    }
  ]
}
```

### 字段说明

- **relevance_score**: 相关度评分（0.0-1.0）
  - 0.8+ : 高度相关
  - 0.5-0.8 : 中度相关
  - 0.1-0.5 : 低度相关
  - < 0.1 : 自动过滤

- **category**: 来源类别
  - `official`: Anthropic官方
  - `community`: 社区开发

- **source**: 来源仓库
  - `anthropic-official`: 官方仓库
  - `username/repo`: GitHub用户仓库

## 搜索后的下一步

### 1. 查看搜索结果

系统会展示Top 10最相关的Skills，包含：
- Skill名称
- 相关度评分
- 简短描述
- GitHub URL

### 2. 自动快速评估

Top 3最相关的Skills会自动进行快速评估：

```
📊 快速评分：

1. csv-data-summarizer: 74/100 ✅ 建议安装
2. xlsx: 96/100 ✅ 建议安装
3. pdf: 97/100 ✅ 建议安装
```

### 3. 深度评估（可选）

如果你对某个Skill特别感兴趣，可以要求详细评估：

```
请详细评估第2个Skill
或
评估 xlsx Skill
```

系统会提供完整的六维评分报告和安装建议。

## 支持的搜索领域

当前关键词映射库支持以下领域：

### 数据与分析
- 数据分析、数据可视化、表格处理
- csv, excel, pandas, analytics

### 项目管理
- 项目管理、任务追踪
- project management, kanban, linear, jira

### 软件开发
- 代码审查、测试、调试
- 前端开发、后端开发
- code review, testing, tdd, frontend, backend

### 文档处理
- 文档、演示文稿、写作
- documentation, presentation, docx, pdf

### 安全
- 安全、加密
- security, vulnerability, crypto

### 研究
- 研究、学术
- research, academic, citation

### 设计
- 设计、艺术
- design, ui/ux, creative, art

### 自动化
- 自动化、集成
- automation, workflow, integration

## 高级搜索技巧

### 1. 精确匹配

使用引号包围关键词（在命令行中需要转义）：

```bash
python3 scripts/search_skills.py "project management"
```

### 2. 排除结果

目前不支持排除语法，但可以通过更具体的关键词来缩小范围。

### 3. 领域限定

在查询中加入领域关键词：

```
前端开发 React TypeScript
数据分析 Python pandas
项目管理 敏捷 Scrum
```

## 故障排除

### 问题1: 搜索返回结果太少

**解决方案**:
- 使用更通用的关键词
- 减少限定词
- 尝试英文查询

### 问题2: 搜索结果不相关

**解决方案**:
- 使用更具体的技术术语
- 组合多个关键词
- 查看关键词扩展是否准确

### 问题3: GitHub API限流

**错误**: `API rate limit exceeded`

**解决方案**:
- 等待一小时后重试
- 设置GitHub Personal Access Token（未实现）

### 问题4: 网络超时

**解决方案**:
- 检查网络连接
- 使用VPN（如需要）
- 增加超时时间（脚本中修改）

## 反馈与改进

如果你发现：
- 关键词映射不准确
- 搜索结果不相关
- 需要支持新的搜索领域

请更新 `scripts/search_skills.py` 中的 `KEYWORD_MAPPINGS` 字典。

## 总结

Skill搜索功能让你：
- ✅ 无需知道Skill名称即可查找
- ✅ 自动扩展关键词覆盖更多结果
- ✅ 优先展示高质量官方Skills
- ✅ 自动评估Top结果节省时间
- ✅ 支持中英文双语查询

从此，发现和评估Claude Skills变得更简单！🚀
