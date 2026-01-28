#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查hosts文件配置
显示已绑定的千图相关域名
"""

import os
import sys
import platform
import re
from typing import List, Dict, Tuple, Optional

# 千图相关域名列表
QIANTU_DOMAINS = [
    'preview.qiantucdn.com',
    'js.qiantucdn.com',
    'icon.qiantucdn.com',
    'dl.58pic.com',
    'y.58pic.com',
    'proxy-rar.58pic.com',
    'proxy-vip.58pic.com',
    'proxy-vd.58pic.com',
    '58pic.com',
    'qiantucdn.com'
]


def get_hosts_path() -> str:
    """获取hosts文件路径"""
    system = platform.system()
    if system == 'Windows':
        return r'C:\Windows\System32\drivers\etc\hosts'
    elif system == 'Darwin':  # macOS
        return '/etc/hosts'
    elif system == 'Linux':
        return '/etc/hosts'
    else:
        raise OSError(f"不支持的操作系统: {system}")


def read_hosts(max_lines: int = None) -> List[str]:
    """
    读取hosts文件内容（优化版本，不阻塞启动）
    
    Args:
        max_lines: 最大读取行数，None表示读取全部（用于大文件优化）
    """
    hosts_path = get_hosts_path()
    try:
        # 使用更快的读取方式，添加错误处理
        with open(hosts_path, 'r', encoding='utf-8', errors='ignore') as f:
            if max_lines:
                # 只读取前N行（对于大文件优化）
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break
                    lines.append(line)
                return lines
            else:
                return f.readlines()
    except PermissionError:
        # 不退出程序，返回空列表（GUI模式下不应该退出）
        print(f"警告: 没有权限读取hosts文件: {hosts_path}")
        return []
    except FileNotFoundError:
        # 不退出程序，返回空列表
        print(f"警告: hosts文件不存在: {hosts_path}")
        return []
    except Exception as e:
        # 不退出程序，返回空列表
        print(f"读取hosts文件失败: {e}")
        return []


def parse_hosts_entry(line: str) -> Tuple[Optional[str], Optional[str]]:
    """
    解析hosts文件中的一行
    
    Returns:
        (ip, domain) 元组，如果是注释或空行返回 (None, None)
    """
    line = line.strip()
    
    # 跳过空行和注释
    if not line or line.startswith('#'):
        return None, None
    
    # 移除行尾注释
    if '#' in line:
        line = line[:line.index('#')].strip()
    
    # 分割IP和域名
    parts = line.split()
    if len(parts) >= 2:
        ip = parts[0]
        domain = parts[1]
        # 验证IP格式
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            return ip, domain
    
    return None, None


def check_hosts(max_lines: int = 1000) -> Dict[str, Dict[str, str]]:
    """
    检查hosts文件中的千图相关域名配置（优化版本）
    
    Args:
        max_lines: 最大读取行数，默认1000行（对于大文件优化）
    
    Returns:
        字典，键为域名，值为包含ip和line_num的字典
    """
    # 对于大文件，只读取前N行（通常hosts绑定在前几行）
    lines = read_hosts(max_lines=max_lines)
    results = {}
    
    for line_num, line in enumerate(lines, 1):
        ip, domain = parse_hosts_entry(line)
        
        if domain:
            # 检查是否是千图相关域名
            for qiantu_domain in QIANTU_DOMAINS:
                if domain == qiantu_domain or domain.endswith('.' + qiantu_domain):
                    if domain not in results:
                        results[domain] = {
                            'ip': ip,
                            'line': line_num,
                            'raw_line': line.strip()
                        }
                    break
    
    return results


def print_hosts_status():
    """打印hosts文件状态"""
    print("=" * 60)
    print("Hosts文件配置检查")
    print("=" * 60)
    
    hosts_path = get_hosts_path()
    print(f"\nHosts文件路径: {hosts_path}")
    
    try:
        results = check_hosts()
        
        if not results:
            print("\n未发现千图相关域名的hosts绑定")
            return
        
        print(f"\n发现 {len(results)} 个千图相关域名的绑定:")
        print("-" * 60)
        print(f"{'域名':<30} {'IP地址':<20} {'行号':<10}")
        print("-" * 60)
        
        for domain, info in sorted(results.items()):
            print(f"{domain:<30} {info['ip']:<20} {info['line']:<10}")
        
        print("-" * 60)
        
        # 检查是否有问题配置
        issues = []
        for domain, info in results.items():
            if not info['ip'] or info['ip'] == '0.0.0.0':
                issues.append(f"{domain} 的IP配置可能有问题: {info['ip']}")
        
        if issues:
            print("\n⚠️  发现潜在问题:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("\n✓ 所有配置看起来正常")
            
    except Exception as e:
        print(f"\n检查失败: {e}")
        sys.exit(1)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='检查hosts文件中的千图相关域名配置')
    parser.add_argument('--domain', help='只检查指定域名')
    
    args = parser.parse_args()
    
    if args.domain:
        # 只检查指定域名
        results = check_hosts()
        if args.domain in results:
            info = results[args.domain]
            print(f"域名: {args.domain}")
            print(f"IP地址: {info['ip']}")
            print(f"行号: {info['line']}")
            print(f"原始行: {info['raw_line']}")
        else:
            print(f"未找到域名 {args.domain} 的配置")
            sys.exit(1)
    else:
        print_hosts_status()


if __name__ == '__main__':
    main()
