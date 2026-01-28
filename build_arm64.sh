#!/bin/bash
# ARM64架构打包脚本

echo "检查Python环境..."

# 查找ARM64架构的Python
PYTHON_BIN=""
for py in python3 python3.11 python3.12; do
    if command -v $py &> /dev/null; then
        ARCH=$($py -c "import platform; print(platform.machine())" 2>/dev/null)
        if [ "$ARCH" = "arm64" ]; then
            PYTHON_BIN=$(which $py)
            echo "✓ 找到ARM64 Python: $PYTHON_BIN"
            break
        fi
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "✗ 未找到ARM64架构的Python"
    echo "请安装ARM64版本的Python和PyQt6"
    exit 1
fi

# 安装所有依赖
echo "检查并安装依赖..."
if [ -f "requirements.txt" ]; then
    echo "从 requirements.txt 安装依赖..."
    $PYTHON_BIN -m pip install -r requirements.txt --quiet
else
    # 如果没有requirements.txt，安装必要的包
    echo "安装必要的依赖包..."
    $PYTHON_BIN -m pip install PyQt6 PyQt6-Qt6 beautifulsoup4 lxml requests netifaces pyinstaller --quiet
fi

# 验证关键模块
echo "验证关键模块..."
$PYTHON_BIN -c "import PyQt6; import bs4; import requests; import lxml; print('✓ 所有依赖已安装')" 2>&1
if [ $? -ne 0 ]; then
    echo "✗ 依赖安装失败，请检查"
    exit 1
fi

# 使用ARM64 Python打包
echo "开始打包..."
$PYTHON_BIN build_no_sign.py
