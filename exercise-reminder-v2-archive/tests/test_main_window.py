# -*- coding: utf-8 -*-
"""
主窗口测试
"""
import pytest
from PySide6.QtCore import Qt


@pytest.fixture
def main_window(qtbot):
    """创建主窗口"""
    from src.ui.main_window import MainWindow
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_main_window_creation(main_window):
    """测试主窗口创建"""
    assert main_window is not None
    assert "灵动休息" in main_window.windowTitle()


def test_window_size(main_window):
    """测试窗口尺寸"""
    assert main_window.width() == 900
    assert main_window.minimumHeight() == 550


def test_has_goal_progress_module(main_window):
    """测试有目标进度模块"""
    assert main_window.goal_progress_widget is not None


def test_has_activity_list_module(main_window):
    """测试有活动列表模块"""
    assert main_window.activity_list_widget is not None


def test_has_quick_actions_module(main_window):
    """测试有快速操作模块"""
    assert main_window.quick_actions_widget is not None


def test_quick_actions_buttons(main_window):
    """测试快速操作按钮"""
    assert main_window.action_library_button is not None
    assert main_window.settings_button is not None
    assert main_window.user_info_button is not None
    assert main_window.basic_settings_button is not None


def test_refresh_interval(main_window):
    """测试自动刷新间隔"""
    assert main_window.refresh_interval == 30000  # 30秒
