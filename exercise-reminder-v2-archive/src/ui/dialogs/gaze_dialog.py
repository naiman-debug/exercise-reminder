# -*- coding: utf-8 -*-
"""
强制远眺提醒弹窗

显示"请远眺"和60秒倒计时，不可跳过
"""
from PySide6.QtWidgets import QLabel, QVBoxLayout, QApplication, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor
from .base_dialog import BaseReminderDialog


class GazeReminderDialog(BaseReminderDialog):
    """
    强制远眺提醒弹窗

    显示"请远眺20秒外"和60秒倒计时，不可跳过，不可关闭
    """

    def __init__(self, duration: int = 60, parent=None):
        """
        初始化强制远眺弹窗

        Args:
            duration: 倒计时时长（秒），默认60秒
            parent: 父窗口
        """
        self.duration = duration
        # 明确指定无边框（设计文档5.3节要求）
        super().__init__(parent, has_title_bar=False)

        # 覆盖尺寸：设计文档5.3节要求屏幕宽×50%，高×40%
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width = int(screen_geometry.width() * 0.50)
        height = int(screen_geometry.height() * 0.40)
        self.setFixedSize(width, height)

        # UI 组件
        self.title_label = None
        self.countdown_label = None
        self.hint_label = None

        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 创建布局
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # 标题图标和文字
        title_widget = self._create_title_widget()
        layout.addWidget(title_widget)

        # 倒计时
        self.countdown_label = QLabel()
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        countdown_font = QFont("Consolas", 96, QFont.Weight.Bold)
        self.countdown_label.setFont(countdown_font)

        # 提示
        self.hint_label = QLabel("（放松眼睛，眺望远方，让眼睛休息）")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_font = QFont("Microsoft YaHei UI", 16)
        self.hint_label.setFont(hint_font)

        # 添加到布局
        layout.addStretch(1)
        layout.addWidget(self.countdown_label)
        layout.addStretch(1)
        layout.addWidget(self.hint_label)

        self.setLayout(layout)

    def showEvent(self, event):
        """
        窗口显示事件 - 自动启动倒计时
        """
        super().showEvent(event)
        # 自动启动倒计时
        self.start_countdown(self.duration)

    def _create_title_widget(self) -> QWidget:
        """创建标题组件"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 图标
        self.icon_label = QLabel("👁️")
        icon_font = QFont("Microsoft YaHei UI", 64)
        self.icon_label.setFont(icon_font)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 文字
        self.text_label = QLabel("请远眺20秒外")
        text_font = QFont("Microsoft YaHei UI", 32, QFont.Weight.Bold)
        self.text_label.setFont(text_font)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)

        return widget

    def _apply_styles(self):
        """应用样式"""
        # 移除独立设置大小，现在使用 base_dialog 的统一大小

        # 设置浅蓝色背景（保持远眺的特色）
        self.setStyleSheet("""
            GazeReminderDialog {
                background-color: #E3F2FD;
                border-radius: 16px;
            }
        """)

        # 设置图标颜色
        icon_palette = self.icon_label.palette()
        icon_palette.setColor(QPalette.ColorRole.WindowText, QColor("#1565C0"))
        self.icon_label.setPalette(icon_palette)

        # 设置文字颜色
        text_palette = self.text_label.palette()
        text_palette.setColor(QPalette.ColorRole.WindowText, QColor("#1565C0"))
        self.text_label.setPalette(text_palette)

        # 设置提示颜色
        hint_palette = self.hint_label.palette()
        hint_palette.setColor(QPalette.ColorRole.WindowText, QColor("#0D47A1"))
        self.hint_label.setPalette(hint_palette)

    def _update_countdown_display(self):
        """更新倒计时显示"""
        # 更新显示文本
        self.countdown_label.setText(f"{self.remaining_seconds:02d}")

        # 使用统一的倒计时颜色方案
        color = self.get_countdown_color(self.remaining_seconds, self.duration)

        self.countdown_label.setStyleSheet(f"QLabel {{ color: {color}; }}")

    def _show_complete_feedback(self):
        """显示完成反馈"""
        # 显示✓反馈
        original_text = self.countdown_label.text()
        self.countdown_label.setText("✓ 完成")
        self.countdown_label.setStyleSheet("QLabel { color: #4CAF50; }")

    def skip(self):
        """
        跳过（重写基类方法，强制远眺不允许跳过）

        强制远眺弹窗不允许跳过，所以此方法不做任何操作
        """
        # 强制远眺不允许跳过
        pass

    def keyPressEvent(self, event):
        """
        键盘事件处理

        Args:
            event: 键盘事件
        """
        # 所有键盘事件都禁用（包括 ESC）
        pass
