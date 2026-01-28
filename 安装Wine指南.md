# Wine 安装指南

## 问题说明

Wine 安装超时，可能是因为：
1. 下载文件较大（约 200MB+）
2. 网络连接问题
3. GitHub 下载速度限制

## 安装方法

### 方法 1：使用 Homebrew（推荐，但可能超时）

```bash
# 直接安装（可能超时）
brew install --cask wine-stable

# 如果超时，可以尝试：
# 1. 检查网络连接
# 2. 使用代理
# 3. 手动下载后安装
```

### 方法 2：手动下载安装

1. **下载 Wine**
   ```bash
   # 下载地址
   https://github.com/Gcenx/macOS_Wine_builds/releases/download/11.0/wine-stable-11.0-osx64.tar.xz
   
   # 或使用 curl 下载
   cd ~/Downloads
   curl -L -o wine-stable.tar.xz \
     "https://github.com/Gcenx/macOS_Wine_builds/releases/download/11.0/wine-stable-11.0-osx64.tar.xz"
   ```

2. **解压并安装**
   ```bash
   # 解压
   tar -xzf wine-stable.tar.xz
   
   # 移动到 Applications
   mv "Wine Stable.app" /Applications/
   
   # 创建符号链接到 PATH
   sudo ln -s /Applications/Wine\ Stable.app/Contents/Resources/wine/bin/wine /usr/local/bin/wine
   sudo ln -s /Applications/Wine\ Stable.app/Contents/Resources/wine/bin/wine64 /usr/local/bin/wine64
   ```

### 方法 3：使用其他 Wine 版本

```bash
# 尝试开发版本（可能更小）
brew install --cask wine@devel

# 或使用 staging 版本
brew install --cask wine@staging
```

### 方法 4：使用 CrossOver（商业软件，更稳定）

CrossOver 是基于 Wine 的商业版本，更稳定但需要付费：
- 下载：https://www.codeweavers.com/crossover

## 安装后验证

```bash
# 检查 Wine 是否安装
which wine
wine --version

# 检查 Wine 配置
winecfg
```

## 注意事项

1. **Rosetta 2 要求**
   - Wine 需要 Rosetta 2（Intel 兼容层）
   - 如果未安装，运行：
     ```bash
     softwareupdate --install-rosetta --agree-to-license
     ```

2. **Gatekeeper 警告**
   - Wine 无法通过 macOS Gatekeeper 检查
   - 需要在"系统设置 > 隐私与安全性"中允许运行
   - 或使用命令：
     ```bash
     xattr -d com.apple.quarantine "/Applications/Wine Stable.app"
     ```

3. **架构限制**
   - Wine 是 x86_64 版本，在 Apple Silicon 上需要 Rosetta 2
   - 性能可能不如原生应用

## 使用 Wine 打包 Windows 应用

安装 Wine 后，构建脚本会自动检测并使用：

```bash
./build_all_platforms.sh --windows
```

**注意：** 在 macOS 上使用 Wine 打包 Windows 应用可能不稳定，建议：
- 在 Windows 系统上直接打包（推荐）
- 使用 CI/CD 服务（如 GitHub Actions）在 Windows 环境中打包

## 替代方案

如果 Wine 安装困难，考虑：

1. **在 Windows 系统上打包**
   - 使用 `build_windows.bat` 脚本
   - 最稳定可靠

2. **使用 GitHub Actions**
   - 创建 `.github/workflows/build.yml`
   - 在 Windows runner 上自动打包

3. **使用 Docker**
   - 在 Windows 容器中打包
   - 需要 Docker Desktop

## 快速安装脚本

创建 `install_wine.sh`：

```bash
#!/bin/bash
set -e

echo "安装 Wine..."

# 检查 Rosetta 2
if ! pgrep -q oahd; then
    echo "需要安装 Rosetta 2..."
    softwareupdate --install-rosetta --agree-to-license
fi

# 尝试 Homebrew 安装
if command -v brew &> /dev/null; then
    echo "使用 Homebrew 安装..."
    brew install --cask wine-stable || {
        echo "Homebrew 安装失败，尝试手动安装..."
        # 手动安装逻辑
    }
else
    echo "未找到 Homebrew，请手动安装"
fi

# 验证安装
if command -v wine &> /dev/null; then
    echo "✓ Wine 安装成功"
    wine --version
else
    echo "✗ Wine 安装失败"
    exit 1
fi
```
