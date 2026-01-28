# Windows 打包说明

## 问题

在 Windows 上运行 `build_windows.bat` 时出现编码错误，中文字符无法正确显示。

## 解决方案

### 方案 1：使用英文版批处理文件（推荐）

使用 `build_windows.bat`（已更新为英文版本，避免编码问题）：

```cmd
.\build_windows.bat
```

### 方案 2：使用 GBK 编码版本

如果希望使用中文提示，使用 `build_windows_gbk.bat`：

```cmd
.\build_windows_gbk.bat
```

**注意**：需要将文件保存为 GBK/ANSI 编码。如果仍有问题，请使用方案 1。

### 方案 3：直接使用 Python 脚本

跳过批处理文件，直接运行 Python 脚本：

```cmd
python build_windows.py
```

## 文件说明

- `build_windows.bat` - 英文版批处理文件（UTF-8，兼容性最好）
- `build_windows_gbk.bat` - 中文版批处理文件（GBK 编码）
- `build_windows.py` - Python 打包脚本（推荐直接使用）

## 打包步骤

1. **检查 Python**：
   ```cmd
   python --version
   ```

2. **安装依赖**（如果需要）：
   ```cmd
   pip install -r requirements.txt
   ```

3. **运行打包**：
   ```cmd
   python build_windows.py
   ```
   或
   ```cmd
   .\build_windows.bat
   ```

## 输出文件

打包成功后，会在 `dist/windows/` 目录生成：

- `QiantuTroubleshooter_v0.0.1_Windows-x64.exe` - 可执行文件
- `QiantuTroubleshooter_v0.0.1_Windows-x64.zip` - ZIP 压缩包

## 常见问题

### Q1: 编码错误

**A:** 使用英文版批处理文件 `build_windows.bat` 或直接运行 `python build_windows.py`

### Q2: Python 未找到

**A:** 确保 Python 已安装并添加到 PATH 环境变量

### Q3: PyInstaller 未安装

**A:** 脚本会自动安装，或手动运行：
```cmd
pip install pyinstaller
```

### Q4: 依赖安装失败

**A:** 手动安装依赖：
```cmd
pip install -r requirements.txt
```

## 推荐工作流

```cmd
# 1. 检查环境
python --version
pip --version

# 2. 安装依赖（首次）
pip install -r requirements.txt

# 3. 打包
python build_windows.py
```
