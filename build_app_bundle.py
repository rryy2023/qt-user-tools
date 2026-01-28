#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建 macOS App Bundle 并打包为 DMG
"""

import sys
import os
import subprocess
import platform
import shutil
from pathlib import Path

# 检查架构
if platform.machine() != 'arm64':
    print(f"⚠️  警告: 当前Python架构为 {platform.machine()}，需要 arm64")
    print("请使用ARM64架构的Python环境进行打包")
    sys.exit(1)

print(f"✓ 使用 {platform.machine()} 架构的Python: {sys.executable}")

# 添加PyInstaller路径
import site
for path in site.getsitepackages():
    if path not in sys.path:
        sys.path.insert(0, path)

# 在导入PyInstaller之前patch签名函数
import PyInstaller.utils.osx as osx_utils

_original_sign_binary = osx_utils.sign_binary

def _ad_hoc_sign_binary(binary_path, codesign_identity, entitlements_file):
    """使用 ad-hoc 签名"""
    print(f"使用 ad-hoc 签名: {binary_path}")
    try:
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

osx_utils.sign_binary = _ad_hoc_sign_binary

# 现在导入并运行PyInstaller
from PyInstaller import __main__

if __name__ == '__main__':
    print("\n开始创建 App Bundle...")
    sys.argv = ['pyinstaller', 'build_app.spec', '--clean', '--noconfirm']
    __main__.run()
    
    # 打包完成后，对 .app 进行 ad-hoc 签名
    app_path = os.path.join('dist', '千图网问题解决工具.app')
    if os.path.exists(app_path):
        print(f"\n对 App Bundle 进行 ad-hoc 签名...")
        result = subprocess.run(
            ['codesign', '--force', '--deep', '--sign', '-', app_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ App Bundle 签名成功: {app_path}")
        else:
            print(f"✗ App Bundle 签名失败: {result.stderr}")
    else:
        print(f"✗ 未找到 App Bundle: {app_path}")
