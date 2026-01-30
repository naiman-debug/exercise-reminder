# -*- coding: utf-8 -*-
"""
数据模型定义

使用 Peewee ORM 定义所有数据模型
"""
from peewee import *
from datetime import datetime
from .database import get_database


class BaseModel(Model):
    """基础模型类"""

    class Meta:
        database = get_database()


class Setting(BaseModel):
    """
    用户设置表

    存储键值对形式的用户配置
    """
    key = CharField(unique=True, index=True)
    value = TextField()
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "settings"


class Exercise(BaseModel):
    """
    动作库表

    存储运动动作的基本信息
    """
    name = CharField()
    duration_seconds = IntegerField()
    met_value = FloatField()
    category = CharField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "exercises"
        indexes = (
            (("category", "name"), True),
        )


class ExercisePlan(BaseModel):
    """
    运动方案表

    存储用户自定义的运动方案
    """
    name = CharField()
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "exercise_plans"


class PlanExercise(BaseModel):
    """
    方案-动作关联表

    定义运动方案包含哪些动作及其顺序
    """
    plan = ForeignKeyField(
        ExercisePlan,
        backref="plan_exercises",
        on_delete="CASCADE"
    )
    exercise = ForeignKeyField(
        Exercise,
        backref="plan_exercises",
        on_delete="CASCADE"
    )
    order_index = IntegerField()

    class Meta:
        table_name = "plan_exercises"
        indexes = (
            (("plan", "order_index"), True),
        )


class ActivityLog(BaseModel):
    """
    活动记录表

    记录用户的站立、运动、远眺活动
    """
    activity_type = CharField()  # 'stand', 'exercise', 'gaze'
    duration_seconds = IntegerField()
    calories_burned = FloatField(default=0.0)
    completed = BooleanField(default=True)
    skipped = BooleanField(default=False)
    timestamp = DateTimeField(default=datetime.now, index=True)

    class Meta:
        table_name = "activity_logs"
        indexes = (
            (("timestamp",), False),
            (("activity_type", "timestamp"), False),
        )

    @classmethod
    def log_stand(cls, duration_seconds: int) -> "ActivityLog":
        """记录站立活动"""
        return cls.create(
            activity_type="stand",
            duration_seconds=duration_seconds,
            calories_burned=0
        )

    @classmethod
    def log_exercise(cls, duration_seconds: int, calories: float, completed: bool = True) -> "ActivityLog":
        """记录运动活动"""
        return cls.create(
            activity_type="exercise",
            duration_seconds=duration_seconds,
            calories_burned=calories,
            completed=completed,
            skipped=not completed
        )

    @classmethod
    def log_gaze(cls, duration_seconds: int = 60) -> "ActivityLog":
        """记录远眺活动"""
        return cls.create(
            activity_type="gaze",
            duration_seconds=duration_seconds,
            calories_burned=0
        )

    @classmethod
    def get_today_stats(cls) -> dict:
        """
        获取今日统计

        Returns:
            dict: {stand_count, stand_duration, exercise_count, exercise_duration, exercise_calories, gaze_count, gaze_duration}
        """
        from datetime import date
        today = date.today()

        logs = cls.select().where(cls.timestamp >= today)

        stats = {
            "stand_count": 0,
            "stand_duration": 0,
            "exercise_count": 0,
            "exercise_duration": 0,
            "exercise_calories": 0,
            "exercise_skipped": 0,
            "gaze_count": 0,
            "gaze_duration": 0,
        }

        for log in logs:
            if log.activity_type == "stand" and log.completed:
                stats["stand_count"] += 1
                stats["stand_duration"] += log.duration_seconds
            elif log.activity_type == "exercise":
                if log.completed:
                    stats["exercise_count"] += 1
                    stats["exercise_duration"] += log.duration_seconds
                    stats["exercise_calories"] += log.calories_burned
                elif log.skipped:
                    stats["exercise_skipped"] += 1
            elif log.activity_type == "gaze" and log.completed:
                stats["gaze_count"] += 1
                stats["gaze_duration"] += log.duration_seconds

        return stats

    @classmethod
    def get_recent_activity(cls, limit: int = 10) -> list:
        """
        获取最近活动记录

        Args:
            limit: 返回记录数量

        Returns:
            list: ActivityLog 列表
        """
        return list(
            cls.select()
            .order_by(cls.timestamp.desc())
            .limit(limit)
        )


class UserProfile(BaseModel):
    """
    用户档案表

    存储用户的个人信息
    """
    weight_kg = FloatField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "user_profile"

    @classmethod
    def get_current_weight(cls) -> float:
        """获取当前体重"""
        profile = cls.select().order_by(cls.updated_at.desc()).first()
        if profile:
            return profile.weight_kg
        else:
            # 默认体重
            return 70.0

    @classmethod
    def update_weight(cls, weight_kg: float) -> "UserProfile":
        """更新体重"""
        return cls.create(weight_kg=weight_kg)
