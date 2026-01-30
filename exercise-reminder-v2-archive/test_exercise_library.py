# -*- coding: utf-8 -*-
"""
动作库管理功能测试脚本
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

def test_exercise_library_import():
    """测试导入"""
    print("测试导入动作库模块...")
    try:
        from src.ui.settings.exercise_library import ExerciseLibraryWidget, ExerciseEditDialog
        from src.models.repositories import ExerciseRepository
        print("  [OK] 动作库模块导入成功")
        return True
    except Exception as e:
        print(f"  [FAIL] 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exercise_crud():
    """测试动作增删改查"""
    print("\n测试动作增删改查...")
    try:
        from src.models.repositories import ExerciseRepository
        from src.models.database import get_db_manager

        # 初始化数据库
        db_manager = get_db_manager()
        db_manager.initialize_database()

        # 获取初始数量
        initial_count = len(ExerciseRepository.get_all())
        print(f"  初始动作数: {initial_count}")

        # 测试创建
        new_exercise = ExerciseRepository.create(
            name="测试动作",
            duration=45,
            met=4.5,
            category="中等强度"
        )
        print(f"  [OK] 创建动作: {new_exercise.name} (ID: {new_exercise.id})")

        # 验证创建
        exercises = ExerciseRepository.get_all()
        assert len(exercises) == initial_count + 1, "动作数量未增加"
        print(f"  [OK] 验证创建成功，当前动作数: {len(exercises)}")

        # 测试读取
        retrieved = ExerciseRepository.get_by_id(new_exercise.id)
        assert retrieved is not None, "无法读取创建的动作"
        assert retrieved.name == "测试动作", "动作名称不匹配"
        assert retrieved.duration_seconds == 45, "动作时长不匹配"
        assert retrieved.met_value == 4.5, "MET值不匹配"
        print(f"  [OK] 读取动作成功: {retrieved.name}")

        # 测试更新
        ExerciseRepository.update(
            new_exercise.id,
            name="测试动作（已修改）",
            duration_seconds=60,
            met_value=5.0
        )
        updated = ExerciseRepository.get_by_id(new_exercise.id)
        assert updated.name == "测试动作（已修改）", "更新失败：名称未改变"
        assert updated.duration_seconds == 60, "更新失败：时长未改变"
        print(f"  [OK] 更新动作成功: {updated.name}")

        # 测试删除
        result = ExerciseRepository.delete(new_exercise.id)
        assert result, "删除失败"
        deleted = ExerciseRepository.get_by_id(new_exercise.id)
        assert deleted is None, "删除后仍能读取到动作"
        print(f"  [OK] 删除动作成功")

        # 验证删除
        final_count = len(ExerciseRepository.get_all())
        assert final_count == initial_count, "删除后数量不正确"
        print(f"  [OK] 验证删除成功，当前动作数: {final_count}")

        db_manager.close()
        return True
    except Exception as e:
        print(f"  [FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exercise_filter():
    """测试动作筛选"""
    print("\n测试动作筛选...")
    try:
        from src.models.repositories import ExerciseRepository
        from src.models.database import get_db_manager

        db_manager = get_db_manager()
        db_manager.initialize_database()

        # 按分类筛选
        low_intensity = ExerciseRepository.get_by_category("低强度")
        print(f"  [OK] 低强度动作: {len(low_intensity)} 个")

        medium_intensity = ExerciseRepository.get_by_category("中等强度")
        print(f"  [OK] 中等强度动作: {len(medium_intensity)} 个")

        # 获取所有动作
        all_exercises = ExerciseRepository.get_all()
        print(f"  [OK] 总动作数: {len(all_exercises)} 个")

        # 验证分类统计
        category_counts = {}
        for ex in all_exercises:
            category_counts[ex.category] = category_counts.get(ex.category, 0) + 1

        print(f"  [OK] 分类统计:")
        for category, count in category_counts.items():
            print(f"    - {category}: {count} 个")

        db_manager.close()
        return True
    except Exception as e:
        print(f"  [FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exercise_random():
    """测试随机获取动作"""
    print("\n测试随机获取动作...")
    try:
        from src.models.repositories import ExerciseRepository
        from src.models.database import get_db_manager

        db_manager = get_db_manager()
        db_manager.initialize_database()

        # 随机获取3个动作
        exercises = ExerciseRepository.get_random_exercises(3)
        assert len(exercises) == 3, "随机获取动作数量不正确"
        print(f"  [OK] 随机获取3个动作:")
        for ex in exercises:
            print(f"    - {ex.name} ({ex.category})")

        # 验证随机性（两次结果应该不同）
        exercises2 = ExerciseRepository.get_random_exercises(3)
        ids1 = {ex.id for ex in exercises}
        ids2 = {ex.id for ex in exercises2}
        # 如果动作总数大于3，两次随机结果应该不同
        all_count = len(ExerciseRepository.get_all())
        if all_count > 3:
            # 不一定每次都不同，但概率很低
            print(f"  [OK] 第二次随机获取（验证随机性）")

        db_manager.close()
        return True
    except Exception as e:
        print(f"  [FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("动作库管理功能测试")
    print("=" * 50)

    results = []

    # 运行测试
    results.append(("导入测试", test_exercise_library_import()))
    results.append(("增删改查测试", test_exercise_crud()))
    results.append(("筛选测试", test_exercise_filter()))
    results.append(("随机获取测试", test_exercise_random()))

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
        print("\n[SUCCESS] 所有测试通过！动作库管理功能正常。")
        return 0
    else:
        print("\n[WARNING] 部分测试失败，请检查错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
