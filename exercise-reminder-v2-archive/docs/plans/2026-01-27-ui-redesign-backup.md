# UI 重构与功能增强实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标:** 重构应用 UI，添加首页主窗口，重新设计首次运行向导和设置页面，去掉惩罚机制，更新配置结构。

**架构:**
- 保持现有分层架构（core/models/ui/utils）
- 新增 `src/ui/home.py` - 首页主窗口组件
- 新增 `src/ui/wizards/reminder_settings_page.py` - 向导提醒设置页
- 新增 `src/ui/wizards/confirm_page.py` - 向导确认页
- 重构 `src/utils/config.py` - 支持新的配置结构
- 移除 `src/core/punishment_logic.py` 及相关惩罚机制

**技术栈:**
- Python 3.10+
- PySide6 (Qt for Python)
- SQLite + Peewee ORM

---

## Task 1: 更新配置结构

**Files:**
- Modify: `src/utils/config.py`
- Modify: `data/config.json` (运行时更新)

**Step 1: 添加新的默认配置**

在 `ConfigManager` 中添加新的默认配置结构：

```python
def _get_default_config(self) -> dict:
    """获取默认配置"""
    return {
        # 全局设置
        "reminder": {
            "global_offset_minutes": 15,  # 统一随机偏移
            "stand": {
                "enabled": True,
                "interval_avg": 45,        # 平均间隔（分钟）
                "duration": 90             # 执行时长（秒）
            },
            "exercise": {
                "enabled": True,
                "interval_avg": 60,
                "duration": 120            # 默认2分钟
            },
            "gaze": {
                "enabled": True,
                "interval_avg": 75,
                "duration": 60
            }
        },
        # 用户信息
        "user": {
            "height": 170,
            "weight": 70.0,
            "age": 30,
            "gender": "male",
            "calorie_target": 500,     # 每天要减的卡路里
            "bmr": 1650                # 基础代谢率
        },
        # 音频设置
        "audio": {
            "enabled": True,
            "volume": 0.7,
            "sound_effect": "electronic_beep",  # 电子哔声
            "sound_file": "",          # 自定义音效文件路径
            "tts_enabled": False,
            "tts_api": ""
        },
        # 系统设置
        "system": {
            "autostart": False,        # 开机自动运行
            "minimize_to_tray": True,  # 最小化到托盘
            "show_startup_notification": True
        },
        # 提醒样式
        "ui": {
            "window_position": "center",  # center, random
            "window_opacity": 1.0      # 0.0-1.0
        }
    }
```

**Step 2: 添加配置迁移方法**

```python
def migrate_config(self) -> bool:
    """迁移旧配置到新结构"""
    # 检查是否需要迁移
    if self.get("reminder.stand.interval_min") is not None:
        # 旧配置存在，进行迁移
        old_stand_min = self.get("reminder.stand.interval_min", 30)
        old_stand_max = self.get("reminder.stand.interval_max", 60)
        new_stand_avg = (old_stand_min + old_stand_max) // 2

        self.set("reminder.global_offset_minutes", (old_stand_max - old_stand_min) // 2)
        self.set("reminder.stand.interval_avg", new_stand_avg)
        self.set("reminder.exercise.interval_avg",
                 (self.get("reminder.exercise.interval_min", 45) +
                  self.get("reminder.exercise.interval_max", 75)) // 2)
        self.set("reminder.gaze.interval_avg",
                 (self.get("reminder.gaze.interval_min", 60) +
                  self.get("reminder.gaze.interval_max", 90)) // 2)

        # 删除旧的配置键
        self.config.pop("reminder.stand.interval_min", None)
        self.config.pop("reminder.stand.interval_max", None)
        # ... 其他旧键

        self.save()
        return True
    return False
```

**Step 3: 在初始化时调用迁移**

```python
def __init__(self, config_path: str = None):
    # ... 现有代码
    self.migrate_config()  # 添加迁移调用
```

**Step 4: 测试配置迁移**

创建测试文件 `tests/test_config_migration.py`:

```python
def test_old_config_migrates_to_new_structure():
    config = ConfigManager()
    # 设置旧配置
    config.set("reminder.stand.interval_min", 30)
    config.set("reminder.stand.interval_max", 60)
    config.save()

    # 重新加载并迁移
    config2 = ConfigManager()
    result = config2.migrate_config()

    assert result == True
    assert config2.get("reminder.global_offset_minutes") == 15
    assert config2.get("reminder.stand.interval_avg") == 45
    assert config2.get("reminder.stand.interval_min") is None
```

**Step 5: 运行测试**

```bash
pytest tests/test_config_migration.py -v
```

**Step 6: 提交**

```bash
git add src/utils/config.py tests/test_config_migration.py
git commit -m "feat: 新配置结构支持统一偏移量，添加配置迁移"
```

---

## Task 2: 移除惩罚机制

**Files:**
- Delete: `src/core/punishment_logic.py`
- Modify: `src/core/app.py`
- Modify: `src/models/repositories.py` (移除 PunishmentRepository)
- Modify: `src/models/models.py` (移除 PunishmentState 模型)

**Step 1: 从 app.py 移除惩罚逻辑引用**

```python
# 删除导入
- from ..core.punishment_logic import PunishmentLogic

# 删除初始化
- self.punishment_logic = PunishmentLogic(self.config)

# 删除任何使用惩罚逻辑的代码
```

**Step 2: 更新提醒引擎**

修改 `src/core/reminder_engine.py`，移除惩罚相关逻辑：

```python
# 删除任何检查惩罚状态的代码
- if self.punishment_logic.should_trigger_punishment():
-     # 惩罚模式窗口配置
```

**Step 3: 更新数据库模型**

从 `src/models/models.py` 删除 `PunishmentState` 类及其表。

**Step 4: 更新 Repository**

从 `src/models/repositories.py` 删除 `PunishmentRepository` 类。

**Step 5: 删除惩罚逻辑文件**

```bash
rm src/core/punishment_logic.py
```

**Step 6: 测试应用启动**

```bash
python src/main.py
```

预期：应用正常启动，无惩罚相关错误。

**Step 7: 提交**

```bash
git add -A
git commit -m "refactor: 移除惩罚机制及相关代码"
```

---

## Task 3: 更新提醒引擎支持新配置

**Files:**
- Modify: `src/core/reminder_engine.py`

**Step 1: 修改随机间隔计算**

```python
def _calculate_random_interval(self, avg_min: int, offset_min: int) -> int:
    """
    计算随机间隔（平均间隔 ± 偏移量）

    Args:
        avg_min: 平均间隔（分钟）
        offset_min: 随机偏移（分钟）

    Returns:
        int: 间隔毫秒数
    """
    min_minutes = max(5, avg_min - offset_min)  # 至少5分钟
    max_minutes = avg_min + offset_min
    minutes = random.randint(min_minutes, max_minutes)
    return minutes * 60 * 1000
```

**Step 2: 更新调度方法使用新配置**

```python
def schedule_stand_reminder(self):
    """调度站立提醒"""
    avg_min = self.config.get("reminder.stand.interval_avg", 45)
    offset_min = self.config.get("reminder.global_offset_minutes", 15)
    duration = self.config.get("reminder.stand.duration", 90)

    interval_ms = self._calculate_random_interval(avg_min, offset_min)

    def trigger_stand():
        self.stand_reminder.emit(duration)
        self.schedule_stand_reminder()

    self.timer_manager.create_timer(
        self.REMINDER_STAND,
        interval_ms,
        callback=trigger_stand
    )
    self.timer_manager.start_timer(self.REMINDER_STAND)
    self.active_reminders.add(self.REMINDER_STAND)
```

**Step 3: 同样更新 exercise 和 gaze 的调度方法**

**Step 4: 测试随机间隔**

```python
def test_random_interval_calculation():
    for _ in range(100):
        result = ReminderEngine._calculate_random_interval(45, 15)
        minutes = result // 60000
        assert 30 <= minutes <= 60  # 45±15
```

**Step 5: 提交**

```bash
git add src/core/reminder_engine.py
git commit -m "feat: 提醒引擎支持新的配置结构（平均间隔±偏移量）"
```

---

## Task 4: 添加提醒冷却机制

**Files:**
- Modify: `src/core/reminder_engine.py`
- Modify: `src/core/app.py`

**Step 1: 添加冷却状态管理**

在 `ReminderEngine` 中添加：

```python
class ReminderEngine(QObject):
    # ... 现有代码

    def __init__(self, timer_manager: TimerManager, config: ConfigManager):
        super().__init__()
        self.timer_manager = timer_manager
        self.config = config
        self.active_reminders = set()
        self._cooldown_until = None  # 冷却结束时间

    def is_in_cooldown(self) -> bool:
        """检查是否在冷却期"""
        if self._cooldown_until is None:
            return False
        from PySide6.QtCore import QDateTime
        return QDateTime.currentDateTime() < self._cooldown_until

    def start_cooldown(self, seconds: int = 120):
        """开始冷却（默认2分钟）"""
        from PySide6.QtCore import QDateTime
        self._cooldown_until = QDateTime.currentDateTime().addSecs(seconds)

    def pause_all_timers(self):
        """暂停所有定时器"""
        for reminder_type in list(self.active_reminders):
            self.timer_manager.stop_timer(reminder_type)

    def resume_all_timers(self):
        """恢复所有定时器（重新调度）"""
        if self.REMINDER_STAND in self.active_reminders:
            self.schedule_stand_reminder()
        if self.REMINDER_EXERCISE in self.active_reminders:
            self.schedule_exercise_reminder()
        if self.REMINDER_GAZE in self.active_reminders:
            self.schedule_gaze_reminder()
```

**Step 2: 在 app.py 中实现冷却逻辑**

```python
def _show_stand_reminder(self, duration: int):
    """显示站立提醒弹窗"""
    # 检查冷却
    if self.reminder_engine.is_in_cooldown():
        return  # 冷却中，不显示

    # 开始冷却：暂停其他定时器
    self.reminder_engine.start_cooldown(120)  # 2分钟
    self.reminder_engine.pause_all_timers()

    try:
        dialog = StandReminderDialog(duration)
        dialog.exec()

        # 对话框关闭后，等待2分钟恢复
        from PySide6.QtCore import QTimer
        QTimer.singleShot(120000, self._resume_after_cooldown)

    except Exception as e:
        print(f"显示站立提醒失败: {e}")

def _resume_after_cooldown(self):
    """冷却结束后恢复定时器"""
    self.reminder_engine.resume_all_timers()
```

**Step 3: 测试冷却机制**

```python
def test_cooldown_prevents_simultaneous_reminders():
    engine = ReminderEngine(timer_manager, config)
    engine.start_cooldown(120)
    assert engine.is_in_cooldown() == True
```

**Step 4: 提交**

```bash
git add src/core/reminder_engine.py src/core/app.py
git commit -m "feat: 添加提醒冷却机制（2分钟间隔）"
```

---

## Task 5: 创建首页主窗口

**Files:**
- Create: `src/ui/home.py`

**Step 1: 创建首页组件框架**

```python
# -*- coding: utf-8 -*-
"""
首页主窗口
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QGridLayout
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from ...models.repositories import ActivityRepository, UserRepository
from ...utils.config import ConfigManager
from ...utils.bmr_calculator import BMRCalculator, Gender


class HomePage(QWidget):
    """首页主窗口"""

    # 信号
    open_action_library = Signal()
    open_parameter_settings = Signal()
    open_user_info = Signal()
    open_basic_settings = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager()

        # 刷新定时器（每30秒刷新一次）
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(30000)

        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # 标题
        title = QLabel("灵动休息健康助手")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # 添加各个模块
        layout.addWidget(self._create_today_progress_section())
        layout.addWidget(self._create_calorie_stats_section())
        layout.addWidget(self._create_next_reminder_section())
        layout.addWidget(self._create_today_activity_section())
        layout.addWidget(self._create_quick_actions_section())

        layout.addStretch()
        self.setLayout(layout)

    def _create_today_progress_section(self) -> QFrame:
        """今日目标进度"""
        # TODO: 实现
        return QFrame()

    def _create_calorie_stats_section(self) -> QFrame:
        """热量统计"""
        # TODO: 实现
        return QFrame()

    def _create_next_reminder_section(self) -> QFrame:
        """下次提醒"""
        # TODO: 实现
        return QFrame()

    def _create_today_activity_section(self) -> QFrame:
        """今日活动详情"""
        # TODO: 实现
        return QFrame()

    def _create_quick_actions_section(self) -> QFrame:
        """快速操作"""
        frame = QFrame()
        layout = QVBoxLayout(frame)

        title = QLabel("快速操作")
        title.setFont(QFont("Microsoft YaHei UI", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        btn_layout = QHBoxLayout()

        action_library_btn = QPushButton("🏋️ 动作库")
        action_library_btn.clicked.connect(self.open_action_library.emit)
        btn_layout.addWidget(action_library_btn)

        param_settings_btn = QPushButton("⚙️ 参数设置")
        param_settings_btn.clicked.connect(self.open_parameter_settings.emit)
        btn_layout.addWidget(param_settings_btn)

        user_info_btn = QPushButton("👤 用户信息")
        user_info_btn.clicked.connect(self.open_user_info.emit)
        btn_layout.addWidget(user_info_btn)

        basic_settings_btn = QPushButton("🔧 基础设置")
        basic_settings_btn.clicked.connect(self.open_basic_settings.emit)
        btn_layout.addWidget(basic_settings_btn)

        layout.addLayout(btn_layout)
        return frame

    def refresh_data(self):
        """刷新数据"""
        # TODO: 实现数据刷新逻辑
        pass
```

**Step 2: 在 app.py 中集成首页**

```python
def __init__(self):
    # ... 现有代码
    self.home_window = None

def show_home(self):
    """显示首页"""
    if self.home_window is None:
        from ..ui.home import HomePage
        self.home_window = HomePage()
        self.home_window.open_action_library.connect(self._show_action_library)
        self.home_window.open_parameter_settings.connect(self._show_parameter_settings)
        self.home_window.open_user_info.connect(self._show_user_info)
        self.home_window.open_basic_settings.connect(self._show_basic_settings)

    self.home_window.show()
    self.home_window.raise_()
    self.home_window.activateWindow()
```

**Step 3: 更新托盘菜单**

```python
def _create_tray_icon(self):
    # ... 现有代码
    menu = QMenu()

    # 打开主窗口
    home_action = QAction("打开主窗口", self)
    home_action.triggered.connect(self.show_home)
    menu.addAction(home_action)

    menu.addSeparator()

    # 暂停/恢复
    self.pause_action = QAction("暂停提醒", self)
    self.pause_action.triggered.connect(self._toggle_pause)
    menu.addAction(self.pause_action)

    # 退出
    exit_action = QAction("退出", self)
    exit_action.triggered.connect(self._quit)
    menu.addAction(exit_action)

    # 双击托盘图标也打开首页
    self.tray_icon.activated.connect(self._on_tray_activated)

def _on_tray_activated(self, reason):
    """托盘图标被激活"""
    if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
        self.show_home()
```

**Step 4: 首次运行完成后显示首页**

```python
def _show_first_run_setup(self):
    """显示首次运行设置"""
    wizard = FirstRunWizard(None)

    if wizard.exec() == QWizard.DialogCode.Accepted:
        # ... 保存用户数据

        # 显示首页
        self.show_home()
```

**Step 5: 测试首页显示**

```bash
python src/main.py
```

预期：首次运行完成后显示首页。

**Step 6: 提交**

```bash
git add src/ui/home.py src/core/app.py
git commit -m "feat: 添加首页主窗口"
```

---

## Task 6: 完善首页各个模块

**Files:**
- Modify: `src/ui/home.py`

**Step 1: 实现今日目标进度模块**

```python
def _create_today_progress_section(self) -> QFrame:
    """今日目标进度"""
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background-color: #FFFFFF;
            border-radius: 12px;
            border: 1px solid #E0E0E0;
        }
    """)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(12)

    # 标题
    title = QLabel("🎯 今日目标进度")
    title.setFont(QFont("Microsoft YaHei UI", 14, QFont.Weight.Bold))
    layout.addWidget(title)

    # 热量进度
    self.calorie_progress_label = QLabel("运动热量目标：0/400 千卡 (0%)")
    self.calorie_progress_bar = QProgressBar()
    self.calorie_progress_bar.setRange(0, 100)
    self.calorie_progress_bar.setStyleSheet("""
        QProgressBar {
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            text-align: center;
            height: 24px;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            border-radius: 6px;
        }
    """)

    layout.addWidget(self.calorie_progress_label)
    layout.addWidget(self.calorie_progress_bar)

    # 连续打卡
    self.streak_label = QLabel("🔥 连续打卡：0 天")
    self.streak_label.setFont(QFont("Microsoft YaHei UI", 11))
    layout.addWidget(self.streak_label)

    return frame

def _update_today_progress(self):
    """更新今日目标进度"""
    # 获取今日统计数据
    today_stats = ActivityRepository.get_today_stats()
    calorie_burned = today_stats['exercise_calories']

    # 计算目标
    calorie_target = self.config.get("user.calorie_target", 500) * 0.8
    progress = min(100, int(calorie_burned / calorie_target * 100))

    # 更新UI
    self.calorie_progress_label.setText(
        f"运动热量目标：{int(calorie_burned)}/{int(calorie_target)} 千卡 ({progress}%)"
    )
    self.calorie_progress_bar.setValue(progress)

    # 计算连续打卡天数
    streak = self._calculate_streak()
    self.streak_label.setText(f"🔥 连续打卡：{streak} 天")
```

**Step 2: 实现热量统计模块**

```python
def _create_calorie_stats_section(self) -> QFrame:
    """热量统计"""
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background-color: #F5F5F5;
            border-radius: 12px;
        }
    """)
    layout = QGridLayout(frame)
    layout.setContentsMargins(20, 16, 20, 16)
    layout.setSpacing(16)

    # 4个统计卡片
    self.total_calories_card = self._create_stat_card(
        "🔥 累计消耗热量", "0", "千卡", "#4CAF50"
    )
    self.week_calories_card = self._create_stat_card(
        "📅 本周消耗热量", "0", "千卡", "#2196F3"
    )
    self.today_calories_card = self._create_stat_card(
        "💡 今日热量", "0", "千卡", "#FF9800"
    )
    self.week_avg_calories_card = self._create_stat_card(
        "📊 本周日均", "0", "千卡/天", "#9C27B0"
    )

    layout.addWidget(self.total_calories_card, 0, 0)
    layout.addWidget(self.week_calories_card, 0, 1)
    layout.addWidget(self.today_calories_card, 1, 0)
    layout.addWidget(self.week_avg_calories_card, 1, 1)

    return frame

def _create_stat_card(self, title: str, value: str, unit: str, color: str) -> QFrame:
    """创建统计卡片"""
    card = QFrame()
    card.setStyleSheet(f"""
        QFrame {{
            background-color: {color};
            border-radius: 8px;
        }}
    """)
    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 12, 16, 12)
    layout.setSpacing(8)

    title_label = QLabel(title)
    title_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 11pt;")
    layout.addWidget(title_label)

    value_label = QLabel(f"{value} {unit}")
    value_label.setStyleSheet("color: #FFFFFF; font-size: 20pt; font-weight: bold;")
    layout.addWidget(value_label)

    return card

def _update_calorie_stats(self):
    """更新热量统计"""
    # 累计热量
    total_calories = ActivityRepository.get_total_calories()
    self.total_calories_card.findChild(QLabel).setText(
        f"🔥 累计消耗热量\n{int(total_calories)} 千卡"
    )

    # 本周热量（周一到周日）
    week_calories = ActivityRepository.get_week_calories()
    self.week_calories_card.findChild(QLabel).setText(
        f"📅 本周消耗热量\n{int(week_calories)} 千卡"
    )

    # 今日热量
    today_stats = ActivityRepository.get_today_stats()
    today_calories = today_stats['exercise_calories']
    self.today_calories_card.findChild(QLabel).setText(
        f"💡 今日热量\n{int(today_calories)} 千卡"
    )

    # 本周日均
    week_avg = week_calories / 7  # 简化计算
    self.week_avg_calories_card.findChild(QLabel).setText(
        f"📊 本周日均\n{int(week_avg)} 千卡/天"
    )
```

**Step 3: 添加数据刷新逻辑**

```python
def refresh_data(self):
    """刷新所有数据"""
    self._update_today_progress()
    self._update_calorie_stats()
    self._update_next_reminder()
    self._update_today_activity()

def _calculate_streak(self) -> int:
    """计算连续打卡天数"""
    # TODO: 实现
    return 0
```

**Step 4: 提交**

```bash
git add src/ui/home.py
git commit -m "feat: 完善首页数据展示模块"
```

---

## Task 7: 创建首次运行向导页面

**Files:**
- Create: `src/ui/wizards/reminder_settings_page.py`
- Create: `src/ui/wizards/confirm_page.py`
- Modify: `src/ui/wizards/first_run_wizard.py`

**Step 1: 创建提醒设置页**

```python
# -*- coding: utf-8 -*-
"""首次运行向导 - 提醒设置页"""
from PySide6.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QGroupBox, QWidget
)
from PySide6.QtCore import Qt


class ReminderSettingsPage(QWizardPage):
    """提醒设置页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("提醒设置")
        self.setSubTitle("设置提醒间隔和执行时长")

        self.offset_spin = None
        self.stand_interval_spin = None
        self.exercise_interval_spin = None
        self.gaze_interval_spin = None
        self.stand_duration_spin = None
        self.exercise_duration_spin = None
        self.gaze_duration_spin = None

        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 全局设置
        layout.addWidget(self._create_global_settings())

        # 间隔设置
        layout.addWidget(self._create_interval_settings())

        # 时长设置
        layout.addWidget(self._create_duration_settings())

        layout.addStretch()
        self.setLayout(layout)

    def _create_global_settings(self) -> QGroupBox:
        """全局设置"""
        group = QGroupBox("全局设置")
        group_layout = QVBoxLayout()

        # 统一随机偏移
        offset_layout = QHBoxLayout()
        offset_layout.addWidget(QLabel("统一随机偏移"))
        self.offset_spin = QSpinBox()
        self.offset_spin.setRange(0, 60)
        self.offset_spin.setValue(15)
        self.offset_spin.setSuffix(" 分钟")
        offset_layout.addWidget(self.offset_spin)
        offset_layout.addStretch()

        # 说明
        hint = QLabel("说明：所有提醒的实际间隔会在设定值基础上随机增减\n"
                     "      例如：45±15 = 30-60分钟之间随机")
        hint.setStyleSheet("color: #757575; font-size: 10pt;")
        hint.setWordWrap(True)

        group_layout.addLayout(offset_layout)
        group_layout.addWidget(hint)
        group.setLayout(group_layout)

        self.registerField("global_offset*", self.offset_spin)

        return group

    def _create_interval_settings(self) -> QGroupBox:
        """间隔设置"""
        group = QGroupBox("提醒间隔设置")
        layout = QVBoxLayout()

        self.stand_interval_spin = self._create_input_row(
            layout, "强制站立间隔：", 45, 5, 180
        )
        self.exercise_interval_spin = self._create_input_row(
            layout, "微运动间隔：", 60, 5, 180
        )
        self.gaze_interval_spin = self._create_input_row(
            layout, "强制远眺间隔：", 75, 5, 180
        )

        group.setLayout(layout)

        self.registerField("stand_interval*", self.stand_interval_spin)
        self.registerField("exercise_interval*", self.exercise_interval_spin)
        self.registerField("gaze_interval*", self.gaze_interval_spin)

        return group

    def _create_duration_settings(self) -> QGroupBox:
        """执行时长设置"""
        group = QGroupBox("执行时长设置")
        layout = QVBoxLayout()

        self.stand_duration_spin = self._create_input_row(
            layout, "强制站立时长：", 90, 30, 300, suffix=" 秒"
        )
        self.exercise_duration_spin = self._create_input_row(
            layout, "微运动时长：", 120, 60, 180, suffix=" 秒"
        )
        self.gaze_duration_spin = self._create_input_row(
            layout, "强制远眺时长：", 60, 10, 300, suffix=" 秒"
        )

        group.setLayout(layout)

        self.registerField("stand_duration*", self.stand_duration_spin)
        self.registerField("exercise_duration*", self.exercise_duration_spin)
        self.registerField("gaze_duration*", self.gaze_duration_spin)

        return group

    def _create_input_row(self, parent_layout, label, value, min_val, max_val, suffix=" 分钟") -> QSpinBox:
        """创建输入行"""
        row = QHBoxLayout()
        row.addWidget(QLabel(label))

        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(value)
        spin.setSuffix(suffix)
        row.addWidget(spin)
        row.addStretch()

        parent_layout.addLayout(row)
        return spin
```

**Step 2: 创建确认体验页**

```python
# -*- coding: utf-8 -*-
"""首次运行向导 - 确认体验页"""
from PySide6.QtWidgets import (
    QWizardPage, QVBoxLayout, QLabel, QPushButton, QWidget
)
from PySide6.QtCore import Qt, QTimer


class ConfirmPage(QWizardPage):
    """确认体验页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("设置完成")
        self.countdown = 10
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 标题
        title = QLabel("✅ 设置完成！")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24pt; font-weight: bold;")
        layout.addWidget(title)

        # 倒计时
        self.countdown_label = QLabel()
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 14pt;")
        layout.addWidget(self.countdown_label)

        # 设置摘要
        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("font-size: 11pt; color: #555;")
        layout.addWidget(self.summary_label)

        # 提示
        hint = QLabel(
            "💡 第一次体验提示：\n"
            "   • 站立提醒无法跳过，请等待倒计时结束\n"
            "   • 微运动提醒点击完成按钮结束\n"
            "   • 应用会在系统托盘运行，可随时调整设置"
        )
        hint.setStyleSheet("font-size: 10pt; color: #757575;")
        layout.addWidget(hint)

        layout.addStretch()
        self.setLayout(layout)

        # 按钮
        self.skip_button = QPushButton("跳过体验")
        self.experience_button = QPushButton("立即体验")
        self.experience_button.clicked.connect(self._on_experience)

        # 倒计时定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_countdown)

    def initializePage(self):
        """页面初始化"""
        # 获取向导数据
        wizard = self.wizard()
        weight = wizard.field("weight")
        calorie_target = wizard.field("calorie_target")

        # 显示摘要
        self.summary_label.setText(
            f"个人信息：体重 {weight}kg，每天目标减 {calorie_target} 千卡\n"
            f"提醒间隔：站立 {wizard.field('stand_interval')}分钟，"
            f"运动 {wizard.field('exercise_interval')}分钟，"
            f"远眺 {wizard.field('gaze_interval')}分钟\n"
            f"随机偏移：± {wizard.field('global_offset')} 分钟"
        )

        # 开始倒计时
        self.countdown = 10
        self._update_countdown()
        self.timer.start(1000)

    def _update_countdown(self):
        """更新倒计时"""
        self.countdown_label.setText(
            f"应用将在 {self.countdown} 秒后开始运行\n"
            f"倒计时结束后，将弹出首次站立提醒"
        )
        self.countdown -= 1

        if self.countdown < 0:
            self.timer.stop()
            self.wizard().skip_experience = False
            self.wizard().done(1)  # 自动完成

    def _on_experience(self):
        """立即体验"""
        self.timer.stop()
        self.wizard().skip_experience = False
        self.wizard().done(1)
```

**Step 3: 更新首次运行向导**

```python
# src/ui/wizards/first_run_wizard.py
from .reminder_settings_page import ReminderSettingsPage
from .confirm_page import ConfirmPage

class FirstRunWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("灵动休息健康助手 - 首次设置")
        self.setMinimumSize(700, 500)
        self.skip_experience = False

        # 添加页面
        self.addPage(SimpleProfilePage())  # 现有的个人信息页
        self.addPage(ReminderSettingsPage())  # 新增
        self.addPage(ConfirmPage())  # 新增

    def get_reminder_settings(self) -> dict:
        """获取提醒设置"""
        return {
            "global_offset": self.field("global_offset"),
            "stand_interval": self.field("stand_interval"),
            "exercise_interval": self.field("exercise_interval"),
            "gaze_interval": self.field("gaze_interval"),
            "stand_duration": self.field("stand_duration"),
            "exercise_duration": self.field("exercise_duration"),
            "gaze_duration": self.field("gaze_duration"),
        }
```

**Step 4: 提交**

```bash
git add src/ui/wizards/
git commit -m "feat: 添加首次运行向导的提醒设置页和确认页"
```

---

## Task 8: 更新设置对话框

**Files:**
- Modify: `src/ui/settings/settings_dialog.py`

**Step 1: 重构提醒设置标签页**

```python
def _create_reminder_tab(self) -> QWidget:
    """创建提醒设置页面（新结构）"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(20)

    # 全局设置
    layout.addWidget(self._create_global_reminder_settings())

    # 间隔设置
    layout.addWidget(self._create_interval_settings())

    # 时长设置
    layout.addWidget(self._create_duration_settings())

    # 启用开关
    layout.addWidget(self._create_enable_toggles())

    layout.addStretch()
    return widget

def _create_global_reminder_settings(self) -> QGroupBox:
    """全局提醒设置"""
    group = QGroupBox("全局设置")
    layout = QVBoxLayout()

    offset_layout = QHBoxLayout()
    offset_layout.addWidget(QLabel("统一随机偏移"))
    self.global_offset_spin = QSpinBox()
    self.global_offset_spin.setRange(0, 60)
    self.global_offset_spin.setSuffix(" 分钟")
    self.global_offset_spin.valueChanged.connect(self._on_modified)
    offset_layout.addWidget(self.global_offset_spin)
    offset_layout.addStretch()

    hint = QLabel("说明：所有提醒的实际间隔会在设定值基础上随机增减")
    hint.setStyleSheet("color: #757575; font-size: 10pt;")

    layout.addLayout(offset_layout)
    layout.addWidget(hint)
    group.setLayout(layout)
    return group

def _create_interval_settings(self) -> QGroupBox:
    """间隔设置"""
    group = QGroupBox("提醒间隔设置")
    layout = QVBoxLayout()

    self.stand_interval_spin = self._create_input_row(
        layout, "强制站立间隔：", 45
    )
    self.exercise_interval_spin = self._create_input_row(
        layout, "微运动间隔：", 60
    )
    self.gaze_interval_spin = self._create_input_row(
        layout, "强制远眺间隔：", 75
    )

    group.setLayout(layout)
    return group

def _create_duration_settings(self) -> QGroupBox:
    """执行时长设置"""
    group = QGroupBox("执行时长设置")
    layout = QVBoxLayout()

    self.stand_duration_spin = self._create_input_row(
        layout, "强制站立时长：", 90, suffix=" 秒"
    )
    self.exercise_duration_spin = self._create_input_row(
        layout, "微运动时长：", 120, suffix=" 秒"
    )
    self.gaze_duration_spin = self._create_input_row(
        layout, "强制远眺时长：", 60, suffix=" 秒"
    )

    group.setLayout(layout)
    return group

def _create_enable_toggles(self) -> QGroupBox:
    """启用开关"""
    group = QGroupBox("启用提醒")
    layout = QVBoxLayout()

    self.stand_enabled_cb = QCheckBox("启用强制站立提醒")
    self.exercise_enabled_cb = QCheckBox("启用微运动提醒")
    self.gaze_enabled_cb = QCheckBox("启用强制远眺提醒")

    self.stand_enabled_cb.stateChanged.connect(self._on_modified)
    self.exercise_enabled_cb.stateChanged.connect(self._on_modified)
    self.gaze_enabled_cb.stateChanged.connect(self._on_modified)

    layout.addWidget(self.stand_enabled_cb)
    layout.addWidget(self.exercise_enabled_cb)
    layout.addWidget(self.gaze_enabled_cb)

    group.setLayout(layout)
    return group

def _create_input_row(self, parent_layout, label, value, suffix=" 分钟"):
    """创建输入行"""
    row = QHBoxLayout()
    row.addWidget(QLabel(label))

    spin = QSpinBox()
    spin.setRange(5, 180)
    spin.setValue(value)
    spin.setSuffix(suffix)
    spin.valueChanged.connect(self._on_modified)
    row.addWidget(spin)
    row.addStretch()

    parent_layout.addLayout(row)
    return spin
```

**Step 2: 添加基础设置标签页**

```python
def _create_basic_settings_tab(self) -> QWidget:
    """创建基础设置页面"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(20)

    # 启动设置
    layout.addWidget(self._create_startup_settings())

    # 音频设置
    layout.addWidget(self._create_audio_settings())

    # 提醒样式
    layout.addWidget(self._create_reminder_style_settings())

    layout.addStretch()
    return widget

def _create_startup_settings(self) -> QGroupBox:
    """启动设置"""
    group = QGroupBox("启动设置")
    layout = QVBoxLayout()

    self.autostart_cb = QCheckBox("开机自动运行")
    self.show_notification_cb = QCheckBox("启动时显示通知")
    self.minimize_to_tray_cb = QCheckBox("关闭窗口时最小化到托盘（不退出）")
    self.minimize_to_tray_cb.setChecked(True)

    self.autostart_cb.stateChanged.connect(self._on_modified)
    self.show_notification_cb.stateChanged.connect(self._on_modified)
    self.minimize_to_tray_cb.stateChanged.connect(self._on_modified)

    layout.addWidget(self.autostart_cb)
    layout.addWidget(self.show_notification_cb)
    layout.addWidget(self.minimize_to_tray_cb)

    group.setLayout(layout)
    return group
```

**Step 3: 更新加载和保存方法**

```python
def _load_settings(self):
    """加载设置"""
    # 全局偏移
    self.global_offset_spin.setValue(
        self.config.get("reminder.global_offset_minutes", 15)
    )

    # 间隔（新结构）
    self.stand_interval_spin.setValue(
        self.config.get("reminder.stand.interval_avg", 45)
    )
    self.exercise_interval_spin.setValue(
        self.config.get("reminder.exercise.interval_avg", 60)
    )
    self.gaze_interval_spin.setValue(
        self.config.get("reminder.gaze.interval_avg", 75)
    )

    # 时长
    self.stand_duration_spin.setValue(
        self.config.get("reminder.stand.duration", 90)
    )
    self.exercise_duration_spin.setValue(
        self.config.get("reminder.exercise.duration", 120)
    )
    self.gaze_duration_spin.setValue(
        self.config.get("reminder.gaze.duration", 60)
    )

    # 启用开关
    self.stand_enabled_cb.setChecked(self.config.is_reminder_enabled("stand"))
    self.exercise_enabled_cb.setChecked(self.config.is_reminder_enabled("exercise"))
    self.gaze_enabled_cb.setChecked(self.config.is_reminder_enabled("gaze"))

    # 系统设置
    self.autostart_cb.setChecked(self.config.get("system.autostart", False))
    self.show_notification_cb.setChecked(self.config.get("system.show_startup_notification", True))
    self.minimize_to_tray_cb.setChecked(self.config.get("system.minimize_to_tray", True))

def _apply_settings(self):
    """应用设置"""
    # 全局偏移
    self.config.set("reminder.global_offset_minutes", self.global_offset_spin.value())

    # 间隔
    self.config.set("reminder.stand.interval_avg", self.stand_interval_spin.value())
    self.config.set("reminder.exercise.interval_avg", self.exercise_interval_spin.value())
    self.config.set("reminder.gaze.interval_avg", self.gaze_interval_spin.value())

    # 时长
    self.config.set("reminder.stand.duration", self.stand_duration_spin.value())
    self.config.set("reminder.exercise.duration", self.exercise_duration_spin.value())
    self.config.set("reminder.gaze.duration", self.gaze_duration_spin.value())

    # 启用开关
    self.config.set("reminder.stand.enabled", self.stand_enabled_cb.isChecked())
    self.config.set("reminder.exercise.enabled", self.exercise_enabled_cb.isChecked())
    self.config.set("reminder.gaze.enabled", self.gaze_enabled_cb.isChecked())

    # 系统设置
    self.config.set("system.autostart", self.autostart_cb.isChecked())
    self.config.set("system.show_startup_notification", self.show_notification_cb.isChecked())
    self.config.set("system.minimize_to_tray", self.minimize_to_tray_cb.isChecked())

    self.config.save()
    self.settings_changed.emit()
```

**Step 4: 提交**

```bash
git add src/ui/settings/settings_dialog.py
git commit -m "refactor: 重构设置对话框，支持新配置结构"
```

---

## Task 9: 更新弹窗（去掉跳过按钮）

**Files:**
- Modify: `src/ui/dialogs/exercise_dialog.py`

**Step 1: 简化微运动弹窗**

```python
class ExerciseReminderDialog(BaseReminderDialog):
    def __init__(self, exercises: list, weight_kg: float = 70.0, parent=None):
        # ... 现有代码
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # 标题
        self.title_label = QLabel(f"🏃 {self.current_exercise['name']} 🏃")
        # ... 样式设置
        layout.addWidget(self.title_label)

        layout.addStretch(1)

        # 倒计时
        self.countdown_label = QLabel()
        # ... 样式设置
        layout.addWidget(self.countdown_label)

        layout.addStretch(1)

        # 提示
        self.hint_label = QLabel("（请完成该动作，等待倒计时结束）")
        # ... 样式设置
        layout.addWidget(self.hint_label)

        # 热量信息
        calories = METCalculator.calculate_calories_by_exercise(
            self.current_exercise.get('met', 5.0),
            self.duration,
            self.weight_kg
        )
        info_label = QLabel(f"MET: {self.current_exercise.get('met', 5.0)} | 热量: {calories:.1f} 千卡")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 11pt; color: #757575;")
        layout.addWidget(info_label)

        # 完成按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        complete_btn = QPushButton("✓ 完成")
        complete_btn.setMinimumWidth(120)
        complete_btn.setMinimumHeight(40)
        complete_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        complete_btn.clicked.connect(self._on_complete)
        button_layout.addWidget(complete_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _on_complete(self):
        """完成按钮点击"""
        # 停止倒计时
        self.stop_countdown()

        # 显示完成反馈
        self._show_complete_feedback()

        # 延迟关闭
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1500, self.accept)
```

**Step 2: 提交**

```bash
git add src/ui/dialogs/exercise_dialog.py
git commit -m "refactor: 微运动弹窗只保留完成按钮"
```

---

## Task 10: 添加开机自启动功能

**Files:**
- Create: `src/utils/autostart.py`

**Step 1: 创建开机自启动管理器**

```python
# -*- coding: utf-8 -*-
"""开机自启动管理（Windows）"""
import os
import winreg


class AutostartManager:
    """Windows 开机自启动管理"""

    REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "ExerciseReminder"

    @staticmethod
    def is_enabled() -> bool:
        """检查是否启用开机自启动"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AutostartManager.REGISTRY_KEY, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, AutostartManager.APP_NAME)
            winreg.CloseKey(key)
            return value is not None
        except WindowsError:
            return False

    @staticmethod
    def enable(exe_path: str = None) -> bool:
        """启用开机自启动"""
        if exe_path is None:
            exe_path = AutostartManager._get_exe_path()

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AutostartManager.REGISTRY_KEY, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, AutostartManager.APP_NAME, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"启用开机自启动失败: {e}")
            return False

    @staticmethod
    def disable() -> bool:
        """禁用开机自启动"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AutostartManager.REGISTRY_KEY, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, AutostartManager.APP_NAME)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"禁用开机自启动失败: {e}")
            return False

    @staticmethod
    def _get_exe_path() -> str:
        """获取当前可执行文件路径"""
        if getattr(sys, 'frozen', False):
            return sys.executable
        else:
            # 开发环境
            return f'"{sys.executable}" "{os.path.abspath("src/main.py")}"'
```

**Step 2: 在应用启动时处理自启动设置**

```python
# src/core/app.py
from ..utils.autostart import AutostartManager

def __init__(self):
    # ... 现有代码

    # 处理开机自启动
    if self.config.get("system.autostart", False):
        if not AutostartManager.is_enabled():
            AutostartManager.enable()
    else:
        if AutostartManager.is_enabled():
            AutostartManager.disable()
```

**Step 3: 在设置保存时处理**

```python
# src/ui/settings/settings_dialog.py
def _apply_settings(self):
    """应用设置"""
    # ... 现有代码

    # 处理开机自启动
    from ...utils.autostart import AutostartManager
    if self.autostart_cb.isChecked():
        AutostartManager.enable()
    else:
        AutostartManager.disable()
```

**Step 4: 提交**

```bash
git add src/utils/autostart.py src/core/app.py
git commit -m "feat: 添加 Windows 开机自启动功能"
```

---

## Task 11: 添加 Repository 方法

**Files:**
- Modify: `src/models/repositories.py`

**Step 1: 添加热量统计方法**

```python
@staticmethod
def get_total_calories() -> float:
    """获取累计消耗热量（所有时间）"""
    query = (ActivityLog
             .select(fn.SUM(ActivityLog.calories))
             .where(ActivityLog.activity_type == 'exercise'))
    result = query.scalar()
    return result if result else 0.0

@staticmethod
def get_week_calories() -> float:
    """获取本周消耗热量（周一到周日）"""
    from datetime import date, datetime, timedelta

    today = date.today()
    # 获取本周一
    monday = today - timedelta(days=today.weekday())

    query = (ActivityLog
             .select(fn.SUM(ActivityLog.calories))
             .where(
                 (ActivityLog.activity_type == 'exercise') &
                 (ActivityLog.timestamp >= datetime.combine(monday, datetime.min.time()))
             ))
    result = query.scalar()
    return result if result else 0.0
```

**Step 2: 添加连续打卡计算**

```python
@staticmethod
def get_streak_days() -> int:
    """计算连续打卡天数"""
    from datetime import date, datetime, timedelta

    streak = 0
    check_date = date.today()

    while True:
        day_start = datetime.combine(check_date, datetime.min.time())
        day_end = datetime.combine(check_date, datetime.max.time())

        count = ActivityLog.select().where(
            (ActivityLog.timestamp >= day_start) &
            (ActivityLog.timestamp <= day_end)
        ).count()

        if count > 0:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    return streak
```

**Step 3: 提交**

```bash
git add src/models/repositories.py
git commit -m "feat: 添加热量统计和连续打卡方法"
```

---

## Task 12: 综合测试

**Files:**
- Create: `tests/test_integration.py`

**Step 1: 创建集成测试**

```python
def test_first_run_flow():
    """测试首次运行流程"""
    # 清空数据
    reset_database()

    # 启动应用
    app = create_application()
    app.start()

    # 检查向导显示
    assert app._is_first_run() == True

    # 模拟向导输入
    wizard = FirstRunWizard(None)
    # ... 设置字段值

    # 完成向导
    wizard.accept()

    # 检查配置保存
    config = ConfigManager()
    assert config.get("reminder.global_offset_minutes") == 15
    assert config.get("reminder.stand.interval_avg") == 45

    # 检查首页显示
    app.show_home()
    assert app.home_window is not None

def test_reminder_cooldown():
    """测试提醒冷却机制"""
    engine = ReminderEngine(timer_manager, config)

    # 模拟第一个提醒
    engine.start_cooldown(120)
    assert engine.is_in_cooldown() == True

    # 尝试调度第二个提醒
    assert engine.is_in_cooldown() == True

def test_config_migration():
    """测试配置迁移"""
    # 创建旧配置
    config = ConfigManager()
    config.set("reminder.stand.interval_min", 30)
    config.set("reminder.stand.interval_max", 60)
    config.save()

    # 迁移
    config2 = ConfigManager()
    result = config2.migrate_config()

    assert result == True
    assert config2.get("reminder.stand.interval_avg") == 45
    assert config2.get("reminder.global_offset_minutes") == 15
```

**Step 2: 运行测试**

```bash
pytest tests/test_integration.py -v
```

**Step 3: 手动测试清单**

```
□ 首次安装后显示向导
□ 向导保存配置正确
□ 倒计时10秒后弹出站立提醒
□ 首页显示正确
□ 统计数据准确
□ 设置保存生效
□ 提醒间隔正确（随机）
□ 冷却机制生效（2分钟间隔）
□ 开机自启动生效
□ 音效只在最后10秒播放
```

**Step 4: 提交**

```bash
git add tests/test_integration.py
git commit -m "test: 添加集成测试"
```

---

## Task 13: 编写新 PRD 文档

**Files:**
- Create: `docs/PRD-v3.md`

**Step 1: 编写完整 PRD**

根据所有讨论内容编写新的产品需求文档。

**Step 2: 删除旧 PRD**

```bash
rm prd.md
git add docs/PRD-v3.md
git commit -m "docs: 重写 PRD v3（去除惩罚机制，添加首页，新配置结构）"
```

---

## 总结

此计划包含 13 个主要任务，涵盖：
1. 配置结构重构
2. 移除惩罚机制
3. 提醒引擎更新
4. 冷却机制
5. 首页创建
6. 向导页面
7. 设置对话框重构
8. 弹窗简化
9. 开机自启动
10. 数据统计
11. 测试
12. 文档

预计工作量：约 3-5 天
