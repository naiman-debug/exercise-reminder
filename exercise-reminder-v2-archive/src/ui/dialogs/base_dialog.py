# -*- coding: utf-8 -*-
"""
弹窗基类

所有提醒弹窗的基类，提供通用功能
"""
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QApplication
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QPalette, QColor, QMouseEvent
from typing import Optional
from src.utils.audio_player import AudioManager


class PulseAnimation(QPropertyAnimation):
    """
    闪烁动画 - 用于倒计时<10秒时红色闪烁效果

    按照设计文档 10.3 节要求：<10秒时红色闪烁
    """

    def __init__(self, target, property_name=b"windowOpacity"):
        super().__init__(target, property_name)
        self.setDuration(500)  # 500ms 完成一次闪烁
        self.setStartValue(1.0)
        self.setEndValue(0.6)
        self.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def set_looping(self, looping: bool):
        """设置是否循环"""
        if looping:
            self.finished.connect(self._restart)
        else:
            self.finished.disconnect(self._restart)

    def _restart(self):
        """重新启动动画（循环）"""
        if self.state() == QPropertyAnimation.State.Stopped:
            # 交换起始值和结束值，实现来回闪烁
            start = self.startValue()
            end = self.endValue()
            self.setStartValue(end)
            self.setEndValue(start)
            self.start()


class BaseReminderDialog(QDialog):
    """
    提醒弹窗基类

    提供所有提醒弹窗的通用功能：
    - 倒计时
    - 动画效果
    - 样式管理
    - 音效播放
    """

    # 信号
    completed = Signal()  # 完成
    skipped = Signal()  # 跳过

    def __init__(self, parent=None, has_title_bar: bool = False):
        """
        初始化弹窗基类

        Args:
            parent: 父窗口
            has_title_bar: 是否显示标题栏（默认无边框）
        """
        super().__init__(parent)
        self._has_title_bar = has_title_bar

        # 倒计时相关
        self.countdown_timer = CountdownTimer(self)
        self.countdown_timer.tick.connect(self._on_countdown_tick)
        self.countdown_timer.finished.connect(self._on_countdown_complete)

        # 动画相关
        self.fade_animation = None
        self.pulse_animation = None  # 倒计时<10秒时的闪烁动画

        # 音频管理器
        self.audio_manager = AudioManager()

        # 拖动相关
        self._drag_position = None

        # 设置窗口属性
        self._setup_window_properties()

        # 设置样式
        self._setup_styles()

        # 设置统一大小
        self._set_standard_size()

    def _setup_window_properties(self):
        """设置窗口属性"""
        # 基础标志
        flags = [
            Qt.WindowType.Window,
            Qt.WindowType.WindowStaysOnTopHint,
        ]

        # 如果不需要标题栏，添加无边框标志
        if not self._has_title_bar:
            flags.extend([
                Qt.WindowType.CustomizeWindowHint,
                Qt.WindowType.FramelessWindowHint,
            ])
        else:
            # 有标题栏：保留标准标题栏，但自定义窗口样式
            flags.extend([
                Qt.WindowType.CustomizeWindowHint,
            ])

        # 组合所有标志
        combined_flags = Qt.WindowType.Window
        for flag in flags[1:]:
            combined_flags |= flag
        self.setWindowFlags(combined_flags)

        # 不使用透明背景，使用纯色背景
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _setup_styles(self):
        """设置样式"""
        # 设置自动填充背景
        self.setAutoFillBackground(True)

        # 设置字体
        font = QFont("Microsoft YaHei UI", 36)
        self.setFont(font)

        # 设置调色板
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        self.setPalette(palette)

        # 设置背景颜色
        self.setStyleSheet("background-color: #FFFFFF;")

    def _set_standard_size(self):
        """设置统一窗口大小（屏幕的 50% x 45%）"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        width = int(screen_geometry.width() * 0.50)
        height = int(screen_geometry.height() * 0.45)

        self.setFixedSize(width, height)

    def get_countdown_color(self, remaining: int, total: int) -> str:
        """
        获取统一的倒计时颜色

        Args:
            remaining: 剩余秒数
            total: 总秒数

        Returns:
            str: 颜色代码
        """
        ratio = remaining / max(total, 1)
        if ratio > 0.5:
            return "#4CAF50"  # 绿色
        elif ratio > 0.3:
            return "#FFC107"  # 黄色
        elif ratio > 0.1:
            return "#FF9800"  # 橙色
        else:
            return "#F44336"  # 红色

    def showEvent(self, event):
        """
        窗口显示事件

        自动启动倒计时（子类可以重写此方法来禁用自动启动）
        """
        super().showEvent(event)
        # 子类应该设置 self.countdown_duration 并在此时启动
        # 默认不启动，由子类决定何时启动

    def start_reminder(self, seconds: int):
        """
        启动提醒（显示窗口并开始倒计时）

        Args:
            seconds: 倒计时秒数
        """
        self.show()
        self.start_countdown(seconds)

    def setup_ui(self):
        """
        设置UI（子类必须实现）

        子类应该重写此方法来创建自己的UI
        """
        raise NotImplementedError("子类必须实现 setup_ui 方法")

    def start_countdown(self, seconds: int):
        """
        开始倒计时

        Args:
            seconds: 倒计时秒数
        """
        self.remaining_seconds = seconds
        self._update_countdown_display()

        # 播放提示音
        self.audio_manager.play("reminder")

        # 开始倒计时
        self.countdown_timer.start_countdown(seconds)

        # 淡入动画
        self._fade_in()

    def _on_countdown_tick(self, remaining: int):
        """
        倒计时每秒触发

        Args:
            remaining: 剩余秒数
        """
        self.remaining_seconds = remaining
        self._update_countdown_display()

        # <10秒时启动红色闪烁（设计文档 10.3 节）
        if remaining == 10:
            self._start_pulse_animation()

        # 最后10秒播放提示音
        if remaining <= 10 and remaining > 0:
            self.audio_manager.play("tick")

    def _on_countdown_complete(self):
        """倒计时完成"""
        # 停止闪烁动画
        self._stop_pulse_animation()

        # 播放完成音
        self.audio_manager.play("complete")

        # 显示完成反馈
        self._show_complete_feedback()

        # 发送完成信号
        self.completed.emit()

        # 延迟关闭（1秒后自动关闭）
        QTimer.singleShot(1000, self._close_with_animation)

    def _update_countdown_display(self):
        """
        更新倒计时显示（子类实现）

        子类应该重写此方法来更新自己的倒计时显示
        """
        raise NotImplementedError("子类必须实现 _update_countdown_display 方法")

    def _show_complete_feedback(self):
        """显示完成反馈（子类可选实现）"""
        pass

    def _fade_in(self):
        """淡入动画"""
        self.setWindowOpacity(0)
        self.show()

        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)  # 300ms
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_animation.start()

    def _fade_out(self, callback=None):
        """淡出动画"""
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        if callback:
            self.fade_animation.finished.connect(callback)

        self.fade_animation.start()

    def _close_with_animation(self):
        """带动画关闭窗口"""
        self._fade_out(self.close)

    def skip(self):
        """跳过（子类可以重写）"""
        self.skipped.emit()
        self.audio_manager.play("skip")
        self._close_with_animation()

    def set_volume(self, volume: float):
        """
        设置音量

        Args:
            volume: 音量（0.0-1.0）
        """
        self.audio_manager.set_volume(volume)

    def keyPressEvent(self, event):
        """
        键盘事件处理

        Args:
            event: 键盘事件
        """
        # ESC 键禁用（无法关闭）
        if event.key() == Qt.Key.Key_Escape:
            return

        super().keyPressEvent(event)

    # ========== 窗口拖动功能 ==========
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件 - 开始拖动"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件 - 执行拖动"""
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_position is not None:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件 - 结束拖动"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = None
            event.accept()

    # ========== 闪烁动画（倒计时<10秒时红色闪烁）==========
    def _start_pulse_animation(self):
        """
        启动闪烁动画

        按照设计文档 10.3 节：<10秒时红色闪烁
        """
        if self.pulse_animation is None:
            self.pulse_animation = PulseAnimation(self, b"windowOpacity")
            self.pulse_animation.set_looping(True)
            self.pulse_animation.start()

    def _stop_pulse_animation(self):
        """停止闪烁动画"""
        if self.pulse_animation is not None:
            self.pulse_animation.set_looping(False)
            self.pulse_animation.stop()
            self.pulse_animation = None
            # 恢复完全不透明
            self.setWindowOpacity(1.0)


class CountdownTimer(QTimer):
    """
    倒计时时钟

    专用于倒计时的定时器
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
        """获取剩余秒数"""
        return self.remaining_seconds

    def is_finished(self) -> bool:
        """是否已完成"""
        return self.remaining_seconds <= 0
