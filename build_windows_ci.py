#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows EXE 打包脚本（CI/CD 优化版）
适用于 GitHub Actions 等 CI 环境
"""

import os
import sys
import subprocess
import zipfile
from pathlib import Path

# 版本信息
VERSION = os.getenv("VERSION", "0.0.1")
APP_NAME = "千图网问题解决工具"
APP_NAME_EN = "QiantuTroubleshooter"

def get_output_name(platform, format_type):
    """生成平台特定的文件名"""
    if platform == "windows":
        if format_type == "exe":
            return f"{APP_NAME_EN}_v{VERSION}_Windows-x64.exe"
        elif format_type == "zip":
            return f"{APP_NAME_EN}_v{VERSION}_Windows-x64.zip"
    return None

def run_command(cmd, check=True):
    """运行命令并处理错误"""
    if isinstance(cmd, str):
        cmd = cmd.split()
    
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"命令未找到: {cmd[0] if isinstance(cmd, list) else cmd}")
        return False

def main():
    print("=" * 50)
    print("Windows EXE 打包脚本 (CI/CD)")
    print("=" * 50)
    print(f"版本: {VERSION}")
    print()
    
    # 检查 PyInstaller
    print("检查 PyInstaller...")
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("安装 PyInstaller...")
        if not run_command(["pip", "install", "pyinstaller"]):
            print("✗ PyInstaller 安装失败")
            sys.exit(1)
    
    # 检查依赖
    print("\n检查依赖...")
    missing_deps = []
    for dep in ["PyQt6", "bs4", "requests"]:
        try:
            __import__(dep if dep != "bs4" else "bs4")
        except ImportError:
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"⚠ 缺少依赖: {', '.join(missing_deps)}")
        print("安装依赖...")
        if not run_command(["pip", "install", "-r", "requirements.txt"]):
            print("✗ 依赖安装失败")
            sys.exit(1)
    
    print("✓ 依赖检查完成")
    
    # 创建 Windows spec 文件
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# Windows 打包配置

import os

block_cipher = None

a = Analysis(
    ['gui/main.py'],
    pathex=[os.path.dirname(os.path.abspath(SPEC))],
    binaries=[],
    datas=[
        ('gui/resources', 'gui/resources'),
        ('config', 'config'),
        ('resources/images', 'resources/images'),
    ],
    hiddenimports=[
        'hosts', 'hosts.bind_hosts', 'hosts.unbind_hosts', 'hosts.check_hosts', 'hosts.get_domain_ip',
        'browser', 'browser.clear_cache', 'browser.clear_dns', 'browser.check_browser',
        'download', 'download.check_download',
        'utils', 'utils.system_info', 'utils.elevate_permission',
        'gui.image_viewer',
        'bs4', 'bs4.builder', 'bs4.builder._htmlparser', 'bs4.builder._lxml', 'bs4.element', 'bs4.formatter',
        'beautifulsoup4', 'lxml', 'lxml.etree', 'lxml.html',
        'requests', 'netifaces',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    spec_file = "build_windows_temp.spec"
    try:
        with open(spec_file, "w", encoding="utf-8") as f:
            f.write(spec_content)
        print(f"\n✓ Spec 文件已创建: {spec_file}")
    except Exception as e:
        print(f"✗ 创建 Spec 文件失败: {e}")
        sys.exit(1)
    
    # 创建输出目录
    dist_dir = Path("dist/windows")
    build_dir = Path("build/windows")
    dist_dir.mkdir(parents=True, exist_ok=True)
    build_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n开始打包...")
    
    # 运行 PyInstaller
    cmd = [
        "pyinstaller",
        spec_file,
        "--workpath", str(build_dir),
        "--distpath", str(dist_dir),
        "--clean",
        "--noconfirm"
    ]
    
    if not run_command(cmd, check=False):
        print("\n✗ 打包失败")
        if os.path.exists(spec_file):
            os.remove(spec_file)
        sys.exit(1)
    
    # 清理临时文件
    if os.path.exists(spec_file):
        os.remove(spec_file)
    
    # 重命名文件
    old_exe = dist_dir / f"{APP_NAME}.exe"
    new_exe_name = get_output_name("windows", "exe")
    new_exe = dist_dir / new_exe_name
    
    if old_exe.exists():
        if new_exe.exists():
            new_exe.unlink()
        old_exe.rename(new_exe)
        print(f"\n✓ EXE 已重命名: {new_exe}")
        
        # 创建 ZIP 压缩包
        zip_name = get_output_name("windows", "zip")
        zip_path = dist_dir / zip_name
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(new_exe, new_exe.name)
            print(f"✓ ZIP 创建成功: {zip_path}")
        except Exception as e:
            print(f"⚠ ZIP 创建失败: {e}")
            zip_path = None
    else:
        print(f"\n⚠ 未找到生成的 EXE 文件: {old_exe}")
        sys.exit(1)
    
    # 输出总结
    print("\n" + "=" * 50)
    print("打包完成！")
    print("=" * 50)
    print(f"\n输出目录: {dist_dir}")
    
    if new_exe.exists():
        size = new_exe.stat().st_size / (1024 * 1024)
        print(f"EXE 文件: {new_exe_name} ({size:.1f} MB)")
    
    if zip_path and zip_path.exists():
        size = zip_path.stat().st_size / (1024 * 1024)
        print(f"ZIP 文件: {zip_name} ({size:.1f} MB)")
    
    print("\n✓ 所有文件已准备就绪")

if __name__ == "__main__":
    main()
