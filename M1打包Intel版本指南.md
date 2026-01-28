# M1 Mac 打包 Intel 版本指南

## 问题说明

在 M1 Mac（Apple Silicon）上打包 Intel（x86_64）版本时，会遇到架构不兼容错误：

```
IncompatibleBinaryArchError: _cffi_backend.cpython-310-darwin.so is incompatible with target arch x86_64 (has arch: arm64)
```

**原因：** Python 依赖包（PyQt6、lxml、_cffi_backend 等）是 ARM64 架构的，无法用于 x86_64 打包。

## 解决方案

### 方法 1：使用 Rosetta 2 + x86_64 依赖（推荐）

#### 步骤 1：安装 Rosetta 2（如果未安装）

```bash
softwareupdate --install-rosetta --agree-to-license
```

#### 步骤 2：设置 x86_64 Python 环境

运行设置脚本：

```bash
./setup_x86_64_env.sh
```

这个脚本会：
- 检查 Rosetta 2 是否已安装
- 使用 `arch -x86_64` 在 x86_64 环境中安装依赖
- 验证依赖安装是否成功

#### 步骤 3：打包 Intel 版本

```bash
./build_all_platforms.sh --mac-intel
```

### 方法 2：手动安装 x86_64 依赖

如果自动脚本失败，可以手动安装：

```bash
# 1. 升级 pip
arch -x86_64 python3 -m pip install --upgrade pip

# 2. 安装依赖（强制重新安装，不使用二进制包）
arch -x86_64 python3 -m pip install -r requirements.txt --force-reinstall --no-binary :all:

# 3. 验证架构
arch -x86_64 python3 -c "import platform; print(platform.machine())"
# 应该输出: x86_64
```

### 方法 3：使用独立的 x86_64 Python 环境

#### 使用 Homebrew 安装 x86_64 Python

```bash
# 使用 Rosetta 2 安装 x86_64 版本的 Homebrew
arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 x86_64 Python
arch -x86_64 brew install python@3.10

# 使用该 Python 安装依赖
arch -x86_64 /usr/local/bin/python3 -m pip install -r requirements.txt
```

#### 使用 pyenv 安装 x86_64 Python

```bash
# 安装 pyenv（如果未安装）
brew install pyenv

# 安装 x86_64 Python
arch -x86_64 pyenv install 3.10.11

# 设置本地 Python 版本
pyenv local 3.10.11

# 安装依赖
python3 -m pip install -r requirements.txt
```

## 常见问题

### Q1: 依赖安装失败，提示架构不兼容

**A:** 确保使用 `--no-binary :all:` 参数强制从源码编译：

```bash
arch -x86_64 python3 -m pip install -r requirements.txt --force-reinstall --no-binary :all:
```

### Q2: PyQt6 安装失败

**A:** PyQt6 需要编译，可能需要较长时间。如果失败，可以尝试：

```bash
# 安装编译依赖
brew install cmake

# 单独安装 PyQt6
arch -x86_64 python3 -m pip install PyQt6 --no-binary PyQt6
```

### Q3: lxml 安装失败

**A:** lxml 需要 libxml2 和 libxslt：

```bash
# 安装系统依赖
brew install libxml2 libxslt

# 设置环境变量
export LDFLAGS="-L$(brew --prefix libxml2)/lib -L$(brew --prefix libxslt)/lib"
export CPPFLAGS="-I$(brew --prefix libxml2)/include -I$(brew --prefix libxslt)/include"

# 安装 lxml
arch -x86_64 python3 -m pip install lxml --no-binary lxml
```

### Q4: 打包时仍然报架构错误

**A:** 检查是否使用了正确的 Python：

```bash
# 验证 Python 架构
arch -x86_64 python3 -c "import platform; print(platform.machine())"
# 应该输出: x86_64

# 验证依赖架构
arch -x86_64 python3 -c "import _cffi_backend; import _cffi_backend; print(_cffi_backend.__file__)"
file $(arch -x86_64 python3 -c "import _cffi_backend; print(_cffi_backend.__file__)" 2>/dev/null)
# 应该显示: Mach-O 64-bit bundle x86_64
```

## 快速检查清单

- [ ] Rosetta 2 已安装
- [ ] `arch -x86_64 python3` 可以运行
- [ ] `arch -x86_64 python3 -c "import platform; print(platform.machine())"` 输出 `x86_64`
- [ ] x86_64 版本的依赖已安装
- [ ] 依赖包的架构是 x86_64（不是 arm64）

## 验证命令

```bash
# 检查 Python 架构
arch -x86_64 python3 -c "import platform; print('Architecture:', platform.machine())"

# 检查依赖架构
arch -x86_64 python3 -c "
import _cffi_backend
import os
file_path = _cffi_backend.__file__
print('File:', file_path)
os.system(f'file {file_path}')
"

# 检查 PyQt6 架构
arch -x86_64 python3 -c "
import PyQt6.QtCore
import os
import sys
qt_path = sys.modules['PyQt6.QtCore'].__file__
print('QtCore path:', qt_path)
os.system(f'file {qt_path}')
"
```

## 推荐工作流

1. **首次设置**（只需一次）：
   ```bash
   ./setup_x86_64_env.sh
   ```

2. **日常打包**：
   ```bash
   # 只打包 ARM64
   ./build_all_platforms.sh --mac-arm64
   
   # 只打包 Intel
   ./build_all_platforms.sh --mac-intel
   
   # 打包所有平台
   ./build_all_platforms.sh --all
   ```

## 注意事项

1. **编译时间**：在 x86_64 环境中从源码编译依赖可能需要较长时间（10-30分钟）
2. **磁盘空间**：x86_64 和 ARM64 依赖会占用双倍空间
3. **性能**：通过 Rosetta 2 运行 x86_64 Python 会稍慢
4. **兼容性**：某些依赖可能无法在 x86_64 环境中编译，需要特殊处理

## 替代方案

如果上述方法都失败，可以考虑：

1. **在 Intel Mac 上打包**（如果有）
2. **使用 CI/CD 服务**（如 GitHub Actions）在 Intel runner 上打包
3. **使用 Docker**（在 x86_64 容器中打包）
