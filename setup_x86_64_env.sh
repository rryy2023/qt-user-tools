#!/bin/bash
# 为 x86_64 打包设置 Python 环境
# 在 M1 Mac 上使用 Rosetta 2 安装 x86_64 版本的依赖

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  设置 x86_64 Python 环境${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 Rosetta 2
if ! pgrep -q oahd; then
    echo -e "${YELLOW}⚠️  需要安装 Rosetta 2${NC}"
    echo "正在安装 Rosetta 2..."
    softwareupdate --install-rosetta --agree-to-license
    echo -e "${GREEN}✓ Rosetta 2 已安装${NC}"
fi

# 检查 arch 命令
if ! command -v arch &> /dev/null; then
    echo -e "${RED}✗ 未找到 arch 命令${NC}"
    exit 1
fi

# 测试 x86_64 Python
echo -e "${BLUE}测试 x86_64 Python...${NC}"
ARCH_TEST=$(arch -x86_64 python3 -c "import platform; print(platform.machine())" 2>/dev/null)

if [ "$ARCH_TEST" != "x86_64" ]; then
    echo -e "${RED}✗ 无法通过 Rosetta 2 运行 x86_64 Python${NC}"
    exit 1
fi

echo -e "${GREEN}✓ x86_64 Python 可用${NC}"
echo ""

# 安装 x86_64 版本的依赖
echo -e "${BLUE}安装 x86_64 版本的依赖包...${NC}"
echo -e "${YELLOW}注意：这将在 x86_64 环境中安装依赖，可能需要一些时间${NC}"
echo ""

# 使用 arch -x86_64 安装依赖
arch -x86_64 python3 -m pip install --upgrade pip --quiet
arch -x86_64 python3 -m pip install -r requirements.txt --force-reinstall --no-binary :all: 2>&1 | grep -E "(Installing|Successfully|ERROR)" || true

# 验证安装
echo ""
echo -e "${BLUE}验证 x86_64 依赖安装...${NC}"
arch -x86_64 python3 -c "
import platform
import sys
print(f'Python 架构: {platform.machine()}')
print(f'Python 版本: {sys.version}')

try:
    import PyQt6
    print('✓ PyQt6 已安装')
except ImportError:
    print('✗ PyQt6 未安装')

try:
    import lxml
    print('✓ lxml 已安装')
except ImportError:
    print('✗ lxml 未安装')

try:
    import requests
    print('✓ requests 已安装')
except ImportError:
    print('✗ requests 未安装')
" 2>&1

echo ""
echo -e "${GREEN}✓ x86_64 环境设置完成${NC}"
echo ""
echo -e "${BLUE}现在可以运行打包命令：${NC}"
echo -e "  ./build_all_platforms.sh --mac-intel"
