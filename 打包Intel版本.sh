#!/bin/bash
# 在 M1 Mac 上打包 Intel 版本的简化脚本

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  M1 Mac 打包 Intel 版本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 Rosetta 2
if ! arch -x86_64 /usr/bin/true 2>/dev/null; then
    echo -e "${RED}✗ Rosetta 2 未安装${NC}"
    exit 1
fi

# 检查依赖架构
echo -e "${BLUE}检查依赖架构...${NC}"
ARCH_CHECK=$(arch -x86_64 python3 -c "
import _cffi_backend
import os
result = os.popen('file ' + _cffi_backend.__file__).read()
if 'universal' in result or 'x86_64' in result:
    print('OK')
else:
    print('FAIL')
" 2>&1)

if [ "$ARCH_CHECK" != "OK" ]; then
    echo -e "${YELLOW}⚠️  依赖架构可能不匹配，尝试重新安装...${NC}"
    echo ""
    echo -e "${BLUE}重新安装关键依赖为 Universal Binary...${NC}"
    
    # 重新安装关键依赖
    arch -x86_64 python3 -m pip install --force-reinstall --upgrade \
        cffi cryptography lxml PyQt6 PyQt6-Qt6 2>&1 | grep -E "(Installing|Successfully|ERROR)" || true
    
    echo ""
fi

# 使用 arch -x86_64 直接打包
echo -e "${BLUE}开始打包 Intel 版本...${NC}"
echo ""

PYTHON_BIN="arch -x86_64 python3"
BUILD_DIR="build/mac_intel"
DIST_DIR="dist/mac_intel"
APP_NAME="千图网问题解决工具"

mkdir -p "$BUILD_DIR"
mkdir -p "$DIST_DIR"

# 安装依赖（如果需要）
echo -e "${BLUE}检查依赖...${NC}"
$PYTHON_BIN -m pip install -r requirements.txt --quiet 2>/dev/null || true

# 打包
echo -e "${BLUE}使用 PyInstaller 打包...${NC}"
$PYTHON_BIN -m PyInstaller build_app.spec \
    --workpath "$BUILD_DIR" \
    --distpath "$DIST_DIR" \
    --clean \
    --noconfirm 2>&1 | grep -E "(INFO|WARNING|ERROR|Building|Successfully)" | tail -20

# 检查结果
if [ -d "$DIST_DIR/$APP_NAME.app" ]; then
    echo ""
    echo -e "${GREEN}✓ macOS Intel 打包成功${NC}"
    echo -e "  输出: $DIST_DIR/$APP_NAME.app"
    
    # 创建 ZIP
    ZIP_NAME="QiantuTroubleshooter_v0.0.1_macOS-Intel.zip"
    cd "$DIST_DIR"
    zip -r -q "$ZIP_NAME" "$APP_NAME.app" 2>/dev/null || zip -r "$ZIP_NAME" "$APP_NAME.app"
    cd - > /dev/null
    
    if [ -f "$DIST_DIR/$ZIP_NAME" ]; then
        echo -e "${GREEN}✓ ZIP 创建成功: $DIST_DIR/$ZIP_NAME${NC}"
    fi
else
    echo ""
    echo -e "${RED}✗ macOS Intel 打包失败${NC}"
    exit 1
fi
