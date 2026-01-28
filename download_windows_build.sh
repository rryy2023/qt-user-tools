#!/bin/bash
# 从 GitHub Actions 下载 Windows 构建产物

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  下载 Windows 构建产物${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 GitHub CLI
if ! command -v gh &> /dev/null; then
    echo -e "${RED}✗ GitHub CLI 未安装${NC}"
    echo "安装方法：brew install gh"
    exit 1
fi

# 获取仓库信息
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")

if [ -z "$REPO" ]; then
    echo -e "${YELLOW}无法获取仓库信息，请手动指定：${NC}"
    read -p "GitHub 仓库 (格式: owner/repo): " REPO
fi

echo -e "${BLUE}仓库: ${REPO}${NC}"
echo ""

# 获取最新的工作流运行
echo -e "${BLUE}查找最新的构建...${NC}"
RUN_ID=$(gh run list --workflow="Build Windows EXE" --repo "$REPO" --limit 1 --json databaseId -q '.[0].databaseId' 2>/dev/null || echo "")

if [ -z "$RUN_ID" ]; then
    echo -e "${RED}✗ 未找到构建记录${NC}"
    echo "请先触发构建："
    echo "  ./trigger_windows_build.sh"
    exit 1
fi

echo -e "${GREEN}找到构建: #${RUN_ID}${NC}"

# 检查构建状态
STATUS=$(gh run view "$RUN_ID" --repo "$REPO" --json status -q '.status' 2>/dev/null || echo "unknown")

if [ "$STATUS" != "completed" ]; then
    echo -e "${YELLOW}⚠️  构建尚未完成 (状态: $STATUS)${NC}"
    echo "等待构建完成..."
    gh run watch "$RUN_ID" --repo "$REPO"
fi

# 下载产物
echo -e "${BLUE}下载构建产物...${NC}"
mkdir -p dist/windows

gh run download "$RUN_ID" --repo "$REPO" --dir dist/windows --pattern "windows-*"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 下载完成${NC}"
    echo ""
    echo -e "${BLUE}文件位置:${NC}"
    ls -lh dist/windows/
else
    echo -e "${RED}✗ 下载失败${NC}"
    exit 1
fi
