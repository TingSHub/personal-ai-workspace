---
name: resource-manager
description: 管理 Skill/Agent 执行资源与可跨项目复用的媒体/设计资源——注册、安装、更新、查看、修改、验证、归档，并维护调用注意事项、踩坑与辅助脚本。当用户说“注册/安装/更新/管理 skill、agent、字体、音色或通用资源”“添加辅助脚本”“查看资源调用方法”时使用。
---

# Resource Manager

统一管理 Skill、Agent 和可跨项目复用资源：注册、安装、查询、验证与归档。资源层是技术调用说明书，不做能力评价、资源推荐或质量打分；资源选择依据以 Workflow SOP 的 Required Resources 注记与项目证据为准，Experience 由 Experience Curator 维护。

## 目录与边界

- Skill 资产：`.ai/skills/<name>/<name>.md`（单文件 Markdown 文档：`## 元数据` 表格 + 调用说明正文；辅助脚本在同目录 `scripts/`），字段读取 `.ai/templates/skill.yaml.template`
- Agent 资产：`.ai/agents/<name>/<name>.md`（单文件，结构同上），字段读取 `.ai/templates/agent.yaml.template`；实体定义在顶层 `.agents/<name>.md`（可被加载执行）
- 外部 Skill 安装：`.claude/skills/<name>/`；这是 workspace 唯一 Skill 安装根
- Codex 安装树：`.codex/skills` 必须是指向 `../.claude/skills` 的单一目录软链接；`.codex/skills/<name>` 通过该目录映射自动可见
- `.agents/` 只保存 Agent 实体定义，禁止创建 `.agents/skills` 目录、镜像或软链接
- 外部 Skill 的本地说明和辅助脚本保存在资源资产目录，不直接修改外部安装实体；workspace 一方 Skill 可将其执行所需脚本放在 `.claude/skills/<name>/scripts/`，并在对应 `.ai/skills/<name>/<name>.md` 登记
- 字段清单只能从模板读取，本文不复制字段定义
- 不维护状态、配置成本、使用次数或更新历史数组等记录
- 归档是显式操作，必须先取得用户确认

### 通用媒体/设计资源

- 通用资源存放在 `.ai/assets/<kind>/<name>/`，元数据为该目录下的 `ASSET.md`，字段读取 `.ai/templates/asset.md.template`。
- `kind` 至少支持 `voices`、`fonts`、`images`、`music`、`icons`；资源本体和许可证与 `ASSET.md` 一起保存。
- 资源记录必须使用稳定的 `resource_key`，例如 `voice.zhiwei`、`font.noto-serif-sc`；项目不得复制一份资源正文作为自己的资产本体。
- 项目的 `account-profile` 只记录 `resource_key → 角色/视觉用途/选择`；Workflow 只记录运行参数，不登记资源本体。
- 候选、公司专属裁剪、未经验证的参考音频留在项目实验目录，不注册为通用资源。

## add：注册资源

输入：资源类型（Skill/Agent）、GitHub URL、安装包、本地目录或其他来源。

1. 检查 `.ai/skills/` 与 `.ai/agents/`，避免重名和重复能力资源。
2. 远程来源先获取到 `/tmp/`，检查 README、入口、依赖、LICENSE 和版本标识，绝不直接 clone 到 workspace。
3. 从对应模板生成单个 `<name>.md`：`# 标题` + `> 位置引用` + `## 元数据` 表格（模板字段）+ 调用说明正文（作用、来源、用途、注意事项、踩坑和辅助脚本用法）。
5. 记录实际安装的 tag、版本或 commit SHA；无版本上游优先记录 commit SHA。
6. 若资源适配相关 Workflow 的 Phase，可建议在相关 Workflow SOP 的 Required Resources 注记补充。

### add-asset：注册通用资源

1. 先确认资源跨项目复用边界、来源、授权/许可证、格式、文件指纹和最小验证方法。
2. 检查 `.ai/assets/<kind>/<name>/` 是否已有同名资源；不要把项目 `account-profile` 目录直接注册为通用资源。
3. 将资源本体、许可证和 `ASSET.md` 放在同一目录；`ASSET.md` 只写调用所需信息，不复制项目角色或公司事实。
4. 记录稳定的 `resource_key`、来源标识、版本/指纹、文件列表、调用方式和验证结果；不记录密钥。
5. 项目接入时只写资源 key 和用途映射；不要为项目再复制字体、音频或 logo 本体。

## install：安装资源

1. 按来源安装到约定位置，不改写第三方原文件。
2. 检查必要配置，但不记录密钥值。
3. **密钥/凭据扫描（常设）**：对安装实体执行密钥扫描（搜索常见 secret pattern：`-----BEGIN (RSA|EC|OPENSSH|PRIVATE) PRIVATE KEY-----` 私钥块、`api[_-]?key`/`access[_-]?token`/`secret`/`password` 等赋值且值形态像真实凭据、`.env` 文件含非占位真实值）；发现即拒绝安装并报告文件位置，不写入 `installed_ref`；仅占位符（`your-key-here`、`xxx`）不视为凭据。
4. 验证 `.codex/skills -> ../.claude/skills`；只在目录级链接缺失或错误时修复，禁止创建逐 Skill 二级链接。
5. 执行模板声明的最小验证；成功后记录实际 `installed_ref`。

## update：更新外部资源

1. 按资源 `source` 和 `update` 说明将新版本获取到临时目录。
2. 对比入口、依赖、配置、工具权限和输入输出是否变化。
3. 只更新外部安装实体，保留 `.ai/skills/` 或 `.ai/agents/` 中的 `<name>.md` 本地说明与 `scripts/`。
4. 执行更新后最小验证；失败时保留原可用版本，不写入新的 `installed_ref`。
5. 验证通过后更新当前 `installed_ref`。普通更新过程由 Git 记录，不追加更新流水账。
6. 输入、输出或结果质量发生实质变化时，提示需要在真实项目重新验证；未经项目证据，不调整 Workflow 中资源注记的推荐顺序。
7. **by-name 维护契约（常设）**：资源重命名或删除前，先 grep 全量 `projects/*/workflows/*/workflow.md` 与 `.ai/workflows/` 的 Required Resources 并同步 by-name 引用；每次资源变更后运行 V5 式解析检查（所有 Required Resources 均可解析到 `.ai/skills/` 或 `.ai/agents/`）。

## add-script：添加辅助脚本

1. 先确认脚本解决的是该资源的实际调用问题，而不是独立的新能力。
2. 保存到资源目录 `scripts/`。
3. 在资源元数据和说明中记录问题、作用、使用条件、调用方式、要求和限制。
4. 执行最小验证。不要创建 Helper/Adapter/Wrapper 分类。
5. 只有脚本后来能够脱离原资源并被多个项目独立复用时，才按普通资源另行注册。

## view / modify / verify

- `view`：读取资源元数据与本地说明；资源被哪些 Workflow 引用可从 workflow-registry 索引查询（索引含每 SOP 的 Required Resources by-name 列表）。
- `modify`：仅修改资源职责内的信息，修改后验证模板和引用。
- `verify`：检查安装实体、调用入口、依赖声明、辅助脚本和最小调用；Agent 额外检查模型、工具和权限兼容性。
- 通用资源 `verify`：检查 `ASSET.md`、本体文件、许可证/来源、格式、指纹和最小打开/渲染/试听验证。

## archive

取得用户明确确认后，删除安装实体；目录级 Codex 映射会同步隐藏该资源，不单独修改 `.codex/skills`。保留仍有来源或避坑价值的资源元数据。若 Workflow SOP 的 Required Resources 仍引用该资源，先按 by-name 维护契约（见 update）同步引用。归档原因写入保留说明，不新增状态记录。

## Validation

- 对应资源元数据和说明文件存在并符合模板
- 外部资源包含可复现的 `installed_ref`、更新方法和更新后验证方式
- requirements 中只记录配置名称，不包含 secret 值
- 声明的本地脚本均存在并能通过最小验证；一方 Skill 的实体脚本位于其 `.claude/skills/<name>/scripts/`
- `.codex/skills` 是指向 `../.claude/skills` 的有效目录软链接，且安装实体能从两条路径解析到同一目录
- `.agents/skills` 不存在，Skill 没有第二份 workspace 安装实体
- 资源变更后 Required Resources 解析检查通过（workflow.md 的引用均可解析到 `.ai/skills/` 或 `.ai/agents/`）
- 通用资源记录存在，资源本体与 `ASSET.md` 同目录，项目只通过 `resource_key` 引用
- 不直接写 Workflow SOP 的资源注记或 Experience Knowledge
