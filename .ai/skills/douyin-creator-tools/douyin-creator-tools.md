# douyin-creator-tools

> 管理资产：`.ai/skills/douyin-creator-tools/douyin-creator-tools.md`；安装实体：`.claude/skills/douyin-creator-tools/`（完整 Node 仓库）

## 元数据

| 字段 | 值 |
|---|---|
| name | douyin-creator-tools |
| kind | skill |
| description | 本人抖音账号数据采集与互动工具：登录态管理、作品列表、指标 Excel 导出、评论导出/回复 |
| source | github · https://github.com/wenyg/douyin-creator-tools · installed_ref e35dbe27548cff292cc2d709417467a3bd464ed1（2026-07-15 "gpt 5.6重构"） |
| runtime | claude / codex（Node CLI，任何 agent 可调用） |
| invocation | 在安装目录内执行 `npm run <command>`；指标导出走本地辅助脚本（见 scripts） |
| requirements | Node ≥ 22（本机 v25.9.0）；`npm install` 已装 playwright/express/better-sqlite3；Playwright Chromium 已装；openpyxl 3.1.5（xlsx 解析）；WSL2 有头浏览器需 WSLg 图形支持 |
| update | git · 进入安装目录 `git pull && npm install`，对比 `git log` 后保留本地说明；verify：`node --check` 两个辅助脚本（未登录态跑导出脚本应报「登录态过期」并退出码 2，属预期验证路径） |
| scripts | `.ai/skills/douyin-creator-tools/scripts/export-works-metrics.mjs`（作品列表 Excel）；`scripts/parse_works_xlsx.py`（Excel → works-metrics.json）；`scripts/export-work-detail.mjs`（单作品详情页官方导出 Excel）；`scripts/parse-work-detail-exports.py`（详情导出 Excel → JSON）；`scripts/collect-work-detail.mjs`（详情页补充 JSON + 页面证据截图） |
| experience_refs | 无 |

## 调用说明

### 用途与边界

- 采集**本人账号**的创作者中心数据：作品列表、互动数据、评论。禁止用于他人账号、批量操作或绕过登录/验证码/风控。
- 指标 Excel 字段（官方导出）：作品名称/发布时间/体裁/审核状态/播放量/完播率/5s完播率/2s跳出率/封面点击率/平均播放时长/点赞/评论/分享/收藏/主页访问量/粉丝增量。
- 局限：官方导出**没有小时级留存曲线和观众画像**（那两个只在页面可视化里）；导出上限约 30 天/100 条，超出用页面取数（未实现）。

### 首次使用（唯一必须人工的步骤）

1. `cd .claude/skills/douyin-creator-tools && npm run auth`（有头浏览器打开，**用户本人**用抖音 APP 扫码；Agent 不得替代扫码）
2. 扫码成功后登录态存于仓库内 `.playwright/douyin-profile/`，不要清空或移动该目录。
3. 验证登录态：跑一次指标导出辅助脚本（未登录会在导航后报「登录态过期」退出）；本仓库 auth 无 check 子命令。

### 常用调用

```bash
cd .claude/skills/douyin-creator-tools
npm run works                     # 作品列表 -> comments-output/list-works.json
npm run comments:export -- "<作品标题>"   # 该作品未回复评论 -> unreplied-comments.json
# 指标导出（本地辅助脚本，含完播率/5s完播率/2s跳出率/封面点击率）：
node ../../.ai/skills/douyin-creator-tools/scripts/export-works-metrics.mjs --out /tmp/作品列表.xlsx
python3 ../../.ai/skills/douyin-creator-tools/scripts/parse_works_xlsx.py /tmp/作品列表.xlsx <输出.json>
# 单作品详情页（只读）：总览、趋势、章节、搜索词与页面截图
node ../../.ai/skills/douyin-creator-tools/scripts/collect-work-detail.mjs \
  --item-id <作品ID> \
  --output /absolute/path/detail-snapshot-YYYY-MM-DD.json \
  --screenshot /absolute/path/detail-page-YYYY-MM-DD.png
# 单作品详情页官方导出：内容吸引力、观众参与度、流量来源、观众分析
node ../../.ai/skills/douyin-creator-tools/scripts/export-work-detail.mjs \
  --item-id <作品ID> \
  --out-dir /absolute/path/work-detail-exports-YYYY-MM-DD
python3 ../../.ai/skills/douyin-creator-tools/scripts/parse-work-detail-exports.py \
  /absolute/path/work-detail-exports-YYYY-MM-DD \
  /absolute/path/detail-exports-YYYY-MM-DD.json
```

详情采集优先使用详情页官方“导出”按钮保存 Excel，再解析为 JSON；目前实测覆盖内容吸引力（含进度分析）、观众参与度、流量来源、观众分析。JSON 是结构化事实源，原始 Excel 用于审计；截图和接口采集仅补充章节点击率、搜索关键词、留存曲线等导出文件没有的数据。脚本只保存脱敏后的来源端点，不保存 Cookie、`msToken` 或 `a_bogus` 等请求鉴权参数。

### 使用约束（合规，写入每次采集 SOP）

1. 低频采集：每日 ≤ 2 次全量导出，单作品详情查询间隔 ≥ 30 分钟。
2. 只操作登录态对应的账号；出现滑块/验证码立即停止并交人工。
3. 失败即停：页面结构变化导致失败时，人工核查页面，不改代码硬修。
4. 不读取/导出 cookie 与会话凭证；登录态目录不入 git（.gitignore 已覆盖）。

### 踩坑（继承自 TzFilm 实战记录 + 2026-08-31 本 workspace 实测）

1. **2026-05-22 改版 + 2026-08-31 实测**：旧 URL `/creator-micro/data-center/content` 仍可用，但默认进入「投稿分析」聚合视图（含条均指标，可作辅助校验源）；「投稿列表」radio 旧类名 `douyin-creator-pc-radio-addon` 已失效，改用文本定位 `getByText("投稿列表", { exact: true })`；页面有**两个「导出数据」按钮**（投稿概览/投稿表现），点第一个。辅助脚本已内置以上逻辑。
2. **登录态过期两种模式**：Mode A 近期过期——导出返回 JSON 错误体（PK 头校验捕获）；Mode B 深度过期——根本不触发下载，直接超时。两种都需人工重新扫码。
3. Garfish 微前端初始化约需 15s，控件等待不要低于 20s。
4. 导出 Excel 百分比字段是小数（0.2723 = 27.23%），`parse_works_xlsx.py` 已统一 ×100；数值列以文本存储，解析器已做数字转换。
5. 导出 Excel 表头实测（2026-08-31）：作品名称/发布时间/体裁/审核状态/播放量/完播率/5s完播率/封面点击率/2s跳出率/平均播放时长/点赞量/分享量/评论量/收藏量/主页访问量/粉丝增量。
6. AppleScript/TCC 坑仅适用 macOS，WSL2 不涉及。

### 与调研结论的对应

- 首次闭环已跑通（2026-08-31）：登录 → 指标导出 → 解析落盘 → 归因报告，见 `projects/investment-research-video/outputs/companies/中科曙光/2026-08-27-editorial-gate-fix/publish/traffic/`。
- 竞品/他人视频的公开数据（播放/点赞/评赞比等）**不在本资源范围内**；如需批量获取需另行评估合规边界（第三方 API 有 ToS 风险）。
