# no-negative-echo

> 管理资产：`.ai/skills/no-negative-echo/no-negative-echo.md`；安装实体：`~/.agents/skills/no-negative-echo/`

## 元数据

| 字段 | 值 |
|---|---|
| name | no-negative-echo |
| kind | skill |
| description | 在长对话迭代后的文档、提交信息、PR 或交付说明中，清除只属于工作过程的否定式残留，同时保留安全、兼容、迁移和审计所必需的事实 |
| source | github · https://github.com/LB623/no-negative-echo |
| installed_ref | 2dfbefdc41f9f728984096850d90a61e20054923 |
| runtime | both |
| invocation | 显式调用 `$no-negative-echo`；收尾 Workflow 在文档、commit message 和 handoff 交付前后调用其规则与 `check_surface.py` |
| requirements | Python 3.10+（仅使用内置库）；当前 Codex 用户级目录 `~/.agents/skills/no-negative-echo/`；不需要 API 密钥 |
| update | git · 拉取 GitHub 到临时目录，按上游 `INSTALL.md` 完成来源审查、117 项测试/同等测试、provenance 校验和冲突预检后，用官方 installer 更新；验证：读取安装实体、检查 provenance、运行 `check_surface.py --help` |
| 辅助脚本 | `~/.agents/skills/no-negative-echo/scripts/check_surface.py`：对最终文本表面和文件名执行精确项扫描；只输出计数和索引，不输出受保护词本身；收尾 Workflow 的最终质量门使用 |
| 经验引用 | — |

## 作用

把最终产物描述为“已经接受的结果”，而不是复述被否决的方案、用户纠正或中间草稿。适用表面包括正式文档、标题、文件名、代码注释、测试名、commit message、PR/发布说明和 handoff。

## 调用

1. 先建立每个表面的正向目标、最终状态、权威基线、必要事实、敏感信息和预-existing 用户修改清单。
2. 预检最终内容：只保留读者理解结果所必需的安全、准确、兼容、迁移、审计和实际外部事件事实。
3. 用冻结后的内容执行授权的文件写入或本地提交；不要在 mutation 阶段重新生成文案。
4. 读回实际结果，再运行 `scripts/check_surface.py`，最后据读回结果生成交付说明。

## 注意事项与踩坑

- 这是后置缓解层，不保证宿主一定自动激活，也不能改变对话上下文已经暴露的工具输出；关键收尾面必须显式调用。
- “删除/迁移/兼容性变化”若是正式行为变化，可以保留；只属于讨论过程的替代方案不应进入标题、commit 或普通 handoff。
- pre-existing 未提交修改不等于本次任务内容；必须先记录并保护，不能顺手纳入提交。
- scanner 是精确项和路径扫描器，不能替代语义审阅；零命中不等于完成全部质量检查。
- 安装实体属于外部资源，不在本地说明中复制或改写；本地增强只写在 Workflow 或本资源记录中。

## 验证记录

- 来源 checkout：`2dfbefdc41f9f728984096850d90a61e20054923`
- 上游安装契约 provenance SHA256：`9cc10a0f1d2d87f0de8517bf40c59e364783e2410308a0c8f815288f53a7cc47`
- 安装前测试：`python3 -I -m unittest discover -s tests -p 'test_*.py'`，117 项通过，7 项按环境跳过。
- 安装后验证：目标为 `~/.agents/skills/no-negative-echo/`，provenance 一致，`check_surface.py --help` 通过；Codex 映射路径可解析到同一安装实体。
