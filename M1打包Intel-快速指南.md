# M1 Mac 打包 Intel 版本 - 快速指南

## 问题

在 M1 Mac 上打包 Intel 版本时出现架构不匹配错误。

## ✅ 最简单解决方案

### 方法 1：使用 Universal Binary 依赖（推荐）

大多数现代 Python 包已经是 Universal Binary（同时支持 x86_64 和 arm64），直接打包即可：

```bash
./build_all_platforms.sh --mac-intel
```

如果失败，检查依赖是否为 Universal Binary：

```bash
# 检查 _cffi_backend 架构
arch -x86_64 python3 -c "
import _cffi_backend
import os
result = os.popen('file ' + _cffi_backend.__file__).read()
print(result)
"
```

如果显示 `universal binary` 或包含 `x86_64`，说明依赖支持 Intel 架构。

### 方法 2：重新安装 Universal Binary 依赖

如果依赖不是 Universal Binary，重新安装：

```bash
# 1. 升级 pip
arch -x86_64 python3 -m pip install --upgrade pip

# 2. 重新安装依赖（会自动下载 Universal Binary）
arch -x86_64 python3 -m pip install --force-reinstall \
    cffi cryptography lxml PyQt6 PyQt6-Qt6 beautifulsoup4 requests netifaces

# 3. 验证
arch -x86_64 python3 -c "
import _cffi_backend
import os
result = os.popen('file ' + _cffi_backend.__file__).read()
if 'universal' in result or 'x86_64' in result:
    print('✓ 依赖架构正确')
else:
    print('✗ 依赖架构不匹配')
"
```

### 方法 3：使用预编译的二进制包

如果从源码编译失败，使用预编译的二进制包：

```bash
arch -x86_64 python3 -m pip install --force-reinstall --only-binary :all: \
    PyQt6 PyQt6-Qt6 lxml cffi cryptography
```

## 当前状态检查

运行以下命令检查当前状态：

```bash
# 1. 检查 Rosetta 2
arch -x86_64 /usr/bin/true && echo "✓ Rosetta 2 可用" || echo "✗ Rosetta 2 不可用"

# 2. 检查 Python 架构
arch -x86_64 python3 -c "import platform; print('架构:', platform.machine())"
# 应该输出: x86_64

# 3. 检查依赖架构
arch -x86_64 python3 -c "
try:
    import _cffi_backend
    import os
    result = os.popen('file ' + _cffi_backend.__file__).read()
    print('_cffi_backend:', result)
except Exception as e:
    print('错误:', e)
"
```

## 如果仍然失败

### 选项 1：跳过 Intel 版本

如果只需要 ARM64 版本：

```bash
./build_all_platforms.sh --mac-arm64
```

### 选项 2：使用 CI/CD

在 GitHub Actions 等 CI 服务上使用 Intel runner 自动打包。

### 选项 3：在 Intel Mac 上打包

如果有 Intel Mac，直接在那台机器上运行：

```bash
./build_all_platforms.sh --mac-intel
```

## 常见错误

### 错误：架构不匹配

**解决：** 重新安装依赖为 Universal Binary（见方法 2）

### 错误：网络连接失败

**解决：** 检查网络连接，或使用国内镜像：

```bash
arch -x86_64 python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 错误：编译失败

**解决：** 使用预编译的二进制包（见方法 3）

## 推荐工作流

1. **首次设置**（如果依赖不是 Universal Binary）：
   ```bash
   arch -x86_64 python3 -m pip install --force-reinstall \
       cffi cryptography lxml PyQt6 PyQt6-Qt6
   ```

2. **日常打包**：
   ```bash
   ./build_all_platforms.sh --mac-intel
   ```

## 验证打包结果

```bash
# 检查生成的 app 架构
file dist/mac_intel/千图网问题解决工具.app/Contents/MacOS/千图网问题解决工具

# 应该显示: Mach-O 64-bit executable x86_64
```
