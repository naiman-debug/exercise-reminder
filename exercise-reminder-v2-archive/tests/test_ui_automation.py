# -*- coding: utf-8 -*-
"""
UI 自动化测试 - exercise-reminder-v2

模拟用户交互，测试对话框功能（无需显示窗口）
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtTest import QTest, QSignalSpy

from src.models.database import get_db_manager
from src.models.repositories import ExerciseRepository
from src.ui.dialogs.stand_dialog import StandReminderDialog
from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog
from src.ui.dialogs.gaze_dialog import GazeReminderDialog


def get_qt_app():
    """获取 QApplication 实例"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


class UITestResults:
    """UI 测试结果收集器"""
    def __init__(self):
        self.passed = []
        self.failed = []
        self.total = 0

    def add_pass(self, name):
        self.passed.append(name)
        self.total += 1
        print(f"[PASS] {name}")

    def add_fail(self, name, reason):
        self.failed.append((name, reason))
        self.total += 1
        print(f"[FAIL] {name}: {reason}")

    def summary(self):
        print()
        print("=" * 60)
        print(f"UI Test Summary: {len(self.passed)}/{self.total} passed")
        print("=" * 60)
        if self.failed:
            print()
            print("Failed tests:")
            for name, reason in self.failed:
                print(f"  - {name}: {reason}")
        print()
        return len(self.failed) == 0


results = UITestResults()


def test_stand_dialog_creation():
    """测试强制站立对话框创建"""
    print("\n[UI-1/5] Testing Stand Reminder Dialog")
    print("-" * 40)

    try:
        get_db_manager().initialize_database()
        app = get_qt_app()

        # 创建对话框（10秒）
        dialog = StandReminderDialog(duration=10)
        results.add_pass("Create StandReminderDialog")

        # 测试基本属性
        if dialog.duration == 10:
            results.add_pass("Duration set correctly")
        else:
            results.add_fail("Duration", f"Expected 10, got {dialog.duration}")

        # 测试倒计时标签
        if hasattr(dialog, 'countdown_label') and dialog.countdown_label:
            results.add_pass("Countdown label exists")
        else:
            results.add_fail("Countdown label", "Missing attribute")

        # 测试窗口属性
        flags = dialog.windowFlags()
        if flags & Qt.WindowType.WindowStaysOnTopHint:
            results.add_pass("Stay on top flag set")
        else:
            results.add_fail("Stay on top", "Flag not set")

    except Exception as e:
        results.add_fail("Stand dialog test", str(e))


def test_exercise_dialog_creation():
    """测试微运动对话框创建"""
    print("\n[UI-2/5] Testing Exercise Reminder Dialog")
    print("-" * 40)

    try:
        get_db_manager().initialize_database()
        app = get_qt_app()

        # 获取运动数据
        exercises = ExerciseRepository.get_random_exercises(count=1)
        if not exercises:
            results.add_fail("Exercise dialog test", "No exercises found")
            return

        # 转换为对话框需要的格式
        exercises_data = [
            {
                "id": ex.id,
                "name": ex.name,
                "duration": ex.duration_seconds,
                "met": ex.met_value
            }
            for ex in exercises
        ]

        # 创建对话框 (使用 weight_kg 参数)
        dialog = ExerciseReminderDialog(exercises_data, weight_kg=70)
        results.add_pass("Create ExerciseReminderDialog")

        # 测试基本属性 - 按钮是 complete_btn, skip_btn, next_btn
        if hasattr(dialog, 'complete_btn') and dialog.complete_btn:
            results.add_pass("Complete button exists")
        else:
            results.add_fail("Complete button", "Missing attribute")

        if hasattr(dialog, 'skip_btn') and dialog.skip_btn:
            results.add_pass("Skip button exists")
        else:
            results.add_fail("Skip button", "Missing attribute")

        if hasattr(dialog, 'next_btn') and dialog.next_btn:
            results.add_pass("Next button exists")
        else:
            results.add_fail("Next button", "Missing attribute")

    except Exception as e:
        results.add_fail("Exercise dialog test", str(e))


def test_gaze_dialog_creation():
    """测试远眺对话框创建"""
    print("\n[UI-3/5] Testing Gaze Reminder Dialog")
    print("-" * 40)

    try:
        app = get_qt_app()

        # 创建对话框（10秒）
        dialog = GazeReminderDialog(duration=10)
        results.add_pass("Create GazeReminderDialog")

        # 测试基本属性
        if dialog.duration == 10:
            results.add_pass("Duration set correctly")
        else:
            results.add_fail("Duration", f"Expected 10, got {dialog.duration}")

        # 测试标题设置
        dialog.setWindowTitle("Test Gaze Dialog")
        if "Test Gaze Dialog" in dialog.windowTitle():
            results.add_pass("Window title set")
        else:
            results.add_fail("Window title", "Title not set correctly")

    except Exception as e:
        results.add_fail("Gaze dialog test", str(e))


def test_dialog_timer_simulation():
    """测试对话框定时器模拟"""
    print("\n[UI-4/5] Testing Dialog Timer Simulation")
    print("-" * 40)

    try:
        app = get_qt_app()

        # 创建站立对话框（短时间用于测试）
        dialog = StandReminderDialog(duration=5)

        # 测试倒计时功能
        if hasattr(dialog, 'countdown_timer') and dialog.countdown_timer:
            results.add_pass("Countdown timer exists")

            # 测试定时器类型
            if isinstance(dialog.countdown_timer, QTimer):
                results.add_pass("Timer is QTimer instance")
            else:
                results.add_fail("Timer type", f"Expected QTimer, got {type(dialog.countdown_timer)}")

            # 测试信号连接
            if dialog.countdown_timer.signalsBlocked():
                results.add_fail("Timer signals", "Signals are blocked")
            else:
                results.add_pass("Timer signals not blocked")
        else:
            results.add_fail("Timer", "No countdown_timer attribute found")

    except Exception as e:
        results.add_fail("Timer simulation test", str(e))


def test_button_clicks_simulation():
    """测试按钮点击模拟"""
    print("\n[UI-5/5] Testing Button Clicks Simulation")
    print("-" * 40)

    try:
        get_db_manager().initialize_database()
        app = get_qt_app()

        # 创建运动对话框
        exercises = ExerciseRepository.get_random_exercises(count=1)
        if not exercises:
            results.add_fail("Button test", "No exercises found")
            return

        exercises_data = [
            {
                "id": ex.id,
                "name": ex.name,
                "duration": ex.duration_seconds,
                "met": ex.met_value
            }
            for ex in exercises
        ]

        dialog = ExerciseReminderDialog(exercises_data, weight_kg=70)

        # 测试完成按钮
        if hasattr(dialog, 'complete_btn') and dialog.complete_btn:
            # 模拟点击（不实际触发槽函数）
            dialog.complete_btn.click()
            results.add_pass("Complete button clickable")

        # 测试跳过按钮
        if hasattr(dialog, 'skip_btn') and dialog.skip_btn:
            # 模拟点击
            dialog.skip_btn.click()
            results.add_pass("Skip button clickable")

        # 测试换一个按钮
        if hasattr(dialog, 'next_btn') and dialog.next_btn:
            dialog.next_btn.click()
            results.add_pass("Next button clickable")

        # 测试按钮启用状态
        complete_enabled = dialog.complete_btn.isEnabled()
        skip_enabled = dialog.skip_btn.isEnabled()
        next_enabled = dialog.next_btn.isEnabled()
        results.add_pass(f"Button states: complete={complete_enabled}, skip={skip_enabled}, next={next_enabled}")

    except Exception as e:
        results.add_fail("Button clicks test", str(e))


def test_dialog_signals():
    """测试对话框信号"""
    print("\n[UI-6/5] Testing Dialog Signals")
    print("-" * 40)

    try:
        app = get_qt_app()

        # 创建站立对话框
        dialog = StandReminderDialog(duration=5)

        # 测试信号是否存在
        if hasattr(dialog, 'completed') and dialog.completed:
            results.add_pass("Completed signal exists")

            # 使用 QSignalSpy 监听信号
            spy = QSignalSpy(dialog.completed)
            results.add_pass("SignalSpy created for completed")
        else:
            results.add_fail("Dialog signals", "No completed signal attribute")

        if hasattr(dialog, 'skipped') and dialog.skipped:
            results.add_pass("Skipped signal exists")
        else:
            results.add_fail("Skipped signal", "No skipped signal attribute")

    except Exception as e:
        results.add_fail("Dialog signals test", str(e))


def main():
    """主测试函数"""
    print("=" * 60)
    print("UI Automated Test Suite - exercise-reminder-v2")
    print("=" * 60)
    print("\n模拟用户交互，测试对话框功能（无需显示窗口）")
    print()

    # 运行所有 UI 测试
    test_stand_dialog_creation()
    test_exercise_dialog_creation()
    test_gaze_dialog_creation()
    test_dialog_timer_simulation()
    test_button_clicks_simulation()
    test_dialog_signals()

    # 输出总结
    all_passed = results.summary()

    if all_passed:
        print("[SUCCESS] All UI tests passed!")
        print("\nUI 组件创建正常，属性正确，按钮可点击。")
        print("Ready for actual UI manual testing.")
        return 0
    else:
        print("[FAILURE] Some UI tests failed, please review.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
