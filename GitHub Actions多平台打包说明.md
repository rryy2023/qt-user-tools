# GitHub Actions 多平台自动打包

## ✅ 已配置

现在推送代码到 GitHub 后，**会自动打包 3 个平台**：

1. ✅ **macOS ARM64** (Apple Silicon)
2. ✅ **macOS Intel** (x86_64)
3. ✅ **Windows** (x64)

## 🚀 使用方法

### 自动触发（推荐）

#### 1. 发布版本（创建 Release）

```bash
# 创建标签
git tag v0.0.2
git push origin v0.0.2
```

**结果**：
- ✅ 自动打包 3 个平台
- ✅ 自动创建 GitHub Release
- ✅ 所有文件上传到 Release

#### 2. 推送到主分支

```bash
git push origin main
```

**结果**：
- ✅ 自动打包 3 个平台
- ✅ 构建产物在 Actions 中可下载
- ❌ 不创建 Release

### 手动触发

1. 进入 GitHub 仓库
2. 点击 `Actions` 标签
3. 选择 `Build All Platforms`
4. 点击 `Run workflow` → `Run workflow`

## 📦 构建产物

### 下载位置

#### 方法 1：从 Actions 下载

1. `Actions` → 最新运行
2. 在 `Artifacts` 部分下载：
   - `macos-arm64` - macOS ARM64 版本
   - `macos-intel` - macOS Intel 版本
   - `windows-exe` - Windows 版本

#### 方法 2：从 Release 下载（标签触发）

1. `Releases` → 最新版本
2. 下载所有平台文件

### 文件命名

- **macOS ARM64**: `QiantuTroubleshooter_v0.0.1_macOS-ARM64.dmg`
- **macOS Intel**: `QiantuTroubleshooter_v0.0.1_macOS-Intel.dmg`
- **Windows**: `QiantuTroubleshooter_v0.0.1_Windows-x64.exe`

## ⏱️ 构建时间

- **macOS ARM64**: ~5-10 分钟
- **macOS Intel**: ~5-10 分钟
- **Windows**: ~3-5 分钟
- **总计**: ~15-25 分钟（并行执行）

## 🔍 工作流文件

### `build-all-platforms.yml`

包含 3 个构建任务：

1. **build-macos-arm64**: 在 macOS runner 上构建 ARM64 版本
2. **build-macos-intel**: 在 macOS runner 上构建 Intel 版本（使用 x64 Python）
3. **build-windows**: 在 Windows runner 上构建 Windows 版本

### 并行执行

三个平台**并行构建**，不互相等待，节省时间。

## 📋 完整工作流示例

### 发布新版本

```bash
# 1. 更新代码
# ... 修改代码 ...

# 2. 提交
git add .
git commit -m "Update features"
git push origin main

# 3. 创建标签（自动触发打包和 Release）
git tag v0.0.2
git push origin v0.0.2

# 4. 等待构建完成（15-25 分钟）

# 5. 在 GitHub 上：
#    - Actions: 查看构建状态
#    - Releases: 下载所有平台文件
```

## 🎯 优势

1. **自动化**：推送即自动构建
2. **多平台**：一次推送，三个平台
3. **并行执行**：节省时间
4. **版本管理**：标签自动创建 Release
5. **无需本地环境**：不需要 Mac/Windows 机器

## ⚠️ 注意事项

1. **标签格式**：必须使用 `v*` 格式（如 `v0.0.1`）才会创建 Release
2. **构建时间**：首次构建可能需要更长时间（下载依赖）
3. **缓存**：后续构建会使用缓存，速度更快
4. **Artifacts 保留**：构建产物保留 30 天

## 🔧 故障排除

### 问题 1：构建失败

**检查**：
- 查看 Actions 日志
- 检查错误信息
- 验证依赖是否正确

### 问题 2：Release 未创建

**原因**：
- 只有标签触发才会创建 Release
- 确保标签格式为 `v*`

### 问题 3：某些平台失败

**解决**：
- 查看对应平台的日志
- 检查平台特定的依赖
- 验证构建脚本

## 📝 相关文件

- `.github/workflows/build-all-platforms.yml` - 多平台工作流（包含所有平台）
- `build_all_platforms.sh` - 本地打包脚本

## 🎉 总结

现在只需：

1. **推送代码** → 自动打包 3 个平台
2. **创建标签** → 自动创建 Release
3. **下载文件** → 从 Actions 或 Release 下载

**完全自动化，无需手动操作！**
