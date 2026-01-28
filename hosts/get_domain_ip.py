#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取域名对应的最优IP地址
支持从17ce.com获取或使用配置的IP
"""

import requests
import json
import os
import sys
from bs4 import BeautifulSoup
from typing import Optional, Dict, Tuple

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'config', 'domain_mappings.json')


def load_config() -> Dict[str, str]:
    """加载域名映射配置"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"警告: 配置文件 {CONFIG_PATH} 格式错误")
        return {}


def get_ip_from_17ce(domain: str) -> Optional[str]:
    """
    从17ce.com获取域名的最优IP
    
    尝试多种方式从17ce.com获取IP：
    1. 访问17ce.com的ping测试页面
    2. 解析返回的JSON或HTML数据
    3. 提取最快的节点IP
    
    Args:
        domain: 域名
        
    Returns:
        最优IP地址，如果获取失败返回None
    """
    try:
        # 方法1: 尝试访问17ce.com的ping测试API
        url = "http://17ce.com/site/ping"
        data = {
            'url': domain,
            'type': 'ping'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'http://17ce.com/',
            'Accept': 'application/json, text/html, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        response = requests.post(url, data=data, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # 尝试解析返回的JSON
            try:
                result = response.json()
                if result.get('status') == 'success' and result.get('data'):
                    # 找到最快的节点IP
                    nodes = result.get('data', [])
                    if nodes:
                        # 按响应时间排序，取最快的IPv4地址
                        sorted_nodes = sorted(nodes, key=lambda x: x.get('time', 999))
                        for node in sorted_nodes:
                            ip = node.get('ip')
                            if ip and is_ipv4(ip):  # 只使用IPv4地址
                                return ip
            except (ValueError, KeyError, TypeError):
                pass
            
            # 如果不是JSON，尝试解析HTML
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                import re
                # 查找IP地址
                ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                matches = re.findall(ip_pattern, response.text)
                if matches:
                    # 验证IP格式并返回第一个有效的IPv4地址
                    for match in matches:
                        if is_ipv4(match):
                            return match
            except:
                pass
        
        # 方法2: 尝试访问17ce.com的网站测速页面
        try:
            test_url = f"http://17ce.com/site/{domain}"
            response = requests.get(test_url, headers=headers, timeout=10)
            if response.status_code == 200:
                import re
                ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                matches = re.findall(ip_pattern, response.text)
                if matches:
                    for match in matches:
                        if is_ipv4(match):
                            # 排除一些明显不是目标IP的地址（如127.0.0.1, 0.0.0.0等）
                            if not match.startswith(('127.', '0.', '192.168.', '10.', '172.')):
                                return match
        except:
            pass
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"从17ce.com获取IP失败（网络错误）: {e}")
        return None
    except Exception as e:
        print(f"从17ce.com获取IP失败: {e}")
        return None


def get_ip_from_dns(domain: str) -> Optional[str]:
    """
    通过DNS查询获取域名IP（仅作为最后备用，用户本地可能无法访问域名）
    
    Args:
        domain: 域名
        
    Returns:
        IPv4地址，如果获取失败返回None
    """
    try:
        import socket
        # 只获取IPv4地址
        ip = socket.gethostbyname(domain)
        if ip and is_ipv4(ip):
            return ip
        return None
    except socket.gaierror:
        print(f"DNS查询失败: 无法解析域名 {domain}（用户本地可能无法访问此域名）")
        return None
    except Exception as e:
        print(f"DNS查询失败: {e}")
        return None


# 注意：已移除ping测试功能
# 因为用户本地可能无法访问这些域名，ping测试会失败
# 只使用第三方服务获取IP


def is_ipv4(ip: str) -> bool:
    """检查是否为IPv4地址"""
    import re
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(p) <= 255 for p in parts)
    return False


def get_ip_from_ipapi(domain: str) -> Optional[str]:
    """
    从ip-api.com获取域名IP（第三方服务）
    
    Args:
        domain: 域名
        
    Returns:
        IPv4地址，如果获取失败返回None
    """
    try:
        url = f"http://ip-api.com/json/{domain}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                ip = result.get('query')
                if ip and is_ipv4(ip):  # 只返回IPv4地址
                    return ip
        return None
    except Exception as e:
        print(f"从ip-api.com获取IP失败: {e}")
        return None


def get_ip_from_ipapi_co(domain: str) -> Optional[str]:
    """
    从ipapi.co获取域名IP（第三方服务）
    
    Args:
        domain: 域名
        
    Returns:
        IPv4地址，如果获取失败返回None
    """
    try:
        url = f"https://ipapi.co/{domain}/json/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if not result.get('error'):
                ip = result.get('ip')
                if ip and is_ipv4(ip):  # 只返回IPv4地址
                    return ip
        return None
    except Exception as e:
        print(f"从ipapi.co获取IP失败: {e}")
        return None


def get_ip_from_multiple_sources(domain: str) -> Tuple[Optional[str], str]:
    """
    从多个第三方服务获取IP地址
    
    注意：用户本地可能无法访问这些域名，因此：
    - 不使用ping测试（本地无法访问域名）
    - 不使用DNS查询作为主要方法（本地可能无法解析）
    - 优先使用第三方IP查询服务
    
    Args:
        domain: 域名
        
    Returns:
        (IP地址, 来源) 元组
    """
    # 第三方服务列表（按优先级排序）
    sources = [
        ("17ce.com", get_ip_from_17ce),
        ("ip-api.com", get_ip_from_ipapi),
        ("ipapi.co", get_ip_from_ipapi_co),
    ]
    
    for source_name, get_func in sources:
        try:
            print(f"正在从 {source_name} 获取 {domain} 的IP...")
            ip = get_func(domain)
            if ip and is_ipv4(ip):  # 确保是IPv4地址
                print(f"从 {source_name} 获取成功: {domain} -> {ip}")
                return ip, source_name
        except Exception as e:
            print(f"从 {source_name} 获取失败: {e}")
            continue
    
    # 如果所有第三方服务都失败，尝试DNS查询作为最后手段
    # 注意：用户本地可能无法访问这些域名，DNS查询很可能失败
    print(f"\n所有第三方服务获取失败，尝试DNS查询作为最后手段...")
    print(f"注意: 用户本地可能无法访问此域名，DNS查询可能失败")
    ip = get_ip_from_dns(domain)
    if ip and is_ipv4(ip):
        print(f"DNS查询成功: {domain} -> {ip}")
        return ip, "DNS查询"
    
    print(f"\n❌ 所有方法都失败，无法获取 {domain} 的IP地址")
    print(f"💡 提示:")
    print(f"   - 用户本地可能无法访问此域名")
    print(f"   - 建议在配置文件中手动设置IP地址")
    print(f"   - 或联系技术支持获取最新IP")
    return None, "失败"


def get_domain_ip(domain: str, use_config: bool = True) -> Optional[str]:
    """
    获取域名对应的IP地址（向后兼容版本，只返回IP）
    
    Args:
        domain: 域名
        use_config: 是否优先使用配置文件中的IP
        
    Returns:
        IP地址，如果获取失败返回None
    """
    ip, source = get_domain_ip_with_source(domain, use_config)
    return ip


def get_domain_ip_with_source(domain: str, use_config: bool = True) -> Tuple[Optional[str], str]:
    """
    获取域名对应的IP地址和来源
    
    Args:
        domain: 域名
        use_config: 是否优先使用配置文件中的IP
        
    Returns:
        (IP地址, 来源) 元组，如果获取失败返回 (None, "失败")
        来源可能的值: "配置文件", "17ce.com", "ip-api.com", "ipapi.co", "DNS查询", "失败"
        
    注意: 优先使用第三方服务，因为用户本地可能无法访问这些域名
    """
    # 优先使用配置文件中的IP
    if use_config:
        config = load_config()
        if domain in config and config[domain]:
            print(f"使用配置文件中的IP: {config[domain]}")
            return config[domain], "配置文件"
    
    # 从多个来源获取IP（按优先级顺序）
    ip, source = get_ip_from_multiple_sources(domain)
    
    if ip:
        return ip, source
    else:
        print(f"无法获取 {domain} 的IP地址")
        return None, "失败"


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='获取域名对应的IP地址')
    parser.add_argument('domain', help='要查询的域名')
    parser.add_argument('--no-config', action='store_true', 
                       help='不使用配置文件中的IP')
    
    args = parser.parse_args()
    
    ip, source = get_domain_ip_with_source(args.domain, use_config=not args.no_config)
    
    if ip:
        print(f"\n域名: {args.domain}")
        print(f"IP地址: {ip}")
        print(f"来源: {source}")
        sys.exit(0)
    else:
        print(f"\n无法获取 {args.domain} 的IP地址")
        sys.exit(1)


if __name__ == '__main__':
    main()
