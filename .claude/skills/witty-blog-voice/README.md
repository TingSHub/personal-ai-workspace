# witty-blog-voice

> 一个给 Claude / OpenCode / Codex等 AI Agent用的「幽默·犀利（文明毒舌）」文风 skill。把干巴巴的文字改得有梗有刺，或从零写扎心短评、吐槽、神回复。

[English] A skill that rewrites or authors blog / WeChat-article text in a witty, sharp, "civilized snark" voice for Claude / OpenCode / Codex agents.

## 这是什么

让你的 agent 化身博客 / 公众号的「毒舌段子手」：幽默、犀利、一针见血，但守住文明底线。覆盖两种模式：

- **改写（模式 A）**：给一段文字，改成幽默犀利风
- **创作（模式 B）**：只给主题 / 角度，从零写毒舌内容

中文为主，适用于博客、公众号等场景。

## 特性

- **风格 DNA**：阴阳怪气但讲理、一针见血、自嘲式幽默、修辞三板斧（夸张 / 比喻 / 反讽）、短句节奏、共情打底
- **明确红线**：不人身攻击、不歧视、不涉政、不造谣、不脏话
- **两种工作流**：改写（A）/ 创作（B），按步骤执行
- **内置例句库**：`references/examples.md` 含 9 类场景例句与一篇完整长文改写范例

## 目录结构

```
witty-blog-voice/
├── SKILL.md            # 风格定义、工作流、红线、正反对照
├── references/
│   └── examples.md     # 例句与场景示范
├── README.md
├── LICENSE
└── .gitignore
```

## 安装

将本仓库克隆 / 复制到你的 agent 的 skills 目录下（目录名需保持为 `witty-blog-voice`）：

```bash
# 以 OpenCode 为例
git clone https://github.com/houguofei/witty-blog-voice.git ~/.agents/skills/

# Claude Code 等其他 agent，放到其对应的 skills 目录即可
```

新开会话后，agent 会在匹配到相关请求时自动加载本 skill。

## 触发词

- 「把这段改得犀利点」
- 「用幽默方式重写」
- 「写个毒舌吐槽」
- 「把这篇公众号文章写得尖刻点」
- 「来段扎心的评论」
- 「帮我想个带刺的标题」

## 红线（文明毒舌）

可以狠怼现象 / 产品 / 观点，但**不攻击具体活人**；不歧视、不涉政、不造谣、不脏话。毒舌靠逻辑和修辞，不靠音量。
