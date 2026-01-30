# -*- coding: utf-8 -*-
"""
主窗口测试启动脚本

用于测试和验证主窗口的所有功能
"""
import sys
from PySide6.QtWidgets import QApplication
from src.utils.logger import get_logger, setup_logger
from src.ui.main_window import MainWindow

# 设置日志
setup_logger()
logger = get_logger(__name__)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("启动主窗口测试")
    logger.info("=" * 60)

    # 创建应用
    app = QApplication(sys.argv)

    # 创建主窗口
    logger.info("创建主窗口...")
    main_window = MainWindow()

    # 显示窗口
    logger.info("显示主窗口...")
    main_window.show()

    logger.info("主窗口已显示，可以开始测试")
    logger.info("快速操作按钮:")
    logger.info("  - 🏋️ 动作库")
    logger.info("  - ⚙️ 参数设置")
    logger.info("  - 👤 用户信息")
    logger.info("  - 🔧 基础设置")
    logger.info("")
    logger.info("数据刷新: 每 30 秒自动刷新一次")

    # 运行应用
    result = app.exec()

    logger.info(f"应用退出，结果码: {result}")
    return result


if __name__ == "__main__":
    main()
