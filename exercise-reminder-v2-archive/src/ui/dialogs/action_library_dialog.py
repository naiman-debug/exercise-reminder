# -*- coding: utf-8 -*-
"""
动作库对话框 - 管理运动动作

TODO: 实现完整的动作库功能
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ActionLibraryDialog(QDialog):
    """动作库对话框 - 占位实现"""

    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("打开动作库")

        self.setWindowTitle("🏋️ 动作库管理")
        self.setMinimumSize(600, 400)

        self._setup_ui()

    def _setup_ui(self):
        """设置 UI"""
        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("🏋️ 动作库管理")
        title.setStyleSheet("font-size: 18pt; font-weight: 600; color: #2C2C2C;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 占位内容区域
        content_frame = QFrame()
        content_frame.setStyleSheet("background-color: #F5F5F5; border-radius: 12px;")
        content_layout = QVBoxLayout(content_frame)

        placeholder_label = QLabel("动作库功能开发中...")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_label.setStyleSheet("font-size: 14pt; color: #6B6B6B; padding: 40px;")
        content_layout.addWidget(placeholder_label)

        layout.addWidget(content_frame)

        # 关闭按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_button = QPushButton("关闭")
        close_button.setFixedSize(100, 36)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

    def accept(self):
        """接受对话框"""
        logger.info("关闭动作库")
        super().accept()

    def reject(self):
        """拒绝对话框"""
        logger.info("取消动作库")
        super().reject()
