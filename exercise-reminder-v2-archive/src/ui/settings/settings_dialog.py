# -*- coding: utf-8 -*-
"""
设置主对话框

提供应用的设置界面
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QWidget,
    QLabel, QSpinBox, QDoubleSpinBox, QCheckBox,
    QGroupBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from src.utils.config import ConfigManager
from src.models.repositories import UserRepository
from src.ui.statistics.stats_view import StatisticsView
from src.ui.design.tokens import DesignTokens


class SettingsDialog(QDialog):
    """
    设置主对话框

    提供标签页式的设置界面
    """

    # 信号：设置已更改
    settings_changed = Signal()

    def __init__(self, parent=None):
        """
        初始化设置对话框

        Args:
            parent: 父窗口
        """
        super().__init__(parent)

        self.config = ConfigManager()
        self.modified = False

        # UI 组件
        self.tabs = None
        self.apply_btn = None
        self.cancel_btn = None

        self.setup_ui()
        self._load_settings()

    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("设置")
        self.setModal(True)
        self.setMinimumSize(700, 500)

        # 主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # 标签页
        self.tabs = QTabWidget()

        # 各个设置页面
        self.tabs.addTab(self._create_reminder_tab(), "提醒")
        self.tabs.addTab(self._create_exercise_tab(), "动作库")
        self.tabs.addTab(self._create_audio_tab(), "音频")
        self.tabs.addTab(self._create_user_tab(), "用户")
        # 统计页面
        self.stats_view = StatisticsView()
        self.tabs.addTab(self.stats_view, "统计")

        layout.addWidget(self.tabs)

        # 按钮栏
        btn_layout = self._create_button_layout()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # 应用呼吸感设计样式
        DesignTokens.apply_stylesheet(self, "all")

    def _create_button_layout(self) -> QHBoxLayout:
        """创建按钮布局"""
        layout = QHBoxLayout()
        layout.addStretch()

        self.apply_btn = QPushButton("应用")
        self.apply_btn.setMinimumWidth(100)
        self.apply_btn.clicked.connect(self._apply_settings)
        self.apply_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.clicked.connect(self.reject)

        layout.addWidget(self.apply_btn)
        layout.addWidget(self.cancel_btn)

        return layout

    def _create_reminder_tab(self) -> QWidget:
        """创建提醒设置页面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # 强制站立提醒
        stand_group = self._create_stand_settings()
        layout.addWidget(stand_group)

        # 微运动提醒
        exercise_group = self._create_exercise_settings()
        layout.addWidget(exercise_group)

        # 强制远眺提醒
        gaze_group = self._create_gaze_settings()
        layout.addWidget(gaze_group)

        layout.addStretch()
        return widget

    def _create_stand_settings(self) -> QGroupBox:
        """创建强制站立提醒设置"""
        group = QGroupBox("强制站立提醒")
        layout = QVBoxLayout()

        # 启用复选框
        self.stand_enabled_cb = QCheckBox("启用强制站立提醒")
        self.stand_enabled_cb.stateChanged.connect(self._on_modified)

        # 间隔范围
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("间隔范围："))

        self.stand_interval_min_spin = QSpinBox()
        self.stand_interval_min_spin.setRange(5, 120)
        self.stand_interval_min_spin.setSuffix(" 分钟")
        self.stand_interval_min_spin.valueChanged.connect(self._on_modified)

        interval_layout.addWidget(self.stand_interval_min_spin)
        interval_layout.addWidget(QLabel("-"))

        self.stand_interval_max_spin = QSpinBox()
        self.stand_interval_max_spin.setRange(5, 180)
        self.stand_interval_max_spin.setSuffix(" 分钟")
        self.stand_interval_max_spin.valueChanged.connect(self._on_modified)

        interval_layout.addWidget(self.stand_interval_max_spin)
        interval_layout.addStretch()

        # 倒计时时长
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("倒计时时长："))

        self.stand_duration_spin = QSpinBox()
        self.stand_duration_spin.setRange(30, 300)
        self.stand_duration_spin.setSuffix(" 秒")
        self.stand_duration_spin.valueChanged.connect(self._on_modified)

        duration_layout.addWidget(self.stand_duration_spin)
        duration_layout.addStretch()

        layout.addWidget(self.stand_enabled_cb)
        layout.addLayout(interval_layout)
        layout.addLayout(duration_layout)

        group.setLayout(layout)
        return group

    def _create_exercise_settings(self) -> QGroupBox:
        """创建微运动提醒设置"""
        group = QGroupBox("微运动提醒")
        layout = QVBoxLayout()

        # 启用复选框
        self.exercise_enabled_cb = QCheckBox("启用微运动提醒")
        self.exercise_enabled_cb.stateChanged.connect(self._on_modified)

        # 间隔范围
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("间隔范围："))

        self.exercise_interval_min_spin = QSpinBox()
        self.exercise_interval_min_spin.setRange(5, 120)
        self.exercise_interval_min_spin.setSuffix(" 分钟")
        self.exercise_interval_min_spin.valueChanged.connect(self._on_modified)

        interval_layout.addWidget(self.exercise_interval_min_spin)
        interval_layout.addWidget(QLabel("-"))

        self.exercise_interval_max_spin = QSpinBox()
        self.exercise_interval_max_spin.setRange(5, 180)
        self.exercise_interval_max_spin.setSuffix(" 分钟")
        self.exercise_interval_max_spin.valueChanged.connect(self._on_modified)

        interval_layout.addWidget(self.exercise_interval_max_spin)
        interval_layout.addStretch()

        # 每次动作数范围
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("每次动作数："))

        self.exercise_count_min_spin = QSpinBox()
        self.exercise_count_min_spin.setRange(1, 10)
        self.exercise_count_min_spin.setSuffix(" -")
        self.exercise_count_min_spin.valueChanged.connect(self._on_modified)

        count_layout.addWidget(self.exercise_count_min_spin)

        self.exercise_count_max_spin = QSpinBox()
        self.exercise_count_max_spin.setRange(1, 20)
        self.exercise_count_max_spin.valueChanged.connect(self._on_modified)

        count_layout.addWidget(self.exercise_count_max_spin)
        count_layout.addWidget(QLabel(" 个"))
        count_layout.addStretch()

        layout.addWidget(self.exercise_enabled_cb)
        layout.addLayout(interval_layout)
        layout.addLayout(count_layout)

        group.setLayout(layout)
        return group

    def _create_gaze_settings(self) -> QGroupBox:
        """创建强制远眺提醒设置"""
        group = QGroupBox("强制远眺提醒")
        layout = QVBoxLayout()

        # 启用复选框
        self.gaze_enabled_cb = QCheckBox("启用强制远眺提醒")
        self.gaze_enabled_cb.stateChanged.connect(self._on_modified)

        # 间隔范围
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("间隔范围："))

        self.gaze_interval_min_spin = QSpinBox()
        self.gaze_interval_min_spin.setRange(5, 120)
        self.gaze_interval_min_spin.setSuffix(" 分钟")
        self.gaze_interval_min_spin.valueChanged.connect(self._on_modified)

        interval_layout.addWidget(self.gaze_interval_min_spin)
        interval_layout.addWidget(QLabel("-"))

        self.gaze_interval_max_spin = QSpinBox()
        self.gaze_interval_max_spin.setRange(5, 180)
        self.gaze_interval_max_spin.setSuffix(" 分钟")
        self.gaze_interval_max_spin.valueChanged.connect(self._on_modified)

        interval_layout.addWidget(self.gaze_interval_max_spin)
        interval_layout.addStretch()

        # 倒计时时长
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("倒计时时长："))

        self.gaze_duration_spin = QSpinBox()
        self.gaze_duration_spin.setRange(10, 120)
        self.gaze_duration_spin.setSuffix(" 秒")
        self.gaze_duration_spin.valueChanged.connect(self._on_modified)

        duration_layout.addWidget(self.gaze_duration_spin)
        duration_layout.addStretch()

        layout.addWidget(self.gaze_enabled_cb)
        layout.addLayout(interval_layout)
        layout.addLayout(duration_layout)

        group.setLayout(layout)
        return group

    def _create_exercise_tab(self) -> QWidget:
        """创建动作库页面"""
        from .exercise_library import ExerciseLibraryWidget

        # 使用动作库管理组件
        widget = ExerciseLibraryWidget()
        widget.data_changed.connect(self._on_exercise_data_changed)

        return widget

    def _on_exercise_data_changed(self):
        """动作数据已更改"""
        self.modified = True

    def _create_audio_tab(self) -> QWidget:
        """创建音频设置页面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # 启用音频
        self.audio_enabled_cb = QCheckBox("启用音效")
        self.audio_enabled_cb.setChecked(True)
        self.audio_enabled_cb.stateChanged.connect(self._on_modified)

        # 音量
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("音量："))

        self.volume_spin = QDoubleSpinBox()
        self.volume_spin.setRange(0.0, 1.0)
        self.volume_spin.setSingleStep(0.1)
        self.volume_spin.setValue(0.7)
        self.volume_spin.setSuffix(" (0.0-1.0)")
        self.volume_spin.valueChanged.connect(self._on_modified)

        volume_layout.addWidget(self.volume_spin)
        volume_layout.addStretch()

        # TTS 设置
        tts_group = QGroupBox("语音播报（TTS）")
        tts_layout = QVBoxLayout()

        self.tts_enabled_cb = QCheckBox("启用最后5秒语音倒计时")
        self.tts_enabled_cb.setToolTip("需要配置 TTS API")
        self.tts_enabled_cb.stateChanged.connect(self._on_modified)

        # TTS API 地址
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("TTS API 地址："))

        from PySide6.QtWidgets import QLineEdit
        self.tts_api_input = QLineEdit()
        self.tts_api_input.setPlaceholderText("https://example.com/tts/api")
        self.tts_api_input.textChanged.connect(self._on_modified)

        api_layout.addWidget(self.tts_api_input)

        tts_layout.addWidget(self.tts_enabled_cb)
        tts_layout.addLayout(api_layout)

        tts_group.setLayout(tts_layout)

        layout.addWidget(self.audio_enabled_cb)
        layout.addLayout(volume_layout)
        layout.addWidget(tts_group)
        layout.addStretch()

        return widget

    def _create_user_tab(self) -> QWidget:
        """创建用户设置页面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # 体重设置
        weight_group = QGroupBox("用户信息")
        weight_layout = QVBoxLayout()

        weight_input_layout = QHBoxLayout()
        weight_input_layout.addWidget(QLabel("体重（千克）："))

        from PySide6.QtWidgets import QLineEdit
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("70")
        self.weight_input.textChanged.connect(self._on_modified)

        weight_input_layout.addWidget(self.weight_input)
        weight_input_layout.addStretch()

        # 说明
        hint_label = QLabel("体重用于计算运动消耗的热量")
        hint_label.setStyleSheet("color: #757575; font-size: 11pt;")

        weight_layout.addLayout(weight_input_layout)
        weight_layout.addWidget(hint_label)

        weight_group.setLayout(weight_layout)

        layout.addWidget(weight_group)
        layout.addStretch()

        return widget

    def _load_settings(self):
        """加载设置"""
        # 强制站立提醒
        self.stand_enabled_cb.setChecked(self.config.is_reminder_enabled("stand"))
        self.stand_interval_min_spin.setValue(self.config.get("reminder.stand.interval_min", 30))
        self.stand_interval_max_spin.setValue(self.config.get("reminder.stand.interval_max", 60))
        self.stand_duration_spin.setValue(self.config.get("reminder.stand.duration", 90))

        # 微运动提醒
        self.exercise_enabled_cb.setChecked(self.config.is_reminder_enabled("exercise"))
        self.exercise_interval_min_spin.setValue(self.config.get("reminder.exercise.interval_min", 45))
        self.exercise_interval_max_spin.setValue(self.config.get("reminder.exercise.interval_max", 75))
        self.exercise_count_min_spin.setValue(self.config.get("reminder.exercise.exercises_per_session_min", 3))
        self.exercise_count_max_spin.setValue(self.config.get("reminder.exercise.exercises_per_session_max", 5))

        # 强制远眺提醒
        self.gaze_enabled_cb.setChecked(self.config.is_reminder_enabled("gaze"))
        self.gaze_interval_min_spin.setValue(self.config.get("reminder.gaze.interval_min", 60))
        self.gaze_interval_max_spin.setValue(self.config.get("reminder.gaze.interval_max", 90))
        self.gaze_duration_spin.setValue(self.config.get("reminder.gaze.duration", 20))

        # 音频
        self.audio_enabled_cb.setChecked(self.config.is_audio_enabled())
        self.volume_spin.setValue(self.config.get_audio_volume())
        self.tts_enabled_cb.setChecked(self.config.is_tts_enabled())
        self.tts_api_input.setText(self.config.get("audio.tts_api", ""))

        # 用户
        weight = UserRepository.get_weight()
        self.weight_input.setText(str(weight))

        self.modified = False

    def _apply_settings(self):
        """应用设置"""
        # 强制站立提醒
        self.config.set("reminder.stand.enabled", self.stand_enabled_cb.isChecked())
        self.config.set("reminder.stand.interval_min", self.stand_interval_min_spin.value())
        self.config.set("reminder.stand.interval_max", self.stand_interval_max_spin.value())
        self.config.set("reminder.stand.duration", self.stand_duration_spin.value())

        # 微运动提醒
        self.config.set("reminder.exercise.enabled", self.exercise_enabled_cb.isChecked())
        self.config.set("reminder.exercise.interval_min", self.exercise_interval_min_spin.value())
        self.config.set("reminder.exercise.interval_max", self.exercise_interval_max_spin.value())
        self.config.set("reminder.exercise.exercises_per_session_min", self.exercise_count_min_spin.value())
        self.config.set("reminder.exercise.exercises_per_session_max", self.exercise_count_max_spin.value())

        # 强制远眺提醒
        self.config.set("reminder.gaze.enabled", self.gaze_enabled_cb.isChecked())
        self.config.set("reminder.gaze.interval_min", self.gaze_interval_min_spin.value())
        self.config.set("reminder.gaze.interval_max", self.gaze_interval_max_spin.value())
        self.config.set("reminder.gaze.duration", self.gaze_duration_spin.value())

        # 音频
        self.config.set("audio.enabled", self.audio_enabled_cb.isChecked())
        self.config.set("audio.volume", self.volume_spin.value())
        self.config.set("audio.tts_enabled", self.tts_enabled_cb.isChecked())
        self.config.set("audio.tts_api", self.tts_api_input.text())

        # 用户
        try:
            weight = float(self.weight_input.text())
            UserRepository.set_weight(weight)
        except ValueError:
            pass  # 忽略无效输入

        # 保存配置
        self.config.save()

        self.modified = False
        self.settings_changed.emit()

    def _on_modified(self):
        """设置已修改"""
        self.modified = True
