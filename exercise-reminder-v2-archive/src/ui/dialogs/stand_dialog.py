# -*- coding: utf-8 -*-
"""
强制站立提醒弹窗

显示"请站立"和倒计时，不可跳过
"""
from PySide6.QtWidgets import QLabel, QVBoxLayout, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor
from .base_dialog import BaseReminderDialog


class StandReminderDialog(BaseReminderDialog):
    """
    强制站立提醒弹窗

    显示"请站立"和大字倒计时，不可跳过，不可关闭
    """

    def __init__(self, duration: int, parent=None):
        """
        初始化强制站立弹窗

        Args:
            duration: 倒计时时长（秒）
            parent: 父窗口
        """
        self.duration = duration
        # 明确指定无边框（设计文档5.1节要求）
        super().__init__(parent, has_title_bar=False)

        # 覆盖尺寸：设计文档5.1节要求屏幕宽×60%，高×50%
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width = int(screen_geometry.width() * 0.60)
        height = int(screen_geometry.height() * 0.50)
        self.setFixedSize(width, height)

        # UI 组件
        self.title_label = None
        self.countdown_label = None
        self.hint_label = None

        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 创建主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # 标题
        self.title_label = QLabel("⏰ 请站立休息 ⏰")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Microsoft YaHei UI", 48, QFont.Weight.Bold)
        self.title_label.setFont(title_font)

        # 倒计时
        self.countdown_label = QLabel()
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        countdown_font = QFont("Consolas", 120, QFont.Weight.Bold)
        self.countdown_label.setFont(countdown_font)

        # 提示
        self.hint_label = QLabel("（请保持站立，等待倒计时结束）")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_font = QFont("Microsoft YaHei UI", 18)
        self.hint_label.setFont(hint_font)

        # 设置样式
        self._apply_styles()

        # 添加到布局
        layout.addWidget(self.title_label)
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

    def _apply_styles(self):
        """应用样式"""
        # 移除独立设置大小，现在使用 base_dialog 的统一大小

        # 设置样式表
        self.setStyleSheet("""
            QLabel#centralWidget {
                background-color: #FFFFFF;
                border-radius: 16px;
            }
            StandReminderDialog {
                background-color: #FFFFFF;
                border-radius: 16px;
            }
        """)

        # 设置标题颜色
        title_palette = self.title_label.palette()
        title_palette.setColor(QPalette.ColorRole.WindowText, QColor("#212121"))
        self.title_label.setPalette(title_palette)

        # 设置提示颜色
        hint_palette = self.hint_label.palette()
        hint_palette.setColor(QPalette.ColorRole.WindowText, QColor("#757575"))
        self.hint_label.setPalette(hint_palette)

    def _update_countdown_display(self):
        """更新倒计时显示"""
        mins, secs = divmod(self.remaining_seconds, 60)

        # 使用统一的倒计时颜色方案
        color = self.get_countdown_color(self.remaining_seconds, self.duration)

        self.countdown_label.setStyleSheet(
            f"QLabel {{ color: {color}; }}"
        )

        # 更新显示文本
        self.countdown_label.setText(f"{mins:02d}:{secs:02d}")

    def _show_complete_feedback(self):
        """显示完成反馈"""
        # 显示✓反馈
        original_text = self.countdown_label.text()
        self.countdown_label.setText("✓ 完成")
        self.countdown_label.setStyleSheet("QLabel { color: #4CAF50; }")

        # 恢复原始文本（被关闭覆盖，所以不需要）

    def skip(self):
        """
        跳过（重写基类方法，强制站立不允许跳过）

        强制站立弹窗不允许跳过，所以此方法不做任何操作
        """
        # 强制站立不允许跳过
        pass

    def keyPressEvent(self, event):
        """
        键盘事件处理

        Args:
            event: 键盘事件
        """
        # 所有键盘事件都禁用（包括 ESC）
        pass
