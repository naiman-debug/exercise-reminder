# -*- coding: utf-8 -*-
"""
配置管理模块

管理应用的配置设置
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """
    配置管理器

    从 JSON 文件加载和保存配置
    """

    # 默认配置
    DEFAULT_CONFIG = {
        "reminder": {
            "global_offset_minutes": 15,
            "stand": {
                "enabled": True,
                "interval_avg": 45,
                "duration": 90
            },
            "exercise": {
                "enabled": True,
                "interval_avg": 60,
                "duration": 120
            },
            "gaze": {
                "enabled": True,
                "interval_avg": 75,
                "duration": 60
            }
        },
        "user": {
            "height": 170,
            "weight": 70.0,
            "age": 30,
            "gender": "male",
            "calorie_target": 500,
            "bmr": 1650
        },
        "audio": {
            "enabled": True,
            "volume": 0.7,
            "sound_effect": "electronic_beep",
            "sound_file": "",
            "tts_enabled": False,
            "tts_api": ""
        },
        "system": {
            "autostart": False,
            "minimize_to_tray": True,
            "show_startup_notification": True
        },
        "ui": {
            "window_position": "center",
            "window_opacity": 1.0
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径（默认为 data/config.json）
        """
        if config_path is None:
            config_path = "data/config.json"

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.migrate_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置

        Returns:
            dict: 配置字典
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # 合并默认配置（防止缺少键）
                return self._merge_config(self.DEFAULT_CONFIG, loaded_config)
            except (json.JSONDecodeError, IOError):
                pass

        return self.DEFAULT_CONFIG.copy()

    def _merge_config(self, base: Dict, override: Dict) -> Dict:
        """
        递归合并配置

        Args:
            base: 基础配置
            override: 覆盖配置

        Returns:
            dict: 合并后的配置
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value

        return result

    def migrate_config(self) -> bool:
        """
        迁移旧配置到新结构

        Returns:
            bool: 是否执行了迁移
        """
        if self.get("reminder.stand.interval_min") is not None:
            old_stand_min = self.get("reminder.stand.interval_min", 30)
            old_stand_max = self.get("reminder.stand.interval_max", 60)
            new_stand_avg = (old_stand_min + old_stand_max) // 2

            self.set("reminder.global_offset_minutes", (old_stand_max - old_stand_min) // 2, save=False)
            self.set("reminder.stand.interval_avg", new_stand_avg, save=False)
            self.set("reminder.exercise.interval_avg",
                     (self.get("reminder.exercise.interval_min", 45) +
                      self.get("reminder.exercise.interval_max", 75)) // 2, save=False)
            self.set("reminder.gaze.interval_avg",
                     (self.get("reminder.gaze.interval_min", 60) +
                      self.get("reminder.gaze.interval_max", 90)) // 2, save=False)

            # 删除旧键
            for reminder in ["stand", "exercise", "gaze"]:
                self.config.get("reminder", {}).get(reminder, {}).pop("interval_min", None)
                self.config.get("reminder", {}).get(reminder, {}).pop("interval_max", None)

            self.save()
            return True
        return False

    def save(self):
        """保存配置到文件"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        支持点号分隔的嵌套键，如 "reminder.stand.enabled"

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值

        示例：
            >>> config.get("reminder.stand.enabled")
            True
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any, save: bool = True):
        """
        设置配置值

        支持点号分隔的嵌套键，如 "reminder.stand.enabled"

        Args:
            key: 配置键
            value: 配置值
            save: 是否立即保存到文件
        """
        keys = key.split('.')
        config = self.config

        # 导航到最后一级的父级
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # 设置值
        config[keys[-1]] = value

        if save:
            self.save()

    def get_reminder_config(self, reminder_type: str) -> Dict[str, Any]:
        """
        获取特定提醒类型的配置

        Args:
            reminder_type: 提醒类型（stand/exercise/gaze）

        Returns:
            dict: 提醒配置
        """
        return self.get(f"reminder.{reminder_type}", {})

    def is_reminder_enabled(self, reminder_type: str) -> bool:
        """
        检查提醒是否启用

        Args:
            reminder_type: 提醒类型（stand/exercise/gaze）

        Returns:
            bool: 是否启用
        """
        return self.get(f"reminder.{reminder_type}.enabled", False)

    def get_interval_range(self, reminder_type: str) -> tuple:
        """
        获取提醒间隔范围

        基于平均间隔和全局偏移量计算最小值和最大值

        Args:
            reminder_type: 提醒类型（stand/exercise/gaze）

        Returns:
            tuple: (min_minutes, max_minutes)
        """
        avg = self.get(f"reminder.{reminder_type}.interval_avg", 45)
        offset = self.get("reminder.global_offset_minutes", 15)
        min_val = max(5, avg - offset)
        max_val = avg + offset
        return (min_val, max_val)

    def get_user_weight(self) -> float:
        """
        获取用户体重

        Returns:
            float: 体重（千克）
        """
        return self.get("user.weight_kg", 70.0)

    def set_user_weight(self, weight_kg: float, save: bool = True):
        """
        设置用户体重

        Args:
            weight_kg: 体重（千克）
            save: 是否立即保存
        """
        self.set("user.weight_kg", weight_kg, save)

    def get_audio_volume(self) -> float:
        """
        获取音量

        Returns:
            float: 音量（0.0-1.0）
        """
        return self.get("audio.volume", 0.7)

    def is_audio_enabled(self) -> bool:
        """
        检查音频是否启用

        Returns:
            bool: 是否启用
        """
        return self.get("audio.enabled", True)

    def is_tts_enabled(self) -> bool:
        """
        检查 TTS 是否启用

        Returns:
            bool: 是否启用
        """
        return self.get("audio.tts_enabled", False)

    def reset_to_default(self):
        """重置为默认配置"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()

    def reload(self):
        """重新加载配置"""
        self.config = self._load_config()
