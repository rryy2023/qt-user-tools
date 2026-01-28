#!/bin/bash
# 创建 x86_64 虚拟环境（M1 Mac 专用）

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  创建 x86_64 虚拟环境${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 Rosetta 2
if ! arch -x86_64 /usr/bin/true 2>/dev/null; then
    echo -e "${RED}✗ Rosetta 2 未安装${NC}"
    echo "请运行: softwareupdate --install-rosetta --agree-to-license"
    exit 1
fi

echo -e "${GREEN}✓ Rosetta 2 可用${NC}"
echo ""

# 检查是否已存在虚拟环境
if [ -d "venv_x86_64" ]; then
    echo -e "${YELLOW}虚拟环境已存在，是否重新创建？${NC}"
    read -p "输入 y 重新创建，n 跳过 (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}删除旧虚拟环境...${NC}"
        rm -rf venv_x86_64
    else
        echo -e "${GREEN}使用现有虚拟环境${NC}"
        exit 0
    fi
fi

# 创建虚拟环境
echo -e "${BLUE}创建 x86_64 虚拟环境...${NC}"
arch -x86_64 python3 -m venv venv_x86_64

# 激活虚拟环境并验证
echo -e "${BLUE}验证虚拟环境架构...${NC}"
source venv_x86_64/bin/activate

ARCH=$(python -c "import platform; print(platform.machine())" 2>/dev/null)
if [ "$ARCH" != "x86_64" ]; then
    echo -e "${RED}✗ 虚拟环境架构不正确: $ARCH${NC}"
    rm -rf venv_x86_64
    exit 1
fi

echo -e "${GREEN}✓ 虚拟环境架构: $ARCH${NC}"
echo ""

# 升级 pip
echo -e "${BLUE}升级 pip...${NC}"
pip install --upgrade pip --quiet

# 安装依赖
echo -e "${BLUE}安装依赖包...${NC}"
echo -e "${YELLOW}这可能需要一些时间（5-15分钟）${NC}"
pip install -r requirements.txt

# 验证安装
echo ""
echo -e "${BLUE}验证依赖安装...${NC}"
python -c "
import platform
print(f'Python 架构: {platform.machine()}')

try:
    import PyQt6
    print('✓ PyQt6 已安装')
except Exception as e:
    print(f'✗ PyQt6: {e}')

try:
    import lxml
    print('✓ lxml 已安装')
except Exception as e:
    print(f'✗ lxml: {e}')

try:
    import _cffi_backend
    import os
    result = os.popen('file ' + _cffi_backend.__file__).read()
    if 'x86_64' in result:
        print('✓ _cffi_backend: x86_64 架构正确')
    else:
        print('✗ _cffi_backend: 架构检查失败')
except Exception as e:
    print(f'✗ _cffi_backend: {e}')
" 2>&1

deactivate

echo ""
echo -e "${GREEN}✓ 虚拟环境创建完成${NC}"
echo ""
echo -e "${BLUE}使用方法：${NC}"
echo "  1. 直接运行打包: ./build_all_platforms.sh --mac-intel"
echo "  2. 脚本会自动检测并使用 venv_x86_64 虚拟环境"
echo ""
echo -e "${YELLOW}注意：虚拟环境已包含所有依赖，可以直接打包${NC}"
