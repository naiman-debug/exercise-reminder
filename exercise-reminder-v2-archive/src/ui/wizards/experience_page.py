# -*- coding: utf-8 -*-
"""
体验倒计时页面 - 首次启动向导第3页

包含 10 秒倒计时功能，替代原有的主题选择页
呼吸感设计 - 柔和有机主义风格
"""
from PySide6.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QWidget
)
from PySide6.QtCore import Qt, Signal, QTimer
from ..design.tokens import DesignTokens
from src.utils.logger import get_logger

# 颜色常量（根据设计规范）
COLOR_SUCCESS_GREEN = "#4CAF50"
COLOR_COUNTDOWN_ORANGE = "#FF9800"
COLOR_HINT_BG = "#E8F5E9"
COLOR_SKIP_BG = "#F5F5F5"


class ExperiencePage(QWizardPage):
    """体验倒计时页面 - 呼吸感设计"""

    # 信号定义
    start_experience = Signal()  # 立即体验/倒计时结束

    def __init__(self, parent=None):
        super().__init__(parent)

        # 初始化日志
        self.logger = get_logger(__name__)
        self.logger.info("初始化体验倒计时页面")

        # 设置页面标题
        self.setTitle("准备就绪")
        self.setSubTitle("开始您的健康之旅")

        # 倒计时相关
        self.countdown_time = 10  # 倒计时 10 秒
        self.countdown_timer = QTimer()
        self.countdown_timer.setInterval(1000)  # 1 秒间隔
        self.countdown_timer.timeout.connect(self._on_countdown_tick)

        # UI 组件
        self.success_icon = None
        self.main_title = None
        self.countdown_label = None
        self.hint_card = None
        self.hint_label = None
        self.start_button = None

        # 应用设计系统样式
        DesignTokens.apply_stylesheet(self, "label")

        # 构建 UI
        self._setup_ui()

    def showEvent(self, event):
        """页面显示时启动倒计时"""
        super().showEvent(event)
        # 页面显示时才开始倒计时
        if not self.countdown_timer.isActive():
            self.logger.info(f"页面显示，启动倒计时: {self.countdown_time} 秒")
            self.countdown_timer.start()

    def _setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 主容器
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(
            DesignTokens.SPACING.XL,
            DesignTokens.SPACING.LG,
            DesignTokens.SPACING.XL,
            DesignTokens.SPACING.LG
        )
        main_layout.setSpacing(DesignTokens.SPACING.LG)

        # 成功图标
        self.success_icon = QLabel("✅")
        self.success_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_icon.setStyleSheet(f"""
            QLabel {{
                font-size: 64pt;
                background-color: transparent;
            }}
        """)
        main_layout.addWidget(self.success_icon)

        # 主标题
        self.main_title = QLabel("设置完成")
        self.main_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_title.setStyleSheet(f"""
            QLabel {{
                font-size: 32pt;
                font-weight: bold;
                color: {COLOR_SUCCESS_GREEN};
                background-color: transparent;
            }}
        """)
        main_layout.addWidget(self.main_title)

        # 倒计时数字
        self.countdown_label = QLabel(f"应用将在 {self.countdown_time} 秒后开始运行")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet(f"""
            QLabel {{
                font-size: 48pt;
                font-weight: bold;
                color: {COLOR_COUNTDOWN_ORANGE};
                background-color: transparent;
            }}
        """)
        main_layout.addWidget(self.countdown_label)

        main_layout.addSpacing(DesignTokens.SPACING.MD)

        # 提示卡片
        self.hint_card = self._create_hint_card()
        main_layout.addWidget(self.hint_card)

        main_layout.addStretch()

        # 按钮区域 - 居中显示
        button_layout = QHBoxLayout()
        button_layout.setSpacing(DesignTokens.SPACING.MD)
        button_layout.addStretch()

        # 立即体验按钮
        self.start_button = QPushButton("立即体验")
        self.start_button.setFixedSize(120, 40)
        self.start_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SUCCESS_GREEN};
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 14pt;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #45A049;
            }}
            QPushButton:pressed {{
                background-color: #3D8B40;
            }}
        """)
        self.start_button.clicked.connect(self._on_start_clicked)
        button_layout.addWidget(self.start_button)

        button_layout.addStretch()

        button_layout.setContentsMargins(
            DesignTokens.SPACING.XL,
            0,
            DesignTokens.SPACING.XL,
            0
        )

        main_layout.addLayout(button_layout)

        layout.addWidget(main_container)
        self.setLayout(layout)

    def _create_hint_card(self) -> QFrame:
        """创建提示卡片"""
        card = QFrame()
        card.setObjectName("hintCard")
        card.setStyleSheet(f"""
            QFrame#hintCard {{
                background-color: {COLOR_HINT_BG};
                border-radius: 12px;
                border: 1px solid {DesignTokens.COLOR.BORDER_LIGHT};
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(
            DesignTokens.SPACING.LG,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.LG,
            DesignTokens.SPACING.MD
        )

        self.hint_label = QLabel(
            "• 所有提醒都是倒计时自动结束\n"
            "• 站起提醒: 请站立等待倒计时\n"
            "• 微运动: 跟着动作做，等待倒计时\n"
            "• 远眺: 放松眼睛，眺望远方\n"
            "• 应用在系统托盘运行，随时可调整设置"
        )
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hint_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13pt;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
                line-height: 1.8;
                background-color: transparent;
            }}
        """)
        self.hint_label.setWordWrap(True)
        card_layout.addWidget(self.hint_label)

        return card

    def _on_countdown_tick(self):
        """倒计时每秒触发"""
        self.countdown_time -= 1
        self.logger.debug(f"倒计时: {self.countdown_time} 秒")

        if self.countdown_time > 0:
            # 更新倒计时显示
            self.countdown_label.setText(f"应用将在 {self.countdown_time} 秒后开始运行")
        else:
            # 倒计时结束
            self.countdown_timer.stop()
            self.logger.info("倒计时结束，开始体验")
            self.countdown_label.setText("开始体验！")
            self.start_experience.emit()

    def _on_start_clicked(self):
        """立即体验按钮点击"""
        self.logger.info("用户点击立即体验")
        self.countdown_timer.stop()
        self.start_experience.emit()

    def cleanupPage(self):
        """页面清理"""
        self.logger.debug("清理体验倒计时页面")
        if self.countdown_timer.isActive():
            self.countdown_timer.stop()
