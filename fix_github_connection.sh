#!/bin/bash
# 快速修复 GitHub 连接问题

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  GitHub 连接问题修复工具${NC}"
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

# 方案 1: 使用 ghproxy 镜像
echo -e "${YELLOW}[方案 1] 使用 ghproxy 镜像...${NC}"

# 提取仓库路径
if [[ $CURRENT_URL == *"github.com"* ]]; then
    REPO_PATH=$(echo $CURRENT_URL | sed 's|https://github.com/||' | sed 's|git@github.com:||' | sed 's|\.git$||')
    MIRROR_URL="https://ghproxy.com/https://github.com/$REPO_PATH.git"
    
    echo -e "${BLUE}修改远程地址为:${NC} $MIRROR_URL"
    git remote set-url origin "$MIRROR_URL"
    
    # 测试连接
    echo -e "${BLUE}测试连接...${NC}"
    if timeout 10 git fetch --dry-run 2>&1 | grep -q "fatal\|error"; then
        echo -e "${RED}✗ 镜像连接失败${NC}"
        MIRROR_FAILED=true
    else
        echo -e "${GREEN}✓ 镜像连接成功${NC}"
        echo ""
        echo -e "${GREEN}修复完成！现在可以使用以下命令：${NC}"
        echo "  git fetch"
        echo "  git push"
        echo "  git pull"
        exit 0
    fi
else
    echo -e "${YELLOW}⚠️  当前地址不是 GitHub，跳过镜像方案${NC}"
    MIRROR_FAILED=true
fi

echo ""

# 方案 2: 使用 SSH
if [ "$MIRROR_FAILED" = true ]; then
    echo -e "${YELLOW}[方案 2] 尝试使用 SSH...${NC}"
    
    if [[ $CURRENT_URL == *"github.com"* ]]; then
        REPO_PATH=$(echo $CURRENT_URL | sed 's|https://github.com/||' | sed 's|git@github.com:||' | sed 's|\.git$||')
        SSH_URL="git@github.com:$REPO_PATH.git"
        
        echo -e "${BLUE}修改远程地址为:${NC} $SSH_URL"
        git remote set-url origin "$SSH_URL"
        
        # 测试 SSH 连接
        echo -e "${BLUE}测试 SSH 连接...${NC}"
        if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated\|You've successfully authenticated"; then
            echo -e "${GREEN}✓ SSH 连接成功${NC}"
            echo ""
            echo -e "${GREEN}修复完成！现在可以使用以下命令：${NC}"
            echo "  git fetch"
            echo "  git push"
            echo "  git pull"
            exit 0
        else
            echo -e "${RED}✗ SSH 连接失败${NC}"
            echo -e "${YELLOW}提示: 需要配置 SSH 密钥${NC}"
            echo ""
            echo "配置步骤："
            echo "  1. 生成密钥: ssh-keygen -t ed25519 -C \"your_email@example.com\""
            echo "  2. 添加公钥到 GitHub: cat ~/.ssh/id_ed25519.pub"
            echo "  3. 测试: ssh -T git@github.com"
        fi
    fi
fi

echo ""
echo -e "${YELLOW}其他解决方案：${NC}"
echo "  1. 检查网络连接: ping github.com"
echo "  2. 配置代理: git config --global http.proxy http://127.0.0.1:7890"
echo "  3. 增加超时: git config --global http.timeout 300"
echo ""
echo -e "${BLUE}详细说明请查看: GitHub连接问题解决方案.md${NC}"
