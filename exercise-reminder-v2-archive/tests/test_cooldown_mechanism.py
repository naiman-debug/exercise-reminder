# -*- coding: utf-8 -*-
"""
提醒冷却机制测试
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import time
from datetime import datetime, timedelta
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from src.core.reminder_engine import ReminderEngine
from src.core.timer_manager import TimerManager
from src.utils.config import ConfigManager
from src.models.database import get_db_manager


@pytest.fixture
def app():
    """创建 QApplication"""
    return QApplication.instance() or QApplication([])


@pytest.fixture
def db(tmp_path):
    """创建临时数据库"""
    from src.models.database import DatabaseManager
    original_path = DatabaseManager.DB_PATH
    DatabaseManager.DB_PATH = tmp_path / "test.db"
    db_manager = get_db_manager()
    db_manager.initialize_database()
    yield db_manager
    DatabaseManager.DB_PATH = original_path


@pytest.fixture
def timer_manager(app):
    """创建定时器管理器"""
    return TimerManager()


@pytest.fixture
def config(db):
    """创建配置管理器"""
    return ConfigManager()


@pytest.fixture
def engine(timer_manager, config):
    """创建提醒引擎"""
    return ReminderEngine(timer_manager, config)


def test_cooldown_tracking_after_trigger(engine, timer_manager):
    """测试触发后正确记录冷却时间"""
    # Arrange: 初始状态不在冷却期
    assert not engine.is_in_cooldown(engine.REMINDER_STAND)

    # Act: 模拟触发站立提醒
    engine._record_trigger(engine.REMINDER_STAND)

    # Assert: 应该在冷却期
    assert engine.is_in_cooldown(engine.REMINDER_STAND)
    assert engine.is_in_cooldown()  # 全局冷却检查


def test_cooldown_expires_after_120_seconds(engine):
    """测试冷却期在120秒后过期"""
    # Arrange: 设置触发时间为121秒前
    engine.last_trigger_time[engine.REMINDER_EXERCISE] = datetime.now() - timedelta(seconds=121)

    # Act & Assert: 不应该在冷却期
    assert not engine.is_in_cooldown(engine.REMINDER_EXERCISE)


def test_cooldown_remaining_decreases(engine):
    """测试冷却期剩余时间递减"""
    # Arrange: 设置触发时间
    engine.last_trigger_time[engine.REMINDER_GAZE] = datetime.now()

    # Act: 等待1秒
    time.sleep(1)

    # Assert: 剩余时间应该约119秒
    remaining = engine.get_cooldown_remaining(engine.REMINDER_GAZE)
    assert 118 <= remaining <= 120  # 允许1秒误差


def test_global_cooldown_checks_all_types(engine):
    """测试全局冷却期检查所有提醒类型"""
    # Arrange: 只触发站立提醒
    engine._record_trigger(engine.REMINDER_STAND)

    # Act & Assert: 全局冷却应该返回 True
    assert engine.is_in_cooldown()
    assert engine.is_in_cooldown(engine.REMINDER_STAND)
    assert not engine.is_in_cooldown(engine.REMINDER_EXERCISE)  # 其他类型单独检查返回 False


def test_get_cooldown_remaining_returns_zero_when_not_in_cooldown(engine):
    """测试不在冷却期时返回0"""
    # Act & Assert: 从未触发过，应该返回0
    assert engine.get_cooldown_remaining(engine.REMINDER_STAND) == 0


def test_multiple_reminders_have_independent_cooldowns(engine):
    """测试不同类型的提醒有独立的冷却期"""
    # Arrange: 触发站立提醒
    engine._record_trigger(engine.REMINDER_STAND)

    # Act & Assert: 站立在冷却期，但运动不在
    assert engine.is_in_cooldown(engine.REMINDER_STAND)
    assert not engine.is_in_cooldown(engine.REMINDER_EXERCISE)

    # 触发运动提醒
    engine._record_trigger(engine.REMINDER_EXERCISE)

    # Assert: 两者都在冷却期
    assert engine.is_in_cooldown(engine.REMINDER_STAND)
    assert engine.is_in_cooldown(engine.REMINDER_EXERCISE)


def test_cooldown_constant_value(engine):
    """测试冷却期常量值为120秒"""
    # Assert: 验证常量定义
    assert engine.COOLDOWN_SECONDS == 120


def test_trigger_records_current_time(engine):
    """测试触发时间记录为当前时间"""
    # Arrange: 获取当前时间
    before_trigger = datetime.now()

    # Act: 记录触发
    engine._record_trigger(engine.REMINDER_STAND)

    # Assert: 记录的时间应该在当前时间附近
    recorded_time = engine.last_trigger_time[engine.REMINDER_STAND]
    time_diff = (datetime.now() - recorded_time).total_seconds()
    assert time_diff < 1  # 应该小于1秒


def test_cooldown_with_timer_integration(engine, timer_manager, qtbot):
    """测试冷却期与定时器集成"""
    # 计数器
    trigger_count = {"count": 0}

    # 创建信号槽来捕获触发
    def on_stand_trigger(duration):
        trigger_count["count"] += 1

    engine.stand_reminder.connect(on_stand_trigger)

    # 启动提醒
    engine.schedule_stand_reminder()

    # 手动触发一次（模拟）
    engine._record_trigger(engine.REMINDER_STAND)

    # 验证在冷却期
    assert engine.is_in_cooldown(engine.REMINDER_STAND)
