# chart-visualization

> 管理资产：`.ai/skills/chart-visualization/chart-visualization.md`；安装实体：`~/.agents/skills/chart-visualization/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/antvis/chart-visualization-skills |
| installed_ref | local-installed · 2026-08-22 |
| runtime | both |
| 调用入口 | `$chart-visualization` |
| 要求 | AntV API network access if generating preview images; final HyperFrames output must not depend on returned image URLs |
| 更新 | `npx skills update` / re-install source; review SKILL.md and security audit before update |
| 辅助脚本 | — |

## 用途

图表选择和数据关系表达参考。根据数据关系选择 line/bar/column/waterfall/dual-axes/scatter/radar/sankey 等类型，并把选择结果转成项目 `chart-spec`。

## 项目使用边界

- 只负责 chart grammar、数据字段和草图/规划。
- 事实、数字、来源和单位必须来自已验收 evidence；Skill 不补数据。
- 外部 AntV API 生成的图片只作为设计参考，不进入最终视频资产链。
- 最终渲染使用项目 `chart-registry.json` 和 HyperFrames inline SVG，保证确定性和跨公司复用。

## 已知限制

- 原生调用会 POST 到 `antv-studio.alipay.com` 生成图片；存在网络、外部 URL 和可复现性边界。
- 不支持项目自定义的所有图表语义；dumbbell/validation-dashboard 需要映射到项目 registry。
- 安装安全审计记录存在 Snyk Medium Risk，更新前必须重新审阅。
