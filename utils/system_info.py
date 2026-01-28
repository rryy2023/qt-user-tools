#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统信息收集工具
收集系统、浏览器、网络、DNS、hosts、ping等信息
"""

import os
import sys
import platform
import socket
import subprocess
import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import netifaces
    HAS_NETIFACES = True
except ImportError:
    HAS_NETIFACES = False

# 导入现有模块
from browser.check_browser import check_browser_version, check_all_browsers
from hosts.check_hosts import get_hosts_path, check_hosts, QIANTU_DOMAINS


class SystemInfoCollector:
    """系统信息收集器"""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_system_info(self) -> Dict:
        """获取系统信息"""
        try:
            info = {
                'os': self.system,
                'version': platform.version(),
                'release': platform.release(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'python_implementation': platform.python_implementation(),
            }
            
            # 获取更详细的系统版本信息
            if self.system == 'Darwin':  # macOS
                try:
                    result = subprocess.run(['sw_vers'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if 'ProductVersion:' in line:
                                info['version'] = line.split(':')[1].strip()
                            elif 'ProductName:' in line:
                                info['os'] = line.split(':')[1].strip()
                except:
                    pass
            elif self.system == 'Windows':
                try:
                    result = subprocess.run(['systeminfo'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if 'OS Name:' in line:
                                info['os'] = line.split(':', 1)[1].strip()
                            elif 'OS Version:' in line:
                                info['version'] = line.split(':', 1)[1].strip()
                except:
                    pass
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def get_browser_info(self) -> Dict:
        """获取浏览器信息"""
        try:
            browsers = check_all_browsers()
            result = {}
            
            for browser_name, browser_info in browsers.items():
                result[browser_name] = {
                    'installed': browser_info.get('installed', False),
                    'version': browser_info.get('version'),
                    'compatible': browser_info.get('compatible', False),
                    'needs_upgrade': browser_info.get('needs_upgrade', False),
                }
            
            return result
        except Exception as e:
            return {'error': str(e)}
    
    def get_network_info(self) -> Dict:
        """获取网络信息"""
        try:
            info = {
                'local_ip': None,
                'public_ip': None,
                'hostname': socket.gethostname(),
                'interfaces': [],
            }
            
            # 获取本机IP地址
            try:
                # 方法1: 通过socket连接获取
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 80))
                info['local_ip'] = s.getsockname()[0]
                s.close()
            except:
                pass
            
            # 使用netifaces获取网络接口信息
            if HAS_NETIFACES:
                try:
                    interfaces = netifaces.interfaces()
                    for iface in interfaces:
                        addrs = netifaces.ifaddresses(iface)
                        if netifaces.AF_INET in addrs:
                            for addr in addrs[netifaces.AF_INET]:
                                interface_info = {
                                    'name': iface,
                                    'ip': addr.get('addr'),
                                    'netmask': addr.get('netmask'),
                                    'broadcast': addr.get('broadcast'),
                                }
                                info['interfaces'].append(interface_info)
                                
                                # 如果还没有本地IP，使用第一个非回环接口的IP
                                if not info['local_ip'] and iface != 'lo':
                                    info['local_ip'] = addr.get('addr')
                except:
                    pass
            
            # 获取公网IP
            try:
                import requests
                response = requests.get('https://api.ipify.org?format=json', timeout=5)
                if response.status_code == 200:
                    info['public_ip'] = response.json().get('ip')
            except:
                try:
                    # 备用方法
                    import requests
                    response = requests.get('https://ifconfig.me/ip', timeout=5)
                    if response.status_code == 200:
                        info['public_ip'] = response.text.strip()
                except:
                    pass
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def get_dns_info(self) -> Dict:
        """获取DNS信息"""
        try:
            info = {
                'servers': [],
                'cache_status': 'unknown',
            }
            
            if self.system == 'Windows':
                try:
                    result = subprocess.run(['ipconfig', '/all'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if 'DNS Servers' in line or 'DNS 服务器' in line:
                                # 提取DNS服务器地址
                                match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                                if match:
                                    info['servers'].append(match.group(1))
                    info['cache_status'] = 'active'
                except:
                    pass
            elif self.system == 'Darwin':  # macOS
                try:
                    result = subprocess.run(['scutil', '--dns'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if 'nameserver' in line.lower():
                                match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                                if match and match.group(1) not in info['servers']:
                                    info['servers'].append(match.group(1))
                    info['cache_status'] = 'active'
                except:
                    pass
            elif self.system == 'Linux':
                try:
                    with open('/etc/resolv.conf', 'r') as f:
                        for line in f:
                            if line.startswith('nameserver'):
                                ip = line.split()[1] if len(line.split()) > 1 else None
                                if ip and ip not in info['servers']:
                                    info['servers'].append(ip)
                    info['cache_status'] = 'active'
                except:
                    pass
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def get_hosts_info(self) -> Dict:
        """获取Hosts信息"""
        try:
            hosts_path = get_hosts_path()
            bindings = check_hosts()
            
            info = {
                'path': hosts_path,
                'exists': os.path.exists(hosts_path),
                'readable': os.access(hosts_path, os.R_OK) if os.path.exists(hosts_path) else False,
                'writable': os.access(hosts_path, os.W_OK) if os.path.exists(hosts_path) else False,
                'bindings': [],
                'binding_count': len(bindings),
            }
            
            for domain, binding_info in bindings.items():
                info['bindings'].append({
                    'domain': domain,
                    'ip': binding_info.get('ip'),
                    'line': binding_info.get('line'),
                    'raw_line': binding_info.get('raw_line'),
                })
            
            return info
        except Exception as e:
            return {'error': str(e), 'path': get_hosts_path()}
    
    def ping_domain(self, domain: str, count: int = 4) -> Dict:
        """Ping域名测试"""
        try:
            result = {
                'domain': domain,
                'ip': None,
                'latency': None,
                'loss': None,
                'success': False,
                'error': None,
            }
            
            # 先解析域名获取IP
            try:
                ip = socket.gethostbyname(domain)
                result['ip'] = ip
            except socket.gaierror as e:
                result['error'] = f'DNS解析失败: {str(e)}'
                return result
            
            # 执行ping
            if self.system == 'Windows':
                cmd = ['ping', '-n', str(count), domain]
            else:
                cmd = ['ping', '-c', str(count), domain]
            
            try:
                ping_result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if ping_result.returncode == 0:
                    # 解析ping结果
                    output = ping_result.stdout
                    
                    # 提取延迟信息
                    if self.system == 'Windows':
                        # Windows格式: 平均 = 12ms
                        match = re.search(r'平均\s*=\s*(\d+)ms', output)
                        if not match:
                            match = re.search(r'Average\s*=\s*(\d+)ms', output)
                        if match:
                            result['latency'] = f"{match.group(1)}ms"
                    else:
                        # Unix格式: min/avg/max/mdev = 10.123/12.456/15.789/2.123 ms
                        match = re.search(r'min/avg/max/[^=]*=\s*([\d.]+)/([\d.]+)/([\d.]+)', output)
                        if match:
                            result['latency'] = f"{match.group(2)}ms"
                    
                    # 提取丢包率
                    if self.system == 'Windows':
                        match = re.search(r'\((\d+)%', output)
                        if match:
                            loss = int(match.group(1))
                            result['loss'] = f"{loss}%"
                        else:
                            result['loss'] = "0%"
                    else:
                        match = re.search(r'(\d+)% packet loss', output)
                        if match:
                            result['loss'] = f"{match.group(1)}%"
                        else:
                            result['loss'] = "0%"
                    
                    result['success'] = True
                else:
                    result['error'] = 'Ping失败'
                    result['loss'] = "100%"
                    
            except subprocess.TimeoutExpired:
                result['error'] = 'Ping超时'
            except Exception as e:
                result['error'] = str(e)
            
            return result
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e),
                'success': False,
            }
    
    def ping_domains(self, domains: Optional[List[str]] = None) -> Dict:
        """Ping多个域名"""
        if domains is None:
            domains = [
                'preview.qiantucdn.com',
                'js.qiantucdn.com',
                'icon.qiantucdn.com',
                'dl.58pic.com',
                'y.58pic.com',
                'proxy-rar.58pic.com',
                'proxy-vip.58pic.com',
                'proxy-vd.58pic.com',
            ]
        
        results = {}
        for domain in domains:
            results[domain] = self.ping_domain(domain)
        
        return results
    
    def check_permissions(self) -> Dict:
        """检查权限状态"""
        try:
            info = {
                'admin': False,
                'hosts_readable': False,
                'hosts_writable': False,
            }
            
            if self.system == 'Windows':
                try:
                    import ctypes
                    info['admin'] = ctypes.windll.shell32.IsUserAnAdmin() != 0
                except:
                    pass
            else:
                info['admin'] = os.geteuid() == 0
            
            hosts_path = get_hosts_path()
            if os.path.exists(hosts_path):
                info['hosts_readable'] = os.access(hosts_path, os.R_OK)
                info['hosts_writable'] = os.access(hosts_path, os.W_OK)
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def collect_all(self) -> Dict:
        """收集所有信息"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system': self.get_system_info(),
            'browser': self.get_browser_info(),
            'network': self.get_network_info(),
            'dns': self.get_dns_info(),
            'hosts': self.get_hosts_info(),
            'ping': self.ping_domains(),
            'permissions': self.check_permissions(),
        }
    
    def format_text_report(self, data: Optional[Dict] = None) -> str:
        """格式化文本报告"""
        if data is None:
            data = self.collect_all()
        
        lines = []
        lines.append("=" * 60)
        lines.append("千图网问题解决工具 - 系统信息报告")
        lines.append("=" * 60)
        lines.append(f"生成时间: {data.get('timestamp', 'N/A')}")
        lines.append("")
        
        # 系统信息
        lines.append("【系统信息】")
        sys_info = data.get('system', {})
        lines.append(f"  操作系统: {sys_info.get('os', 'N/A')}")
        lines.append(f"  系统版本: {sys_info.get('version', 'N/A')}")
        lines.append(f"  系统架构: {sys_info.get('architecture', 'N/A')}")
        lines.append(f"  Python版本: {sys_info.get('python_version', 'N/A')}")
        lines.append("")
        
        # 浏览器信息
        lines.append("【浏览器信息】")
        browser_info = data.get('browser', {})
        for browser_name, info in browser_info.items():
            if info.get('installed'):
                lines.append(f"  {browser_name}:")
                lines.append(f"    版本: {info.get('version', 'N/A')}")
                lines.append(f"    兼容性: {'✓ 兼容' if info.get('compatible') else '⚠ 需要升级'}")
            else:
                lines.append(f"  {browser_name}: 未安装")
        lines.append("")
        
        # 网络信息
        lines.append("【网络信息】")
        net_info = data.get('network', {})
        lines.append(f"  主机名: {net_info.get('hostname', 'N/A')}")
        lines.append(f"  本机IP: {net_info.get('local_ip', 'N/A')}")
        lines.append(f"  公网IP: {net_info.get('public_ip', 'N/A')}")
        if net_info.get('interfaces'):
            lines.append("  网络接口:")
            for iface in net_info['interfaces']:
                lines.append(f"    {iface.get('name')}: {iface.get('ip')}")
        lines.append("")
        
        # DNS信息
        lines.append("【DNS信息】")
        dns_info = data.get('dns', {})
        lines.append(f"  DNS服务器: {', '.join(dns_info.get('servers', [])) or 'N/A'}")
        lines.append(f"  缓存状态: {dns_info.get('cache_status', 'N/A')}")
        lines.append("")
        
        # Hosts信息
        lines.append("【Hosts信息】")
        hosts_info = data.get('hosts', {})
        lines.append(f"  文件路径: {hosts_info.get('path', 'N/A')}")
        lines.append(f"  可读: {'✓' if hosts_info.get('readable') else '✗'}")
        lines.append(f"  可写: {'✓' if hosts_info.get('writable') else '✗'}")
        lines.append(f"  已绑定域名数: {hosts_info.get('binding_count', 0)}")
        if hosts_info.get('bindings'):
            lines.append("  绑定列表:")
            for binding in hosts_info['bindings']:
                lines.append(f"    {binding.get('domain')} -> {binding.get('ip', 'N/A')} (行{binding.get('line', 'N/A')})")
        lines.append("")
        
        # Ping测试
        lines.append("【Ping测试】")
        ping_info = data.get('ping', {})
        for domain, result in ping_info.items():
            if result.get('success'):
                lines.append(f"  {domain}:")
                lines.append(f"    IP: {result.get('ip', 'N/A')}")
                lines.append(f"    延迟: {result.get('latency', 'N/A')}")
                lines.append(f"    丢包率: {result.get('loss', 'N/A')}")
            else:
                lines.append(f"  {domain}: ✗ 失败 ({result.get('error', 'N/A')})")
        lines.append("")
        
        # 权限信息
        lines.append("【权限信息】")
        perm_info = data.get('permissions', {})
        lines.append(f"  管理员权限: {'✓' if perm_info.get('admin') else '✗'}")
        lines.append(f"  Hosts可读: {'✓' if perm_info.get('hosts_readable') else '✗'}")
        lines.append(f"  Hosts可写: {'✓' if perm_info.get('hosts_writable') else '✗'}")
        lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


if __name__ == '__main__':
    collector = SystemInfoCollector()
    data = collector.collect_all()
    print(collector.format_text_report(data))
