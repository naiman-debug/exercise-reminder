# -*- coding: utf-8 -*-
"""
设计语言指南 - 呼吸感设计系统

美学定位: 柔和有机主义
- 流动、呼吸、韵律、柔和边界
- 参考: Raycast 的轻盈 + Notion 的柔和 + Headspace 的亲和力
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class ColorTokens:
    """颜色系统 - 柔和的自然色系"""

    # 主色调
    PRIMARY_GRADIENT_START = "#A8D5BA"  # 柔和绿
    PRIMARY_GRADIENT_END = "#7CB9E8"    # 柔和蓝
    PRIMARY_SOLID = "#8FB8C9"
    PRIMARY_LIGHT = "#E8F4F0"
    PRIMARY_DARK = "#5A8A9E"

    # 背景色 - 温暖的灰
    BG_PRIMARY = "#FAFAF8"
    BG_SECONDARY = "#F0F0EE"
    BG_CARD = "#FFFFFF"
    BG_ELEVATED = "#FFFFFF"

    # 文本色
    TEXT_PRIMARY = "#2C2C2C"
    TEXT_SECONDARY = "#6B6B6B"
    TEXT_TERTIARY = "#9B9B9B"

    # 功能色
    ACCENT = "#7CB9E8"
    SUCCESS = "#A8D5BA"
    WARNING = "#F5C782"
    ERROR = "#E8A5A5"

    # 边框色
    BORDER_LIGHT = "#E8E8E6"
    BORDER_MEDIUM = "#D8D8D6"

    # 主题色
    THEME_DAY_BG = "#FFFFFF"
    THEME_DAY_TEXT = "#2C2C2C"

    THEME_NIGHT_BG = "#1A1A2E"
    THEME_NIGHT_TEXT = "#E8E8E8"
    THEME_NIGHT_CARD = "#252540"

    THEME_EYE_BG = "#F5F0E6"
    THEME_EYE_TEXT = "#3D3D2E"
    THEME_EYE_CARD = "#FAF6EC"


@dataclass
class TypographyTokens:
    """字体系统"""

    # 字体家族
    FONT_DISPLAY = "Nunito, Quicksand, Nunito Sans, sans-serif"
    FONT_BODY = "Nunito, system-ui, -apple-system, sans-serif"
    FONT_MONO = "SF Mono, JetBrains Mono, Consolas, monospace"

    # 字号 (pt)
    TEXT_XS = 9
    TEXT_SM = 10
    TEXT_BASE = 11
    TEXT_LG = 13
    TEXT_XL = 16
    TEXT_2XL = 20
    TEXT_3XL = 24
    TEXT_4XL = 32


@dataclass
class SpacingTokens:
    """空间系统"""

    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    TWO_XL = 48
    THREE_XL = 64


@dataclass
class RadiusTokens:
    """圆角系统"""

    SM = 6
    MD = 10
    LG = 16
    XL = 24
    FULL = 9999


@dataclass
class ShadowTokens:
    """阴影系统"""

    SM = "0 1px 2px rgba(0,0,0,0.04)"
    MD = "0 4px 12px rgba(0,0,0,0.06)"
    LG = "0 8px 24px rgba(0,0,0,0.08)"
    XL = "0 16px 48px rgba(0,0,0,0.10)"
    GLOW = "0 0 40px rgba(168, 213, 186, 0.3)"


class DesignTokens:
    """设计令牌统一入口"""

    COLOR = ColorTokens()
    TYPOGRAPHY = TypographyTokens()
    SPACING = SpacingTokens()
    RADIUS = RadiusTokens()
    SHADOW = ShadowTokens()

    @staticmethod
    def get_wizard_stylesheet() -> str:
        """获取向导主窗口样式"""
        return f"""
            QWizard {{
                background-color: {DesignTokens.COLOR.BG_PRIMARY};
            }}

            QWizard::QWidget {{
                background-color: {DesignTokens.COLOR.BG_PRIMARY};
            }}

            /* 标题区域 */
            QWizard QWidget {{
                background-color: transparent;
            }}

            /* 页面标题 */
            QWizardPage {{
                background-color: transparent;
            }}

            /* 导航按钮 */
            QWizard QPushButton {{
                background-color: {DesignTokens.COLOR.PRIMARY_SOLID};
                color: white;
                border: none;
                border-radius: {DesignTokens.RADIUS.MD}px;
                padding: 10px 24px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
                font-weight: 600;
                font-family: {DesignTokens.TYPOGRAPHY.FONT_BODY};
            }}

            QWizard QPushButton:hover {{
                background-color: {DesignTokens.COLOR.PRIMARY_DARK};
            }}

            QWizard QPushButton:disabled {{
                background-color: {DesignTokens.COLOR.BG_SECONDARY};
                color: {DesignTokens.COLOR.TEXT_TERTIARY};
            }}

            /* 取消按钮 */
            QWizard QPushButton[buttonType="cancel"] {{
                background-color: transparent;
                color: {DesignTokens.COLOR.TEXT_SECONDARY};
                border: 1px solid {DesignTokens.COLOR.BORDER_MEDIUM};
            }}

            QWizard QPushButton[buttonType="cancel"]:hover {{
                background-color: {DesignTokens.COLOR.BG_SECONDARY};
            }}
        """

    @staticmethod
    def get_card_stylesheet() -> str:
        """获取卡片样式"""
        return f"""
            QFrame[frameShape="4"], /* HLine = 4 */
            QFrame[frameShape="5"]  /* VLine = 5 */
            {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.LG}px;
                border: 1px solid {DesignTokens.COLOR.BORDER_LIGHT};
            }}

            QGroupBox {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.LG}px;
                border: 1px solid {DesignTokens.COLOR.BORDER_LIGHT};
                margin-top: 12px;
                padding-top: 16px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_LG}pt;
                font-weight: 600;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
            }}

            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                background-color: transparent;
            }}
        """

    @staticmethod
    def get_input_stylesheet() -> str:
        """获取输入框样式"""
        return f"""
            QSpinBox, QDoubleSpinBox {{
                background-color: {DesignTokens.COLOR.BG_PRIMARY};
                border: 1px solid {DesignTokens.COLOR.BORDER_MEDIUM};
                border-radius: {DesignTokens.RADIUS.SM}px;
                padding: 8px 12px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
                selection-background-color: {DesignTokens.COLOR.PRIMARY_SOLID};
            }}

            QSpinBox:focus, QDoubleSpinBox:focus {{
                border: 1px solid {DesignTokens.COLOR.PRIMARY_SOLID};
                background-color: {DesignTokens.COLOR.BG_CARD};
            }}

            QSpinBox::up-button, QSpinBox::down-button,
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
                border: none;
                width: 20px;
                background-color: transparent;
            }}

            QSpinBox::up-button:hover, QSpinBox::down-button:hover,
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
                background-color: {DesignTokens.COLOR.BG_SECONDARY};
                border-radius: 4px;
            }}

            QSpinBox::up-arrow, QSpinBox::down-arrow,
            QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
            }}

            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
                border-bottom: 4px solid {DesignTokens.COLOR.TEXT_SECONDARY};
            }}

            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                border-top: 4px solid {DesignTokens.COLOR.TEXT_SECONDARY};
            }}

            QLineEdit {{
                background-color: {DesignTokens.COLOR.BG_PRIMARY};
                border: 1px solid {DesignTokens.COLOR.BORDER_MEDIUM};
                border-radius: {DesignTokens.RADIUS.SM}px;
                padding: 8px 12px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
                selection-background-color: {DesignTokens.COLOR.PRIMARY_SOLID};
            }}

            QLineEdit:focus {{
                border: 1px solid {DesignTokens.COLOR.PRIMARY_SOLID};
                background-color: {DesignTokens.COLOR.BG_CARD};
            }}
        """

    @staticmethod
    def get_label_stylesheet() -> str:
        """获取标签样式"""
        return f"""
            QLabel {{
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
                font-family: {DesignTokens.TYPOGRAPHY.FONT_BODY};
                background-color: transparent;
            }}

            QLabel[heading="true"] {{
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_2XL}pt;
                font-weight: 700;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
            }}

            QLabel[subheading="true"] {{
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
                font-weight: 500;
                color: {DesignTokens.COLOR.TEXT_SECONDARY};
            }}

            QLabel[description="true"] {{
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
                color: {DesignTokens.COLOR.TEXT_SECONDARY};
                line-height: 1.5;
            }}

            QLabel[hint="true"] {{
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_SM}pt;
                color: {DesignTokens.COLOR.TEXT_TERTIARY};
            }}
        """

    @staticmethod
    def get_button_stylesheet() -> str:
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {DesignTokens.COLOR.PRIMARY_SOLID};
                color: white;
                border: none;
                border-radius: {DesignTokens.RADIUS.MD}px;
                padding: 10px 20px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
                font-weight: 600;
                font-family: {DesignTokens.TYPOGRAPHY.FONT_BODY};
            }}

            QPushButton:hover {{
                background-color: {DesignTokens.COLOR.PRIMARY_DARK};
            }}

            QPushButton:pressed {{
                background-color: {DesignTokens.COLOR.PRIMARY_DARK};
                padding: 9px 19px 11px 21px;
            }}

            QPushButton:disabled {{
                background-color: {DesignTokens.COLOR.BG_SECONDARY};
                color: {DesignTokens.COLOR.TEXT_TERTIARY};
            }}

            QPushButton[type="secondary"] {{
                background-color: transparent;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
                border: 1px solid {DesignTokens.COLOR.BORDER_MEDIUM};
            }}

            QPushButton[type="secondary"]:hover {{
                background-color: {DesignTokens.COLOR.BG_SECONDARY};
            }}

            QRadioButton {{
                spacing: 8px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
            }}

            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid {DesignTokens.COLOR.BORDER_MEDIUM};
                background-color: {DesignTokens.COLOR.BG_CARD};
            }}

            QRadioButton::indicator:hover {{
                border: 2px solid {DesignTokens.COLOR.PRIMARY_SOLID};
            }}

            QRadioButton::indicator:checked {{
                background-color: {DesignTokens.COLOR.PRIMARY_SOLID};
                border: 2px solid {DesignTokens.COLOR.PRIMARY_SOLID};
                image: none;
            }}

            QRadioButton::indicator:checked::after {{
                content: "";
                width: 8px;
                height: 8px;
                border-radius: 4px;
                background-color: white;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }}

            QCheckBox {{
                spacing: 8px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
            }}

            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: {DesignTokens.RADIUS.SM}px;
                border: 2px solid {DesignTokens.COLOR.BORDER_MEDIUM};
                background-color: {DesignTokens.COLOR.BG_CARD};
            }}

            QCheckBox::indicator:hover {{
                border: 2px solid {DesignTokens.COLOR.PRIMARY_SOLID};
            }}

            QCheckBox::indicator:checked {{
                background-color: {DesignTokens.COLOR.PRIMARY_SOLID};
                border: 2px solid {DesignTokens.COLOR.PRIMARY_SOLID};
            }}
        """

    @staticmethod
    def apply_stylesheet(widget, stylesheet_type: str = "all"):
        """应用样式到组件"""
        if stylesheet_type == "all":
            stylesheet = (
                DesignTokens.get_wizard_stylesheet() +
                DesignTokens.get_card_stylesheet() +
                DesignTokens.get_input_stylesheet() +
                DesignTokens.get_label_stylesheet() +
                DesignTokens.get_button_stylesheet()
            )
        elif stylesheet_type == "card":
            stylesheet = DesignTokens.get_card_stylesheet()
        elif stylesheet_type == "input":
            stylesheet = DesignTokens.get_input_stylesheet()
        elif stylesheet_type == "label":
            stylesheet = DesignTokens.get_label_stylesheet()
        elif stylesheet_type == "button":
            stylesheet = DesignTokens.get_button_stylesheet()
        else:
            stylesheet = ""

        widget.setStyleSheet(stylesheet)


# 导出设计令牌类
tokens = DesignTokens()
