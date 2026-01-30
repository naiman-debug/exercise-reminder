# -*- coding: utf-8 -*-
"""
MET 热量计算器（极简版）

使用统一公式：热量 = MET值 × 体重(kg) × 时长(小时)
"""
from typing import Union


class METCalculator:
    """
    MET 热量计算器（极简版）

    核心公式：热量 = MET值 × 体重(kg) × 时长(小时)

    统一 MET 值：
    - 中等强度：6.0（适配深蹲、弓步、平板支撑等办公室常见运动）
    - 高强度：8.0（快速开合跳、波比跳等）
    """

    # 统一 MET 值
    MET_MODERATE = 6.0  # 中等强度
    MET_HIGH = 8.0      # 高强度

    @staticmethod
    def calculate_calories(
        met_value: float,
        weight_kg: float,
        duration_seconds: int
    ) -> float:
        """
        计算消耗热量（极简公式）

        Args:
            met_value: MET 值（推荐使用 6.0 或 8.0）
            weight_kg: 体重（千克）
            duration_seconds: 时长（秒）

        Returns:
            float: 消耗热量（千卡），保留1位小数

        示例：
            >>> METCalculator.calculate_calories(6.0, 70, 30)
            3.5
            >>> METCalculator.calculate_calories(6.0, 70, 120)
            14.0
        """
        # 将秒转换为小时
        duration_hours = duration_seconds / 3600.0

        # 计算热量（极简公式，无效率因子）
        calories = met_value * weight_kg * duration_hours

        return round(calories, 1)

    @staticmethod
    def calculate_calories_by_exercise(
        met_value: float,
        duration_seconds: int,
        weight_kg: float = None
    ) -> float:
        """
        根据动作计算消耗热量

        Args:
            met_value: MET 值
            duration_seconds: 时长（秒）
            weight_kg: 体重（千克），如果为 None 则使用默认值

        Returns:
            float: 消耗热量（千卡），保留1位小数
        """
        if weight_kg is None:
            weight_kg = 70.0  # 默认体重

        return METCalculator.calculate_calories(
            met_value,
            weight_kg,
            duration_seconds
        )

    @staticmethod
    def get_met_reference() -> dict:
        """
        获取简化的 MET 值参考表

        Returns:
            dict: {分类: MET值}
        """
        return {
            "中等强度": METCalculator.MET_MODERATE,  # 6.0
            "高强度": METCalculator.MET_HIGH,        # 8.0
        }

    @staticmethod
    def estimate_met_by_intensity(intensity: str) -> float:
        """
        根据强度估算 MET 值（简化版）

        Args:
            intensity: 强度（低/中/高）

        Returns:
            float: 估算的 MET 值
        """
        # 简化映射：只有中等和高强度
        met_map = {
            "低": METCalculator.MET_MODERATE,
            "低强度": METCalculator.MET_MODERATE,
            "中": METCalculator.MET_MODERATE,
            "中等": METCalculator.MET_MODERATE,
            "中等强度": METCalculator.MET_MODERATE,
            "高": METCalculator.MET_HIGH,
            "高强度": METCalculator.MET_HIGH,
            "中高强度": METCalculator.MET_HIGH,
        }

        return met_map.get(intensity, METCalculator.MET_MODERATE)


def calculate_calories(
    met_value: float,
    weight_kg: float,
    duration_seconds: int
) -> float:
    """
    便捷函数：计算热量

    Args:
        met_value: MET 值
        weight_kg: 体重（千克）
        duration_seconds: 时长（秒）

    Returns:
        float: 消耗热量（千卡），保留1位小数
    """
    return METCalculator.calculate_calories(
        met_value,
        weight_kg,
        duration_seconds
    )
