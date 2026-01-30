# -*- coding: utf-8 -*-
"""
测试主题选择页面
"""
import pytest


def test_theme_page_selection():
    """Test theme page allows selection"""
    from src.ui.wizards.theme_page import ThemePage
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    page = ThemePage()

    # Has theme options
    assert page.day_theme_btn is not None
    assert page.night_theme_btn is not None
    assert page.eye_protection_theme_btn is not None

    # Can select theme
    page.night_theme_btn.click()
    app.processEvents()
    assert page.selectedTheme() == "night"
