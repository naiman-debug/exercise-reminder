# -*- coding: utf-8 -*-
"""
Hook 测试脚本

测试 Pre-commit Hook 的假验证检测逻辑
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_fake_patterns():
    """测试假验证模式检测"""
    from git.hooks.pre_commit import check_fake_verification, check_real_verification

    fake_commands = [
        'python -c "from src.ui.dialogs import"',
        'python -c "import audio_player"',
        'ls src/main.py',
        'dir src/main.py',
        'grep "pattern" file',
        'cat docs/EVIDENCE-SPEC.md',
        'type file.txt',
    ]

    print("=" * 60)
    print("测试假验证模式检测")
    print("=" * 60)

    all_detected = True
    for cmd in fake_commands:
        is_fake = check_fake_verification(cmd)
        is_real = check_real_verification(cmd)
        status = "✓" if is_fake and not is_real else "✗"
        print(f"{status} {cmd}")
        print(f"   假验证: {is_fake}, 真实验证: {is_real}")
        if not is_fake:
            all_detected = False

    print()
    if all_detected:
        print("✅ 所有假验证模式都被正确检测")
    else:
        print("❌ 部分假验证模式未被检测")

    return all_detected


def test_real_patterns():
    """测试真实验证模式检测"""
    from git.hooks.pre_commit import check_fake_verification, check_real_verification

    real_commands = [
        'python src/main.py',
        'python demo.py',
        'python tests/test_dialogs.py',
        'pytest tests/',
    ]

    print()
    print("=" * 60)
    print("测试真实验证模式检测")
    print("=" * 60)

    all_detected = True
    for cmd in real_commands:
        is_fake = check_fake_verification(cmd)
        is_real = check_real_verification(cmd)
        status = "✓" if is_real and not is_fake else "✗"
        print(f"{status} {cmd}")
        print(f"   假验证: {is_fake}, 真实验证: {is_real}")
        if not is_real:
            all_detected = False

    print()
    if all_detected:
        print("✅ 所有真实验证模式都被正确识别")
    else:
        print("❌ 部分真实验证模式未被识别")

    return all_detected


def main():
    """主函数"""
    print()
    print("Hook 测试脚本")
    print()

    # 由于 hook 脚本在 .git/hooks/ 下，需要特殊导入方式
    # 这里直接测试核心逻辑函数

    # 将 hook 脚本的核心逻辑复制过来测试
    FAKE_PATTERNS = [
        r'^python\s+-c\s+".*from\s+\S+\s+import',
        r'^python\s+-c\s+"*import\s+',
        r'^ls\s+',
        r'^dir\s+',
        r'^grep\s+',
        r'^cat\s+',
        r'^type\s+',
    ]

    REAL_PATTERNS = [
        r'^python\s+src/main\.py',
        r'^python\s+demo\.py',
        r'^python\s+tests/test_',
        r'^python\s+.*\.py\s+.*→',
        r'^pytest\s+',
    ]

    import re

    def check_fake(command: str) -> bool:
        for pattern in FAKE_PATTERNS:
            if re.match(pattern, command.strip()):
                return True
        return False

    def check_real(command: str) -> bool:
        for pattern in REAL_PATTERNS:
            if re.match(pattern, command.strip()):
                return True
        return False

    # 测试假验证
    print("=" * 60)
    print("测试假验证模式检测")
    print("=" * 60)

    fake_commands = [
        'python -c "from src.ui.dialogs import"',
        'python -c "import audio_player"',
        'ls src/main.py',
        'grep "pattern" file',
        'cat docs/EVIDENCE-SPEC.md',
    ]

    all_fake_ok = True
    for cmd in fake_commands:
        is_fake = check_fake(cmd)
        is_real = check_real(cmd)
        status = "[OK]" if is_fake and not is_real else "[FAIL]"
        print(f"{status} {cmd} -> Fake:{is_fake}, Real:{is_real}")
        if not is_fake:
            all_fake_ok = False

    print()
    # 测试真实验证
    print("=" * 60)
    print("测试真实验证模式检测")
    print("=" * 60)

    real_commands = [
        'python src/main.py → 应用启动成功',
        'python demo.py → 演示可用',
        'python tests/test_dialogs.py → 通过',
        'pytest tests/',
    ]

    all_real_ok = True
    for cmd in real_commands:
        is_fake = check_fake(cmd)
        is_real = check_real(cmd)
        status = "[OK]" if is_real and not is_fake else "[FAIL]"
        print(f"{status} {cmd} -> Fake:{is_fake}, Real:{is_real}")
        if not is_real:
            all_real_ok = False

    print()
    print("=" * 60)
    if all_fake_ok and all_real_ok:
        print("[PASS] All tests passed! Hook logic is correct.")
        return 0
    else:
        print("[FAIL] Some tests failed, need to fix Hook logic.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
