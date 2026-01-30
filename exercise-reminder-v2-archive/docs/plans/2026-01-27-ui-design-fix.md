# UI 设计规范修复实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标:** 修复现有实现与 [DESIGN-UI-001.md](DESIGN-UI-001.md) 设计文档之间的所有差异

**架构:** 按照 UI 设计规范修改向导页面、提醒弹窗和设置界面，确保与设计文档完全一致

**技术栈:** PySide6 (Qt for Python), pytest, loguru

---

## 问题分析

### 设计文档要求 vs 当前实现差异

| 组件 | 设计要求 | 当前实现 | 差异 |
|------|---------|---------|------|
| **向导页面数** | 3页 | 4页 | 多了欢迎页 |
| **向导第1页** | 个人基础设置（身高/体重/年龄/性别/目标） | 欢迎页 | 完全不同 |
| **微运动弹窗** | 有标题栏、可拖动、纯倒计时 | 无标题栏、无边框 | 窗口样式不符 |
| **倒计时闪烁** | <10秒红色闪烁 | 仅变色，无闪烁动画 | 缺少闪烁效果 |
| **基础设置页** | 5个标签页 | 已实现 | ✓ 符合 |

---

## Task 1: 简化向导为3页（删除欢迎页）

**问题:** 设计要求3页，当前实现有4页（多了欢迎页）

**Files:**
- Modify: `src/ui/wizards/first_run_wizard.py:48-74`
- Modify: `src/ui/wizards/profile_page.py`
- Modify: `src/core/app.py:99-140`
- Delete: `src/ui/wizards/welcome_page.py`
- Test: `tests/test_wizard.py`

**Step 1: 更新向导为3页结构**

修改 `src/ui/wizards/first_run_wizard.py`，删除欢迎页引用：

```python
def _setup_pages(self):
    """设置向导页面 - 简化为3页"""
    self.logger.info("设置向导页面")

    # 页面 1: 个人基础设置页 (ID: 0)
    self.profile_page = ProfilePage(self)
    self.profile_page_id = self.addPage(self.profile_page)
    self.logger.debug("添加个人基础设置页 (Page ID: 0)")

    # 页面 2: 提醒设置页 (ID: 1)
    self.settings_page = ReminderSettingsPage(self)
    self.settings_page_id = self.addPage(self.settings_page)
    self.logger.debug("添加提醒设置页 (Page ID: 1)")

    # 页面 3: 体验倒计时页 (ID: 2)
    self.experience_page = ExperiencePage(self)
    self.experience_page_id = self.addPage(self.experience_page)
    self.logger.debug("添加体验倒计时页 (Page ID: 2)")

    # 设置起始页
    self.setStartId(self.profile_page_id)
    self.logger.debug(f"设置起始页为: {self.profile_page_id}")
```

**Step 2: 删除 welcome_page.py**

```bash
rm src/ui/wizards/welcome_page.py
```

**Step 3: 更新 __init__.py**

修改 `src/ui/wizards/__init__.py`，删除欢迎页导入：

```python
from .profile_page import ProfilePage
from .reminder_settings_page import ReminderSettingsPage
from .experience_page import ExperiencePage
```

**Step 4: 运行测试验证**

Run: `pytest tests/test_wizard.py -v`
Expected: 所有测试通过（需要更新测试中的页面ID）

**Step 5: 提交**

```bash
git add src/ui/wizards/first_run_wizard.py src/ui/wizards/__init__.py
git rm src/ui/wizards/welcome_page.py
git commit -m "refactor: 简化向导为3页，删除欢迎页"
```

---

## Task 2: 修改ProfilePage为设计规范格式

**问题:** 当前ProfilePage布局与设计文档第4.2节要求不符

**Files:**
- Modify: `src/ui/wizards/profile_page.py`
- Test: `tests/test_wizard.py`

**Step 1: 重写ProfilePage布局**

按照设计文档第4.2节的布局重写 `src/ui/wizards/profile_page.py`：

```python
# -*- coding: utf-8 -*-
"""
个人基础设置页 - 向导第1页

按设计文档4.2节实现：4个输入卡片 + 目标设置卡片
"""
from PySide6.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDoubleSpinBox, QRadioButton,
    QButtonGroup, QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ProfilePage(QWizardPage):
    """个人基础设置页 - 按设计文档实现"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("个人基础设置")
        self.setSubTitle("请输入您的基本信息，我们将为您定制合适的提醒计划")

        # 注册字段
        self._register_fields()

        # 创建UI
        self._setup_ui()

    def _register_fields(self):
        """注册向导字段"""
        # 身高
        self.height_spin = QSpinBox()
        self.height_spin.setRange(140, 220)
        self.height_spin.setValue(170)
        self.height_spin.setSuffix(" 厘米")
        self.registerField("height*", self.height_spin)

        # 体重
        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setRange(40.0, 150.0)
        self.weight_spin.setValue(70.0)
        self.weight_spin.setSuffix(" 千克")
        self.registerField("weight*", self.weight_spin)

        # 年龄
        self.age_spin = QSpinBox()
        self.age_spin.setRange(18, 80)
        self.age_spin.setValue(30)
        self.age_spin.setSuffix(" 岁")
        self.registerField("age*", self.age_spin)

        # 性别
        self.gender_group = QButtonGroup()
        self.male_radio = QRadioButton("男")
        self.female_radio = QRadioButton("女")
        self.male_radio.setChecked(True)
        self.gender_group.addButton(self.male_radio, 1)
        self.gender_group.addButton(self.female_radio, 2)
        self.registerField("gender", self.male_radio, "checked", "toggled")

        # 每日目标
        self.calorie_spin = QSpinBox()
        self.calorie_spin.setRange(100, 1000)
        self.calorie_spin.setValue(300)
        self.calorie_spin.setSuffix(" kcal")
        self.registerField("calorieTarget", self.calorie_spin)

    def _setup_ui(self):
        """设置UI - 按设计文档布局"""
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 4个输入卡片（身高、体重、年龄、性别）
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        # 身高卡片
        height_card = self._create_input_card("📏", "身高", self.height_spin)
        cards_layout.addWidget(height_card)

        # 体重卡片
        weight_card = self._create_input_card("⚖️", "体重", self.weight_spin)
        cards_layout.addWidget(weight_card)

        # 年龄卡片
        age_card = self._create_input_card("🎂", "年龄", self.age_spin)
        cards_layout.addWidget(age_card)

        # 性别卡片
        gender_card = self._create_gender_card()
        cards_layout.addWidget(gender_card)

        layout.addLayout(cards_layout)

        # 每日目标卡片
        target_card = self._create_target_card()
        layout.addWidget(target_card)

        layout.addStretch()
        self.setLayout(layout)

    def _create_input_card(self, icon: str, title: str, spinbox: QSpinBox) -> QFrame:
        """创建输入卡片 (140 x 180 px)"""
        card = QFrame()
        card.setFixedSize(140, 180)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E0E0E0;
            }
            QFrame:hover {
                border: 2px solid #4CAF50;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(8)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 图标
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 40pt;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14pt; color: #757575;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)

        # 输入框
        spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spinbox.setStyleSheet("""
            QSpinBox {
                font-size: 18pt;
                font-weight: bold;
                border: none;
                background: transparent;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
            }
        """)
        card_layout.addWidget(spinbox)

        # 单位标签（已包含在spinbox中）

        return card

    def _create_gender_card(self) -> QFrame:
        """创建性别选择卡片"""
        card = QFrame()
        card.setFixedSize(140, 180)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E0E0E0;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(8)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 图标
        icon_label = QLabel("👤")
        icon_label.setStyleSheet("font-size: 40pt;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)

        # 标题
        title_label = QLabel("性别")
        title_label.setStyleSheet("font-size: 14pt; color: #757575;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)

        # 性别选项
        gender_layout = QHBoxLayout()
        self.male_radio.setStyleSheet("font-size: 14pt;")
        self.female_radio.setStyleSheet("font-size: 14pt;")
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        card_layout.addLayout(gender_layout)

        return card

    def _create_target_card(self) -> QFrame:
        """创建每日目标卡片"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        # 标题
        title_layout = QHBoxLayout()
        icon_label = QLabel("🔥")
        icon_label.setStyleSheet("font-size: 24pt;")
        title_layout.addWidget(icon_label)

        title_label = QLabel("每日运动目标")
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        card_layout.addLayout(title_layout)

        # 输入
        input_layout = QHBoxLayout()
        input_layout.addStretch()

        self.calorie_spin.setStyleSheet("""
            QSpinBox {
                font-size: 24pt;
                font-weight: bold;
                border: none;
                background: transparent;
                color: #4CAF50;
            }
        """)
        input_layout.addWidget(self.calorie_spin)

        unit_label = QLabel("建议每日通过运动消耗的热量目标")
        unit_label.setStyleSheet("font-size: 12pt; color: #757575;")
        card_layout.addWidget(unit_label)

        return card
```

**Step 2: 更新app.py获取性别数据**

修改 `src/core/app.py` 第113行附近：

```python
gender = "male" if user_data.get("gender") else "female"
```

改为：

```python
# 获取性别选择（male_radio.checked=True时为male）
gender = user_data.get("gender", "male")
```

**Step 3: 运行测试**

Run: `pytest tests/test_wizard.py -v`
Expected: 测试通过

**Step 4: 提交**

```bash
git add src/ui/wizards/profile_page.py src/core/app.py
git commit -m "refactor: 按设计文档重写ProfilePage布局"
```

---

## Task 3: 微运动弹窗添加标题栏

**问题:** 设计要求微运动弹窗有标题栏（可拖动），当前实现为无边框

**Files:**
- Modify: `src/ui/dialogs/exercise_dialog.py`
- Modify: `src/ui/dialogs/base_dialog.py`
- Test: `tests/test_dialogs.py`

**Step 1: 修改基类支持可选标题栏**

修改 `src/ui/dialogs/base_dialog.py` 添加标题栏支持：

```python
class BaseReminderDialog(QDialog):
    # ... existing code ...

    def __init__(self, parent=None, has_title_bar: bool = False):
        """
        初始化弹窗基类

        Args:
            parent: 父窗口
            has_title_bar: 是否显示标题栏（默认无边框）
        """
        super().__init__(parent)
        self._has_title_bar = has_title_bar

        # ... existing code ...
        self._setup_window_properties()  # 现在会检查 has_title_bar
```

修改 `_setup_window_properties` 方法：

```python
def _setup_window_properties(self):
    """设置窗口属性"""
    # 基础标志
    flags = [
        Qt.WindowType.Window,
        Qt.WindowType.WindowStaysOnTopHint,
    ]

    # 如果不需要标题栏，添加无边框标志
    if not self._has_title_bar:
        flags.extend([
            Qt.WindowType.CustomizeWindowHint,
            Qt.WindowType.FramelessWindowHint,
        ])
    else:
        # 有标题栏：保留标准标题栏，但移除最大化/最小化按钮
        flags.extend([
            Qt.WindowType.CustomizeWindowHint,
        ])

    self.setWindowFlags(Qt.WindowType(flags[0] | flags[1] | flags[2] | (flags[3] if len(flags) > 3 else 0)))
```

**Step 2: 修改ExerciseDialog使用标题栏**

修改 `src/ui/dialogs/exercise_dialog.py`：

```python
class ExerciseReminderDialog(BaseReminderDialog):
    def __init__(self, exercises: list, weight_kg: float = 70.0, parent=None):
        self.exercises = exercises
        self.current_index = 0
        self.weight_kg = weight_kg

        # 获取当前动作
        self.current_exercise = exercises[0] if exercises else {"name": "深蹲", "duration": 30, "met": 5.0}
        self.duration = self.current_exercise.get('duration', self.current_exercise.get('duration_seconds', 30))

        # 传入 has_title_bar=True
        super().__init__(parent, has_title_bar=True)

        # 设置窗口标题
        self.setWindowTitle(f"🏃 {self.current_exercise['name']}")

        # UI 组件
        self.title_label = None
        self.countdown_label = None
        self.hint_label = None

        self.setup_ui()
```

修改 `setup_ui` 方法，移除自定义标题：

```python
def setup_ui(self):
    """设置UI"""
    # 创建主布局
    layout = QVBoxLayout()
    layout.setContentsMargins(40, 20, 40, 40)
    layout.setSpacing(20)

    # 倒计时（移除自定义标题，使用系统标题栏）
    self.countdown_label = QLabel()
    self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    countdown_font = QFont("Consolas", 96, QFont.Weight.Bold)
    self.countdown_label.setFont(countdown_font)

    # MET 值显示
    self.met_label = QLabel(f"MET: {self.current_exercise.get('met', 5.0)}")
    self.met_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.met_label.setStyleSheet("font-size: 14pt; color: #757575;")

    # 提示
    self.hint_label = QLabel("请完成该动作，等待倒计时结束")
    self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    hint_font = QFont("Microsoft YaHei UI", 16)
    self.hint_label.setFont(hint_font)
    self.hint_label.setStyleSheet("color: #757575;")

    # 设置样式
    self._apply_styles()

    # 添加到布局
    layout.addStretch(1)
    layout.addWidget(self.countdown_label)
    layout.addWidget(self.met_label)
    layout.addStretch(1)
    layout.addWidget(self.hint_label)

    self.setLayout(layout)
```

**Step 3: 更新StandDialog和GazeDialog**

确保这两个对话框继续使用无边框样式：

```python
# src/ui/dialogs/stand_dialog.py
class StandReminderDialog(BaseReminderDialog):
    def __init__(self, duration: int, parent=None):
        self.duration = duration
        super().__init__(parent, has_title_bar=False)  # 明确指定无边框
```

```python
# src/ui/dialogs/gaze_dialog.py
class GazeReminderDialog(BaseReminderDialog):
    def __init__(self, duration: int, parent=None):
        self.duration = duration
        super().__init__(parent, has_title_bar=False)  # 明确指定无边框
```

**Step 4: 设置微运动弹窗大小**

按设计文档，微运动弹窗应为 800x600px。在 `exercise_dialog.py` 修改：

```python
def __init__(self, exercises: list, weight_kg: float = 70.0, parent=None):
    # ... existing code ...
    super().__init__(parent, has_title_bar=True)

    # 设置固定大小（覆盖基类的默认大小）
    self.setFixedSize(800, 600)

    # ... rest of code ...
```

**Step 5: 运行测试**

Run: `pytest tests/test_dialogs.py -v`
Expected: 所有对话框测试通过

**Step 6: 提交**

```bash
git add src/ui/dialogs/base_dialog.py src/ui/dialogs/exercise_dialog.py src/ui/dialogs/stand_dialog.py src/ui/dialogs/gaze_dialog.py
git commit -m "feat: 微运动弹窗添加标题栏，保持站立/远眺无边框"
```

---

## Task 4: 添加倒计时<10秒红色闪烁效果

**问题:** 设计要求<10秒时红色闪烁，当前仅变色

**Files:**
- Modify: `src/ui/dialogs/base_dialog.py`
- Test: `tests/test_dialogs.py`

**Step 1: 在BaseReminderDialog添加闪烁动画**

修改 `src/ui/dialogs/base_dialog.py`：

```python
from PySide6.QtCore import QPropertyAnimation, QEasingCurve

class BaseReminderDialog(QDialog):
    # ... existing code ...

    def __init__(self, parent=None, has_title_bar: bool = False):
        super().__init__(parent)
        self._has_title_bar = has_title_bar

        # 倒计时相关
        self.countdown_timer = CountdownTimer(self)
        self.countdown_timer.tick.connect(self._on_countdown_tick)
        self.countdown_timer.finished.connect(self._on_countdown_complete)

        # 动画相关
        self.fade_animation = None
        self.pulse_animation = None  # 新增：闪烁动画

        # ... rest of existing code ...
```

添加闪烁方法：

```python
def _start_pulse_animation(self):
    """开始红色闪烁动画（最后10秒）"""
    if self.pulse_animation:
        self.pulse_animation.stop()

    self.pulse_animation = QPropertyAnimation(self, b"windowOpacity")
    self.pulse_animation.setDuration(400)  # 400ms per cycle
    self.pulse_animation.setStartValue(1.0)
    self.pulse_animation.setEndValue(0.7)
    self.pulse_animation.setLoopCount(-1)  # 无限循环
    self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    self.pulse_animation.start()

def _stop_pulse_animation(self):
    """停止闪烁动画"""
    if self.pulse_animation:
        self.pulse_animation.stop()
        self.pulse_animation = None
        self.setWindowOpacity(1.0)
```

修改 `_on_countdown_tick` 方法：

```python
def _on_countdown_tick(self, remaining: int):
    """
    倒计时每秒触发

    Args:
        remaining: 剩余秒数
    """
    self.remaining_seconds = remaining
    self._update_countdown_display()

    # 最后10秒播放提示音
    if remaining <= 10 and remaining > 0:
        self.audio_manager.play("tick")

        # 开始红色闪烁动画
        if remaining == 10:
            self._start_pulse_animation()

    # 停止闪烁动画（如果从10秒以上回到11秒）
    if remaining > 10:
        self._stop_pulse_animation()
```

修改 `_on_countdown_complete` 方法：

```python
def _on_countdown_complete(self):
    """倒计时完成"""
    # 停止闪烁动画
    self._stop_pulse_animation()

    # 播放完成音
    self.audio_manager.play("complete")

    # 显示完成反馈
    self._show_complete_feedback()

    # 发送完成信号
    self.completed.emit()

    # 延迟关闭（1秒后自动关闭）
    QTimer.singleShot(1000, self._close_with_animation)
```

**Step 2: 测试闪烁效果**

创建测试文件验证闪烁逻辑：

```python
# tests/test_countdown_pulse.py
import pytest
from unittest.mock import Mock, patch
from PySide6.QtWidgets import QApplication
from src.ui.dialogs.base_dialog import BaseReminderDialog

@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])

def test_pulse_animation_starts_at_10_seconds(app):
    """测试倒计时到10秒时开始闪烁"""
    dialog = BaseReminderDialog()
    dialog.remaining_seconds = 30
    dialog.duration = 30

    # 模拟倒计时到10秒
    dialog._on_countdown_tick(10)

    # 验证闪烁动画已启动
    assert dialog.pulse_animation is not None
    assert dialog.pulse_animation.state() == QPropertyAnimation.State.Running

def test_pulse_animation_stops_above_10_seconds(app):
    """测试倒计时大于10秒时停止闪烁"""
    dialog = BaseReminderDialog()
    dialog._start_pulse_animation()  # 先启动动画

    # 模拟倒计时到11秒
    dialog._on_countdown_tick(11)

    # 验证闪烁动画已停止
    assert dialog.pulse_animation is None

def test_pulse_animation_stops_on_complete(app):
    """测试倒计时完成时停止闪烁"""
    dialog = BaseReminderDialog()
    dialog._start_pulse_animation()  # 先启动动画

    # 模拟倒计时完成
    dialog._on_countdown_complete()

    # 验证闪烁动画已停止
    assert dialog.pulse_animation is None
```

**Step 3: 运行测试**

Run: `pytest tests/test_countdown_pulse.py -v`
Expected: 所有闪烁测试通过

**Step 4: 提交**

```bash
git add src/ui/dialogs/base_dialog.py tests/test_countdown_pulse.py
git commit -m "feat: 添加倒计时<10秒红色闪烁效果"
```

---

## Task 5: 验证所有弹窗尺寸规范

**问题:** 确保所有弹窗尺寸符合设计文档

**Files:**
- Modify: `src/ui/dialogs/stand_dialog.py`
- Modify: `src/ui/dialogs/gaze_dialog.py`
- Test: `tests/test_dialog_sizes.py`

**设计文档要求尺寸:**
- 站立弹窗: 屏幕宽 × 60%，屏幕高 × 50%
- 微运动弹窗: 800 × 600 px
- 远眺弹窗: 屏幕宽 × 50%，屏幕高 × 40%

**Step 1: 检查并修正站立弹窗尺寸**

`src/ui/dialogs/stand_dialog.py` 当前使用基类的 `_set_standard_size()` (50% x 45%)，需要改为60% x 50%：

```python
def __init__(self, duration: int, parent=None):
    self.duration = duration
    super().__init__(parent, has_title_bar=False)

    # 覆盖基类默认尺寸
    screen = QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()

    width = int(screen_geometry.width() * 0.60)  # 60%
    height = int(screen_geometry.height() * 0.50)  # 50%

    self.setFixedSize(width, height)

    # ... rest of code ...
```

**Step 2: 检查并修正远眺弹窗尺寸**

`src/ui/dialogs/gaze_dialog.py` 需要改为50% x 40%：

```python
def __init__(self, duration: int, parent=None):
    self.duration = duration
    super().__init__(parent, has_title_bar=False)

    # 覆盖基类默认尺寸
    screen = QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()

    width = int(screen_geometry.width() * 0.50)  # 50%
    height = int(screen_geometry.height() * 0.40)  # 40%

    self.setFixedSize(width, height)

    # ... rest of code ...
```

**Step 3: 创建尺寸验证测试**

```python
# tests/test_dialog_sizes.py
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.ui.dialogs.stand_dialog import StandReminderDialog
from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog
from src.ui.dialogs.gaze_dialog import GazeReminderDialog

@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])

@pytest.fixture
def screen_geometry(app):
    return QApplication.primaryScreen().availableGeometry()

def test_stand_dialog_size(app, screen_geometry):
    """测试站立弹窗尺寸为屏幕的60% x 50%"""
    dialog = StandReminderDialog(90)

    expected_width = int(screen_geometry.width() * 0.60)
    expected_height = int(screen_geometry.height() * 0.50)

    assert dialog.width() == expected_width
    assert dialog.height() == expected_height

def test_exercise_dialog_size(app):
    """测试微运动弹窗尺寸为800 x 600"""
    exercises = [{"name": "开合跳", "duration": 30, "met": 5.0}]
    dialog = ExerciseReminderDialog(exercises, 70.0)

    assert dialog.width() == 800
    assert dialog.height() == 600

def test_gaze_dialog_size(app, screen_geometry):
    """测试远眺弹窗尺寸为屏幕的50% x 40%"""
    dialog = GazeReminderDialog(60)

    expected_width = int(screen_geometry.width() * 0.50)
    expected_height = int(screen_geometry.height() * 0.40)

    assert dialog.width() == expected_width
    assert dialog.height() == expected_height
```

**Step 4: 运行测试**

Run: `pytest tests/test_dialog_sizes.py -v`
Expected: 所有尺寸测试通过

**Step 5: 提交**

```bash
git add src/ui/dialogs/stand_dialog.py src/ui/dialogs/gaze_dialog.py tests/test_dialog_sizes.py
git commit -m "fix: 修正所有弹窗尺寸符合设计规范"
```

---

## Task 6: 更新向导测试以匹配3页结构

**问题:** 测试仍然假设4页结构

**Files:**
- Modify: `tests/test_wizard.py`
- Test: `tests/test_wizard.py`

**Step 1: 更新页面ID引用**

修改 `tests/test_wizard.py` 中所有页面ID引用：

```python
# 旧代码
wizard.welcome_page_id
# 改为
wizard.profile_page_id

# 旧代码
assert wizard.currentId() == 1  # profile page
# 改为
assert wizard.currentId() == 0  # profile page is now first

# 旧代码
assert wizard.currentId() == 2  # settings page
# 改为
assert wizard.currentId() == 1  # settings page is now second

# 旧代码
assert wizard.currentId() == 3  # experience page
# 改为
assert wizard.currentId() == 2  # experience page is now third
```

**Step 2: 更新欢迎页相关测试**

删除或重命名与欢迎页相关的测试：

```python
# 删除
def test_welcome_page_shows():
    """测试欢迎页显示"""
    # 这个测试需要删除，因为欢迎页已不存在
```

**Step 3: 运行测试**

Run: `pytest tests/test_wizard.py -v`
Expected: 所有测试通过

**Step 4: 提交**

```bash
git add tests/test_wizard.py
git commit -m "test: 更新向导测试以匹配3页结构"
```

---

## Task 7: 完整集成测试

**问题:** 确保所有修改协同工作

**Files:**
- Create: `tests/test_ui_design_compliance.py`
- Test: `tests/test_ui_design_compliance.py`

**Step 1: 创建设计规范合规性测试**

```python
# tests/test_ui_design_compliance.py
# -*- coding: utf-8 -*-
"""
UI设计规范合规性测试

验证实现符合 DESIGN-UI-001.md 设计文档要求
"""
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.ui.wizards.first_run_wizard import FirstRunWizard
from src.ui.dialogs.stand_dialog import StandReminderDialog
from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog
from src.ui.dialogs.gaze_dialog import GazeReminderDialog


@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])


class TestWizardDesign:
    """向导设计规范测试"""

    def test_wizard_has_3_pages(self, app):
        """设计4.2节: 向导应为3页"""
        wizard = FirstRunWizard()
        assert wizard.pageIds()[0] == 0  # ProfilePage
        assert wizard.pageIds()[1] == 1  # ReminderSettingsPage
        assert wizard.pageIds()[2] == 2  # ExperiencePage
        assert len(wizard.pageIds()) == 3

    def test_first_page_is_profile(self, app):
        """设计4.2节: 第1页应为个人基础设置页"""
        wizard = FirstRunWizard()
        wizard.setStartId(0)
        assert "个人基础设置" in wizard.currentPage().title()


class TestDialogDesign:
    """弹窗设计规范测试"""

    def test_stand_dialog_has_no_title_bar(self, app):
        """设计5.1节: 站立弹窗应无边框"""
        dialog = StandReminderDialog(90)
        flags = dialog.windowFlags()
        assert flags & Qt.WindowType.FramelessWindowHint

    def test_exercise_dialog_has_title_bar(self, app):
        """设计5.2节: 微运动弹窗应有标题栏"""
        exercises = [{"name": "开合跳", "duration": 30, "met": 5.0}]
        dialog = ExerciseReminderDialog(exercises, 70.0)
        flags = dialog.windowFlags()
        assert not (flags & Qt.WindowType.FramelessWindowHint)

    def test_all_dialogs_stay_on_top(self, app):
        """设计10.1节: 所有弹窗应强制置顶"""
        stand = StandReminderDialog(90)
        exercises = [{"name": "开合跳", "duration": 30, "met": 5.0}]
        exercise = ExerciseReminderDialog(exercises, 70.0)
        gaze = GazeReminderDialog(60)

        for dialog in [stand, exercise, gaze]:
            flags = dialog.windowFlags()
            assert flags & Qt.WindowType.WindowStaysOnTopHint


class TestCountdownColors:
    """倒计时颜色规范测试"""

    def test_countdown_color_above_50_percent(self, app):
        """设计10.3节: >50% 时间应为绿色"""
        from src.ui.dialogs.stand_dialog import StandReminderDialog
        dialog = StandReminderDialog(100)
        color = dialog.get_countdown_color(60, 100)
        assert color == "#4CAF50"

    def test_countdown_color_30_to_50_percent(self, app):
        """设计10.3节: 30-50% 时间应为黄色"""
        from src.ui.dialogs.stand_dialog import StandReminderDialog
        dialog = StandReminderDialog(100)
        color = dialog.get_countdown_color(40, 100)
        assert color == "#FFC107"

    def test_countdown_color_10_to_30_percent(self, app):
        """设计10.3节: 10-30% 时间应为橙色"""
        from src.ui.dialogs.stand_dialog import StandReminderDialog
        dialog = StandReminderDialog(100)
        color = dialog.get_countdown_color(15, 100)
        assert color == "#FF9800"

    def test_countdown_color_below_10_seconds(self, app):
        """设计10.3节: <10秒应为红色"""
        from src.ui.dialogs.stand_dialog import StandReminderDialog
        dialog = StandReminderDialog(100)
        color = dialog.get_countdown_color(9, 100)
        assert color == "#F44336"
```

**Step 2: 运行完整测试套件**

Run: `pytest tests/ -v --tb=short`
Expected: 所有测试通过

**Step 3: 最终提交**

```bash
git add tests/test_ui_design_compliance.py
git commit -m "test: 添加UI设计规范合规性测试"
```

---

## 总结

完成以上7个任务后，UI实现将与 [DESIGN-UI-001.md](DESIGN-UI-001.md) 设计文档完全一致：

✅ 向导简化为3页
✅ 个人基础设置页按设计文档布局
✅ 微运动弹窗有标题栏
✅ 站立/远眺弹窗无边框
✅ 倒计时<10秒红色闪烁
✅ 所有弹窗尺寸符合规范
✅ 设计规范合规性测试

**执行顺序建议:** Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7
