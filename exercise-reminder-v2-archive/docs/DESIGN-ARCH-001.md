# DESIGN-ARCH-001 技术架构设计文档

**项目**："灵动休息"健康助手
**版本**：v1.0
**日期**：2026-01-26
**设计者**：Claude Code

---

## 一、 架构概览

### 1.1 架构风格

采用 **分层架构** + **事件驱动** 的混合模式：

```
┌─────────────────────────────────────────────────────────┐
│                    UI Layer (PySide6)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Dialogs  │  │ Settings │  │ Statistics│             │
│  └──────────┘  └──────────┘  └──────────┘             │
├─────────────────────────────────────────────────────────┤
│                  Business Logic Layer                  │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │Timer Manager │  │Reminder Engine│  │Punishment   │ │
│  │              │  │              │  │Logic        │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────┤
│                     Data Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │  Database    │  │ Repositories │  │   Models    │ │
│  │  (SQLite)    │  │              │  │             │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────┤
│                    Utils Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Config  │  │  Audio   │  │   MET    │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

### 1.2 核心原则

- **单一职责**：每个模块只负责一个功能
- **依赖倒置**：高层模块不依赖低层模块
- **开闭原则**：对扩展开放，对修改关闭
- **接口隔离**：使用抽象接口解耦

---

## 二、 技术栈

### 2.1 核心技术

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **GUI 框架** | PySide6 | 6.6+ | Qt 桌面应用 |
| **数据库** | SQLite | 3.x | 本地数据存储 |
| **ORM** | Peewee | 3.17+ | 轻量级 ORM |
| **图表** | matplotlib | 3.8+ | 统计图表 |
| **构建工具** | PyInstaller | 6.0+ | Windows 打包 |
| **测试** | pytest + pytest-qt | 7.0+ | 单元测试 |

### 2.2 依赖清单

```txt
# requirements.txt
PySide6>=6.6.0
peewee>=3.17.0
matplotlib>=3.8.0
pytest>=7.0.0
pytest-qt>=4.2.0
pyinstaller>=6.0.0
```

---

## 三、 模块设计

### 3.1 模块划分

```
src/
├── main.py                    # 应用入口
├── core/                      # 核心业务逻辑
│   ├── __init__.py
│   ├── app.py                 # 应用主类
│   ├── timer_manager.py       # 定时器管理器
│   ├── reminder_engine.py     # 提醒引擎
│   └── punishment_logic.py    # 惩罚机制逻辑
├── models/                    # 数据模型
│   ├── __init__.py
│   ├── database.py            # 数据库管理
│   ├── models.py              # 数据模型定义
│   └── repositories.py        # 数据仓储层
├── ui/                        # UI 组件
│   ├── __init__.py
│   ├── main_window.py         # 主窗口
│   ├── dialogs/               # 弹窗组件
│   │   ├── __init__.py
│   │   ├── base_dialog.py     # 弹窗基类
│   │   ├── stand_dialog.py    # 强制站立弹窗
│   │   ├── exercise_dialog.py # 微运动弹窗
│   │   └── gaze_dialog.py     # 强制远眺弹窗
│   ├── settings/              # 设置界面
│   │   ├── __init__.py
│   │   ├── settings_dialog.py    # 设置主对话框
│   │   ├── exercise_library.py   # 动作库管理
│   │   └── audio_config.py       # 音频配置
│   └── statistics/            # 统计界面
│       ├── __init__.py
│       ├── stats_view.py      # 统计视图
│       └── charts.py          # 图表组件
├── utils/                     # 工具函数
│   ├── __init__.py
│   ├── config.py              # 配置管理
│   ├── audio_player.py        # 音频播放
│   └── met_calculator.py      # MET 热量计算
└── resources/                 # 资源文件
    ├── sounds/                # 音效文件
    ├── icons/                 # 图标文件
    └── styles/                # 样式表
```

### 3.2 模块职责

#### 3.2.1 core/app.py

**职责**：应用程序主类，协调各模块

```python
class Application(QApplication):
    """应用主类"""

    def __init__(self):
        # 初始化数据库
        # 初始化配置
        # 创建系统托盘
        # 启动提醒引擎

    def start(self):
        """启动应用"""

    def stop(self):
        """停止应用"""
```

#### 3.2.2 core/timer_manager.py

**职责**：管理所有定时器

```python
class TimerManager(QObject):
    """定时器管理器"""

    # 信号
    reminder_triggered = Signal(str)  # 提醒触发

    def __init__(self):
        self.timers = {}  # 提醒类型 -> QTimer

    def start_timer(self, reminder_type: str, interval_ms: int):
        """启动定时器"""

    def stop_timer(self, reminder_type: str):
        """停止定时器"""

    def stop_all(self):
        """停止所有定时器"""
```

#### 3.2.3 core/reminder_engine.py

**职责**：提醒调度引擎

```python
class ReminderEngine(QObject):
    """提醒引擎"""

    # 信号
    show_stand_dialog = Signal(int)      # 显示站立弹窗（秒数）
    show_exercise_dialog = Signal(list)   # 显示运动弹窗（动作列表）
    show_gaze_dialog = Signal()           # 显示远眺弹窗

    def __init__(self, timer_manager, config):
        self.timer_manager = timer_manager
        self.config = config

    def calculate_interval(self, min_min: int, max_min: int) -> int:
        """计算随机间隔"""

    def trigger_stand_reminder(self):
        """触发站立提醒"""

    def trigger_exercise_reminder(self):
        """触发运动提醒"""

    def trigger_gaze_reminder(self):
        """触发远眺提醒"""
```

#### 3.2.4 core/punishment_logic.py

**职责**：惩罚机制逻辑

```python
class PunishmentLogic:
    """惩罚机制逻辑"""

    def __init__(self, config, database):
        self.skip_count = 0
        self.punishment_active = False

    def record_skip(self):
        """记录跳过"""

    def record_complete(self):
        """记录完成"""

    def should_trigger_punishment(self) -> bool:
        """是否应该触发惩罚"""

    def get_window_config(self) -> dict:
        """获取窗口配置（惩罚模式）"""
```

---

## 四、 数据库设计

### 4.1 表结构

#### settings 表
```sql
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### exercises 表
```sql
CREATE TABLE exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    met_value REAL NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### exercise_plans 表
```sql
CREATE TABLE exercise_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### plan_exercises 表
```sql
CREATE TABLE plan_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    order_index INTEGER NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES exercise_plans(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);
```

#### activity_logs 表
```sql
CREATE TABLE activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_type TEXT NOT NULL,  -- 'stand', 'exercise', 'gaze'
    duration_seconds INTEGER NOT NULL,
    calories_burned REAL DEFAULT 0,
    completed BOOLEAN DEFAULT 1,
    skipped BOOLEAN DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### user_profile 表
```sql
CREATE TABLE user_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weight_kg REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4.2 数据模型（Peewee）

```python
from peewee import *
from datetime import datetime

db = SqliteDatabase('data/app.db')

class BaseModel(Model):
    class Meta:
        database = db

class Setting(BaseModel):
    key = CharField(unique=True)
    value = TextField()
    updated_at = DateTimeField(default=datetime.now)

class Exercise(BaseModel):
    name = CharField()
    duration_seconds = IntegerField()
    met_value = FloatField()
    category = CharField()
    created_at = DateTimeField(default=datetime.now)

class ExercisePlan(BaseModel):
    name = CharField()
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)

class PlanExercise(BaseModel):
    plan = ForeignKeyField(ExercisePlan, backref='exercises')
    exercise = ForeignKeyField(Exercise, backref='plans')
    order_index = IntegerField()

class ActivityLog(BaseModel):
    activity_type = CharField()  # 'stand', 'exercise', 'gaze'
    duration_seconds = IntegerField()
    calories_burned = FloatField(default=0)
    completed = BooleanField(default=True)
    skipped = BooleanField(default=False)
    timestamp = DateTimeField(default=datetime.now)

class UserProfile(BaseModel):
    weight_kg = FloatField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
```

---

## 五、 UI 组件设计

### 5.1 弹窗基类

```python
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, Signal

class BaseReminderDialog(QDialog):
    """提醒弹窗基类"""

    # 信号
    completed = Signal()
    skipped = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # 窗口设置
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        # 倒计时
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

        self.setup_ui()

    def setup_ui(self):
        """设置UI（子类实现）"""
        raise NotImplementedError

    def start_countdown(self, seconds: int):
        """开始倒计时"""
        self.remaining_seconds = seconds
        self.countdown_timer.start(1000)

    def update_countdown(self):
        """更新倒计时"""
        self.remaining_seconds -= 1

        if self.remaining_seconds <= 0:
            self.countdown_timer.stop()
            self.on_countdown_complete()

        self.update_countdown_display()

    def update_countdown_display(self):
        """更新倒计时显示（子类实现）"""
        raise NotImplementedError

    def on_countdown_complete(self):
        """倒计时完成"""
        self.completed.emit()
        self.close()
```

### 5.2 强制站立弹窗

```python
class StandReminderDialog(BaseReminderDialog):
    """强制站立提醒弹窗"""

    def __init__(self, seconds: int, parent=None):
        self.seconds = seconds
        super().__init__(parent)

    def setup_ui(self):
        layout = QVBoxLayout()

        # 标题
        title = QLabel("⏰ 请站立休息 ⏰")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 48pt; font-weight: bold;")

        # 倒计时
        self.countdown_label = QLabel()
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 120pt; font-family: Consolas;")

        # 提示
        hint = QLabel("（请保持站立，等待倒计时结束）")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("font-size: 18pt; color: #757575;")

        layout.addWidget(title)
        layout.addWidget(self.countdown_label)
        layout.addWidget(hint)

        self.setLayout(layout)

    def update_countdown_display(self):
        mins, secs = divmod(self.remaining_seconds, 60)
        self.countdown_label.setText(f"{mins:02d}:{secs:02d}")
```

### 5.3 微运动弹窗

```python
class ExerciseReminderDialog(BaseReminderDialog):
    """微运动提醒弹窗"""

    def __init__(self, exercises: list, parent=None):
        self.exercises = exercises
        self.current_index = 0
        super().__init__(parent)

    def setup_ui(self):
        layout = QVBoxLayout()

        # 标题
        title = QLabel("🏃 微运动时间 🏃")
        title.setStyleSheet("font-size: 24pt; font-weight: bold;")

        # 动作信息
        self.exercise_label = QLabel()
        self.exercise_label.setStyleSheet("font-size: 36pt; font-weight: bold;")

        self.met_label = QLabel()
        self.met_label.setStyleSheet("font-size: 18pt;")

        # 倒计时
        self.countdown_label = QLabel()
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 96pt; font-family: Consolas;")

        # 热量
        self.calories_label = QLabel()
        self.calories_label.setStyleSheet("font-size: 18pt;")

        # 按钮
        btn_layout = QHBoxLayout()
        self.complete_btn = QPushButton("✓ 完成")
        self.skip_btn = QPushButton("✗ 跳过")
        self.next_btn = QPushButton("↻ 换一个")

        self.complete_btn.clicked.connect(self.on_complete)
        self.skip_btn.clicked.connect(self.on_skip)
        self.next_btn.clicked.connect(self.on_next)

        btn_layout.addWidget(self.complete_btn)
        btn_layout.addWidget(self.skip_btn)
        btn_layout.addWidget(self.next_btn)

        layout.addWidget(title)
        layout.addWidget(self.exercise_label)
        layout.addWidget(self.met_label)
        layout.addWidget(self.countdown_label)
        layout.addWidget(self.calories_label)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # 显示第一个动作
        self.show_exercise(0)

    def show_exercise(self, index: int):
        """显示动作"""
        exercise = self.exercises[index]
        self.exercise_label.setText(f"动作: {exercise['name']}")
        self.met_label.setText(f"MET: {exercise['met']}")

        # 计算热量
        calories = calculate_calories(
            exercise['met'],
            exercise['duration']
        )
        self.calories_label.setText(f"预计消耗: {calories} 千卡")

    def on_complete(self):
        """完成"""
        self.completed.emit()
        self.close()

    def on_skip(self):
        """跳过"""
        self.skipped.emit()
        self.close()

    def on_next(self):
        """下一个动作"""
        self.current_index = (self.current_index + 1) % len(self.exercises)
        self.show_exercise(self.current_index)
```

---

## 六、 定时器设计

### 6.1 定时器管理

```python
from PySide6.QtCore import QObject, QTimer, Signal

class TimerManager(QObject):
    """定时器管理器"""

    # 信号
    timeout = Signal(str)  # timer_name

    def __init__(self):
        super().__init__()
        self.timers = {}

    def create_timer(self, name: str, interval_ms: int, callback=None):
        """创建定时器"""
        if name in self.timers:
            self.stop_timer(name)

        timer = QTimer()
        timer.setSingleShot(True)

        if callback:
            timer.timeout.connect(callback)
        else:
            timer.timeout.connect(lambda: self.timeout.emit(name))

        self.timers[name] = timer
        return timer

    def start_timer(self, name: str, interval_ms: int = None):
        """启动定时器"""
        if name not in self.timers:
            return False

        timer = self.timers[name]
        if interval_ms:
            timer.setInterval(interval_ms)

        timer.start()
        return True

    def stop_timer(self, name: str):
        """停止定时器"""
        if name in self.timers:
            self.timers[name].stop()

    def stop_all(self):
        """停止所有定时器"""
        for timer in self.timers.values():
            timer.stop()
```

### 6.2 提醒调度

```python
class ReminderScheduler(QObject):
    """提醒调度器"""

    # 信号
    stand_reminder = Signal(int)
    exercise_reminder = Signal(list)
    gaze_reminder = Signal()

    def __init__(self, timer_manager, config):
        super().__init__()
        self.timer_manager = timer_manager
        self.config = config

        # 连接信号
        self.timer_manager.timeout.connect(self.on_timer_timeout)

    def schedule_all(self):
        """调度所有提醒"""
        self.schedule_stand_reminder()
        self.schedule_exercise_reminder()
        self.schedule_gaze_reminder()

    def schedule_stand_reminder(self):
        """调度站立提醒"""
        min_min = self.config.get('stand.interval_min', 30)
        max_min = self.config.get('stand.interval_max', 60)
        interval = self.calculate_random_interval(min_min, max_min)
        duration = self.config.get('stand.duration', 90)

        # 启动定时器
        self.timer_manager.create_timer('stand', interval, lambda: self.stand_reminder.emit(duration))
        self.timer_manager.start_timer('stand')

    def schedule_exercise_reminder(self):
        """调度运动提醒"""
        min_min = self.config.get('exercise.interval_min', 45)
        max_min = self.config.get('exercise.interval_max', 75)
        interval = self.calculate_random_interval(min_min, max_min)

        # 获取动作列表
        exercises = self.get_exercise_list()

        # 启动定时器
        self.timer_manager.create_timer('exercise', interval, lambda: self.exercise_reminder.emit(exercises))
        self.timer_manager.start_timer('exercise')

    def schedule_gaze_reminder(self):
        """调度远眺提醒"""
        min_min = self.config.get('gaze.interval_min', 60)
        max_min = self.config.get('gaze.interval_max', 90)
        interval = self.calculate_random_interval(min_min, max_min)

        # 启动定时器
        self.timer_manager.create_timer('gaze', interval, lambda: self.gaze_reminder.emit())
        self.timer_manager.start_timer('gaze')

    @staticmethod
    def calculate_random_interval(min_min: int, max_min: int) -> int:
        """计算随机间隔（毫秒）"""
        import random
        minutes = random.randint(min_min, max_min)
        return minutes * 60 * 1000

    def on_timer_timeout(self, timer_name: str):
        """定时器超时"""
        # 重新调度该提醒
        if timer_name == 'stand':
            self.schedule_stand_reminder()
        elif timer_name == 'exercise':
            self.schedule_exercise_reminder()
        elif timer_name == 'gaze':
            self.schedule_gaze_reminder()
```

---

## 七、 配置管理

### 7.1 配置文件结构

```json
{
  "reminder": {
    "stand": {
      "enabled": true,
      "interval_min": 30,
      "interval_max": 60,
      "duration": 90
    },
    "exercise": {
      "enabled": true,
      "interval_min": 45,
      "interval_max": 75,
      "exercises_per_session": [3, 5]
    },
    "gaze": {
      "enabled": true,
      "interval_min": 60,
      "interval_max": 90,
      "duration": 60
    }
  },
  "punishment": {
    "enabled": true,
    "skip_threshold": 2
  },
  "audio": {
    "enabled": true,
    "volume": 0.7,
    "tts_enabled": false,
    "tts_api": ""
  },
  "user": {
    "weight_kg": 70
  }
}
```

### 7.2 配置管理器

```python
import json
from pathlib import Path

class ConfigManager:
    """配置管理器"""

    DEFAULT_CONFIG = {
        "reminder": {...},
        "punishment": {...},
        "audio": {...},
        "user": {...}
    }

    def __init__(self, config_path: str = "data/config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self) -> dict:
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self.DEFAULT_CONFIG.copy()

    def save_config(self):
        """保存配置"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default=None):
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
```

---

## 八、 音频系统

### 8.1 音频播放器

```python
from PySide6.QtMultimedia import QSoundEffect

class AudioManager:
    """音频管理器"""

    def __init__(self, config):
        self.config = config
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        """加载音效"""
        sound_dir = Path("src/resources/sounds")

        self.sounds = {
            'reminder': QSoundEffect(sound_dir / "reminder.wav"),
            'complete': QSoundEffect(sound_dir / "complete.wav"),
            'skip': QSoundEffect(sound_dir / "skip.wav"),
            'tick': QSoundEffect(sound_dir / "tick.wav")
        }

        # 设置音量
        volume = self.config.get('audio.volume', 0.7)
        for sound in self.sounds.values():
            sound.setVolume(volume)

    def play(self, sound_name: str):
        """播放音效"""
        if self.config.get('audio.enabled', True):
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
```

---

## 九、 打包与分发

### 9.1 PyInstaller 配置

```python
# build.spec
from PySide6.QtWidgets import QApplication

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/resources', 'src/resources'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'peewee',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='灵动休息',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/resources/icons/app.ico'
)
```

### 9.2 安装程序

使用 NSIS 制作 Windows 安装程序：

```nsis
; setup.nsi
!define APP_NAME "灵动休息"
!define APP_VERSION "1.0.0"

OutFile "灵动休息-Setup-${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
RequestExecutionLevel admin

Section "Main"
    SetOutPath $INSTDIR
    File /r "dist\*"

    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\灵动休息.exe"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\卸载.lnk" "$INSTDIR\uninstall.exe"

    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\*"
    RMDir "$INSTDIR"
    Delete "$SMPROGRAMS\${APP_NAME}\*"
    RMDir "$SMPROGRAMS\${APP_NAME}"
SectionEnd
```

---

## 十、 测试策略

### 10.1 单元测试

```python
import pytest
from src.core.timer_manager import TimerManager
from src.core.reminder_engine import ReminderEngine

def test_timer_manager():
    """测试定时器管理器"""
    tm = TimerManager()

    # 创建定时器
    timer = tm.create_timer('test', 1000)
    assert timer is not None
    assert 'test' in tm.timers

    # 启动定时器
    tm.start_timer('test')

    # 停止定时器
    tm.stop_timer('test')

def test_reminder_engine():
    """测试提醒引擎"""
    tm = TimerManager()
    config = MockConfig()
    engine = ReminderEngine(tm, config)

    # 测试随机间隔计算
    interval = engine.calculate_interval(30, 60)
    assert 30 * 60 * 1000 <= interval <= 60 * 60 * 1000
```

### 10.2 集成测试

```python
def test_stand_reminder_flow(qtbot):
    """测试站立提醒流程"""
    app = Application()
    dialog = StandReminderDialog(90)
    dialog.show()

    # 模拟倒计时
    for _ in range(90):
        dialog.countdown_timer.timeout.emit()

    # 验证弹窗关闭
    assert not dialog.isVisible()
```

---

**文档版本**：v1.0
**最后更新**：2026-01-26
