# macOS DMG 打包说明

## 打包步骤

### 方法一：一键打包（推荐）
```bash
./build_app_bundle.sh
```

这个脚本会自动：
1. 检查并安装依赖
2. 创建 App Bundle (.app)
3. 创建 DMG 安装包

### 方法二：分步打包

#### 1. 创建 App Bundle
```bash
./build_app_bundle.sh
# 或者
python3 build_app_bundle.py
```

#### 2. 创建 DMG
```bash
./create_dmg.sh
```

## 输出文件

- **App Bundle**: `dist/千图网问题解决工具.app`
- **DMG 安装包**: `dist/千图网问题解决工具_V0.0.1.dmg`

## DMG 内容

DMG 文件包含：
- `千图网问题解决工具.app` - 应用程序
- `Applications` - 指向系统应用程序文件夹的链接（方便拖拽安装）
- `README.txt` - 安装说明

## 额外要求

### 1. 应用图标（可选）

如果需要自定义应用图标，需要：
1. 准备 `.icns` 格式的图标文件
2. 在 `build_app.spec` 中指定图标路径：
   ```python
   icon='path/to/icon.icns',
   ```

### 2. 代码签名（可选）

如果需要正式签名（非 ad-hoc）：
1. 需要 Apple Developer 账号
2. 在 `build_app.spec` 中设置：
   ```python
   codesign_identity='Developer ID Application: Your Name (TEAM_ID)',
   ```

### 3. 公证（可选）

如果要通过 Gatekeeper 检查：
1. 需要 Apple Developer 账号
2. 使用 `notarytool` 或 `altool` 进行公证

## 当前配置

- **签名方式**: ad-hoc（临时签名）
- **架构**: ARM64 (Apple Silicon)
- **版本**: V0.0.1
- **Bundle ID**: com.qiantu.troubleshooter

## 注意事项

1. **首次运行**: 用户可能需要右键点击应用选择"打开"
2. **系统设置**: 如果被阻止，需要在"系统设置" > "隐私与安全性"中允许
3. **权限提升**: 修改hosts文件时会自动提示输入密码（类似SwitchHosts!）

## 测试 DMG

1. 双击打开 DMG 文件
2. 将应用拖拽到 Applications 文件夹
3. 在启动台或应用程序中找到并运行
