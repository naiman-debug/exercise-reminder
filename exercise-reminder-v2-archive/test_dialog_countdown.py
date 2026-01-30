# -*- coding: utf-8 -*-
"""
测试对话框倒计时功能
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from src.ui.dialogs.stand_dialog import StandReminderDialog
from src.ui.dialogs.gaze_dialog import GazeReminderDialog
from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog


def test_stand_dialog():
    """测试站立提醒对话框"""
    print("\n=== 测试站立提醒对话框 ===")
    app = QApplication(sys.argv)

    dialog = StandReminderDialog(10)  # 10秒倒计时
    print("站立对话框创建成功")

    # 测试显示
    dialog.show()
    print("站立对话框显示成功")

    # 检查初始倒计时
    print(f"初始倒计时: {dialog.remaining_seconds}秒")

    # 关闭
    dialog.close()
    print("站立对话框测试完成")


def test_gaze_dialog():
    """测试远眺提醒对话框"""
    print("\n=== 测试远眺提醒对话框 ===")
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    dialog = GazeReminderDialog(10)  # 10秒倒计时
    print("远眺对话框创建成功")

    # 测试显示
    dialog.show()
    print("远眺对话框显示成功")

    # 检查初始倒计时
    print(f"初始倒计时: {dialog.remaining_seconds}秒")

    # 关闭
    dialog.close()
    print("远眺对话框测试完成")


def test_exercise_dialog():
    """测试微运动提醒对话框"""
    print("\n=== 测试微运动提醒对话框 ===")
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    exercises = [{"name": "深蹲", "duration": 10, "met": 5.0}]
    dialog = ExerciseReminderDialog(exercises, 70.0)
    print("微运动对话框创建成功")

    # 测试显示
    dialog.show()
    print("微运动对话框显示成功")

    # 检查初始倒计时
    print(f"初始倒计时: {dialog.remaining_seconds}秒")
    print(f"当前动作: {dialog.current_exercise['name']}")
    print(f"动作时长: {dialog.duration}秒")

    # 关闭
    dialog.close()
    print("微运动对话框测试完成")


if __name__ == '__main__':
    try:
        test_stand_dialog()
        test_gaze_dialog()
        test_exercise_dialog()
        print("\n=== 所有测试完成 ===")
    except Exception as e:
        print(f"\n!!! 测试失败: {e}")
        import traceback
        traceback.print_exc()
