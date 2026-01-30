# -*- coding: utf-8 -*-
"""
定时器管理模块

管理应用的所有定时器
"""
from PySide6.QtCore import QObject, QTimer, Signal
from typing import Dict, Callable, Optional


class TimerManager(QObject):
    """
    定时器管理器

    负责创建、启动、停止和管理所有定时器
    """

    # 信号：定时器超时
    timeout = Signal(str)  # timer_name

    def __init__(self):
        """初始化定时器管理器"""
        super().__init__()
        self.timers: Dict[str, QTimer] = {}
        self.timer_callbacks: Dict[str, Callable] = {}

    def create_timer(
        self,
        name: str,
        interval_ms: int,
        single_shot: bool = True,
        callback: Optional[Callable] = None
    ) -> QTimer:
        """
        创建定时器

        Args:
            name: 定时器名称
            interval_ms: 间隔（毫秒）
            single_shot: 是否单次触发
            callback: 超时回调函数

        Returns:
            QTimer: 创建的定时器

        示例：
            >>> tm = TimerManager()
            >>> tm.create_timer("test", 1000, callback=lambda: print("timeout"))
            >>> tm.start_timer("test")
        """
        # 如果已存在同名定时器，先停止
        if name in self.timers:
            self.stop_timer(name)

        timer = QTimer()
        timer.setSingleShot(single_shot)
        timer.setInterval(interval_ms)

        # 连接回调
        if callback:
            self.timer_callbacks[name] = callback
            timer.timeout.connect(callback)
        else:
            timer.timeout.connect(lambda: self.timeout.emit(name))

        self.timers[name] = timer
        return timer

    def start_timer(self, name: str, interval_ms: Optional[int] = None) -> bool:
        """
        启动定时器

        Args:
            name: 定时器名称
            interval_ms: 间隔（毫秒），可选，用于覆盖创建时的设置

        Returns:
            bool: 是否成功启动
        """
        if name not in self.timers:
            return False

        timer = self.timers[name]
        if interval_ms is not None:
            timer.setInterval(interval_ms)

        timer.start()
        return True

    def stop_timer(self, name: str) -> bool:
        """
        停止定时器

        Args:
            name: 定时器名称

        Returns:
            bool: 是否成功停止
        """
        if name not in self.timers:
            return False

        self.timers[name].stop()
        return True

    def is_active(self, name: str) -> bool:
        """
        检查定时器是否活跃

        Args:
            name: 定时器名称

        Returns:
            bool: 是否活跃
        """
        if name not in self.timers:
            return False

        return self.timers[name].isActive()

    def remove_timer(self, name: str) -> bool:
        """
        移除定时器

        Args:
            name: 定时器名称

        Returns:
            bool: 是否成功移除
        """
        if name not in self.timers:
            return False

        timer = self.timers.pop(name)
        timer.stop()
        timer.deleteLater()

        if name in self.timer_callbacks:
            del self.timer_callbacks[name]

        return True

    def stop_all(self):
        """停止所有定时器"""
        for timer in self.timers.values():
            timer.stop()

    def clear_all(self):
        """清除所有定时器"""
        self.stop_all()
        self.timers.clear()
        self.timer_callbacks.clear()

    def get_timer(self, name: str) -> Optional[QTimer]:
        """
        获取定时器

        Args:
            name: 定时器名称

        Returns:
            QTimer: 定时器对象，不存在则返回 None
        """
        return self.timers.get(name)

    def get_active_timers(self) -> list:
        """
        获取所有活跃的定时器名称

        Returns:
            list: 活跃定时器名称列表
        """
        return [
            name for name, timer in self.timers.items()
            if timer.isActive()
        ]


class CountdownTimer(QTimer):
    """
    倒计时定时器

    专门用于倒计时的定时器类
    """

    # 信号
    tick = Signal(int)  # 剩余秒数
    finished = Signal()  # 倒计时结束

    def __init__(self, parent=None):
        """
        初始化倒计时时钟

        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self.remaining_seconds = 0
        self.timeout.connect(self._on_timeout)

    def start_countdown(self, seconds: int):
        """
        开始倒计时

        Args:
            seconds: 倒计时秒数
        """
        self.remaining_seconds = seconds
        self.setInterval(1000)  # 每秒触发一次
        self.tick.emit(seconds)
        super().start()

    def _on_timeout(self):
        """超时处理"""
        self.remaining_seconds -= 1

        if self.remaining_seconds <= 0:
            self.stop()
            self.finished.emit()
        else:
            self.tick.emit(self.remaining_seconds)

    def get_remaining(self) -> int:
        """
        获取剩余秒数

        Returns:
            int: 剩余秒数
        """
        return self.remaining_seconds

    def is_finished(self) -> bool:
        """
        是否已完成

        Returns:
            bool: 是否已完成
        """
        return self.remaining_seconds <= 0
