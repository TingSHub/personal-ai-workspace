# Project scripts

本目录保存项目产物工具和历史实验。可跨项目复用的选题信号扫描已沉淀为 topic-forward-signal-scanner，音频生产入口由 podcast-audio-compiler 管理。具体步骤与参数以当前 Workflow 为准；本说明提供导航，不把目录中每个脚本都视为生产入口。

选题工具：

- `build-topic-candidates.py`：读取可选 `signals.json`，并可通过 `--leads` 接收按 `topic-forward-candidate` 模板填写、有来源的事件、产品、行业、观众问题或比较线索，输出 `candidate-pool.json`。行情种子的观众问题和 `content_line` 保持为空，交 `topic-angle-router-agent` 在轻量核验后形成；脚本不把价格变化自动解释成财务问题。
- `check-topic-angle-routing.py`：读取含 `cards` 的 `topic-forward.json`，校验 `content_line`、`expression_agent`、`expression_mode` 的固定映射及最低问题字段；只用于 topic card 进入研究前的结构门禁。

批准卡随后交给 topic-research；上述选题工具不负责研究或审批。

## 内容编译与检查

| 入口 | 用途与依据 |
|---|---|
| `build_podcast_episode.py` | 从模板输入编译 episode；支持 `--input` 与 `--run-root`，最小合成案例见 `../tests/test_build_podcast_episode.py` |
| `build_podcast_opening_test.py` | 提取开场输入；由同一编译测试覆盖，不等于完成开场配音试听 |
| `check_content_collaboration.py` | 协作稿结构与阶段检查；见对应 test_check_content_collaboration 测试 |
| `check_editorial_gate.py` | 研究/表达交接门禁；见对应 test_check_editorial_gate 测试 |
| `check_podcast_dialogue.py` | 对白契约与数字双文本检查；见对应 test_check_podcast_dialogue 测试 |

## 画面与验收

| 入口 | 用途与限制 |
|---|---|
| `build_podcast_composition.py` | 生成 HyperFrames Composition，须提供完整 scene manifest；账号素材与字体可由 `--account-media-dir`、`--font-dir` 指定。结尾标题有本地测试，完整渲染仍需执行 SOP 验收 |
| `check_podcast_visual_sync.py` | investagent-video-execution 引用的场景/真实音频/图表同步检查；有本地合成测试 |
| `check_mobile_legibility.py` | investagent-video-execution 引用的 HTML 可读性静态检查；不能替代手机缩小截图与人工观看 |

## 实验及其他辅助工具

`test-doubao-*`、`generate-doubao-*`、`build_cosyvoice_ab_manifests.py` 等用于音色或后端实验；当前生产后端由 investagent-video-execution 指定，不能因为脚本存在就切换后端。`make_feilong_episode.py` 等主题专用脚本不作为通用启动入口。

其他字幕、对齐、封面和旧构图脚本保留供具体任务使用；本次未逐一验证其生产适用性。调用前检查实际代码、输入路径与副作用，并确认是否适用于当前 SOP，不直接批量运行实验脚本。

## 本地复跑

从工作区根目录运行项目 README 中的 unittest 命令。2026-09-11 已验证 49 项测试通过；测试构造临时输入，覆盖编译和检查行为，不调用真实研究、TTS、渲染或发布服务。可复用案例与完整生产验收边界见项目 README。
