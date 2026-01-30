# -*- coding: utf-8 -*-
"""
BMR 基础代谢率计算器

使用 Mifflin-St Jeor 公式计算基础代谢率
"""
from typing import Union
from enum import Enum


class Gender(Enum):
    """性别枚举"""
    MALE = "male"      # 男性
    FEMALE = "female"  # 女性


class BMRCalculator:
    """
    基础代谢率（BMR）计算器

    使用 Mifflin-St Jeor 公式：
    - 男性: BMR = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄) + 5
    - 女性: BMR = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄) - 161
    """

    @staticmethod
    def calculate_bmr(
        weight_kg: float,
        height_cm: int,
        age: int,
        gender: Union[Gender, str] = Gender.MALE
    ) -> float:
        """
        计算基础代谢率（BMR）

        Args:
            weight_kg: 体重（千克）
            height_cm: 身高（厘米）
            age: 年龄（岁）
            gender: 性别（Gender.MALE 或 Gender.FEMALE）

        Returns:
            float: 基础代谢率（千卡/天）

        示例：
            >>> BMRCalculator.calculate_bmr(70, 175, 30, Gender.MALE)
            1685.0
        """
        # 转换 gender 参数
        if isinstance(gender, str):
            gender = Gender.MALE if gender.lower() in ["male", "m", "男", "男性"] else Gender.FEMALE

        # Mifflin-St Jeor 公式
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)

        if gender == Gender.MALE:
            bmr += 5
        else:
            bmr -= 161

        return round(bmr, 1)

    @staticmethod
    def calculate_tdee(
        weight_kg: float,
        height_cm: int,
        age: int,
        gender: Union[Gender, str] = Gender.MALE,
        activity_level: float = 1.2
    ) -> float:
        """
        计算每日总能量消耗（TDEE）

        Args:
            weight_kg: 体重（千克）
            height_cm: 身高（厘米）
            age: 年龄（岁）
            gender: 性别
            activity_level: 活动系数
                - 久坐不动: 1.2
                - 轻度活动: 1.375
                - 中度活动: 1.55
                - 高度活动: 1.725
                - 极重度活动: 1.9

        Returns:
            float: 每日总能量消耗（千卡/天）
        """
        bmr = BMRCalculator.calculate_bmr(weight_kg, height_cm, age, gender)
        return round(bmr * activity_level, 1)

    @staticmethod
    def get_activity_levels() -> dict:
        """
        获取活动系数参考表

        Returns:
            dict: {活动级别: 系数}
        """
        return {
            "久坐不动（办公室工作，几乎不运动）": 1.2,
            "轻度活动（每周1-3次轻度运动）": 1.375,
            "中度活动（每周3-5次中等运动）": 1.55,
            "高度活动（每周6-7次高强度运动）": 1.725,
            "极重度活动（体力工作或每天高强度训练）": 1.9,
        }

    @staticmethod
    def calculate_calorie_deficit_target(
        weight_kg: float,
        height_cm: int,
        age: int,
        gender: Union[Gender, str] = Gender.MALE,
        activity_level: float = 1.2,
        deficit_per_week_kg: float = 0.5
    ) -> dict:
        """
        计算热量缺口目标

        Args:
            weight_kg: 体重（千克）
            height_cm: 身高（厘米）
            age: 年龄（岁）
            gender: 性别
            activity_level: 活动系数
            deficit_per_week_kg: 每周减重目标（千克）
                1公斤脂肪 ≈ 7700千卡

        Returns:
            dict: {
                'bmr': 基础代谢率,
                'tdee': 每日总消耗,
                'daily_calorie_target': 每日摄入目标,
                'daily_deficit': 每日热量缺口
            }
        """
        tdee = BMRCalculator.calculate_tdee(
            weight_kg, height_cm, age, gender, activity_level
        )

        # 每日热量缺口 = 每周目标缺口 / 7
        weekly_deficit = deficit_per_week_kg * 7700  # 1kg ≈ 7700kcal
        daily_deficit = round(weekly_deficit / 7, 1)

        # 每日摄入目标 = TDEE - 每日缺口
        daily_target = round(tdee - daily_deficit, 1)

        return {
            'bmr': BMRCalculator.calculate_bmr(weight_kg, height_cm, age, gender),
            'tdee': tdee,
            'daily_calorie_target': daily_target,
            'daily_deficit': daily_deficit
        }


def calculate_bmr(
    weight_kg: float,
    height_cm: int,
    age: int,
    gender: Union[Gender, str] = Gender.MALE
) -> float:
    """
    便捷函数：计算基础代谢率

    Args:
        weight_kg: 体重（千克）
        height_cm: 身高（厘米）
        age: 年龄（岁）
        gender: 性别

    Returns:
        float: 基础代谢率（千卡/天）
    """
    return BMRCalculator.calculate_bmr(weight_kg, height_cm, age, gender)
