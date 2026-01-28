# Windows EXE 打包 - CI/CD 方案

## 🎯 核心优势

✅ **无需本地 Windows 环境**  
✅ **自动化构建流程**  
✅ **稳定可靠**  
✅ **免费使用（GitHub Actions）**  

## 🚀 三步完成

### 1. 推送代码

```bash
git add .
git commit -m "Add CI/CD"
git push origin main
```

### 2. 触发构建

**自动触发**：推送代码后自动开始构建

**手动触发**：
```bash
# 方法 1：使用脚本
./trigger_windows_build.sh

# 方法 2：GitHub CLI
gh workflow run "Build Windows EXE"

# 方法 3：GitHub 网页
# Actions -> Build Windows EXE -> Run workflow
```

### 3. 下载产物

**GitHub 网页**：
- Actions -> 最新运行 -> Artifacts -> windows-exe

**GitHub CLI**：
```bash
gh run download --name windows-exe
```

## 📦 输出文件

构建成功后，在 `dist/windows/` 目录：

- `QiantuTroubleshooter_v0.0.1_Windows-x64.exe`
- `QiantuTroubleshooter_v0.0.1_Windows-x64.zip`

## 🔧 发布版本

```bash
# 1. 更新版本号（build_windows_ci.py）
VERSION = "0.0.2"

# 2. 提交并推送
git add .
git commit -m "Release v0.0.2"
git push

# 3. 创建标签（自动创建 Release）
git tag v0.0.2
git push origin v0.0.2
```

## 📋 文件说明

- `.github/workflows/build-windows.yml` - GitHub Actions 工作流
- `build_windows_ci.py` - CI/CD 打包脚本
- `trigger_windows_build.sh` - 本地触发脚本
- `Mac打包Windows指南.md` - 详细文档

## ⚡ 快速命令

```bash
# 触发构建
./trigger_windows_build.sh

# 查看构建状态
gh run list --workflow="Build Windows EXE"

# 下载最新构建
gh run download --name windows-exe

# 查看构建日志
gh run watch
```

## 🎉 总结

**旧方案**：Mac + Wine → 复杂、不稳定  
**新方案**：GitHub Actions → 简单、可靠、自动化

只需推送代码，一切自动完成！
