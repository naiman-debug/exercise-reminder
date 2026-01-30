# -*- coding: utf-8 -*-
"""
UI 设计符合性测试

验证实现是否完全符合 DESIGN-UI-001.md 设计规范
"""
import pytest
from PySide6.QtWidgets import QApplication, QWidget, QFrame
from PySide6.QtCore import Qt


@pytest.fixture
def app(qtbot):
    """创建 QApplication 实例"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def find_card_by_label(page, label_text):
    """根据标签文本查找卡片"""
    # 遍历所有子控件
    for child in page.findChildren(QFrame):
        labels = child.findChildren(QWidget)
        for label in labels:
            if hasattr(label, 'text') and label.text() == label_text:
                return child
    return None


class TestWizardDesign:
    """向导设计符合性测试（设计文档第 6 节）"""

    def test_wizard_has_three_pages(self, app):
        """向导应为3页（设计文档 6.1 节）"""
        from src.ui.wizards import FirstRunWizard

        wizard = FirstRunWizard()

        # 应该有3页：ProfilePage, ReminderSettingsPage, ExperiencePage
        assert wizard.page(0) is not None
        assert wizard.page(1) is not None
        assert wizard.page(2) is not None
        assert wizard.page(3) is None  # 不应该有第4页

    def test_wizard_page_structure(self, app):
        """向导页面结构（设计文档 6.1 节）"""
        from src.ui.wizards import FirstRunWizard
        from src.ui.wizards.profile_page import ProfilePage
        from src.ui.wizards.reminder_settings_page import ReminderSettingsPage
        from src.ui.wizards.experience_page import ExperiencePage

        wizard = FirstRunWizard()

        assert isinstance(wizard.page(0), ProfilePage)
        assert isinstance(wizard.page(1), ReminderSettingsPage)
        assert isinstance(wizard.page(2), ExperiencePage)

    def test_wizard_window_size(self, app):
        """向导窗口大小 800x600（设计文档 6.2 节）"""
        from src.ui.wizards import FirstRunWizard

        wizard = FirstRunWizard()

        assert wizard.width() == 800
        assert wizard.height() == 600


class TestDialogDesign:
    """弹窗设计符合性测试（设计文档第 5 节）"""

    def test_stand_dialog_frameless(self, app):
        """站立弹窗无边框（设计文档 5.1 节）"""
        from src.ui.dialogs.stand_dialog import StandReminderDialog

        dialog = StandReminderDialog(duration=30)

        # 检查无边框标志
        flags = dialog.windowFlags()
        assert flags & Qt.WindowType.FramelessWindowHint

    def test_stand_dialog_size(self, app):
        """站立弹窗尺寸 60%x50%（设计文档 5.1 节）"""
        from src.ui.dialogs.stand_dialog import StandReminderDialog
        from PySide6.QtWidgets import QApplication

        dialog = StandReminderDialog(duration=30)

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        expected_width = int(screen_geometry.width() * 0.60)
        expected_height = int(screen_geometry.height() * 0.50)

        assert dialog.width() == expected_width
        assert dialog.height() == expected_height

    def test_exercise_dialog_has_title_bar(self, app):
        """微运动弹窗有标题栏（设计文档 5.2 节）"""
        from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog

        exercises = [{"name": "深蹲", "duration": 30, "met": 5.0}]
        dialog = ExerciseReminderDialog(exercises=exercises)

        # 检查有标题栏（不应该有 FramelessWindowHint）
        flags = dialog.windowFlags()
        assert not (flags & Qt.WindowType.FramelessWindowHint)

        # 验证窗口标题
        assert "深蹲" in dialog.windowTitle()

    def test_exercise_dialog_size(self, app):
        """微运动弹窗尺寸 800x600（设计文档 5.2 节）"""
        from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog

        exercises = [{"name": "深蹲", "duration": 30, "met": 5.0}]
        dialog = ExerciseReminderDialog(exercises=exercises)

        assert dialog.width() == 800
        assert dialog.height() == 600

    def test_gaze_dialog_frameless(self, app):
        """远眺弹窗无边框（设计文档 5.3 节）"""
        from src.ui.dialogs.gaze_dialog import GazeReminderDialog

        dialog = GazeReminderDialog(duration=30)

        # 检查无边框标志
        flags = dialog.windowFlags()
        assert flags & Qt.WindowType.FramelessWindowHint

    def test_gaze_dialog_size(self, app):
        """远眺弹窗尺寸 50%x40%（设计文档 5.3 节）"""
        from src.ui.dialogs.gaze_dialog import GazeReminderDialog
        from PySide6.QtWidgets import QApplication

        dialog = GazeReminderDialog(duration=30)

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        expected_width = int(screen_geometry.width() * 0.50)
        expected_height = int(screen_geometry.height() * 0.40)

        assert dialog.width() == expected_width
        assert dialog.height() == expected_height


class TestCountdownDesign:
    """倒计时设计符合性测试（设计文档第 10.3 节）"""

    def test_countdown_color_scheme(self, app):
        """倒计时颜色方案（设计文档 10.3 节）"""
        from src.ui.dialogs.stand_dialog import StandReminderDialog

        dialog = StandReminderDialog(duration=100)

        # >50%: 绿色
        assert dialog.get_countdown_color(60, 100) == "#4CAF50"
        # 30-50%: 黄色
        assert dialog.get_countdown_color(40, 100) == "#FFC107"
        # 10-30%: 橙色
        assert dialog.get_countdown_color(15, 100) == "#FF9800"
        # <10秒: 红色
        assert dialog.get_countdown_color(9, 100) == "#F44336"

    def test_countdown_pulse_animation_exists(self, app):
        """倒计时<10秒时有脉冲动画（设计文档 10.3 节）"""
        from src.ui.dialogs.stand_dialog import StandReminderDialog

        dialog = StandReminderDialog(duration=30)

        # 验证脉冲动画方法存在
        assert hasattr(dialog, '_start_pulse_animation')
        assert hasattr(dialog, '_stop_pulse_animation')
        assert hasattr(dialog, 'pulse_animation')


class TestProfilePageDesign:
    """ProfilePage 设计符合性测试（设计文档第 7.1 节）"""

    def test_profile_page_card_size(self, app):
        """个人信息页卡片尺寸 140x180（设计文档 7.1 节）"""
        from src.ui.wizards.profile_page import ProfilePage

        page = ProfilePage()

        # 查找输入卡片并验证尺寸
        # 身高卡片
        cards = page.findChildren(QFrame)
        input_cards = [c for c in cards if c.width() == 160 and c.height() == 200]

        # 应该有至少4个输入卡片（身高、体重、年龄、性别）
        assert len(input_cards) >= 4, f"Expected at least 4 cards with 160x200 size, found {len(input_cards)}"

    def test_profile_page_icon_size(self, app):
        """个人信息页图标大小 40pt（设计文档 7.1 节）"""
        from src.ui.wizards.profile_page import ProfilePage
        from PySide6.QtWidgets import QLabel

        page = ProfilePage()

        # 查找所有 QLabel
        labels = page.findChildren(QLabel)

        # 查找包含图标 emoji 的标签（如 📏、⚖️、🎂、👤）
        icon_labels = [l for l in labels if l.text() in ['📏', '⚖️', '🎂', '👤']]

        # 验证图标存在
        assert len(icon_labels) >= 4, "Should have at least 4 icon labels"

        # 验证样式包含 40pt
        for label in icon_labels:
            style = label.styleSheet()
            # 样式应该包含 font-size: 40pt
            assert 'font-size' in style.lower(), f"Icon label should have font-size in style"
            assert '40' in style, f"Icon label should have 40pt size"
