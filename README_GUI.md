# 千图网问题解决工具 - GUI版本

基于PyQt6开发的可视化桌面应用，提供友好的图形界面来解决千图网使用过程中的常见问题。

## 功能特性

- ✅ **问题快速修复**: 6种常见问题一键修复
- ✅ **工具箱**: 检查配置、清除缓存、DNS刷新等工具
- ✅ **系统信息收集**: 一键获取系统、浏览器、网络、DNS、hosts、ping等信息
- ✅ **Hosts管理**: 可视化查看和管理hosts文件配置
- ✅ **现代化UI**: 扁平化设计，美观易用

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
# 普通用户运行（部分功能需要权限）
python gui/main.py

# Mac/Linux需要管理员权限运行（修改hosts文件）
sudo python gui/main.py

# Windows需要以管理员身份运行
# 右键点击 -> 以管理员身份运行
```

## 使用说明

### 主界面

- **问题卡片**: 点击卡片或"一键修复"按钮开始修复
- **工具箱**: 提供各种实用工具
- **状态栏**: 显示系统信息、权限状态、hosts绑定数量

### 问题修复

1. 点击问题卡片
2. 查看问题描述和解决方案
3. 点击"立即修复"按钮
4. 等待修复完成（会自动获取IP、备份hosts、修改配置、清除DNS缓存）
5. 刷新浏览器使更改生效

### 系统信息收集

1. 点击"📊 一键获取系统信息"按钮
2. 等待信息收集完成（会自动收集系统、浏览器、网络、DNS、hosts、ping等信息）
3. 在标签页中查看各类信息
4. 可以导出为文本文件或复制到剪贴板

### Hosts配置管理

1. 点击"📋 检查Hosts配置"按钮
2. 查看当前所有千图相关域名的绑定状态
3. 可以单独解绑某个域名
4. 可以一键解绑所有域名

## 打包为可执行文件

### 使用PyInstaller

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包（Mac/Linux）
pyinstaller build.spec

# 打包（Windows）
pyinstaller build.spec

# 生成的可执行文件在 dist/ 目录
```

### 打包选项

- **Mac**: 生成 `.app` 应用包
- **Windows**: 生成 `.exe` 可执行文件
- **Linux**: 生成可执行文件

## 注意事项

1. ⚠️ 修改hosts文件需要管理员/root权限
2. ⚠️ 清除浏览器缓存前请先关闭浏览器
3. ⚠️ IP地址可能会变化，工具会自动获取最新IP
4. ⚠️ 修改hosts后需要刷新浏览器或清除DNS缓存才能生效

## 故障排除

### 权限问题

- **Mac/Linux**: 使用 `sudo` 运行
- **Windows**: 右键点击程序，选择"以管理员身份运行"

### 导入错误

确保所有依赖已安装：
```bash
pip install -r requirements.txt
```

### 界面显示异常

检查PyQt6是否正确安装：
```bash
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"
```

## 开发

### 项目结构

```
gui/
├── main.py              # 应用入口
├── main_window.py       # 主窗口
├── problem_dialog.py    # 问题修复对话框
├── info_dialog.py       # 信息收集对话框
├── hosts_viewer.py      # Hosts查看窗口
├── widgets/             # 自定义组件
└── resources/           # 资源文件
    └── styles.qss       # 样式表
```

### 修改样式

编辑 `gui/resources/styles.qss` 文件修改界面样式。

## 更新日志

### v1.0.0 (2026-01-22)
- 初始版本发布
- 支持6种问题快速修复
- 系统信息收集功能
- Hosts配置管理
- 工具箱功能集成
