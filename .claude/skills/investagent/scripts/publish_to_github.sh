#!/bin/bash
# ── InvestAgent · GitHub Publish Script ───────────────────────
#
# This script:
#   1. Creates a public GitHub repository for InvestAgent
#   2. Pushes the local commit (main branch)
#   3. Prints the repository URL at the end
#
# Usage:
#   GITHUB_TOKEN="ghp_xxx" bash scripts/publish_to_github.sh
#   (or paste the token when prompted)
#
# Token requirements:
#   Scopes: repo, workflow, read:user
#   URL: https://github.com/settings/tokens → Generate new token
#
# ───────────────────────────────────────────────────────────────

set -euo pipefail

REPO_NAME="investagent"
REPO_DESC="全栈AI投研Agent · Your AI research co-pilot for smarter investment decisions. Five integrated research frameworks: Serenity industry-chain analysis, Buffett value-investing filter, UZI-Skill 22-dim deep analysis, TradingAgents multi-agent decision, QuantDinger quant backtest."
REPO_HOMEPAGE=""

# ── 1. Get token ──────────────────────────────────────────────

if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🟢  InvestAgent · GitHub Publish"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  请在 https://github.com/settings/tokens 生成一个具有 repo 权限的 token"
    echo "  Please generate a token with 'repo' scope at:"
    echo "  https://github.com/settings/tokens"
    echo ""
    read -rsp "  粘贴 token / Paste token here: " GITHUB_TOKEN
    echo ""
fi

if [ ${#GITHUB_TOKEN} -lt 20 ]; then
    echo "❌ Token seems too short or empty. Aborting."
    exit 1
fi

# ── 2. Authenticate gh CLI ────────────────────────────────────

echo ""
echo "→ Authenticating with GitHub..."
echo "$GITHUB_TOKEN" | gh auth login --with-token

if gh auth status 2>&1 | grep -q "Logged in"; then
    echo "✅ Authenticated successfully"
else
    echo "❌ Authentication failed. Please check your token."
    gh auth status 2>&1 || true
    exit 1
fi

# ── 3. Create the repository ──────────────────────────────────

echo ""
echo "→ Creating GitHub repository: $REPO_NAME..."

# Check if repo already exists
if gh repo view "$REPO_NAME" >/dev/null 2>&1; then
    echo "⚠️  Repository already exists — will not overwrite."
    read -rsp "  按 Enter 继续（仅推送）/ Press Enter to push only..." _
else
    gh repo create "$REPO_NAME" \
        --public \
        --description "$REPO_DESC" \
        --enable-issues \
        --enable-wiki \
        --homepage "$REPO_HOMEPAGE" \
        --confirm
    echo "✅ Repository created"
fi

# Get the repository URL
REPO_URL=$(gh repo view "$REPO_NAME" --json sshUrl --jq '.sshUrl' 2>/dev/null ||
           gh repo view "$REPO_NAME" --json url --jq '.url' 2>/dev/null)

if [ -z "$REPO_URL" ]; then
    # Fallback to HTTPS URL
    GITHUB_USER=$(gh api user --jq '.login')
    REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
fi

echo "   Repository URL: $REPO_URL"

# ── 4. Set git remote and push ───────────────────────────────

echo ""
echo "→ Setting git remote and pushing main branch..."

cd "$(dirname "$0")/.." || exit 1

# Remove existing 'origin' remote if present
if git remote get-url origin >/dev/null 2>&1; then
    git remote remove origin
fi

# Add origin using HTTPS (with token embedded for auth)
GITHUB_USER=$(gh api user --jq '.login')
git remote add origin "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

# Push main branch with submodules
echo "   Pushing main branch..."
git branch --set-upstream-to=origin/main main
git push -u origin main 2>&1

echo ""
echo "✅ Push completed"

# ── 5. Set repository topics (GitHub tags) ──────────────────

echo ""
echo "→ Setting repository topics..."
gh api \
    --method PUT \
    -H "Accept: application/vnd.github+json" \
    "/repos/${GITHUB_USER}/${REPO_NAME}/topics" \
    -f names[]="investment-research" \
    -f names[]="ai-agent" \
    -f names[]="stock-analysis" \
    -f names[]="quantitative-finance" \
    -f names[]="value-investing" \
    -f names[]="trading-agents" \
    -f names[]="claude-code-skill" \
    -f names[]="financial-analysis" \
    -f names[]="chinese-stock-market" \
    -f names[]="industry-chain-analysis" > /dev/null 2>&1 || true
echo "✅ Topics set"

# ── 6. Print summary ─────────────────────────────────────────

GITHUB_USER=$(gh api user --jq '.login')
PUBLIC_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎉  发布成功！InvestAgent is live on GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📦  仓库地址  /  Repository:   ${PUBLIC_URL}"
echo "  🔗  Git 地址 / Git URL:        ${REPO_URL}"
echo "  📖  中文文档  / Chinese README:  ${PUBLIC_URL}/blob/main/README_CN.md"
echo "  🐛  Issue 追踪 / Issues:        ${PUBLIC_URL}/issues"
echo "  💡  Tips: 可以去 GitHub 页面给个 Star ⭐"
echo ""
echo "  后续操作建议 / Next steps:"
echo "    1. 去 ${PUBLIC_URL} 确认页面显示正常"
echo "    2. 设置 About 中的 Website / Social links"
echo "    3. 考虑创建 GitHub Wiki 记录更多研究方法"
echo "    4. 开启 GitHub Discussions 供社区讨论"
echo ""
