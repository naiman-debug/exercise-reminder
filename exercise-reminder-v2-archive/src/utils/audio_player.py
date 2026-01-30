# -*- coding: utf-8 -*-
"""
音频播放模块

提供音效播放功能
"""
from pathlib import Path
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl
from typing import Dict


class AudioManager:
    """
    音频管理器

    管理音效的加载和播放
    """

    # 音效文件名映射
    SOUND_FILES = {
        "reminder": "reminder.wav",
        "complete": "complete.wav",
        "skip": "skip.wav",
        "tick": "tick.wav",
        "punishment": "punishment.wav",
    }

    def __init__(self, volume: float = 0.7):
        """
        初始化音频管理器

        Args:
            volume: 音量（0.0-1.0）
        """
        self.volume = volume
        self.sounds: Dict[str, QSoundEffect] = {}
        self.enabled = True
        self._load_sounds()

    def _load_sounds(self):
        """加载音效文件"""
        sound_dir = Path("src/resources/sounds")

        # 检查音效目录是否存在
        if not sound_dir.exists():
            # 音效目录不存在，静默处理
            return

        for name, filename in self.SOUND_FILES.items():
            sound_path = sound_dir / filename
            if sound_path.exists():
                try:
                    sound = QSoundEffect()
                    # 使用 QUrl 从本地文件路径
                    sound.setSource(QUrl.fromLocalFile(str(sound_path)))
                    sound.setVolume(self.volume)
                    self.sounds[name] = sound
                except Exception:
                    # 音效加载失败，静默处理
                    pass

    def play(self, sound_name: str) -> bool:
        """
        播放音效

        Args:
            sound_name: 音效名称（reminder/complete/skip/tick/punishment）

        Returns:
            bool: 是否成功播放
        """
        if not self.enabled:
            return False

        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
                return True
            except Exception:
                return False

        return False

    def set_volume(self, volume: float):
        """
        设置音量

        Args:
            volume: 音量（0.0-1.0）
        """
        self.volume = max(0.0, min(1.0, volume))

        # 更新所有音效的音量
        for sound in self.sounds.values():
            sound.setVolume(self.volume)

    def enable(self):
        """启用音频"""
        self.enabled = True

    def disable(self):
        """禁用音频"""
        self.enabled = False

    def is_available(self, sound_name: str) -> bool:
        """
        检查音效是否可用

        Args:
            sound_name: 音效名称

        Returns:
            bool: 是否可用
        """
        return sound_name in self.sounds


class TTSManager:
    """
    文本转语音管理器

    支持本地 TTS (pyttsx3) 和外部 API
    """

    def __init__(self, api_url: str = ""):
        """
        初始化 TTS 管理器

        Args:
            api_url: TTS API 地址
        """
        self.api_url = api_url
        self.enabled = False
        self.use_local_tts = True  # 默认使用本地 TTS
        self._local_tts_engine = None
        self._init_local_tts()

    def _init_local_tts(self):
        """初始化本地 TTS 引擎"""
        try:
            import pyttsx3
            self._local_tts_engine = pyttsx3.init()
            # 设置中文语音（如果可用）
            voices = self._local_tts_engine.getProperty('voices')
            for voice in voices:
                if 'chinese' in voice.name.lower() or 'zh' in voice.languages[0].lower():
                    self._local_tts_engine.setProperty('voice', voice.id)
                    break
            # 设置语速
            self._local_tts_engine.setProperty('rate', 150)
        except ImportError:
            self._local_tts_engine = None
        except Exception:
            self._local_tts_engine = None

    def speak(self, text: str) -> bool:
        """
        播报文本

        Args:
            text: 要播报的文本

        Returns:
            bool: 是否成功
        """
        if not self.enabled:
            return False

        # 优先使用本地 TTS
        if self.use_local_tts and self._local_tts_engine:
            try:
                self._local_tts_engine.say(text)
                self._local_tts_engine.runAndWait()
                return True
            except Exception:
                return False

        # 使用外部 API
        if self.api_url:
            return self._speak_with_api(text)

        return False

    def _speak_with_api(self, text: str) -> bool:
        """
        使用外部 API 播报

        Args:
            text: 要播报的文本

        Returns:
            bool: 是否成功
        """
        import requests

        try:
            # 通用 TTS API 调用格式
            response = requests.post(
                self.api_url,
                json={"text": text},
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False

    def countdown(self, seconds: int = 5) -> None:
        """
        倒计时播报

        Args:
            seconds: 倒计时秒数
        """
        if not self.enabled:
            return

        for i in range(seconds, 0, -1):
            self.speak(str(i))

    def set_api_url(self, api_url: str):
        """
        设置 TTS API 地址

        Args:
            api_url: API 地址
        """
        self.api_url = api_url
        if api_url:
            self.enabled = True

    def enable(self):
        """启用 TTS"""
        if self._local_tts_engine or self.api_url:
            self.enabled = True

    def disable(self):
        """禁用 TTS"""
        self.enabled = False

    def is_available(self) -> bool:
        """
        检查 TTS 是否可用

        Returns:
            bool: 是否可用
        """
        return self._local_tts_engine is not None or bool(self.api_url)

    def set_local_tts_mode(self, use_local: bool):
        """
        设置使用本地 TTS 模式

        Args:
            use_local: 是否使用本地 TTS
        """
        self.use_local_tts = use_local
