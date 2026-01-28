#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清除DNS缓存
支持Windows和Mac系统
"""

import os
import sys
import platform
import subprocess


def clear_dns_windows() -> bool:
    """清除Windows系统的DNS缓存"""
    try:
        print("正在清除Windows DNS缓存...")
        result = subprocess.run(['ipconfig', '/flushdns'], 
                              capture_output=True, 
                              text=True,
                              check=True)
        print("✓ DNS缓存已清除")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 清除DNS缓存失败: {e}")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("✗ 未找到 ipconfig 命令")
        return False
    except Exception as e:
        print(f"✗ 执行失败: {e}")
        return False


def clear_dns_mac() -> bool:
    """清除Mac系统的DNS缓存"""
    try:
        print("正在清除Mac DNS缓存...")
        
        # 执行清除DNS缓存的命令
        commands = [
            ['sudo', 'dscacheutil', '-flushcache'],
            ['sudo', 'killall', '-HUP', 'mDNSResponder']
        ]
        
        for cmd in commands:
            print(f"执行: {' '.join(cmd)}")
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode != 0:
                if 'sudo' in cmd:
                    print(f"⚠️  需要管理员权限，请手动执行: {' '.join(cmd)}")
                else:
                    print(f"✗ 命令执行失败: {result.stderr}")
                    return False
        
        print("✓ DNS缓存已清除")
        return True
    except Exception as e:
        print(f"✗ 执行失败: {e}")
        return False


def clear_dns_linux() -> bool:
    """清除Linux系统的DNS缓存"""
    try:
        print("正在清除Linux DNS缓存...")
        
        # 不同的Linux发行版使用不同的命令
        commands_to_try = [
            ['sudo', 'systemd-resolve', '--flush-caches'],  # systemd
            ['sudo', 'service', 'nscd', 'restart'],  # nscd
            ['sudo', 'service', 'dnsmasq', 'restart'],  # dnsmasq
        ]
        
        for cmd in commands_to_try:
            try:
                result = subprocess.run(cmd, 
                                     capture_output=True, 
                                     text=True,
                                     timeout=5)
                if result.returncode == 0:
                    print(f"✓ DNS缓存已清除 (使用: {' '.join(cmd)})")
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        print("⚠️  无法自动清除DNS缓存")
        print("请手动执行以下命令之一:")
        for cmd in commands_to_try:
            print(f"  {' '.join(cmd)}")
        return False
    except Exception as e:
        print(f"✗ 执行失败: {e}")
        return False


def clear_dns() -> bool:
    """根据操作系统清除DNS缓存"""
    system = platform.system()
    
    print("=" * 60)
    print("DNS缓存清理工具")
    print("=" * 60)
    print(f"操作系统: {system}\n")
    
    if system == 'Windows':
        return clear_dns_windows()
    elif system == 'Darwin':  # macOS
        return clear_dns_mac()
    elif system == 'Linux':
        return clear_dns_linux()
    else:
        print(f"✗ 不支持的操作系统: {system}")
        return False


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='清除系统DNS缓存')
    
    args = parser.parse_args()
    
    success = clear_dns()
    
    if success:
        print("\n✓ 操作完成")
        print("提示: 如果问题仍然存在，请尝试重启浏览器")
    else:
        print("\n✗ 操作失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
