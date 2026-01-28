#!/bin/bash
# 快速修复 Intel 打包问题（M1 Mac）

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  快速修复 Intel 打包问题${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 方案 1: 重新安装关键依赖（快速）
echo -e "${BLUE}方案 1: 重新安装关键依赖（推荐，快速）${NC}"
echo ""

# 安装 cffi（x86_64）
echo -e "${YELLOW}[1/4] 安装 cffi (x86_64)...${NC}"
arch -x86_64 python3 -m pip install cffi --force-reinstall --no-binary :all: --quiet 2>&1 | tail -3

# 安装 cryptography（x86_64）
echo -e "${YELLOW}[2/4] 安装 cryptography (x86_64)...${NC}"
arch -x86_64 python3 -m pip install cryptography --force-reinstall --no-binary :all: --quiet 2>&1 | tail -3

# 安装 lxml（x86_64）- 可能需要编译
echo -e "${YELLOW}[3/4] 安装 lxml (x86_64)...${NC}"
arch -x86_64 python3 -m pip install lxml --force-reinstall --no-binary lxml 2>&1 | tail -5

# 安装 PyQt6（x86_64）- 尝试二进制包
echo -e "${YELLOW}[4/4] 安装 PyQt6 (x86_64)...${NC}"
echo -e "${YELLOW}注意：PyQt6 可能需要较长时间...${NC}"
arch -x86_64 python3 -m pip install PyQt6 PyQt6-Qt6 --force-reinstall 2>&1 | tail -5

# 验证
echo ""
echo -e "${BLUE}验证安装...${NC}"
arch -x86_64 python3 -c "
import platform
print(f'Python 架构: {platform.machine()}')

try:
    import _cffi_backend
    import os
    result = os.popen(f'file {_cffi_backend.__file__}').read()
    if 'x86_64' in result:
        print('✓ _cffi_backend: x86_64 架构正确')
    else:
        print('✗ _cffi_backend: 架构不匹配')
        print(f'  实际: {result}')
except Exception as e:
    print(f'✗ _cffi_backend 检查失败: {e}')

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
" 2>&1

echo ""
echo -e "${GREEN}✓ 修复完成${NC}"
echo ""
echo -e "${BLUE}现在可以尝试打包：${NC}"
echo "  ./build_all_platforms.sh --mac-intel"
