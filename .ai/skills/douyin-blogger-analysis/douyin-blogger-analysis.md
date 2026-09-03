# douyin-blogger-analysis

> 管理资产：`.ai/skills/douyin-blogger-analysis/douyin-blogger-analysis.md`；安装实体：`.claude/skills/douyin-blogger-analysis/`（含打包的 douyin-agent）

## 元数据

| 字段 | 值 |
|---|---|
| name | douyin-blogger-analysis |
| kind | skill |
| description | 竞品博主分析管线：采集对标账号作品列表/评论/视频/截图/转写字幕（打包 douyin-agent，CDP 挂接真实 Chrome） |
| source | github · https://github.com/ganymedenil/poxiaoxing-skills 子目录 douyin-blogger-analysis/ · installed_ref 417ceca85d09ad587cd524fc7a81b946792dd367（Apache-2.0，74★） |
| runtime | claude / codex（Python + 打包 douyin-agent，uv 管理） |
| invocation | `python3 scripts/douyin_blogger_analysis.py <setup|collect-posts|collect-comments|download-videos|extract-screenshots|transcribe> [参数]`；五步可独立跑也可串成完整管线 |
| requirements | uv（~/.local/bin/uv）+ ffmpeg + Python 3.12 已就绪；**采集需用户本机 Chrome 开 CDP 调试端口并登录抖音**（挂真实会话，Agent 不碰登录凭证） |
| update | manual · 重新获取上游固定 commit 的子目录对比后替换；verify：`python3 scripts/douyin_blogger_analysis.py setup` 全绿 |
| scripts | 无（五步脚本属安装实体本体） |
| experience_refs | 无 |

## 调用说明

### 用途（竞品三问的数据层）

- **市场正在奖励什么**：collect-posts 采对标账号作品列表 → 找"明显高于该账号自身平均播放"的视频（账号相对基线，不是绝对最高）
- **用户还有什么没被回答**：collect-comments 采高表现视频的评论与回复链 → 反复追问/争议点/没听懂/想看的公司 = 免费需求调研
- **你能增加什么独特价值**：产出导入 publish-review 证据包归因，用 boundary-rewrite / finance-content-engineering 生成差异化角度（对方讲上涨逻辑→我们验现金流与应收；对方下结论→我们展示证据链）

### 与 douyin-creator-tools 的边界

- douyin-creator-tools：**自己账号**后台数据（登录态 Playwright，导出 Excel）
- douyin-blogger-analysis：**竞品账号**公开数据（CDP 挂接真实 Chrome，采公开页面）
- 两者互补不重叠；douyin-blogger-analysis 的输出可作为 publish-review P3 证据包的"竞品"第七源

### 使用约束（合规）

1. 只采对标账号**公开页面**数据，低频（单账号每周 ≤1 次全量），不批量、不并发
2. 机制为 CDP 挂接用户本人 Chrome 会话；不破解签名、不绕验证码；出现滑块立即停，交人工
3. 爬他人公开数据有 ToS 灰色与判例风险（抖音诉刷宝案）：仅用于内部选题研究，数据不对外发布
4. 转写用 AuralWise（其内置）；如需本地转写可换 faster-whisper

### 已知限制

- 机制依赖用户本机 Chrome CDP（WSL2 场景 = Windows 侧 Chrome 开 --remote-debugging-port，WSL2 经 host IP 挂接）；首次联调需要用户配合
- AuralWise 转写质量未验证；投研术语多的视频建议用 faster-whisper 复核
- 上游安装实体未做本地改动；改版风险由上游维护
