# -*- coding: utf-8 -*-
"""
用户信息对话框 - 查看和编辑个人信息

TODO: 实现完整的用户信息功能
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QSpinBox, QButtonGroup, QRadioButton
)
from PySide6.QtCore import Qt
from src.utils.logger import get_logger
from src.models.repositories import UserRepository, SettingRepository

logger = get_logger(__name__)


class UserInfoDialog(QDialog):
    """用户信息对话框 - 占位实现"""

    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("打开用户信息")

        self.setWindowTitle("👤 用户信息")
        self.setMinimumSize(500, 400)

        # UI 组件
        self.height_spin = None
        self.weight_spin = None
        self.age_spin = None
        self.male_radio = None
        self.female_radio = None

        self._setup_ui()
        self._load_user_data()

    def _setup_ui(self):
        """设置 UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # 标题
        title = QLabel("👤 个人信息")
        title.setStyleSheet("font-size: 16pt; font-weight: 600; color: #2C2C2C;")
        layout.addWidget(title)

        # 信息卡片
        card = QFrame()
        card.setStyleSheet("background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E0E0E0;")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)

        # 身高
        height_row = self._create_input_row("身高 (cm):", 100, 250, 170)
        self.height_spin = height_row["spin"]
        card_layout.addLayout(height_row["layout"])

        # 体重
        weight_row = self._create_input_row("体重 (kg):", 30, 200, 70, decimals=1)
        self.weight_spin = weight_row["spin"]
        card_layout.addLayout(weight_row["layout"])

        # 年龄
        age_row = self._create_input_row("年龄:", 10, 100, 30)
        self.age_spin = age_row["spin"]
        card_layout.addLayout(age_row["layout"])

        # 性别
        gender_layout = QHBoxLayout()
        gender_label = QLabel("性别:")
        gender_label.setStyleSheet("font-size: 12pt; color: #2C2C2C;")
        gender_label.setMinimumWidth(100)
        gender_layout.addWidget(gender_label)

        self.male_radio = QRadioButton("男")
        self.female_radio = QRadioButton("女")
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        gender_layout.addStretch()

        card_layout.addLayout(gender_layout)
        layout.addWidget(card)

        # 提示信息
        hint_label = QLabel("💡 提示：修改个人信息后请点击保存")
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

    def _create_input_row(self, label_text: str, min_val: int, max_val: int, default: int, decimals: int = 0) -> dict:
        """创建输入行"""
        layout = QHBoxLayout()

        label = QLabel(label_text)
        label.setStyleSheet("font-size: 12pt; color: #2C2C2C;")
        label.setMinimumWidth(100)
        layout.addWidget(label)

        if decimals == 0:
            spin = QSpinBox()
            spin.setRange(min_val, max_val)
            spin.setValue(default)
        else:
            from PySide6.QtWidgets import QDoubleSpinBox
            spin = QDoubleSpinBox()
            spin.setRange(float(min_val), float(max_val))
            spin.setDecimals(decimals)
            spin.setValue(float(default))

        spin.setMinimumWidth(150)
        spin.setStyleSheet("""
            QSpinBox, QDoubleSpinBox {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 6px;
                font-size: 12pt;
            }
        """)
        layout.addWidget(spin)
        layout.addStretch()

        return {"layout": layout, "spin": spin}

    def _load_user_data(self):
        """加载用户数据"""
        try:
            weight = UserRepository.get_weight()
            height = SettingRepository.get_int("user.height", 170)
            age = SettingRepository.get_int("user.age", 30)
            gender = SettingRepository.get("user.gender", "male")

            self.height_spin.setValue(height)
            self.weight_spin.setValue(weight)
            self.age_spin.setValue(age)

            if gender == "male":
                self.male_radio.setChecked(True)
            else:
                self.female_radio.setChecked(True)

        except Exception as e:
            logger.error(f"加载用户数据失败: {e}")

    def _save_and_close(self):
        """保存并关闭"""
        try:
            from src.utils.bmr_calculator import BMRCalculator, Gender

            height = self.height_spin.value()
            weight = self.weight_spin.value()
            age = self.age_spin.value()
            gender_str = "male" if self.male_radio.isChecked() else "female"

            # 保存到设置
            SettingRepository.set("user.height", str(height))
            SettingRepository.set("user.age", str(age))
            SettingRepository.set("user.gender", gender_str)

            # 计算 BMR
            gender = Gender.MALE if gender_str == "male" else Gender.FEMALE
            bmr = BMRCalculator.calculate_bmr(weight, height, age, gender)
            SettingRepository.set("user.bmr", str(bmr))

            # 保存体重到数据库
            UserRepository.set_weight(weight)

            logger.info(f"用户信息已保存: height={height}, weight={weight}, age={age}")
            self.accept()

        except Exception as e:
            logger.error(f"保存用户信息失败: {e}")

    def accept(self):
        """接受对话框"""
        super().accept()

    def reject(self):
        """拒绝对话框"""
        logger.info("取消用户信息编辑")
        super().reject()
