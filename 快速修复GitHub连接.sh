#!/bin/bash
# 快速修复 GitHub 连接问题

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  快速修复 GitHub 连接${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}✗ 当前目录不是 Git 仓库${NC}"
    exit 1
fi

# 获取当前远程地址
CURRENT_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$CURRENT_URL" ]; then
    echo -e "${RED}✗ 未找到远程仓库${NC}"
    exit 1
fi

echo -e "${BLUE}当前远程地址:${NC} $CURRENT_URL"
echo ""

# 提取仓库路径
if [[ $CURRENT_URL == *"github.com"* ]]; then
    REPO_PATH=$(echo $CURRENT_URL | sed 's|https://github.com/||' | sed 's|git@github.com:||' | sed 's|\.git$||' | sed 's|ghproxy.com/https://github.com/||')
    
    # 方案 1: 使用 ghproxy 镜像
    MIRROR_URL="https://ghproxy.com/https://github.com/$REPO_PATH.git"
    
    echo -e "${YELLOW}[方案 1] 使用 ghproxy 镜像...${NC}"
    echo -e "${BLUE}修改远程地址为:${NC} $MIRROR_URL"
    
    if git remote set-url origin "$MIRROR_URL" 2>&1; then
        echo -e "${GREEN}✓ 远程地址已更新${NC}"
        
        # 测试连接
        echo -e "${BLUE}测试连接...${NC}"
        if timeout 10 git fetch --dry-run 2>&1 | grep -q "fatal\|error"; then
            echo -e "${RED}✗ 镜像连接失败，尝试其他方案...${NC}"
        else
            echo -e "${GREEN}✓ 连接成功！${NC}"
            echo ""
            echo -e "${GREEN}现在可以使用以下命令：${NC}"
            echo "  git fetch"
            echo "  git push"
            echo "  git pull"
            exit 0
        fi
    else
        echo -e "${RED}✗ 修改远程地址失败${NC}"
        echo -e "${YELLOW}请手动执行：${NC}"
        echo "  git remote set-url origin $MIRROR_URL"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  当前地址不是 GitHub，跳过${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}如果仍有问题，请查看: GitHub连接问题解决方案.md${NC}"
