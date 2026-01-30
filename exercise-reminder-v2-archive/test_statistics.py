# -*- coding: utf-8 -*-
"""
统计功能测试脚本
"""
import sys
import io
from pathlib import Path
from datetime import date, datetime, timedelta

# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_statistics_import():
    """测试导入"""
    print("测试导入统计模块...")
    try:
        from src.ui.statistics.statistics_widget import (
            StatisticsWidget, StatCard, CalorieChart,
            ActivityChart, RecentActivityList
        )
        print("  [OK] 统计模块导入成功")
        return True
    except Exception as e:
        print(f"  [FAIL] 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_today_stats():
    """测试今日统计"""
    print("\n测试今日统计...")
    try:
        from src.models.repositories import ActivityRepository
        from src.models.database import get_db_manager

        db_manager = get_db_manager()
        db_manager.initialize_database()

        # 获取今日统计
        stats = ActivityRepository.get_today_stats()
        print(f"  [OK] 今日统计:")
        print(f"    - 站立: {stats['stand_count']} 次, {stats['stand_duration']} 秒")
        print(f"    - 运动: {stats['exercise_count']} 次, {stats['exercise_duration']} 秒, {stats['exercise_calories']:.1f} 千卡")
        print(f"    - 远眺: {stats['gaze_count']} 次, {stats['gaze_duration']} 秒")
        print(f"    - 跳过: {stats['exercise_skipped']} 次")

        db_manager.close()
        return True
    except Exception as e:
        print(f"  [FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_calories_data():
    """测试热量数据"""
    print("\n测试热量数据...")
    try:
        from src.models.repositories import ActivityRepository
        from src.models.database import get_db_manager

        db_manager = get_db_manager()
        db_manager.initialize_database()

        # 获取今日热量
        today = date.today()
        calories_today = ActivityRepository.get_calories_by_date(today)
        print(f"  [OK] 今日热量: {calories_today:.1f} 千卡")

        # 获取最近7天热量
        calories_7days = ActivityRepository.get_calories_last_7_days()
        print(f"  [OK] 最近7天热量:")
        for item in calories_7days:
            print(f"    - {item['date']}: {item['calories']:.1f} 千卡")

        db_manager.close()
        return True
    except Exception as e:
        print(f"  [FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_recent_activities():
    """测试最近活动"""
    print("\n测试最近活动...")
    try:
        from src.models.repositories import ActivityRepository
        from src.models.database import get_db_manager

        db_manager = get_db_manager()
        db_manager.initialize_database()

        # 添加一些测试数据
        ActivityRepository.log_stand(90)
        ActivityRepository.log_exercise(30, 5.0, completed=True)
        ActivityRepository.log_gaze(60)

        # 获取最近活动
        activities = ActivityRepository.get_recent_activities(5)
        print(f"  [OK] 最近活动 (最近5条):")
        for activity in activities:
            type_name = {"stand": "站立", "exercise": "运动", "gaze": "远眺"}.get(activity.activity_type, activity.activity_type)
            status = "完成" if activity.completed else ("跳过" if activity.skipped else "")
            calories_text = f", {activity.calories_burned:.0f}千卡" if activity.calories_burned > 0 else ""
            print(f"    - [{activity.timestamp.strftime('%H:%M')}] {type_name} {activity.duration_seconds}秒{calories_text} {status}")

        db_manager.close()
        return True
    except Exception as e:
        print(f"  [FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_statistics_widget():
    """测试统计组件"""
    print("\n测试统计组件...")
    try:
        from src.ui.statistics.statistics_widget import StatisticsWidget
        from PySide6.QtWidgets import QApplication

        app = QApplication.instance() or QApplication(sys.argv)

        # 创建统计组件
        widget = StatisticsWidget()
        print(f"  [OK] 统计组件创建成功")

        # 刷新数据
        widget.refresh_data()
        print(f"  [OK] 数据刷新成功")

        return True
    except Exception as e:
        print(f"  [FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("统计功能测试")
    print("=" * 50)

    results = []

    # 运行测试
    results.append(("导入测试", test_statistics_import()))
    results.append(("今日统计测试", test_today_stats()))
    results.append(("热量数据测试", test_calories_data()))
    results.append(("最近活动测试", test_recent_activities()))
    results.append(("统计组件测试", test_statistics_widget()))

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
        print("\n[SUCCESS] 所有测试通过！统计功能正常。")
        return 0
    else:
        print("\n[WARNING] 部分测试失败，请检查错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
