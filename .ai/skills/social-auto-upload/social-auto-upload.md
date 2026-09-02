# social-auto-upload

> 管理资产：`.ai/skills/social-auto-upload/social-auto-upload.md`；外部执行仓库按项目运行说明单独安装，不复制进 workspace 资源层

## 元数据

| 字段 | 值 |
|---|---|
| name | social-auto-upload |
| kind | skill/tool resource |
| description | 国内多平台视频/图文上传与定时发布 CLI，支持抖音、小红书、快手、B站、视频号等 |
| source | github · https://github.com/dreammis/social-auto-upload · installed_ref `1c66b7db4b30585bbb40c58eb0aa572ffa3cce97` |
| runtime | claude / codex（通过外部 `sau` CLI） |
| invocation | `sau <platform> check|upload-video|upload-note ...`；登录态按账号名隔离 |
| requirements | Python 3.10–3.12、uv、Patchright/Chromium；首次登录和二维码/短信验证可能需要用户在真实终端完成 |
| update | git · 拉取上游后复查 CLI、平台选择器、依赖和平台规则；verify：运行 `sau --help` 及各平台 `check` |
| scripts | 无本地辅助脚本；平台执行使用上游 CLI |
| experience_refs | aitoearn-publishing-flow-with-safe-fallback |

## 调用说明

### 作用

作为 AiToEarn 不支持、接口失败或需要浏览器自动化时的国内平台回退。当前主线覆盖抖音、小红书、快手、B站、视频号等；不同平台的定时、草稿和封面能力不同，必须以对应 CLI 帮助和运行日志为准。

### 回退边界

- 只在 AiToEarn 明确返回“不支持”或明确失败后使用。
- AiToEarn 状态未知、超时但可能已提交时禁止自动回退，先查询发布记录，避免重复发布。
- 不在资源记录或日志中保存 Cookie、验证码、API Key；不清空既有登录态目录。
- 首次接入先使用 `--draft` 或测试账号；真实平台页面和账号风控可能变化，脚本通过不代表平台发布成功。

### 证据要求

每个平台结果至少记录账号别名、平台、提交时间、状态、错误信息和作品链接；只有平台返回明确成功并拿到链接后，才回写账号级 `published-works.md`。
