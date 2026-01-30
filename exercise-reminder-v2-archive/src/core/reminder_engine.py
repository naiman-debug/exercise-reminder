# -*- coding: utf-8 -*-
"""
提醒引擎模块

负责调度和触发所有类型的提醒
"""
import random
from datetime import datetime, timedelta
from PySide6.QtCore import QObject, Signal
from typing import List, Dict, Any, Optional
from .timer_manager import TimerManager
from ..utils.config import ConfigManager
from ..models.repositories import ExerciseRepository, ActivityRepository


class ReminderEngine(QObject):
    """
    提醒引擎

    管理所有提醒的调度和触发
    """

    # 信号：提醒触发
    stand_reminder = Signal(int)  # 强制站立（秒数）
    exercise_reminder = Signal(list)  # 微运动（动作列表）
    gaze_reminder = Signal(int)  # 强制远眺（秒数）

    # 提醒类型常量
    REMINDER_STAND = "stand"
    REMINDER_EXERCISE = "exercise"
    REMINDER_GAZE = "gaze"

    # 冷却期配置（秒）
    COOLDOWN_SECONDS = 120  # 2分钟冷却期

    def __init__(self, timer_manager: TimerManager, config: ConfigManager):
        """
        初始化提醒引擎

        Args:
            timer_manager: 定时器管理器
            config: 配置管理器
        """
        super().__init__()
        self.timer_manager = timer_manager
        self.config = config
        self.active_reminders = set()
        # 冷却期跟踪：记录每种类型上次触发时间
        self.last_trigger_time: Dict[str, Optional[datetime]] = {
            self.REMINDER_STAND: None,
            self.REMINDER_EXERCISE: None,
            self.REMINDER_GAZE: None,
        }

    def start_all(self):
        """启动所有已启用的提醒"""
        if self.config.is_reminder_enabled(self.REMINDER_STAND):
            self.schedule_stand_reminder()

        if self.config.is_reminder_enabled(self.REMINDER_EXERCISE):
            self.schedule_exercise_reminder()

        if self.config.is_reminder_enabled(self.REMINDER_GAZE):
            self.schedule_gaze_reminder()

    def stop_all(self):
        """停止所有提醒"""
        self.timer_manager.stop_all()
        self.active_reminders.clear()

    def schedule_stand_reminder(self):
        """调度站立提醒"""
        min_min, max_min = self.config.get_interval_range(self.REMINDER_STAND)
        duration = self.config.get(f"reminder.{self.REMINDER_STAND}.duration", 90)

        # 计算随机间隔
        interval_ms = self._calculate_random_interval(min_min, max_min)

        # 创建定时器
        def trigger_stand():
            # 记录触发时间
            self._record_trigger(self.REMINDER_STAND)
            self.stand_reminder.emit(duration)
            # 重新调度
            self.schedule_stand_reminder()

        self.timer_manager.create_timer(
            self.REMINDER_STAND,
            interval_ms,
            callback=trigger_stand
        )
        self.timer_manager.start_timer(self.REMINDER_STAND)
        self.active_reminders.add(self.REMINDER_STAND)

    def schedule_exercise_reminder(self):
        """调度运动提醒"""
        min_min, max_min = self.config.get_interval_range(self.REMINDER_EXERCISE)

        # 计算随机间隔
        interval_ms = self._calculate_random_interval(min_min, max_min)

        # 获取 1 个随机动作
        exercises = ExerciseRepository.get_random_exercises(1)
        exercise_list = [
            {
                "id": ex.id,
                "name": ex.name,
                "duration": ex.duration_seconds,
                "met": ex.met_value
            }
            for ex in exercises
        ]

        # 创建定时器
        def trigger_exercise():
            # 记录触发时间
            self._record_trigger(self.REMINDER_EXERCISE)
            self.exercise_reminder.emit(exercise_list)
            # 重新调度
            self.schedule_exercise_reminder()

        self.timer_manager.create_timer(
            self.REMINDER_EXERCISE,
            interval_ms,
            callback=trigger_exercise
        )
        self.timer_manager.start_timer(self.REMINDER_EXERCISE)
        self.active_reminders.add(self.REMINDER_EXERCISE)

    def schedule_gaze_reminder(self):
        """调度远眺提醒"""
        min_min, max_min = self.config.get_interval_range(self.REMINDER_GAZE)
        duration = self.config.get(f"reminder.{self.REMINDER_GAZE}.duration", 20)

        # 计算随机间隔
        interval_ms = self._calculate_random_interval(min_min, max_min)

        # 创建定时器
        def trigger_gaze():
            # 记录触发时间
            self._record_trigger(self.REMINDER_GAZE)
            self.gaze_reminder.emit(duration)
            # 重新调度
            self.schedule_gaze_reminder()

        self.timer_manager.create_timer(
            self.REMINDER_GAZE,
            interval_ms,
            callback=trigger_gaze
        )
        self.timer_manager.start_timer(self.REMINDER_GAZE)
        self.active_reminders.add(self.REMINDER_GAZE)

    @staticmethod
    def _calculate_random_interval(min_min: int, max_min: int) -> int:
        """
        计算随机间隔

        Args:
            min_min: 最小分钟数
            max_min: 最大分钟数

        Returns:
            int: 间隔毫秒数

        示例：
            >>> ReminderEngine._calculate_random_interval(30, 60)
            1800000  # 30分钟
        """
        minutes = random.randint(min_min, max_min)
        return minutes * 60 * 1000

    def is_reminder_active(self, reminder_type: str) -> bool:
        """
        检查提醒是否活跃

        Args:
            reminder_type: 提醒类型

        Returns:
            bool: 是否活跃
        """
        return reminder_type in self.active_reminders

    def get_active_reminders(self) -> List[str]:
        """
        获取所有活跃的提醒类型

        Returns:
            list: 活跃提醒类型列表
        """
        return list(self.active_reminders)

    def pause_reminder(self, reminder_type: str):
        """
        暂停指定提醒

        Args:
            reminder_type: 提醒类型
        """
        self.timer_manager.stop_timer(reminder_type)
        self.active_reminders.discard(reminder_type)

    def resume_reminder(self, reminder_type: str):
        """
        恢复指定提醒

        Args:
            reminder_type: 提醒类型
        """
        if reminder_type == self.REMINDER_STAND:
            self.schedule_stand_reminder()
        elif reminder_type == self.REMINDER_EXERCISE:
            self.schedule_exercise_reminder()
        elif reminder_type == self.REMINDER_GAZE:
            self.schedule_gaze_reminder()

    def is_in_cooldown(self, reminder_type: Optional[str] = None) -> bool:
        """
        检查是否在冷却期

        Args:
            reminder_type: 提醒类型，如果为 None 则检查全局冷却期

        Returns:
            bool: 是否在冷却期
        """
        now = datetime.now()

        if reminder_type is not None:
            # 检查特定类型的冷却期
            last_time = self.last_trigger_time.get(reminder_type)
            if last_time is None:
                return False
            cooldown_end = last_time + timedelta(seconds=self.COOLDOWN_SECONDS)
            return now < cooldown_end
        else:
            # 检查全局冷却期（任何提醒类型）
            for last_time in self.last_trigger_time.values():
                if last_time is not None:
                    cooldown_end = last_time + timedelta(seconds=self.COOLDOWN_SECONDS)
                    if now < cooldown_end:
                        return True
            return False

    def get_cooldown_remaining(self, reminder_type: Optional[str] = None) -> float:
        """
        获取冷却期剩余时间（秒）

        Args:
            reminder_type: 提醒类型，如果为 None 则检查全局冷却期

        Returns:
            float: 剩余秒数，0 表示不在冷却期
        """
        now = datetime.now()

        if reminder_type is not None:
            last_time = self.last_trigger_time.get(reminder_type)
            if last_time is None:
                return 0
            cooldown_end = last_time + timedelta(seconds=self.COOLDOWN_SECONDS)
            remaining = (cooldown_end - now).total_seconds()
            return max(0, remaining)
        else:
            # 返回所有类型中的最大剩余时间
            max_remaining = 0
            for last_time in self.last_trigger_time.values():
                if last_time is not None:
                    cooldown_end = last_time + timedelta(seconds=self.COOLDOWN_SECONDS)
                    remaining = (cooldown_end - now).total_seconds()
                    max_remaining = max(max_remaining, remaining)
            return max(0, max_remaining)

    def _record_trigger(self, reminder_type: str):
        """
        记录提醒触发时间

        Args:
            reminder_type: 提醒类型
        """
        self.last_trigger_time[reminder_type] = datetime.now()
