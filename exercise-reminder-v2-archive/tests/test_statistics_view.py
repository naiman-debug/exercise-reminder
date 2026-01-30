# -*- coding: utf-8 -*-
"""
统计页面测试
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from datetime import datetime
from PySide6.QtWidgets import QApplication
from src.ui.statistics.stats_view import StatisticsView
from src.models.database import get_db_manager
from src.models.models import ActivityLog


@pytest.fixture
def app():
    """创建 QApplication"""
    return QApplication.instance() or QApplication([])


@pytest.fixture
def db(tmp_path):
    """创建临时数据库"""
    # 保存原始数据库路径
    from src.models.database import DatabaseManager
    original_path = DatabaseManager.DB_PATH

    # 设置临时数据库路径
    DatabaseManager.DB_PATH = tmp_path / "test.db"

    # 初始化测试数据库
    db_manager = get_db_manager()
    db_manager.initialize_database()

    yield db_manager

    # 恢复原始路径
    DatabaseManager.DB_PATH = original_path


@pytest.fixture
def view(app, db):
    """创建统计视图"""
    return StatisticsView()


def test_today_stats_shows_calories(view, db):
    """测试今日统计显示热量消耗"""
    # Arrange: 清除今日数据并创建测试数据
    ActivityLog.delete().where(ActivityLog.timestamp >= datetime.now().date()).execute()
    ActivityLog.create(
        activity_type="exercise",
        duration_seconds=60,
        calories_burned=5.0,
        completed=True,
        timestamp=datetime.now()
    )

    # Act: 刷新统计
    view.refresh_data()

    # Assert: 验证显示热量
    assert view.calories_label.text() == "5.0 kcal"


def test_today_stats_shows_count(view, db):
    """测试今日统计显示完成次数"""
    # Arrange: 清除今日数据并创建3个活动
    ActivityLog.delete().where(ActivityLog.timestamp >= datetime.now().date()).execute()
    for _ in range(3):
        ActivityLog.create(
            activity_type="stand",
            duration_seconds=90,
            calories_burned=0,
            completed=True,
            timestamp=datetime.now()
        )

    # Act: 刷新统计
    view.refresh_data()

    # Assert: 验证显示次数
    assert "3" in view.count_label.text()


def test_today_stats_shows_duration(view, db):
    """测试今日统计显示总时长"""
    # Arrange: 清除今日数据并创建不同时长的活动
    ActivityLog.delete().where(ActivityLog.timestamp >= datetime.now().date()).execute()
    ActivityLog.create(
        activity_type="stand",
        duration_seconds=90,
        calories_burned=0,
        completed=True,
        timestamp=datetime.now()
    )
    ActivityLog.create(
        activity_type="exercise",
        duration_seconds=45,
        calories_burned=3.0,
        completed=True,
        timestamp=datetime.now()
    )

    # Act: 刷新统计
    view.refresh_data()

    # Assert: 验证显示时长 (135秒 = 2.25分钟)
    assert "2" in view.duration_label.text()  # 显示分钟数


def test_weekly_chart_displays_7_days(view, db):
    """测试本周图表显示7天数据"""
    # Arrange: 清除数据并创建过去7天的数据
    ActivityLog.delete().execute()
    for i in range(7):
        target_date = datetime.now().date()
        ActivityLog.create(
            activity_type="exercise",
            duration_seconds=60,
            calories_burned=float(100 + i * 10),
            completed=True,
            timestamp=datetime.combine(target_date, datetime.min.time())
        )

    # Act: 刷新图表
    view.refresh_data()

    # Assert: 验证图表有7个数据点
    assert view.weekly_chart is not None
    assert len(view.weekly_chart.get_data_points()) == 7


def test_weekly_chart_shows_correct_calories(view, db):
    """测试本周图表显示正确热量"""
    # Arrange: 清除数据并创建特定数据
    ActivityLog.delete().execute()
    ActivityLog.create(
        activity_type="exercise",
        duration_seconds=60,
        calories_burned=185.0,
        completed=True,
        timestamp=datetime.now()
    )

    # Act: 刷新图表
    view.refresh_data()

    # Assert: 验证热量值
    data_points = view.weekly_chart.get_data_points()
    # 数据会被聚合到今天，检查是否有185.0的值
    has_185 = any(abs(point["calories"] - 185.0) < 0.1 for point in data_points)
    assert has_185, f"Expected 185.0 in data points, got: {data_points}"


def test_statistics_in_settings_dialog(app, db):
    """测试统计页面已集成到设置对话框"""
    from src.ui.settings.settings_dialog import SettingsDialog

    dialog = SettingsDialog()

    # Assert: 验证统计标签页存在
    assert dialog.tabs.count() >= 5  # 至少有5个标签页

    # 验证统计标签页可以访问
    stats_tab = dialog.tabs.widget(4)  # 统计是第5个标签
    assert isinstance(stats_tab, StatisticsView)
