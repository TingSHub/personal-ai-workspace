# Account Cover Reference（封面参考资产）

账本两面账户的**平台封面固定参考**（by-name：`account-cover-reference`）。所有后续视频封面按此风格生成；再创作的边界见 `account-profile/design.md`「平台封面规范」小节。

## 文件

| 文件 | 说明 |
|---|---|
| `cover-template.html` | 封面模板（完整可编辑：文字可点击编辑、「替换当前背景」可换图、「保存当前HTML」导出）。演示内容为 2026-09-05 数据基础设施案例；正文文字会被下一期 `episode-input.json` 的 `cover.*` 字段替换 |
| `assets/background-portrait.png` | 竖版 3:4 米白羊皮纸账本摄影背景 |
| `assets/background-landscape.png` | 横版 4:3 同风格背景 |
| `reference-3x4.png` | 官方参考效果图（1086×1448，风格事实源：比例、字重、排版节奏以此为准） |

> 注：仓库 `.gitignore` 全局排除 `**/*.png`（与 `account/` 下 logo/背景媒体一致的媒体治理策略），三张 PNG 为本机资产不入库；模板所指相对路径在使用时随 `assets/` 一并复制到 `podcast/project/`。风格记录以 design.md 规范文本为主。如后续需要跨机克隆可用，可考虑把背景翻转为 SVG 或单独放宽忽略规则（需单独决策）。

## 使用方式（下一期）

1. 按 workflow 生成/在 `account-profile/cover-reference/` 基础上创建 `podcast/project/cover.html`：复制模板 + `assets/`（字体 `assets/fonts/NotoSerifSC-{Regular,Bold}.otf` 取自 `font.noto-serif-sc` 资源）。
2. 用 `episode-input.json` 的 `cover.subject_label` / `cover.large_text` / `cover.subtitle` 替换演示文字；保留 `.headline` 两行结构与行尾标点 `.qm` 包裹（见 design.md）。
3. 渲染：`scripts/render_cover_4x3.js` 导出 4:3 `cover.png`（1440×1080）、`scripts/render_cover_3x4.js` 导出 3:4 `cover-3x4.png`（1080×1440）。
4. 验收：尺寸必须匹配；标题墨迹中心与画布中心偏差 ≤3px；视觉对齐 `reference-3x4.png`。

## 边界

- 允许的创意变体：同风格背景摄影替代、纸章/imprint 微调、大字关键词化、模板内 token 不变的重设计。
- 禁止：亮红/黄色投流海报风、纯色铺底、无语义几何装饰、反色 Logo、日期/免责声明/研究编号等不可读信息层。
- 2026-09-05 落地（closeout，来自数据基础设施封面任务，含「？」字身/墨迹差 `.qm` 补偿与加粗合成修正）。
