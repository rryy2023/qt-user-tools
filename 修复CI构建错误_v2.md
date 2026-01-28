# 修复 GitHub Actions CI 构建错误 v2

## 🐛 问题分析

### 1. macOS Intel - gettext 库路径问题

**错误**：
```
Library not loaded: /usr/local/opt/gettext/lib/libintl.8.dylib
```

**原因**：
- gettext 已安装，但 Python 找不到库文件
- GitHub Actions 的 macOS runner 可能使用不同的 Homebrew 路径
- 需要设置正确的库路径和符号链接

### 2. 所有平台构建失败

**问题**：
- 构建脚本失败但没有详细错误信息
- 无法判断具体失败原因

## ✅ 修复方案

### 1. macOS Intel - gettext 路径修复

```yaml
- name: Install system dependencies
  run: |
    brew install gettext || true
    # 查找 gettext 库的实际路径
    GETTEXT_PATH=$(brew --prefix gettext 2>/dev/null || echo "/opt/homebrew/opt/gettext" || echo "/usr/local/opt/gettext")
    # 设置环境变量
    echo "GETTEXT_PATH=$GETTEXT_PATH" >> $GITHUB_ENV
    echo "DYLD_LIBRARY_PATH=$GETTEXT_PATH/lib:$DYLD_LIBRARY_PATH" >> $GITHUB_ENV
    # 创建符号链接（如果需要）
    if [ ! -f "/usr/local/opt/gettext/lib/libintl.8.dylib" ] && [ -f "$GETTEXT_PATH/lib/libintl.8.dylib" ]; then
      sudo mkdir -p /usr/local/opt/gettext/lib || true
      sudo ln -sf "$GETTEXT_PATH/lib/libintl.8.dylib" /usr/local/opt/gettext/lib/libintl.8.dylib || true
    fi
```

### 2. 改进错误输出

#### build_all_platforms.sh

```bash
# 保存日志到文件
$PYTHON_BIN -m PyInstaller ... 2>&1 | tee /tmp/pyinstaller_arm64.log

# 失败时显示日志
if [ $? -ne 0 ]; then
    echo "最后 50 行日志:"
    tail -50 /tmp/pyinstaller_arm64.log
    return 1
fi
```

#### GitHub Actions 工作流

```yaml
- name: Build macOS ARM64
  run: |
    set -x  # 显示详细输出
    ./build_all_platforms.sh --mac-arm64 || {
      echo "Build failed, checking dist directory..."
      ls -la dist/ || true
      ls -la dist/mac_arm64/ || true
      exit 1
    }
```

### 3. 改进验证步骤

```yaml
- name: Verify build output
  run: |
    echo "Checking build output..."
    # 显示目录内容
    ls -la dist/mac_arm64/ || exit 1
    # 使用 find 命令检查（更可靠）
    if [ -n "$(find dist/mac_arm64 -name '*.app' -o -name '*.dmg' -o -name '*.zip' 2>/dev/null | head -1)" ]; then
      echo "✓ Build artifacts found"
    else
      echo "Error: No build artifacts found"
      find dist/mac_arm64 -type f -o -type d | head -20
      exit 1
    fi
```

## 📋 修复内容

### `.github/workflows/build-all-platforms.yml`

1. ✅ **macOS Intel**：
   - 在 Python 设置前安装 gettext
   - 动态查找 gettext 路径
   - 创建符号链接
   - 设置 DYLD_LIBRARY_PATH

2. ✅ **所有平台**：
   - 添加 `set -x` 显示详细输出
   - 构建失败时显示目录内容
   - 改进验证步骤的错误信息

### `build_all_platforms.sh`

1. ✅ 保存 PyInstaller 日志到文件
2. ✅ 失败时显示最后 50 行日志
3. ✅ 显示 Python 路径和输出目录

## 🔍 调试信息

现在构建失败时会显示：

1. **构建日志**：PyInstaller 的完整输出
2. **目录内容**：dist 目录的文件列表
3. **环境信息**：Python 路径、工作目录等

## 🚀 下一步

提交修复并观察构建结果：

```bash
git add .
git commit -m "Fix: CI build errors - gettext path and error handling"
git push origin main
```

## 📝 相关文件

- `.github/workflows/build-all-platforms.yml` - 已修复
- `build_all_platforms.sh` - 已修复
- `修复CI构建错误.md` - 之前的修复说明
