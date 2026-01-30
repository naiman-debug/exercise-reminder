# -*- coding: utf-8 -*-
"""
配置迁移测试模块
"""
import pytest
import os
import tempfile
import json
from src.utils.config import ConfigManager


def test_old_config_migrates_to_new_structure():
    """测试旧配置能够正确迁移到新结构"""
    # 使用临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        # 手动创建旧配置文件（绕过 ConfigManager 的自动迁移）
        old_config = {
            "reminder": {
                "stand": {
                    "enabled": True,
                    "interval_min": 30,
                    "interval_max": 60,
                    "duration": 90
                },
                "exercise": {
                    "enabled": True,
                    "interval_min": 45,
                    "interval_max": 75,
                    "duration": 120
                },
                "gaze": {
                    "enabled": True,
                    "interval_min": 60,
                    "interval_max": 90,
                    "duration": 60
                }
            }
        }

        # 直接写入旧配置到文件
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(old_config, f)

        # 创建 ConfigManager，会触发自动迁移
        config = ConfigManager(temp_path)

        # 验证迁移结果
        assert config.get("reminder.global_offset_minutes") == 15
        assert config.get("reminder.stand.interval_avg") == 45
        assert config.get("reminder.exercise.interval_avg") == 60
        assert config.get("reminder.gaze.interval_avg") == 75

        # 验证旧键已删除
        assert config.get("reminder.stand.interval_min") is None
        assert config.get("reminder.stand.interval_max") is None
        assert config.get("reminder.exercise.interval_min") is None
        assert config.get("reminder.exercise.interval_max") is None
        assert config.get("reminder.gaze.interval_min") is None
        assert config.get("reminder.gaze.interval_max") is None
    finally:
        os.unlink(temp_path)


def test_new_config_does_not_need_migration():
    """测试新配置不需要迁移"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        config = ConfigManager(temp_path)
        # 新配置，没有旧键
        result = config.migrate_config()

        assert result == False
    finally:
        os.unlink(temp_path)


def test_get_interval_range_with_new_config():
    """测试新配置下 get_interval_range 方法"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        config = ConfigManager(temp_path)
        # 设置新配置
        config.set("reminder.global_offset_minutes", 15)
        config.set("reminder.stand.interval_avg", 45)
        config.set("reminder.exercise.interval_avg", 60)

        # 获取范围
        stand_min, stand_max = config.get_interval_range("stand")
        exercise_min, exercise_max = config.get_interval_range("exercise")

        # 验证计算结果：avg ± offset
        assert stand_min == 30  # 45 - 15
        assert stand_max == 60  # 45 + 15
        assert exercise_min == 45  # 60 - 15
        assert exercise_max == 75  # 60 + 15
    finally:
        os.unlink(temp_path)


def test_default_config_has_new_structure():
    """测试默认配置使用新结构"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        config = ConfigManager(temp_path)

        # 验证新键存在
        assert config.get("reminder.global_offset_minutes") == 15
        assert config.get("reminder.stand.interval_avg") == 45
        assert config.get("reminder.exercise.interval_avg") == 60
        assert config.get("reminder.gaze.interval_avg") == 75

        # 验证旧键不存在
        assert config.get("reminder.stand.interval_min") is None
        assert config.get("reminder.stand.interval_max") is None
    finally:
        os.unlink(temp_path)
