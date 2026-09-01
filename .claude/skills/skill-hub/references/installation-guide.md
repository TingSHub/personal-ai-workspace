# Skill 安装指南

## 三种安装方式

### 方式 1：从 GitHub 直接安装（推荐）

适用于：Skill 托管在 GitHub 上

```bash
# 步骤 1：克隆仓库到临时目录
cd ~/Downloads
git clone <github_repo_url> temp-skill

# 步骤 2：复制到 Claude Skills 目录
cp -r temp-skill ~/.claude/skills/<skill-name>

# 步骤 3：清理临时文件
rm -rf temp-skill

# 步骤 4：重启 Claude Code
# 按 Cmd+Q 退出，然后重新启动
```

**示例**：
```bash
cd ~/Downloads
git clone https://github.com/user/awesome-skill awesome-skill
cp -r awesome-skill ~/.claude/skills/awesome-skill
rm -rf awesome-skill
```

---

### 方式 2：从 .skill 文件安装

适用于：获得了打包的 .skill 文件

```bash
# 步骤 1：下载 .skill 文件（如果是 URL）
curl -L <skill_url> -o ~/Downloads/skill-name.skill

# 步骤 2：解压到 Skills 目录
unzip ~/Downloads/skill-name.skill -d ~/.claude/skills/

# 步骤 3：重启 Claude Code
```

**注意**：.skill 文件实际上是 ZIP 格式，解压后会自动创建对应的文件夹。

---

### 方式 3：从本地文件夹安装

适用于：已经在本地开发或下载的 Skill

```bash
# 直接复制到 Skills 目录
cp -r /path/to/local-skill ~/.claude/skills/skill-name

# 重启 Claude Code
```

---

## 验证安装

安装完成后，可以通过以下方式验证：

1. **检查文件是否存在**：
   ```bash
   ls ~/.claude/skills/<skill-name>/SKILL.md
   ```

2. **查看 Claude 是否识别**：
   - 重启 Claude Code 后，发送消息："你有哪些 skills"
   - 或者直接尝试触发该 Skill 的功能

---

## 常见问题

### Q1: 安装后 Claude 没有识别到 Skill？

**解决方案**：
1. 确认文件夹名称与 SKILL.md 中的 `name` 字段一致
2. 检查 `~/.claude/skills/` 目录权限
3. 完全退出 Claude Code（Cmd+Q），而非只是关闭窗口
4. 重新启动 Claude Code

### Q2: 如何卸载 Skill？

```bash
# 删除 Skill 目录
rm -rf ~/.claude/skills/<skill-name>

# 重启 Claude Code
```

### Q3: 如何更新 Skill？

```bash
# 方法 1：重新安装（覆盖）
cp -r /path/to/updated-skill ~/.claude/skills/skill-name

# 方法 2：使用 git pull（如果是从 GitHub 克隆的）
cd ~/.claude/skills/skill-name
git pull

# 重启 Claude Code
```

---

## 安全提醒

- ⚠️ 只安装来自可信来源的 Skills
- ⚠️ 安装前使用 safe-skill-copy Skill 进行安全评估
- ⚠️ 检查 SKILL.md 中的 `allowed-tools` 字段，了解 Skill 需要的权限
- ⚠️ 阅读 scripts/ 目录中的脚本内容，确保无恶意代码
