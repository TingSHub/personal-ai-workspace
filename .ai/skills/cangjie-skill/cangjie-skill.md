# cangjie-skill

> 管理资产：`.ai/skills/cangjie-skill/cangjie-skill.md`；安装实体：`.claude/skills/cangjie-skill/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| name | cangjie-skill |
| kind | skill |
| description | 把书/长视频转写/播客/课程/访谈蒸馏成一组原子化可执行 skills 的元 skill（RIA-TV++ 五阶段流水线） |
| source | github · https://github.com/kangarooking/cangjie-skill |
| installed_ref | 3a8c23a67884167411af230a5ff20975548756a5 |
| runtime | both |
| invocation | 用户说「拆书 / 蒸馏这本书/视频/播客/课程成 skill」时触发；按 SKILL.md 五阶段执行，输出 `books/<slug>/` |
| requirements | 内容文本来源（PDF/EPUB/TXT/字幕/转写稿路径）——无文本不蒸馏；内容元信息（书名+作者+出版年 / 视频标题+UP主+发布时间）；无 npm 依赖（纯 markdown 方法论 + 模板 + 1 个 python 脚本） |
| update | git · 拉取上游新版本到临时目录审查（SKILL.md、methodology/、LICENSE 变更）后更新 vendor 安装；保留本资源说明；验证：SKILL.md frontmatter 有效 + 五阶段文件齐全 |
| 辅助脚本 | — |
| 经验引用 | — |

## 作用

元 skill：不是直接干活的技能，而是**把长内容蒸馏成一组可复用 skills 的流水线**。核心方法论 RIA-TV++：阶段 0 Adler 整书理解 → 阶段 1 五个 extractor 并行提取（principle/framework/case/counter-example/glossary）→ 阶段 1.5 三重验证 → 阶段 2 RIA++ 构造 skill → 阶段 3 Zettelkasten 链接（INDEX/GLOSSARY）→ 阶段 4 darwin 兼容压力测试 → 阶段 5 交付（DIGEST + 安装）。边界：做方法论/框架/清单/原则蒸馏，不做书摘/读后感/作者角色扮演（后者归 nuwa-skill）。

## 调用

- 输入必须确认：内容文本来源（视频需先拿到转写稿/字幕）+ 元信息；**无文本不凭记忆蒸馏**
- 断点续跑：先查 `books/<slug>/PIPELINE_STATE.md`，存在则续跑不重来
- 输出结构：`books/<slug>/`（BOOK_OVERVIEW / verified / INDEX / GLOSSARY / DIGEST / candidates/ / rejected/ / 各 skill 目录含 SKILL.md + test-prompts.json）
- 非书籍内容字段映射：`source_chapter` 对视频填时间戳/分 P，保证可追溯
- 首次使用建议先蒸馏 1 份内容验证流程再批量

## 调用注意事项

- **适配本项目场景（蒸馏视频改进工作流）**：本 skill 面向"内容→skills"，我们用它时输入是「成片转写稿 + 设计产物（BRIEF/SCRIPT/scene-design/frame.md/QA 记录）」+ 参考视频（抖音目标效果），输出应是「视频创作方法论 skills」——即把参考视频的创作手法和自身成片的得失蒸馏成可调用技能，再回写 investagent-video-by-hyperframes 工作流
- 阶段 4 压力测试（darwin 兼容）依赖 darwin-skill 生态，本环境无 darwin 时可降级为 test-prompts.json 手工执行，如实记录
- LICENSE 为 AGPL-3.0：蒸馏产出的 skills 为原创内容不受传染；vendor 安装实体整体保留 LICENSE

## 常见失败原因

- 无文本直接蒸馏（凭记忆）——违反输入要求，必须停下要文本
- 跳过阶段 0 用户确认直接进并行提取——骨架理解偏差会放大到所有候选单元
- 大文件不分块阅读——阶段 0 内存溢出/遗漏，须分块

## 最佳实践

- 视频类输入先转写（hyperframes CLI `transcribe` 或 media-use 引擎）再蒸馏，转写稿是阶段 0 的输入
- 候选单元池（candidates/）与淘汰记录（rejected/）保留完整审计链，蒸馏结论可追溯
