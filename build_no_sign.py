#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义打包脚本 - 使用 ad-hoc 签名
注意：必须使用ARM64架构的Python进行打包（Apple Silicon）
"""

import sys
import os
import subprocess
import platform

# 检查架构
if platform.machine() != 'arm64':
    print(f"⚠️  警告: 当前Python架构为 {platform.machine()}，需要 arm64")
    print("请使用ARM64架构的Python环境进行打包")
    sys.exit(1)

print(f"✓ 使用 {platform.machine()} 架构的Python: {sys.executable}")

# 添加PyInstaller路径
# 确保使用当前Python环境的site-packages
import site
for path in site.getsitepackages():
    if path not in sys.path:
        sys.path.insert(0, path)

# 在导入PyInstaller之前patch签名函数
import PyInstaller.utils.osx as osx_utils

# 保存原始函数
_original_sign_binary = osx_utils.sign_binary

def _ad_hoc_sign_binary(binary_path, codesign_identity, entitlements_file):
    """使用 ad-hoc 签名"""
    print(f"使用 ad-hoc 签名: {binary_path}")
    try:
        # 使用 ad-hoc 签名（- 表示使用临时签名）
        result = subprocess.run(
            ['codesign', '--force', '--deep', '--sign', '-', binary_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  ✓ 签名成功: {binary_path}")
            return True
        else:
            print(f"  ✗ 签名失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ 签名异常: {e}")
        return False

# 替换签名函数
osx_utils.sign_binary = _ad_hoc_sign_binary

# 现在导入并运行PyInstaller
from PyInstaller import __main__

if __name__ == '__main__':
    sys.argv = ['pyinstaller', 'build.spec', '--clean', '--noconfirm']
    __main__.run()
    
    # 打包完成后，对最终的可执行文件进行 ad-hoc 签名
    exe_path = os.path.join('dist', '千图网问题解决工具')
    if os.path.exists(exe_path):
        print(f"\n对最终可执行文件进行 ad-hoc 签名...")
        result = subprocess.run(
            ['codesign', '--force', '--deep', '--sign', '-', exe_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ 最终文件签名成功: {exe_path}")
        else:
            print(f"✗ 最终文件签名失败: {result.stderr}")
