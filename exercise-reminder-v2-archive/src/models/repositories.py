# -*- coding: utf-8 -*-
"""
数据仓储层

提供对数据模型的高级访问接口
"""
from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from .models import (
    Setting, Exercise, ExercisePlan, PlanExercise,
    ActivityLog, UserProfile
)


class SettingRepository:
    """设置仓储"""

    @staticmethod
    def get(key: str, default: str = "") -> str:
        """
        获取设置值

        Args:
            key: 设置键
            default: 默认值

        Returns:
            str: 设置值
        """
        try:
            setting = Setting.get(Setting.key == key)
            return setting.value
        except Setting.DoesNotExist:
            return default

    @staticmethod
    def set(key: str, value: str) -> None:
        """
        设置值

        Args:
            key: 设置键
            value: 设置值
        """
        Setting.insert(
            key=key,
            value=value,
            updated_at=datetime.now()
        ).on_conflict(
            conflict_target=[Setting.key],
            update={"value": value, "updated_at": datetime.now()}
        ).execute()

    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        """获取整数设置值"""
        value = SettingRepository.get(key, str(default))
        try:
            return int(value)
        except ValueError:
            return default

    @staticmethod
    def get_float(key: str, default: float = 0.0) -> float:
        """获取浮点数设置值"""
        value = SettingRepository.get(key, str(default))
        try:
            return float(value)
        except ValueError:
            return default

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """获取布尔设置值"""
        value = SettingRepository.get(key, str(default)).lower()
        return value in ("true", "1", "yes", "on")

    @staticmethod
    def get_all() -> Dict[str, str]:
        """获取所有设置"""
        settings = {}
        for setting in Setting.select():
            settings[setting.key] = setting.value
        return settings


class ExerciseRepository:
    """动作仓储"""

    @staticmethod
    def get_all() -> List[Exercise]:
        """获取所有动作"""
        return list(Exercise.select().order_by(Exercise.category, Exercise.name))

    @staticmethod
    def get_by_id(exercise_id: int) -> Optional[Exercise]:
        """根据 ID 获取动作"""
        try:
            return Exercise.get_by_id(exercise_id)
        except Exercise.DoesNotExist:
            return None

    @staticmethod
    def get_by_category(category: str) -> List[Exercise]:
        """根据分类获取动作"""
        return list(Exercise.select().where(Exercise.category == category))

    @staticmethod
    def create(name: str, duration: int, met: float, category: str) -> Exercise:
        """创建新动作"""
        return Exercise.create(
            name=name,
            duration_seconds=duration,
            met_value=met,
            category=category
        )

    @staticmethod
    def update(exercise_id: int, **kwargs) -> bool:
        """更新动作"""
        try:
            Exercise.update(**kwargs).where(Exercise.id == exercise_id).execute()
            return True
        except Exception:
            return False

    @staticmethod
    def delete(exercise_id: int) -> bool:
        """删除动作"""
        try:
            Exercise.delete_by_id(exercise_id)
            return True
        except Exception:
            return False

    @staticmethod
    def get_random_exercises(count: int) -> List[Exercise]:
        """
        随机获取指定数量的动作

        Args:
            count: 动作数量

        Returns:
            list: 随机动作列表
        """
        import random
        exercises = ExerciseRepository.get_all()
        if len(exercises) <= count:
            return exercises
        return random.sample(exercises, count)


class ExercisePlanRepository:
    """运动方案仓储"""

    @staticmethod
    def get_all() -> List[ExercisePlan]:
        """获取所有方案"""
        return list(ExercisePlan.select().order_by(ExercisePlan.name))

    @staticmethod
    def get_by_id(plan_id: int) -> Optional[ExercisePlan]:
        """根据 ID 获取方案"""
        try:
            return ExercisePlan.get_by_id(plan_id)
        except ExercisePlan.DoesNotExist:
            return None

    @staticmethod
    def create(name: str, description: str = None) -> ExercisePlan:
        """创建新方案"""
        return ExercisePlan.create(name=name, description=description)

    @staticmethod
    def add_exercise(plan_id: int, exercise_id: int, order_index: int) -> PlanExercise:
        """添加动作到方案"""
        return PlanExercise.create(
            plan=plan_id,
            exercise=exercise_id,
            order_index=order_index
        )

    @staticmethod
    def get_exercises(plan_id: int) -> List[Exercise]:
        """获取方案的动作列表"""
        query = (Exercise
                 .select()
                 .join(PlanExercise)
                 .where(PlanExercise.plan == plan_id)
                 .order_by(PlanExercise.order_index))
        return list(query)


class ActivityRepository:
    """活动记录仓储"""

    @staticmethod
    def log_stand(duration_seconds: int) -> ActivityLog:
        """记录站立"""
        return ActivityLog.log_stand(duration_seconds)

    @staticmethod
    def log_exercise(duration_seconds: int, calories: float, completed: bool = True) -> ActivityLog:
        """记录运动"""
        return ActivityLog.log_exercise(duration_seconds, calories, completed)

    @staticmethod
    def log_gaze(duration_seconds: int = 60) -> ActivityLog:
        """记录远眺"""
        return ActivityLog.log_gaze(duration_seconds)

    @staticmethod
    def get_today_stats() -> dict:
        """获取今日统计"""
        return ActivityLog.get_today_stats()

    @staticmethod
    def get_recent_activities(limit: int = 10) -> List[ActivityLog]:
        """获取最近活动"""
        return ActivityLog.get_recent_activity(limit)

    @staticmethod
    def get_activities_by_date(start_date: date, end_date: date = None) -> List[ActivityLog]:
        """
        获取指定日期范围的活动

        Args:
            start_date: 开始日期
            end_date: 结束日期（可选）

        Returns:
            list: 活动记录列表
        """
        if end_date is None:
            end_date = start_date

        # 将 date 转换为 datetime 边界
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        query = (ActivityLog
                 .select()
                 .where(
                    (ActivityLog.timestamp >= start_datetime) &
                    (ActivityLog.timestamp <= end_datetime)
                 )
                 .order_by(ActivityLog.timestamp))
        return list(query)

    @staticmethod
    def get_calories_by_date(target_date: date) -> float:
        """
        获取指定日期消耗的总热量

        Args:
            target_date: 目标日期

        Returns:
            float: 总热量（千卡）
        """
        logs = ActivityRepository.get_activities_by_date(target_date)
        return sum(log.calories_burned for log in logs if log.completed)

    @staticmethod
    def get_calories_last_7_days() -> List[Dict]:
        """
        获取最近 7 天的热量消耗

        Returns:
            list: [{"date": date, "calories": float}, ...]
        """
        result = []
        for i in range(7):
            target_date = date.today() - timedelta(days=i)
            calories = ActivityRepository.get_calories_by_date(target_date)
            result.append({
                "date": target_date.strftime("%m-%d"),
                "calories": calories
            })
        return result


class UserRepository:
    """用户仓储"""

    @staticmethod
    def get_weight() -> float:
        """获取当前体重"""
        return UserProfile.get_current_weight()

    @staticmethod
    def set_weight(weight_kg: float) -> UserProfile:
        """设置体重"""
        return UserProfile.update_weight(weight_kg)
