#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hosts配置查看窗口
表格显示绑定列表，支持解绑
"""

import os
import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hosts.check_hosts import get_hosts_path, check_hosts
from hosts.unbind_hosts import unbind_domain, unbind_all_qiantu


class HostsViewer(QDialog):
    """Hosts配置查看窗口"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("Hosts配置管理")
        self.setMinimumSize(700, 500)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("📋 当前已绑定的千图相关域名")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["域名", "IP地址", "行号", "操作"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # 设置列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # 统计信息
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.stats_label)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.refresh_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)
        button_layout.addWidget(refresh_btn)
        
        unbind_all_btn = QPushButton("一键解绑所有")
        unbind_all_btn.clicked.connect(self.unbind_all)
        unbind_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4f;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #ff7875;
            }
        """)
        button_layout.addWidget(unbind_all_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def refresh_data(self):
        """刷新数据"""
        try:
            bindings = check_hosts()
            hosts_path = get_hosts_path()
            
            # 更新表格
            self.table.setRowCount(len(bindings))
            
            row = 0
            for domain, info in sorted(bindings.items()):
                # 域名
                domain_item = QTableWidgetItem(domain)
                self.table.setItem(row, 0, domain_item)
                
                # IP地址
                ip = info.get('ip', '未绑定')
                ip_item = QTableWidgetItem(ip)
                if ip == '未绑定':
                    ip_item.setForeground(Qt.GlobalColor.gray)
                self.table.setItem(row, 1, ip_item)
                
                # 行号
                line_item = QTableWidgetItem(str(info.get('line', 'N/A')))
                self.table.setItem(row, 2, line_item)
                
                # 操作按钮
                if ip != '未绑定':
                    unbind_btn = QPushButton("解绑")
                    unbind_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #ff4d4f;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 4px 10px;
                        }
                        QPushButton:hover {
                            background-color: #ff7875;
                        }
                    """)
                    unbind_btn.clicked.connect(lambda checked, d=domain: self.unbind_domain(d))
                    self.table.setCellWidget(row, 3, unbind_btn)
                else:
                    self.table.setItem(row, 3, QTableWidgetItem("-"))
                
                row += 1
            
            # 更新统计信息
            bound_count = sum(1 for info in bindings.values() if info.get('ip') and info.get('ip') != '未绑定')
            total_count = len(bindings)
            self.stats_label.setText(
                f"统计: 已绑定 {bound_count} 个域名，未绑定 {total_count - bound_count} 个域名 | "
                f"Hosts文件: {hosts_path}"
            )
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"刷新数据失败: {str(e)}")
    
    def unbind_domain(self, domain: str):
        """解绑域名"""
        reply = QMessageBox.question(
            self,
            "确认解绑",
            f"确定要解绑域名 {domain} 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = unbind_domain(domain, auto_fix=True)
                if success:
                    QMessageBox.information(
                        self,
                        "成功",
                        f"已成功解绑域名: {domain}\n\n请刷新浏览器以使更改生效。"
                    )
                    self.refresh_data()
                else:
                    QMessageBox.warning(self, "失败", "解绑失败，请检查权限")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"解绑失败: {str(e)}")
    
    def unbind_all(self):
        """解绑所有域名"""
        reply = QMessageBox.question(
            self,
            "确认解绑",
            "确定要解绑所有千图相关域名吗？\n\n此操作不可撤销！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = unbind_all_qiantu(auto_fix=True)
                if success:
                    QMessageBox.information(
                        self,
                        "成功",
                        "已成功解绑所有千图相关域名\n\n请刷新浏览器以使更改生效。"
                    )
                    self.refresh_data()
                else:
                    QMessageBox.warning(self, "失败", "解绑失败，请检查权限")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"解绑失败: {str(e)}")
