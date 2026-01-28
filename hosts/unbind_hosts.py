#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解绑hosts文件中的域名
支持解绑指定域名或所有千图相关域名
"""

import os
import sys
import platform
import shutil
from datetime import datetime
from typing import List, Optional

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hosts.check_hosts import get_hosts_path, read_hosts, parse_hosts_entry, QIANTU_DOMAINS
from utils.elevate_permission import check_permission, elevate_write_file, elevate_copy_file
from utils.elevate_permission import check_permission, elevate_write_file


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


def unbind_domain(domain: str, auto_fix: bool = False) -> bool:
    """
    解绑指定域名
    
    Args:
        domain: 要解绑的域名
        auto_fix: 是否自动修改hosts文件
        
    Returns:
        是否成功
    """
    hosts_path = get_hosts_path()
    lines = read_hosts()
    new_lines = []
    removed = False
    
    for line in lines:
        ip, parsed_domain = parse_hosts_entry(line)
        
        if parsed_domain and (parsed_domain == domain or 
                             parsed_domain.endswith('.' + domain) or
                             domain.endswith('.' + parsed_domain)):
            print(f"发现绑定: {ip} {parsed_domain} (将被移除)")
            removed = True
            # 跳过这一行，不添加到新内容中
            continue
        
        new_lines.append(line)
    
    if not removed:
        print(f"未找到域名 {domain} 的绑定")
        return False
    
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
                print(f"✓ 已成功解绑域名: {domain}")
                print(f"✓ hosts文件已更新")
                return True
            else:
                # 没有权限，使用权限提升工具
                print(f"\n需要管理员权限来修改hosts文件，正在请求权限...")
                success, error_msg = elevate_write_file(hosts_path, file_content)
                if success:
                    print(f"✓ 已成功解绑域名: {domain}（已获取管理员权限）")
                    print(f"✓ hosts文件已更新")
                    return True
                else:
                    print(f"✗ 错误: 无法获取管理员权限")
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
                print(f"✓ 已成功解绑域名: {domain}（已获取管理员权限）")
                print(f"✓ hosts文件已更新")
                return True
            else:
                print(f"✗ 错误: 无法获取管理员权限")
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
            print(f"✗ 修改hosts文件失败: {e}")
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
        print("\n预览修改后的hosts文件内容（前10行）:")
        print("-" * 60)
        for i, line in enumerate(new_lines[:10], 1):
            print(f"{i:3d}: {line.rstrip()}")
        if len(new_lines) > 10:
            print(f"... (还有 {len(new_lines) - 10} 行)")
        print("-" * 60)
        print("\n提示: 使用 --auto-fix 参数自动应用修改")
        return True


def unbind_all_qiantu(auto_fix: bool = False) -> bool:
    """
    解绑所有千图相关域名
    
    Args:
        auto_fix: 是否自动修改hosts文件
        
    Returns:
        是否成功
    """
    hosts_path = get_hosts_path()
    lines = read_hosts()
    new_lines = []
    removed_count = 0
    removed_domains = []
    
    for line in lines:
        ip, domain = parse_hosts_entry(line)
        
        if domain:
            # 检查是否是千图相关域名
            is_qiantu = False
            for qiantu_domain in QIANTU_DOMAINS:
                if domain == qiantu_domain or domain.endswith('.' + qiantu_domain):
                    is_qiantu = True
                    break
            
            if is_qiantu:
                print(f"发现绑定: {ip} {domain} (将被移除)")
                removed_count += 1
                if domain not in removed_domains:
                    removed_domains.append(domain)
                continue
        
        new_lines.append(line)
    
    if removed_count == 0:
        print("未找到任何千图相关域名的绑定")
        return False
    
    print(f"\n共发现 {removed_count} 个绑定，涉及 {len(removed_domains)} 个域名")
    
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
                print(f"✓ 已成功解绑所有千图相关域名")
                print(f"✓ hosts文件已更新")
                return True
            else:
                # 没有权限，使用权限提升工具
                print(f"\n需要管理员权限来修改hosts文件，正在请求权限...")
                success, error_msg = elevate_write_file(hosts_path, file_content)
                if success:
                    print(f"✓ 已成功解绑所有千图相关域名（已获取管理员权限）")
                    print(f"✓ hosts文件已更新")
                    return True
                else:
                    print(f"✗ 错误: 无法获取管理员权限")
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
                print(f"✓ 已成功解绑所有千图相关域名（已获取管理员权限）")
                print(f"✓ hosts文件已更新")
                return True
            else:
                print(f"✗ 错误: 无法获取管理员权限")
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
            print(f"✗ 修改hosts文件失败: {e}")
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
        print("\n预览修改后的hosts文件内容（前10行）:")
        print("-" * 60)
        for i, line in enumerate(new_lines[:10], 1):
            print(f"{i:3d}: {line.rstrip()}")
        if len(new_lines) > 10:
            print(f"... (还有 {len(new_lines) - 10} 行)")
        print("-" * 60)
        print("\n提示: 使用 --auto-fix 参数自动应用修改")
        return True


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='解绑hosts文件中的域名')
    parser.add_argument('--domain', help='要解绑的域名（不指定则解绑所有千图相关域名）')
    parser.add_argument('--auto-fix', action='store_true', 
                       help='自动修改hosts文件（需要管理员权限）')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Hosts域名解绑工具")
    print("=" * 60)
    
    if args.domain:
        success = unbind_domain(args.domain, args.auto_fix)
    else:
        print("将解绑所有千图相关域名")
        confirm = input("确认继续? (y/N): ")
        if confirm.lower() != 'y':
            print("已取消")
            sys.exit(0)
        success = unbind_all_qiantu(args.auto_fix)
    
    if success:
        print("\n✓ 操作完成")
    else:
        print("\n✗ 操作失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
