# -*- coding: utf-8 -*-
"""今日统计视图组件"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel
from PySide6.QtCore import Qt
from src.models.repositories import ActivityRepository
from src.models.models import ActivityLog
from src.ui.design.tokens import DesignTokens
from .weekly_chart import WeeklyChart


class TodayStatsCard(QFrame):
    """今日统计卡片"""

    def __init__(self, icon: str, title: str, value: str, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.Box)
        self.setup_ui(icon, title, value)

    def setup_ui(self, icon: str, title: str, value: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # 图标 + 标题
        header = QLabel(f"{icon} {title}")
        header.setProperty("heading", "true")
        layout.addWidget(header)

        # 数值
        self.value_label = QLabel(value)
        self.value_label.setProperty("heading", "true")
        layout.addWidget(self.value_label)

        # 应用样式
        DesignTokens.apply_stylesheet(self, "card")

    def update_value(self, value: str):
        """更新数值显示"""
        self.value_label.setText(value)


class StatisticsView(QWidget):
    """统计页面主视图"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calories_label = None
        self.count_label = None
        self.duration_label = None
        self.weekly_chart = None
        self.weekly_stats_label = None
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        """设置 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # 今日统计标题
        title = QLabel("今日统计")
        title.setProperty("heading", "true")
        layout.addWidget(title)

        # 三个统计卡片
        cards_layout = QGridLayout()
        cards_layout.setSpacing(16)

        self.calories_card = TodayStatsCard("🔥", "今日消耗", "0 kcal")
        self.count_card = TodayStatsCard("✅", "完成次数", "0 次")
        self.duration_card = TodayStatsCard("⏱️", "总时长", "0 分钟")

        cards_layout.addWidget(self.calories_card, 0, 0)
        cards_layout.addWidget(self.count_card, 0, 1)
        cards_layout.addWidget(self.duration_card, 0, 2)

        layout.addLayout(cards_layout)

        # 本周统计标题
        weekly_title = QLabel("本周统计")
        weekly_title.setProperty("heading", "true")
        layout.addWidget(weekly_title)

        # 本周图表
        self.weekly_chart = WeeklyChart()
        layout.addWidget(self.weekly_chart)

        # 统计信息
        self.weekly_stats_label = QLabel()
        self.weekly_stats_label.setProperty("description", "true")
        layout.addWidget(self.weekly_stats_label)

        # 应用样式
        DesignTokens.apply_stylesheet(self, "all")

        # 保存引用
        self.calories_label = self.calories_card.value_label
        self.count_label = self.count_card.value_label
        self.duration_label = self.duration_card.value_label

    def refresh_data(self):
        """刷新统计数据"""
        stats = ActivityLog.get_today_stats()

        # 计算今日总热量
        total_calories = (
            stats.get("exercise_calories", 0) +
            stats.get("stand_calories", 0) +
            stats.get("gaze_calories", 0)
        )
        self.calories_label.setText(f"{total_calories:.1f} kcal")

        # 计算完成次数
        total_count = (
            stats.get("exercise_count", 0) +
            stats.get("stand_count", 0) +
            stats.get("gaze_count", 0)
        )
        self.count_label.setText(f"{total_count} 次")

        # 计算总时长（转换为分钟）
        total_seconds = (
            stats.get("exercise_duration", 0) +
            stats.get("stand_duration", 0) +
            stats.get("gaze_duration", 0)
        )
        total_minutes = total_seconds / 60
        self.duration_label.setText(f"{total_minutes:.0f} 分钟")

        # 更新本周图表
        weekly_data = ActivityRepository.get_calories_last_7_days()
        self.weekly_chart.update_chart(weekly_data)

        # 更新本周统计
        total_weekly = sum(point["calories"] for point in weekly_data)
        avg_daily = total_weekly / 7 if total_weekly > 0 else 0
        self.weekly_stats_label.setText(f"总消耗: {total_weekly:.0f} kcal  |  平均每天: {avg_daily:.0f} kcal")
