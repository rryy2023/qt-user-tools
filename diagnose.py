#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主诊断工具
交互式问题选择菜单，根据用户选择的问题类型调用相应工具
"""

import os
import sys
import subprocess
from pathlib import Path

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入各个工具模块
from hosts.bind_hosts import bind_by_problem
from hosts.unbind_hosts import unbind_domain, unbind_all_qiantu
from hosts.check_hosts import print_hosts_status
from browser.clear_cache import clear_all_browsers
from browser.clear_dns import clear_dns
from browser.check_browser import print_browser_status
from download.check_download import diagnose_download_issue


# 问题菜单
PROBLEMS = {
    '1': {
        'title': '主站卡片预览图无法显示、加载慢',
        'type': 'preview',
        'description': '需要绑定 preview.qiantucdn.com',
    },
    '2': {
        'title': '下载页面样式乱了',
        'type': 'js',
        'description': '需要绑定 js.qiantucdn.com',
    },
    '3': {
        'title': '主站样式丢了',
        'type': 'icon',
        'description': '需要绑定 icon.qiantucdn.com',
    },
    '4': {
        'title': '下载页面显示无法访问网站',
        'type': 'download',
        'description': '需要绑定 dl.58pic.com',
    },
    '5': {
        'title': '云设计首页显示无法访问',
        'type': 'cloud',
        'description': '需要绑定 y.58pic.com',
    },
    '6': {
        'title': '千图首页面卡片无法加载但上面有标签文字',
        'type': 'unbind_preview',
        'description': '需要解绑 preview.qiantucdn.com',
    },
    '7': {
        'title': '下载失败-网络错误、下载中断',
        'type': 'download_fail',
        'description': '需要绑定 proxy-rar.58pic.com, proxy-vip.58pic.com, proxy-vd.58pic.com',
    },
    '8': {
        'title': '检查hosts文件配置',
        'type': 'check_hosts',
        'description': '查看当前hosts文件中的千图相关域名绑定',
    },
    '9': {
        'title': '清除浏览器缓存',
        'type': 'clear_cache',
        'description': '清除Chrome/Safari/Edge浏览器缓存和Cookie',
    },
    '10': {
        'title': '清除DNS缓存',
        'type': 'clear_dns',
        'description': '清除系统DNS缓存',
    },
    '11': {
        'title': '检查浏览器版本',
        'type': 'check_browser',
        'description': '检查浏览器版本和兼容性',
    },
    '12': {
        'title': '诊断下载问题',
        'type': 'check_download',
        'description': '检查下载工具和设置',
    },
    '0': {
        'title': '退出',
        'type': 'exit',
        'description': '退出程序',
    },
}


def print_menu():
    """打印主菜单"""
    print("\n" + "=" * 60)
    print("千图网客服问题解决工具")
    print("=" * 60)
    print("\n请选择您遇到的问题:")
    print()
    
    for key, problem in PROBLEMS.items():
        if key == '0':
            print(f"  {key}. {problem['title']}")
        else:
            print(f"  {key}. {problem['title']}")
            print(f"     {problem['description']}")
    
    print()


def get_user_choice() -> str:
    """获取用户选择"""
    while True:
        choice = input("请输入选项编号 (0-12): ").strip()
        if choice in PROBLEMS:
            return choice
        print("无效的选项，请重新输入")


def handle_problem(choice: str):
    """处理用户选择的问题"""
    problem = PROBLEMS[choice]
    problem_type = problem['type']
    
    print("\n" + "=" * 60)
    print(f"处理: {problem['title']}")
    print("=" * 60)
    print(f"描述: {problem['description']}\n")
    
    if problem_type == 'exit':
        print("感谢使用！")
        sys.exit(0)
    
    elif problem_type in ['preview', 'js', 'icon', 'download', 'cloud', 'download_fail']:
        # hosts绑定问题
        print("此问题需要修改hosts文件绑定域名。")
        print("工具将自动获取域名对应的IP地址并更新hosts文件。\n")
        
        auto_fix = input("是否自动修复? (y/N): ").strip().lower() == 'y'
        
        if auto_fix:
            print("\n⚠️  注意: 修改hosts文件需要管理员/root权限")
            print("如果权限不足，请以管理员身份运行此脚本\n")
        
        try:
            success = bind_by_problem(problem_type, auto_fix=auto_fix)
            if success and auto_fix:
                print("\n✓ 修复完成！")
                print("提示: 请刷新浏览器或重启浏览器以使更改生效")
                
                # 询问是否清除DNS缓存
                clear_dns_choice = input("\n是否清除DNS缓存? (y/N): ").strip().lower()
                if clear_dns_choice == 'y':
                    clear_dns()
        except Exception as e:
            print(f"\n✗ 修复失败: {e}")
    
    elif problem_type == 'unbind_preview':
        # 解绑preview域名
        print("此问题需要解绑 preview.qiantucdn.com。\n")
        
        auto_fix = input("是否自动修复? (y/N): ").strip().lower() == 'y'
        
        if auto_fix:
            print("\n⚠️  注意: 修改hosts文件需要管理员/root权限")
            print("如果权限不足，请以管理员身份运行此脚本\n")
        
        try:
            success = unbind_domain('preview.qiantucdn.com', auto_fix=auto_fix)
            if success and auto_fix:
                print("\n✓ 修复完成！")
                print("提示: 请刷新浏览器或重启浏览器以使更改生效")
        except Exception as e:
            print(f"\n✗ 修复失败: {e}")
    
    elif problem_type == 'check_hosts':
        # 检查hosts配置
        try:
            print_hosts_status()
        except Exception as e:
            print(f"\n✗ 检查失败: {e}")
    
    elif problem_type == 'clear_cache':
        # 清除浏览器缓存
        print("⚠️  警告: 清除缓存前请先关闭浏览器！\n")
        auto_fix = input("是否自动清除? (y/N): ").strip().lower() == 'y'
        
        if auto_fix:
            try:
                clear_all_browsers(auto_fix=True)
                print("\n✓ 清除完成！")
                print("提示: 请重新打开浏览器")
            except Exception as e:
                print(f"\n✗ 清除失败: {e}")
        else:
            print("已取消")
    
    elif problem_type == 'clear_dns':
        # 清除DNS缓存
        try:
            clear_dns()
        except Exception as e:
            print(f"\n✗ 清除失败: {e}")
    
    elif problem_type == 'check_browser':
        # 检查浏览器版本
        try:
            print_browser_status()
        except Exception as e:
            print(f"\n✗ 检查失败: {e}")
    
    elif problem_type == 'check_download':
        # 诊断下载问题
        url = input("请输入下载失败的URL（可选，直接回车跳过）: ").strip()
        url = url if url else None
        
        try:
            diagnose_download_issue(url=url)
        except Exception as e:
            print(f"\n✗ 诊断失败: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("欢迎使用千图网客服问题解决工具")
    print("=" * 60)
    print("\n本工具可以帮助您解决千图网使用过程中的常见问题")
    print("包括hosts绑定、浏览器缓存清理、下载问题诊断等\n")
    
    while True:
        try:
            print_menu()
            choice = get_user_choice()
            handle_problem(choice)
            
            if choice != '0':
                input("\n按回车键继续...")
        except KeyboardInterrupt:
            print("\n\n程序已中断")
            sys.exit(0)
        except Exception as e:
            print(f"\n发生错误: {e}")
            import traceback
            traceback.print_exc()
            input("\n按回车键继续...")


if __name__ == '__main__':
    main()
