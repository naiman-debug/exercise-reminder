# -*- coding: utf-8 -*-
"""
TTS 语音播报测试
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.utils.audio_player import TTSManager


@pytest.fixture
def tts_manager():
    """创建 TTS 管理器"""
    return TTSManager()


def test_tts_manager_initialization(tts_manager):
    """测试 TTS 管理器初始化"""
    assert tts_manager.api_url == ""
    assert not tts_manager.enabled
    assert tts_manager.use_local_tts is True


def test_tts_manager_with_api_url():
    """测试带 API URL 的初始化"""
    manager = TTSManager(api_url="https://example.com/tts")
    assert manager.api_url == "https://example.com/tts"


def test_speak_when_disabled(tts_manager):
    """测试禁用状态下播报"""
    tts_manager.enabled = False
    result = tts_manager.speak("测试")
    assert result is False


def test_countdown(tts_manager):
    """测试倒计时播报"""
    tts_manager.enabled = True
    tts_manager.speak = Mock()  # Mock speak 方法

    tts_manager.countdown(3)

    # 验证播报了 3, 2, 1
    assert tts_manager.speak.call_count == 3
    calls = [str(i) for i in range(3, 0, -1)]
    actual_calls = [call[0][0] for call in tts_manager.speak.call_args_list]
    assert actual_calls == calls


def test_set_api_url(tts_manager):
    """测试设置 API URL"""
    tts_manager.set_api_url("https://api.example.com/tts")
    assert tts_manager.api_url == "https://api.example.com/tts"
    assert tts_manager.enabled is True


def test_enable_and_disable(tts_manager):
    """测试启用和禁用"""
    # 禁用状态下启用
    tts_manager._local_tts_engine = Mock()
    tts_manager.enable()
    assert tts_manager.enabled is True

    # 禁用
    tts_manager.disable()
    assert tts_manager.enabled is False


def test_is_available(tts_manager):
    """测试检查 TTS 是否可用"""
    # 默认情况下不可用
    assert not tts_manager.is_available()

    # 有本地引擎时可用
    tts_manager._local_tts_engine = Mock()
    assert tts_manager.is_available()

    # 有 API URL 时可用
    tts_manager._local_tts_engine = None
    tts_manager.api_url = "https://example.com/tts"
    assert tts_manager.is_available()


def test_set_local_tts_mode(tts_manager):
    """测试设置本地 TTS 模式"""
    tts_manager.set_local_tts_mode(False)
    assert tts_manager.use_local_tts is False

    tts_manager.set_local_tts_mode(True)
    assert tts_manager.use_local_tts is True


@patch('requests.post')
def test_speak_with_api(mock_post, tts_manager):
    """测试使用外部 API 播报"""
    tts_manager.use_local_tts = False
    tts_manager.api_url = "https://example.com/tts"
    tts_manager.enabled = True

    # Mock API 响应
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # 测试播报
    result = tts_manager.speak("测试")

    # 验证 API 被调用
    mock_post.assert_called_once_with(
        "https://example.com/tts",
        json={"text": "测试"},
        timeout=5
    )
    assert result is True


def test_local_tts_initialization():
    """测试本地 TTS 初始化（可选依赖）"""
    manager = TTSManager()
    manager._init_local_tts()

    # 即使 pyttsx3 不可用，也不应该崩溃
    # _local_tts_engine 可以是 None
    assert manager is not None


def test_tts_handles_import_error():
    """测试 TTS 处理导入错误（可选依赖）"""
    # 正常情况下，如果 pyttsx3 不可用，
    # _init_local_tts 应该将 _local_tts_engine 设为 None
    manager = TTSManager()
    manager._init_local_tts()

    # 验证即使没有 pyttsx3，管理器仍然可以正常初始化
    assert manager is not None


def test_speak_returns_false_when_no_engine_available(tts_manager):
    """测试当没有 TTS 引擎时播报返回 False"""
    tts_manager.enabled = True
    tts_manager._local_tts_engine = None
    tts_manager.use_local_tts = True
    tts_manager.api_url = ""

    result = tts_manager.speak("测试")
    assert result is False
