# -*- coding: utf-8 -*-
"""
微运动提醒弹窗

显示动作名称和倒计时 - 有标题栏版本（按设计文档5.2节）
"""
from PySide6.QtWidgets import QLabel, QVBoxLayout, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor
from .base_dialog import BaseReminderDialog
from ...utils.met_calculator import METCalculator
from ...models.repositories import ActivityRepository


class ExerciseReminderDialog(BaseReminderDialog):
    """
    微运动提醒弹窗

    显示动作名称和倒计时 - 有标题栏（设计文档5.2节要求）
    """

    def __init__(self, exercises: list, weight_kg: float = 70.0, parent=None):
        """
        初始化微运动弹窗

        Args:
            exercises: 动作列表 [{"id", "name", "duration", "met"}, ...]
            weight_kg: 用户体重（千克）
            parent: 父窗口
        """
        self.exercises = exercises
        self.current_index = 0
        self.weight_kg = weight_kg

        # 获取当前动作
        self.current_exercise = exercises[0] if exercises else {"name": "深蹲", "duration": 30, "met": 5.0}
        self.duration = self.current_exercise.get('duration', self.current_exercise.get('duration_seconds', 30))

        # 传入 has_title_bar=True - 设计文档5.2节要求有标题栏
        super().__init__(parent, has_title_bar=True)

        # 设置窗口标题（显示在系统标题栏）
        self.setWindowTitle(f"🏃 {self.current_exercise['name']}")

        # 设置固定大小（设计文档要求：800 x 600 px）
        self.setFixedSize(800, 600)

        # UI 组件
        self.countdown_label = None
        self.hint_label = None
        self.met_label = None

        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 创建主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 40)  # 减少顶部边距因为有标题栏
        layout.setSpacing(20)

        # MET 值显示
        self.met_label = QLabel(f"MET: {self.current_exercise.get('met', 5.0)}")
        self.met_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.met_label.setStyleSheet("font-size: 14pt; color: #757575;")
        layout.addWidget(self.met_label)

        # 倒计时（移除自定义标题，使用系统标题栏）
        self.countdown_label = QLabel()
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        countdown_font = QFont("Consolas", 96, QFont.Weight.Bold)
        self.countdown_label.setFont(countdown_font)
        layout.addWidget(self.countdown_label)

        layout.addStretch(1)

        # 提示
        self.hint_label = QLabel("请完成该动作，等待倒计时结束")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_font = QFont("Microsoft YaHei UI", 16)
        self.hint_label.setFont(hint_font)
        self.hint_label.setStyleSheet("color: #757575;")
        layout.addWidget(self.hint_label)

        self.setLayout(layout)

    def showEvent(self, event):
        """
        窗口显示事件 - 自动启动倒计时
        """
        super().showEvent(event)
        # 自动启动倒计时
        print(f"[DEBUG] 开始微运动倒计时: {self.current_exercise['name']}, 时长={self.duration}秒")
        self.start_countdown(self.duration)

    def _apply_styles(self):
        """应用样式"""
        # 设置样式表
        self.setStyleSheet("""
            ExerciseReminderDialog {
                background-color: #FFFFFF;
            }
        """)

    def _update_countdown_display(self):
        """更新倒计时显示"""
        mins, secs = divmod(self.remaining_seconds, 60)

        # 使用统一的倒计时颜色方案
        color = self.get_countdown_color(self.remaining_seconds, self.duration)

        self.countdown_label.setStyleSheet(
            f"QLabel {{ color: {color}; }}"
        )

        # 更新显示文本
        self.countdown_label.setText(f"{mins:02d}:{secs:02d}")

    def _show_complete_feedback(self):
        """显示完成反馈（显示热量消耗）"""
        # 计算热量消耗
        calories = METCalculator.calculate_calories_by_exercise(
            self.current_exercise.get('met', 5.0),
            self.duration,
            self.weight_kg
        )

        # 显示完成反馈 + 热量消耗
        self.countdown_label.setText(f"✅ 完成！\n消耗 {calories:.1f} 千卡")
        self.countdown_label.setStyleSheet("QLabel { color: #4CAF50; }")

        # 记录完成
        ActivityRepository.log_exercise(self.duration, calories, completed=True)
        print(f"[DEBUG] 完成运动: {self.current_exercise['name']}, 消耗={calories}千卡")

    def skip(self):
        """
        跳过（重写基类方法）

        微运动允许跳过
        """
        # 记录跳过
        ActivityRepository.log_exercise(self.duration, 0, completed=False)
        print(f"[DEBUG] 跳过运动: {self.current_exercise['name']}")

        # 调用基类跳过方法
        super().skip()
