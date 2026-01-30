# -*- coding: utf-8 -*-
"""
GUI 测试脚本 - 手动测试界面
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QWidget, QDialog, QMessageBox
)
from src.ui.settings.settings_dialog import SettingsDialog
from src.ui.settings.exercise_library import ExerciseLibraryWidget, ExerciseEditDialog
from src.ui.statistics.statistics_widget import StatisticsWidget
from src.core.app import Application


class TestWindow(QMainWindow):
    """测试窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("灵动休息 - GUI 测试")
        self.setGeometry(100, 100, 400, 300)

        # 创建中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 添加测试按钮
        btn1 = QPushButton("打开设置对话框（完整）")
        btn1.clicked.connect(self._test_settings_dialog)
        layout.addWidget(btn1)

        btn2 = QPushButton("打开动作库管理")
        btn2.clicked.connect(self._test_exercise_library)
        layout.addWidget(btn2)

        btn3 = QPushButton("打开动作编辑对话框")
        btn3.clicked.connect(self._test_exercise_edit)
        layout.addWidget(btn3)

        btn4 = QPushButton("打开统计界面")
        btn4.clicked.connect(self._test_statistics)
        layout.addWidget(btn4)

        btn5 = QPushButton("启动完整应用")
        btn5.clicked.connect(self._test_full_app)
        layout.addWidget(btn5)

        layout.addStretch()

        # 状态标签
        from PySide6.QtWidgets import QLabel
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #757575;")
        layout.addWidget(self.status_label)

    def _test_settings_dialog(self):
        """测试设置对话框"""
        self.status_label.setText("打开设置对话框...")
        dialog = SettingsDialog(self)
        if dialog.exec():
            self.status_label.setText("设置已保存")
        else:
            self.status_label.setText("设置已取消")

    def _test_exercise_library(self):
        """测试动作库管理"""
        self.status_label.setText("打开动作库管理...")
        dialog = QDialog(self)
        dialog.setWindowTitle("动作库管理测试")
        dialog.setMinimumSize(700, 500)

        layout = QVBoxLayout(dialog)
        widget = ExerciseLibraryWidget()
        layout.addWidget(widget)

        dialog.exec()
        self.status_label.setText("动作库管理已关闭")

    def _test_exercise_edit(self):
        """测试动作编辑对话框"""
        self.status_label.setText("打开动作编辑对话框...")
        dialog = ExerciseEditDialog(parent=self)
        if dialog.exec():
            self.status_label.setText("动作已保存")
        else:
            self.status_label.setText("动作编辑已取消")

    def _test_statistics(self):
        """测试统计界面"""
        self.status_label.setText("打开统计界面...")
        dialog = QDialog(self)
        dialog.setWindowTitle("统计界面测试")
        dialog.setMinimumSize(900, 700)

        layout = QVBoxLayout(dialog)
        widget = StatisticsWidget()
        layout.addWidget(widget)

        # 关闭按钮
        from PySide6.QtWidgets import QPushButton, QHBoxLayout
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        close_btn = QPushButton("关闭")
        close_btn.setMinimumWidth(100)
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

        dialog.exec()
        self.status_label.setText("统计界面已关闭")

    def _test_full_app(self):
        """测试完整应用"""
        self.status_label.setText("启动完整应用...")
        reply = QMessageBox.question(
            self,
            "确认",
            "这将启动完整的后台应用，包括系统托盘和提醒功能。\n是否继续？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            # 关闭测试窗口
            self.close()

            # 创建并启动应用
            app = Application()
            app.start()


def main():
    """主函数"""
    # 创建 Qt 应用
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName("灵动休息健康助手")

    # 初始化数据库（确保有数据）
    from src.models.database import get_db_manager
    db_manager = get_db_manager()
    db_manager.initialize_database()
    db_manager.close()

    # 创建测试窗口
    window = TestWindow()
    window.show()

    # 运行事件循环
    exit_code = qt_app.exec()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
