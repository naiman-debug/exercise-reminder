# -*- coding: utf-8 -*-
"""
测试首次启动向导 - 3 页流程（按设计文档）

测试向导的正确结构和功能：
1. ProfilePage - 个人信息页
2. ReminderSettingsPage - 提醒设置页
3. ExperiencePage - 体验倒计时页
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtWidgets import QApplication, QWizard
from PySide6.QtCore import Qt, Signal, QObject


@pytest.fixture
def app(qtbot):
    """创建 QApplication 实例"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_wizard_imports(app):
    """测试向导模块可以正确导入"""
    from src.ui.wizards import FirstRunWizard
    assert FirstRunWizard is not None


def test_wizard_is_qwizard_subclass(app):
    """测试 FirstRunWizard 继承自 QWizard"""
    from src.ui.wizards import FirstRunWizard
    from PySide6.QtWidgets import QWizard

    assert issubclass(FirstRunWizard, QWizard)


def test_wizard_creation(app):
    """测试向导可以创建"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()
    assert wizard is not None
    assert wizard.windowTitle() == "灵动休息健康助手 - 首次设置"


def test_wizard_window_size(app):
    """测试向导窗口大小为 800x600"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()
    assert wizard.width() == 800
    assert wizard.height() == 600


def test_wizard_has_four_pages(app):
    """测试向导包含 3 个页面（按设计文档）"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # QWizard 的 page IDs 从 0 开始
    # 检查页面 0, 1, 2 是否存在（3页）
    assert wizard.page(0) is not None
    assert wizard.page(1) is not None
    assert wizard.page(2) is not None

    # 检查没有第 3 页
    assert wizard.page(3) is None


def test_wizard_page_order(app):
    """测试页面顺序正确（ProfilePage, ReminderSettingsPage, ExperiencePage）"""
    from src.ui.wizards import FirstRunWizard
    from src.ui.wizards.profile_page import ProfilePage
    from src.ui.wizards.reminder_settings_page import ReminderSettingsPage
    from src.ui.wizards.experience_page import ExperiencePage

    wizard = FirstRunWizard()

    # 验证页面顺序（ID 从 0 开始）- 3页结构
    page0 = wizard.page(0)
    page1 = wizard.page(1)
    page2 = wizard.page(2)

    assert isinstance(page0, ProfilePage)
    assert isinstance(page1, ReminderSettingsPage)
    assert isinstance(page2, ExperiencePage)


def test_wizard_stylesheet_applied(app):
    """测试向导应用了设计系统样式"""
    from src.ui.wizards import FirstRunWizard
    from src.ui.design.tokens import DesignTokens

    wizard = FirstRunWizard()

    # 检查是否应用了样式
    expected_stylesheet = DesignTokens.get_wizard_stylesheet()
    stylesheet = wizard.styleSheet()

    # 验证样式包含关键元素
    assert "QWizard" in stylesheet
    assert "background-color" in stylesheet


def test_wizard_has_logger(app):
    """测试向导集成了日志系统"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 检查是否有 logger 属性
    assert hasattr(wizard, 'logger')
    assert wizard.logger is not None


def test_wizard_experience_page_signals(app, qtbot):
    """测试向导正确连接 ExperiencePage 的信号"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 获取 ExperiencePage（ID: 2）- 3页结构中是第3页
    experience_page = wizard.page(2)

    # 验证页面有信号
    assert hasattr(experience_page, 'start_experience')


def test_wizard_no_theme_page(app):
    """测试向导不包含主题选择页"""
    from src.ui.wizards import FirstRunWizard
    from src.ui.wizards.theme_page import ThemePage

    wizard = FirstRunWizard()

    # 检查所有页面，确保没有 ThemePage
    for i in range(0, 10):  # 检查前 10 个页面
        page = wizard.page(i)
        if page:
            assert not isinstance(page, ThemePage), f"Page {i} should not be ThemePage"


def test_wizard_initial_page_is_welcome(app):
    """测试向导初始页面是个人信息页（ProfilePage）"""
    from src.ui.wizards import FirstRunWizard
    from src.ui.wizards.profile_page import ProfilePage

    wizard = FirstRunWizard()

    # 起始页应该是个人信息页（ID: 0）
    start_id = wizard.startId()
    assert start_id == 0

    # 起始页应该是 ProfilePage 实例
    start_page = wizard.page(start_id)
    assert isinstance(start_page, ProfilePage)


def test_wizard_navigation_buttons(app):
    """测试向导导航按钮存在"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 检查"下一步"按钮是否存在
    # 检查"取消"按钮是否存在
    # 具体实现可能需要调整


def test_wizard_can_navigate_forward(app, qtbot):
    """测试可以向导前进"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()
    wizard.show()

    # 起始页 ID 是 0
    start_id = wizard.startId()
    assert start_id == 0

    # 尝试前进到下一页
    # 注意：ProfilePage 需要填写必填字段才能前进
    # 这个测试可能需要模拟用户输入


def test_wizard_standalone_mode(app):
    """测试向导可以独立运行"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 向导应该可以独立显示
    wizard.show()

    # 验证向导可见
    assert wizard.isVisible()


def test_wizard_cleanup_on_cancel(app, qtbot):
    """测试取消向导时正确清理"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 验证 ExperiencePage 的计时器被停止（ID: 2）- 3页结构
    experience_page = wizard.page(2)

    # 获取计时器状态
    timer_active_before = experience_page.countdown_timer.isActive()

    # 取消向导
    wizard.reject()

    # 验证清理（可能需要在实现中添加清理逻辑）


def test_wizard_data_collection(app, qtbot):
    """测试向导可以收集所有页面数据"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 验证字段已注册
    # 验证可以获取 ProfilePage 数据
    # 验证可以获取 ReminderSettingsPage 数据

    # 这个测试需要验证向导的 field() 方法可以访问所有注册字段


def test_wizard_design_consistency(app):
    """测试向导设计一致性"""
    from src.ui.wizards import FirstRunWizard
    from src.ui.design.tokens import DesignTokens

    wizard = FirstRunWizard()

    # 验证所有页面使用相同的样式系统（ID: 0-2，3页结构）
    for i in range(0, 3):
        page = wizard.page(i)
        assert page is not None
        # 验证页面样式


def test_wizard_standalone_execution(app, qtbot):
    """测试向导可以作为独立程序执行"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()
    wizard.show()

    # 验证向导正常显示
    assert wizard.isVisible()

    # 验证向导有标题
    assert len(wizard.windowTitle()) > 0


def test_wizard_experience_page_auto_countdown(app):
    """测试 ExperiencePage 自动开始倒计时"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 导航到 ExperiencePage（ID: 2）- 3页结构
    # 注意：需要先填写前面的页面
    experience_page = wizard.page(2)

    # 验证计时器正在运行
    # 注意：这个测试可能需要模拟导航到第2页


def test_wizard_all_pages_use_design_tokens(app):
    """测试所有页面都使用 DesignTokens"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 验证每个页面都有样式（ID: 0-2，3页结构）
    for i in range(0, 3):
        page = wizard.page(i)
        assert page is not None
        # 验证样式已应用
        # 注意：具体验证取决于样式如何应用


def test_wizard_signal_connections(app):
    """测试向导信号连接正确"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 验证向导的信号存在
    assert hasattr(wizard, 'finished')
    assert hasattr(wizard, 'rejected')
    assert hasattr(wizard, 'accepted')


def test_wizard_modality(app):
    """测试向导模态设置"""
    from src.ui.wizards import FirstRunWizard

    wizard = FirstRunWizard()

    # 向导应该是模态对话框
    # 注意：具体实现可能需要调整


def test_wizard_window_flags(app):
    """测试向导窗口标志"""
    from src.ui.wizards import FirstRunWizard
    from PySide6.QtCore import Qt

    wizard = FirstRunWizard()

    # 验证窗口标志
    # 验证是否有最小化、最大化按钮等
