# -*- coding: utf-8 -*-
"""
提醒设置页面 - 首次启动向导第2页

按照设计文档 4.3 节实现：
- 全局设置：统一随机偏移
- 提醒间隔设置：站立、微运动、远眺间隔
- 执行时长设置：站立、微运动、远眺时长
"""
from PySide6.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QFrame, QWidget
)
from PySide6.QtCore import Qt


class ReminderSettingsPage(QWizardPage):
    """提醒设置页面 - 按设计文档实现"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("提醒设置")

        # UI 组件 - 全局设置
        self.global_offset_spin = None

        # UI 组件 - 提醒间隔
        self.stand_interval_spin = None
        self.exercise_interval_spin = None
        self.gaze_interval_spin = None

        # UI 组件 - 执行时长
        self.stand_duration_spin = None
        self.exercise_duration_spin = None
        self.gaze_duration_spin = None

        self.setup_ui()

        # 注册字段
        self.registerField("globalOffset", self.global_offset_spin, "value", "valueChanged")
        self.registerField("standInterval", self.stand_interval_spin, "value", "valueChanged")
        self.registerField("exerciseInterval", self.exercise_interval_spin, "value", "valueChanged")
        self.registerField("gazeInterval", self.gaze_interval_spin, "value", "valueChanged")
        self.registerField("standDuration", self.stand_duration_spin, "value", "valueChanged")
        self.registerField("exerciseDuration", self.exercise_duration_spin, "value", "valueChanged")
        self.registerField("gazeDuration", self.gaze_duration_spin, "value", "valueChanged")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 0, 20, 20)
        layout.setSpacing(16)

        # 全局设置卡片
        global_card = self._create_global_settings_card()
        layout.addWidget(global_card)

        # 提醒间隔设置卡片
        interval_card = self._create_interval_settings_card()
        layout.addWidget(interval_card)

        # 执行时长设置卡片
        duration_card = self._create_duration_settings_card()
        layout.addWidget(duration_card)

        layout.addStretch()
        self.setLayout(layout)

    def _create_card(self, title: str, icon: str) -> QFrame:
        """创建卡片容器"""
        card = QFrame()
        card.setMinimumWidth(550)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(16)

        # 标题和图标
        title_label = QLabel(f"{icon} {title}")
        title_label.setStyleSheet("font-size: 12pt; font-weight: 600; color: #212121; min-height: 22px; padding: 1px 0px;")
        card_layout.addWidget(title_label)

        return card

    def _create_setting_row(self, label_text: str, spinbox: QSpinBox, default: int, suffix: str) -> QHBoxLayout:
        """创建设置行"""
        row = QHBoxLayout()
        row.setSpacing(12)

        label = QLabel(label_text)
        label.setStyleSheet("font-size: 10pt; color: #212121; font-weight: 500; min-height: 20px; padding: 1px 0px;")
        label.setMinimumWidth(200)
        row.addWidget(label)

        # 向左移动SpinBox - 添加固定宽度的spacing而不是stretch
        row.addSpacing(200)

        spinbox.setRange(5, 180)
        spinbox.setValue(default)
        spinbox.setSuffix(f" {suffix}")
        spinbox.setMinimumWidth(100)
        # 调整 SpinBox padding
        spinbox.setStyleSheet("""
            QSpinBox {
                font-size: 12pt;
                font-weight: 600;
                color: #212121;
                padding: 2px 8px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                background-color: #FFFFFF;
                min-height: 20px;
            }
            QSpinBox:focus {
                border: 2px solid #4CAF50;
            }
        """)
        row.addWidget(spinbox)

        return row

    def _create_global_settings_card(self) -> QFrame:
        """创建全局设置卡片"""
        card = self._create_card("全局设置", "⏰")

        # 统一随机偏移
        self.global_offset_spin = QSpinBox()
        offset_row = self._create_setting_row("统一随机偏移", self.global_offset_spin, 15, "分钟")
        card.layout().addLayout(offset_row)

        # 说明文字
        hint_label = QLabel(
            "💡 说明: 所有提醒的实际间隔会在设定值基础上随机增减。"
        )
        hint_label.setStyleSheet("font-size: 10pt; color: #6B6B6B; line-height: 1.5; min-height: 20px; padding: 1px 0px;")
        hint_label.setWordWrap(True)
        card.layout().addWidget(hint_label)

        return card

    def _create_interval_settings_card(self) -> QFrame:
        """创建提醒间隔设置卡片"""
        card = self._create_card("提醒间隔设置", "⏱️")

        # 强制站立间隔
        self.stand_interval_spin = QSpinBox()
        stand_row = self._create_setting_row("强制站立间隔", self.stand_interval_spin, 45, "分钟")
        card.layout().addLayout(stand_row)

        # 微运动间隔
        self.exercise_interval_spin = QSpinBox()
        exercise_row = self._create_setting_row("微运动间隔", self.exercise_interval_spin, 60, "分钟")
        card.layout().addLayout(exercise_row)

        # 强制远眺间隔
        self.gaze_interval_spin = QSpinBox()
        gaze_row = self._create_setting_row("强制远眺间隔", self.gaze_interval_spin, 75, "分钟")
        card.layout().addLayout(gaze_row)

        return card

    def _create_duration_settings_card(self) -> QFrame:
        """创建执行时长设置卡片"""
        card = self._create_card("执行时长设置", "⏳")

        # 强制站立时长
        self.stand_duration_spin = QSpinBox()
        self.stand_duration_spin.setRange(30, 300)
        stand_row = self._create_setting_row("强制站立时长", self.stand_duration_spin, 90, "秒")
        card.layout().addLayout(stand_row)

        # 微运动时长
        self.exercise_duration_spin = QSpinBox()
        self.exercise_duration_spin.setRange(30, 300)
        exercise_row = self._create_setting_row("微运动时长", self.exercise_duration_spin, 120, "秒")
        card.layout().addLayout(exercise_row)

        # 强制远眺时长
        self.gaze_duration_spin = QSpinBox()
        self.gaze_duration_spin.setRange(30, 300)
        gaze_row = self._create_setting_row("强制远眺时长", self.gaze_duration_spin, 60, "秒")
        card.layout().addLayout(gaze_row)

        return card
