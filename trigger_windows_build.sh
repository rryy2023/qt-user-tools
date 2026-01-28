#!/bin/bash
# 在 Mac 上触发 Windows 打包（使用 GitHub Actions）

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  触发 Windows EXE 云端打包${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}✗ 当前目录不是 Git 仓库${NC}"
    echo "请先初始化 Git 仓库："
    echo "  git init"
    echo "  git remote add origin <your-repo-url>"
    exit 1
fi

# 检查 GitHub CLI
if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}⚠️  GitHub CLI (gh) 未安装${NC}"
    echo ""
    echo "安装方法："
    echo "  brew install gh"
    echo ""
    echo "或使用以下方法："
    echo "  1. 推送代码到 GitHub"
    echo "  2. 在 GitHub 网页上手动触发 Actions"
    echo "  3. 或使用 GitHub API"
    exit 1
fi

# 检查是否已登录
if ! gh auth status > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  未登录 GitHub${NC}"
    echo "正在登录..."
    gh auth login
fi

# 获取仓库信息
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")

if [ -z "$REPO" ]; then
    echo -e "${YELLOW}⚠️  无法获取仓库信息${NC}"
    echo "请确保："
    echo "  1. 已设置远程仓库：git remote add origin <repo-url>"
    echo "  2. 已登录 GitHub CLI：gh auth login"
    exit 1
fi

echo -e "${GREEN}✓ 仓库: $REPO${NC}"
echo ""

# 触发工作流
echo -e "${BLUE}触发 Windows 打包工作流...${NC}"
if gh workflow run "Build Windows EXE" --repo "$REPO" 2>/dev/null; then
    echo -e "${GREEN}✓ 工作流已触发${NC}"
    echo ""
    echo -e "${BLUE}查看运行状态：${NC}"
    echo "  gh run list --workflow='Build Windows EXE'"
    echo ""
    echo -e "${BLUE}查看最新运行：${NC}"
    echo "  gh run watch"
    echo ""
    echo -e "${BLUE}下载构建产物：${NC}"
    echo "  gh run download --name windows-exe"
else
    echo -e "${RED}✗ 触发失败${NC}"
    echo ""
    echo "替代方法："
    echo "  1. 推送代码到 GitHub"
    echo "  2. 在 GitHub 网页上：Actions -> Build Windows EXE -> Run workflow"
    exit 1
fi
