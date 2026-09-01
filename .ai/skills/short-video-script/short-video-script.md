# short-video-script

> 外部参考资源：GitHub `jiner0330/short-video-script`

## 元数据

| 字段 | 值 |
|---|---|
| name | short-video-script |
| kind | skill |
| description | 短视频口播脚本方法论：六种结构、情绪曲线和逐段检查清单 |
| source | github: https://github.com/jiner0330/short-video-script |
| installed_ref | `61c2a0f759cb9ccf50620fe8fe854ff5a2fd5c91` |
| runtime | claude / codex（参考，不作为视频渲染运行时） |
| invocation | Phase 2 读取六种结构、情绪曲线和逐段检查清单；不把短视频时长限制带入长篇播客 |
| requirements | 无运行时依赖；上游仓库 MIT |
| update | manual：重新读取 GitHub 固定 commit；verify：检查结构、情绪曲线和合规边界是否变化 |
| scripts | 无本地辅助脚本 |
| experience_refs | 无 |

## 调用说明

### 可复用部分

- 情绪曲线优先走“好奇心 → 认同感 → 获得感”，不靠恐惧和焦虑制造刺激。
- 数据段落按“规模 → 身份/结构 → 差距 → 趋势”递进，适合改造成播客中的证据回合。
- 数据反直觉钩子、两条路线对比、数据分层递进和具体场景收尾可作为话题级结构模板。
- 每段单独检查：是否有真实痛点、是否有数据支撑、情绪是否服务于理解、结尾是否落到具体场景。

### 当前项目的适配方式

- 只吸收 Phase 2 的结构和情绪曲线，不使用其短视频平台节奏或 3 秒钩子约束。
- 与 `debate-rounds` 结合：一个话题先建立矛盾，再按“承认 → 追问 → 反证 → 类比 → 收束”推进。
- 与 `podcast-workflow` 结合：将情绪曲线映射到 `emotion` / `delivery`，由 Phase 3 TTS 消费。

### 限制

- 这是短视频脚本方法论，不提供音频生成、双主持人回合编排或 HyperFrames Composition。
- 不把“情绪曲线”当作声学情绪保证；仍需通过 TTS 和音频抽检验证。
