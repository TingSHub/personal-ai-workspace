# infographic-creator

> 管理资产：`.ai/skills/infographic-creator/infographic-creator.md`；安装实体：`~/.agents/skills/infographic-creator/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/antvis/chart-visualization-skills |
| installed_ref | local-installed · 2026-08-22 |
| runtime | both |
| 调用入口 | `$infographic-creator` |
| 要求 | AntV Infographic syntax knowledge; optional network/CDN for preview only |
| 更新 | `npx skills update` / re-install source; review SKILL.md and security audit before update |
| 辅助脚本 | — |

## 用途

把复杂信息压缩成比较、序列、层级、关系、流程和图表结构，帮助信息可视化规划层选择模板。

## 项目使用边界

- 只输出结构参考和 chart-spec/infographic-spec，不替代研究编辑或事实核验。
- 参考其 compare、sequence、relation、chart 模板；最终画面由 HyperFrames 项目组件重绘。
- 不把 AntV CDN、返回图片 URL 或第三方 HTML 作为最终 Composition 依赖。

## 已知限制

- 原生 Infographic 运行需要 AntV CDN/运行时，不满足本项目的确定性离线渲染要求。
- 模板表达适合规划复杂关系，但视频中仍需控制信息密度和中文排版。
- 安装安全审计记录存在 Snyk Medium Risk，更新前必须重新审阅。
