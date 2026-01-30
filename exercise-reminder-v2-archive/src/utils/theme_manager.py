# -*- coding: utf-8 -*-
"""
主题管理器

管理应用的主题样式，支持日间、夜间、护眼三种主题
"""
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal
from typing import Dict


class ThemeManager(QObject):
    """主题管理器"""

    # 信号：主题已变更
    theme_changed = Signal(str)

    # 主题定义
    THEMES = {
        "day": {
            "name": "日间模式",
            "colors": {
                "background": "#FFFFFF",
                "foreground": "#333333",
                "primary": "#2196F3",
                "secondary": "#64B5F6",
                "accent": "#FF9800",
                "success": "#4CAF50",
                "warning": "#FF9800",
                "error": "#F44336",
                "border": "#E0E0E0",
                "card": "#F5F5F5",
                "text_disabled": "#999999",
            },
            "dialog": {
                "background": "#FFFFFF",
                "title_color": "#333333",
                "text_color": "#333333",
                "countdown_color": "#2196F3",
                "button_bg": "#2196F3",
                "button_text": "#FFFFFF",
            }
        },
        "night": {
            "name": "夜间模式",
            "colors": {
                "background": "#2B2B2B",
                "foreground": "#FFFFFF",
                "primary": "#64B5F6",
                "secondary": "#2196F3",
                "accent": "#FFB74D",
                "success": "#66BB6A",
                "warning": "#FFB74D",
                "error": "#EF5350",
                "border": "#424242",
                "card": "#383838",
                "text_disabled": "#757575",
            },
            "dialog": {
                "background": "#2B2B2B",
                "title_color": "#FFFFFF",
                "text_color": "#FFFFFF",
                "countdown_color": "#64B5F6",
                "button_bg": "#64B5F6",
                "button_text": "#2B2B2B",
            }
        },
        "eye_protection": {
            "name": "护眼模式",
            "colors": {
                "background": "#F5F5DC",
                "foreground": "#333333",
                "primary": "#66BB6A",
                "secondary": "#81C784",
                "accent": "#FFA726",
                "success": "#66BB6A",
                "warning": "#FFA726",
                "error": "#E57373",
                "border": "#D7CCC8",
                "card": "#EFEBE9",
                "text_disabled": "#8D6E63",
            },
            "dialog": {
                "background": "#F5F5DC",
                "title_color": "#5D4037",
                "text_color": "#333333",
                "countdown_color": "#66BB6A",
                "button_bg": "#66BB6A",
                "button_text": "#FFFFFF",
            }
        }
    }

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        super().__init__()
        self._current_theme = "day"
        self._config = None
        self._initialized = True

    def set_config_manager(self, config_manager):
        """设置配置管理器"""
        self._config = config_manager
        # 加载保存的主题
        saved_theme = self._config.get("theme.current", "day")
        if saved_theme in self.THEMES:
            self._current_theme = saved_theme

    def get_available_themes(self) -> Dict[str, str]:
        """获取可用主题列表"""
        return {key: value["name"] for key, value in self.THEMES.items()}

    def get_current_theme(self) -> str:
        """获取当前主题"""
        return self._current_theme

    def set_theme(self, theme_name: str):
        """设置当前主题"""
        if theme_name not in self.THEMES:
            raise ValueError(f"Unknown theme: {theme_name}")

        self._current_theme = theme_name

        # 保存到配置
        if self._config:
            self._config.set("theme.current", theme_name)
            self._config.save()

        # 发送信号
        self.theme_changed.emit(theme_name)

    def get_color(self, color_name: str) -> str:
        """获取当前主题的颜色值"""
        theme = self.THEMES[self._current_theme]
        return theme["colors"].get(color_name, "#000000")

    def get_dialog_style(self) -> str:
        """获取对话框样式"""
        theme = self.THEMES[self._current_theme]
        dialog = theme["dialog"]

        return f"""
            QDialog {{
                background-color: {dialog['background']};
            }}
            QLabel {{
                color: {dialog['text_color']};
                font-size: 14pt;
            }}
            QPushButton {{
                background-color: {dialog['button_bg']};
                color: {dialog['button_text']};
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme['colors']['secondary']};
            }}
            QPushButton:pressed {{
                background-color: {theme['colors']['primary']};
            }}
            QPushButton:disabled {{
                background-color: {theme['colors']['border']};
                color: {theme['colors']['text_disabled']};
            }}
        """

    def get_countdown_style(self) -> str:
        """获取倒计时样式"""
        theme = self.THEMES[self._current_theme]
        dialog = theme["dialog"]

        return f"""
            QLabel {{
                background-color: {dialog['background']};
                color: {dialog['countdown_color']};
                font-size: 48pt;
                font-weight: bold;
            }}
        """

    def get_settings_style(self) -> str:
        """获取设置对话框样式"""
        theme = self.THEMES[self._current_theme]
        colors = theme["colors"]

        return f"""
            QGroupBox {{
                border: 2px solid {colors['border']};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                font-size: 12pt;
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }}
            QTabWidget::pane {{
                border: 1px solid {colors['border']};
                background-color: {colors['background']};
            }}
            QTabBar::tab {{
                background-color: {colors['card']};
                color: {colors['foreground']};
                padding: 8px 16px;
                border: 1px solid {colors['border']};
                border-bottom: none;
            }}
            QTabBar::tab:selected {{
                background-color: {colors['background']};
                border-bottom: 2px solid {colors['primary']};
            }}
            QCheckBox {{
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QSpinBox {{
                padding: 4px;
                border: 1px solid {colors['border']};
                border-radius: 4px;
                background-color: {colors['background']};
                color: {colors['foreground']};
            }}
            QSpinBox:focus {{
                border: 2px solid {colors['primary']};
            }}
        """

    def apply_to_widget(self, widget, style_type: str = "dialog"):
        """应用主题到指定组件"""
        if style_type == "dialog":
            widget.setStyleSheet(self.get_dialog_style())
        elif style_type == "settings":
            widget.setStyleSheet(self.get_settings_style())
        elif style_type == "countdown":
            widget.setStyleSheet(self.get_countdown_style())


# 全局实例
_theme_manager = None


def get_theme_manager() -> ThemeManager:
    """获取主题管理器单例"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
