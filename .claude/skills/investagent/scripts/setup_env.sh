#!/bin/bash
# 投研Agent 环境安装脚本
# 安装所有5个skill的依赖

set -e

AGENT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$AGENT_ROOT/skills"

echo "╔══════════════════════════════════════════╗"
echo "║   全栈AI投研Agent - 环境安装            ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 检查Python版本
echo "▶ 检查Python版本..."
python3 --version || { echo "✗ Python3 未安装"; exit 1; }

# 创建虚拟环境（可选）
if [ "$1" = "--venv" ]; then
    echo "▶ 创建虚拟环境..."
    python3 -m venv "$AGENT_ROOT/.venv"
    source "$AGENT_ROOT/.venv/bin/activate"
    echo "✓ 虚拟环境已激活"
fi

# 安装UZI-Skill依赖
echo ""
echo "▶ 安装 UZI-Skill 依赖..."
UZI_REQ="$SKILLS_DIR/uzi-skill/skills/deep-analysis/requirements.txt"
if [ -f "$UZI_REQ" ]; then
    pip install -r "$UZI_REQ" --break-system-packages -q 2>/dev/null || \
    pip install -r "$UZI_REQ" -q 2>/dev/null
    echo "✓ UZI-Skill 依赖安装完成"
else
    echo "○ UZI-Skill requirements.txt 未找到，跳过"
fi

# 安装TradingAgents依赖
echo ""
echo "▶ 安装 TradingAgents 依赖..."
TA_REQ="$SKILLS_DIR/TradingAgents/requirements.txt"
if [ -f "$TA_REQ" ]; then
    pip install -r "$TA_REQ" --break-system-packages -q 2>/dev/null || \
    pip install -r "$TA_REQ" -q 2>/dev/null
    echo "✓ TradingAgents 依赖安装完成"
else
    echo "○ TradingAgents requirements.txt 未找到，跳过"
fi

# Buffett Skills 和 Serenity Skill 无代码依赖
echo ""
echo "○ Buffett Skills - 无代码依赖（纯方法论Skill）"
echo "○ Serenity Skill - 无代码依赖（纯方法论Skill）"

# QuantDinger 需要Docker
echo ""
echo "▶ 检查 Docker 环境..."
if command -v docker &> /dev/null; then
    echo "✓ Docker 已安装: $(docker --version)"
    if docker compose version &> /dev/null; then
        echo "✓ Docker Compose 已安装"
        echo ""
        echo "  QuantDinger 启动命令:"
        echo "  cd $SKILLS_DIR/QuantDinger && docker-compose up -d"
    else
        echo "○ Docker Compose 未安装（QuantDinger需要）"
    fi
else
    echo "○ Docker 未安装（QuantDinger需要Docker环境）"
fi

# 创建符号链接到skills目录
echo ""
echo "▶ 配置Skill路径..."
echo "  SKILLS_DIR=$SKILLS_DIR"
echo ""

echo "╔══════════════════════════════════════════╗"
echo "║   环境安装完成                            ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "使用方法:"
echo "  主题研究: python scripts/run_research.py --theme 'A股AI半导体'"
echo "  个股分析: python scripts/run_stock_analysis.py --ticker 600519.SH"
echo ""
echo "注意事项:"
echo "  - TradingAgents 需要配置 LLM API Key"
echo "  - QuantDinger 需要启动 Docker 服务"
echo "  - Buffett/Serenity 为方法论Skill，由AI Agent执行"
