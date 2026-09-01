# information-visualization-architect

> 管理资产：`.ai/agents/information-visualization-architect/information-visualization-architect.md`；安装实体：`.agents/information-visualization-architect.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · workspace internal agent profile |
| installed_ref | — |
| runtime | both |
| 调用入口 | 由 research-content-direction Phase 3 调用；输入 content-assets/，输出 content-assets/visual-plan/ |
| 要求 | 已验收的 content-assets/（content-thesis + narrative-plan + visual-brief）；执行层 dataviz（图表规范）+ lieflat-charts/antvis（图表生产）+ hyperframes（HTML/Web 视频） |
| 更新 | internal · 只调整本地 Agent 调用说明、工作流与输出契约；不得复制外部 Skill 内容或伪造未执行资源；验证：用一份已验收 content-thesis/ 产出 visual-plan 四件套，核对图表数字回指 fact-map 且禁用项零出现 |
| 辅助脚本 | scripts/check_ev_refs.py（visual-brief EV 引用 ↔ evidence-reference 可解析性检查，输入前/输出后运行） |
| 经验引用 | — |

## 作用

视觉叙事决策角色：回答「内容应该如何被观众看到」。将 content-assets/ 内容观点方案转化为视觉叙事方案（scene-plan / chart-spec / asset-requirements / style-guide）。**不是执行者**——不实际编码、不渲染、不制作视觉资产。

## 实体位置（可加载定义）

- `.agents/information-visualization-architect.md`——完整职责（定位/输入/工作流/输出契约/财经补位纪律/边界/验收）

## 调用方式

- 输入（v0.2 明确化）：`content-assets/`（content-thesis.md + **visual-brief.md** + **evidence-reference.md**——视觉需求从 visual-brief 显式读取，不再从 content-thesis 隐式提取；visual-brief 缺失时显式报告请求补齐）
- 输出：`content-assets/visual-plan/`（scene-plan / chart-spec / asset-requirements / style-guide）

## 注意事项与踩坑

- 方法骨架：visual-storytelling-design（2026-08-15 茅台案例实测：四路径菜单/Step-by-Step Arc/六图形模式/注解清单/诚实原则有效）——提取骨架重写，不安装原 skill；Scrollytelling 对图文/视频形态价值低，降级使用。
- 财经补位（自建，外部方法均缺失）：可信度视觉系统（估算=虚线+角标+脚注）、A 股语义色（红涨绿跌）、合规边界（目标价不醒目呈现、不误导）、中文排版 + tabular 数字。
- 图表数据只回指 fact-map 可信度分层：必用/慎用（标注口径）可用，禁用项（PEG/失真分位/已证伪记忆/代理数据/未落地政策）绝不使用。
- 分层补位：叙事注解层=本 Agent 方法，图表规范=dataviz，视觉语法=lieflat-charts（PolyForm 非商业许可，个人使用 OK），合规审校=finance-content-engineering 注入。
- 视觉方案不改变研究事实；不做投资判断；输出四件套后由执行层（dataviz/lieflat/hyperframes/omc designer）落地，本 Agent 不越界代做。
- **输入约束（v0.2.1）**：禁止重新读取原始 research-materials/，禁止自行补充事实；发现 visual-brief 引用不存在必须反馈问题，不占位猜测。
