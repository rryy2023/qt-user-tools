#!/bin/bash
# 在 x86_64 环境中安装依赖（M1 Mac 专用）

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  安装 x86_64 版本依赖（M1 Mac）${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 Rosetta 2
if ! arch -x86_64 /usr/bin/true 2>/dev/null; then
    echo -e "${RED}✗ Rosetta 2 未安装或不可用${NC}"
    echo "请运行: softwareupdate --install-rosetta --agree-to-license"
    exit 1
fi

echo -e "${GREEN}✓ Rosetta 2 可用${NC}"
echo ""

# 使用用户隔离安装，避免覆盖 ARM64 依赖
INSTALL_DIR="$HOME/.local/python_x86_64"
export PYTHONUSERBASE="$INSTALL_DIR"
export PATH="$INSTALL_DIR/bin:$PATH"

echo -e "${BLUE}使用隔离安装目录: $INSTALL_DIR${NC}"
echo -e "${YELLOW}注意：这将从源码编译依赖，可能需要 10-30 分钟${NC}"
echo ""

# 升级 pip
echo -e "${BLUE}[1/5] 升级 pip...${NC}"
arch -x86_64 python3 -m pip install --user --upgrade pip --quiet

# 安装编译依赖
echo -e "${BLUE}[2/5] 安装编译工具...${NC}"
if command -v brew &> /dev/null; then
    brew install cmake pkg-config libxml2 libxslt 2>/dev/null || true
fi

# 设置编译环境变量
export LDFLAGS="-L$(brew --prefix libxml2)/lib -L$(brew --prefix libxslt)/lib 2>/dev/null" || true
export CPPFLAGS="-I$(brew --prefix libxml2)/include -I$(brew --prefix libxslt)/include 2>/dev/null" || true

# 安装基础依赖（从源码编译）
echo -e "${BLUE}[3/5] 安装基础依赖（cffi, cryptography）...${NC}"
arch -x86_64 python3 -m pip install --user --force-reinstall --no-binary :all: \
    cffi cryptography 2>&1 | grep -E "(Installing|Successfully|Building|ERROR)" || true

# 安装 lxml（可能需要编译）
echo -e "${BLUE}[4/5] 安装 lxml（可能需要编译）...${NC}"
arch -x86_64 python3 -m pip install --user --force-reinstall --no-binary lxml \
    lxml 2>&1 | grep -E "(Installing|Successfully|Building|ERROR)" || true

# 安装其他依赖
echo -e "${BLUE}[5/5] 安装其他依赖...${NC}"
arch -x86_64 python3 -m pip install --user --force-reinstall \
    beautifulsoup4 requests netifaces 2>&1 | grep -E "(Installing|Successfully|ERROR)" || true

# PyQt6 特殊处理（可能需要较长时间）
echo -e "${BLUE}[额外] 安装 PyQt6（这可能需要较长时间）...${NC}"
echo -e "${YELLOW}提示：如果 PyQt6 安装失败，可以尝试使用预编译的二进制包${NC}"
arch -x86_64 python3 -m pip install --user --force-reinstall \
    PyQt6 PyQt6-Qt6 2>&1 | grep -E "(Installing|Successfully|Building|ERROR)" || {
    echo -e "${YELLOW}PyQt6 从源码编译失败，尝试使用二进制包...${NC}"
    arch -x86_64 python3 -m pip install --user --force-reinstall \
        --only-binary PyQt6 PyQt6 PyQt6-Qt6 2>&1 | grep -E "(Installing|Successfully|ERROR)" || true
}

# 安装 PyInstaller
echo -e "${BLUE}[额外] 安装 PyInstaller...${NC}"
arch -x86_64 python3 -m pip install --user pyinstaller --quiet

# 验证安装
echo ""
echo -e "${BLUE}验证安装...${NC}"
arch -x86_64 python3 -c "
import sys
sys.path.insert(0, '$INSTALL_DIR/lib/python3.10/site-packages')

import platform
print(f'Python 架构: {platform.machine()}')

try:
    import _cffi_backend
    import os
    result = os.popen(f'file {_cffi_backend.__file__}').read()
    if 'x86_64' in result:
        print('✓ _cffi_backend: x86_64')
    else:
        print('✗ _cffi_backend: 架构不匹配')
except Exception as e:
    print(f'✗ _cffi_backend: {e}')

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
echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""
echo -e "${BLUE}使用方法：${NC}"
echo "  1. 修改 build_all_platforms.sh 中的 PYTHON_BIN"
echo "  2. 或使用: PYTHONUSERBASE=$INSTALL_DIR arch -x86_64 python3 ..."
echo ""
echo -e "${YELLOW}注意：打包时需要设置 PYTHONUSERBASE 环境变量${NC}"
