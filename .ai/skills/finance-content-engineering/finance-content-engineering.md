# finance-content-engineering

> 管理资产：`.ai/skills/finance-content-engineering/finance-content-engineering.md`；安装实体：`.claude/skills/finance-content-engineering/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | internal · internal adaptation from huashu experiment（2026-08-15 测试提取方法重写为本地财经化版本，不复制 huashu 原 SKILL） |
| installed_ref | internal |
| runtime | both |
| 调用入口 | 选题模式输入 research-intelligence/ 或 research-summary/ → topic-options.md；口播模式输入 draft-script.md → polished-script.md |
| 要求 | 输入研究资产必须来自已验收产物（research-materials/ → research-intelligence/），本 Skill 不自动搜索、不新增研究事实；重要数字必须可回指来源、时间范围与口径（fact-map 可信度分层） |
| 更新 | internal · 在 workspace 源码中评审修改并同步安装实体；方法迭代须以真实内容案例验证；验证：用一份已验收研究资产产出选题候选，用一份内容草稿产出口播稿，核对事实保真与 280 字/分语速 |
| 辅助脚本 | scripts/check-fact-drift.py（口播稿改写事实零漂移校验：新旧版本数字集合对比 + 近似词对比式检测 + 中文读法核验，改写后必跑） |
| 经验引用 | huashu-test；notes-spoken-polish |

## 作用

为财经研究内容提供：选题设计辅助（topic-gen）、口播脚本工程化处理（script-polish）、内容表达优化。不是研究 Agent、投资分析 Agent、Content Director Agent。

## 来源

- internal（workspace 自建，2026-08-15；internal adaptation from huashu experiment）
- 安装位置：`.claude/skills/finance-content-engineering/`（workspace 内，所有项目可见；可加载定义见安装实体）
- 方法提取自 huashu-topic-gen（选题）与 huashu-script-polish（三遍审校），财经化重写；不复制 huashu 原 SKILL（无明确 LICENSE、面向泛内容）

## 用途

- **topic-gen**：输入 `research-intelligence/`（或 `research-summary/`）→ 输出 `topic-options.md`（3-4 个角度互斥的选题候选，含支撑事实与风险提示）
- **script-polish**：输入 `draft-script.md` → 输出 `polished-script.md`（280 字/分口播稿 + 停顿/重音/数字朗读建议）

## 注意事项与踩坑

- 输入研究资产必须来自已验收产物（research-materials/ → research-intelligence/），不自动搜索、不新增研究事实。
- 财经化规则：事实约束（重要数字必须来源 + 时间范围 + 口径）、投资纪律（反标题党/反绝对化/反荐股，保留 Bull Case / Bear Case / 不确定性）、口播规则（280 字/分、单句宜 ≤25 字、大数读法、术语不失准）。
- 三遍审校：Review 1 事实检查 → Review 2 表达检查 → Review 3 传播检查。
- 不代替 Content Director：只输出资产（topic-options / polished-script），不做内容决策。

## 回写条目（来源: huashu-test）

本 Skill 即为 huashu 实测结论的产物（方法财经化重写）；`skill.yaml` 的 `experience_refs` 引用已归档经验 `huashu-test`。


## 回写条目（来源: notes-spoken-polish）

- script-polish 应用于 speaker script/notes 时：百分比直读（「营收负 1.2%」→「营收下降 1.2%」）、大数读法、单句 ≤25 字；**数字转中文读法允许（70→七十、两百/两千 用「两」、年份→去年/今年），近似化禁止（36.1% 不得写「超过三分之一」）**。
- 改写后必跑 `scripts/check-fact-drift.py <旧版> <新版>`：removed 须为读法/指代、added 不允许、近似词对比式检测（约/左右/大概 等价组替换允许）。
