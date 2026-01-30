# -*- coding: utf-8 -*-
"""
对话框测试 - 动作库、用户信息、基础设置
"""
import pytest
from unittest.mock import Mock, patch
from PySide6.QtWidgets import QPushButton


@pytest.fixture
def app(qtbot):
    """创建 QApplication 实例"""
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_action_library_dialog_creation(app):
    """测试动作库对话框可以创建"""
    from src.ui.dialogs.action_library_dialog import ActionLibraryDialog

    dialog = ActionLibraryDialog()
    assert dialog is not None
    assert "动作库" in dialog.windowTitle()
    assert dialog.minimumWidth() == 600
    assert dialog.minimumHeight() == 400


def test_user_info_dialog_creation(app):
    """测试用户信息对话框可以创建"""
    from src.ui.dialogs.user_info_dialog import UserInfoDialog

    dialog = UserInfoDialog()
    assert dialog is not None
    assert "用户信息" in dialog.windowTitle()
    assert dialog.minimumWidth() == 500
    assert dialog.minimumHeight() == 400

    # 验证UI组件存在
    assert dialog.height_spin is not None
    assert dialog.weight_spin is not None
    assert dialog.age_spin is not None
    assert dialog.male_radio is not None
    assert dialog.female_radio is not None


def test_user_info_dialog_loads_data(app):
    """测试用户信息对话框加载数据"""
    with patch('src.ui.dialogs.user_info_dialog.UserRepository') as mock_repo, \
         patch('src.ui.dialogs.user_info_dialog.SettingRepository') as mock_setting:

        # 配置 mock
        mock_repo.get_weight.return_value = 70.0
        mock_setting.get_int.side_effect = lambda key, default: {
            "user.height": 175,
            "user.age": 30
        }.get(key, default)
        mock_setting.get.return_value = "male"

        from src.ui.dialogs.user_info_dialog import UserInfoDialog

        dialog = UserInfoDialog()

        # 验证数据被加载
        assert dialog.height_spin.value() == 175
        assert dialog.weight_spin.value() == 70.0
        assert dialog.age_spin.value() == 30
        assert dialog.male_radio.isChecked() == True


def test_user_info_dialog_saves_data(app):
    """测试用户信息对话框保存数据"""
    with patch('src.ui.dialogs.user_info_dialog.UserRepository') as mock_repo, \
         patch('src.ui.dialogs.user_info_dialog.SettingRepository') as mock_setting, \
         patch('src.utils.bmr_calculator.BMRCalculator') as mock_bmr:

        # 配置 mock
        mock_bmr.calculate_bmr.return_value = 1500.0

        from src.ui.dialogs.user_info_dialog import UserInfoDialog

        dialog = UserInfoDialog()
        # 修改值
        dialog.height_spin.setValue(180)
        dialog.weight_spin.setValue(75.0)
        dialog.age_spin.setValue(35)
        dialog.female_radio.click()

        # 调用保存
        dialog._save_and_close()

        # 验证保存被调用
        mock_repo.set_weight.assert_called_once_with(75.0)


def test_basic_settings_dialog_creation(app):
    """测试基础设置对话框可以创建"""
    from src.ui.dialogs.basic_settings_dialog import BasicSettingsDialog

    dialog = BasicSettingsDialog()
    assert dialog is not None
    assert "基础设置" in dialog.windowTitle()
    assert dialog.minimumWidth() == 500
    assert dialog.minimumHeight() == 400

    # 验证UI组件存在
    assert dialog.autostart_checkbox is not None
    assert dialog.startup_notify_checkbox is not None
    assert dialog.minimize_to_tray_checkbox is not None
    assert dialog.sound_enabled_checkbox is not None
    assert dialog.volume_slider is not None


def test_basic_settings_dialog_volume_slider(app):
    """测试音量滑块更新标签"""
    from src.ui.dialogs.basic_settings_dialog import BasicSettingsDialog

    dialog = BasicSettingsDialog()

    # 测试音量滑块
    dialog.volume_slider.setValue(50)
    assert "50%" in dialog.volume_value_label.text()

    dialog.volume_slider.setValue(80)
    assert "80%" in dialog.volume_value_label.text()


def test_basic_settings_dialog_sound_toggle(app):
    """测试音效开关控制音量滑块"""
    from src.ui.dialogs.basic_settings_dialog import BasicSettingsDialog

    dialog = BasicSettingsDialog()

    # 取消音效时，音量滑块应该禁用
    dialog.sound_enabled_checkbox.setChecked(False)
    assert not dialog.volume_slider.isEnabled()

    # 启用音效时，音量滑块应该启用
    dialog.sound_enabled_checkbox.setChecked(True)
    assert dialog.volume_slider.isEnabled()


def test_basic_settings_dialog_saves_settings(app):
    """测试基础设置对话框保存设置"""
    with patch('src.ui.dialogs.basic_settings_dialog.SettingRepository') as mock_setting:
        from src.ui.dialogs.basic_settings_dialog import BasicSettingsDialog

        dialog = BasicSettingsDialog()
        dialog.volume_slider.setValue(60)
        dialog.autostart_checkbox.setChecked(True)

        # 调用保存
        dialog._save_and_close()

        # 验证保存被调用
        assert mock_setting.set.called


def test_action_library_dialog_has_close_button(app):
    """测试动作库对话框有关闭按钮"""
    from src.ui.dialogs.action_library_dialog import ActionLibraryDialog
    from PySide6.QtCore import Qt

    dialog = ActionLibraryDialog()

    # 验证对话框可以被接受
    assert dialog.result() == 0  # QDialog.DialogCode.Rejected

    # 模拟点击关闭按钮
    buttons = dialog.findChildren(QPushButton)
    assert len(buttons) > 0  # 应该有关闭按钮

