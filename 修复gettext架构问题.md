# 修复 gettext 架构不匹配问题

## 🐛 问题

在 GitHub Actions 的 macOS runner 上构建 Intel 版本时：

```
mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64')
```

**根本原因**：
- GitHub Actions 的 macOS runner 是 **ARM64** 架构
- 我们使用 `actions/setup-python@v5` 设置了 `architecture: 'x64'` 来获取 **x86_64 Python**
- Homebrew 安装的 gettext 是 **ARM64** 版本
- x86_64 Python 无法链接 ARM64 的库

## ✅ 解决方案

### 方案：使用系统自带的 gettext

macOS 系统自带 `libintl.dylib`，通常是通用二进制（包含 x86_64 和 ARM64），可以直接使用。

**优势**：
- ✅ 不需要安装额外的包
- ✅ 系统库通常是通用二进制，支持多架构
- ✅ 避免架构不匹配问题

### 实现

1. **检查系统 gettext**：
   ```bash
   if [ -f "/usr/lib/libintl.dylib" ]; then
     echo "USE_SYSTEM_GETTEXT=true" >> $GITHUB_ENV
   fi
   ```

2. **设置库路径**：
   ```bash
   if [ "$USE_SYSTEM_GETTEXT" = "true" ]; then
     export DYLD_LIBRARY_PATH="/usr/lib:$DYLD_LIBRARY_PATH"
   fi
   ```

3. **移除 Homebrew gettext 安装**：
   - 不再使用 `brew install gettext`
   - 直接使用系统库

## 📋 修改内容

### `.github/workflows/build-all-platforms.yml`

1. ✅ **移除 Homebrew gettext 安装**
2. ✅ **检查系统 gettext**
3. ✅ **使用系统库路径**

### 关键变化

**之前**：
```yaml
- name: Install system dependencies
  run: |
    brew install gettext || true
    # 复杂的路径查找逻辑...
```

**现在**：
```yaml
- name: Check system gettext
  run: |
    if [ -f "/usr/lib/libintl.dylib" ]; then
      echo "USE_SYSTEM_GETTEXT=true" >> $GITHUB_ENV
    fi
```

## 🔍 验证

构建时会显示：
- Python 架构（应该是 `x86_64`）
- 是否使用系统 gettext
- Python 导入测试

## 🚀 如果仍然失败

如果系统 gettext 不可用，可以尝试：

1. **在 Rosetta 2 环境下安装 x86_64 gettext**：
   ```bash
   arch -x86_64 brew install gettext
   ```

2. **检查 Python 是否真的需要 gettext**：
   - 如果 Python 能正常导入，可能不需要 gettext
   - 某些包（如 PyQt6）可能间接依赖

3. **使用 conda 环境**：
   - conda 可以更好地管理跨架构依赖

## 📝 相关文件

- `.github/workflows/build-all-platforms.yml` - 已修复
- `修复gettext架构问题.md` - 本文档
