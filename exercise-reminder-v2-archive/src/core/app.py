# -*- coding: utf-8 -*-
"""
应用主类

协调所有模块，管理应用生命周期
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QMessageBox, QDialog,
    QVBoxLayout, QHBoxLayout, QPushButton, QWizard
)
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtCore import QObject, Signal, QSize, Qt

from .timer_manager import TimerManager, CountdownTimer
from .reminder_engine import ReminderEngine
from ..models.database import get_db_manager
from ..utils.config import ConfigManager
from ..utils.audio_player import AudioManager
from ..ui.dialogs.stand_dialog import StandReminderDialog
from ..ui.dialogs.exercise_dialog import ExerciseReminderDialog
from ..ui.dialogs.gaze_dialog import GazeReminderDialog
from ..ui.settings.settings_dialog import SettingsDialog
from ..ui.wizards import FirstRunWizard


class Application(QObject):
    """
    应用主类

    负责初始化和协调所有模块
    """

    # 信号
    app_started = Signal()
    app_stopped = Signal()

    def __init__(self):
        """初始化应用"""
        super().__init__()

        # 加载配置
        self.config = ConfigManager()

        # 初始化数据库
        self.db_manager = get_db_manager()
        self.db_manager.initialize_database()

        # 创建核心组件
        self.timer_manager = TimerManager()
        self.reminder_engine = ReminderEngine(self.timer_manager, self.config)

        # 音频管理器
        self.audio_manager = AudioManager(
            volume=self.config.get_audio_volume()
        )

        # 系统托盘
        self.tray_icon = None
        self.pause_action = None

        # 连接信号
        self._connect_signals()

    def _connect_signals(self):
        """连接信号"""
        # 提醒信号连接到显示弹窗
        self.reminder_engine.stand_reminder.connect(self._show_stand_reminder)
        self.reminder_engine.exercise_reminder.connect(self._show_exercise_reminder)
        self.reminder_engine.gaze_reminder.connect(self._show_gaze_reminder)

    def start(self):
        """启动应用"""
        # 检查是否首次运行
        is_first_run = self._is_first_run()
        print(f"========== 检查首次运行: {is_first_run} ==========")

        if is_first_run:
            # 首次运行，显示设置对话框
            print("========== 首次运行！准备显示引导向导 ==========")
            from PySide6.QtCore import QTimer
            QTimer.singleShot(500, self._show_first_run_setup)
        else:
            # 正常启动所有提醒
            print("========== 非首次运行，直接启动提醒 ==========")
            self.reminder_engine.start_all()

        # 创建系统托盘
        self._create_tray_icon()

        # 显示启动通知
        self._show_startup_notification()

        self.app_started.emit()

    def _is_first_run(self) -> bool:
        """检查是否首次运行"""
        from ..models.repositories import SettingRepository
        # 检查是否已完成首次运行
        value = SettingRepository.get("first_run_completed", "")
        print(f"_is_first_run: first_run_completed = '{value}'")
        return value != "true"

    def _show_first_run_setup(self):
        """显示首次运行设置（简化版）"""
        from ..models.repositories import SettingRepository, UserRepository
        from ..utils.bmr_calculator import BMRCalculator, Gender

        wizard = FirstRunWizard(self, None)

        if wizard.exec() == QWizard.DialogCode.Accepted:
            # 用户完成了向导，保存数据
            user_data = wizard.get_user_data()

            # 保存个人信息到配置
            self.config.set("user.height", user_data["height"])
            self.config.set("user.age", user_data["age"])
            # gender字段返回True(男)或False(女)，转换为字符串
            gender_str = "male" if user_data.get("gender") else "female"
            self.config.set("user.gender", gender_str)

            # 计算 BMR（基础代谢率）
            gender = Gender.MALE if gender_str == "male" else Gender.FEMALE
            bmr = BMRCalculator.calculate_bmr(
                weight_kg=user_data["weight"],
                height_cm=user_data["height"],
                age=user_data["age"],
                gender=gender
            )
            self.config.set("user.bmr", bmr)

            # 保存体重到数据库
            UserRepository.set_weight(user_data["weight"])

            # 保存提醒设置到配置
            self.config.set("reminder.global_offset", user_data.get("global_offset", 15))
            self.config.set("reminder.stand.interval", user_data.get("stand_interval", 45))
            self.config.set("reminder.stand.duration", user_data.get("stand_duration", 90))
            self.config.set("reminder.exercise.interval", user_data.get("exercise_interval", 60))
            self.config.set("reminder.exercise.duration", user_data.get("exercise_duration", 120))
            self.config.set("reminder.gaze.interval", user_data.get("gaze_interval", 75))
            self.config.set("reminder.gaze.duration", user_data.get("gaze_duration", 60))

            self.config.save()

            # 标记首次运行已完成
            SettingRepository.set("first_run_completed", "true")

            # 首次设置完成后，启动提醒（使用配置的值）
            self.reminder_engine.start_all()
        else:
            # 用户取消了向导，仍然标记为已完成并使用默认值
            SettingRepository.set("first_run_completed", "true")
            self.reminder_engine.start_all()

    def _show_startup_notification(self):
        """显示启动通知"""
        if self.tray_icon and self.tray_icon.isVisible():
            from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QFont
            from PySide6.QtCore import Qt

            # 创建简单的消息
            self.tray_icon.showMessage(
                "灵动休息健康助手",
                "应用已在后台运行\n点击托盘图标查看选项",
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )
        else:
            # 托盘不可用时，用消息框代替
            QMessageBox.information(
                None,
                "灵动休息健康助手",
                "应用已在后台运行\n请查看系统托盘"
            )

    def stop(self):
        """停止应用"""
        # 停止所有提醒
        self.reminder_engine.stop_all()

        # 停止定时器
        self.timer_manager.clear_all()

        # 关闭数据库
        self.db_manager.close()

        self.app_stopped.emit()

    def _create_tray_icon(self):
        """创建系统托盘图标"""
        # 创建简单的图标（使用系统标准图标）
        from PySide6.QtWidgets import QApplication
        from PySide6.QtGui import QPixmap, QPainter, QColor, QFont

        self.tray_icon = QSystemTrayIcon()

        # 创建简单的图标
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#4CAF50"))  # 绿色背景

        painter = QPainter(pixmap)
        painter.setPen(QColor("#FFFFFF"))
        font = QFont("Arial", 16, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "💪")
        painter.end()

        icon = QIcon(pixmap)
        self.tray_icon.setIcon(icon)

        # 设置工具提示
        self.tray_icon.setToolTip("灵动休息健康助手")

        # 创建托盘菜单
        menu = QMenu()

        # 查看统计
        stats_action = QAction("查看统计", self)
        stats_action.triggered.connect(self._show_statistics)
        menu.addAction(stats_action)

        # 设置
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self._show_settings)
        menu.addAction(settings_action)

        # 分隔符
        menu.addSeparator()

        # 暂停/恢复
        self.pause_action = QAction("暂停提醒", self)
        self.pause_action.triggered.connect(self._toggle_pause)
        menu.addAction(self.pause_action)

        # 分隔符
        menu.addSeparator()

        # 退出
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self._quit)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)

        # 显示托盘图标
        self.tray_icon.show()

    def _toggle_pause(self):
        """切换暂停/恢复状态"""
        if self.reminder_engine.get_active_reminders():
            # 当前运行中，暂停
            self.reminder_engine.stop_all()
            self.pause_action.setText("恢复提醒")
            self.tray_icon.setToolTip("灵动休息健康助手（已暂停）")
        else:
            # 当前暂停，恢复
            self.reminder_engine.start_all()
            self.pause_action.setText("暂停提醒")
            self.tray_icon.setToolTip("灵动休息健康助手（运行中）")

    def _show_stand_reminder(self, duration: int):
        """显示站立提醒弹窗"""
        try:
            dialog = StandReminderDialog(duration)
            # 设置为模态对话框
            dialog.exec()

        except Exception as e:
            print(f"显示站立提醒失败: {e}")

    def _show_exercise_reminder(self, exercises: list):
        """显示运动提醒弹窗"""
        try:
            # 获取用户体重
            weight = self.config.get_user_weight()

            dialog = ExerciseReminderDialog(exercises, weight)
            dialog.exec()

        except Exception as e:
            print(f"显示运动提醒失败: {e}")

    def _show_gaze_reminder(self, duration: int):
        """显示远眺提醒弹窗"""
        try:
            dialog = GazeReminderDialog(duration)
            dialog.exec()

        except Exception as e:
            print(f"显示远眺提醒失败: {e}")

    def _show_statistics(self):
        """显示统计界面"""
        from ..ui.statistics.statistics_widget import StatisticsWidget

        dialog = QDialog(None)
        dialog.setWindowTitle("活动统计")
        dialog.setMinimumSize(900, 700)
        # 设置关闭时不删除，防止影响应用
        dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)

        layout = QVBoxLayout(dialog)

        # 统计组件
        stats_widget = StatisticsWidget()
        layout.addWidget(stats_widget)

        # 关闭按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        close_btn = QPushButton("关闭")
        close_btn.setMinimumWidth(100)
        close_btn.clicked.connect(dialog.close)  # 使用 close 而不是 accept
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

        dialog.exec()

    def _show_settings(self):
        """显示设置界面"""
        try:
            dialog = SettingsDialog(None)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # 设置已更改，需要重新加载配置
                pass

        except Exception as e:
            print(f"显示设置失败: {e}")

    def _quit(self):
        """退出应用"""
        self.stop()
        QApplication.quit()


def create_application() -> Application:
    """
    创建应用实例

    注意：调用前需要先创建 QApplication 实例

    Returns:
        Application: 应用实例
    """
    application = Application()
    return application
