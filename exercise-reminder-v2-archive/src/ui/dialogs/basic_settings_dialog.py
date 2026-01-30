# -*- coding: utf-8 -*-
"""
基础设置对话框 - 音效、启动等设置

TODO: 实现完整的基础设置功能
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QCheckBox, QSlider, QComboBox
)
from PySide6.QtCore import Qt
from src.utils.logger import get_logger
from src.models.repositories import SettingRepository

logger = get_logger(__name__)


class BasicSettingsDialog(QDialog):
    """基础设置对话框 - 占位实现"""

    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("打开基础设置")

        self.setWindowTitle("🔧 基础设置")
        self.setMinimumSize(500, 400)

        # UI 组件
        self.autostart_checkbox = None
        self.startup_notify_checkbox = None
        self.minimize_to_tray_checkbox = None
        self.sound_enabled_checkbox = None
        self.volume_slider = None

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """设置 UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # 标题
        title = QLabel("🔧 基础设置")
        title.setStyleSheet("font-size: 16pt; font-weight: 600; color: #2C2C2C;")
        layout.addWidget(title)

        # 启动设置卡片
        startup_card = self._create_card("🚀 启动设置")
        startup_layout = startup_card.layout()

        self.autostart_checkbox = QCheckBox("开机自动运行")
        self.autostart_checkbox.setStyleSheet("font-size: 12pt; color: #2C2C2C;")
        startup_layout.addWidget(self.autostart_checkbox)

        self.startup_notify_checkbox = QCheckBox("启动时显示通知")
        self.startup_notify_checkbox.setStyleSheet("font-size: 12pt; color: #2C2C2C;")
        startup_layout.addWidget(self.startup_notify_checkbox)

        self.minimize_to_tray_checkbox = QCheckBox("关闭窗口时最小化到托盘")
        self.minimize_to_tray_checkbox.setStyleSheet("font-size: 12pt; color: #2C2C2C;")
        startup_layout.addWidget(self.minimize_to_tray_checkbox)

        layout.addWidget(startup_card)

        # 音频设置卡片
        audio_card = self._create_card("🔊 音频设置")
        audio_layout = audio_card.layout()

        self.sound_enabled_checkbox = QCheckBox("启用音效")
        self.sound_enabled_checkbox.setStyleSheet("font-size: 12pt; color: #2C2C2C;")
        self.sound_enabled_checkbox.toggled.connect(self._on_sound_enabled_changed)
        audio_layout.addWidget(self.sound_enabled_checkbox)

        # 音量控制
        volume_layout = QHBoxLayout()
        volume_label = QLabel("音量:")
        volume_label.setStyleSheet("font-size: 12pt; color: #2C2C2C;")
        volume_label.setMinimumWidth(60)
        volume_layout.addWidget(volume_label)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setMinimumWidth(200)
        volume_layout.addWidget(self.volume_slider)

        self.volume_value_label = QLabel("70%")
        self.volume_value_label.setStyleSheet("font-size: 12pt; color: #6B6B6B;")
        self.volume_value_label.setMinimumWidth(40)
        volume_layout.addWidget(self.volume_value_label)

        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        audio_layout.addLayout(volume_layout)

        layout.addWidget(audio_card)

        # 提示信息
        hint_label = QLabel("💡 提示：部分设置需要重启应用后生效")
        hint_label.setStyleSheet("font-size: 10pt; color: #6B6B6B; padding: 8px;")
        layout.addWidget(hint_label)

        layout.addStretch()

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("保存")
        save_button.setFixedSize(100, 36)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        save_button.clicked.connect(self._save_and_close)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("取消")
        cancel_button.setFixedSize(100, 36)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #2C2C2C;
                border: none;
                border-radius: 6px;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def _create_card(self, title: str) -> QFrame:
        """创建设置卡片"""
        card = QFrame()
        card.setStyleSheet("background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E0E0E0;")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13pt; font-weight: 600; color: #2C2C2C;")
        layout.addWidget(title_label)

        return card

    def _on_volume_changed(self, value: int):
        """音量滑块值改变"""
        self.volume_value_label.setText(f"{value}%")

    def _on_sound_enabled_changed(self, checked: bool):
        """音效启用状态改变"""
        self.volume_slider.setEnabled(checked)

    def _load_settings(self):
        """加载设置"""
        try:
            # 从配置加载（使用默认值，因为还没实现配置持久化）
            self.autostart_checkbox.setChecked(False)
            self.startup_notify_checkbox.setChecked(True)
            self.minimize_to_tray_checkbox.setChecked(True)
            self.sound_enabled_checkbox.setChecked(True)

            volume = SettingRepository.get_int("audio.volume", 70)
            self.volume_slider.setValue(volume)
            self.volume_value_label.setText(f"{volume}%")

        except Exception as e:
            logger.error(f"加载设置失败: {e}")

    def _save_and_close(self):
        """保存并关闭"""
        try:
            # TODO: 实现设置保存到配置文件
            SettingRepository.set("audio.volume", str(self.volume_slider.value()))
            SettingRepository.set("basic.autostart", str(self.autostart_checkbox.isChecked()))
            SettingRepository.set("basic.startup_notify", str(self.startup_notify_checkbox.isChecked()))
            SettingRepository.set("basic.minimize_to_tray", str(self.minimize_to_tray_checkbox.isChecked()))
            SettingRepository.set("basic.sound_enabled", str(self.sound_enabled_checkbox.isChecked()))

            logger.info("基础设置已保存")
            self.accept()

        except Exception as e:
            logger.error(f"保存设置失败: {e}")

    def accept(self):
        """接受对话框"""
        super().accept()

    def reject(self):
        """拒绝对话框"""
        logger.info("取消基础设置")
        super().reject()
