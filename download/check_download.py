#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查下载问题
- 检查是否使用迅雷等第三方下载工具
- 检查浏览器云加速下载设置
- 从下载链接提取域名
- 提供修复建议
"""

import os
import sys
import re
import platform
from urllib.parse import urlparse
from typing import List, Optional, Dict


# 下载代理域名列表
DOWNLOAD_PROXY_DOMAINS = [
    'proxy-rar.58pic.com',
    'proxy-vip.58pic.com',
    'proxy-vd.58pic.com',
]


def extract_domain_from_url(url: str) -> Optional[str]:
    """从URL中提取域名"""
    try:
        parsed = urlparse(url)
        return parsed.netloc or parsed.hostname
    except:
        return None


def check_download_url(url: str) -> Dict[str, any]:
    """
    检查下载URL
    
    Args:
        url: 下载链接
        
    Returns:
        检查结果字典
    """
    result = {
        'url': url,
        'domain': None,
        'is_proxy_domain': False,
        'needs_hosts_bind': False,
        'suggestions': [],
    }
    
    domain = extract_domain_from_url(url)
    if not domain:
        result['suggestions'].append('无法从URL中提取域名，请检查URL格式')
        return result
    
    result['domain'] = domain
    
    # 检查是否是下载代理域名
    for proxy_domain in DOWNLOAD_PROXY_DOMAINS:
        if domain == proxy_domain or domain.endswith('.' + proxy_domain):
            result['is_proxy_domain'] = True
            result['needs_hosts_bind'] = True
            result['suggestions'].append(f'需要绑定hosts: {domain}')
            break
    
    return result


def check_third_party_download_tools() -> List[str]:
    """
    检查是否安装了第三方下载工具
    
    Returns:
        已安装的下载工具列表
    """
    installed_tools = []
    system = platform.system()
    
    if system == 'Windows':
        # 检查迅雷
        thunder_paths = [
            r'C:\Program Files\Thunder Network',
            r'C:\Program Files (x86)\Thunder Network',
        ]
        for path in thunder_paths:
            if os.path.exists(path):
                installed_tools.append('迅雷')
                break
        
        # 检查其他下载工具
        # 可以添加更多检查逻辑
        
    elif system == 'Darwin':  # macOS
        # 检查迅雷
        thunder_path = '/Applications/Thunder.app'
        if os.path.exists(thunder_path):
            installed_tools.append('迅雷')
    
    return installed_tools


def check_browser_cloud_acceleration() -> Dict[str, bool]:
    """
    检查浏览器云加速下载设置
    
    Returns:
        各浏览器的云加速状态（如果可检测）
    """
    # 注意：实际检测浏览器设置比较复杂，这里只提供提示
    return {
        'Chrome': None,  # 无法自动检测
        'Edge': None,
        'Safari': None,
        '360': True,  # 360浏览器默认开启云加速
    }


def diagnose_download_issue(url: Optional[str] = None) -> Dict[str, any]:
    """
    诊断下载问题
    
    Args:
        url: 下载失败的URL（可选）
        
    Returns:
        诊断结果
    """
    result = {
        'third_party_tools': [],
        'cloud_acceleration': {},
        'url_check': None,
        'suggestions': [],
    }
    
    print("=" * 60)
    print("下载问题诊断")
    print("=" * 60)
    
    # 检查第三方下载工具
    print("\n1. 检查第三方下载工具...")
    third_party = check_third_party_download_tools()
    result['third_party_tools'] = third_party
    
    if third_party:
        print(f"   ⚠️  发现已安装: {', '.join(third_party)}")
        result['suggestions'].append(
            f'检测到已安装第三方下载工具: {", ".join(third_party)}。'
            '建议使用浏览器自带下载功能，不要使用第三方下载工具。'
        )
    else:
        print("   ✓ 未发现常见的第三方下载工具")
    
    # 检查浏览器云加速
    print("\n2. 检查浏览器云加速设置...")
    cloud_accel = check_browser_cloud_acceleration()
    result['cloud_acceleration'] = cloud_accel
    
    print("   提示: 请手动检查浏览器设置，关闭云加速下载功能")
    result['suggestions'].append(
        '检查浏览器设置，关闭云加速下载功能（如360浏览器的云加速）'
    )
    
    # 检查下载URL
    if url:
        print(f"\n3. 检查下载URL: {url}")
        url_check = check_download_url(url)
        result['url_check'] = url_check
        
        if url_check['domain']:
            print(f"   域名: {url_check['domain']}")
        
        if url_check['needs_hosts_bind']:
            print(f"   ⚠️  需要绑定hosts: {url_check['domain']}")
            result['suggestions'].append(
                f"需要绑定hosts文件: {url_check['domain']}。"
                "可以使用 bind_hosts.py 工具自动绑定。"
            )
        else:
            print("   ✓ URL域名检查通过")
    
    # 输出建议
    print("\n" + "=" * 60)
    print("修复建议:")
    print("=" * 60)
    
    if not result['suggestions']:
        print("未发现明显问题，建议:")
        print("1. 使用浏览器自带下载功能")
        print("2. 关闭浏览器云加速下载")
        print("3. 检查网络连接")
    else:
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"{i}. {suggestion}")
    
    return result


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='检查下载问题')
    parser.add_argument('--url', help='下载失败的URL')
    
    args = parser.parse_args()
    
    diagnose_download_issue(url=args.url)


if __name__ == '__main__':
    main()
