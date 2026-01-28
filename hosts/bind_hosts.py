#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hosts绑定工具
支持Windows和Mac系统，8种绑定场景
"""

import os
import sys
import platform
import shutil
from datetime import datetime
from typing import List, Optional, Dict

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hosts.check_hosts import get_hosts_path, read_hosts, parse_hosts_entry
from hosts.get_domain_ip import get_domain_ip
from utils.elevate_permission import check_permission, elevate_write_file, elevate_copy_file

# 问题类型到域名的映射
PROBLEM_DOMAINS = {
    'preview': ['preview.qiantucdn.com'],  # 主站卡片预览图无法显示
    'js': ['js.qiantucdn.com'],  # 下载页面样式乱了
    'icon': ['icon.qiantucdn.com'],  # 主站样式丢了
    'download': ['dl.58pic.com'],  # 下载页面显示无法访问网站
    'cloud': ['y.58pic.com'],  # 云设计首页显示无法访问
    'main_site': ['www.58pic.com', 'qiye.58pic.com'],  # 主站打不开
    'download_fail': ['proxy-rar.58pic.com', 'proxy-vip.58pic.com', 'proxy-vd.58pic.com'],  # 下载失败
}


def backup_hosts(hosts_path: str) -> str:
    """备份hosts文件（支持权限提升）"""
    backup_path = f"{hosts_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # 先尝试直接备份
    if check_permission():
        try:
            shutil.copy2(hosts_path, backup_path)
            print(f"✓ 已备份hosts文件到: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"✗ 备份hosts文件失败: {e}")
            # 如果失败，尝试权限提升
            print(f"需要管理员权限，正在请求权限...")
            success, error_msg = elevate_copy_file(hosts_path, backup_path)
            if success:
                print(f"✓ 已备份hosts文件到: {backup_path}（已获取管理员权限）")
                return backup_path
            else:
                print(f"✗ 备份失败: {error_msg}")
                raise Exception(f"备份失败: {error_msg}")
    else:
        # 没有权限，使用权限提升
        print(f"需要管理员权限来备份hosts文件，正在请求权限...")
        success, error_msg = elevate_copy_file(hosts_path, backup_path)
        if success:
            print(f"✓ 已备份hosts文件到: {backup_path}（已获取管理员权限）")
            return backup_path
        else:
            print(f"✗ 备份失败: {error_msg}")
            raise Exception(f"备份失败: {error_msg}")


def is_domain_bound(domain: str, lines: List[str]) -> bool:
    """检查域名是否已绑定"""
    for line in lines:
        ip, parsed_domain = parse_hosts_entry(line)
        if parsed_domain == domain:
            return True
    return False


def add_hosts_entry(domain: str, ip: str, lines: List[str]) -> List[str]:
    """
    添加hosts条目
    
    Args:
        domain: 域名
        ip: IP地址
        lines: 现有hosts文件行列表
        
    Returns:
        更新后的行列表
    """
    # 检查是否已存在
    if is_domain_bound(domain, lines):
        # 更新现有条目
        new_lines = []
        updated = False
        for line in lines:
            parsed_ip, parsed_domain = parse_hosts_entry(line)
            if parsed_domain == domain:
                if not updated:
                    # 替换为新的IP
                    new_lines.append(f"{ip}\t{domain}\n")
                    updated = True
                # 跳过旧的条目
                continue
            new_lines.append(line)
        
        if updated:
            print(f"✓ 已更新域名绑定: {domain} -> {ip}")
        return new_lines
    else:
        # 添加新条目
        entry = f"{ip}\t{domain}\n"
        lines.append(entry)
        print(f"✓ 已添加域名绑定: {domain} -> {ip}")
        return lines


def bind_domains(domains: List[str], auto_fix: bool = False, 
                 use_config: bool = True) -> bool:
    """
    绑定域名到hosts文件
    
    Args:
        domains: 域名列表
        auto_fix: 是否自动修改hosts文件
        use_config: 是否优先使用配置文件中的IP
        
    Returns:
        是否成功
    """
    hosts_path = get_hosts_path()
    lines = read_hosts()
    
    # 获取每个域名的IP
    domain_ips = {}
    for domain in domains:
        print(f"\n正在获取 {domain} 的IP地址...")
        ip = get_domain_ip(domain, use_config=use_config)
        if not ip:
            print(f"✗ 无法获取 {domain} 的IP地址，跳过")
            continue
        domain_ips[domain] = ip
    
    if not domain_ips:
        print("\n✗ 没有成功获取任何域名的IP地址")
        return False
    
    # 添加hosts条目
    new_lines = lines.copy()
    for domain, ip in domain_ips.items():
        new_lines = add_hosts_entry(domain, ip, new_lines)
    
    if auto_fix:
        # 备份原文件（会自动处理权限）
        try:
            backup_path = backup_hosts(hosts_path)
        except Exception as e:
            print(f"\n✗ 备份失败: {e}")
            return False
        
        # 准备文件内容
        file_content = ''.join(new_lines)
        
        # 尝试写入文件
        try:
            # 先尝试直接写入（如果有权限）
            if check_permission():
                with open(hosts_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                print(f"\n✓ 已成功更新hosts文件")
                print(f"✓ 共绑定 {len(domain_ips)} 个域名")
                return True
            else:
                # 没有权限，使用权限提升工具（类似SwitchHosts!）
                print(f"\n需要管理员权限来修改hosts文件，正在请求权限...")
                success, error_msg = elevate_write_file(hosts_path, file_content)
                if success:
                    print(f"\n✓ 已成功更新hosts文件（已获取管理员权限）")
                    print(f"✓ 共绑定 {len(domain_ips)} 个域名")
                    return True
                else:
                    print(f"\n✗ 错误: 无法获取管理员权限")
                    print(f"错误信息: {error_msg}")
                    # 尝试恢复备份
                    try:
                        if check_permission():
                            shutil.copy2(backup_path, hosts_path)
                        else:
                            elevate_copy_file(backup_path, hosts_path)
                        print(f"已恢复备份文件")
                    except:
                        pass
                    return False
        except PermissionError:
            # 如果直接写入失败，尝试权限提升
            print(f"\n需要管理员权限来修改hosts文件，正在请求权限...")
            success, error_msg = elevate_write_file(hosts_path, file_content)
            if success:
                print(f"\n✓ 已成功更新hosts文件（已获取管理员权限）")
                print(f"✓ 共绑定 {len(domain_ips)} 个域名")
                return True
            else:
                print(f"\n✗ 错误: 无法获取管理员权限")
                print(f"错误信息: {error_msg}")
                # 尝试恢复备份
                try:
                    if check_permission():
                        shutil.copy2(backup_path, hosts_path)
                    else:
                        elevate_copy_file(backup_path, hosts_path)
                    print(f"已恢复备份文件")
                except:
                    pass
                return False
        except Exception as e:
            print(f"\n✗ 修改hosts文件失败: {e}")
            # 尝试恢复备份
            try:
                if check_permission():
                    shutil.copy2(backup_path, hosts_path)
                else:
                    elevate_copy_file(backup_path, hosts_path)
                print(f"已恢复备份文件")
            except:
                pass
            return False
    else:
        # 只显示预览
        print("\n预览修改后的hosts文件内容（新增/更新的条目）:")
        print("-" * 60)
        for domain, ip in domain_ips.items():
            print(f"{ip}\t{domain}")
        print("-" * 60)
        print("\n提示: 使用 --auto-fix 参数自动应用修改")
        return True


def bind_by_problem(problem_type: str, auto_fix: bool = False, 
                   use_config: bool = True) -> bool:
    """
    根据问题类型绑定域名
    
    Args:
        problem_type: 问题类型（preview/js/icon/download/cloud/download_fail）
        auto_fix: 是否自动修改hosts文件
        use_config: 是否优先使用配置文件中的IP
        
    Returns:
        是否成功
    """
    if problem_type not in PROBLEM_DOMAINS:
        print(f"✗ 未知的问题类型: {problem_type}")
        print(f"支持的类型: {', '.join(PROBLEM_DOMAINS.keys())}")
        return False
    
    domains = PROBLEM_DOMAINS[problem_type]
    print(f"问题类型: {problem_type}")
    print(f"需要绑定的域名: {', '.join(domains)}")
    
    return bind_domains(domains, auto_fix=auto_fix, use_config=use_config)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='绑定域名到hosts文件')
    parser.add_argument('--problem', choices=list(PROBLEM_DOMAINS.keys()),
                       help='问题类型: preview/js/icon/download/cloud/download_fail')
    parser.add_argument('--domain', action='append', 
                       help='要绑定的域名（可多次使用）')
    parser.add_argument('--auto-fix', action='store_true',
                       help='自动修改hosts文件（需要管理员权限）')
    parser.add_argument('--no-config', action='store_true',
                       help='不使用配置文件中的IP')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Hosts域名绑定工具")
    print("=" * 60)
    
    if args.problem:
        success = bind_by_problem(args.problem, auto_fix=args.auto_fix, 
                                 use_config=not args.no_config)
    elif args.domain:
        success = bind_domains(args.domain, auto_fix=args.auto_fix,
                              use_config=not args.no_config)
    else:
        parser.print_help()
        print("\n请指定 --problem 或 --domain 参数")
        sys.exit(1)
    
    if success:
        print("\n✓ 操作完成")
        if args.auto_fix:
            print("\n提示: 请刷新浏览器或重启浏览器以使更改生效")
    else:
        print("\n✗ 操作失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
