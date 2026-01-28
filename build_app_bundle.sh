#!/bin/bash
# 创建 macOS App Bundle 并打包为 DMG

# 检查是否使用 sudo（不需要 sudo，但如果在 sudo 环境下，保留环境变量）
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  警告: 检测到使用 sudo 运行"
    echo "   打包脚本不需要管理员权限"
    echo "   建议: 不使用 sudo 运行此脚本"
    echo ""
    # 保留当前用户的环境变量
    export HOME=$(eval echo ~${SUDO_USER:-$USER})
    export USER=${SUDO_USER:-$USER}
    # 保留 PATH（如果可能）
    if [ -n "$SUDO_USER" ]; then
        export PATH=$(su - $SUDO_USER -c 'echo $PATH')
    fi
fi

echo "检查Python环境..."

# 查找ARM64架构的Python
PYTHON_BIN=""

# 首先尝试直接使用 python3（可能在 conda 环境中）
if command -v python3 &> /dev/null; then
    ARCH=$(python3 -c "import platform; print(platform.machine())" 2>/dev/null)
    if [ "$ARCH" = "arm64" ]; then
        PYTHON_BIN=$(which python3)
        echo "✓ 找到ARM64 Python: $PYTHON_BIN"
    fi
fi

# 如果还没找到，尝试其他版本
if [ -z "$PYTHON_BIN" ]; then
    for py in python3.11 python3.12 python3.13; do
        if command -v $py &> /dev/null; then
            ARCH=$($py -c "import platform; print(platform.machine())" 2>/dev/null)
            if [ "$ARCH" = "arm64" ]; then
                PYTHON_BIN=$(which $py)
                echo "✓ 找到ARM64 Python: $PYTHON_BIN"
                break
            fi
        fi
    done
fi

# 如果还是没找到，尝试使用当前环境的 python（可能是 conda）
if [ -z "$PYTHON_BIN" ]; then
    if command -v python &> /dev/null; then
        ARCH=$(python -c "import platform; print(platform.machine())" 2>/dev/null)
        if [ "$ARCH" = "arm64" ]; then
            PYTHON_BIN=$(which python)
            echo "✓ 找到ARM64 Python: $PYTHON_BIN"
        fi
    fi
fi

# 最后检查：如果系统是 ARM64，但检测失败，给出更详细的错误信息
if [ -z "$PYTHON_BIN" ]; then
    echo "✗ 未找到ARM64架构的Python"
    echo ""
    echo "调试信息:"
    echo "  当前系统架构: $(uname -m)"
    echo "  当前用户: $USER"
    echo "  是否使用 sudo: $([ "$EUID" -eq 0 ] && echo "是" || echo "否")"
    if command -v python3 &> /dev/null; then
        echo "  python3 路径: $(which python3)"
        echo "  python3 架构: $(python3 -c "import platform; print(platform.machine())" 2>/dev/null || echo "检测失败")"
    else
        echo "  python3: 未找到"
    fi
    if command -v python &> /dev/null; then
        echo "  python 路径: $(which python)"
        echo "  python 架构: $(python -c "import platform; print(platform.machine())" 2>/dev/null || echo "检测失败")"
    else
        echo "  python: 未找到"
    fi
    echo ""
    if [ "$EUID" -eq 0 ]; then
        echo "⚠️  检测到使用 sudo 运行"
        echo "   建议: 退出 sudo，直接运行: ./build_app_bundle.sh"
        echo ""
    fi
    echo "请确保:"
    echo "  1. 已安装ARM64版本的Python"
    echo "  2. Python 在 PATH 中"
    echo "  3. 如果使用 conda，确保环境已激活"
    echo "  4. 不要使用 sudo 运行此脚本"
    exit 1
fi

# 安装所有依赖
echo "检查并安装依赖..."
if [ -f "requirements.txt" ]; then
    echo "从 requirements.txt 安装依赖..."
    $PYTHON_BIN -m pip install -r requirements.txt --quiet
else
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
echo "开始创建 App Bundle..."
$PYTHON_BIN build_app_bundle.py

# 如果 App Bundle 创建成功，创建 DMG
if [ -d "dist/千图网问题解决工具.app" ]; then
    echo ""
    echo "App Bundle 创建成功，开始创建 DMG..."
    chmod +x create_dmg.sh
    ./create_dmg.sh
else
    echo "✗ App Bundle 创建失败"
    exit 1
fi
