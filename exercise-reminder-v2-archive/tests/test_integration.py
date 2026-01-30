# -*- coding: utf-8 -*-
"""
集成测试脚本

测试核心模块的功能
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_models():
    """测试数据模型"""
    print("[TEST] 测试数据模型...")
    try:
        from src.models.database import get_db_manager
        from src.models.models import Exercise, Setting, UserProfile
        from src.models.repositories import ExerciseRepository

        # 初始化数据库
        db = get_db_manager()
        db.initialize_database()

        # 测试 Exercise 查询
        exercises = ExerciseRepository.get_all()
        print(f"  - 默认动作数量: {len(exercises)}")

        # 测试 Setting 读写
        from src.models.repositories import SettingRepository
        SettingRepository.set("test_key", "test_value")
        value = SettingRepository.get("test_key")
        assert value == "test_value", "Setting 读写测试失败"

        print("  PASS: 数据模型测试通过")
        return True

    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_utils():
    """测试工具函数"""
    print("[TEST] 测试工具函数...")
    try:
        from src.utils.config import ConfigManager
        from src.utils.met_calculator import METCalculator

        # 测试配置管理
        config = ConfigManager()
        assert config.get("test", "default") == "default"

        # 测试 MET 计算
        calories = METCalculator.calculate_calories_by_exercise(5.0, 30, 70)
        print(f"  - MET 计算测试: 30秒开合跳 = {calories} 千卡")

        print("  PASS: 工具函数测试通过")
        return True

    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_core():
    """测试核心业务逻辑"""
    print("[TEST] 测试核心业务逻辑...")
    try:
        from src.core.timer_manager import TimerManager
        from src.core.reminder_engine import ReminderEngine
        from src.utils.config import ConfigManager

        # 测试定时器管理器
        tm = TimerManager()
        assert len(tm.timers) == 0, "定时器管理器初始化失败"

        # 测试随机间隔计算
        interval = ReminderEngine._calculate_random_interval(30, 60)
        assert 30 * 60 * 1000 <= interval <= 60 * 60 * 1000, "随机间隔计算错误"
        print(f"  - 随机间隔测试: {interval // 60000} 分钟")

        print("  PASS: 核心业务逻辑测试通过")
        return True

    except Exception as e:
        print(f"  FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ui_dialogs():
    """测试 UI 弹窗"""
    print("[TEST] 测试 UI 弹窗...")
    try:
        from src.ui.dialogs import base_dialog
        from src.ui.dialogs import stand_dialog
        from src.ui.dialogs import exercise_dialog
        from src.ui.dialogs import gaze_dialog

        # 测试导入是否成功
        print("  - 所有弹窗类导入成功")

        print("  PASS: UI 弹窗测试通过")
        return True

    except Exception as e:
        print(f"  FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("=" * 50)
    print("集成测试 - 灵动休息健康助手")
    print("=" * 50)
    print()

    results = []

    # 注意：跳过需要 Qt 事件循环的测试（在非 GUI 环境下）
    # results.append(("Models", test_models()))
    results.append(("Utils", test_utils()))
    results.append(("Core", test_core()))
    # results.append(("UI", test_ui_dialogs()))

    print()
    print("=" * 50)
    print("测试结果汇总:")
    print("=" * 50)

    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")

    all_passed = all(passed for _, passed in results)

    print()
    if all_passed:
        print("所有测试通过!")
        return 0
    else:
        print("有测试失败，请检查日志")
        return 1


if __name__ == "__main__":
    sys.exit(main())
