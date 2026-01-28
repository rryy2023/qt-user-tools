#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题卡片组件
可点击的问题卡片，用于主界面显示
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ProblemCard(QWidget):
    """问题卡片组件"""
    
    # 定义信号，点击修复按钮时发出
    fix_clicked = pyqtSignal(str)  # 传递问题类型
    
    # 问题图标映射
    ICONS = {
        'preview': '🖼️',
        'js': '🎨',
        'icon': '🎨',
        'download': '⬇️',
        'cloud': '☁️',
        'unbind_preview': '📦',
        'download_fail': '⚠️',
    }
    
    def __init__(self, problem_type: str, title: str, description: str, parent=None):
        super().__init__(parent)
        self.problem_type = problem_type
        self.title = title
        self.description = description
        
        self.init_ui()
        self.apply_style()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 判断是否为关键问题
        is_critical = self.problem_type in ['main_site', 'safari_cache']
        
        # 判断是否为关键问题
        is_critical = self.problem_type in ['main_site', 'safari_cache']
        
        # 图标和标题
        icon_text = self.ICONS.get(self.problem_type, '❓')
        title_label = QLabel(f"{icon_text} {self.title}")
        title_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))  # 增大字体
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        # 关键问题使用红色，普通问题使用深黑色（确保在白色背景上清晰可见）
        title_color = "#ff4d4f" if is_critical else "#000000"
        title_label.setStyleSheet(f"color: {title_color}; font-weight: bold;")
        self.title_label = title_label  # 保存引用
        
        # 描述
        desc_label = QLabel(self.description)
        desc_label.setFont(QFont("Arial", 10))  # 增大字体
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        # 描述文字使用深灰色（确保在白色背景上清晰可见）
        desc_color = "#333333"
        desc_label.setStyleSheet(f"color: {desc_color};")
        self.desc_label = desc_label  # 保存引用
        
        # 修复按钮
        fix_btn = QPushButton("一键修复")
        fix_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        fix_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        fix_btn.clicked.connect(lambda: self.fix_clicked.emit(self.problem_type))
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(fix_btn)
        
        self.setLayout(layout)
    
    def apply_style(self):
        """应用样式"""
        # 根据问题类型设置不同的背景色
        is_critical = self.problem_type in ['main_site', 'safari_cache']
        
        if is_critical:
            # 关键问题使用浅红色背景，文字使用深红色
            bg_color = "#fff1f0"
            hover_bg = "#ffe7e5"
            border_color = "#ffccc7"
        else:
            # 普通问题使用白色背景，提高文字可读性
            bg_color = "#ffffff"
            hover_bg = "#fafafa"
            border_color = "#e0e0e0"
        
        self.setStyleSheet(f"""
            ProblemCard {{
                background: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                min-height: 150px;
            }}
            ProblemCard:hover {{
                background: {hover_bg};
                border-color: #1890ff;
            }}
            ProblemCard QLabel {{
                background: transparent;
                color: #000000;
            }}
            ProblemCard QPushButton {{
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: bold;
                font-size: 11px;
            }}
            ProblemCard QPushButton:hover {{
                background-color: #40a9ff;
            }}
            ProblemCard QPushButton:pressed {{
                background-color: #096dd9;
            }}
        """)
        
        # 确保标题和描述颜色不被样式表覆盖（优先级更高）
        if is_critical:
            self.title_label.setStyleSheet("color: #ff4d4f; font-weight: bold;")
        else:
            self.title_label.setStyleSheet("color: #000000; font-weight: bold;")
        self.desc_label.setStyleSheet("color: #333333;")
