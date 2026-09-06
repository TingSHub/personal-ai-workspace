# finance-content-engineering

> 管理资产：`.ai/skills/finance-content-engineering/finance-content-engineering.md`；安装实体：`.claude/skills/finance-content-engineering/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | internal · internal adaptation from huashu experiment（2026-08-15 测试提取方法重写为本地财经化版本，不复制 huashu 原 SKILL） |
| installed_ref | internal |
| runtime | both |
| 调用入口 | 选题模式输入 research-intelligence/ 或 research-summary/ → topic-options.md（先锁定 `content_line` 并绑定表达 Agent）；口播模式输入 draft-script.md → polished-script.md |
| 要求 | 输入研究资产必须来自已验收产物（research-materials/ → research-intelligence/），本 Skill 不自动搜索、不新增研究事实；重要数字必须可回指来源、时间范围与口径（fact-map 可信度分层） |
| 更新 | internal · 在 workspace 源码中评审修改并同步安装实体；方法迭代须以真实内容案例验证；验证：用一份已验收研究资产产出选题候选，用一份内容草稿产出口播稿，核对事实保真与 280 字/分语速 |
| 辅助脚本 | scripts/check-fact-drift.py（口播稿改写事实零漂移校验：新旧版本数字集合对比 + 近似词对比式检测 + 中文读法核验，改写后必跑） |
| 经验引用 | huashu-test；notes-spoken-polish |

## 作用

为财经研究内容提供：选题设计辅助（topic-gen）、统一口播脚本工程化处理（script-polish）、内容表达优化。统一口播入口内部吸收听觉理解、真实双人承接、概念命名意识、适度幽默和 AI 腔清理。不是研究 Agent、投资分析 Agent、Content Director Agent。

## 来源

- internal（workspace 自建，2026-08-15；internal adaptation from huashu experiment）
- 安装位置：`.claude/skills/finance-content-engineering/`（workspace 内，所有项目可见；可加载定义见安装实体）
- 方法提取自 huashu-topic-gen（选题）与 huashu-script-polish（三遍审校），财经化重写；不复制 huashu 原 SKILL（无明确 LICENSE、面向泛内容）

## 用途

- **topic-gen**：输入 `research-intelligence/`（或 `research-summary/`）→ 输出 `topic-options.md`（按 `content_line` 路由、角度互斥、含支撑事实与风险提示，并绑定后续表达 Agent）
- **script-polish**：输入 `draft-script.md` → 输出 `polished-script.md`（280 字/分口播稿 + 停顿/重音/数字朗读建议）

## 注意事项与踩坑

- 输入研究资产必须来自已验收产物（research-materials/ → research-intelligence/），不自动搜索、不新增研究事实。
- 财经化规则：事实约束（重要数字必须来源 + 时间范围 + 口径）、投资纪律（反标题党/反绝对化/反荐股，保留 Bull Case / Bear Case / 不确定性）、口播规则（280 字/分、单句宜 ≤25 字、大数读法、术语不失准）。
- 口语表达统一入口：本 Skill 内部依次处理听觉理解、对话连续性、概念命名机会、适度幽默和 AI 腔清理；调用方不再逐个调度拆分的表达 Skill。真实 speaker、角色比例和回合关系由 `dialogue-director-agent` 负责。
- 三遍审校：Review 1 事实检查 → Review 2 表达检查 → Review 3 传播检查。
- 不代替 Content Director：只输出资产（topic-options / polished-script），不做内容决策。
- 应用于 speaker script、notes 或 narration 时，改写只能做表达层调整；不得新增、删除、近似化事实或改变结论强度。改写后必须运行 `scripts/check-fact-drift.py`。
- `polished-script.md` 被下游锁定后，字幕和 TTS 只能从锁定文本派生；需要改变核心观点或事实时，退回内容导演/编辑阶段。

### 补充规则

- script-polish 应用于 speaker script/notes 时：百分比直读（「营收负 1.2%」→「营收下降 1.2%」）、大数读法、单句 ≤25 字；**数字转中文读法允许（70→七十、两百/两千 用「两」、年份→去年/今年），近似化禁止（36.1% 不得写「超过三分之一」）**。
- 改写后必跑 `scripts/check-fact-drift.py <旧版> <新版>`：removed 须为读法/指代、added 不允许、近似词对比式检测（约/左右/大概 等价组替换允许）。
