#!/bin/bash
# Wine 安装脚本

set -e

echo "=========================================="
echo "  Wine 安装脚本"
echo "=========================================="
echo ""

# 检查 Rosetta 2
if ! pgrep -q oahd; then
    echo "⚠️  检测到需要 Rosetta 2"
    echo "    Wine 需要 Rosetta 2 才能运行"
    read -p "是否现在安装 Rosetta 2? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        softwareupdate --install-rosetta --agree-to-license
    fi
fi

# 检查 Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ 未找到 Homebrew"
    echo "   请先安装 Homebrew: https://brew.sh"
    exit 1
fi

echo "📦 开始安装 Wine..."
echo "   注意：下载可能需要一些时间（约 200MB）"
echo ""

# 尝试安装
if brew install --cask wine-stable; then
    echo ""
    echo "✅ Wine 安装成功！"
    echo ""
    
    # 验证安装
    if command -v wine &> /dev/null; then
        echo "版本信息："
        wine --version
    else
        # 创建符号链接
        echo "创建符号链接..."
        sudo ln -sf "/Applications/Wine Stable.app/Contents/Resources/wine/bin/wine" /usr/local/bin/wine 2>/dev/null || true
        sudo ln -sf "/Applications/Wine Stable.app/Contents/Resources/wine/bin/wine64" /usr/local/bin/wine64 2>/dev/null || true
        
        if command -v wine &> /dev/null; then
            wine --version
        fi
    fi
    
    echo ""
    echo "🎉 安装完成！现在可以使用 Wine 了"
    echo ""
    echo "验证命令："
    echo "  wine --version"
    echo "  winecfg"
else
    echo ""
    echo "❌ 安装失败"
    echo ""
    echo "可能的原因："
    echo "  1. 网络连接问题"
    echo "  2. 下载超时"
    echo ""
    echo "建议："
    echo "  1. 检查网络连接"
    echo "  2. 重试安装命令"
    echo "  3. 或参考 安装Wine指南.md 手动安装"
    exit 1
fi
