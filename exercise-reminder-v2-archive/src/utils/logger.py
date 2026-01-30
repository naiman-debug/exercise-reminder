# -*- coding: utf-8 -*-
"""
统一日志系统

基于 loguru 提供结构化、可配置的日志功能
"""
import sys
from pathlib import Path
from loguru import logger as _logger


# 日志目录
LOG_DIR = Path(__file__).parent.parent.parent / "data" / "logs"

# 日志文件路径
LOG_FILE = LOG_DIR / "app_{time:YYYY-MM-DD}.log"

# 日志格式
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# 简化的日志格式（用于控制台）
CONSOLE_FORMAT = (
    "<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>"
)

# 存储已配置的 logger 实例
_loggers = {}

__all__ = ['get_logger', 'setup_logger', 'reset_logger', 'LOG_DIR']


def setup_logger(
    console_level: str = "INFO",
    file_level: str = "DEBUG",
    rotation: str = "10 MB",
    retention: str = "30 days",
    compression: str = "zip"
) -> None:
    """
    配置全局日志系统

    Args:
        console_level: 控制台日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        file_level: 文件日志级别
        rotation: 日志轮转大小
        retention: 日志保留时间
        compression: 压缩格式
    """
    # 确保日志目录存在
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # 移除默认处理器
    _logger.remove()

    # 添加控制台处理器（彩色输出）
    _logger.add(
        sys.stderr,
        format=CONSOLE_FORMAT,
        level=console_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )

    # 添加文件处理器（结构化输出）
    _logger.add(
        LOG_FILE,
        format=LOG_FORMAT,
        level=file_level,
        rotation=rotation,
        retention=retention,
        compression=compression,
        encoding="utf-8",
        enqueue=True,  # 异步写入，避免阻塞
        backtrace=True,
        diagnose=True
    )


def get_logger(name: str):
    """
    获取一个命名 logger 实例

    使用单例模式，相同名称返回相同实例

    Args:
        name: logger 名称，建议使用 __name__ 或模块名

    Returns:
        logger 实例
    """
    # 如果是第一次调用，先设置全局配置并确保日志目录存在
    if not _loggers:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        setup_logger()

    # 如果该名称的 logger 已经存在，直接返回
    if name in _loggers:
        return _loggers[name]

    # 创建新的 logger 实例
    # 使用 bind 添加上下文信息
    named_logger = _logger.bind(name=name)

    # 缓存实例
    _loggers[name] = named_logger

    return named_logger


def reset_logger() -> None:
    """重置日志系统（主要用于测试）"""
    global _loggers
    _loggers.clear()
    _logger.remove()


# 自动初始化（可选）
# setup_logger()
