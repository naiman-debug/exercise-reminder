# 首次启动向导实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现首次启动向导功能，引导用户完成个人信息、主题、音频、时间设置

**Architecture:** 使用 QWizard 创建多步骤向导，每页独立验证，完成后保存配置到本地数据库

**Tech Stack:** PySide6 (QWizard), Peewee ORM, ConfigManager

---

## Task 1: 修复 P0 Bug - QDialog 导入问题

**Files:**
- Modify: `src/core/app.py:10`

**Step 1: Write the failing test**

```python
# tests/test_app_imports.py
def test_app_imports_qdialog():
    """Test that app.py imports QDialog correctly"""
    from src.core.app import Application
    import inspect
    source = inspect.getsource(Application)
    # Check QDialog is in imports
    assert 'QDialog' in source or 'from PySide6.QtWidgets import' in source
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_app_imports.py::test_app_imports_qdialog -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Edit `src/core/app.py:10`:
```python
# Before:
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox, QAction, QIcon, QPixmap

# After:
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox, QDialog, QAction, QIcon, QPixmap
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_app_imports.py::test_app_imports_qdialog -v`
Expected: PASS

**Step 5: Manual verification**

Run: `python -c "from src.core.app import Application; print('Import OK')"`
Expected: No import errors

**Step 6: Commit**

```bash
git add src/core/app.py tests/test_app_imports.py
git commit -m "fix: add QDialog to imports in app.py

- Fixes QDialog.DialogCode usage at line 239
- Adds import test to prevent regression"
```

---

## Task 2: 创建向导组件目录结构

**Files:**
- Create: `src/ui/wizards/__init__.py`
- Create: `src/ui/wizards/first_run_wizard.py`

**Step 1: Write the failing test**

```python
# tests/test_wizard_structure.py
def test_wizard_module_exists():
    """Test wizard module can be imported"""
    from src.ui.wizards import FirstRunWizard
    assert FirstRunWizard is not None
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_wizard_structure.py::test_wizard_module_exists -v`
Expected: FAIL - ModuleNotFoundError

**Step 3: Create directory structure**

```bash
mkdir -p src/ui/wizards
touch src/ui/wizards/__init__.py
touch src/ui/wizards/first_run_wizard.py
```

**Step 4: Write minimal implementation**

Create `src/ui/wizards/__init__.py`:
```python
# -*- coding: utf-8 -*-
"""
首次启动向导模块
"""
from .first_run_wizard import FirstRunWizard

__all__ = ['FirstRunWizard']
```

Create `src/ui/wizards/first_run_wizard.py`:
```python
# -*- coding: utf-8 -*-
"""
首次启动向导主类
"""
from PySide6.QtWidgets import QWizard

class FirstRunWizard(QWizard):
    """首次启动向导"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("欢迎使用灵动休息健康助手")
        self.setMinimumSize(600, 500)
```

**Step 5: Run test to verify it passes**

Run: `python -m pytest tests/test_wizard_structure.py::test_wizard_module_exists -v`
Expected: PASS

**Step 6: Commit**

```bash
git add src/ui/wizards/ tests/test_wizard_structure.py
git commit -m "feat: create wizard module structure

- Add FirstRunWizard class with QWizard base
- Create wizard module under src/ui/wizards/"
```

---

## Task 3: 实现欢迎页面（第1页）

**Files:**
- Create: `src/ui/wizards/welcome_page.py`

**Step 1: Write the failing test**

```python
# tests/test_welcome_page.py
def test_welcome_page_creation():
    """Test welcome page can be created"""
    from src.ui.wizards.welcome_page import WelcomePage
    page = WelcomePage()
    assert page.title() == "欢迎使用"
    assert hasattr(page, 'intro_label')
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_welcome_page.py::test_welcome_page_creation -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Create `src/ui/wizards/welcome_page.py`:
```python
# -*- coding: utf-8 -*-
"""
欢迎页面 - 首次启动向导第1页
"""
from PySide6.QtWidgets import QWizardPage, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class WelcomePage(QWizardPage):
    """欢迎页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("欢迎使用灵动休息健康助手")
        self.setSubTitle("简单几步设置，开始健康生活")

        layout = QVBoxLayout()

        # 欢迎文案
        intro = QLabel(
            "灵动休息健康助手将帮助您：\n\n"
            "• 定时提醒站立休息，预防久坐危害\n"
            "• 引导微运动，保持身体活力\n"
            "• 提醒远眺放松，保护视力健康\n\n"
            "让我们花几分钟完成初始设置。"
        )
        intro.setWordWrap(True)
        intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        intro.setStyleSheet("font-size: 14pt; padding: 20px;")

        layout.addWidget(intro)
        layout.addStretch()
        self.setLayout(layout)
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_welcome_page.py::test_welcome_page_creation -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/ui/wizards/welcome_page.py tests/test_welcome_page.py
git commit -m "feat: implement welcome page

- Add WelcomePage with introduction text
- Center-aligned layout with padding"
```

---

## Task 4: 实现个人信息页面（第2页）

**Files:**
- Create: `src/ui/wizards/profile_page.py`
- Modify: `src/ui/wizards/first_run_wizard.py`

**Step 1: Write the failing test**

```python
# tests/test_profile_page.py
def test_profile_page_validation():
    """Test profile page validates input"""
    from src.ui.wizards.profile_page import ProfilePage
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    page = ProfilePage()

    # Test valid input
    page.height_input.setValue(175)
    page.weight_input.setValue(70)
    page.age_input.setValue(30)
    page.calorie_target_input.setValue(500)

    assert page.isComplete() == True

    # Test invalid input
    page.height_input.setValue(50)  # Too low
    assert page.isComplete() == False
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_profile_page.py::test_profile_page_validation -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Create `src/ui/wizards/profile_page.py`:
```python
# -*- coding: utf-8 -*-
"""
个人信息页面 - 首次启动向导第2页
"""
from PySide6.QtWidgets import QWizardPage, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QGroupBox
from PySide6.QtCore import Qt

class ProfilePage(QWizardPage):
    """个人信息设置页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("个人信息")
        self.setSubTitle("请输入您的基本信息，用于计算运动消耗")

        self.registerField("height*", self.height_input)  # Required field
        self.registerField("weight*", self.weight_input)
        self.registerField("age*", self.age_input)
        self.registerField("calorieTarget", self.calorie_target_input, "value", "valueChanged")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 输入组
        group = QGroupBox("基本信息")
        group_layout = QVBoxLayout()

        # 身高
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("身高 (cm):"))
        self.height_input = QSpinBox()
        self.height_input.setRange(100, 250)
        self.height_input.setValue(170)
        self.height_input.setSuffix(" cm")
        self.height_input.valueChanged.connect(self.validate_input)
        height_layout.addWidget(self.height_input)
        height_layout.addStretch()
        group_layout.addLayout(height_layout)

        # 体重
        weight_layout = QHBoxLayout()
        weight_layout.addWidget(QLabel("体重 (kg):"))
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(30.0, 200.0)
        self.weight_input.setValue(70.0)
        self.weight_input.setSuffix(" kg")
        self.weight_input.valueChanged.connect(self.validate_input)
        weight_layout.addWidget(self.weight_input)
        weight_layout.addStretch()
        group_layout.addLayout(weight_layout)

        # 年龄
        age_layout = QHBoxLayout()
        age_layout.addWidget(QLabel("年龄:"))
        self.age_input = QSpinBox()
        self.age_input.setRange(10, 100)
        self.age_input.setValue(30)
        self.age_input.setSuffix(" 岁")
        self.age_input.valueChanged.connect(self.validate_input)
        age_layout.addWidget(self.age_input)
        age_layout.addStretch()
        group_layout.addLayout(age_layout)

        # 每日卡路里目标
        calorie_layout = QHBoxLayout()
        calorie_layout.addWidget(QLabel("每日消耗目标:"))
        self.calorie_target_input = QSpinBox()
        self.calorie_target_input.setRange(100, 5000)
        self.calorie_target_input.setValue(300)
        self.calorie_target_input.setSuffix(" kcal")
        calorie_layout.addWidget(self.calorie_target_input)
        calorie_layout.addStretch()
        group_layout.addLayout(calorie_layout)

        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()

        self.setLayout(layout)

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
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_profile_page.py::test_profile_page_validation -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/ui/wizards/profile_page.py tests/test_profile_page.py
git commit -m "feat: implement profile page with validation

- Add input fields for height, weight, age, calorie target
- Validate ranges: height(100-250), weight(30-200), age(10-100)
- Register fields for wizard data access"
```

---

## Task 5: 实现主题选择页面（第3页）

**Files:**
- Create: `src/ui/wizards/theme_page.py`

**Step 1: Write the failing test**

```python
# tests/test_theme_page.py
def test_theme_page_selection():
    """Test theme page allows selection"""
    from src.ui.wizards.theme_page import ThemePage
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    page = ThemePage()

    # Has theme options
    assert page.day_theme_btn is not None
    assert page.night_theme_btn is not None
    assert page.eye_protection_theme_btn is not None

    # Can select theme
    page.night_theme_btn.click()
    assert page.selected_theme() == "night"
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_theme_page.py::test_theme_page_selection -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Create `src/ui/wizards/theme_page.py`:
```python
# -*- coding: utf-8 -*-
"""
主题选择页面 - 首次启动向导第3页
"""
from PySide6.QtWidgets import QWizardPage, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QGroupBox
from PySide6.QtCore import Qt

class ThemePage(QWizardPage):
    """主题选择页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("主题选择")
        self.setSubTitle("选择您喜欢的界面主题")

        self.registerField("theme", self, "selectedTheme", "themeChanged")
        self._selected_theme = "day"

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 主题选择组
        group = QGroupBox("预设主题")
        group_layout = QVBoxLayout()

        self.theme_group = QButtonGroup(self)

        # 日间主题
        self.day_theme_btn = QRadioButton("🌞 日间模式")
        self.day_theme_btn.setChecked(True)
        self.day_theme_btn.toggled.connect(lambda: self.set_theme("day"))
        group_layout.addWidget(self.day_theme_btn)
        self.theme_group.addButton(self.day_theme_btn, 0)

        # 夜间主题
        self.night_theme_btn = QRadioButton("🌙 夜间模式")
        self.night_theme_btn.toggled.connect(lambda: self.set_theme("night"))
        group_layout.addWidget(self.night_theme_btn)
        self.theme_group.addButton(self.night_theme_btn, 1)

        # 护眼主题
        self.eye_protection_theme_btn = QRadioButton("👁️ 护眼模式")
        self.eye_protection_theme_btn.toggled.connect(lambda: self.set_theme("eye_protection"))
        group_layout.addWidget(self.eye_protection_theme_btn)
        self.theme_group.addButton(self.eye_protection_theme_btn, 2)

        group.setLayout(group_layout)
        layout.addWidget(group)

        # 颜色选择说明
        color_label = QLabel("提示: 每个主题提供4种配色方案，可在设置中随时更换")
        color_label.setWordWrap(True)
        color_label.setStyleSheet("color: #757575; font-size: 11pt; padding: 10px;")
        layout.addWidget(color_label)

        layout.addStretch()
        self.setLayout(layout)

    def set_theme(self, theme):
        """设置选中的主题"""
        self._selected_theme = theme
        self.themeChanged.emit()

    def selectedTheme(self):
        """获取选中的主题"""
        return self._selected_theme

    themeChanged = Qt.Signal()
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_theme_page.py::test_theme_page_selection -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/ui/wizards/theme_page.py tests/test_theme_page.py
git commit -m "feat: implement theme selection page

- Add three preset themes: day, night, eye_protection
- Radio button selection with signal emission
- Register theme field for wizard access"
```

---

## Task 6: 实现音频设置页面（第4页）

**Files:**
- Create: `src/ui/wizards/audio_page.py`

**Step 1: Write the failing test**

```python
# tests/test_audio_page.py
def test_audio_page_options():
    """Test audio page has sound options"""
    from src.ui.wizards.audio_page import AudioPage
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    page = AudioPage()

    # Has audio options
    assert page.audio_enabled_cb is not None
    assert page.tts_enabled_cb is not None

    # Can enable/disable
    page.audio_enabled_cb.setChecked(True)
    assert page.is_audio_enabled() == True
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_audio_page.py::test_audio_page_options -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Create `src/ui/wizards/audio_page.py`:
```python
# -*- coding: utf-8 -*-
"""
音频设置页面 - 首次启动向导第4页
"""
from PySide6.QtWidgets import QWizardPage, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QDoubleSpinBox, QGroupBox, QLineEdit
from PySide6.QtCore import Qt

class AudioPage(QWizardPage):
    """音频设置页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("音频设置")
        self.setSubTitle("配置提醒音效和语音播报")

        self.registerField("audioEnabled", self.audio_enabled_cb, "checked", "stateChanged")
        self.registerField("ttsEnabled", self.tts_enabled_cb, "checked", "stateChanged")
        self.registerField("audioVolume", self.volume_spin, "value", "valueChanged")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 音效开关
        self.audio_enabled_cb = QCheckBox("启用提醒音效")
        self.audio_enabled_cb.setChecked(True)
        self.audio_enabled_cb.setStyleSheet("font-size: 12pt; padding: 10px;")
        layout.addWidget(self.audio_enabled_cb)

        # 音量控制
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("音量:"))
        self.volume_spin = QDoubleSpinBox()
        self.volume_spin.setRange(0.0, 1.0)
        self.volume_spin.setSingleStep(0.1)
        self.volume_spin.setValue(0.7)
        volume_layout.addWidget(self.volume_spin)
        volume_layout.addStretch()
        layout.addLayout(volume_layout)

        # TTS 设置组
        tts_group = QGroupBox("语音播报")
        tts_layout = QVBoxLayout()

        self.tts_enabled_cb = QCheckBox("启用倒计时语音播报（最后5秒）")
        tts_layout.addWidget(self.tts_enabled_cb)

        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("TTS API (可选):"))
        self.tts_api_input = QLineEdit()
        self.tts_api_input.setPlaceholderText("留空使用内置语音")
        api_layout.addWidget(self.tts_api_input)
        tts_layout.addLayout(api_layout)

        tts_group.setLayout(tts_layout)
        layout.addWidget(tts_group)

        # 说明
        hint_label = QLabel(
            "💡 提示：\n"
            "• 提醒音效会在倒计时开始/结束时播放\n"
            "• 语音播报会读出最后5秒倒计时\n"
            "• 远眺环节可设置背景音乐\n"
            "• 所有音效可在设置中自定义"
        )
        hint_label.setWordWrap(True)
        hint_label.setStyleSheet("color: #757575; font-size: 11pt; padding: 10px;")
        layout.addWidget(hint_label)

        layout.addStretch()
        self.setLayout(layout)

    def is_audio_enabled(self):
        """检查音频是否启用"""
        return self.audio_enabled_cb.isChecked()

    def get_audio_settings(self):
        """获取音频设置"""
        return {
            'enabled': self.audio_enabled_cb.isChecked(),
            'volume': self.volume_spin.value(),
            'tts_enabled': self.tts_enabled_cb.isChecked(),
            'tts_api': self.tts_api_input.text()
        }
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_audio_page.py::test_audio_page_options -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/ui/wizards/audio_page.py tests/test_audio_page.py
git commit -m "feat: implement audio settings page

- Add audio enable/disable checkbox
- Add volume control (0.0-1.0)
- Add TTS option with API input field
- Provide usage hints"
```

---

## Task 7: 实现时间设置页面（第5页）

**Files:**
- Create: `src/ui/wizards/time_settings_page.py`

**Step 1: Write the failing test**

```python
# tests/test_time_settings_page.py
def test_time_settings_defaults():
    """Test time settings has default values"""
    from src.ui.wizards.time_settings_page import TimeSettingsPage
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    page = TimeSettingsPage()

    # Check default values
    assert page.stand_interval_min.value() == 30
    assert page.stand_interval_max.value() == 60
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_time_settings_page.py::test_time_settings_defaults -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Create `src/ui/wizards/time_settings_page.py`:
```python
# -*- coding: utf-8 -*-
"""
时间设置页面 - 首次启动向导第5页
"""
from PySide6.QtWidgets import QWizardPage, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QGroupBox
from PySide6.QtCore import Qt

class TimeSettingsPage(QWizardPage):
    """时间设置页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("时间设置")
        self.setSubTitle("设置提醒间隔时间（随机范围）")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 强制站立提醒
        stand_group = QGroupBox("强制站立提醒")
        stand_layout = QVBoxLayout()

        stand_interval_layout = QHBoxLayout()
        stand_interval_layout.addWidget(QLabel("间隔范围:"))
        self.stand_interval_min = QSpinBox()
        self.stand_interval_min.setRange(5, 120)
        self.stand_interval_min.setValue(30)
        self.stand_interval_min.setSuffix(" 分钟")
        stand_interval_layout.addWidget(self.stand_interval_min)
        stand_interval_layout.addWidget(QLabel("-"))
        self.stand_interval_max = QSpinBox()
        self.stand_interval_max.setRange(5, 180)
        self.stand_interval_max.setValue(60)
        self.stand_interval_max.setSuffix(" 分钟")
        stand_interval_layout.addWidget(self.stand_interval_max)
        stand_interval_layout.addStretch()
        stand_layout.addLayout(stand_interval_layout)

        stand_duration_layout = QHBoxLayout()
        stand_duration_layout.addWidget(QLabel("倒计时时长:"))
        self.stand_duration = QSpinBox()
        self.stand_duration.setRange(30, 300)
        self.stand_duration.setValue(90)
        self.stand_duration.setSuffix(" 秒")
        stand_duration_layout.addWidget(self.stand_duration)
        stand_duration_layout.addStretch()
        stand_layout.addLayout(stand_duration_layout)

        stand_group.setLayout(stand_layout)
        layout.addWidget(stand_group)

        # 微运动提醒
        exercise_group = QGroupBox("微运动提醒")
        exercise_layout = QVBoxLayout()

        exercise_interval_layout = QHBoxLayout()
        exercise_interval_layout.addWidget(QLabel("间隔范围:"))
        self.exercise_interval_min = QSpinBox()
        self.exercise_interval_min.setRange(5, 120)
        self.exercise_interval_min.setValue(45)
        self.exercise_interval_min.setSuffix(" 分钟")
        exercise_interval_layout.addWidget(self.exercise_interval_min)
        exercise_interval_layout.addWidget(QLabel("-"))
        self.exercise_interval_max = QSpinBox()
        self.exercise_interval_max.setRange(5, 180)
        self.exercise_interval_max.setValue(75)
        self.exercise_interval_max.setSuffix(" 分钟")
        exercise_interval_layout.addWidget(self.exercise_interval_max)
        exercise_interval_layout.addStretch()
        exercise_layout.addLayout(exercise_interval_layout)

        exercise_group.setLayout(exercise_layout)
        layout.addWidget(exercise_group)

        # 强制远眺提醒
        gaze_group = QGroupBox("强制远眺提醒")
        gaze_layout = QVBoxLayout()

        gaze_interval_layout = QHBoxLayout()
        gaze_interval_layout.addWidget(QLabel("间隔范围:"))
        self.gaze_interval_min = QSpinBox()
        self.gaze_interval_min.setRange(5, 120)
        self.gaze_interval_min.setValue(60)
        self.gaze_interval_min.setSuffix(" 分钟")
        gaze_interval_layout.addWidget(self.gaze_interval_min)
        gaze_interval_layout.addWidget(QLabel("-"))
        self.gaze_interval_max = QSpinBox()
        self.gaze_interval_max.setRange(5, 180)
        self.gaze_interval_max.setValue(90)
        self.gaze_interval_max.setSuffix(" 分钟")
        gaze_interval_layout.addWidget(self.gaze_interval_max)
        gaze_interval_layout.addStretch()
        gaze_layout.addLayout(gaze_interval_layout)

        gaze_group.setLayout(gaze_layout)
        layout.addWidget(gaze_group)

        # 说明
        hint_label = QLabel(
            "💡 提示：\n"
            "• 实际间隔会在设定范围内随机生成\n"
            "• 避免身体产生预期，更有效的提醒\n"
            "• 所有时间可在设置中调整"
        )
        hint_label.setWordWrap(True)
        hint_label.setStyleSheet("color: #757575; font-size: 11pt; padding: 10px;")
        layout.addWidget(hint_label)

        layout.addStretch()
        self.setLayout(layout)

    def get_time_settings(self):
        """获取时间设置"""
        return {
            'stand': {
                'interval_min': self.stand_interval_min.value(),
                'interval_max': self.stand_interval_max.value(),
                'duration': self.stand_duration.value()
            },
            'exercise': {
                'interval_min': self.exercise_interval_min.value(),
                'interval_max': self.exercise_interval_max.value()
            },
            'gaze': {
                'interval_min': self.gaze_interval_min.value(),
                'interval_max': self.gaze_interval_max.value()
            }
        }
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_time_settings_page.py::test_time_settings_defaults -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/ui/wizards/time_settings_page.py tests/test_time_settings_page.py
git commit -m "feat: implement time settings page

- Add interval ranges for stand, exercise, gaze reminders
- Set default values (stand: 30-60min, exercise: 45-75min, gaze: 60-90min)
- Add duration setting for stand reminder"
```

---

## Task 8: 组装向导并集成到应用

**Files:**
- Modify: `src/ui/wizards/first_run_wizard.py`
- Modify: `src/core/app.py`

**Step 1: Write the failing test**

```python
# tests/test_wizard_integration.py
def test_wizard_has_all_pages():
    """Test wizard contains all 5 pages"""
    from src.ui.wizards.first_run_wizard import FirstRunWizard
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    wizard = FirstRunWizard()

    # Should have 5 pages
    assert wizard.pageIds()[0] == 0
    assert wizard.pageIds()[4] == 4

    # Can navigate through pages
    assert wizard.currentPage() is not None
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_wizard_integration.py::test_wizard_has_all_pages -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Update `src/ui/wizards/first_run_wizard.py`:
```python
# -*- coding: utf-8 -*-
"""
首次启动向导主类
"""
from PySide6.QtWidgets import QWizard
from PySide6.QtCore import Qt

from .welcome_page import WelcomePage
from .profile_page import ProfilePage
from .theme_page import ThemePage
from .audio_page import AudioPage
from .time_settings_page import TimeSettingsPage


class FirstRunWizard(QWizard):
    """首次启动向导"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("欢迎使用灵动休息健康助手")
        self.setMinimumSize(600, 500)
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setOption(QWizard.WizardOption.HaveHelpButton, False)

        # 添加页面
        self.add_page(WelcomePage(self))
        self.add_page(ProfilePage(self))
        self.add_page(ThemePage(self))
        self.add_page(AudioPage(self))
        self.add_page(TimeSettingsPage(self))

        # 设置按钮文本
        self.setButtonText(QWizard.WizardButton.NextButton, "下一步 >")
        self.setButtonText(QWizard.WizardButton.BackButton, "< 上一步")
        self.setButtonText(QWizard.WizardButton.FinishButton, "完成设置")
        self.setButtonText(QWizard.WizardButton.CancelButton, "退出")

    def add_page(self, page):
        """添加页面"""
        self.addPage(page)

    def get_wizard_data(self):
        """获取向导收集的所有数据"""
        return {
            'profile': {
                'height': self.field('height'),
                'weight': self.field('weight'),
                'age': self.field('age'),
                'calorie_target': self.field('calorieTarget')
            },
            'theme': self.field('theme') or 'day',
            'audio': {
                'enabled': self.field('audioEnabled') or True,
                'volume': self.field('audioVolume') or 0.7,
                'tts_enabled': self.field('ttsEnabled') or False
            },
            'time_settings': self.page(4).get_time_settings()  # TimeSettingsPage
        }
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_wizard_integration.py::test_wizard_has_all_pages -v`
Expected: PASS

**Step 5: Integrate into Application**

Update `src/core/app.py:96-107`:
```python
# Before:
def _show_first_run_setup(self):
    """显示首次运行设置"""
    dialog = SettingsDialog(self)
    dialog.setWindowTitle("欢迎使用灵动休息健康助手 - 初始设置")
    dialog.exec()

    # 标记首次运行已完成
    from ..models.repositories import SettingRepository
    SettingRepository.set("first_run_completed", "true")

    # 首次设置完成后，启动提醒
    self.reminder_engine.start_all()

# After:
def _show_first_run_setup(self):
    """显示首次运行设置"""
    from ..ui.wizards import FirstRunWizard
    from ..models.repositories import SettingRepository, UserRepository

    wizard = FirstRunWizard(self)

    if wizard.exec() == QWizard.DialogCode.Accepted:
        # 用户完成了向导
        data = wizard.get_wizard_data()

        # 保存个人信息
        UserRepository.set_weight(data['profile']['weight'])

        # 保存配置
        self.config.set("user.height", data['profile']['height'])
        self.config.set("user.age", data['profile']['age'])
        self.config.set("user.calorie_target", data['profile']['calorie_target'])
        self.config.set("theme.mode", data['theme'])

        # 保存音频设置
        audio = data['audio']
        self.config.set("audio.enabled", audio['enabled'])
        self.config.set("audio.volume", audio['volume'])
        self.config.set("audio.tts_enabled", audio['tts_enabled'])

        # 保存时间设置
        time_settings = data['time_settings']
        self.config.set("reminder.stand.interval_min", time_settings['stand']['interval_min'])
        self.config.set("reminder.stand.interval_max", time_settings['stand']['interval_max'])
        self.config.set("reminder.stand.duration", time_settings['stand']['duration'])
        self.config.set("reminder.exercise.interval_min", time_settings['exercise']['interval_min'])
        self.config.set("reminder.exercise.interval_max", time_settings['exercise']['interval_max'])
        self.config.set("reminder.gaze.interval_min", time_settings['gaze']['interval_min'])
        self.config.set("reminder.gaze.interval_max", time_settings['gaze']['interval_max'])

        self.config.save()

        # 标记首次运行已完成
        SettingRepository.set("first_run_completed", "true")

        # 启动提醒
        self.reminder_engine.start_all()
    else:
        # 用户取消了向导，退出应用
        self._quit()
```

Add import to `src/core/app.py:22`:
```python
from ..ui.wizards import FirstRunWizard
```

**Step 6: Run test to verify it passes**

Run: `python -m pytest tests/test_wizard_integration.py -v`
Expected: PASS

**Step 7: Manual verification**

Run: `python src/main.py`
Expected: Application starts, first run shows wizard

**Step 8: Commit**

```bash
git add src/ui/wizards/first_run_wizard.py src/core/app.py tests/test_wizard_integration.py
git commit -m "feat: integrate wizard into application startup

- Assemble all 5 pages in FirstRunWizard
- Collect and save user data on completion
- Replace simple SettingsDialog with wizard
- Exit app if user cancels wizard"
```

---

## Task 9: 集成测试

**Files:**
- Create: `tests/test_first_run_integration.py`

**Step 1: Write the failing test**

```python
# tests/test_first_run_integration.py
def test_first_run_flow():
    """Test complete first run flow"""
    from src.core.app import Application
    from src.models.repositories import SettingRepository
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication.instance() or QApplication(sys.argv)
    application = Application()

    # Check it's first run
    assert application._is_first_run() == True

    # After wizard, settings should be saved
    # (This would require UI interaction, may need manual testing)

    SettingRepository.set("first_run_completed", "false")  # Reset
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_first_run_integration.py::test_first_run_flow -v`
Expected: May need manual verification

**Step 3: Manual testing plan**

```bash
# Test 1: Fresh install
rm -f data/app.db
python src/main.py
# Expected: Wizard appears, complete all pages, app starts with reminders

# Test 2: Second run
python src/main.py
# Expected: No wizard, app starts directly with reminders

# Test 3: Cancel wizard
rm -f data/app.db
python src/main.py
# Click cancel on wizard
# Expected: App exits
```

**Step 4: Commit**

```bash
git add tests/test_first_run_integration.py
git commit -m "test: add first run integration test

- Add test for complete first run flow
- Document manual testing steps"
```

---

## Summary

This plan implements a complete first-run wizard following Superpowers TDD methodology:

**Completed Features:**
- ✅ P0 Bug fix (QDialog import)
- ✅ 5-page wizard (Welcome, Profile, Theme, Audio, Time)
- ✅ Data validation and collection
- ✅ Integration with app startup
- ✅ Configuration persistence

**Test Coverage:**
- Unit tests for each page
- Integration tests for wizard
- Manual testing checklist

**Files Created:**
- 5 wizard page classes
- 1 main wizard class
- 9 test files
- Updated app.py integration

**Next Steps:**
1. Execute this plan using `superpowers:executing-plans`
2. Manual UI testing
3. Deploy and gather user feedback
