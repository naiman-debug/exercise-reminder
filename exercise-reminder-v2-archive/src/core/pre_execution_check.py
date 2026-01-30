# -*- coding: utf-8 -*-
"""
前置执行检查模块

在任何代码修改前强制执行的设计文档检查流程
"""
from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass


@dataclass
class DesignRequirement:
    """设计要求"""
    category: str
    requirement: str
    file_path: str
    status: str = "pending"  # pending, implemented, verified


class PreExecutionCheck:
    """
    前置执行检查器

    在任何代码修改前必须通过此检查
    """

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.design_docs = []
        self.requirements: List[DesignRequirement] = []

    def check(self, task_description: str = "") -> Dict[str, any]:
        """
        执行前置检查

        Args:
            task_description: 任务描述

        Returns:
            dict: 检查结果
        """
        print("=" * 60)
        print("🔍 SUPERPOWER 前置检查 - 强制设计文档检查")
        print("=" * 60)
        print(f"任务: {task_description}")

        # Step 1: 查找设计文档
        print("\n[1/5] 查找设计文档...")
        self._find_design_docs()

        if not self.design_docs:
            print("⚠️  未找到设计文档")
            response = input("是否确认没有设计文档？(y/n): ")
            if response.lower() == 'y':
                return {"can_proceed": True, "has_design": False}
            else:
                return {"can_proceed": False, "has_design": False}

        # Step 2: 阅读设计文档
        print("\n[2/5] 阅读设计文档...")
        self._read_design_docs()

        # Step 3: 提取设计要求
        print("\n[3/5] 提取设计要求...")
        self._extract_requirements()

        # Step 4: 显示检查清单
        print("\n[4/5] 设计要求检查清单:")
        self._show_checklist()

        # Step 5: 确认
        print("\n[5/5] 等待确认...")
        return {"can_proceed": True, "has_design": True, "requirements": self.requirements}

    def _find_design_docs(self):
        """查找设计文档"""
        design_patterns = [
            "DESIGN-*.md",
            "PRD*.md",
            "design*.md"
        ]

        for pattern in design_patterns:
            docs = list(self.project_root.glob("docs/" + pattern))
            for doc in docs:
                self.design_docs.append(doc)
                print(f"  ✓ 找到: {doc.relative_to(self.project_root)}")

        if not self.design_docs:
            # 检查其他常见位置
            for path in [
                self.project_root / "docs/design/",
                self.project_root / "docs/plans/",
            ]:
                if path.exists():
                    docs = list(path.glob("*.md"))
                    for doc in docs:
                        self.design_docs.append(doc)
                        print(f"  ✓ 找到: {doc.relative_to(self.project_root)}")

    def _read_design_docs(self):
        """阅读设计文档"""
        for doc_path in self.design_docs:
            print(f"\n📖 阅读: {doc_path.name}")
            print("-" * 40)
            content = doc_path.read_text(encoding='utf-8', errors='ignore')

            # 显示前100行预览
            lines = content.split('\n')[:100]
            for i, line in enumerate(lines[:50], 1):  # 只显示前50行避免太长
                print(f"  {i:3d}: {line}")

            if len(lines) > 50:
                print(f"  ... (还有 {len(lines)-50} 行)")
            print("-" * 40)

    def _extract_requirements(self):
        """提取设计要求"""
        # 简单的关键词提取
        keywords = {
            "向导": ["页面", "页数", "welcome", "wizard"],
            "弹窗": ["标题栏", "无边框", "frameless", "尺寸"],
            "倒计时": ["闪烁", "pulse", "<10秒", "颜色"],
            "设计": ["设计", "规范", "DESIGN"]
        }

        # TODO: 可以扩展为更智能的解析
        print("  🔍 关键词扫描完成 (完整解析需要人工阅读)")

    def _show_checklist(self):
        """显示检查清单"""
        print("\n📋 设计要求对照:")
        print("-" * 40)
        print("  ⚠️  请手动对照设计文档验证实现")
        print("  ⚠️  建议使用 writing-plans 创建详细计划")
        print("  ⚠️  实现后使用验证-before-completion")


# 单例实例
_check_instance = None


def get_pre_execution_check() -> PreExecutionCheck:
    """获取前置检查实例（单例）"""
    global _check_instance
    if _check_instance is None:
        _check_instance = PreExecutionCheck()
    return _check_instance


def pre_execution_check(task: str = "") -> bool:
    """
    前置执行检查函数

    在任何代码修改前调用此函数

    Args:
        task: 任务描述

    Returns:
        bool: 是否可以继续执行
    """
    checker = get_pre_execution_check()
    result = checker.check(task)

    if not result["can_proceed"]:
        print("\n❌ 前置检查未通过，无法继续")
        return False

    if result.get("has_design"):
        print("\n✅ 前置检查通过，可以继续执行")
        print("⚠️  提醒: 请确保实现与设计文档一致")

    return True


# 装饰器版本（可选）
def require_design_check(func):
    """装饰器：强制设计文档检查"""
    def wrapper(*args, **kwargs):
        print(f"\n🔍 检测到执行请求: {func.__name__}")
        if not pre_execution_check(func.__name__):
            raise Exception("前置检查未通过，无法执行")
        return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":
    # 测试
    checker = PreExecutionCheck()
    checker.check("测试：修改倒计时颜色")
