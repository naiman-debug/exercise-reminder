# -*- coding: utf-8 -*-
"""
Evidence 验证脚本

验证项目级 Evidence 规范是否被遵守
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_item(name, test_func, success_msg=None):
    """执行单项测试"""
    try:
        result = test_func()
        if result:
            print(f"[{name}] [PASS]")
            if success_msg:
                print(f"  {success_msg}")
            return True
        else:
            print(f"[{name}] [FAIL]")
            return False
    except Exception as e:
        print(f"[{name}] [ERROR]: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("Evidence Validation Script")
    print("=" * 60)
    print()

    passed = 0
    failed = 0

    # 1. 检查 Evidence 规范文档存在
    if test_item("Evidence Spec",
                 lambda: (project_root / "docs" / "EVIDENCE-SPEC.md").exists(),
                 "docs/EVIDENCE-SPEC.md exists"):
        passed += 1
    else:
        failed += 1

    # 2. 检查归档文档存在
    def check_archive():
        archive_files = list((project_root).glob("CC-ARCHIVE-*.md"))
        return len(archive_files) > 0

    if test_item("Archive Document", check_archive, "CC-ARCHIVE-*.md exists"):
        passed += 1
    else:
        failed += 1

    # 3. 检查数据库初始化正常
    def test_db():
        from src.models.database import get_db_manager
        db = get_db_manager()
        db.initialize_database()
        return True

    if test_item("Database Init", test_db, "Database initializes correctly"):
        passed += 1
    else:
        failed += 1

    # 4. 检查弹窗可以导入
    def test_dialogs():
        from src.ui.dialogs.stand_dialog import StandReminderDialog
        from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog
        from src.ui.dialogs.gaze_dialog import GazeReminderDialog
        return True

    if test_item("Dialogs Import", test_dialogs, "All dialog modules import correctly"):
        passed += 1
    else:
        failed += 1

    # 5. 检查音频模块导入
    def test_audio():
        from src.utils.audio_player import AudioManager
        return True

    if test_item("Audio Module", test_audio, "Audio module imports correctly"):
        passed += 1
    else:
        failed += 1

    # 6. 检查音效目录存在
    if test_item("Sounds Directory",
                 lambda: (project_root / "src" / "resources" / "sounds").exists(),
                 "src/resources/sounds directory exists"):
        passed += 1
    else:
        failed += 1

    # 7. 检查 demo.py 存在
    if test_item("Demo Script",
                 lambda: (project_root / "demo.py").exists(),
                 "demo.py exists"):
        passed += 1
    else:
        failed += 1

    # 8. 检查主程序存在
    if test_item("Main Program",
                 lambda: (project_root / "src" / "main.py").exists(),
                 "src/main.py exists"):
        passed += 1
    else:
        failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print()
        print("All checks passed! Evidence spec is correctly implemented.")
        return 0
    else:
        print()
        print(f"{failed} check(s) failed. Please fix and retry.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
