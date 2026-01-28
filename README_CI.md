# CI/CD 打包说明

## 🚀 快速开始

### Mac 上打包 Windows EXE

**推荐方案：使用 GitHub Actions**

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "Add CI/CD"
   git push
   ```

2. **触发构建**
   - 自动：推送代码到 main 分支
   - 手动：GitHub 网页 -> Actions -> Run workflow
   - 脚本：`./trigger_windows_build.sh`

3. **下载构建产物**
   - GitHub 网页：Actions -> Artifacts
   - GitHub CLI：`gh run download --name windows-exe`

## 📋 工作流说明

### 自动触发条件

- ✅ 推送到 `main`/`master` 分支
- ✅ 创建 `v*` 标签（自动创建 Release）
- ✅ Pull Request（用于测试）

### 手动触发

```bash
# 使用脚本
./trigger_windows_build.sh

# 或使用 GitHub CLI
gh workflow run "Build Windows EXE"
```

## 📦 输出文件

- `QiantuTroubleshooter_v0.0.1_Windows-x64.exe`
- `QiantuTroubleshooter_v0.0.1_Windows-x64.zip`

## 🔗 详细文档

查看 `Mac打包Windows指南.md` 获取完整说明。
