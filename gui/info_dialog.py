#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户信息收集对话框
标签页显示各类信息，支持导出
"""

import os
import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QTextEdit, QProgressBar, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QClipboard, QGuiApplication

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.system_info import SystemInfoCollector


class InfoCollectorWorker(QThread):
    """信息收集工作线程"""
    progress_updated = pyqtSignal(int, str)  # 进度, 消息
    finished = pyqtSignal(dict)  # 收集的数据
    
    def __init__(self):
        super().__init__()
        self.collector = SystemInfoCollector()
    
    def run(self):
        """执行收集"""
        try:
            self.progress_updated.emit(10, "正在收集系统信息...")
            system_info = self.collector.get_system_info()
            
            self.progress_updated.emit(25, "正在收集浏览器信息...")
            browser_info = self.collector.get_browser_info()
            
            self.progress_updated.emit(40, "正在收集网络信息...")
            network_info = self.collector.get_network_info()
            
            self.progress_updated.emit(55, "正在收集DNS信息...")
            dns_info = self.collector.get_dns_info()
            
            self.progress_updated.emit(70, "正在收集Hosts信息...")
            hosts_info = self.collector.get_hosts_info()
            
            self.progress_updated.emit(85, "正在执行Ping测试...")
            ping_info = self.collector.ping_domains()
            
            self.progress_updated.emit(95, "正在检查权限...")
            perm_info = self.collector.check_permissions()
            
            data = {
                'system': system_info,
                'browser': browser_info,
                'network': network_info,
                'dns': dns_info,
                'hosts': hosts_info,
                'ping': ping_info,
                'permissions': perm_info,
            }
            
            self.progress_updated.emit(100, "收集完成！")
            self.finished.emit(data)
            
        except Exception as e:
            self.finished.emit({'error': str(e)})


class InfoDialog(QDialog):
    """信息收集对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {}
        self.worker = None
        self.init_ui()
        self.start_collect()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("系统信息收集")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 进度条（收集时显示）
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("正在收集信息...")
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)
        
        # 标签页
        self.tabs = QTabWidget()
        
        # 系统信息标签页
        self.system_tab = self.create_table_tab()
        self.tabs.addTab(self.system_tab, "系统信息")
        
        # 浏览器信息标签页
        self.browser_tab = self.create_table_tab()
        self.tabs.addTab(self.browser_tab, "浏览器信息")
        
        # 网络信息标签页
        self.network_tab = self.create_table_tab()
        self.tabs.addTab(self.network_tab, "网络信息")
        
        # DNS信息标签页
        self.dns_tab = self.create_table_tab()
        self.tabs.addTab(self.dns_tab, "DNS信息")
        
        # Hosts信息标签页
        self.hosts_tab = self.create_table_tab()
        self.tabs.addTab(self.hosts_tab, "Hosts信息")
        
        # Ping测试标签页
        self.ping_tab = self.create_table_tab()
        self.tabs.addTab(self.ping_tab, "Ping测试")
        
        # 权限信息标签页
        self.perm_tab = self.create_table_tab()
        self.tabs.addTab(self.perm_tab, "权限信息")
        
        layout.addWidget(self.tabs, 1)  # 标签页占据剩余空间
        
        # 按钮区域（固定在底部）
        button_widget = QWidget()
        button_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 1px solid #e0e0e0;
            }
        """)
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(15, 15, 15, 15)
        button_layout.setSpacing(10)
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.start_collect)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)
        button_layout.addWidget(refresh_btn)
        
        copy_btn = QPushButton("📋 复制到剪贴板")
        copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(copy_btn)
        
        export_btn = QPushButton("💾 导出为文本")
        export_btn.clicked.connect(self.export_to_file)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget, 0)  # 按钮区域不拉伸，固定在底部
        
        self.setLayout(layout)
    
    def create_table_tab(self) -> QWidget:
        """创建表格标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["项目", "值"])
        table.horizontalHeader().setStretchLastSection(True)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(table)
        widget.setLayout(layout)
        return widget
    
    def populate_table(self, table: QTableWidget, data: dict):
        """填充表格数据"""
        table.setRowCount(len(data))
        row = 0
        for key, value in data.items():
            if key == 'error':
                continue
            
            key_item = QTableWidgetItem(str(key))
            value_item = QTableWidgetItem(str(value) if value is not None else 'N/A')
            
            table.setItem(row, 0, key_item)
            table.setItem(row, 1, value_item)
            row += 1
    
    def start_collect(self):
        """开始收集信息"""
        self.progress_bar.setVisible(True)
        self.status_label.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("正在收集信息...")
        
        self.worker = InfoCollectorWorker()
        self.worker.progress_updated.connect(self.on_progress_updated)
        self.worker.finished.connect(self.on_collect_finished)
        self.worker.start()
    
    def on_progress_updated(self, value: int, message: str):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def on_collect_finished(self, data: dict):
        """收集完成"""
        self.progress_bar.setVisible(False)
        self.status_label.setVisible(False)
        
        if 'error' in data:
            QMessageBox.warning(self, "错误", f"收集信息时出错: {data['error']}")
            return
        
        self.data = data
        
        # 更新各个标签页
        self.update_system_tab(data.get('system', {}))
        self.update_browser_tab(data.get('browser', {}))
        self.update_network_tab(data.get('network', {}))
        self.update_dns_tab(data.get('dns', {}))
        self.update_hosts_tab(data.get('hosts', {}))
        self.update_ping_tab(data.get('ping', {}))
        self.update_perm_tab(data.get('permissions', {}))
    
    def update_system_tab(self, data: dict):
        """更新系统信息标签页"""
        table = self.system_tab.findChild(QTableWidget)
        if table:
            items = [
                ('操作系统', data.get('os', 'N/A')),
                ('系统版本', data.get('version', 'N/A')),
                ('系统架构', data.get('architecture', 'N/A')),
                ('处理器', data.get('processor', 'N/A')),
                ('Python版本', data.get('python_version', 'N/A')),
            ]
            table.setRowCount(len(items))
            for row, (key, value) in enumerate(items):
                table.setItem(row, 0, QTableWidgetItem(key))
                table.setItem(row, 1, QTableWidgetItem(str(value)))
    
    def update_browser_tab(self, data: dict):
        """更新浏览器信息标签页"""
        table = self.browser_tab.findChild(QTableWidget)
        if table:
            items = []
            for browser_name, info in data.items():
                if info.get('installed'):
                    items.append((browser_name, f"版本: {info.get('version', 'N/A')}, 兼容: {'✓' if info.get('compatible') else '✗'}"))
                else:
                    items.append((browser_name, "未安装"))
            
            table.setRowCount(len(items))
            for row, (key, value) in enumerate(items):
                table.setItem(row, 0, QTableWidgetItem(key))
                table.setItem(row, 1, QTableWidgetItem(str(value)))
    
    def update_network_tab(self, data: dict):
        """更新网络信息标签页"""
        table = self.network_tab.findChild(QTableWidget)
        if table:
            items = [
                ('主机名', data.get('hostname', 'N/A')),
                ('本机IP', data.get('local_ip', 'N/A')),
                ('公网IP', data.get('public_ip', 'N/A')),
            ]
            
            if data.get('interfaces'):
                for iface in data['interfaces']:
                    items.append((f"接口: {iface.get('name')}", f"IP: {iface.get('ip', 'N/A')}"))
            
            table.setRowCount(len(items))
            for row, (key, value) in enumerate(items):
                table.setItem(row, 0, QTableWidgetItem(key))
                table.setItem(row, 1, QTableWidgetItem(str(value)))
    
    def update_dns_tab(self, data: dict):
        """更新DNS信息标签页"""
        table = self.dns_tab.findChild(QTableWidget)
        if table:
            items = [
                ('DNS服务器', ', '.join(data.get('servers', [])) or 'N/A'),
                ('缓存状态', data.get('cache_status', 'N/A')),
            ]
            table.setRowCount(len(items))
            for row, (key, value) in enumerate(items):
                table.setItem(row, 0, QTableWidgetItem(key))
                table.setItem(row, 1, QTableWidgetItem(str(value)))
    
    def update_hosts_tab(self, data: dict):
        """更新Hosts信息标签页"""
        table = self.hosts_tab.findChild(QTableWidget)
        if table:
            items = [
                ('文件路径', data.get('path', 'N/A')),
                ('文件存在', '✓' if data.get('exists') else '✗'),
                ('可读', '✓' if data.get('readable') else '✗'),
                ('可写', '✓' if data.get('writable') else '✗'),
                ('已绑定域名数', str(data.get('binding_count', 0))),
            ]
            
            if data.get('bindings'):
                for binding in data['bindings']:
                    items.append((binding.get('domain', 'N/A'), f"{binding.get('ip', 'N/A')} (行{binding.get('line', 'N/A')})"))
            
            table.setRowCount(len(items))
            for row, (key, value) in enumerate(items):
                table.setItem(row, 0, QTableWidgetItem(key))
                table.setItem(row, 1, QTableWidgetItem(str(value)))
    
    def update_ping_tab(self, data: dict):
        """更新Ping测试标签页"""
        table = self.ping_tab.findChild(QTableWidget)
        if table:
            items = []
            for domain, result in data.items():
                if result.get('success'):
                    items.append((domain, f"IP: {result.get('ip', 'N/A')}, 延迟: {result.get('latency', 'N/A')}, 丢包: {result.get('loss', 'N/A')}"))
                else:
                    items.append((domain, f"✗ 失败: {result.get('error', 'N/A')}"))
            
            table.setRowCount(len(items))
            for row, (key, value) in enumerate(items):
                table.setItem(row, 0, QTableWidgetItem(key))
                table.setItem(row, 1, QTableWidgetItem(str(value)))
    
    def update_perm_tab(self, data: dict):
        """更新权限信息标签页"""
        table = self.perm_tab.findChild(QTableWidget)
        if table:
            items = [
                ('管理员权限', '✓' if data.get('admin') else '✗'),
                ('Hosts可读', '✓' if data.get('hosts_readable') else '✗'),
                ('Hosts可写', '✓' if data.get('hosts_writable') else '✗'),
            ]
            table.setRowCount(len(items))
            for row, (key, value) in enumerate(items):
                table.setItem(row, 0, QTableWidgetItem(key))
                table.setItem(row, 1, QTableWidgetItem(str(value)))
    
    def copy_to_clipboard(self):
        """复制到剪贴板"""
        if not self.data:
            QMessageBox.warning(self, "提示", "请先收集信息")
            return
        
        collector = SystemInfoCollector()
        text = collector.format_text_report(self.data)
        
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "成功", "信息已复制到剪贴板")
    
    def export_to_file(self):
        """导出为文本文件"""
        if not self.data:
            QMessageBox.warning(self, "提示", "请先收集信息")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "导出信息",
            f"系统信息_{os.path.basename(os.getcwd())}.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if filename:
            try:
                collector = SystemInfoCollector()
                text = collector.format_text_report(self.data)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                QMessageBox.information(self, "成功", f"信息已导出到: {filename}")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导出失败: {str(e)}")
