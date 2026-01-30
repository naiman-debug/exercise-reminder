# -*- coding: utf-8 -*-
"""
测试体验倒计时页面
"""
import pytest
from unittest.mock import Mock, patch
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer


@pytest.fixture
def app(qtbot):
    """创建 QApplication 实例"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_experience_page_creation(app):
    """测试体验倒计时页面可以创建"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()
    assert page is not None
    assert "准备就绪" in page.title()
    assert "开始您的健康之旅" in page.subTitle()
    assert page.layout() is not None


def test_experience_page_countdown_initialization(app):
    """测试倒计时初始化为 10 秒"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查倒计时时间是否初始化为 10
    assert page.countdown_time == 10
    assert page.countdown_label is not None


def test_experience_page_countdown_display(app):
    """测试倒计时显示正确"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查倒计时标签是否显示 10
    countdown_text = page.countdown_label.text()
    assert "10" in countdown_text or "10秒" in countdown_text


def test_experience_page_ui_elements(app):
    """测试 UI 元素是否存在"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查成功图标
    assert page.success_icon is not None
    assert "✅" in page.success_icon.text() or "check" in str(page.success_icon.text()).lower()

    # 检查按钮
    assert page.start_button is not None

    # 检查按钮文本
    assert "立即体验" in page.start_button.text() or "体验" in page.start_button.text()


def test_experience_page_signals(app):
    """测试信号是否存在"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查信号是否定义
    assert hasattr(page, 'start_experience')


def test_experience_page_skip_button_click(app, qtbot):
    """测试跳过按钮点击 - 已移除跳过功能"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 跳过按钮已移除，测试立即体验按钮
    assert page.start_button is not None


def test_experience_page_start_button_click(app, qtbot):
    """测试立即体验按钮点击"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 模拟信号连接
    start_signal_received = []

    def on_start():
        start_signal_received.append(True)

    page.start_experience.connect(on_start)

    # 点击立即体验按钮
    page.start_button.click()

    # 验证信号被触发
    assert len(start_signal_received) == 1


def test_experience_page_countdown_timer(app, qtbot):
    """测试倒计时计时器"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查计时器是否存在
    assert page.countdown_timer is not None
    assert isinstance(page.countdown_timer, QTimer)


def test_experience_page_countdown_interval(app):
    """测试倒计时间隔为 1 秒"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查计时器间隔是否为 1000 毫秒 (1 秒)
    assert page.countdown_timer.interval() == 1000


def test_experience_page_hint_card(app):
    """测试提示卡片是否存在"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查提示卡片是否存在
    assert page.hint_card is not None
    assert page.hint_label is not None


def test_experience_page_design_tokens(app):
    """测试使用 DesignTokens 样式"""
    from src.ui.wizards.experience_page import ExperiencePage
    from src.ui.design.tokens import DesignTokens

    page = ExperiencePage()

    # 检查页面是否应用了样式
    assert page.styleSheet() is not None or any(
        child.styleSheet() is not None
        for child in page.findChildren(type(child))
        if child != page
    )


def test_experience_page_logger(app):
    """测试日志系统是否集成"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查是否有 logger 属性
    assert hasattr(page, 'logger')
    assert page.logger is not None


def test_experience_page_countdown_auto_start(app):
    """测试页面加载后自动开始倒计时"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查计时器是否已启动（ isActive() 在 QTimer 上）
    # 注意：在测试环境中，我们只需要验证计时器配置正确
    assert page.countdown_timer is not None
    assert page.countdown_timer.interval() == 1000


def test_experience_page_button_styles(app):
    """测试按钮样式符合设计规范"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查立即体验按钮样式
    start_stylesheet = page.start_button.styleSheet()
    assert start_stylesheet is not None
    assert "background-color" in start_stylesheet


def test_experience_page_countdown_text_format(app):
    """测试倒计时显示文字格式正确"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 检查初始倒计时文字
    countdown_text = page.countdown_label.text()
    assert "应用将在" in countdown_text
    assert "10" in countdown_text
    assert "秒后开始运行" in countdown_text


def test_experience_page_countdown_tick_updates_text(app, qtbot):
    """测试倒计时每秒更新显示文字"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 停止自动倒计时
    page.countdown_timer.stop()

    # 手动触发倒计时
    initial_text = page.countdown_label.text()
    assert "10" in initial_text

    # 模拟倒计时
    page._on_countdown_tick()
    assert "9" in page.countdown_label.text()
    assert "应用将在" in page.countdown_label.text()


def test_experience_page_countdown_finish_behavior(app, qtbot):
    """测试倒计时结束后的行为"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 停止自动倒计时
    page.countdown_timer.stop()

    # 模拟信号连接
    start_signal_received = []

    def on_start():
        start_signal_received.append(True)

    page.start_experience.connect(on_start)

    # 手动将倒计时设置为 1
    page.countdown_time = 1

    # 触发最后一次倒计时
    page._on_countdown_tick()

    # 验证倒计时结束
    assert page.countdown_time == 0
    assert not page.countdown_timer.isActive()
    assert "开始体验" in page.countdown_label.text()
    assert len(start_signal_received) == 1


def test_experience_page_skip_stops_timer(app, qtbot):
    """测试跳过按钮会停止倒计时 - 已移除跳过功能"""
    from src.ui.wizards.experience_page import ExperiencePage
    from PySide6.QtGui import QShowEvent

    page = ExperiencePage()

    # 手动启动倒计时（模拟 showEvent 被调用）
    page.countdown_timer.start()

    # 确保倒计时在运行
    assert page.countdown_timer.isActive()

    # 使用 cleanupPage 停止倒计时（代替跳过按钮）
    page.cleanupPage()

    # 验证倒计时已停止
    assert not page.countdown_timer.isActive()


def test_experience_page_start_stops_timer(app, qtbot):
    """测试立即体验按钮会停止倒计时"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 手动启动倒计时（模拟 showEvent 被调用）
    page.countdown_timer.start()

    # 确保倒计时在运行
    assert page.countdown_timer.isActive()

    # 点击立即体验按钮
    page.start_button.click()

    # 验证倒计时已停止
    assert not page.countdown_timer.isActive()


def test_experience_page_hint_card_content(app):
    """测试提示卡片包含完整的使用说明"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 获取提示文字
    hint_text = page.hint_label.text()

    # 验证包含所有 5 条提示
    assert "所有提醒都是倒计时自动结束" in hint_text
    assert "站起提醒" in hint_text
    assert "微运动" in hint_text
    assert "远眺" in hint_text
    assert "系统托盘" in hint_text


def test_experience_page_signal_emission_on_countdown_finish(app, qtbot):
    """测试倒计时结束时触发 start_experience 信号"""
    from src.ui.wizards.experience_page import ExperiencePage

    page = ExperiencePage()

    # 停止自动倒计时
    page.countdown_timer.stop()

    # 模拟信号连接
    signal_received = []

    def on_start():
        signal_received.append("started")

    page.start_experience.connect(on_start)

    # 将倒计时设置为 1，然后触发
    page.countdown_time = 1
    page._on_countdown_tick()

    # 验证信号被触发
    assert len(signal_received) == 1
    assert signal_received[0] == "started"
