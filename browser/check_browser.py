#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查浏览器版本
判断是否需要升级
检测浏览器兼容性
"""

import os
import sys
import platform
import subprocess
import re
from pathlib import Path
from typing import Optional, Dict, Tuple


# 浏览器可执行文件路径
BROWSER_EXECUTABLES = {
    'Windows': {
        'Chrome': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        ],
        'Edge': [
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        ],
    },
    'Darwin': {  # macOS
        'Chrome': [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        ],
        'Safari': [
            '/Applications/Safari.app/Contents/MacOS/Safari',
        ],
        'Edge': [
            '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
        ],
    },
}

# 推荐的最低浏览器版本
MIN_VERSIONS = {
    'Chrome': 90,
    'Safari': 14,
    'Edge': 90,
    'Firefox': 88,
}


def get_chrome_version_windows() -> Optional[str]:
    """获取Windows系统Chrome版本"""
    try:
        # 尝试从注册表获取
        import winreg
        key_path = r'SOFTWARE\Google\Chrome\BLBeacon'
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
            version, _ = winreg.QueryValueEx(key, 'version')
            winreg.CloseKey(key)
            return version
        except:
            pass
    except ImportError:
        pass
    
    # 尝试从可执行文件获取
    for exe_path in BROWSER_EXECUTABLES['Windows']['Chrome']:
        if os.path.exists(exe_path):
            try:
                result = subprocess.run([exe_path, '--version'],
                                      capture_output=True,
                                      text=True,
                                      timeout=5)
                if result.returncode == 0:
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout)
                    if match:
                        return match.group(1)
            except:
                pass
    
    return None


def get_chrome_version_mac() -> Optional[str]:
    """获取Mac系统Chrome版本"""
    for exe_path in BROWSER_EXECUTABLES['Darwin']['Chrome']:
        if os.path.exists(exe_path):
            try:
                result = subprocess.run([exe_path, '--version'],
                                      capture_output=True,
                                      text=True,
                                      timeout=5)
                if result.returncode == 0:
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout)
                    if match:
                        return match.group(1)
            except:
                pass
    
    return None


def get_safari_version() -> Optional[str]:
    """获取Safari版本"""
    try:
        result = subprocess.run(['/usr/bin/defaults', 'read',
                               '/Applications/Safari.app/Contents/Info.plist',
                               'CFBundleShortVersionString'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None


def get_edge_version() -> Optional[str]:
    """获取Edge版本"""
    system = platform.system()
    exe_paths = BROWSER_EXECUTABLES.get(system, {}).get('Edge', [])
    
    for exe_path in exe_paths:
        if os.path.exists(exe_path):
            try:
                result = subprocess.run([exe_path, '--version'],
                                      capture_output=True,
                                      text=True,
                                      timeout=5)
                if result.returncode == 0:
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout)
                    if match:
                        return match.group(1)
            except:
                pass
    
    return None


def parse_version(version_str: str) -> Tuple[int, ...]:
    """解析版本号字符串为元组"""
    parts = version_str.split('.')
    try:
        return tuple(int(part) for part in parts[:4])
    except:
        return (0, 0, 0, 0)


def compare_versions(version1: str, version2: str) -> int:
    """
    比较两个版本号
    Returns: -1 if version1 < version2, 0 if equal, 1 if version1 > version2
    """
    v1 = parse_version(version1)
    v2 = parse_version(version2)
    
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0


def check_browser_version(browser: str) -> Dict[str, any]:
    """
    检查浏览器版本
    
    Returns:
        包含版本信息和兼容性状态的字典
    """
    system = platform.system()
    result = {
        'browser': browser,
        'installed': False,
        'version': None,
        'compatible': False,
        'needs_upgrade': False,
    }
    
    if system == 'Windows':
        if browser == 'Chrome':
            version = get_chrome_version_windows()
        elif browser == 'Edge':
            version = get_edge_version()
        else:
            return result
    elif system == 'Darwin':  # macOS
        if browser == 'Chrome':
            version = get_chrome_version_mac()
        elif browser == 'Safari':
            version = get_safari_version()
        elif browser == 'Edge':
            version = get_edge_version()
        else:
            return result
    else:
        return result
    
    if version:
        result['installed'] = True
        result['version'] = version
        
        # 检查是否满足最低版本要求
        min_version = MIN_VERSIONS.get(browser)
        if min_version:
            major_version = parse_version(version)[0]
            if major_version >= min_version:
                result['compatible'] = True
            else:
                result['needs_upgrade'] = True
        else:
            result['compatible'] = True  # 没有最低版本要求，认为兼容
    else:
        result['installed'] = False
    
    return result


def check_all_browsers() -> Dict[str, Dict]:
    """检查所有浏览器"""
    system = platform.system()
    browsers = list(BROWSER_EXECUTABLES.get(system, {}).keys())
    
    results = {}
    for browser in browsers:
        results[browser] = check_browser_version(browser)
    
    return results


def print_browser_status():
    """打印浏览器状态"""
    print("=" * 60)
    print("浏览器版本检查")
    print("=" * 60)
    print(f"操作系统: {platform.system()}\n")
    
    results = check_all_browsers()
    
    for browser, info in results.items():
        print(f"{browser}:")
        if info['installed']:
            print(f"  版本: {info['version']}")
            if info['compatible']:
                print(f"  状态: ✓ 兼容")
            elif info['needs_upgrade']:
                print(f"  状态: ⚠️  需要升级（推荐版本 >= {MIN_VERSIONS.get(browser, '?')}）")
            else:
                print(f"  状态: ? 未知")
        else:
            print(f"  状态: ✗ 未安装")
        print()
    
    # 总结
    compatible_browsers = [b for b, info in results.items() 
                          if info['installed'] and info['compatible']]
    
    if compatible_browsers:
        print(f"✓ 找到 {len(compatible_browsers)} 个兼容的浏览器: {', '.join(compatible_browsers)}")
    else:
        print("⚠️  未找到兼容的浏览器，建议升级浏览器版本")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='检查浏览器版本和兼容性')
    parser.add_argument('--browser', choices=['Chrome', 'Safari', 'Edge'],
                       help='要检查的浏览器（不指定则检查所有）')
    
    args = parser.parse_args()
    
    if args.browser:
        result = check_browser_version(args.browser)
        print(f"\n浏览器: {args.browser}")
        if result['installed']:
            print(f"版本: {result['version']}")
            if result['compatible']:
                print("状态: ✓ 兼容")
            elif result['needs_upgrade']:
                print(f"状态: ⚠️  需要升级")
            else:
                print("状态: ? 未知")
        else:
            print("状态: ✗ 未安装")
    else:
        print_browser_status()


if __name__ == '__main__':
    main()
