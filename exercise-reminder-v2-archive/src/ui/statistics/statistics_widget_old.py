# -*- coding: utf-8 -*-
"""
统计界面组件

显示活动数据和趋势图表
"""
from datetime import date, datetime, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QScrollArea, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

# 先配置 matplotlib，再导入其他模块
import matplotlib
matplotlib.use('QtAgg')

import matplotlib.font_manager as fm
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams

# 找到可用的中文字体
def get_chinese_font():
    """获取可用的中文字体"""
    preferred_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun', 'Microsoft JhengHei']
    available_fonts = set([f.name for f in fm.fontManager.ttflist])

    for font in preferred_fonts:
        if font in available_fonts:
            return font
    return 'DejaVu Sans'  # 回退字体

chinese_font = get_chinese_font()
rcParams['font.sans-serif'] = [chinese_font, 'DejaVu Sans', 'Arial']
rcParams['axes.unicode_minus'] = False
rcParams['figure.dpi'] = 100
rcParams['figure.facecolor'] = 'white'

from ...models.repositories import ActivityRepository

print(f'[Statistics] 使用字体: {chinese_font}')  # 调试信息


class StatCard(QFrame):
    """
    统计卡片组件

    显示单个统计数据
    """

    def __init__(self, title: str, value: str, unit: str = "", color: str = "#4CAF50", parent=None):
        """
        初始化统计卡片

        Args:
            title: 标题
            value: 数值
            unit: 单位
            color: 主题色
            parent: 父窗口
        """
        super().__init__(parent)
        self.setup_ui(title, value, unit, color)

    def setup_ui(self, title: str, value: str, unit: str, color: str):
        """设置UI"""
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

        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 12pt;")
        layout.addWidget(title_label)

        # 数值
        value_label = QLabel(f"{value} {unit}")
        value_label.setStyleSheet("color: #FFFFFF; font-size: 24pt; font-weight: bold;")
        layout.addWidget(value_label)

        layout.addStretch()
        self.setLayout(layout)

    def update_value(self, value: str, unit: str = ""):
        """更新数值"""
        value_label = self.findChild(QLabel)
        if value_label:
            value_label.setText(f"{value} {unit}")


class CalorieChart(FigureCanvas):
    """
    热量趋势图表

    显示最近7天的热量消耗趋势
    """

    def __init__(self, parent=None):
        """初始化图表"""
        self.figure = Figure(figsize=(8, 3), dpi=100)
        self.figure.patch.set_facecolor('#FFFFFF')
        super().__init__(self.figure)
        self.setParent(parent)

        self.ax = self.figure.add_subplot(111)
        self._setup_chart()

    def _setup_chart(self):
        """设置图表"""
        self.ax.set_facecolor('#FAFAFA')
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def update_data(self, data: list):
        """
        更新图表数据

        Args:
            data: [{"date": "MM-DD", "calories": float}, ...]
        """
        self.ax.clear()
        self._setup_chart()

        if not data:
            # 无数据显示提示
            self.ax.text(0.5, 0.5, '暂无数据', ha='center', va='center',
                       fontsize=14, color='#999999', style='italic',
                       transform=self.ax.transAxes)
            self.ax.set_title('近7天热量消耗趋势', fontsize=12, fontweight='bold', pad=15)
            self.figure.tight_layout()
            self.draw()
            return

        dates = [item["date"] for item in data]
        calories = [item["calories"] for item in data]

        # 绘制折线图
        self.ax.plot(dates, calories, marker='o', linewidth=2, markersize=6, color='#4CAF50')

        # 填充区域
        self.ax.fill_between(dates, 0, calories, alpha=0.2, color='#4CAF50')

        # 设置标签
        self.ax.set_xlabel('日期', fontsize=10)
        self.ax.set_ylabel('热量（千卡）', fontsize=10)
        self.ax.set_title('近7天热量消耗趋势', fontsize=12, fontweight='bold', pad=15)

        # 旋转x轴标签
        self.ax.tick_params(axis='x', rotation=0)

        # 设置y轴从0开始，并给一些顶部空间
        max_calories = max(calories) if calories else 10
        self.ax.set_ylim(bottom=0, top=max(max_calories * 1.2, 10))

        self.figure.tight_layout()
        self.draw()


class ActivityChart(FigureCanvas):
    """
    活动统计图表

    显示今日各类活动的统计
    """

    def __init__(self, parent=None):
        """初始化图表"""
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.figure.patch.set_facecolor('#FFFFFF')
        super().__init__(self.figure)
        self.setParent(parent)

        self.ax = self.figure.add_subplot(111)
        self._setup_chart()

    def _setup_chart(self):
        """设置图表"""
        self.ax.set_facecolor('#FAFAFA')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.axis('off')

    def update_data(self, stats: dict):
        """
        更新图表数据

        Args:
            stats: 今日统计数据
        """
        self.ax.clear()
        self.ax.axis('off')

        # 准备数据
        categories = ['站立', '运动', '远眺']
        counts = [
            stats.get('stand_count', 0),
            stats.get('exercise_count', 0),
            stats.get('gaze_count', 0)
        ]
        durations = [
            stats.get('stand_duration', 0) // 60,  # 转换为分钟
            stats.get('exercise_duration', 0) // 60,
            stats.get('gaze_duration', 0) // 60
        ]
        colors = ['#4CAF50', '#2196F3', '#FF9800']

        # 创建水平条形图
        y_pos = range(len(categories))
        bars = self.ax.barh(y_pos, counts, color=colors, alpha=0.7, height=0.5)

        # 添加数值标签
        for i, (bar, count, duration) in enumerate(zip(bars, counts, durations)):
            width = bar.get_width()
            self.ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2,
                        f'{count}次 ({duration}分钟)',
                        ha='left', va='center', fontsize=11, fontweight='bold')

        # 设置y轴标签
        self.ax.set_yticks(y_pos)
        self.ax.set_yticklabels(categories, fontsize=12)

        # 设置标题
        self.ax.set_title('今日活动统计', fontsize=14, fontweight='bold', pad=20, x=0, ha='left')

        # 调整布局（处理全0情况）
        max_count = max(counts) if counts else 0
        if max_count > 0:
            self.ax.set_xlim(0, max_count * 1.3)
        else:
            self.ax.set_xlim(0, 10)  # 默认范围
            # 显示提示
            self.ax.text(5, 1, '暂无活动数据', ha='center', va='center',
                       fontsize=14, color='#999999', style='italic')

        self.figure.tight_layout()
        self.draw()


class RecentActivityList(QFrame):
    """
    最近活动列表组件

    显示最近的活动记录
    """

    def __init__(self, parent=None):
        """初始化组件"""
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
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

        # 标题
        title = QLabel("最近活动")
        title.setFont(QFont("Microsoft YaHei UI", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # 滚动区域
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
        """
        更新活动列表

        Args:
            activities: ActivityLog 列表
        """
        # 清空现有内容
        while self.container_layout.count() > 1:
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 添加新活动
        for activity in activities[:10]:  # 最多显示10条
            item = self._create_activity_item(activity)
            self.container_layout.insertWidget(0, item)  # 插入到顶部

    def _create_activity_item(self, activity) -> QFrame:
        """创建活动项"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 4px;
                padding: 8px;
            }
        """)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)

        # 活动类型图标
        type_icons = {
            'stand': '🧍',
            'exercise': '🏃',
            'gaze': '👀'
        }
        type_names = {
            'stand': '站立',
            'exercise': '运动',
            'gaze': '远眺'
        }

        icon_label = QLabel(type_icons.get(activity.activity_type, '📋'))
        icon_label.setStyleSheet("font-size: 20pt;")
        layout.addWidget(icon_label)

        # 活动信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        name_label = QLabel(type_names.get(activity.activity_type, activity.activity_type))
        name_label.setStyleSheet("font-size: 11pt; font-weight: bold;")
        info_layout.addWidget(name_label)

        time_text = activity.timestamp.strftime("%H:%M")
        if activity.activity_type == 'exercise':
            calories_text = f" · {activity.calories_burned:.0f} 千卡" if activity.completed else " · 已跳过"
            detail_label = QLabel(f"{time_text} · {activity.duration_seconds}秒{calories_text}")
        else:
            detail_label = QLabel(f"{time_text} · {activity.duration_seconds}秒")
        detail_label.setStyleSheet("font-size: 10pt; color: #757575;")
        info_layout.addWidget(detail_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        return frame


class StatisticsWidget(QWidget):
    """
    统计界面主组件

    显示所有统计数据和图表
    """

    # 信号：数据已刷新
    data_refreshed = Signal()

    def __init__(self, parent=None):
        """初始化组件"""
        super().__init__(parent)
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        """设置UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 标题
        title_label = QLabel("活动统计")
        title_font = QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # 今日统计卡片
        self.cards_layout = QGridLayout()
        self.cards_layout.setSpacing(15)
        main_layout.addLayout(self.cards_layout)

        # 创建统计卡片
        self.stand_count_card = StatCard("今日站立", "0", "次", "#4CAF50")
        self.stand_duration_card = StatCard("站立时长", "0", "分钟", "#8BC34A")
        self.exercise_count_card = StatCard("今日运动", "0", "次", "#2196F3")
        self.exercise_calories_card = StatCard("消耗热量", "0", "千卡", "#03A9F4")
        self.gaze_count_card = StatCard("今日远眺", "0", "次", "#FF9800")

        self.cards_layout.addWidget(self.stand_count_card, 0, 0)
        self.cards_layout.addWidget(self.stand_duration_card, 0, 1)
        self.cards_layout.addWidget(self.exercise_count_card, 0, 2)
        self.cards_layout.addWidget(self.exercise_calories_card, 1, 0)
        self.cards_layout.addWidget(self.gaze_count_card, 1, 1)

        # 活动统计图表
        self.activity_chart = ActivityChart()
        chart_container = QWidget()
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.addWidget(self.activity_chart)
        main_layout.addWidget(chart_container)

        # 热量趋势图表
        self.calorie_chart = CalorieChart()
        trend_container = QWidget()
        trend_layout = QVBoxLayout(trend_container)
        trend_layout.setContentsMargins(0, 0, 0, 0)
        trend_layout.addWidget(self.calorie_chart)
        main_layout.addWidget(trend_container)

        # 最近活动列表
        self.recent_list = RecentActivityList()
        main_layout.addWidget(self.recent_list, 1)

        self.setLayout(main_layout)

    def refresh_data(self):
        """刷新所有数据"""
        # 获取今日统计
        today_stats = ActivityRepository.get_today_stats()

        # 更新统计卡片
        self.stand_count_card.update_value(str(today_stats['stand_count']), "次")
        self.stand_duration_card.update_value(str(today_stats['stand_duration'] // 60), "分钟")
        self.exercise_count_card.update_value(str(today_stats['exercise_count']), "次")
        self.exercise_calories_card.update_value(f"{today_stats['exercise_calories']:.0f}", "千卡")
        self.gaze_count_card.update_value(str(today_stats['gaze_count']), "次")

        # 更新活动图表
        self.activity_chart.update_data(today_stats)

        # 更新热量趋势
        calorie_data = ActivityRepository.get_calories_last_7_days()
        self.calorie_chart.update_data(list(reversed(calorie_data)))  # 按时间正序显示

        # 更新最近活动列表
        recent_activities = ActivityRepository.get_recent_activities(10)
        self.recent_list.update_data(recent_activities)

        self.data_refreshed.emit()

    def refresh(self):
        """刷新数据（供外部调用）"""
        self.refresh_data()
