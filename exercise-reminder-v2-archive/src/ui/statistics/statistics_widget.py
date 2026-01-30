# -*- coding: utf-8 -*-
"""
统计界面组件 - 简化版

使用纯Qt组件，避免matplotlib中文字体问题
"""
from datetime import date, datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QScrollArea, QGridLayout,
    QProgressBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ...models.repositories import ActivityRepository


class StatCard(QFrame):
    """统计卡片组件"""
    def __init__(self, title: str, value: str, unit: str = "", color: str = "#4CAF50", parent=None):
        super().__init__(parent)
        self.setup_ui(title, value, unit, color)

    def setup_ui(self, title: str, value: str, unit: str, color: str):
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 16px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 11pt;")
        layout.addWidget(title_label)

        value_label = QLabel(f"{value} {unit}")
        value_label.setStyleSheet("color: #FFFFFF; font-size: 20pt; font-weight: bold;")
        layout.addWidget(value_label)

        layout.addStretch()
        self.setLayout(layout)

    def update_value(self, value: str, unit: str = ""):
        # 查找并更新第二个标签（数值标签）
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, QLabel) and widget.text().count(' ') > 0:
                    widget.setText(f"{value} {unit}")
                    break


class SimpleBarChart(QWidget):
    """简单的条形图组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bars = []
        self.labels = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 标题
        self.title_label = QLabel("今日活动统计")
        self.title_label.setFont(QFont("Microsoft YaHei UI", 12, QFont.Weight.Bold))
        layout.addWidget(self.title_label)

        # 条形图容器
        self.bars_container = QWidget()
        self.bars_layout = QVBoxLayout(self.bars_container)
        self.bars_layout.setSpacing(12)
        layout.addWidget(self.bars_container)

        layout.addStretch()
        self.setLayout(layout)

    def update_data(self, stats: dict):
        """更新数据"""
        # 清空现有条形
        while self.bars_layout.count():
            item = self.bars_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 数据
        data = [
            ("站立", stats.get('stand_count', 0), stats.get('stand_duration', 0) // 60, "#4CAF50"),
            ("运动", stats.get('exercise_count', 0), stats.get('exercise_duration', 0) // 60, "#2196F3"),
            ("远眺", stats.get('gaze_count', 0), stats.get('gaze_duration', 0) // 60, "#FF9800"),
        ]

        max_count = max((d[1] for d in data), default=1)

        for name, count, duration, color in data:
            # 行容器
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(10)

            # 标签
            label = QLabel(name)
            label.setFixedWidth(50)
            label.setStyleSheet("font-size: 11pt;")
            row_layout.addWidget(label)

            # 进度条背景
            bg = QFrame()
            bg.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
            bg.setStyleSheet("background-color: #E0E0E0; border-radius: 3px;")
            bg.setFixedHeight(24)

            # 进度条前景
            bar = QFrame(bg)
            bar.setStyleSheet(f"background-color: {color}; border-radius: 3px;")
            width = int((count / max_count * 100)) if max_count > 0 else 0
            bar.setFixedWidth(max(width, 2))  # 至少显示一点

            # 文字
            text = QLabel(f"  {count}次 ({duration}分钟)")
            text.setStyleSheet("font-size: 10pt; color: #555;")
            row_layout.addWidget(text)

            row_layout.addStretch()
            self.bars_layout.addWidget(row)


class SimpleTrendChart(QWidget):
    """简单的趋势图组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 标题
        self.title_label = QLabel("近7天热量消耗")
        self.title_label.setFont(QFont("Microsoft YaHei UI", 12, QFont.Weight.Bold))
        layout.addWidget(self.title_label)

        # 趋势数据容器
        self.trend_container = QWidget()
        self.trend_layout = QHBoxLayout(self.trend_container)
        self.trend_layout.setSpacing(8)
        self.trend_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.trend_container)

        layout.addStretch()
        self.setLayout(layout)

    def update_data(self, data: list):
        """更新数据"""
        # 清空现有组件
        while self.trend_layout.count():
            item = self.trend_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not data:
            no_data = QLabel("暂无数据")
            no_data.setStyleSheet("color: #999999; font-style: italic;")
            self.trend_layout.addWidget(no_data)
            return

        max_calories = max((d["calories"] for d in data), default=1)

        for item in data:
            # 每天的数据
            day_widget = QWidget()
            day_layout = QVBoxLayout(day_widget)
            day_layout.setSpacing(4)
            day_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # 日期
            date_label = QLabel(item["date"])
            date_label.setStyleSheet("font-size: 9pt; color: #666;")
            date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_layout.addWidget(date_label)

            # 条形
            height = int((item["calories"] / max_calories * 80)) if max_calories > 0 else 0
            bar = QFrame()
            bar.setFixedWidth(30)
            bar.setFixedHeight(max(height, 3))  # 至少3像素
            bar.setStyleSheet("background-color: #4CAF50; border-radius: 3px;")
            day_layout.addWidget(bar)

            # 热量值
            calories_label = QLabel(f"{int(item['calories'])}")
            calories_label.setStyleSheet("font-size: 9pt; color: #555;")
            calories_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_layout.addWidget(calories_label)

            self.trend_layout.addWidget(day_widget)


class RecentActivityList(QFrame):
    """最近活动列表"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("最近活动")
        title.setFont(QFont("Microsoft YaHei UI", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(8)
        self.container_layout.addStretch()

        scroll.setWidget(self.container)
        layout.addWidget(scroll)

        self.setLayout(layout)

    def update_data(self, activities: list):
        """更新活动列表"""
        while self.container_layout.count() > 1:
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for activity in activities[:10]:
            item = self._create_activity_item(activity)
            self.container_layout.insertWidget(0, item)

    def _create_activity_item(self, activity) -> QFrame:
        """创建活动项"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 4px;
                padding: 10px;
            }
        """)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)

        # 图标
        type_icons = {'stand': '🧍', 'exercise': '🏃', 'gaze': '👀'}
        icon_label = QLabel(type_icons.get(activity.activity_type, '📋'))
        icon_label.setStyleSheet("font-size: 18pt;")
        layout.addWidget(icon_label)

        # 信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        type_names = {'stand': '站立', 'exercise': '运动', 'gaze': '远眺'}
        name_label = QLabel(type_names.get(activity.activity_type, activity.activity_type))
        name_label.setStyleSheet("font-size: 10pt; font-weight: bold;")
        info_layout.addWidget(name_label)

        time_text = activity.timestamp.strftime("%H:%M")
        detail_label = QLabel(f"{time_text} · {activity.duration_seconds}秒")
        detail_label.setStyleSheet("font-size: 9pt; color: #757575;")
        info_layout.addWidget(detail_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        return frame


class StatisticsWidget(QWidget):
    """统计界面主组件 - 简化版"""

    data_refreshed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # 标题
        title_label = QLabel("活动统计")
        title_font = QFont("Microsoft YaHei UI", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # 今日统计卡片
        cards_widget = QWidget()
        cards_layout = QGridLayout(cards_widget)
        cards_layout.setSpacing(12)

        self.stand_count_card = StatCard("今日站立", "0", "次", "#4CAF50")
        self.stand_duration_card = StatCard("站立时长", "0", "分钟", "#8BC34A")
        self.exercise_count_card = StatCard("今日运动", "0", "次", "#2196F3")
        self.exercise_calories_card = StatCard("消耗热量", "0", "千卡", "#03A9F4")
        self.gaze_count_card = StatCard("今日远眺", "0", "次", "#FF9800")

        cards_layout.addWidget(self.stand_count_card, 0, 0)
        cards_layout.addWidget(self.stand_duration_card, 0, 1)
        cards_layout.addWidget(self.exercise_count_card, 0, 2)
        cards_layout.addWidget(self.exercise_calories_card, 1, 0)
        cards_layout.addWidget(self.gaze_count_card, 1, 1)

        main_layout.addWidget(cards_widget)

        # 活动统计图表
        self.activity_chart = SimpleBarChart()
        main_layout.addWidget(self.activity_chart)

        # 热量趋势图表
        self.calorie_chart = SimpleTrendChart()
        main_layout.addWidget(self.calorie_chart)

        # 最近活动列表
        self.recent_list = RecentActivityList()
        main_layout.addWidget(self.recent_list, 1)

        self.setLayout(main_layout)

    def refresh_data(self):
        """刷新数据"""
        today_stats = ActivityRepository.get_today_stats()

        self.stand_count_card.update_value(str(today_stats['stand_count']), "次")
        self.stand_duration_card.update_value(str(today_stats['stand_duration'] // 60), "分钟")
        self.exercise_count_card.update_value(str(today_stats['exercise_count']), "次")
        self.exercise_calories_card.update_value(f"{today_stats['exercise_calories']:.0f}", "千卡")
        self.gaze_count_card.update_value(str(today_stats['gaze_count']), "次")

        self.activity_chart.update_data(today_stats)

        calorie_data = ActivityRepository.get_calories_last_7_days()
        self.calorie_chart.update_data(list(reversed(calorie_data)))

        recent_activities = ActivityRepository.get_recent_activities(10)
        self.recent_list.update_data(recent_activities)

        self.data_refreshed.emit()

    def refresh(self):
        self.refresh_data()
