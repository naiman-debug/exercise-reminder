# -*- coding: utf-8 -*-
"""
完成页面 - 首次启动向导最后一页

呼吸感设计 - 柔和有机主义风格
"""
from PySide6.QtWidgets import QWizardPage, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from ..design.tokens import DesignTokens


class FinishPage(QWizardPage):
    """向导完成页面 - 呼吸感设计"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("准备就绪")
        self.setSubTitle("开始您的健康之旅")

        # 应用设计系统样式
        DesignTokens.apply_stylesheet(self, "label")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 主内容卡片
        content_card = self._create_content_card()
        layout.addWidget(content_card)
        layout.addStretch()

        self.setLayout(layout)

    def _create_content_card(self) -> QFrame:
        """创建主内容卡片"""
        card = QFrame()
        card.setObjectName("finishCard")
        card.setStyleSheet(f"""
            QFrame#finishCard {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {DesignTokens.COLOR.PRIMARY_GRADIENT_START},
                    stop:1 {DesignTokens.COLOR.PRIMARY_GRADIENT_END}
                );
                border-radius: {DesignTokens.RADIUS.XL}px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(
            DesignTokens.SPACING.XL * 2,
            DesignTokens.SPACING.XL * 2,
            DesignTokens.SPACING.XL * 2,
            DesignTokens.SPACING.XL * 2
        )
        card_layout.setSpacing(DesignTokens.SPACING.LG)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 成功图标
        icon_label = QLabel("完成")
        icon_label.setStyleSheet(f"""
            font-size: 64pt;
            color: white;
            background-color: transparent;
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)

        # 主标题
        title = QLabel("设置完成")
        title.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_3XL}pt;
            font-weight: 800;
            color: white;
            background-color: transparent;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        # 副标题
        subtitle = QLabel("所有设置已完成")
        subtitle.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            color: rgba(255, 255, 255, 0.9);
            background-color: transparent;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(DesignTokens.SPACING.MD)

        # 说明文字
        desc = QLabel(
            "灵动休息健康助手将根据您的设置，\\n"
            "定时提醒您站立、运动和远眺。\\n\\n"
            "点击完成即可开始使用。"
        )
        desc.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            color: rgba(255, 255, 255, 0.85);
            background-color: transparent;
            line-height: 1.6;
        """)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        card_layout.addWidget(desc)

        card_layout.addSpacing(DesignTokens.SPACING.LG)

        # 提示卡片
        hint_card = self._create_hint_card()
        card_layout.addWidget(hint_card)

        return card

    def _create_hint_card(self) -> QFrame:
        """创建提示卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: {DesignTokens.RADIUS.MD}px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD
        )
        card_layout.setSpacing(DesignTokens.SPACING.SM)

        # 提示标题
        hint_title = QLabel("小贴士")
        hint_title.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_SM}pt;
            font-weight: 600;
            color: white;
            background-color: transparent;
        """)
        hint_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(hint_title)

        # 提示内容
        hint_text = QLabel(
            "• 您可以随时在设置中修改这些选项\n"
            "• 建议先从较低的提醒频率开始\n"
            "• 记得查看数据统计了解您的进度"
        )
        hint_text.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_XS}pt;
            color: rgba(255, 255, 255, 0.9);
            background-color: transparent;
            line-height: 1.5;
        """)
        hint_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_text.setWordWrap(True)
        card_layout.addWidget(hint_text)

        return card
