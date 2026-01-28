#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清除浏览器缓存和Cookie
支持Chrome、Safari、Edge浏览器
支持Windows和Mac系统
"""

import os
import sys
import platform
import shutil
from pathlib import Path
from typing import List, Dict


# 浏览器缓存路径配置
BROWSER_PATHS = {
    'Windows': {
        'Chrome': [
            os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data\Default\Cache'),
            os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data\Default\Cookies'),
        ],
        'Edge': [
            os.path.expanduser(r'~\AppData\Local\Microsoft\Edge\User Data\Default\Cache'),
            os.path.expanduser(r'~\AppData\Local\Microsoft\Edge\User Data\Default\Cookies'),
        ],
    },
    'Darwin': {  # macOS
        'Chrome': [
            os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Cache'),
            os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Cookies'),
        ],
        'Safari': [
            os.path.expanduser('~/Library/Caches/com.apple.Safari'),
            os.path.expanduser('~/Library/Cookies'),
        ],
        'Edge': [
            os.path.expanduser('~/Library/Application Support/Microsoft Edge/Default/Cache'),
            os.path.expanduser('~/Library/Application Support/Microsoft Edge/Default/Cookies'),
        ],
    },
}


def clear_browser_cache(browser: str, auto_fix: bool = False) -> bool:
    """
    清除指定浏览器的缓存
    
    Args:
        browser: 浏览器名称 (Chrome/Safari/Edge)
        auto_fix: 是否自动清除
        
    Returns:
        是否成功
    """
    system = platform.system()
    
    if system not in BROWSER_PATHS:
        print(f"✗ 不支持的操作系统: {system}")
        return False
    
    if browser not in BROWSER_PATHS[system]:
        print(f"✗ 在 {system} 系统上不支持浏览器: {browser}")
        return False
    
    paths = BROWSER_PATHS[system][browser]
    cleared = []
    failed = []
    
    print(f"\n正在检查 {browser} 浏览器的缓存路径...")
    
    for path in paths:
        full_path = Path(path)
        if full_path.exists():
            print(f"  发现: {full_path}")
            if auto_fix:
                try:
                    if full_path.is_file():
                        # 删除文件
                        full_path.unlink()
                        print(f"  ✓ 已删除: {full_path.name}")
                    elif full_path.is_dir():
                        # 删除目录内容
                        shutil.rmtree(full_path)
                        print(f"  ✓ 已清除目录: {full_path.name}")
                    cleared.append(str(full_path))
                except PermissionError:
                    print(f"  ✗ 权限不足，无法删除: {full_path}")
                    print(f"    提示: 请先关闭 {browser} 浏览器")
                    failed.append(str(full_path))
                except Exception as e:
                    print(f"  ✗ 删除失败: {e}")
                    failed.append(str(full_path))
            else:
                print(f"  [预览] 将删除: {full_path}")
                cleared.append(str(full_path))
        else:
            print(f"  [未找到] {full_path}")
    
    if not cleared and not failed:
        print(f"  ⚠️  未找到 {browser} 浏览器的缓存文件")
        return False
    
    if auto_fix:
        if cleared:
            print(f"\n✓ 成功清除 {len(cleared)} 个缓存项")
        if failed:
            print(f"✗ 失败 {len(failed)} 个缓存项")
            return False
        return True
    else:
        print(f"\n[预览模式] 将清除 {len(cleared)} 个缓存项")
        print("提示: 使用 --auto-fix 参数自动清除")
        return True


def clear_all_browsers(auto_fix: bool = False) -> bool:
    """清除所有浏览器的缓存"""
    system = platform.system()
    
    if system not in BROWSER_PATHS:
        print(f"✗ 不支持的操作系统: {system}")
        return False
    
    browsers = list(BROWSER_PATHS[system].keys())
    print(f"将清除以下浏览器的缓存: {', '.join(browsers)}")
    
    if not auto_fix:
        confirm = input("确认继续? (y/N): ")
        if confirm.lower() != 'y':
            print("已取消")
            return False
    
    success_count = 0
    for browser in browsers:
        print(f"\n{'=' * 60}")
        print(f"处理 {browser} 浏览器")
        print('=' * 60)
        if clear_browser_cache(browser, auto_fix=auto_fix):
            success_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"完成: 成功清除 {success_count}/{len(browsers)} 个浏览器的缓存")
    print('=' * 60)
    
    return success_count > 0


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='清除浏览器缓存和Cookie')
    parser.add_argument('--browser', choices=['Chrome', 'Safari', 'Edge'],
                       help='要清除缓存的浏览器（不指定则清除所有）')
    parser.add_argument('--auto-fix', action='store_true',
                       help='自动清除缓存（需要先关闭浏览器）')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("浏览器缓存清理工具")
    print("=" * 60)
    print(f"操作系统: {platform.system()}\n")
    
    if args.auto_fix:
        print("⚠️  警告: 清除缓存前请先关闭相应的浏览器！\n")
    
    if args.browser:
        success = clear_browser_cache(args.browser, auto_fix=args.auto_fix)
    else:
        success = clear_all_browsers(auto_fix=args.auto_fix)
    
    if success:
        print("\n✓ 操作完成")
        print("提示: 请重新打开浏览器以使更改生效")
    else:
        print("\n✗ 操作失败或未找到缓存")
        if not args.auto_fix:
            print("提示: 使用 --auto-fix 参数自动清除")
        sys.exit(1)


if __name__ == '__main__':
    main()
