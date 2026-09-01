#!/usr/bin/env bash
# screenshot-fullpage.sh — 长文 HTML 全页截图（企业研究报告/长文页面预览用）
#
# 用途：对单文件长文 HTML 生成全页 PNG 预览。html-ppt-skill 自带 render.sh
# 面向翻页 deck（逐 slide 渲染），本脚本面向滚动长文页（一页到底）。
#
# 用法：
#   ./screenshot-fullpage.sh <input.html> [output.png] [width]
#     默认 output.png = 与输入同目录同名 .png；默认宽度 1440
#
# 退出码：
#   0 = 成功；1 = 截图失败（含 playwright 不可用）；2 = 用法错误
#
# 依赖：Playwright CLI（npx playwright，含 chromium）——验证命令：
#   npx playwright screenshot --full-page --viewport-size=1440,900 file:///... out.png
set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 3 ]; then
  echo "用法: $0 <input.html> [output.png] [width]" >&2
  exit 2
fi

INPUT="$1"
OUTPUT="${2:-${INPUT%.html}.png}"
WIDTH="${3:-1440}"

if [ ! -f "$INPUT" ]; then
  echo "错误: 文件不存在 $INPUT" >&2
  exit 2
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "错误: 需要 npx（Playwright CLI）" >&2
  exit 1
fi

URL="file://$(realpath "$INPUT")"
echo "截图: $URL → $OUTPUT (宽 ${WIDTH}px, 全页)"
npx playwright screenshot --full-page --viewport-size="${WIDTH},900" "$URL" "$OUTPUT" 2>/dev/null || {
  echo "错误: playwright 截图失败（检查 chromium 是否安装: npx playwright install chromium）" >&2
  exit 1
}

echo "完成: $(realpath "$OUTPUT") ($(du -h "$OUTPUT" | cut -f1))"
exit 0
