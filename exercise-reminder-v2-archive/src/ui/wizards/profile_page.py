# -*- coding: utf-8 -*-
"""
个人信息页面 - 首次启动向导第1页

呼吸感设计 - 柔和有机主义风格
"""
from PySide6.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDoubleSpinBox, QFrame, QGridLayout,
    QRadioButton, QButtonGroup, QWidget
)
from PySide6.QtCore import Qt, Signal
from ..design.tokens import DesignTokens


class ProfilePage(QWizardPage):
    """个人信息设置页面 - 呼吸感设计"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("个人基础设置")
        self.setSubTitle("定制您的健康计划")

        # UI 组件引用
        self.height_input = None
        self.weight_input = None
        self.age_input = None
        self.gender_input = None  # 性别选择
        self.male_radio = None  # 男性单选按钮引用
        self.female_radio = None  # 女性单选按钮引用
        self._selected_gender = "male"  # 默认男性

        self.setup_ui()

        # 注册字段
        self.registerField("height*", self.height_input)
        self.registerField("weight*", self.weight_input)
        self.registerField("age*", self.age_input)
        # 注册性别字段 - 使用male按钮的checked状态
        self.registerField("gender", self.male_radio, "checked", "toggled")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(24)

        # 输入卡片网格
        input_grid = self._create_input_grid()
        layout.addWidget(input_grid)

        layout.addStretch()
        self.setLayout(layout)

    def _create_input_grid(self) -> QFrame:
        """创建输入卡片网格"""
        grid_container = QFrame()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setSpacing(20)

        # 第一行：身高、体重、年龄、性别
        row1_fields = [
            {
                "icon": "📏",
                "label": "身高",
                "value": 170,
                "min": 100,
                "max": 250,
                "suffix": " cm",
                "input": None
            },
            {
                "icon": "⚖️",
                "label": "体重",
                "value": 70.0,
                "min": 30.0,
                "max": 200.0,
                "suffix": " kg",
                "input": None,
                "is_double": True
            },
            {
                "icon": "🎂",
                "label": "年龄",
                "value": 30,
                "min": 10,
                "max": 100,
                "suffix": " 岁",
                "input": None
            },
        ]

        for i, field in enumerate(row1_fields):
            card = self._create_input_card(field)
            row1_fields[i]["input"] = card.findChild(QSpinBox) or card.findChild(QDoubleSpinBox)
            grid_layout.addWidget(card, 0, i)

        # 性别选择卡片（特殊处理）
        gender_card = self._create_gender_card()
        grid_layout.addWidget(gender_card, 0, 3)

        # 保存引用
        self.height_input = row1_fields[0]["input"]
        self.weight_input = row1_fields[1]["input"]
        self.age_input = row1_fields[2]["input"]

        # 连接验证信号
        self.height_input.valueChanged.connect(self.validate_input)
        self.weight_input.valueChanged.connect(self.validate_input)
        self.age_input.valueChanged.connect(self.validate_input)

        # 移除第二行的每日运动目标
        # 根据用户反馈，不显示这一行

        # 均匀分布
        for i in range(4):
            grid_layout.setColumnStretch(i, 1)

        return grid_container

    def _create_input_card(self, field: dict) -> QFrame:
        """创建单个输入卡片 - 增大高度，移除提示文字"""
        card = QFrame()

        # 增大卡片高度以容纳图标和输入框
        if not field.get("full_width"):
            card.setFixedSize(160, 200)  # 从 140x180 增大到 160x200
        else:
            card.setMinimumSize(600, 120)

        card.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border-radius: 12px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 16, 12, 12)  # 增加顶部边距确保图标不被切断
        card_layout.setSpacing(8)

        # 图标 (40pt as per design doc)
        icon_label = QLabel(field["icon"])
        icon_label.setStyleSheet("font-size: 40pt;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)

        # 标签
        label = QLabel(field["label"])
        label.setStyleSheet("font-size: 14pt; font-weight: 600; color: #212121;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(label)

        # 输入框 - 移除上下按钮
        if field.get("is_double"):
            input_widget = QDoubleSpinBox()
        else:
            input_widget = QSpinBox()

        input_widget.setRange(field["min"], field["max"])
        input_widget.setValue(field["value"])
        input_widget.setSuffix(field["suffix"])
        input_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 移除上下按钮并增大字体
        input_widget.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        input_widget.setStyleSheet("""
            QSpinBox, QDoubleSpinBox {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 8px;
                font-size: 18pt;
                font-weight: 600;
                color: #212121;
            }
            QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #4CAF50;
                background-color: #FFFFFF;
            }
            /* 隐藏上下按钮 */
            QSpinBox::up-button, QSpinBox::down-button,
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                width: 0px;
                border: none;
                background: none;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow,
            QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {
                background: none;
            }
        """)
        card_layout.addWidget(input_widget)

        # 不再添加单位标签和提示文字

        return card

    def _create_gender_card(self) -> QFrame:
        """创建性别选择卡片 - 增大高度，移除提示文字"""
        card = QFrame()
        card.setFixedSize(160, 200)  # 增大高度
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 16, 12, 12)  # 增加顶部边距确保图标不被切断
        card_layout.setSpacing(8)

        # 图标 (40pt as per design doc)
        icon_label = QLabel("👤")
        icon_label.setStyleSheet("font-size: 40pt;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)

        # 标签
        label = QLabel("性别")
        label.setStyleSheet("font-size: 14pt; font-weight: 600; color: #212121;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(label)

        # 性别选择按钮组 - 水平布局
        self.gender_button_group = QButtonGroup(self)

        # 创建水平布局用于性别按钮
        gender_layout = QHBoxLayout()
        gender_layout.setSpacing(8)

        # 男
        self.male_radio = QRadioButton("男")
        self.male_radio.setChecked(True)
        self.male_radio.setStyleSheet("""
            QRadioButton {
                font-size: 13pt;
                color: #212121;
                padding: 4px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        self.male_radio.toggled.connect(lambda checked: checked and self._set_gender("male"))
        self.gender_button_group.addButton(self.male_radio, 0)
        gender_layout.addWidget(self.male_radio)

        # 女
        self.female_radio = QRadioButton("女")
        self.female_radio.setStyleSheet("""
            QRadioButton {
                font-size: 13pt;
                color: #212121;
                padding: 4px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        self.female_radio.toggled.connect(lambda checked: checked and self._set_gender("female"))
        self.gender_button_group.addButton(self.female_radio, 1)
        gender_layout.addWidget(self.female_radio)

        gender_layout.addStretch()
        card_layout.addLayout(gender_layout)

        card_layout.addStretch()

        return card

    def _set_gender(self, gender: str):
        """设置选中的性别"""
        self._selected_gender = gender
        self.genderChanged.emit()

    def get_selected_gender(self) -> str:
        """获取选中的性别"""
        return self._selected_gender

    @property
    def selectedGender(self) -> str:
        """属性：选中的性别（用于向导字段注册）"""
        return self._selected_gender

    @selectedGender.setter
    def selectedGender(self, value: str):
        """设置选中性别"""
        self._set_gender(value)

    genderChanged = Signal()

    def validate_input(self):
        """验证输入并更新完成状态"""
        self.completeChanged.emit()

    def isComplete(self):
        """重写验证逻辑"""
        return (
            100 <= self.height_input.value() <= 250 and
            30 <= self.weight_input.value() <= 200 and
            10 <= self.age_input.value() <= 100
        )
