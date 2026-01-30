# -*- coding: utf-8 -*-
"""
"灵动休息"健康助手 - 主程序入口

一个 Windows 桌面健康提醒应用，通过随机间隔的强制提醒，
帮助用户定时中断久坐，执行站姿微运动与远眺。
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.core.app import create_application
from src.utils import get_logger

# 获取主程序 logger
logger = get_logger(__name__)


def main():
    """主函数"""
    try:
        # 记录应用启动
        logger.info("=" * 60)
        logger.info("灵动休息健康助手启动中...")
        logger.info("=" * 60)

        # 启用高 DPI 缩放
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        logger.debug("高 DPI 缩放已启用")

        # 创建 Qt 应用
        qt_app = QApplication(sys.argv)
        qt_app.setApplicationName("灵动休息健康助手")
        qt_app.setOrganizationName("灵动健康")
        logger.info("Qt 应用实例已创建")

        # 创建业务应用实例
        app = create_application()
        logger.info("业务应用实例已创建")

        # 启动应用
        logger.info("正在启动应用...")
        app.start()
        logger.info("应用已成功启动")

        # 运行事件循环
        logger.info("进入事件循环...")
        exit_code = qt_app.exec()

        # 清理资源
        logger.info(f"应用退出，退出码: {exit_code}")
        app.stop()
        logger.info("资源已清理")

        logger.info("=" * 60)
        logger.info("灵动休息健康助手已退出")
        logger.info("=" * 60)

        sys.exit(exit_code)

    except Exception as e:
        logger.exception(f"应用崩溃: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
