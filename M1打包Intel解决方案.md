# M1 Mac 打包 Intel 版本 - 完整解决方案

## 问题根源

在 M1 Mac 上打包 Intel 版本时，错误信息：
```
IncompatibleBinaryArchError: _cffi_backend.cpython-310-darwin.so is incompatible with target arch x86_64 (has arch: arm64)
```

**原因：** Python 依赖包是 ARM64 架构，无法用于 x86_64 打包。

## ✅ 已验证的解决方案

### 当前状态

检查显示 `_cffi_backend` 已经是 **Universal Binary**（包含 x86_64 和 arm64）：
```
Mach-O universal binary with 2 architectures: [x86_64] [arm64]
```

这意味着依赖包已经支持两种架构。

### 解决方案 1：使用 Universal Binary 依赖（最简单）

如果依赖已经是 Universal Binary，直接打包即可：

```bash
./build_all_platforms.sh --mac-intel
```

### 解决方案 2：重新安装 Universal Binary 依赖

如果仍有问题，重新安装支持多架构的依赖：

```bash
# 1. 卸载现有依赖
arch -x86_64 python3 -m pip uninstall -y cffi cryptography lxml PyQt6

# 2. 重新安装（会自动下载 Universal Binary）
arch -x86_64 python3 -m pip install cffi cryptography lxml PyQt6 PyQt6-Qt6

# 3. 验证架构
arch -x86_64 python3 -c "
import _cffi_backend
import os
result = os.popen('file ' + _cffi_backend.__file__).read()
print(result)
"
# 应该显示: Mach-O universal binary with 2 architectures
```

### 解决方案 3：使用隔离环境（推荐，避免冲突）

创建独立的 x86_64 Python 环境：

```bash
# 1. 创建虚拟环境（x86_64）
arch -x86_64 python3 -m venv venv_x86_64

# 2. 激活环境
source venv_x86_64/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 修改 build_all_platforms.sh，使用虚拟环境
# 将 PYTHON_BIN 改为: venv_x86_64/bin/python3
```

## 修改构建脚本以使用虚拟环境

编辑 `build_all_platforms.sh`，在 `build_mac_intel()` 函数中添加：

```bash
# 检查虚拟环境
if [ -d "venv_x86_64" ]; then
    PYTHON_BIN="venv_x86_64/bin/python3"
    echo -e "${GREEN}使用虚拟环境: $PYTHON_BIN${NC}"
elif [ "$ARCH_TEST" = "x86_64" ]; then
    PYTHON_BIN="arch -x86_64 python3"
    echo -e "${GREEN}使用 Rosetta 2 运行 x86_64 Python${NC}"
fi
```

## 快速修复脚本

已创建 `快速修复Intel打包.sh`，运行：

```bash
./快速修复Intel打包.sh
```

## 验证步骤

### 1. 检查 Python 架构

```bash
arch -x86_64 python3 -c "import platform; print(platform.machine())"
# 应该输出: x86_64
```

### 2. 检查依赖架构

```bash
arch -x86_64 python3 -c "
import _cffi_backend
import os
result = os.popen('file ' + _cffi_backend.__file__).read()
if 'universal' in result or 'x86_64' in result:
    print('✓ 依赖架构正确')
    print(result)
else:
    print('✗ 依赖架构不匹配')
"
```

### 3. 测试打包

```bash
./build_all_platforms.sh --mac-intel
```

## 常见错误及解决

### 错误 1: 架构不匹配

**错误信息：**
```
IncompatibleBinaryArchError: ... is incompatible with target arch x86_64 (has arch: arm64)
```

**解决：**
```bash
# 重新安装依赖为 Universal Binary
arch -x86_64 python3 -m pip install --force-reinstall --upgrade cffi cryptography lxml PyQt6
```

### 错误 2: PyQt6 安装失败

**解决：**
```bash
# 使用二进制包（更快）
arch -x86_64 python3 -m pip install --only-binary PyQt6 PyQt6 PyQt6-Qt6
```

### 错误 3: lxml 编译失败

**解决：**
```bash
# 安装系统依赖
brew install libxml2 libxslt

# 设置环境变量
export LDFLAGS="-L$(brew --prefix libxml2)/lib"
export CPPFLAGS="-I$(brew --prefix libxml2)/include"

# 安装 lxml
arch -x86_64 python3 -m pip install lxml --no-binary lxml
```

## 推荐工作流

### 首次设置（一次性）

```bash
# 1. 创建 x86_64 虚拟环境
arch -x86_64 python3 -m venv venv_x86_64

# 2. 激活环境
source venv_x86_64/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 验证
python -c "import platform; print(platform.machine())"
# 应该输出: x86_64
```

### 日常打包

```bash
# 激活虚拟环境
source venv_x86_64/bin/activate

# 打包 Intel 版本
./build_all_platforms.sh --mac-intel
```

## 性能提示

1. **首次编译**：从源码编译依赖可能需要 10-30 分钟
2. **后续打包**：使用已编译的依赖，打包时间约 2-5 分钟
3. **使用二进制包**：如果网络允许，使用预编译的二进制包会更快

## 替代方案

如果上述方法都失败，考虑：

1. **在 Intel Mac 上打包**（如果有）
2. **使用 GitHub Actions**：在 Intel runner 上自动打包
3. **使用 Docker**：在 x86_64 容器中打包
