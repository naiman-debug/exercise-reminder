# -*- coding: utf-8 -*-
"""
体验倒计时页面演示脚本

用于手动测试体验倒计时页面的功能和样式
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from src.ui.wizards.experience_page import ExperiencePage


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle("体验倒计时页面演示")
    window.setMinimumSize(800, 600)

    # 创建中央容器
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    layout.setContentsMargins(0, 0, 0, 0)

    # 创建体验页面
    experience_page = ExperiencePage()

    # 连接信号
    def on_skip():
        print("跳过体验信号触发")
        window.close()

    def on_start():
        print("开始体验信号触发")
        # 这里可以添加弹出站立提醒的逻辑
        window.close()

    experience_page.skip_experience.connect(on_skip)
    experience_page.start_experience.connect(on_start)

    # 添加到布局
    layout.addWidget(experience_page)

    window.setCentralWidget(central_widget)
    window.show()

    print("体验倒计时页面已启动")
    print("- 倒计时将自动开始")
    print("- 点击'跳过体验'将关闭窗口")
    print("- 点击'立即体验'或倒计时结束将触发开始体验信号")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
