# Statistics Page Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build statistics page with today's metrics cards and 7-day calorie trend chart

**Architecture:** Create new statistics module with StatsView (today's cards) and WeeklyChart (matplotlib integration). Data layer already complete via ActivityRepository.

**Tech Stack:** PySide6, matplotlib 3.8.0, Peewee ORM, DesignTokens styling

---

## Task 1: Create Statistics Module Directory Structure

**Files:**
- Create: `src/ui/statistics/__init__.py`
- Create: `src/ui/statistics/stats_view.py`
- Create: `src/ui/statistics/weekly_chart.py`

**Step 1: Create module __init__.py**

```python
# src/ui/statistics/__init__.py
# -*- coding: utf-8 -*-
"""统计页面模块"""
from .stats_view import StatisticsView

__all__ = ["StatisticsView"]
```

**Step 2: Verify directory structure**

Run: `ls -la src/ui/statistics/`
Expected: Shows `__init__.py`, `stats_view.py`, `weekly_chart.py`

**Step 3: Commit**

```bash
git add src/ui/statistics/
git commit -m "feat: create statistics module structure"
```

---

## Task 2: Write Tests for Today's Stats Cards

**Files:**
- Create: `tests/test_statistics_view.py`

**Step 1: Write failing test for today's stats display**

```python
# tests/test_statistics_view.py
# -*- coding: utf-8 -*-
import pytest
from datetime import date, datetime
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.ui.statistics.stats_view import StatisticsView
from src.models.repositories import ActivityRepository
from src.models.models import ActivityLog, initialize_db


@pytest.fixture
def app(qtbot):
    """创建 QApplication"""
    return QApplication.instance() or QApplication([])


@pytest.fixture
def db(tmp_path):
    """创建临时数据库"""
    db_path = tmp_path / "test.db"
    initialize_db(db_path)
    yield db_path


@pytest.fixture
def view(app, db):
    """创建统计视图"""
    return StatisticsView()


def test_today_stats_shows_calories(view, db):
    """测试今日统计显示热量消耗"""
    # Arrange: 创建今日活动数据
    ActivityLog.create(
        activity_type="exercise",
        duration_seconds=60,
        calories_burned=5.0,
        completed=True,
        timestamp=datetime.now()
    )

    # Act: 刷新统计
    view.refresh_data()

    # Assert: 验证显示热量
    assert view.calories_label.text() == "5.0 kcal"


def test_today_stats_shows_count(view, db):
    """测试今日统计显示完成次数"""
    # Arrange: 创建3个活动
    for _ in range(3):
        ActivityLog.create(
            activity_type="stand",
            duration_seconds=90,
            calories_burned=0,
            completed=True,
            timestamp=datetime.now()
        )

    # Act: 刷新统计
    view.refresh_data()

    # Assert: 验证显示次数
    assert "3" in view.count_label.text()


def test_today_stats_shows_duration(view, db):
    """测试今日统计显示总时长"""
    # Arrange: 创建不同时长的活动
    ActivityLog.create(activity_type="stand", duration_seconds=90, calories_burned=0, completed=True, timestamp=datetime.now())
    ActivityLog.create(activity_type="exercise", duration_seconds=45, calories_burned=3.0, completed=True, timestamp=datetime.now())

    # Act: 刷新统计
    view.refresh_data()

    # Assert: 验证显示时长 (135秒 = 2.25分钟)
    assert "2" in view.duration_label.text()  # 显示分钟数
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_statistics_view.py -v`
Expected: FAIL with "StatisticsView not defined" or "AttributeError"

**Step 3: Commit test file**

```bash
git add tests/test_statistics_view.py
git commit -m "test: add statistics view tests"
```

---

## Task 3: Implement Today's Stats Cards UI

**Files:**
- Modify: `src/ui/statistics/stats_view.py`

**Step 1: Write minimal implementation to pass tests**

```python
# src/ui/statistics/stats_view.py
# -*- coding: utf-8 -*-
"""今日统计视图组件"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel
from PySide6.QtCore import Qt
from src.models.repositories import ActivityRepository
from src.models.models import ActivityLog
from src.ui.design.tokens import DesignTokens


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


class StatisticsView(QWidget):
    """统计页面主视图"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calories_label = None
        self.count_label = None
        self.duration_label = None
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
        layout.addStretch()

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
```

**Step 2: Run test to verify it passes**

Run: `pytest tests/test_statistics_view.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add src/ui/statistics/stats_view.py
git commit -m "feat: implement today's stats cards UI"
```

---

## Task 4: Write Tests for Weekly Chart

**Files:**
- Modify: `tests/test_statistics_view.py`

**Step 1: Add failing test for weekly chart**

```python
# Add to tests/test_statistics_view.py

def test_weekly_chart_displays_7_days(view, db):
    """测试本周图表显示7天数据"""
    # Arrange: 创建过去7天的数据
    for i in range(7):
        target_date = datetime.now().date()
        ActivityLog.create(
            activity_type="exercise",
            duration_seconds=60,
            calories_burned=float(100 + i * 10),
            completed=True,
            timestamp=datetime.combine(target_date, datetime.min.time())
        )

    # Act: 刷新图表
    view.refresh_data()

    # Assert: 验证图表有7个数据点
    assert view.weekly_chart is not None
    assert len(view.weekly_chart.get_data_points()) == 7


def test_weekly_chart_shows_correct_calories(view, db):
    """测试本周图表显示正确热量"""
    # Arrange: 创建特定数据
    ActivityLog.create(
        activity_type="exercise",
        duration_seconds=60,
        calories_burned=185.0,
        completed=True,
        timestamp=datetime.now()
    )

    # Act: 刷新图表
    view.refresh_data()

    # Assert: 验证热量值
    data_points = view.weekly_chart.get_data_points()
    assert any(point["calories"] == 185.0 for point in data_points)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_statistics_view.py::test_weekly_chart_displays_7_days -v`
Expected: FAIL with "AttributeError: 'StatisticsView' object has no attribute 'weekly_chart'"

**Step 3: Commit test additions**

```bash
git add tests/test_statistics_view.py
git commit -m "test: add weekly chart tests"
```

---

## Task 5: Implement Weekly Chart with Matplotlib

**Files:**
- Create: `src/ui/statistics/weekly_chart.py`
- Modify: `src/ui/statistics/stats_view.py`

**Step 1: Create weekly chart widget**

```python
# src/ui/statistics/weekly_chart.py
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

        # 旋转 x 轴标签
        self.ax.tick_params(axis='x', rotation=0)

        # 刷新画布
        self.canvas.draw()

    def get_data_points(self) -> List[Dict]:
        """获取当前显示的数据点"""
        return self.data_points
```

**Step 2: Integrate chart into StatisticsView**

```python
# Add to src/ui/statistics/stats_view.py

# Import at top
from .weekly_chart import WeeklyChart

# Modify setup_ui() method, add after cards_layout:
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

# Modify refresh_data() method, add at end:
        # 更新本周图表
        weekly_data = ActivityRepository.get_calories_last_7_days()
        self.weekly_chart.update_chart(weekly_data)

        # 更新本周统计
        total_weekly = sum(point["calories"] for point in weekly_data)
        avg_daily = total_weekly / 7 if total_weekly > 0 else 0
        self.weekly_stats_label.setText(f"总消耗: {total_weekly:.0f} kcal  |  平均每天: {avg_daily:.0f} kcal")
```

**Step 3: Run tests to verify they pass**

Run: `pytest tests/test_statistics_view.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add src/ui/statistics/weekly_chart.py src/ui/statistics/stats_view.py
git commit -m "feat: implement weekly chart with matplotlib"
```

---

## Task 6: Integrate Statistics Page into Settings Dialog

**Files:**
- Modify: `src/ui/settings/settings_dialog.py`

**Step 1: Add statistics tab to settings dialog**

```python
# Add import at top
from src.ui.statistics.stats_view import StatisticsView

# In SettingsDialog.__init__(), add tab:
# Find where tabs are added, add:
        # 统计页面
        self.stats_view = StatisticsView()
        self.tabs.addTab(self.stats_view, "统计")
```

**Step 2: Write integration test**

```python
# Add to tests/test_statistics_view.py

def test_statistics_in_settings_dialog(app, db):
    """测试统计页面已集成到设置对话框"""
    from src.ui.settings.settings_dialog import SettingsDialog

    dialog = SettingsDialog()

    # Assert: 验证统计标签页存在
    assert dialog.tabs.count() >= 5  # 至少有5个标签页

    # 验证统计标签页可以访问
    stats_tab = dialog.tabs.widget(4)  # 统计是第5个标签
    assert isinstance(stats_tab, StatisticsView)
```

**Step 3: Run integration test**

Run: `pytest tests/test_statistics_view.py::test_statistics_in_settings_dialog -v`
Expected: PASS

**Step 4: Commit**

```bash
git add src/ui/settings/settings_dialog.py tests/test_statistics_view.py
git commit -m "feat: integrate statistics page into settings dialog"
```

---

## Task 7: Style Refinement and Polish

**Files:**
- Modify: `src/ui/statistics/stats_view.py`
- Modify: `src/ui/statistics/weekly_chart.py`

**Step 1: Add card-specific styling**

```python
# Add to TodayStatsCard class in stats_view.py

    def update_value(self, value: str):
        """更新数值显示"""
        self.value_label.setText(value)
```

**Step 2: Add chart animations**

```python
# Modify WeeklyChart.update_chart() to add smooth transitions

# After self.ax.plot(), add:
        # 添加渐变色背景
        self.ax.set_ylim(bottom=0, max(max(calories) * 1.2, 100))
```

**Step 3: Run all tests**

Run: `pytest tests/test_statistics_view.py -v`
Expected: All PASS

**Step 4: Run full test suite**

Run: `pytest tests/ -v`
Expected: All tests pass (including existing 91 tests)

**Step 5: Commit**

```bash
git add src/ui/statistics/
git commit -m "style: polish statistics page styling and animations"
```

---

## Task 8: Final Verification and Documentation

**Step 1: Verify statistics page works end-to-end**

Run: `python -c "from src.ui.statistics.stats_view import StatisticsView; from PySide6.QtWidgets import QApplication; app = QApplication([]); view = StatisticsView(); print('Statistics view created successfully')"`
Expected: No errors, view created

**Step 2: Verify matplotlib integration**

Run: `python -c "import matplotlib; print(f'Matplotlib version: {matplotlib.__version__}')"`
Expected: Matplotlib version: 3.8.x

**Step 3: Run complete test suite**

Run: `pytest tests/ -v --tb=short`
Expected: All tests pass

**Step 4: Update PRD with completion status**

Modify `docs/PRD-v2.0.md`, change "统计页面" from ⏳ to ✅

**Step 5: Final commit**

```bash
git add docs/PRD-v2.0.md
git commit -m "docs: mark statistics page as complete in PRD"
```

---

## Summary

**Total Tasks:** 8
**Estimated Time:** 5-7 hours
**Dependencies:**
- matplotlib 3.8.0 (already in requirements.txt)
- ActivityRepository methods (already implemented)
- DesignTokens (already implemented)

**Key Design Decisions:**
1. Separate StatisticsView and WeeklyChart for modularity
2. matplotlib with Qt5Agg backend for PySide6 integration
3. Today's stats shown as 3 cards (calories, count, duration)
4. Weekly chart shows 7-day trend with fill and markers
5. Integrated into settings dialog as "统计" tab
6. No history table (per user feedback)

**Testing Strategy:**
- Unit tests for each component
- Integration test for settings dialog
- UI verification with pytest-qt
- Full test suite regression check
