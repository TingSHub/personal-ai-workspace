# impeccable

> 管理资产：`.ai/skills/impeccable/impeccable.md`；安装实体：`.claude/skills/impeccable/`（已安装，2026-08-19）

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | external · github: https://github.com/pbakaus/impeccable |
| installed_ref | v4.1.1（安装实体 SKILL.md 内 version；npm 包 3.6.0）· commit f88b2837a7d7c3182e46307bbbb091a1ed547571（2026-08-19 拉取并安装） |
| runtime | both |
| 调用入口 | 已安装：workspace 根执行 `npx impeccable install --providers=claude --scope=project --no-hooks`（未装 hook，纯命令调用）→ 会话内 `/impeccable init` 生成 PRODUCT.md / DESIGN.md → 之后 `/impeccable <command> <target>` 调用；`/impeccable pin <command>` 可生成独立命令 |
| 要求 | node + npx（CLI 与确定性检测必需）；init 生成的 PRODUCT.md / DESIGN.md 是后续命令读取的设计上下文；live 模式与部分命令需浏览器；hook 检测器未安装（`--no-hooks`） |
| 更新 | `npx impeccable update`（或 git 重拉取）；验证：对已知页面跑 `/impeccable audit`，确定性规则结果与版本一致 |
| 辅助脚本 | 无本地辅助脚本（skill 自带 scripts/ 位于安装实体 `.claude/skills/impeccable/scripts/`，含 context.mjs / detect.mjs / live-*.mjs 等） |
| 经验引用 | impeccable-detect-quality-gate |

## 作用

AI 前端设计质量 Skill：23 个设计命令（init / shape / critique / audit / polish / typeset / layout / colorize / animate / harden 等）+ 59 条确定性检测规则（无需 LLM、无需 API key）+ 浏览器实时迭代（live 模式）。让 AI 生成的前端界面摆脱模板感、达到生产级设计质量，并按 Persuade / Operate / Read / Experience 四种访客模式定位设计。

## 来源

- github · Apache 2.0（LICENSE 在仓库根）
- 从 Anthropic frontend-design 起点扩展；单 Skill 多命令结构

## 用途

- 任意 HTML 前端界面（landing / 仪表盘 / 产品 UI / 文档与长文阅读页）的设计、评审、审计与打磨：
  - `audit`：确定性技术质量检查（a11y / 性能 / 响应式），无 LLM 依赖，可独立作为视觉质量门禁
  - `critique`：UX 设计评审（层级 / 清晰度 / 情感共鸣）
  - `polish`：最终打磨与设计系统对齐（ship 前）
  - `typeset` / `layout`：字体、层级、间距、视觉节奏修复
  - `init` / `document`：设计上下文建立（PRODUCT.md / DESIGN.md）

## 注意事项与踩坑

- **与内容边界的关系**：impeccable 默认「Go all out / Dream big and bold」，但本项目（investagent-html-report 等）金融长文报告属 **Read 模式**，且受企业研究内容边界约束（措辞克制、无营销化、无目标价/买卖建议）——使用 audit/polish/typeset 等质量类命令时保留克制，不使用 bolder/overdrive 等激进增强命令；红涨绿跌等金融语义由项目规则覆盖。
- **hook 副作用**：`npx impeccable install` 会写入项目级 hook（PostToolUse 设计检测器），作用于安装目录的全部会话；建议在需要它的项目目录安装，而非 workspace 根。
- **live 模式依赖浏览器**；国内网络下 playwright/chromium 下载可能超时（与 investagent UZI 同问题）。
- 确定性检测（audit/detect）与 static-html-qa 维度互补：前者覆盖 a11y/对比度/间距节奏，后者覆盖 DOM 溢出/SVG 出界/数值一致性/内容边界；两者不可互相替代。
- **detect 实战阈值（经验: impeccable-detect-quality-gate）**：`npx impeccable detect <html>` 无 LLM 即可跑，实测 32 项中 low-contrast（4.5:1）、tiny-text（≥12px）、side-tab、layout-transition 最常命中——预防起点：meta/来源字号 12px、弱化文本对比度 ≥4.6:1、容器内动画用 clip-path；flat-type-hierarchy 类按「发现项人工裁决、不阻塞 PASS」处理并写入执行记录。

### 补充规则

- 2026-08-19：注册并安装外部 Skill（`npx impeccable install --no-hooks`，实体 `.claude/skills/impeccable/`，SKILL.md version 4.1.1）；investagent-html-report Phase 3/4 注记为可选资源。

### 补充规则

- 2026-08-19：真实项目验证（investagent-html-report Phase 4，贵州茅台 600519）——detect 32 项全部归零/裁决；阈值与预防起点见注意事项。
