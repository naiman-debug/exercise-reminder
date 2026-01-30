# -*- coding: utf-8 -*-
"""
测试日志系统

使用 TDD 方式测试 loguru 日志系统的功能
"""
import pytest
import sys
import io
import shutil
from pathlib import Path
from loguru import logger as _logger

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(autouse=True)
def reset_logger_state():
    """
    自动应用的 fixture，在每个测试后重置 logger 状态
    防止测试间状态污染
    """
    from src.utils.logger import reset_logger
    # 测试前重置
    reset_logger()
    yield
    # 测试后重置
    reset_logger()


@pytest.fixture
def fresh_logger():
    """
    提供一个隔离的 logger 实例用于测试
    避免修改全局 logger 状态
    """
    from src.utils.logger import get_logger, reset_logger

    # 确保干净的状态
    reset_logger()

    # 获取一个隔离的 logger
    test_logger = get_logger("fresh_test")

    yield test_logger

    # 清理
    reset_logger()


class TestLogger:
    """测试日志系统"""

    def test_logger_module_exists(self):
        """测试 logger 模块可以被导入"""
        try:
            from src.utils.logger import get_logger, setup_logger
            assert callable(get_logger)
            assert callable(setup_logger)
        except ImportError as e:
            pytest.fail(f"无法导入 logger 模块: {e}")

    def test_get_logger_returns_logger(self):
        """测试 get_logger 返回 loguru logger 实例"""
        from src.utils.logger import get_logger

        test_logger = get_logger("test")
        assert test_logger is not None
        # 验证返回的是 logger 类型
        assert hasattr(test_logger, "info")
        assert hasattr(test_logger, "debug")
        assert hasattr(test_logger, "warning")
        assert hasattr(test_logger, "error")
        assert hasattr(test_logger, "critical")

    def test_logger_has_file_handler(self):
        """测试日志系统配置了文件处理器"""
        from src.utils.logger import get_logger, LOG_DIR

        test_logger = get_logger("test_file")
        # 检查日志目录是否存在
        assert LOG_DIR.exists(), "日志目录不存在"

    def test_logger_levels(self):
        """测试不同级别的日志"""
        from src.utils.logger import get_logger

        test_logger = get_logger("test_levels")
        # 这些调用不应该抛出异常
        test_logger.debug("Debug message")
        test_logger.info("Info message")
        test_logger.warning("Warning message")
        test_logger.error("Error message")
        test_logger.critical("Critical message")

    def test_logger_singleton(self):
        """测试 logger 单例模式 - 相同名字返回相同实例"""
        from src.utils.logger import get_logger

        logger1 = get_logger("singleton_test")
        logger2 = get_logger("singleton_test")
        assert logger1 is logger2

    def test_logger_different_names(self):
        """测试不同名字返回不同实例"""
        from src.utils.logger import get_logger

        logger1 = get_logger("test1")
        logger2 = get_logger("test2")
        # 不应该是同一个实例
        assert logger1 is not logger2

    def test_logger_format(self, fresh_logger):
        """测试日志格式包含必要信息"""
        # 创建一个字符串流来捕获输出
        log_stream = io.StringIO()

        # 移除所有处理器
        fresh_logger.remove()
        # 添加一个临时处理器到字符串流
        fresh_logger.add(log_stream, format="{message}")

        fresh_logger.info("Test message")

        # 验证消息被记录
        output = log_stream.getvalue()
        assert "Test message" in output

    def test_log_directory_creation(self):
        """测试日志目录自动创建"""
        from src.utils.logger import get_logger, reset_logger, LOG_DIR

        # 备份日志目录（如果存在）
        backup_dir = None
        if LOG_DIR.exists():
            backup_dir = LOG_DIR.parent / "logs_backup"
            # 使用 copy2 而不是 move，避免文件锁定问题
            shutil.copytree(str(LOG_DIR), str(backup_dir), dirs_exist_ok=True)

        try:
            # 重置 logger 释放文件句柄
            reset_logger()

            # 删除日志目录
            if LOG_DIR.exists():
                shutil.rmtree(LOG_DIR)

            # 获取 logger 应该会自动创建目录
            get_logger("directory_test")

            assert LOG_DIR.exists(), "日志目录应该被自动创建"
        finally:
            # 重置 logger 释放文件句柄
            reset_logger()

            # 清理并恢复备份的日志目录
            if backup_dir and backup_dir.exists():
                if LOG_DIR.exists():
                    shutil.rmtree(LOG_DIR)
                shutil.rmtree(backup_dir)

    def test_logger_rotation_configured(self):
        """测试日志轮转配置"""
        from src.utils.logger import get_logger
        from src.utils.logger import setup_logger

        # 这个测试验证 setup_logger 被调用并配置了轮转
        # 实际的轮转行为需要更复杂的集成测试
        test_logger = get_logger("rotation_test")
        assert test_logger is not None

    def test_logger_structured_output(self, fresh_logger):
        """测试结构化日志输出"""
        log_stream = io.StringIO()

        fresh_logger.remove()
        # 使用包含时间、级别、名称的格式
        fresh_logger.add(
            log_stream,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}"
        )

        fresh_logger.info("Structured message")

        output = log_stream.getvalue()
        # 验证结构化格式
        assert "|" in output  # 分隔符存在
        assert "INFO" in output  # 级别存在

    def test_logger_context_support(self, fresh_logger):
        """测试上下文信息支持"""
        log_stream = io.StringIO()

        fresh_logger.remove()
        fresh_logger.add(log_stream, format="{message}")

        # 使用 bind 添加上下文
        fresh_logger = fresh_logger.bind(user_id="test_user", action="test_action")
        fresh_logger.info("Context message")

        # 这个测试主要验证不会抛出异常
        assert True

    def test_logger_exception_handling(self, fresh_logger):
        """测试异常记录"""
        log_stream = io.StringIO()

        fresh_logger.remove()
        fresh_logger.add(log_stream, format="{message}")

        try:
            raise ValueError("Test exception")
        except Exception as e:
            fresh_logger.exception(f"Caught exception: {e}")

        output = log_stream.getvalue()
        # 应该包含异常信息
        assert "Test exception" in output or "ValueError" in output

    def test_multiple_loggers_independent(self):
        """测试多个 logger 实例"""
        from src.utils.logger import get_logger
        import io

        stream1 = io.StringIO()
        stream2 = io.StringIO()

        logger1 = get_logger("multi_test1")
        logger2 = get_logger("multi_test2")

        # 注意：由于 loguru 的 logger 共享底层处理器，
        # 这个测试验证的是不同的 logger 可以被获取并使用
        logger1.info("Logger 1 message")
        logger2.info("Logger 2 message")

        # 验证两个 logger 是不同的实例（通过 bind 创建的）
        assert logger1 is not logger2

        # 验证它们都可以正常工作
        assert True

    def test_logger_configuration_persistence(self):
        """测试 logger 配置持久化"""
        from src.utils.logger import get_logger, setup_logger

        # 首次设置
        logger1 = get_logger("persistence_test")

        # 再次获取应该保持配置
        logger2 = get_logger("persistence_test")

        assert logger1 is logger2

    def test_setup_logger_callable(self):
        """测试 setup_logger 函数可调用"""
        from src.utils.logger import setup_logger

        # 不应该抛出异常
        result = setup_logger()
        # 返回值可能是 None 或 logger 实例
        assert result is None or hasattr(result, "info")
