# aitoearn

> 管理资产：`.ai/skills/aitoearn/aitoearn.md`；安装实体：无本地实体（远程 MCP/REST 服务，仓库仅作版本参照）

## 元数据

| 字段 | 值 |
|---|---|
| name | aitoearn |
| kind | skill |
| description | 多平台内容一键分发与账号矩阵管理（14+ 平台），MCP/REST 双协议，发布记录带各平台作品链接回传 |
| source | github · https://github.com/yikart/AiToEarn · installed_ref v2.5.0（MIT，25.6k★，2026-08 活跃维护） |
| runtime | claude / codex（MCP HTTP 协议；REST API 备用） |
| invocation | MCP：`https://aitoearn.cn/api/unified/mcp`，认证头 `x-api-key`；REST：`https://aitoearn.cn/api`，同一 API Key |
| requirements | ① 用户在 aitoearn.cn 注册并创建 API Key（Agent 不得代办账号注册）② Claude Code 注册 MCP server：`claude mcp add --transport http aitoearn https://aitoearn.cn/api/unified/mcp --header "x-api-key: <KEY>"` ③ 平台账号授权在其 web 端完成（OAuth 经其 relay） |
| update | 跟随上游 release tags（当前 v2.5.0）；重大版本变更时复查 API 兼容性；verify：MCP 连接测试 + 平台元数据接口可达 |
| scripts | 无 |
| experience_refs | aitoearn-publishing-flow-with-safe-fallback,podcast-douyin-handoff-and-investor-cover |

## 调用说明

### 用途（本 workspace 的三个结合点）

1. **发布环节自动化**：production workflow 的发布动作 → 一键多平台分发（抖音/视频号/公众号）+ **日历排期**——直接落地复盘改进项"发布时间窗口（12:00 或 18:00–20:00）"
2. **发布登记自动化**：publish API 的 track/发布记录回传**含各平台作品链接** → 回填 `published-works.md` 的 `platform_url`（替代当前手工取 aweme_id）
3. **多账号矩阵**：同一 AiToEarn 账户维度管理多平台多账号，为后续矩阵期做准备

### 能力边界（实测/文档确认）

- **没有流量统计 API**：播放/完播/互动数据仍走 `douyin-creator-tools` 采集，两者互补不重叠
- 发布状态轮询有明确状态机（status 0/2/6 等待、-1/5/9 失败、8 待人工）
- 素材上传走签名 URL 直传对象存储
- 抖音立即发布走 App Scheme 用户接力：当前实现只把视频路径、标题和话题带入 Scheme，独立封面 URL 不会自动进入抖音确认页；发布前必须人工检查并在抖音确认页上传/选择封面。
- 当前后端抖音话题上限实测为 5 个；不要仅依赖旧版发布 Skill 的 5–10 个标签规则，应先读取平台元数据或以接口校验为准。

### 发布调用顺序

1. `GET /api/v2/channels/accounts` 获取已授权账号和 `accountId`。
2. `POST /api/assets/uploadSign` 获取视频/封面签名地址；PUT 文件后调用 `POST /api/assets/{id}/confirm`。
3. `POST /api/v2/channels/publish/flows` 创建一个多平台 Flow；默认使用排期或草稿，不把 Flow 创建成功当作平台发布成功。
4. `GET /api/v2/channels/publish/records/{recordId}` 逐条轮询；记录 `status`、作品链接、错误和 `needs_user_action`。
5. 抖音进入用户操作状态时，调用用户操作信息接口取得短链，由用户在手机端确认后继续轮询。

中国版 API Key 只能配 `aitoearn.cn` 与 `assets.aitoearn.cn`；国际版只能配 `aitoearn.ai` 与 `assets.aitoearn.ai`。发布请求中只记录账号 ID、资源 ID、Flow/record ID 和结果，不写入 API Key。

### 红线（本项目明确不用的部分）

- **Engage 的自动点赞/收藏/关注批量运营**：与平台打击的营销自动化同类，账号资产风险，禁用
- **Monetize 任务市场**：与投研内容定位无关
- **Create 视频生成**：自有 HyperFrames 管线质量更高，不用

### 信任与合规考量

- 当前形态为 **SaaS relay**：平台账号 OAuth 与发布经其服务器。若后续矩阵规模变大或对信任有更高要求，用其 Docker 自部署（仓库含 docker-compose + nginx 配置）
- API Key 等凭证不入库、不写入本文档
