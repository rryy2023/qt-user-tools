# Windows 打包快速指南

## 🚀 快速开始

### 方法 1：直接使用 Python 脚本（推荐）

```cmd
python build_windows.py
```

**优点**：
- 无编码问题
- 错误信息更清晰
- 跨平台兼容

### 方法 2：使用英文版批处理文件

```cmd
.\build_windows.bat
```

**说明**：已更新为英文版本，避免中文编码问题。

### 方法 3：使用 GBK 编码批处理文件

```cmd
.\build_windows_gbk.bat
```

**注意**：需要确保文件以 GBK/ANSI 编码保存。

## 📋 前置要求

1. **Python 3.7+**
   ```cmd
   python --version
   ```

2. **依赖包**
   ```cmd
   pip install -r requirements.txt
   ```

## 🔧 故障排除

### 问题 1：编码错误

**症状**：中文字符显示为乱码

**解决**：
- 使用 `python build_windows.py` 直接运行
- 或使用 `build_windows.bat`（英文版）

### 问题 2：Python 未找到

**症状**：`'python' 不是内部或外部命令`

**解决**：
1. 确认 Python 已安装
2. 将 Python 添加到 PATH 环境变量
3. 或使用完整路径：`C:\Python39\python.exe build_windows.py`

### 问题 3：PyInstaller 未安装

**症状**：`'pyinstaller' 不是内部或外部命令`

**解决**：
```cmd
pip install pyinstaller
```

### 问题 4：依赖安装失败

**解决**：
```cmd
pip install -r requirements.txt
```

如果网络问题，使用国内镜像：
```cmd
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 📦 输出文件

打包成功后，在 `dist/windows/` 目录：

- `QiantuTroubleshooter_v0.0.1_Windows-x64.exe` - 可执行文件
- `QiantuTroubleshooter_v0.0.1_Windows-x64.zip` - ZIP 压缩包

## ✅ 验证打包结果

```cmd
# 检查文件是否存在
dir dist\windows\*.exe
dir dist\windows\*.zip

# 查看文件大小
dir dist\windows\ /s
```

## 🎯 推荐工作流

```cmd
# 1. 进入项目目录
cd qt-user-tools

# 2. 检查环境
python --version
pip --version

# 3. 安装依赖（首次）
pip install -r requirements.txt

# 4. 打包
python build_windows.py

# 5. 检查输出
dir dist\windows\
```

## 📝 注意事项

1. **编码问题**：优先使用 Python 脚本而非批处理文件
2. **路径问题**：确保在项目根目录运行
3. **权限问题**：某些操作可能需要管理员权限
4. **杀毒软件**：打包的 EXE 可能被误报，需要添加白名单

## 🔗 相关文件

- `build_windows.py` - Python 打包脚本（推荐）
- `build_windows.bat` - 英文版批处理文件
- `build_windows_gbk.bat` - 中文版批处理文件（GBK 编码）
- `Windows打包说明.md` - 详细说明文档
