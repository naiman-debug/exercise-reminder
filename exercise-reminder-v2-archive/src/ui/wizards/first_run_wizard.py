# -*- coding: utf-8 -*-
"""
首次启动向导 - 完整 QWizard 实现

3 页流程：
1. ProfilePage - 个人基础设置页
2. ReminderSettingsPage - 提醒设置页
3. ExperiencePage - 体验倒计时页
"""
from PySide6.QtWidgets import QWizard
from src.utils.logger import get_logger
from src.ui.design.tokens import DesignTokens
from functools import partial

# 导入各个页面
from .profile_page import ProfilePage
from .reminder_settings_page import ReminderSettingsPage
from .experience_page import ExperiencePage


class FirstRunWizard(QWizard):
    """首次启动向导 - 完整 QWizard 实现"""

    def __init__(self, app=None, parent=None):
        super().__init__(parent)

        # 保存应用引用
        self.app = app

        # 初始化日志
        self.logger = get_logger(__name__)
        self.logger.info("初始化首次启动向导")

        # 设置窗口属性
        self.setWindowTitle("灵动休息健康助手 - 首次设置")
        self.resize(800, 600)
        self.setMinimumSize(800, 600)

        # 应用样式
        self._apply_styles()

        # 创建并添加页面
        self._setup_pages()

        # 连接信号
        self._connect_signals()

        self.logger.info("首次启动向导初始化完成")

    def _setup_pages(self):
        """设置向导页面 - 简化为3页"""
        self.logger.info("设置向导页面")

        # 页面 1: 个人基础设置页 (ID: 0)
        self.profile_page = ProfilePage(self)
        self.profile_page_id = self.addPage(self.profile_page)
        self.logger.debug("添加个人基础设置页 (Page ID: 0)")

        # 页面 2: 提醒设置页 (ID: 1)
        self.settings_page = ReminderSettingsPage(self)
        self.settings_page_id = self.addPage(self.settings_page)
        self.logger.debug("添加提醒设置页 (Page ID: 1)")

        # 页面 3: 体验倒计时页 (ID: 2)
        self.experience_page = ExperiencePage(self)
        self.experience_page_id = self.addPage(self.experience_page)
        self.logger.debug("添加体验倒计时页 (Page ID: 2)")

        # 设置起始页
        self.setStartId(self.profile_page_id)

        # 隐藏所有标准导航按钮
        self.button(QWizard.WizardButton.CancelButton).hide()
        self.button(QWizard.WizardButton.BackButton).hide()
        self.button(QWizard.WizardButton.NextButton).hide()
        self.button(QWizard.WizardButton.FinishButton).hide()
        self.button(QWizard.WizardButton.CommitButton).hide()
        self.logger.debug(f"设置起始页为: {self.profile_page_id}")

    def _apply_styles(self):
        """应用设计系统样式 - 简化版避免渲染问题"""
        # 使用简化样式，避免复杂的边框和样式导致的显示问题
        stylesheet = """
            QWizard {
                background-color: #FFFFFF;
            }

            QWizardPage {
                background-color: #FFFFFF;
            }
        """
        self.setStyleSheet(stylesheet)
        self.logger.debug("应用向导简化样式")

    def _connect_signals(self):
        """连接信号"""
        # 连接 ExperiencePage 的信号
        self.experience_page.start_experience.connect(self._on_start_experience)

        # 连接向导完成信号
        self.finished.connect(self._on_wizard_finished)
        self.rejected.connect(self._on_wizard_rejected)

        self.logger.debug("连接向导信号")

    def _on_start_experience(self):
        """开始体验（倒计时结束或点击立即体验）"""
        self.logger.info("开始体验 - 随机触发一个提醒")
        # 停止倒计时
        if self.experience_page.countdown_timer.isActive():
            self.experience_page.countdown_timer.stop()

        # 先完成向导并保存数据
        self._complete_wizard_and_save()

        # 随机触发一个提醒让用户体验
        import random
        reminder_type = random.choice(['stand', 'exercise', 'gaze'])
        self._trigger_experience_reminder(reminder_type)

        # 关闭向导（放在最后，确保 QTimer 已设置）
        self.accept()

    def _complete_wizard_and_save(self):
        """完成向导并保存数据"""
        self.logger.info("完成向导并保存数据")

        # 获取用户数据
        user_data = self.get_user_data()

        # 保存数据到配置和数据库
        from src.models.repositories import SettingRepository, UserRepository
        from src.utils.bmr_calculator import BMRCalculator, Gender

        # 保存个人信息到配置
        self.app.config.set("user.height", user_data["height"])
        self.app.config.set("user.age", user_data["age"])
        # gender字段返回True(男)或False(女)，转换为字符串
        gender_str = "male" if user_data.get("gender") else "female"
        self.app.config.set("user.gender", gender_str)

        # 计算 BMR（基础代谢率）
        gender = Gender.MALE if gender_str == "male" else Gender.FEMALE
        bmr = BMRCalculator.calculate_bmr(
            weight_kg=user_data["weight"],
            height_cm=user_data["height"],
            age=user_data["age"],
            gender=gender
        )
        self.app.config.set("user.bmr", bmr)

        # 保存体重到数据库
        UserRepository.set_weight(user_data["weight"])

        # 保存提醒设置到配置
        self.app.config.set("reminder.global_offset", user_data.get("global_offset", 15))
        self.app.config.set("reminder.stand.interval", user_data.get("stand_interval", 45))
        self.app.config.set("reminder.stand.duration", user_data.get("stand_duration", 90))
        self.app.config.set("reminder.exercise.interval", user_data.get("exercise_interval", 60))
        self.app.config.set("reminder.exercise.duration", user_data.get("exercise_duration", 120))
        self.app.config.set("reminder.gaze.interval", user_data.get("gaze_interval", 75))
        self.app.config.set("reminder.gaze.duration", user_data.get("gaze_duration", 60))

        self.app.config.save()

        # 标记首次运行已完成
        SettingRepository.set("first_run_completed", "true")

        # 启动提醒系统
        self.app.reminder_engine.start_all()

        # 不在这里关闭向导，让调用者决定何时关闭

    def _trigger_experience_reminder(self, reminder_type: str):
        """触发体验提醒"""
        self.logger.info(f"触发体验提醒: {reminder_type}")

        # 根据类型获取对应的参数
        if reminder_type == 'stand':
            duration = self.app.config.get("reminder.stand.duration", 90)
        elif reminder_type == 'exercise':
            # 随机选择运动
            from src.data.exercise_data import EXERCISE_DATA
            exercises = random.sample(EXERCISE_DATA, min(3, len(EXERCISE_DATA)))
            # 延迟触发以确保向导已关闭
            from PySide6.QtCore import QTimer
            QTimer.singleShot(0, partial(self._show_exercise_reminder, exercises))
            return
        elif reminder_type == 'gaze':
            duration = self.app.config.get("reminder.gaze.duration", 60)
        else:
            self.logger.warning(f"未知的提醒类型: {reminder_type}")
            return

        # 触发提醒（延迟执行以确保向导已关闭）
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, partial(self._trigger_reminder, reminder_type, duration))

    def _trigger_reminder(self, reminder_type: str, duration: int):
        """实际触发提醒"""
        if reminder_type == 'stand':
            self.app.reminder_engine.stand_reminder.emit(duration)
        elif reminder_type == 'gaze':
            self.app.reminder_engine.gaze_reminder.emit(duration)

    def _show_exercise_reminder(self, exercises: list):
        """显示运动体验提醒"""
        self.logger.info(f"显示运动体验提醒，运动数量: {len(exercises)}")
        try:
            # 获取用户体重
            weight = self.app.config.get_user_weight()
            from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog
            dialog = ExerciseReminderDialog(exercises, weight)
            dialog.exec()
        except Exception as e:
            self.logger.error(f"显示运动提醒失败: {e}")

    def _on_wizard_finished(self, result):
        """向导完成时的处理"""
        self.logger.info(f"向导完成，结果: {result}")

        # 清理资源
        self._cleanup()

    def _on_wizard_rejected(self):
        """向导被取消时的处理"""
        self.logger.info("向导被用户取消")

        # 清理资源
        self._cleanup()

    def _cleanup(self):
        """清理资源"""
        self.logger.debug("清理向导资源")

        # 停止 ExperiencePage 的倒计时
        if self.experience_page and self.experience_page.countdown_timer.isActive():
            self.experience_page.countdown_timer.stop()

    def get_user_data(self) -> dict:
        """获取用户在向导中输入的所有数据

        Returns:
            dict: 包含所有用户输入数据的字典
        """
        self.logger.info("获取用户数据")

        # 直接从页面控件获取数据，避免字段名匹配问题
        profile_page = self.profile_page
        settings_page = self.settings_page

        user_data = {
            # ProfilePage 数据
            "height": profile_page.height_input.value(),
            "weight": profile_page.weight_input.value(),
            "age": profile_page.age_input.value(),
            "gender": profile_page.male_radio.isChecked(),

            # ReminderSettingsPage 数据（新结构）
            "global_offset": settings_page.global_offset_spin.value(),
            "stand_interval": settings_page.stand_interval_spin.value(),
            "exercise_interval": settings_page.exercise_interval_spin.value(),
            "gaze_interval": settings_page.gaze_interval_spin.value(),
            "stand_duration": settings_page.stand_duration_spin.value(),
            "exercise_duration": settings_page.exercise_duration_spin.value(),
            "gaze_duration": settings_page.gaze_duration_spin.value(),
        }

        self.logger.debug(f"用户数据: {user_data}")
        return user_data

    def accept(self):
        """接受向导（完成）"""
        self.logger.info("向导被接受")
        super().accept()

    def reject(self):
        """拒绝向导（取消）"""
        self.logger.info("向导被拒绝")
        self._cleanup()
        super().reject()


# 为了向后兼容，保留旧名称
SimpleProfileDialog = FirstRunWizard
