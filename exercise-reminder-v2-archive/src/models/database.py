# -*- coding: utf-8 -*-
"""
数据库管理模块

负责 SQLite 数据库的连接、初始化和基础操作
"""
import os
from pathlib import Path
from peewee import *
from datetime import datetime


class DatabaseManager:
    """数据库管理器"""

    # 数据库文件路径
    DB_PATH = Path("data/app.db")

    def __init__(self):
        """初始化数据库管理器"""
        self.database = None
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """确保数据目录存在"""
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    def get_database(self) -> SqliteDatabase:
        """
        获取数据库连接

        Returns:
            SqliteDatabase: 数据库连接对象
        """
        if self.database is None:
            self.database = SqliteDatabase(
                self.DB_PATH,
                pragmas={
                    'journal_mode': 'wal',
                    'cache_size': -1024 * 64,  # 64MB
                    'foreign_keys': 1
                }
            )
        return self.database

    def initialize_database(self):
        """初始化数据库表结构"""
        from .models import (
            Setting, Exercise, ExercisePlan, PlanExercise,
            ActivityLog, UserProfile
        )

        db = self.get_database()
        db.create_tables([
            Setting, Exercise, ExercisePlan, PlanExercise,
            ActivityLog, UserProfile
        ], safe=True)

        # 初始化默认数据
        self._seed_default_data()

    def _seed_default_data(self):
        """播种默认数据"""
        from .models import Exercise, Setting

        # 检查是否已有数据
        if Exercise.select().count() > 0:
            return

        # 添加默认动作（使用统一的 MET 值）
        default_exercises = [
            {"name": "开合跳", "duration_seconds": 30, "met_value": 6.0, "category": "中等强度"},
            {"name": "自重深蹲", "duration_seconds": 45, "met_value": 6.0, "category": "中等强度"},
            {"name": "高抬腿", "duration_seconds": 30, "met_value": 6.0, "category": "中等强度"},
            {"name": "原地踏步", "duration_seconds": 60, "met_value": 6.0, "category": "中等强度"},
            {"name": "靠墙静蹲", "duration_seconds": 45, "met_value": 6.0, "category": "中等强度"},
            {"name": "手臂画圈", "duration_seconds": 30, "met_value": 6.0, "category": "中等强度"},
            {"name": "简化波比跳", "duration_seconds": 30, "met_value": 8.0, "category": "高强度"},
            {"name": "登山跑", "duration_seconds": 30, "met_value": 8.0, "category": "高强度"},
            {"name": "哑铃推举", "duration_seconds": 45, "met_value": 6.0, "category": "中等强度"},
            {"name": "弹力绳划船", "duration_seconds": 45, "met_value": 6.0, "category": "中等强度"},
        ]

        for ex in default_exercises:
            Exercise.create(**ex)

        # 添加默认设置
        default_settings = {
            # 强制站立提醒
            "stand.enabled": "true",
            "stand.interval_min": "30",
            "stand.interval_max": "60",
            "stand.duration": "90",

            # 微运动提醒
            "exercise.enabled": "true",
            "exercise.interval_min": "45",
            "exercise.interval_max": "75",
            "exercise.exercises_per_session_min": "3",
            "exercise.exercises_per_session_max": "5",

            # 强制远眺提醒
            "gaze.enabled": "true",
            "gaze.interval_min": "60",
            "gaze.interval_max": "90",
            "gaze.duration": "60",

            # 音频设置
            "audio.enabled": "true",
            "audio.volume": "0.7",
            "audio.tts_enabled": "false",
            "audio.tts_api": "",

            # 用户设置
            "user.weight_kg": "70",
        }

        for key, value in default_settings.items():
            Setting.get_or_create(
                key=key,
                defaults={"value": value}
            )

    def close(self):
        """关闭数据库连接"""
        if self.database:
            self.database.close()
            self.database = None


# 全局数据库管理器实例
_db_manager = None


def get_db_manager() -> DatabaseManager:
    """
    获取全局数据库管理器实例

    Returns:
        DatabaseManager: 数据库管理器单例
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def get_database() -> SqliteDatabase:
    """
    获取数据库连接

    Returns:
        SqliteDatabase: 数据库连接对象
    """
    return get_db_manager().get_database()
