# -*- coding: utf-8 -*-
"""本周统计图表组件"""
from typing import List, Dict
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import rcParams
from src.models.repositories import ActivityRepository
from src.ui.design.tokens import DesignTokens


# 设置中文字体
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False


class WeeklyChart(QWidget):
    """7日热量消耗趋势图"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_points: List[Dict] = []
        self.setup_ui()

    def setup_ui(self):
        """设置 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建 matplotlib 图形
        self.figure = Figure(figsize=(8, 3), dpi=100)
        self.figure.patch.set_facecolor('#FAFAF8')

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)

    def update_chart(self, data: List[Dict]):
        """更新图表数据"""
        self.data_points = data

        # 清空图表
        self.ax.clear()

        # 提取数据
        dates = [point["date"] for point in reversed(data)]
        calories = [point["calories"] for point in reversed(data)]

        # 绘制折线图
        self.ax.plot(
            dates,
            calories,
            marker='o',
            linewidth=2,
            markersize=6,
            color=DesignTokens.COLOR.PRIMARY_SOLID,
            markerfacecolor=DesignTokens.COLOR.ACCENT,
            markeredgewidth=2,
            markeredgecolor=DesignTokens.COLOR.PRIMARY_SOLID
        )

        # 填充区域
        self.ax.fill_between(
            dates,
            calories,
            alpha=0.2,
            color=DesignTokens.COLOR.PRIMARY_SOLID
        )

        # 设置标题和标签
        self.ax.set_title('7日热量消耗趋势', fontsize=12, fontweight='bold', pad=10)
        self.ax.set_xlabel('日期', fontsize=10)
        self.ax.set_ylabel('热量 (千卡)', fontsize=10)

        # 设置网格
        self.ax.grid(True, alpha=0.3, linestyle='--')

        # 设置背景色
        self.ax.set_facecolor('#FAFAF8')
        self.figure.patch.set_facecolor('#FAFAF8')

        # 添加渐变色背景
        ymax = max(max(calories) * 1.2, 100) if calories else 100
        self.ax.set_ylim(0, ymax)

        # 旋转 x 轴标签
        self.ax.tick_params(axis='x', rotation=0)

        # 刷新画布
        self.canvas.draw()

    def get_data_points(self) -> List[Dict]:
        """获取当前显示的数据点"""
        return self.data_points
