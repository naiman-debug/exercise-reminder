# -*- coding: utf-8 -*-
"""
核心功能测试脚本
"""
import sys
import io
from pathlib import Path

# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试导入"""
    print("测试导入模块...")
    try:
        from src.core.app import Application
        from src.core.reminder_engine import ReminderEngine
        from src.core.timer_manager import TimerManager
        from src.core.punishment_logic import PunishmentLogic
        from src.models.database import get_db_manager
        from src.utils.config import ConfigManager
        print("  [OK] 所有模块导入成功")
        return True
    except Exception as e:
        print(f"  [FAIL] 导入失败: {e}")
        return False

def test_database():
    """测试数据库"""
    print("\n测试数据库...")
    try:
        from src.models.database import get_db_manager
        from src.models.models import Exercise, Setting

        db_manager = get_db_manager()
        db_manager.initialize_database()

        # 检查数据
        exercise_count = Exercise.select().count()
        setting_count = Setting.select().count()

        print(f"  [OK] 数据库初始化成功")
        print(f"    - 默认动作数: {exercise_count}")
        print(f"    - 设置项数: {setting_count}")

        db_manager.close()
        return True
    except Exception as e:
        print(f"  [FAIL] 数据库测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """测试配置"""
    print("\n测试配置...")
    try:
        from src.utils.config import ConfigManager

        config = ConfigManager()
        print(f"  [OK] 配置加载成功")
        print(f"    - 站立提醒: {config.is_reminder_enabled('stand')}")
        print(f"    - 运动提醒: {config.is_reminder_enabled('exercise')}")
        print(f"    - 远眺提醒: {config.is_reminder_enabled('gaze')}")
        print(f"    - 用户体重: {config.get_user_weight()} kg")
        return True
    except Exception as e:
        print(f"  [FAIL] 配置测试失败: {e}")
        return False

def test_timer_manager():
    """测试定时器管理器"""
    print("\n测试定时器管理器...")
    try:
        from src.core.timer_manager import TimerManager
        from PySide6.QtWidgets import QApplication

        # 创建 Qt 应用（定时器需要）
        app = QApplication.instance() or QApplication(sys.argv)

        tm = TimerManager()
        print(f"  [OK] 定时器管理器创建成功")

        # 测试创建定时器
        timer = tm.create_timer("test", 1000)
        print(f"    - 测试定时器创建: OK")

        tm.clear_all()
        print(f"    - 清除定时器: OK")

        return True
    except Exception as e:
        print(f"  [FAIL] 定时器管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_reminder_engine():
    """测试提醒引擎"""
    print("\n测试提醒引擎...")
    try:
        from src.core.reminder_engine import ReminderEngine
        from src.core.timer_manager import TimerManager
        from src.utils.config import ConfigManager
        from PySide6.QtWidgets import QApplication

        app = QApplication.instance() or QApplication(sys.argv)

        config = ConfigManager()
        tm = TimerManager()
        engine = ReminderEngine(tm, config)

        print(f"  [OK] 提醒引擎创建成功")

        # 测试随机间隔计算
        interval = engine._calculate_random_interval(30, 60)
        print(f"    - 随机间隔: {interval} ms (范围: 30-60分钟)")

        return True
    except Exception as e:
        print(f"  [FAIL] 提醒引擎测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("灵动休息 - 核心功能测试")
    print("=" * 50)

    results = []

    # 运行测试
    results.append(("导入测试", test_imports()))
    results.append(("数据库测试", test_database()))
    results.append(("配置测试", test_config()))
    results.append(("定时器管理器测试", test_timer_manager()))
    results.append(("提醒引擎测试", test_reminder_engine()))

    # 汇总结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[PASS] 通过" if result else "[FAIL] 失败"
        print(f"  {name}: {status}")

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n[SUCCESS] 所有测试通过！应用核心功能正常。")
        return 0
    else:
        print("\n[WARNING] 部分测试失败，请检查错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
