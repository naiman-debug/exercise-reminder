# v2.0 UI 重构实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 v2.0 版本的 UI 重构，包括新的设计系统、配置结构变更、去掉惩罚机制、所有提醒改为自动倒计时

**Architecture:** 分层架构，TDD 开发，每个功能独立测试，频繁提交

**Tech Stack:** Python 3.10+, PySide6, pytest, loguru

---

## 任务概览

| 任务 | 描述 | 优先级 |
|------|------|--------|
| Task 1 | 完善日志系统 | P0 |
| Task 2 | 新建向导第3页（体验倒计时页） | P0 |
| Task 3 | 更新向导流程（去掉主题页） | P0 |
| Task 4 | 主窗口 UI 更新 | P1 |
| Task 5 | 设置对话框 UI 更新 | P1 |
| Task 6 | 去掉惩罚机制逻辑 | P1 |
| Task 7 | 提醒弹窗改为纯倒计时 | P1 |
| Task 8 | 添加提醒冷却机制 | P2 |
| Task 9 | 统计页面更新 | P2 |
| Task 10 | 动作库导入功能 | P2 |

---

## Task 1: 完善日志系统

**目标:** 使用 loguru 建立统一的日志系统，支持文件轮转、不同级别日志、结构化输出

**Files:**
- Create: `src/utils/logger.py`
- Create: `src/utils/__init__.py` (update)
- Test: `tests/test_logger.py`

**Step 1: 添加 loguru 依赖**

**File:** `F:\claude-code\exercise-reminder-v2\requirements.txt`

Add line:
```txt
loguru>=0.7.0
```

**Step 2: 运行安装**

```bash
cd F:/claude-code/exercise-reminder-v2
pip install loguru>=0.7.0
```

Expected: loguru 安装成功

**Step 3: 编写日志系统测试**

**File:** `F:\claude-code\exercise-reminder-v2\tests\test_logger.py`

```python
# -*- coding: utf-8 -*-
"""
日志系统测试
"""
import pytest
from pathlib import Path
from loguru import logger


def test_logger_import():
    """测试日志模块可导入"""
    from src.utils.logger import get_logger, setup_logger
    assert get_logger is not None
    assert setup_logger is not None


def test_setup_logger(tmp_path):
    """测试日志初始化"""
    from src.utils.logger import setup_logger

    log_file = tmp_path / "test.log"
    setup_logger(log_path=str(log_file))

    assert log_file.exists()


def test_get_logger():
    """测试获取 logger 实例"""
    from src.utils.logger import get_logger

    test_logger = get_logger("test")
    assert test_logger is not None
    assert test_logger.name == "test"


def test_logger_levels(tmp_path):
    """测试不同日志级别"""
    from src.utils.logger import setup_logger, get_logger

    log_file = tmp_path / "test_levels.log"
    setup_logger(log_path=str(log_file))
    logger = get_logger("levels_test")

    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")

    log_content = log_file.read_text(encoding='utf-8')
    assert "info message" in log_content
    assert "warning message" in log_content
    assert "error message" in log_content


def test_logger_rotation(tmp_path):
    """测试日志轮转"""
    from src.utils.logger import setup_logger, get_logger

    log_file = tmp_path / "test_rotation.log"
    setup_logger(log_path=str(log_file), rotation="1 MB")

    logger = get_logger("rotation_test")
    # 写入大量日志
    for i in range(10000):
        logger.info(f"Log message {i}: " + "x" * 100)

    # 检查是否生成了轮转文件
    log_dir = tmp_path
    log_files = list(log_dir.glob("test_rotation*.log"))
    assert len(log_files) >= 1
```

**Step 4: 运行测试验证失败**

```bash
cd F:/claude-code/exercise-reminder-v2
pytest tests/test_logger.py -v
```

Expected: FAIL - ModuleNotFoundError: No module named 'src.utils.logger'

**Step 5: 实现日志系统**

**File:** `F:\claude-code\exercise-reminder-v2\src\utils\logger.py`

```python
# -*- coding: utf-8 -*-
"""
日志系统模块

使用 loguru 提供统一的日志功能
"""
import sys
from pathlib import Path
from loguru import logger
from typing import Optional


# 日志文件路径
LOG_DIR = Path("data/logs")
LOG_FILE = LOG_DIR / "app.log"


def setup_logger(
    log_path: Optional[str] = None,
    level: str = "INFO",
    rotation: str = "10 MB",
    retention: str = "30 days",
    compression: str = "zip"
) -> None:
    """
    配置日志系统

    Args:
        log_path: 日志文件路径（默认为 data/logs/app.log）
        level: 日志级别（DEBUG, INFO, WARNING, ERROR）
        rotation: 日志轮转大小
        retention: 日志保留时间
        compression: 压缩格式
    """
    # 移除默认处理器
    logger.remove()

    # 确保日志目录存在
    if log_path:
        log_file = Path(log_path)
    else:
        log_file = LOG_FILE

    log_file.parent.mkdir(parents=True, exist_ok=True)

    # 控制台输出（带颜色）
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True
    )

    # 文件输出（结构化）
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        rotation=rotation,
        retention=retention,
        compression=compression,
        encoding="utf-8"
    )

    logger.info(f"日志系统初始化完成，日志文件: {log_file}")


def get_logger(name: str):
    """
    获取指定名称的 logger

    Args:
        name: logger 名称

    Returns:
        logger 实例

    示例：
        >>> logger = get_logger("my_module")
        >>> logger.info("Hello")
    """
    return logger.bind(name=name)


# 初始化日志系统（在模块导入时自动调用）
setup_logger()
```

**Step 6: 更新 __init__.py 导出**

**File:** `F:\claude-code\exercise-reminder-v2\src\utils\__init__.py`

```python
# -*- coding: utf-8 -*-
"""
工具模块

提供配置、音频、主题、日志等工具函数
"""
from .logger import setup_logger, get_logger
from .config import ConfigManager
from .audio_player import AudioPlayer
from .theme_manager import ThemeManager

__all__ = [
    "setup_logger",
    "get_logger",
    "ConfigManager",
    "AudioPlayer",
    "ThemeManager"
]
```

**Step 7: 运行测试验证通过**

```bash
cd F:/claude-code/exercise-reminder-v2
pytest tests/test_logger.py -v
```

Expected: PASS (所有测试通过)

**Step 8: 在主应用中集成日志**

**File:** `F:\claude-code\exercise-reminder-v2\src\main.py`

在文件开头添加：
```python
from utils.logger import get_logger

logger = get_logger("main")

# 替换 print 语句为 logger
logger.info("应用启动中...")
```

**Step 9: Commit**

```bash
cd F:/claude-code/exercise-reminder-v2
git add requirements.txt src/utils/logger.py src/utils/__init__.py tests/test_logger.py
git commit -m "feat: 添加基于 loguru 的日志系统

- 支持控制台彩色输出
- 支持文件日志轮转
- 支持结构化日志格式
- 添加完整的单元测试"
```

---

## Task 2: 新建向导第3页（体验倒计时页）

**目标:** 创建新的向导页面，包含 10 秒倒计时功能

**Files:**
- Create: `src/ui/wizards/experience_page.py`
- Modify: `src/ui/wizards/first_run_wizard.py`
- Test: `tests/test_experience_page.py`

**Step 1: 编写测试**

**File:** `F:\claude-code\exercise-reminder-v2\tests\test_experience_page.py`

```python
# -*- coding: utf-8 -*-
"""
体验倒计时页测试
"""
import pytest
from PySide6.QtWidgets import QWizard
from PySide6.QtCore import Qt
from src.ui.wizards.experience_page import ExperiencePage


@pytest.fixture
def experience_page(qtbot):
    """创建体验页面"""
    wizard = QWizard()
    page = ExperiencePage()
    wizard.addPage(page)
    qtbot.addWidget(wizard)
    return page, wizard


def test_experience_page_creation(experience_page):
    """测试页面创建"""
    page, wizard = experience_page
    assert page is not None
    assert page.title() == "准备就绪"


def test_countdown_starts_at_10(experience_page):
    """测试倒计时从 10 开始"""
    page, wizard = experience_page
    assert page.get_countdown() == 10


def test_countdown_decreases(experience_page, qtbot):
    """测试倒计时递减"""
    page, wizard = experience_page

    # 等待 1 秒
    qtbot.wait(1000)

    assert page.get_countdown() < 10


def test_skip_button_stops_countdown(experience_page, qtbot):
    """测试跳过按钮停止倒计时"""
    page, wizard = experience_page

    initial_count = page.get_countdown()
    qtbot.mouseClick(page.skip_button, Qt.LeftButton)
    qtbot.wait(100)

    # 倒计时应该停止
    after_count = page.get_countdown()
    assert after_count == initial_count or after_count == 0


def test_start_now_button_triggers_reminder(experience_page, qtbot):
    """测试立即体验按钮触发提醒信号"""
    page, wizard = experience_page

    with qtbot.waitSignal(page.startNowRequested, timeout=1000):
        qtbot.mouseClick(page.start_now_button, Qt.LeftButton)
```

**Step 2: 运行测试验证失败**

```bash
cd F:/claude-code/exercise-reminder-v2
pytest tests/test_experience_page.py -v
```

Expected: FAIL - ModuleNotFoundError

**Step 3: 实现体验倒计时页**

**File:** `F:\claude-code\exercise-reminder-v2\src\ui\wizards\experience_page.py`

```python
# -*- coding: utf-8 -*-
"""
体验提示页 - 首次启动向导第3页

呼吸感设计 - 柔和有机主义风格
"""
from PySide6.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QGridLayout
)
from PySide6.QtCore import Qt, QTimer, Signal
from ..design.tokens import DesignTokens


class ExperiencePage(QWizardPage):
    """体验提示页 - 10秒倒计时"""

    # 信号：用户点击立即体验
    startNowRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("准备就绪")
        self.setSubTitle("开始您的健康之旅")

        # 倒计时相关
        self._countdown = 10
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_timer_tick)

        # 应用设计系统样式
        DesignTokens.apply_stylesheet(self, "all")

        self.setup_ui()
        self.start_countdown()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 主内容卡片
        content_card = self._create_content_card()
        layout.addWidget(content_card)
        layout.addStretch()

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.skip_button = QPushButton("跳过体验")
        self.skip_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #F5F5F5;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
                border: none;
                border-radius: {DesignTokens.RADIUS.MD}px;
                padding: 12px 30px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            }}
            QPushButton:hover {{
                background-color: #E0E0E0;
            }}
        """)
        self.skip_button.clicked.connect(self._on_skip_clicked)
        button_layout.addWidget(self.skip_button)

        self.start_now_button = QPushButton("立即体验")
        self.start_now_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DesignTokens.COLOR.SUCCESS};
                color: white;
                border: none;
                border-radius: {DesignTokens.RADIUS.MD}px;
                padding: 12px 30px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            }}
            QPushButton:hover {{
                background-color: #43A047;
            }}
        """)
        self.start_now_button.clicked.connect(self._on_start_now_clicked)
        button_layout.addWidget(self.start_now_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _create_content_card(self) -> QFrame:
        """创建主内容卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.XL}px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(
            DesignTokens.SPACING.XL,
            DesignTokens.SPACING.XL,
            DesignTokens.SPACING.XL,
            DesignTokens.SPACING.XL
        )
        card_layout.setSpacing(DesignTokens.SPACING.LG)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 成功图标
        icon_label = QLabel("✅")
        icon_label.setStyleSheet(f"""
            font-size: 64pt;
            background-color: transparent;
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)

        # 主标题
        title = QLabel("设置完成")
        title.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_3XL}pt;
            font-weight: 800;
            color: {DesignTokens.COLOR.SUCCESS};
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(DesignTokens.SPACING.MD)

        # 倒计时文字
        self.countdown_label = QLabel(f"应用将在 {self._countdown} 秒后开始运行")
        self.countdown_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_XL}pt;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.countdown_label)

        # 说明文字
        desc = QLabel("倒计时结束后，将弹出首次站立提醒\n请准备体验一下")
        desc.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            color: {DesignTokens.COLOR.TEXT_SECONDARY};
        """)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(desc)

        card_layout.addSpacing(DesignTokens.SPACING.MD)

        # 提示卡片
        hint_card = self._create_hint_card()
        card_layout.addWidget(hint_card)

        return card

    def _create_hint_card(self) -> QFrame:
        """创建提示卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #E8F5E9;
                border-radius: {DesignTokens.RADIUS.MD}px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD
        )

        hint_title = QLabel("💡 第一次体验提示")
        hint_title.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            font-weight: 600;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        hint_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(hint_title)

        hint_text = QLabel(
            "• 所有提醒都是倒计时自动结束\n"
            "• 站起提醒: 请站立等待倒计时\n"
            "• 微运动: 跟着动作做，等待倒计时\n"
            "• 远眺: 放松眼睛，眺望远方\n"
            "• 应用在系统托盘运行，随时可调整设置"
        )
        hint_text.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_SM}pt;
            color: {DesignTokens.COLOR.TEXT_SECONDARY};
            line-height: 1.6;
        """)
        hint_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(hint_text)

        return card

    def start_countdown(self):
        """开始倒计时"""
        self._countdown = 10
        self._update_countdown_display()
        self._timer.start(1000)  # 每秒触发一次

    def _on_timer_tick(self):
        """定时器触发"""
        self._countdown -= 1
        self._update_countdown_display()

        if self._countdown <= 0:
            self._timer.stop()
            # 倒计时结束，触发向导完成
            self.wizard().next()

    def _update_countdown_display(self):
        """更新倒计时显示"""
        self.countdown_label.setText(f"应用将在 {self._countdown} 秒后开始运行")

    def get_countdown(self) -> int:
        """获取当前倒计时值"""
        return self._countdown

    def _on_skip_clicked(self):
        """跳过按钮点击"""
        self._timer.stop()
        self.wizard().next()

    def _on_start_now_clicked(self):
        """立即体验按钮点击"""
        self._timer.stop()
        self.startNowRequested.emit()
        self.wizard().next()

    def cleanupPage(self):
        """页面清理"""
        if self._timer.isActive():
            self._timer.stop()
```

**Step 4: 运行测试验证通过**

```bash
cd F:/claude-code/exercise-reminder-v2
pytest tests/test_experience_page.py -v
```

Expected: PASS

**Step 5: 更新向导流程**

**File:** `F:\claude-code\exercise-reminder-v2\src\ui\wizards\first_run_wizard.py`

修改向导页面顺序，去掉 theme_page：

```python
# 在文件开头更新导入
from .welcome_page import WelcomePage
from .profile_page import ProfilePage
from .reminder_settings_page import ReminderSettingsPage
from .experience_page import ExperiencePage  # 新增

class FirstRunWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ... 现有代码 ...

        # 添加页面（新顺序）
        self.addPage(WelcomePage(self))
        self.addPage(ProfilePage(self))
        self.addPage(ReminderSettingsPage(self))
        self.addPage(ExperiencePage(self))  # 新增：体验倒计时页
```

**Step 6: Commit**

```bash
cd F:/claude-code/exercise-reminder-v2
git add src/ui/wizards/experience_page.py src/ui/wizards/first_run_wizard.py tests/test_experience_page.py
git commit -m "feat: 添加体验倒计时页

- 新增 ExperiencePage，10秒倒计时功能
- 更新向导流程，去掉主题页
- 支持跳过/立即体验按钮
- 添加完整单元测试"
```

---

## Task 3: 主窗口 UI 更新

**目标:** 根据新设计文档更新主窗口，包含 3 个模块：目标进度、活动详情、快速操作

**Files:**
- Modify: `src/ui/main_window.py` (需要创建)
- Test: `tests/test_main_window.py`

**Step 1: 编写主窗口测试**

**File:** `F:\claude-code\exercise-reminder-v2\tests\test_main_window.py`

```python
# -*- coding: utf-8 -*-
"""
主窗口测试
"""
import pytest
from PySide6.QtCore import Qt
from src.ui.main_window import MainWindow


@pytest.fixture
def main_window(qtbot):
    """创建主窗口"""
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_main_window_creation(main_window):
    """测试主窗口创建"""
    assert main_window is not None
    assert "灵动休息" in main_window.windowTitle()


def test_window_size(main_window):
    """测试窗口尺寸"""
    assert main_window.width() == 900
    assert main_window.minimumHeight() == 550


def test_has_goal_progress_module(main_window):
    """测试有目标进度模块"""
    assert main_window.goal_progress_widget is not None


def test_has_activity_list_module(main_window):
    """测试有活动列表模块"""
    assert main_window.activity_list_widget is not None


def test_has_quick_actions_module(main_window):
    """测试有快速操作模块"""
    assert main_window.quick_actions_widget is not None


def test_quick_actions_buttons(main_window):
    """测试快速操作按钮"""
    assert main_window.action_library_button is not None
    assert main_window.settings_button is not None
    assert main_window.user_info_button is not None
    assert main_window.basic_settings_button is not None


def test_refresh_interval(main_window):
    """测试自动刷新间隔"""
    assert main_window.refresh_interval == 30000  # 30秒
```

**Step 2: 运行测试验证失败**

```bash
cd F:/claude-code/exercise-reminder-v2
pytest tests/test_main_window.py -v
```

Expected: FAIL

**Step 3: 实现主窗口**

**File:** `F:\claude-code\exercise-reminder-v2\src\ui\main_window.py`

```python
# -*- coding: utf-8 -*-
"""
主窗口 - 灵动休息健康助手

呼吸感设计 - 柔和有机主义风格
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QScrollArea, QGridLayout
)
from PySide6.QtCore import Qt, QTimer
from ..design.tokens import DesignTokens
from utils.logger import get_logger

logger = get_logger("main_window")


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("初始化主窗口")

        # 窗口设置
        self.setWindowTitle("🏠 灵动休息健康助手")
        self.resize(900, 550)
        self.setMinimumSize(900, 550)

        # 刷新定时器（30秒）
        self.refresh_interval = 30000
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_data)

        # 应用设计系统样式
        DesignTokens.apply_stylesheet(self, "all")

        # UI 组件引用
        self.goal_progress_widget = None
        self.activity_list_widget = None
        self.quick_actions_widget = None
        self.action_library_button = None
        self.settings_button = None
        self.user_info_button = None
        self.basic_settings_button = None

        self.setup_ui()
        self.refresh_data()  # 初始加载数据
        self.refresh_timer.start(self.refresh_interval)

    def setup_ui(self):
        """设置 UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(
            DesignTokens.SPACING.LG,
            DesignTokens.SPACING.LG,
            DesignTokens.SPACING.LG,
            DesignTokens.SPACING.LG
        )
        main_layout.setSpacing(DesignTokens.SPACING.LG)

        # 目标进度模块
        self.goal_progress_widget = self._create_goal_progress_module()
        main_layout.addWidget(self.goal_progress_widget)

        # 活动详情模块
        self.activity_list_widget = self._create_activity_list_module()
        main_layout.addWidget(self.activity_list_widget)

        # 快速操作模块
        self.quick_actions_widget = self._create_quick_actions_module()
        main_layout.addWidget(self.quick_actions_widget)

        # 自动刷新提示
        refresh_label = QLabel("自动刷新: 每 30 秒")
        refresh_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_XS}pt;
            color: {DesignTokens.COLOR.TEXT_TERTIARY};
        """)
        refresh_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(refresh_label)

    def _create_goal_progress_module(self) -> QFrame:
        """创建目标进度模块"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.LG}px;
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD
        )

        # 标题
        title = QLabel("🎯 今日目标进度")
        title.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_LG}pt;
            font-weight: 600;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        layout.addWidget(title)

        # 进度条（简化实现）
        progress_label = QLabel("运动热量目标：0/300 千卡 (0%)")
        progress_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        layout.addWidget(progress_label)

        progress_bar = QFrame()
        progress_bar.setFixedHeight(8)
        progress_bar.setStyleSheet(f"""
            QFrame {{
                background-color: #E0E0E0;
                border-radius: 4px;
            }}
        """)
        layout.addWidget(progress_bar)

        # 打卡天数
        streak_label = QLabel("🔥 连续打卡：0 天")
        streak_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            color: {DesignTokens.COLOR.SUCCESS};
        """)
        layout.addWidget(streak_label)

        return frame

    def _create_activity_list_module(self) -> QFrame:
        """创建活动列表模块"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.LG}px;
            }}
        """)
        frame.setMinimumHeight(200)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD
        )

        # 标题
        title = QLabel("📋 今日活动详情")
        title.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_LG}pt;
            font-weight: 600;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        layout.addWidget(title)

        # 活动列表（滚动区域）
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)

        # 占位内容
        empty_label = QLabel("今天还没有活动记录")
        empty_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_SM}pt;
            color: {DesignTokens.COLOR.TEXT_TERTIARY};
        """)
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        list_layout.addWidget(empty_label)
        list_layout.addStretch()

        scroll.setWidget(list_widget)
        layout.addWidget(scroll)

        return frame

    def _create_quick_actions_module(self) -> QFrame:
        """创建快速操作模块"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.LG}px;
            }}
        """)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD
        )

        # 四个快速操作按钮
        self.action_library_button = self._create_action_button("🏋️ 动作库")
        self.settings_button = self._create_action_button("⚙️ 参数设置")
        self.user_info_button = self._create_action_button("👤 用户信息")
        self.basic_settings_button = self._create_action_button("🔧 基础设置")

        layout.addWidget(self.action_library_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.user_info_button)
        layout.addWidget(self.basic_settings_button)

        return frame

    def _create_action_button(self, text: str) -> QPushButton:
        """创建操作按钮"""
        button = QPushButton(text)
        button.setFixedSize(160, 50)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: #F5F5F5;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
                border: none;
                border-radius: {DesignTokens.RADIUS.SM}px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            }}
            QPushButton:hover {{
                background-color: {DesignTokens.COLOR.PRIMARY_LIGHT};
            }}
        """)
        return button

    def refresh_data(self):
        """刷新数据"""
        logger.debug("刷新主窗口数据")
        # TODO: 从数据库加载真实数据
        pass

    def closeEvent(self, event):
        """窗口关闭事件"""
        logger.info("主窗口关闭")
        self.refresh_timer.stop()
        event.accept()
```

**Step 4: 运行测试验证通过**

```bash
cd F:/claude-code/exercise-reminder-v2
pytest tests/test_main_window.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
cd F:/claude-code/exercise-reminder-v2
git add src/ui/main_window.py tests/test_main_window.py
git commit -m "feat: 实现新的主窗口设计

- 3个模块：目标进度、活动详情、快速操作
- 30秒自动刷新
- 呼吸感设计风格
- 添加完整单元测试"
```

---

## Task 4: 设置对话框 UI 更新

**目标:** 更新设置对话框为 5 个标签页，新布局

**Files:**
- Modify: `src/ui/settings/settings_dialog.py`
- Test: `tests/test_settings_dialog.py`

**Step 1: 编写测试**

**File:** `F:\claude-code\exercise-reminder-v2\tests\test_settings_dialog.py`

```python
# -*- coding: utf-8 -*-
"""
设置对话框测试
"""
import pytest
from PySide6.QtWidgets import QTabWidget
from src.ui.settings.settings_dialog import SettingsDialog


@pytest.fixture
def settings_dialog(qtbot):
    """创建设置对话框"""
    dialog = SettingsDialog()
    qtbot.addWidget(dialog)
    return dialog


def test_settings_dialog_creation(settings_dialog):
    """测试对话框创建"""
    assert settings_dialog is not None
    assert settings_dialog.windowTitle() == "设置"


def test_has_five_tabs(settings_dialog):
    """测试有 5 个标签页"""
    tab_widget = settings_dialog.findChild(QTabWidget)
    assert tab_widget is not None
    assert tab_widget.count() == 5


def test_tab_names(settings_dialog):
    """测试标签页名称"""
    tab_widget = settings_dialog.findChild(QTabWidget)
    tab_names = [tab_widget.tabText(i) for i in range(tab_widget.count())]

    assert "提醒设置" in tab_names
    assert "用户信息" in tab_names
    assert "动作库" in tab_names
    assert "统计" in tab_names
    assert "基础设置" in tab_names
```

**Step 2-5: 实现设置对话框（类似流程）**

... （由于篇幅限制，具体实现步骤省略，遵循相同的 TDD 模式）

**Commit:**
```bash
git add src/ui/settings/settings_dialog.py tests/test_settings_dialog.py
git commit -m "feat: 更新设置对话框为5标签页布局"
```

---

## Task 5: 去掉惩罚机制逻辑

**目标:** 删除惩罚机制相关代码

**Files:**
- Delete: `src/core/punishment_logic.py`
- Modify: `src/core/reminder_engine.py`
- Test: 更新相关测试

**Step 1: 删除惩罚逻辑文件**

```bash
cd F:/claude-code/exercise-reminder-v2
rm src/core/punishment_logic.py
```

**Step 2: 更新提醒引擎**

**File:** `src/core/reminder_engine.py`

删除所有惩罚相关引用：
```python
# 删除这些行：
# from .punishment_logic import PunishmentLogic
# self.punishment_logic = PunishmentLogic()
```

**Step 3: 更新测试**

删除 `tests/test_punishment.py`（如果存在）

**Step 4: Commit**

```bash
git add -A
git commit -m "refactor: 移除惩罚机制

- 删除 punishment_logic.py
- 从提醒引擎中移除惩罚相关代码
- 更新测试文件"
```

---

## Task 6: 提醒弹窗改为纯倒计时

**目标:** 所有提醒弹窗去掉按钮，改为纯倒计时自动结束

**Files:**
- Modify: `src/ui/dialogs/exercise_dialog.py`
- Test: `tests/test_exercise_dialog.py`

**关键变更：**
1. 去掉"完成"、"跳过"按钮
2. 倒计时归零时自动关闭
3. 显示热量消耗反馈（1秒）

**实现示例（exercise_dialog.py）：**

```python
def _on_countdown_finished(self):
    """倒计时结束"""
    # 显示完成反馈（1秒）
    self.feedback_label.setText("✅ 完成！消耗: 12.5 千卡")
    self.feedback_label.show()

    # 1秒后自动关闭
    QTimer.singleShot(1000, self.accept)
```

**Commit:**
```bash
git add src/ui/dialogs/exercise_dialog.py tests/test_exercise_dialog.py
git commit -m "feat: 微运动弹窗改为纯倒计时

- 移除完成/跳过按钮
- 倒计时结束显示热量反馈
- 1秒后自动关闭"
```

---

## Task 7: 添加提醒冷却机制

**目标:** 提醒结束后进入 2 分钟冷却期

**Files:**
- Modify: `src/core/reminder_engine.py`
- Test: `tests/test_cooldown.py`

**实现：**

```python
class ReminderEngine:
    def __init__(self):
        self.cooldown_until = None
        self.cooldown_duration = 120  # 2分钟

    def is_in_cooldown(self) -> bool:
        """检查是否在冷却期"""
        if self.cooldown_until is None:
            return False
        return datetime.now() < self.cooldown_until

    def start_cooldown(self):
        """开始冷却期"""
        self.cooldown_until = datetime.now() + timedelta(seconds=self.cooldown_duration)
```

**Commit:**
```bash
git add src/core/reminder_engine.py tests/test_cooldown.py
git commit -m "feat: 添加提醒冷却机制

- 提醒结束后进入2分钟冷却期
- 冷却期间暂停其他定时器
- 冷却结束后恢复定时器"
```

---

## Task 8-10: 其他任务

（继续按照相同的 TDD 模式实现剩余任务）

---

## 总结

### 实现原则
1. **TDD**: 先写测试，再写实现
2. **小步提交**: 每个 task 完成后立即 commit
3. **日志完善**: 使用 loguru 记录关键操作
4. **设计系统**: 遵循 DesignTokens 统一规范

### 执行顺序建议
1. Task 1（日志系统）- 最高优先级
2. Task 2（体验倒计时页）- 核心功能
3. Task 3（主窗口）- 核心界面
4. Task 5（去掉惩罚）- 简化逻辑
5. Task 6（纯倒计时）- 核心交互
6. Task 7（冷却机制）- 新功能
7. 其他任务

### 验证清单
- [ ] 所有测试通过: `pytest tests/ -v`
- [ ] 代码覆盖率: `pytest --cov=src tests/`
- [ ] UI 手动测试: 运行应用验证所有页面
- [ ] 日志检查: 查看 `data/logs/app.log`
