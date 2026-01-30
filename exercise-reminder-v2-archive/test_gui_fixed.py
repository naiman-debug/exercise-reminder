# -*- coding: utf-8 -*-
"""
GUI 测试脚本 - 修复版
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QWidget, QDialog, QMessageBox,
    QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer
from src.ui.settings.settings_dialog import SettingsDialog
from src.ui.settings.exercise_library import ExerciseLibraryWidget, ExerciseEditDialog
from src.ui.statistics.statistics_widget import StatisticsWidget
from src.core.app import Application


class TestWindow(QMainWindow):
    """测试窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("灵动休息 - GUI 测试")
        self.setGeometry(100, 100, 450, 350)
        self.application = None

        # 创建中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 添加测试按钮
        btn1 = QPushButton("1. 打开设置对话框（完整）")
        btn1.clicked.connect(self._test_settings_dialog)
        layout.addWidget(btn1)

        btn2 = QPushButton("2. 打开动作库管理")
        btn2.clicked.connect(self._test_exercise_library)
        layout.addWidget(btn2)

        btn3 = QPushButton("3. 打开动作编辑对话框")
        btn3.clicked.connect(self._test_exercise_edit)
        layout.addWidget(btn3)

        btn4 = QPushButton("4. 打开统计界面")
        btn4.clicked.connect(self._test_statistics)
        layout.addWidget(btn4)

        btn5 = QPushButton("5. 启动完整应用（系统托盘）")
        btn5.clicked.connect(self._test_full_app)
        layout.addWidget(btn5)

        layout.addStretch()

        # 说明标签
        hint_label = QLabel("提示：点击按钮测试各项功能，或点击'启动完整应用'运行实际程序")
        hint_label.setWordWrap(True)
        hint_label.setStyleSheet("color: #757575; font-size: 10pt; padding: 10px;")
        layout.addWidget(hint_label)

        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #4CAF50; font-size: 11pt; padding: 5px;")
        layout.addWidget(self.status_label)

    def _update_status(self, message: str, success: bool = True):
        """更新状态"""
        color = "#4CAF50" if success else "#F44336"
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 11pt; padding: 5px;")

    def _test_settings_dialog(self):
        """测试设置对话框"""
        self._update_status("打开设置对话框...")
        try:
            dialog = SettingsDialog(self)
            result = dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                self._update_status("设置已保存", True)
            else:
                self._update_status("设置已取消", True)
        except Exception as e:
            self._update_status(f"设置打开失败: {e}", False)

    def _test_exercise_library(self):
        """测试动作库管理"""
        self._update_status("打开动作库管理...")
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("动作库管理测试")
            dialog.setMinimumSize(750, 550)

            layout = QVBoxLayout(dialog)
            widget = ExerciseLibraryWidget()
            layout.addWidget(widget)

            dialog.exec()
            self._update_status("动作库管理已关闭", True)
        except Exception as e:
            self._update_status(f"动作库打开失败: {e}", False)

    def _test_exercise_edit(self):
        """测试动作编辑对话框"""
        self._update_status("打开动作编辑对话框...")
        try:
            dialog = ExerciseEditDialog(parent=self)
            result = dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                self._update_status("动作已保存", True)
            else:
                self._update_status("动作编辑已取消", True)
        except Exception as e:
            self._update_status(f"动作编辑打开失败: {e}", False)

    def _test_statistics(self):
        """测试统计界面"""
        self._update_status("打开统计界面...")
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("统计界面测试")
            dialog.setMinimumSize(950, 750)

            layout = QVBoxLayout(dialog)

            # 添加标题
            title = QLabel("活动统计 - 数据展示")
            title.setStyleSheet("font-size: 14pt; font-weight: bold; padding: 10px;")
            layout.addWidget(title)

            widget = StatisticsWidget()
            layout.addWidget(widget)

            # 关闭按钮
            btn_layout = QHBoxLayout()
            btn_layout.addStretch()

            close_btn = QPushButton("关闭")
            close_btn.setMinimumWidth(100)
            close_btn.clicked.connect(dialog.accept)
            btn_layout.addWidget(close_btn)

            layout.addLayout(btn_layout)

            dialog.exec()
            self._update_status("统计界面已关闭", True)
        except Exception as e:
            self._update_status(f"统计界面打开失败: {e}", False)

    def _test_full_app(self):
        """测试完整应用"""
        self._update_status("准备启动完整应用...")

        reply = QMessageBox.question(
            self,
            "确认启动",
            "这将启动完整的后台应用，包括系统托盘和提醒功能。\n\n"
            "启动后，测试窗口将关闭，应用将在系统托盘中运行。\n\n"
            "是否继续？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._update_status("正在启动完整应用...")

            # 延迟关闭，让用户看到状态更新
            QTimer.singleShot(500, self._launch_full_app)

    def _launch_full_app(self):
        """实际启动完整应用"""
        try:
            # 创建完整应用
            self.application = Application()
            self.application.app_started.connect(self._on_app_started)
            self.application.app_stopped.connect(self._on_app_stopped)

            # 启动应用
            self.application.start()

            # 关闭测试窗口
            self.close()

        except Exception as e:
            self._update_status(f"启动失败: {e}", False)
            QMessageBox.critical(self, "启动失败", f"完整应用启动失败：\n{e}")

    def _on_app_started(self):
        """应用启动回调"""
        # 应用已在后台运行，可以通过系统托盘访问
        pass

    def _on_app_stopped(self):
        """应用停止回调"""
        pass


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
