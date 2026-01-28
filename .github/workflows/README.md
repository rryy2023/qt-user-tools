# GitHub Actions 工作流说明

## 📦 多平台自动打包

### 工作流文件

1. **`build-all-platforms.yml`** - 三平台自动打包（推荐）
   - macOS ARM64
   - macOS Intel
   - Windows EXE

2. **`build-windows.yml`** - 仅 Windows 打包（保留用于单独测试）

### 触发条件

#### 自动触发

- **推送标签** (`v*`): 自动打包并创建 Release
- **推送到 main/master**: 自动打包（不创建 Release）
- **Pull Request**: 自动打包（用于测试）

#### 手动触发

1. 进入 GitHub 仓库
2. 点击 `Actions` 标签
3. 选择 `Build All Platforms`
4. 点击 `Run workflow`

### 构建平台

| 平台 | Runner | Python 架构 | 输出文件 |
|------|--------|-------------|----------|
| macOS ARM64 | `macos-14` | `arm64` | `.app`, `.dmg`, `.zip` |
| macOS Intel | `macos-14` | `x64` | `.app`, `.dmg`, `.zip` |
| Windows | `windows-latest` | `x64` | `.exe`, `.zip` |

### 输出文件

#### macOS ARM64
- `QiantuTroubleshooter_v0.0.1_macOS-ARM64.dmg`
- `QiantuTroubleshooter_v0.0.1_macOS-ARM64.zip`
- `千图网问题解决工具.app`

#### macOS Intel
- `QiantuTroubleshooter_v0.0.1_macOS-Intel.dmg`
- `QiantuTroubleshooter_v0.0.1_macOS-Intel.zip`
- `千图网问题解决工具.app`

#### Windows
- `QiantuTroubleshooter_v0.0.1_Windows-x64.exe`
- `QiantuTroubleshooter_v0.0.1_Windows-x64.zip`

### 下载构建产物

#### 方法 1：从 Actions 下载

1. 进入 `Actions` 标签
2. 选择最新的运行
3. 在 `Artifacts` 部分下载：
   - `macos-arm64`
   - `macos-intel`
   - `windows-exe`

#### 方法 2：从 Release 下载（标签触发）

1. 进入 `Releases` 标签
2. 选择最新版本
3. 下载所有平台的文件

### 使用示例

#### 发布新版本

```bash
# 1. 更新版本号（在代码中）
VERSION = "0.0.2"

# 2. 提交更改
git add .
git commit -m "Release v0.0.2"
git push

# 3. 创建标签（自动触发打包和 Release）
git tag v0.0.2
git push origin v0.0.2
```

#### 测试构建

```bash
# 推送到 main 分支（自动触发打包，不创建 Release）
git push origin main
```

### 构建时间

- **macOS ARM64**: ~5-10 分钟
- **macOS Intel**: ~5-10 分钟
- **Windows**: ~3-5 分钟
- **总计**: ~15-25 分钟（并行执行）

### 故障排除

#### 问题 1：构建失败

**检查**：
- 查看 Actions 日志
- 检查依赖是否正确
- 验证构建脚本权限

#### 问题 2：Release 未创建

**原因**：
- 只有标签触发才会创建 Release
- 确保标签格式为 `v*`（如 `v0.0.1`）

#### 问题 3：某些平台构建失败

**解决**：
- 查看对应平台的日志
- 检查平台特定的依赖
- 验证构建脚本

### 注意事项

1. **macOS 构建**：需要 macOS runner（GitHub 提供）
2. **并行执行**：三个平台并行构建，节省时间
3. **缓存**：pip 包会被缓存，加速后续构建
4. **Artifacts 保留**：构建产物保留 30 天

### 相关文档

- `Mac打包Windows指南.md` - Mac 上打包 Windows 的说明
- `打包说明_多平台.md` - 本地打包说明
- `build_all_platforms.sh` - 本地打包脚本
