# -*- coding: utf-8 -*-
"""
主题选择页面 - 首次启动向导第3页

呼吸感设计 - 柔和有机主义风格
"""
from PySide6.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout,
    QLabel, QRadioButton, QButtonGroup, QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from ..design.tokens import DesignTokens


class ThemePage(QWizardPage):
    """主题选择页面 - 呼吸感设计"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("选择主题")
        self.setSubTitle("选择适合您的界面风格")

        # 选中的主题
        self._selected_theme = "day"

        # 按钮组
        self.button_group = QButtonGroup(self)

        # UI 组件
        self.day_theme_btn = None
        self.night_theme_btn = None
        self.eye_protection_theme_btn = None

        # 应用设计系统样式
        DesignTokens.apply_stylesheet(self, "all")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 说明文字
        desc_label = QLabel(
            "选择您喜欢的界面风格，随时可以在设置中更改。"
        )
        desc_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            color: {DesignTokens.COLOR.TEXT_SECONDARY};
            padding: {DesignTokens.SPACING.SM}px;
        """)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        layout.addSpacing(DesignTokens.SPACING.LG)

        # 主题选项网格
        themes_grid = self._create_themes_grid()
        layout.addWidget(themes_grid)

        layout.addStretch()
        self.setLayout(layout)

    def _create_themes_grid(self) -> QFrame:
        """创建主题选择网格"""
        grid_container = QFrame()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setSpacing(DesignTokens.SPACING.LG)

        # 主题选项
        themes = [
            {
                "id": "day",
                "name": "日间模式",
                "desc": "清新明亮\n适合白天使用",
                "preview_bg": DesignTokens.COLOR.THEME_DAY_BG,
                "preview_text": DesignTokens.COLOR.THEME_DAY_TEXT,
                "preview_accent": DesignTokens.COLOR.PRIMARY_SOLID,
                "btn": None  # 将在循环中赋值
            },
            {
                "id": "night",
                "name": "夜间模式",
                "desc": "深色调\n保护视力",
                "preview_bg": DesignTokens.COLOR.THEME_NIGHT_BG,
                "preview_text": DesignTokens.COLOR.THEME_NIGHT_TEXT,
                "preview_accent": DesignTokens.COLOR.ACCENT,
                "btn": None
            },
            {
                "id": "eye_protection",
                "name": "护眼模式",
                "desc": "温和色调\n长时间使用更舒适",
                "preview_bg": DesignTokens.COLOR.THEME_EYE_BG,
                "preview_text": DesignTokens.COLOR.THEME_EYE_TEXT,
                "preview_accent": DesignTokens.COLOR.SUCCESS,
                "btn": None
            }
        ]

        for i, theme in enumerate(themes):
            theme_card = self._create_theme_card(theme)
            themes[i]["btn"] = theme_card.findChild(QRadioButton, f"radio_{theme['id']}")
            grid_layout.addWidget(theme_card, 0, i)

            # 添加到按钮组
            if themes[i]["btn"]:
                self.button_group.addButton(themes[i]["btn"], i)

        # 连接信号
        self.button_group.buttonClicked.connect(self._on_theme_selected)

        # 均匀分布
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(2, 1)

        # 保存引用
        self.day_theme_btn = themes[0]["btn"]
        self.night_theme_btn = themes[1]["btn"]
        self.eye_protection_theme_btn = themes[2]["btn"]

        # 默认选中第一个
        if self.day_theme_btn:
            self.day_theme_btn.setChecked(True)

        return grid_container

    def _create_theme_card(self, theme: dict) -> QFrame:
        """创建单个主题卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.XL}px;
                border: 2px solid {DesignTokens.COLOR.BORDER_LIGHT};
            }}
            QFrame:hover {{
                border: 2px solid {DesignTokens.COLOR.PRIMARY_SOLID};
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD
        )
        card_layout.setSpacing(DesignTokens.SPACING.MD)

        # 预览框
        preview_frame = self._create_preview_frame(
            theme["preview_bg"],
            theme["preview_text"],
            theme["preview_accent"]
        )
        card_layout.addWidget(preview_frame)

        # 主题名称
        name_label = QLabel(theme["name"])
        name_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_LG}pt;
            font-weight: 600;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(name_label)

        # 主题描述
        desc_label = QLabel(theme["desc"])
        desc_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_SM}pt;
            color: {DesignTokens.COLOR.TEXT_SECONDARY};
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)

        # 单选按钮
        radio_btn = QRadioButton()
        radio_btn.setObjectName(f"radio_{theme['id']}")
        card_layout.addWidget(radio_btn)
        card_layout.setAlignment(radio_btn, Qt.AlignmentFlag.AlignCenter)

        return card

    def _create_preview_frame(self, bg_color: str, text_color: str, accent_color: str) -> QFrame:
        """创建主题预览框"""
        preview = QFrame()
        preview.setFixedHeight(100)
        preview.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: {DesignTokens.RADIUS.MD}px;
                border: 1px solid {DesignTokens.COLOR.BORDER_LIGHT};
            }}
        """)

        preview_layout = QVBoxLayout(preview)
        preview_layout.setContentsMargins(
            DesignTokens.SPACING.SM,
            DesignTokens.SPACING.SM,
            DesignTokens.SPACING.SM,
            DesignTokens.SPACING.SM
        )
        preview_layout.setSpacing(DesignTokens.SPACING.XS)

        # 模拟标题栏
        title_bar = QFrame()
        title_bar.setStyleSheet(f"background-color: {accent_color}; border-radius: 4px;")
        title_bar.setFixedHeight(8)
        preview_layout.addWidget(title_bar)

        preview_layout.addSpacing(4)

        # 模拟内容行
        for _ in range(2):
            line = QFrame()
            line.setStyleSheet(f"background-color: {text_color}; border-radius: 2px;")
            if _ == 0:
                line.setFixedHeight(8)
            else:
                line.setFixedHeight(6)
            preview_layout.addWidget(line)

        preview_layout.addStretch()

        # 模拟按钮
        button = QFrame()
        button.setStyleSheet(f"background-color: {accent_color}; border-radius: 4px;")
        button.setFixedHeight(20)
        button.setFixedWidth(60)
        preview_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        return preview

    def _on_theme_selected(self, button):
        """主题选择变更"""
        if button == self.day_theme_btn:
            self._selected_theme = "day"
        elif button == self.night_theme_btn:
            self._selected_theme = "night"
        elif button == self.eye_protection_theme_btn:
            self._selected_theme = "eye_protection"

    def selectedTheme(self) -> str:
        """返回选中的主题"""
        return self._selected_theme
