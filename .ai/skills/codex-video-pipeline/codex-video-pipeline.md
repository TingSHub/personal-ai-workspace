# codex-video-pipeline

> 管理资产：`.ai/skills/codex-video-pipeline/codex-video-pipeline.md`；安装实体：`.claude/skills/codex-video-pipeline/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/zoglmk/codex-video-pipeline |
| installed_ref | aab79717ad692dd0b4d770778be28a2fa2b09a6e |
| runtime | codex |
| 调用入口 | $codex-video-pipeline |
| 要求 | Python 3.10+；FFmpeg 与 ffprobe；HyperFrames（默认成片渲染引擎）；network（联网研究或使用 Pexels 时）；PEXELS_API_KEY（仅在选择 Pexels 真实素材时）；最终旁白音频与可输出时间戳 JSON 的声学字幕提供方；Codex imagegen 或其他已配置图像生成能力 |
| 更新 | reinstall · 将上游 revision 获取到临时目录，审查 SKILL.md、references、scripts、tests、依赖和 LICENSE 后，使用 skill-installer 替换 .claude/skills/codex-video-pipeline；保留本地资源记录；验证：编译全部 Python 脚本，运行 unittest，执行 setup.py doctor --json，并确认 Claude/Codex 两条路径解析到同一实体 |
| 辅助脚本 | scripts/setup.py（只读检查生产环境，或创建不含密钥的提供方配置）；scripts/project.py（初始化视频项目并验证最终视频、封面、字幕凭据和发布包）；scripts/caption_gate.py（为最终旁白与声学字幕生成哈希凭据并在发布前复核）；scripts/pexels_video.py（按需检索和下载 Pexels 视频并保留来源与文件指纹）；scripts/package_outputs.py（将视频、横竖封面和发布文案复制为规范发布包）；scripts/example.py（初始化内置 AI 会议记录示例项目） |
| 经验引用 | — |

## 作用

把视频任务推进为完整产品交付：研究、脚本、动态叙事、素材、旁白、声学字幕、HyperFrames 渲染、质量检查、横竖封面和发布包。安装实体来自 `zoglmk/codex-video-pipeline`。

## 调用

- Skill 入口：`$codex-video-pipeline`
- 只读环境检查：`python3 .claude/skills/codex-video-pipeline/scripts/setup.py doctor --json`
- 首次配置：`python3 .claude/skills/codex-video-pipeline/scripts/setup.py configure --recommended`
- 示例初始化：`python3 .claude/skills/codex-video-pipeline/scripts/example.py --root videos`
- 项目终验：`python3 .claude/skills/codex-video-pipeline/scripts/project.py verify --project <项目目录> --json`

## 调用边界与注意事项

- 首次调用必须完整读取安装实体的 `SKILL.md`，并按任务读取 `references/first-run.md`、`project-contract.md`、`research-and-script.md`、`captions.md`、`quality-gates.md` 和 `cover-system.md`。
- `setup.py doctor` 是只读检查；`configure` 会写入用户目录 `~/.config/codex-video-pipeline/config.json`，运行前核对目标。配置不保存密钥。
- HyperFrames 是默认成片渲染依赖。缺失时先按 Codex 插件机制安装，不由本 Skill 自动安装系统软件或包。
- Pexels 是可选真实素材来源；`pexels_video.py` 会联网和下载文件，必须有 `PEXELS_API_KEY`，并保留素材页、创作者、许可和文件指纹。
- 正式字幕必须来自成片实际使用的最终旁白音频；按字数估时只能用于预览。发布前必须通过字幕凭据和项目终验。
- 图片由 Codex 原生 `imagegen` 或已配置的图像能力生成；关键中文使用 HyperFrames、HTML/CSS 或 SVG 确定性排版，不交给图片模型。
- 不把可下载等同于可商用；系统软件安装、付费 API、批量下载和外部发布仍遵守用户授权边界。
- `.codex/skills/codex-video-pipeline` 由 `.codex/skills -> ../.claude/skills` 的目录级映射自动提供，禁止创建逐 Skill 二级链接。

## 更新与验证

更新时锁定上游 commit，先下载到 `/tmp` 审查入口、references、全部脚本、测试、依赖和 MIT LICENSE，再替换安装实体。更新后运行 Python 语法编译、上游 unittest、只读 doctor，并确认 `.claude/skills/codex-video-pipeline` 与 `.codex/skills/codex-video-pipeline` 解析到同一目录。
