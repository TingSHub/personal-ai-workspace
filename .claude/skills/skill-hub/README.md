# 🔍 Skill Hub v3.0

**Skill全链路助手：从搜索到安装到学习的完整解决方案**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Claude Skills](https://img.shields.io/badge/Claude-Skills-purple.svg)](https://github.com/anthropics/skills)

> 一个帮助Claude用户发现、评估、安装和学习构建Skills的完整工具链

---

## ✨ 核心功能

### 🔍 智能搜索
- **三层搜索源**：
  - Anthropic官方Skills（16个高质量）
  - ComposioHQ/awesome-claude-skills（160+精选社区）
  - GitHub全平台搜索（社区开源Skills，**理论上无限**）
- 中英文双语支持
- 自动关键词扩展
- 相关度智能排序（最多返回200+结果）

### ✅ 安全评估
- **六维评分模型**（总分100分）
  - 来源可信度（25分）
  - 社区热度（20分）
  - 任务明确性（20分）
  - 可复用性（15分）
  - 安全性（10分）
  - 跨平台兼容（10分）
- 自动评估Top 3搜索结果
- 详细的安全建议

### 📦 一键安装
- 直接从GitHub URL安装
- 自动验证SKILL.md格式
- 失败自动回滚
- 支持本地路径安装

### 🛠️ 构建指导
- 分析现有Skill的架构模式
- 提取可复用的实现技巧
- 生成7个维度的构建指南
- 推荐相似的参考示例

---

## 🚀 快速开始

### 安装

1. **克隆仓库到Claude skills目录**
```bash
cd ~/.claude/skills
git clone https://github.com/wanghui2323/skill-hub.git
```

2. **重启Claude Code**

就这么简单！skill-hub会自动激活。

### 使用示例

#### 场景1：搜索Skills

```
User: "我需要一个数据分析的Skill"

Claude会：
1. 搜索三层数据源（官方+精选+GitHub全平台）
2. 返回Top 10相关结果（从200+候选中筛选）
3. 自动评估Top 3
4. 提供三个选择：安装/详细评估/学习构建
```

#### 场景2：评估Skill安全性

```
User: "帮我评估这个Skill https://github.com/xxx/skill-name"

Claude会：
1. 获取SKILL.md和scripts内容
2. 进行六维评分
3. 给出安全建议（✅建议安装 / ⚠️谨慎安装 / ❌不建议安装）
```

#### 场景3：一键安装

```
User: "安装xlsx这个Skill"

Claude会：
1. 确认安装信息
2. 从GitHub克隆到~/.claude/skills/
3. 验证SKILL.md有效性
4. 提示重启Claude Code
```

#### 场景4：学习构建

```
User: "教我怎么构建类似xlsx的Skill"

Claude会：
1. 分析xlsx的架构模式
2. 提取关键组件和技术
3. 生成实现步骤指南
4. 推荐参考示例
```

---

## 📊 功能对比

| 传统方式 | skill-hub |
|---------|----------------|
| ❌ 手动在GitHub搜索 | ✅ 三层智能搜索（官方+社区+全平台）|
| ❌ 不知道质量好坏 | ✅ 六维安全评分 |
| ❌ 手动git clone和复制 | ✅ 一键自动安装 |
| ❌ 不知道如何构建 | ✅ 构建指导系统 |
| ⏰ 耗时2-3小时 | ⚡ 5分钟完成 |

---

## 🎯 使用场景

### 适合谁？

- ✅ **Skill重度用户** - 经常需要寻找和安装新Skills
- ✅ **Skill开发者** - 想学习如何构建高质量Skills
- ✅ **追求效率的用户** - 希望快速完成Skill的发现和安装
- ✅ **安全敏感用户** - 需要评估Skill安全性

### 不适合谁？

- ❌ 只使用官方Skills的用户（功能过剩）
- ❌ 不熟悉命令行的用户（需要Python环境）

---

## 📖 详细文档

### 核心文件

- **[SKILL.md](SKILL.md)** - 完整的使用指南和workflows
- **[workflow-details.md](references/workflow-details.md)** - Workflow C/D的详细实现
- **[scoring-criteria.md](references/scoring-criteria.md)** - 六维评分标准
- **[installation-guide.md](references/installation-guide.md)** - Skills安装指南

### Scripts说明

| Script | 功能 | 用法 |
|--------|------|------|
| `search_skills.py` | 搜索Skills | `python3 scripts/search_skills.py "数据分析"` |
| `fetch_skill.py` | 获取Skill内容 | `python3 scripts/fetch_skill.py <url>` |
| `install_skill.py` | 安装Skill | `python3 scripts/install_skill.py <url>` |
| `analyze_skill_patterns.py` | 分析构建模式 | `python3 scripts/analyze_skill_patterns.py <url>` |

---

## 🔧 技术栈

- **Python 3.6+** - 核心脚本语言
- **标准库** - urllib, json, pathlib（无第三方依赖）
- **Git** - 用于克隆Skills仓库
- **Claude Code** - 运行环境

---

## 📈 数据统计

### Skills数据源（三层架构）

| 层级 | 来源 | 数量 | 特点 |
|------|------|------|------|
| **L1: 官方层** | Anthropic官方 | 16个 | 最高质量，官方维护 |
| **L2: 精选层** | awesome-claude-skills | 160+个 | 社区验证，39K⭐ |
| **L3: 开放层** | GitHub全平台搜索 | 理论无限 | 实时搜索，最多返回200个 |

**搜索策略**：优先展示L1和L2，L3补充长尾需求

### 评分分布（100个精选）

- 90+分：3个（3%）
- 85-89分：10个（10%）
- 80-84分：87个（87%）

### 领域覆盖

- 📋 应用自动化：78个（48.8%）
- 💻 开发工具：24个（15.0%）
- 📊 数据处理：12个（7.5%）
- 📝 文档处理：10个（6.3%）
- 其他：36个（22.4%）

---

## 🤝 贡献指南

欢迎贡献！以下是几种参与方式：

1. **报告Bug** - 提交Issue描述问题
2. **功能建议** - 分享您的想法
3. **代码贡献** - 提交Pull Request
4. **文档改进** - 帮助完善文档
5. **分享Skills** - 推荐优质Skills

### 贡献流程

```bash
# 1. Fork本仓库
# 2. 创建特性分支
git checkout -b feature/your-feature

# 3. 提交更改
git commit -m "Add: your feature description"

# 4. 推送到分支
git push origin feature/your-feature

# 5. 创建Pull Request
```

---

## 📝 更新日志

### v3.0 (2026-03-02) - Major Update

**新增功能**：
- ✅ 直接安装功能（install_skill.py）
- ✅ 构建指导系统（analyze_skill_patterns.py）
- ✅ awesome-claude-skills数据源集成（160+ Skills）
- ✅ 职业推荐系统（10大职业 × 100个精选Skills）

**优化**：
- ✅ SKILL.md精简37%（533→336行）
- ✅ Description优化26%（163→120字）
- ✅ 采用Progressive Disclosure设计模式
- ✅ 修复fetch_skill.py的URL解析bug

**文档**：
- ✅ 新增workflow-details.md（295行）
- ✅ 新增真实使用案例
- ✅ 完整的开源文档

详见 [CHANGELOG.md](CHANGELOG.md)

---

## 📜 开源协议

本项目采用 [MIT License](LICENSE) 开源。

您可以自由地：
- ✅ 使用
- ✅ 复制
- ✅ 修改
- ✅ 合并
- ✅ 发布
- ✅ 分发
- ✅ 再授权
- ✅ 出售

唯一要求：保留原作者的版权声明。

---

## 🙏 致谢

- [Anthropic](https://www.anthropic.com/) - Claude和官方Skills
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) - 社区精选Skills列表
- 所有贡献者和使用者

---

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/wanghui2323/skill-hub/issues)
- **Discussions**: [GitHub Discussions](https://github.com/wanghui2323/skill-hub/discussions)
- **Email**: 645447086@qq.com

---

## 🌟 Star History

如果这个项目对您有帮助，请给我们一个⭐Star！

[![Star History Chart](https://api.star-history.com/svg?repos=wanghui2323/skill-hub&type=Date)](https://star-history.com/#wanghui2323/skill-hub&Date)

---

**让Skills的发现、使用、创造变得简单！**

Made with ❤️ by 汪辉
