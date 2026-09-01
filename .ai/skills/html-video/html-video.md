# html-video

> 管理资产：`.ai/skills/html-video/html-video.md`；安装实体：`.claude/skills/html-video/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/nexu-io/html-video |
| installed_ref | c414ecc |
| runtime | both |
| 调用入口 | pnpm install + 本地 Studio（127.0.0.1:3071，HTTP API 可 curl 驱动）；agent 后端支持 claude CLI 或 Anthropic 兼容端点 |
| 要求 | Node 20+ / pnpm 9；FFmpeg、playwright chromium；编码 agent 后端（claude CLI 或 DEEPSEEK Anthropic 兼容端点已实测）；network（onnxruntime postinstall 首次下载 ~190MB） |
| 更新 | git · 拉取上游新版本到临时目录审查（README、CLAUDE.md 已知问题、workflow 变更）后更新 vendor；保留本资源说明；验证：studio 跑通一条 10 秒中文帧渲染 + MP4 导出 |
| 辅助脚本 | — |
| 经验引用 | — |

## 作用

完整编排项目：编码 agent 把 素材/脚本 → content-graph 分镜 → 逐帧 HTML → Hyperframes 引擎录制 → MP4 全自动跑通。本实验 84.93s/1080p60 两版 MP4 均产出，v2 restyle 一次生效（换设计语言数据零改动）。

## 调用

- 安装：pnpm install（首次 13m18s，onnxruntime postinstall ~190MB 是卡点）+ build
- 启动：本地 Studio（127.0.0.1:3071，HTTP API 可 curl 驱动）；工作流 = prompt/素材 → agent loop（content-graph storyboard + 逐帧 HTML）→ 渲染
- agent 后端：PATH 上 `claude --print`（产品原生）或 DEEPSEEK_API_KEY 走 Anthropic 兼容端点（api.deepseek.com/anthropic，已 smoke test 通过）；**不支持 OpenAI 兼容端点**
- 生成后迭代：restyle 卡（保留文案换风格）/ iterate-content / iterate-format
- 本实验参考实现：`projects/investment-research-system/experiments/listed-company-video-production/outputs/web/html-video/`（content-graph.json、帧 HTML、MP4、驱动脚本 hv-driver.mjs）

## 调用注意事项

- 推荐输入：脚本 + 数据引用表（agent 会自动 grounding，实测零外推）+ 风格描述
- 旁白混音需手工：studio 音频只接 MiniMax，外部 TTS 音频用 ffmpeg 手工合成（本实验产出 with-narration 版）
- 分镜结构要人工把关：请求 5 帧它可能自决压成 4 帧（40s 尾帧合并两幕且动画只覆盖前 8s）
- 编码 agent 用 claude CLI 时偶发挂起（产品 CLAUDE.md 自述已知缺陷），kill 重试

## 常见失败原因

- **意图路由关键字劫持**：反馈文本中"叙事节奏"命中格式路由正则（节奏→时长）被导向格式卡而非风格卡——需状态机绕行（提交同值格式→confirm→"换风格"→style 卡→反馈→restyle）；反馈时避免使用产品路由关键字
- 模板清除（templateId→null）走 API 会崩（templates.get(null)），需编辑项目 JSON
- 相对路径 404 / .html-video 目录误建（README 已知问题，实跑全部吻合）
- 尾帧 tpad 冻结：Scene 过多或过长时动画只覆盖开头

## 最佳实践

- 把它当"快速全链路原型机"：验证形态可行性一天内出片；正式生产链路用它确认视觉方向后回 HyperFrames/Remotion 精修
- restyle 路径保留文案与数据（逐字保留约束），适合做视觉 A/B
- DeepSeek Anthropic 兼容端点免 OpenAI key，国内环境可直接用
