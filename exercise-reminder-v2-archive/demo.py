# -*- coding: utf-8 -*-
"""
应用演示脚本

快速启动应用并触发各种提醒用于测试和演示
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from src.core.app import create_application
from src.ui.dialogs.stand_dialog import StandReminderDialog
from src.ui.dialogs.exercise_dialog import ExerciseReminderDialog
from src.ui.dialogs.gaze_dialog import GazeReminderDialog
from src.models.repositories import ExerciseRepository


def demo_main_app():
    """演示主应用（带系统托盘和随机提醒）"""
    from PySide6.QtWidgets import QApplication
    from src.core.app import create_application

    qt_app = get_or_create_qt_app()
    qt_app.setApplicationName("灵动休息健康助手")

    app = create_application()
    app.start()

    # 显示欢迎信息
    QMessageBox.information(
        None,
        "灵动休息健康助手",
        "应用已启动！\n\n"
        "系统托盘图标已显示，点击可查看菜单。\n"
        "提醒将在设定时间后自动触发。\n\n"
        "如需测试特定弹窗，请使用 demo.py 的其他选项。"
    )

    qt_app.exec()
    app.stop()


def get_or_create_qt_app():
    """获取或创建 QApplication 实例"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


def demo_stand_dialog():
    """演示强制站立弹窗"""
    qt_app = get_or_create_qt_app()

    dialog = StandReminderDialog(duration=10)  # 10秒演示
    dialog.setWindowTitle("演示 - 强制站立提醒")
    dialog.exec()

    QMessageBox.information(
        None,
        "演示完成",
        "强制站立提醒演示结束。\n\n"
        "特点：\n"
        "- 不可跳过，不可关闭\n"
        "- 倒计时颜色随时间变化\n"
        "- 完成后显示✓反馈"
    )


def demo_exercise_dialog():
    """演示微运动弹窗"""
    qt_app = get_or_create_qt_app()

    # 初始化数据库
    from src.models.database import get_db_manager
    get_db_manager().initialize_database()

    # 获取示例动作
    exercises = ExerciseRepository.get_random_exercises(count=1)

    if not exercises:
        QMessageBox.critical(None, "错误", "未找到运动动作，请先初始化数据库")
        return

    # 转换为对话框需要的格式
    exercises_data = [
        {
            "id": ex.id,
            "name": ex.name,
            "duration": ex.duration_seconds,
            "met": ex.met_value
        }
        for ex in exercises
    ]

    dialog = ExerciseReminderDialog(exercises_data, weight_kg=70)
    dialog.setWindowTitle("演示 - 微运动提醒")
    dialog.exec()

    QMessageBox.information(
        None,
        "演示完成",
        "微运动提醒演示结束。\n\n"
        "特点：\n"
        "- 显示动作名称和倒计时\n"
        "- 可点击「完成」、「跳过」或「换一个」\n"
        "- 显示 MET 值和热量消耗\n"
        "- 连续跳过可触发惩罚模式"
    )


def demo_gaze_dialog():
    """演示强制远眺弹窗"""
    qt_app = get_or_create_qt_app()

    dialog = GazeReminderDialog(duration=10)  # 10秒演示
    dialog.setWindowTitle("演示 - 强制远眺提醒")
    dialog.exec()

    QMessageBox.information(
        None,
        "演示完成",
        "强制远眺提醒演示结束。\n\n"
        "特点：\n"
        "- 不可跳过，不可关闭\n"
        "- 浅蓝色背景，护眼主题\n"
        "- 引导用户眺望远方"
    )


def demo_punishment_mode():
    """演示惩罚模式"""
    qt_app = get_or_create_qt_app()

    # 初始化数据库
    from src.models.database import get_db_manager
    get_db_manager().initialize_database()

    # 先记录跳过以触发惩罚
    from src.models.repositories import PunishmentRepository
    PunishmentRepository.record_skip()
    PunishmentRepository.record_skip()

    # 获取示例动作
    exercises = ExerciseRepository.get_random_exercises(count=1)

    if not exercises:
        QMessageBox.critical(None, "错误", "未找到运动动作，请先初始化数据库")
        return

    # 转换为对话框需要的格式
    exercises_data = [
        {
            "id": ex.id,
            "name": ex.name,
            "duration": ex.duration_seconds,
            "met": ex.met_value
        }
        for ex in exercises
    ]

    dialog = ExerciseReminderDialog(exercises_data, weight_kg=70)
    dialog.setWindowTitle("演示 - 惩罚模式")
    dialog.set_punishment_mode(True)
    dialog.exec()

    # 清理惩罚状态
    from src.models.repositories import PunishmentRepository
    PunishmentRepository.clear_skip_count()

    QMessageBox.information(
        None,
        "演示完成",
        "惩罚模式演示结束。\n\n"
        "特点：\n"
        "- 窗口尺寸变大（全屏 80%）\n"
        "- 强制置顶，无法切换\n"
        "- 禁用「跳过」和「换一个」按钮\n"
        "- 必须完成或等待倒计时结束"
    )


def demo_all_dialogs():
    """演示所有弹窗（依次显示）"""
    qt_app = get_or_create_qt_app()

    # 初始化数据库
    from src.models.database import get_db_manager
    get_db_manager().initialize_database()

    def show_next(index):
        if index >= 3:
            QMessageBox.information(
                None,
                "演示完成",
                "所有弹窗演示结束！"
            )
            return

        if index == 0:
            dialog = StandReminderDialog(duration=5)
            dialog.setWindowTitle("演示 1/3 - 强制站立")
        elif index == 1:
            exercises = ExerciseRepository.get_random_exercises(count=1)
            if not exercises:
                show_next(2)
                return
            # 转换为对话框需要的格式
            exercises_data = [
                {
                    "id": ex.id,
                    "name": ex.name,
                    "duration": ex.duration_seconds,
                    "met": ex.met_value
                }
                for ex in exercises
            ]
            dialog = ExerciseReminderDialog(exercises_data, weight_kg=70)
            dialog.setWindowTitle("演示 2/3 - 微运动")
        else:
            dialog = GazeReminderDialog(duration=5)
            dialog.setWindowTitle("演示 3/3 - 强制远眺")

        dialog.finished.connect(lambda: show_next(index + 1))
        dialog.exec()

    show_next(0)


def main():
    """主菜单"""
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox

    qt_app = get_or_create_qt_app()
    qt_app.setStyle("Fusion")

    window = QWidget()
    window.setWindowTitle("灵动休息健康助手 - 演示菜单")
    window.setMinimumSize(500, 600)

    layout = QVBoxLayout(window)
    layout.setSpacing(20)
    layout.setContentsMargins(40, 40, 40, 40)

    # 标题
    title = QLabel("灵动休息健康助手")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setFont(QFont("Microsoft YaHei UI", 24, QFont.Weight.Bold))
    layout.addWidget(title)

    subtitle = QLabel("演示和测试菜单")
    subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
    subtitle.setFont(QFont("Microsoft YaHei UI", 14))
    subtitle.setStyleSheet("color: #757575;")
    layout.addWidget(subtitle)

    layout.addSpacing(20)

    # 主应用
    main_group = QGroupBox("主应用")
    main_layout = QVBoxLayout()
    main_btn = QPushButton("启动完整应用（系统托盘 + 随机提醒）")
    main_btn.setMinimumHeight(50)
    main_btn.clicked.connect(demo_main_app)
    main_btn.setStyleSheet("""
        QPushButton {
            background-color: #4CAF50;
            color: white;
            font-size: 14pt;
            border-radius: 8px;
            padding: 12px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """)
    main_layout.addWidget(main_btn)
    main_group.setLayout(main_layout)
    layout.addWidget(main_group)

    # 单独弹窗演示
    dialog_group = QGroupBox("单独弹窗演示")
    dialog_layout = QVBoxLayout()

    stand_btn = QPushButton("强制站立提醒")
    stand_btn.setMinimumHeight(40)
    stand_btn.clicked.connect(demo_stand_dialog)
    dialog_layout.addWidget(stand_btn)

    exercise_btn = QPushButton("微运动提醒")
    exercise_btn.setMinimumHeight(40)
    exercise_btn.clicked.connect(demo_exercise_dialog)
    dialog_layout.addWidget(exercise_btn)

    gaze_btn = QPushButton("强制远眺提醒")
    gaze_btn.setMinimumHeight(40)
    gaze_btn.clicked.connect(demo_gaze_dialog)
    dialog_layout.addWidget(gaze_btn)

    punishment_btn = QPushButton("惩罚模式")
    punishment_btn.setMinimumHeight(40)
    punishment_btn.clicked.connect(demo_punishment_mode)
    punishment_btn.setStyleSheet("""
        QPushButton {
            background-color: #FF9800;
            color: white;
            font-size: 12pt;
            border-radius: 6px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #F57C00;
        }
    """)
    dialog_layout.addWidget(punishment_btn)

    dialog_group.setLayout(dialog_layout)
    layout.addWidget(dialog_group)

    # 全部演示
    all_btn = QPushButton("依次演示所有弹窗")
    all_btn.setMinimumHeight(50)
    all_btn.clicked.connect(demo_all_dialogs)
    all_btn.setStyleSheet("""
        QPushButton {
            background-color: #2196F3;
            color: white;
            font-size: 14pt;
            border-radius: 8px;
            padding: 12px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
    """)
    layout.addWidget(all_btn)

    layout.addStretch()

    window.show()
    qt_app.exec()


if __name__ == '__main__':
    main()
