#!/bin/bash
# 创建 macOS DMG 安装包

set -e

APP_NAME="千图网问题解决工具"
APP_BUNDLE="${APP_NAME}.app"
DMG_NAME="${APP_NAME}_V0.0.1.dmg"
DMG_TEMP="dmg_temp"
DMG_TEMP_DIR="dmg_temp_dir"

# 检查 App Bundle 是否存在
if [ ! -d "dist/${APP_BUNDLE}" ]; then
    echo "✗ 错误: 未找到 App Bundle: dist/${APP_BUNDLE}"
    echo "请先运行: ./build_app_bundle.sh"
    exit 1
fi

echo "开始创建 DMG 安装包..."
echo ""

# 清理旧的临时文件
rm -rf "${DMG_TEMP_DIR}" "${DMG_TEMP}.dmg" "dist/${DMG_NAME}" 2>/dev/null

# 创建临时目录
mkdir -p "${DMG_TEMP_DIR}"

# 复制 App Bundle 到临时目录
echo "复制 App Bundle..."
cp -R "dist/${APP_BUNDLE}" "${DMG_TEMP_DIR}/"

# 创建 Applications 文件夹的符号链接（方便拖拽安装）
echo "创建 Applications 链接..."
ln -s /Applications "${DMG_TEMP_DIR}/Applications"

# 创建 README 文件
cat > "${DMG_TEMP_DIR}/README.txt" << 'EOF'
千图网问题解决工具 V0.0.1
============================

安装说明：
1. 将"千图网问题解决工具.app"拖拽到"Applications"文件夹
2. 在应用程序中找到并打开"千图网问题解决工具"
3. 如果提示"无法打开"，请：
   - 右键点击应用，选择"打开"
   - 或在"系统设置" > "隐私与安全性"中允许

功能说明：
- 一键修复常见问题
- 自动获取最优IP地址
- 权限提升功能（类似SwitchHosts!）
- 查看系统信息和hosts配置

注意：
- 修改hosts文件时会提示输入密码
- 应用启动不需要管理员权限
EOF

# 创建 DMG
echo "创建 DMG 文件..."
hdiutil create -volname "${APP_NAME}" \
    -srcfolder "${DMG_TEMP_DIR}" \
    -ov -format UDZO \
    "dist/${DMG_NAME}" \
    > /dev/null 2>&1

# 清理临时文件
rm -rf "${DMG_TEMP_DIR}"

# 验证 DMG
if [ -f "dist/${DMG_NAME}" ]; then
    echo ""
    echo "✅ DMG 创建成功！"
    echo ""
    echo "📦 DMG 信息："
    echo "  - 文件名: ${DMG_NAME}"
    echo "  - 位置: dist/${DMG_NAME}"
    echo "  - 大小: $(ls -lh dist/${DMG_NAME} | awk '{print $5}')"
    echo ""
    echo "🚀 使用方法："
    echo "  1. 双击打开 DMG 文件"
    echo "  2. 将应用拖拽到 Applications 文件夹"
    echo "  3. 在启动台或应用程序中找到应用"
else
    echo "✗ DMG 创建失败"
    exit 1
fi
