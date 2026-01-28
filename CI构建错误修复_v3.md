# CI 构建错误修复 v3

## 🐛 问题总结

### 1. macOS Intel - gettext 库路径问题

**错误**：
```
Library not loaded: /usr/local/opt/gettext/lib/libintl.8.dylib
Abort trap: 6
```

**根本原因**：
- GitHub Actions 的 macOS runner 可能使用不同的 Homebrew 路径
- Python 在设置时就需要 gettext 库，但此时库路径未配置
- 需要在 Python 设置**之前**安装并配置 gettext

### 2. 所有平台构建失败

**问题**：
- 构建失败但没有详细错误信息
- 无法判断具体失败原因

## ✅ 修复方案

### 1. macOS Intel - 改进 gettext 路径查找

```yaml
- name: Install system dependencies
  run: |
    brew install gettext || true
    # 动态查找 gettext 路径（尝试多个位置）
    GETTEXT_PATH=""
    for path in "$(brew --prefix gettext)" "/opt/homebrew/opt/gettext" "/usr/local/opt/gettext"; do
      if [ -d "$path/lib" ] && [ -f "$path/lib/libintl.8.dylib" ]; then
        GETTEXT_PATH="$path"
        break
      fi
    done
    # 保存到环境变量
    echo "GETTEXT_PATH=$GETTEXT_PATH" >> $GITHUB_ENV
    echo "DYLD_LIBRARY_PATH=$GETTEXT_PATH/lib:$DYLD_LIBRARY_PATH" >> $GITHUB_ENV
```

### 2. 在所有步骤中传递环境变量

```yaml
- name: Install dependencies
  env:
    DYLD_LIBRARY_PATH: ${{ env.DYLD_LIBRARY_PATH }}
    GETTEXT_PATH: ${{ env.GETTEXT_PATH }}
  run: |
    if [ -n "$GETTEXT_PATH" ]; then
      export DYLD_LIBRARY_PATH="$GETTEXT_PATH/lib:$DYLD_LIBRARY_PATH"
      export PATH="$GETTEXT_PATH/bin:$PATH"
    fi
    pip install ...
```

### 3. 改进错误输出

#### build_all_platforms.sh

```bash
# 保存日志并显示
$PYTHON_BIN -m PyInstaller ... 2>&1 | tee /tmp/pyinstaller_arm64.log

# 失败时显示日志
if [ $? -ne 0 ]; then
    echo "最后 50 行日志:"
    tail -50 /tmp/pyinstaller_arm64.log
    return 1
fi
```

#### GitHub Actions

```yaml
- name: Build macOS ARM64
  run: |
    set -x  # 显示详细输出
    ./build_all_platforms.sh --mac-arm64 || {
      echo "Build failed, checking dist directory..."
      ls -la dist/ || true
      exit 1
    }
```

## 📋 修复内容

### `.github/workflows/build-all-platforms.yml`

1. ✅ **macOS Intel**：
   - 在 Python 设置**之前**安装 gettext
   - 动态查找 gettext 路径（支持多个位置）
   - 在所有步骤中传递环境变量
   - 创建符号链接（如果需要）

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

1. **gettext 路径**：实际找到的库路径
2. **构建日志**：PyInstaller 的完整输出
3. **目录内容**：dist 目录的文件列表
4. **环境信息**：Python 路径、工作目录等

## 🚀 下一步

提交修复并观察构建结果：

```bash
git add .
git commit -m "Fix: CI build errors - gettext path detection and error handling"
git push origin main
```

## 📝 相关文件

- `.github/workflows/build-all-platforms.yml` - 已修复
- `build_all_platforms.sh` - 已修复
- `修复CI构建错误_v2.md` - 之前的修复说明
