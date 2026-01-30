# -*- coding: utf-8 -*-
"""
测试个人信息页面
"""
import pytest


def test_profile_page_validation():
    """Test profile page validates input"""
    from src.ui.wizards.profile_page import ProfilePage
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    page = ProfilePage()

    # Test valid input
    page.height_input.setValue(175)
    page.weight_input.setValue(70)
    page.age_input.setValue(30)

    app.processEvents()
    assert page.isComplete() == True

    # Test that QSpinBox enforces range limits
    # When we set 50, it gets clamped to 100 (minimum)
    page.height_input.setValue(50)
    app.processEvents()
    assert page.height_input.value() == 100  # Clamped to min
    assert page.isComplete() == True  # Still complete due to clamping
