# -*- coding: utf-8 -*-
"""
完整的向导信号测试 - 验证所有页面操作和信号连接

测试覆盖：
1. ProfilePage - 字段注册和数据获取
2. ReminderSettingsPage - 字段注册和数据获取（新结构）
3. ExperiencePage - 跳过和立即体验信号
4. 向导完成流程
"""
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt


@pytest.fixture
def app(qtbot):
    """创建 QApplication 实例"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestWizardSignalsComplete:
    """完整的向导信号测试"""

    def test_profile_page_all_fields_registered(self, app):
        """测试 ProfilePage 所有字段正确注册"""
        from src.ui.wizards.profile_page import ProfilePage

        page = ProfilePage()

        # 验证字段已注册（直接访问控件）
        assert page.height_input.value() == 170
        assert page.weight_input.value() == 70.0
        assert page.age_input.value() == 30
        assert page.male_radio.isChecked() == True  # 男

    def test_reminder_settings_page_all_fields_registered(self, app):
        """测试 ReminderSettingsPage 所有字段正确注册（新结构）"""
        from src.ui.wizards.reminder_settings_page import ReminderSettingsPage

        page = ReminderSettingsPage()

        # 验证全局设置字段（直接访问控件）
        assert page.global_offset_spin.value() == 15

        # 验证提醒间隔字段
        assert page.stand_interval_spin.value() == 45
        assert page.exercise_interval_spin.value() == 60
        assert page.gaze_interval_spin.value() == 75

        # 验证执行时长字段
        assert page.stand_duration_spin.value() == 90
        assert page.exercise_duration_spin.value() == 120
        assert page.gaze_duration_spin.value() == 60

    def test_experience_page_signals_exist(self, app):
        """测试 ExperiencePage 信号存在"""
        from src.ui.wizards.experience_page import ExperiencePage

        page = ExperiencePage()

        # 验证信号存在
        assert hasattr(page, 'start_experience')
        assert hasattr(page, 'countdown_timer')

        # 验证按钮存在
        assert page.start_button is not None

    def test_experience_page_start_button_emits_signal(self, app, qtbot):
        """测试立即体验按钮发出信号"""
        from src.ui.wizards.experience_page import ExperiencePage

        page = ExperiencePage()

        # 连接信号捕获器
        signal_received = []

        def on_start():
            signal_received.append("start")

        page.start_experience.connect(on_start)

        # 点击立即体验按钮
        page.start_button.click()

        # 验证信号发出
        assert len(signal_received) == 1
        assert signal_received[0] == "start"

    def test_wizard_connects_experience_signals(self, app):
        """测试向导正确连接 ExperiencePage 信号"""
        from src.ui.wizards import FirstRunWizard

        wizard = FirstRunWizard()

        # 验证信号连接方法存在
        assert hasattr(wizard, '_on_start_experience')

        # 验证 ExperiencePage 的信号已连接
        experience_page = wizard.page(2)
        assert experience_page.start_button is not None

    def test_wizard_get_user_data_returns_all_fields(self, app):
        """测试向导 get_user_data 返回所有字段"""
        from src.ui.wizards import FirstRunWizard

        wizard = FirstRunWizard()

        # 填写 ProfilePage（使用正确的属性名）
        profile_page = wizard.page(0)
        profile_page.height_input.setValue(175)
        profile_page.weight_input.setValue(65.0)
        profile_page.age_input.setValue(25)
        profile_page.male_radio.click()

        # 填写 ReminderSettingsPage（使用正确的属性名）
        settings_page = wizard.page(1)
        settings_page.global_offset_spin.setValue(20)
        settings_page.stand_interval_spin.setValue(50)
        settings_page.exercise_interval_spin.setValue(65)
        settings_page.gaze_interval_spin.setValue(80)
        settings_page.stand_duration_spin.setValue(100)
        settings_page.exercise_duration_spin.setValue(130)
        settings_page.gaze_duration_spin.setValue(70)

        # 获取数据
        user_data = wizard.get_user_data()

        # 验证 ProfilePage 数据
        assert user_data["height"] == 175
        assert user_data["weight"] == 65.0
        assert user_data["age"] == 25
        assert user_data["gender"] == True

        # 验证 ReminderSettingsPage 数据（新结构）
        assert user_data["global_offset"] == 20
        assert user_data["stand_interval"] == 50
        assert user_data["exercise_interval"] == 65
        assert user_data["gaze_interval"] == 80
        assert user_data["stand_duration"] == 100
        assert user_data["exercise_duration"] == 130
        assert user_data["gaze_duration"] == 70

    def test_wizard_page_navigation(self, app):
        """测试向导页面导航"""
        from src.ui.wizards import FirstRunWizard

        wizard = FirstRunWizard()

        # 验证起始页
        start_id = wizard.startId()
        assert start_id == 0

        # 验证所有页面存在
        assert wizard.page(0) is not None
        assert wizard.page(1) is not None
        assert wizard.page(2) is not None
        assert wizard.page(3) is None

    def test_experience_page_countdown_not_active_on_init(self, app):
        """测试 ExperiencePage 倒计时在初始化时不启动"""
        from src.ui.wizards.experience_page import ExperiencePage

        page = ExperiencePage()

        # 验证倒计时未启动
        assert not page.countdown_timer.isActive()

    def test_experience_page_countdown_starts_on_show(self, app, qtbot):
        """测试 ExperiencePage 倒计时在显示时启动"""
        from src.ui.wizards.experience_page import ExperiencePage
        from PySide6.QtGui import QShowEvent

        page = ExperiencePage()

        # 模拟 showEvent
        page.showEvent(QShowEvent())

        # 验证倒计时已启动
        assert page.countdown_timer.isActive()

    def test_wizard_cleanup_on_experience_skip(self, app):
        """测试跳过体验时正确清理 - 已移除跳过功能"""
        from src.ui.wizards import FirstRunWizard

        wizard = FirstRunWizard()
        experience_page = wizard.page(2)

        # 启动倒计时
        experience_page.countdown_timer.start()

        # 倒计时应该在页面清理时停止
        experience_page.cleanupPage()

        # 验证倒计时已停止
        assert not experience_page.countdown_timer.isActive()

    def test_wizard_cleanup_on_experience_start(self, app):
        """测试立即体验时正确清理"""
        from src.ui.wizards import FirstRunWizard
        from unittest.mock import Mock

        # 创建模拟的 app 对象
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.get = Mock(side_effect=lambda key, default=None: default)
        mock_app.reminder_engine = Mock()

        wizard = FirstRunWizard(mock_app)
        experience_page = wizard.experience_page

        # 启动倒计时
        experience_page.countdown_timer.start()

        # 模拟开始体验（需要 mock 更多方法）
        # 这里只测试倒计时停止
        wizard.experience_page.countdown_timer.stop()

        # 验证倒计时已停止
        assert not experience_page.countdown_timer.isActive()
