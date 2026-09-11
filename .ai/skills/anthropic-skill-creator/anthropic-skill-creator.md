# anthropic-skill-creator

> 管理资产：`.ai/skills/anthropic-skill-creator/anthropic-skill-creator.md`；安装包：`.claude/skills/anthropic-skill-creator/`；Skill 入口：该包内 `skills/skill-creator/SKILL.md`。

## 元数据

| 字段 | 值 |
|---|---|
| name | anthropic-skill-creator |
| kind | skill |
| description | Anthropic 官方 Skill 创建、改进与评估工具，支持测试用例、基准对比、人工评审、触发描述优化和打包 |
| source | github · https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator |
| installed_ref | f2cc019c16ebb84cbb809fc91ed35a79842bea2c · 仓库子目录 plugins/skill-creator |
| runtime | both（基础创作与本地工具）；Claude Code 专属触发评测须有 claude CLI 及有效登录 |
| invocation | 按资源名 anthropic-skill-creator 解析本记录，读取安装包内 skills/skill-creator/SKILL.md；上游 frontmatter 与插件名保留 skill-creator |
| requirements | Python 3、PyYAML；模型评测需要可用 Agent 执行环境；run_eval/run_loop/improve_description 使用 claude -p 与其登录态，本版本不要求单独的 Anthropic Python SDK；模型参数必须为 Claude CLI 支持的标识 |
| update | method：git；instructions：从来源仓库获取指定提交到临时目录，比较 plugins/skill-creator 整包，检查许可、依赖与凭据，通过最小验证后更新安装包及 installed_ref，保留本记录；verify：入口校验、临时目录打包、评审工具入口、上游文件一致性与 Workflow 引用检查 |
| scripts | 上游内置 scripts/quick_validate.py、package_skill.py、aggregate_benchmark.py、run_eval.py、run_loop.py、improve_description.py、generate_report.py，以及 eval-viewer/generate_review.py；均相对内层 Skill 根目录；无新增本地脚本 |
| experience_refs | — |

## 调用与名称区分

- 工作区资源名为 anthropic-skill-creator，用户可说“使用 anthropic-skill-creator 创建/改进这个 Skill”。加载时读取 `.claude/skills/anthropic-skill-creator/skills/skill-creator/SKILL.md`，无需原对话上下文。
- Codex 系统自带的 skill-creator 是另一份资源；本次不覆盖它。裸名称 skill-creator 仍可能歧义，明确指定 Anthropic 版本或上述入口路径。资源登记名不是自动生成的斜杠命令。
- 保留完整官方插件目录、许可证与上游文件；本次为工作区资源安装，未执行 Claude 插件市场注册。客户端是否自动发现内层 Skill 取决于其扫描机制；显式读取入口可避免名称与发现差异。
- 按需读取上游 agents/ 与 references/，不用为安装该资源就启动子 Agent 或模型评测。

## 本地工具

以下命令在安装包内 `skills/skill-creator/` 目录执行，输入与输出使用实际路径：

```bash
python3 scripts/quick_validate.py /absolute/path/to/target-skill
python3 -m scripts.package_skill /absolute/path/to/target-skill /absolute/path/to/output
python3 -m scripts.aggregate_benchmark /absolute/path/to/iteration --skill-name target-skill
python3 eval-viewer/generate_review.py /absolute/path/to/iteration --static /absolute/path/to/review.html
```

运行模型评测前读取相关上游脚本。run_eval 会寻找工作目录上方的 `.claude/` 并临时写入 commands；在独立评测工作目录执行，避免污染生产工作区。评测输入、输出与用户反馈保存在项目运行目录，不写入外部安装实体。模型耗时和用量如实记录，未取得的数据不得编造。

## 与工作区项目的交接

用户要求转换时，从项目 README、入口 Workflow、模板、脚本、依赖记录与最小复跑案例收集材料；整套 SOP 或其中独立能力均可作为封装范围。根据实际请求确定范围和目标环境，项目本身无需预先成为 Skill。新资源的安装与登记继续通过 Resource Manager，经验回写遵循 Experience Curator；本地约定保留在资源记录，不修改上游安装包。

## 验证与限制

- 已核对源提交，保留 Apache-2.0 许可证；整包与该提交的 plugins/skill-creator 内容一致。
- 安装前进行了常见凭据模式、隐藏环境文件与符号链接检查，未发现真实凭据或符号链接。
- 已通过上游 quick_validate，并在临时目录实际生成 .skill 压缩包；评审生成器 --help 正常。
- 本机 Python 3 / PyYAML 可用，claude CLI 可定位；未验证其登录态或启动付费模型调用。
- 本次仅验证安装及本地工具，不声称已完成创建质量、基准对比或触发优化的端到端评测。
