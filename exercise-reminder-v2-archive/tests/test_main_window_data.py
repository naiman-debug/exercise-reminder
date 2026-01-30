# -*- coding: utf-8 -*-
"""
主窗口数据刷新功能测试
"""
import pytest
from datetime import date, datetime
from unittest.mock import Mock, patch


@pytest.fixture
def main_window(qtbot):
    """创建主窗口"""
    from src.ui.main_window import MainWindow
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_refresh_data_calls_repositories(main_window):
    """测试 refresh_data 调用 repositories"""
    with patch('src.models.repositories.ActivityRepository') as mock_activity_repo, \
         patch('src.models.repositories.SettingRepository') as mock_setting_repo:

        # 配置 mock 返回值
        mock_activity_repo.get_calories_by_date.return_value = 150.0
        mock_setting_repo.get_int.return_value = 300
        mock_activity_repo.get_activities_by_date.return_value = []

        # 调用刷新
        main_window.refresh_data()

        # 验证调用
        mock_activity_repo.get_calories_by_date.assert_called_once()
        mock_setting_repo.get_int.assert_called_once_with("daily_calorie_goal", 300)
        mock_activity_repo.get_activities_by_date.assert_called_once()


def test_update_goal_progress(main_window):
    """测试更新目标进度"""
    # 测试 50% 进度
    main_window._update_goal_progress(150, 300)

    assert "150/300" in main_window.progress_label.text()
    assert "(50%)" in main_window.progress_label.text()


def test_update_goal_progress_clamps_percent(main_window):
    """测试进度百分比被限制在 0-100"""
    # 测试超过 100%
    main_window._update_goal_progress(400, 300)
    assert "(100%)" in main_window.progress_label.text()

    # 测试负数
    main_window._update_goal_progress(-10, 300)
    assert "(0%)" in main_window.progress_label.text()


def test_update_activity_list_empty(main_window):
    """测试空活动列表显示空状态"""
    main_window._update_activity_list([])

    # 应该显示空状态标签
    layout = main_window.activity_list_container.layout()
    assert layout.itemAt(0).widget() == main_window.empty_label


def test_update_activity_list_with_activities(main_window):
    """测试有活动时正确显示"""
    # 创建模拟活动
    mock_activity = Mock()
    mock_activity.activity_type = "stand"
    mock_activity.duration_seconds = 120
    mock_activity.timestamp = datetime.now()

    main_window._update_activity_list([mock_activity])

    # 应该有活动项
    layout = main_window.activity_list_container.layout()
    # 第一项不应该是空标签
    assert layout.itemAt(0).widget() != main_window.empty_label


def test_format_activity_description_stand(main_window):
    """测试站立活动格式化"""
    mock_activity = Mock()
    mock_activity.activity_type = "stand"
    mock_activity.duration_seconds = 120

    icon, desc = main_window._format_activity_description(mock_activity)

    assert icon == "🧍"
    assert "站立" in desc
    assert "2" in desc


def test_format_activity_description_exercise(main_window):
    """测试运动活动格式化"""
    mock_activity = Mock()
    mock_activity.activity_type = "exercise"
    mock_activity.duration_seconds = 120

    icon, desc = main_window._format_activity_description(mock_activity)

    assert icon == "🏃"
    assert "运动" in desc
    assert "2" in desc


def test_format_activity_description_gaze(main_window):
    """测试远眺活动格式化"""
    mock_activity = Mock()
    mock_activity.activity_type = "gaze"
    mock_activity.duration_seconds = 60

    icon, desc = main_window._format_activity_description(mock_activity)

    assert icon == "👁️"
    assert "远眺" in desc
    assert "1" in desc


def test_format_activity_description_unknown(main_window):
    """测试未知活动类型格式化"""
    mock_activity = Mock()
    mock_activity.activity_type = "unknown"
    mock_activity.duration_seconds = 30

    icon, desc = main_window._format_activity_description(mock_activity)

    assert icon == "📋"
    assert "unknown" in desc
    assert "30" in desc


def test_show_settings_method(main_window):
    """测试显示设置方法"""
    with patch('src.ui.settings.settings_dialog.SettingsDialog') as mock_dialog:
        mock_instance = Mock()
        mock_dialog.return_value = mock_instance
        mock_instance.exec.return_value = 1

        main_window._show_settings()

        # 验证对话框被创建和执行
        mock_dialog.assert_called_once()
        mock_instance.exec.assert_called_once()


def test_quick_action_buttons_exist(main_window):
    """测试快速操作按钮存在"""
    assert main_window.action_library_button is not None
    assert main_window.settings_button is not None
    assert main_window.user_info_button is not None
    assert main_window.basic_settings_button is not None
