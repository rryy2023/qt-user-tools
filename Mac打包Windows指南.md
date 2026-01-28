# Mac 上打包 Windows EXE - 现代方案

## 🎯 问题

在 Mac 上直接打包 Windows EXE 需要 Wine 等工具，配置复杂且不稳定。

## ✅ 解决方案：使用 GitHub Actions（推荐）

### 优势

1. **无需本地 Windows 环境** - 云端自动打包
2. **自动化** - 推送代码即自动构建
3. **稳定可靠** - 使用官方 Windows 运行环境
4. **免费** - GitHub Actions 对公开仓库免费
5. **版本管理** - 自动创建 Release 和下载链接

## 🚀 快速开始

### 步骤 1：设置 GitHub Actions

工作流文件已创建：`.github/workflows/build-all-platforms.yml`（包含 Windows 构建）

### 步骤 2：推送代码到 GitHub

```bash
# 如果还没有 Git 仓库
git init
git add .
git commit -m "Initial commit"

# 添加远程仓库
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### 步骤 3：触发构建

#### 方法 1：自动触发（推荐）

推送代码或创建标签：

```bash
# 推送代码（自动触发）
git push

# 或创建标签（自动触发并创建 Release）
git tag v0.0.1
git push origin v0.0.1
```

#### 方法 2：手动触发

1. 在 GitHub 网页上：
   - 进入 `Actions` 标签
   - 选择 `Build All Platforms` 工作流
   - 点击 `Run workflow`

2. 使用 GitHub CLI（在 Mac 上）：

```bash
# 安装 GitHub CLI
brew install gh

# 登录
gh auth login

# 触发工作流
gh workflow run "Build All Platforms"
```

### 步骤 4：下载构建产物

#### 方法 1：GitHub 网页

1. 进入 `Actions` 标签
2. 选择最新的运行
3. 在 `Artifacts` 部分下载 `windows-exe`

#### 方法 2：GitHub CLI

```bash
# 查看运行列表
gh run list --workflow="Build All Platforms"

# 下载最新构建
gh run download --name windows-exe

# 或指定运行 ID
gh run download <run-id> --name windows-exe
```

#### 方法 3：Release（如果使用标签）

创建标签后，GitHub Actions 会自动创建 Release，可直接下载。

## 📋 工作流配置说明

### 触发条件

- **手动触发**：在 GitHub 网页上手动运行
- **标签触发**：创建 `v*` 标签时自动触发并创建 Release
- **推送触发**：推送到 `main`/`master` 分支时触发
- **PR 触发**：创建 Pull Request 时触发（用于测试）

### 构建环境

- **操作系统**：`windows-latest`（Windows Server 2022）
- **Python 版本**：3.10
- **架构**：x64

### 缓存

- 自动缓存 pip 包，加速后续构建

## 🔧 本地开发（可选）

如果需要本地测试 Windows 打包逻辑，可以使用 Docker：

```bash
# 使用 Windows 容器（需要 Docker Desktop）
docker run --rm -v "$(pwd):/workspace" -w /workspace \
  mcr.microsoft.com/windows/servercore:ltsc2022 \
  powershell -Command "python build_windows_ci.py"
```

**注意**：Docker Windows 容器需要 Windows 主机，Mac 上无法运行。

## 📦 输出文件

构建成功后，会生成：

- `QiantuTroubleshooter_v0.0.1_Windows-x64.exe` - 可执行文件
- `QiantuTroubleshooter_v0.0.1_Windows-x64.zip` - ZIP 压缩包

文件命名遵循规范：`{APP_NAME_EN}_v{VERSION}_Windows-x64.{ext}`

## 🎯 工作流示例

### 日常开发

```bash
# 1. 开发代码
# ... 修改代码 ...

# 2. 提交并推送
git add .
git commit -m "Update features"
git push

# 3. GitHub Actions 自动构建
# 4. 在 Actions 页面下载构建产物
```

### 发布版本

```bash
# 1. 更新版本号（在 build_windows_ci.py 中）
VERSION = "0.0.2"

# 2. 提交更改
git add .
git commit -m "Release v0.0.2"
git push

# 3. 创建标签
git tag v0.0.2
git push origin v0.0.2

# 4. GitHub Actions 自动：
#    - 构建 Windows EXE
#    - 创建 GitHub Release
#    - 上传构建产物到 Release
```

## 🔍 监控构建状态

### GitHub CLI

```bash
# 查看工作流运行列表
gh run list --workflow="Build All Platforms"

# 查看最新运行状态
gh run watch

# 查看运行日志
gh run view <run-id> --log
```

### GitHub 网页

- `Actions` 标签显示所有工作流运行
- 绿色 ✓ 表示成功，红色 ✗ 表示失败
- 点击运行可查看详细日志

## 🛠️ 故障排除

### 问题 1：工作流未触发

**检查**：
- 确保 `.github/workflows/build-all-platforms.yml` 存在
- 检查触发条件是否满足
- 查看 GitHub 仓库设置中的 Actions 权限

### 问题 2：构建失败

**查看日志**：
```bash
gh run view <run-id> --log
```

**常见原因**：
- 依赖安装失败：检查 `requirements.txt`
- PyInstaller 错误：检查 `build_windows_ci.py`
- 路径问题：确保文件路径正确

### 问题 3：无法下载构建产物

**检查**：
- 构建是否成功完成
- Artifacts 是否已过期（默认保留 30 天）
- 是否有下载权限

## 📝 最佳实践

1. **版本管理**：使用语义化版本（Semantic Versioning）
2. **标签发布**：使用标签触发 Release 创建
3. **测试构建**：在 PR 中测试构建，确保主分支稳定
4. **缓存优化**：利用 GitHub Actions 缓存加速构建
5. **安全**：不要在代码中硬编码敏感信息

## 🔗 相关文件

- `.github/workflows/build-all-platforms.yml` - 多平台 GitHub Actions 工作流（包含 Windows）
- `build_windows_ci.py` - CI/CD 优化的打包脚本
- `build_windows.py` - 原始打包脚本（Windows 本地使用）

## 🎉 总结

使用 GitHub Actions 是在 Mac 上打包 Windows EXE 的最佳方案：

- ✅ 无需本地 Windows 环境
- ✅ 自动化构建流程
- ✅ 稳定可靠
- ✅ 免费使用
- ✅ 版本管理集成

只需推送代码，GitHub Actions 会自动完成所有工作！
