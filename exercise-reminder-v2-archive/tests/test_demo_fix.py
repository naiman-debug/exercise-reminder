# -*- coding: utf-8 -*-
"""
自动化测试：验证 demo.py 的 QApplication 单例修复

测试每个演示函数是否能正确复用 QApplication 实例
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from demo import get_or_create_qt_app


def test_qapplication_singleton():
    """测试 QApplication 单例模式"""
    print("=" * 60)
    print("测试 QApplication 单例模式")
    print("=" * 60)

    # 第一次调用应该创建新实例
    app1 = get_or_create_qt_app()
    print(f"[OK] First call successful: {type(app1).__name__}")

    # 第二次调用应该返回同一实例
    app2 = get_or_create_qt_app()
    print(f"[OK] Second call successful: {type(app2).__name__}")

    # 验证是同一个实例
    assert app1 is app2, "[FAIL] Should return same instance"
    print("[OK] Both calls return same instance")

    # 验证只有一个 QApplication 实例
    instance = QApplication.instance()
    assert instance is not None, "[FAIL] Instance should exist"
    assert instance is app1, "[FAIL] instance() should return same object"
    print("[OK] QApplication.instance() returns correct instance")

    print()
    print("=" * 60)
    print("所有测试通过！")
    print("=" * 60)
    return True


def test_multiple_calls():
    """测试多次调用不会报错"""
    print()
    print("=" * 60)
    print("测试多次调用安全性")
    print("=" * 60)

    apps = []
    for i in range(5):
        app = get_or_create_qt_app()
        apps.append(app)
        print(f"[OK] Call {i+1} successful")

    # 验证所有返回的是同一个实例
    for i in range(len(apps) - 1):
        assert apps[i] is apps[i+1], f"[FAIL] Call {i} and {i+1} returned different instances"

    print("[OK] All 5 calls return same instance")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        test_qapplication_singleton()
        test_multiple_calls()
        print()
        print("[PASS] 所有自动化测试通过")
        sys.exit(0)
    except AssertionError as e:
        print()
        print(f"[FAIL] 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"[ERROR] 测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
