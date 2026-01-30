# -*- coding: utf-8 -*-
"""
快速测试脚本 - 立即触发所有提醒

使用呼吸感设计风格
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import QTimer, Qt
from src.core.app import create_application
from src.ui.design.tokens import DesignTokens


def main():
    """主函数"""
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName("灵动休息健康助手 - 测试")

    # 创建业务应用
    app = create_application()

    # 创建测试窗口 - 使用呼吸感设计
    test_window = QWidget()
    test_window.setWindowTitle("测试窗口")
    test_window.setMinimumSize(500, 450)

    # 应用全局样式
    DesignTokens.apply_stylesheet(test_window, "all")

    layout = QVBoxLayout(test_window)
    layout.setContentsMargins(DesignTokens.SPACING.XL, DesignTokens.SPACING.XL,
                              DesignTokens.SPACING.XL, DesignTokens.SPACING.XL)
    layout.setSpacing(DesignTokens.SPACING.LG)

    # 标题
    title_label = QLabel("💪 灵动休息健康助手")
    title_label.setStyleSheet(f"""
        font-size: {DesignTokens.TYPOGRAPHY.TEXT_2XL}pt;
        font-weight: 700;
        color: {DesignTokens.COLOR.TEXT_PRIMARY};
        padding: {DesignTokens.SPACING.MD}px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {DesignTokens.COLOR.PRIMARY_LIGHT},
            stop:1 {DesignTokens.COLOR.PRIMARY_SOLID});
        border-radius: {DesignTokens.RADIUS.LG}px;
        color: white;
    """)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title_label)

    # 添加说明
    info_label = QLabel("点击下方按钮测试不同提醒功能：")
    info_label.setStyleSheet(f"""
        font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
        color: {DesignTokens.COLOR.TEXT_SECONDARY};
        padding: {DesignTokens.SPACING.SM}px;
    """)
    info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    info_label.setWordWrap(True)
    layout.addWidget(info_label)

    layout.addSpacing(DesignTokens.SPACING.LG)

    # 创建按钮样式
    button_style = f"""
        QPushButton {{
            background-color: {DesignTokens.COLOR.PRIMARY_SOLID};
            color: white;
            border: none;
            border-radius: {DesignTokens.RADIUS.MD}px;
            padding: {DesignTokens.SPACING.MD}px;
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_LG}pt;
            font-weight: 600;
            min-height: 55px;
        }}
        QPushButton:hover {{
            background-color: {DesignTokens.COLOR.PRIMARY_DARK};
        }}
        QPushButton:pressed {{
            background-color: {DesignTokens.COLOR.PRIMARY_DARK};
        }}
    """

    # 站立提醒测试按钮
    stand_btn = QPushButton("🧍 测试强制站立提醒")
    stand_btn.setStyleSheet(button_style)
    stand_btn.clicked.connect(lambda: app._show_stand_reminder(10))
    layout.addWidget(stand_btn)

    # 运动提醒测试按钮
    exercise_btn = QPushButton("🏃 测试微运动提醒")
    exercise_btn.setStyleSheet(button_style)
    exercise_btn.clicked.connect(lambda: test_exercise(app))
    layout.addWidget(exercise_btn)

    # 远眺提醒测试按钮
    gaze_btn = QPushButton("👀 测试强制远眺提醒")
    gaze_btn.setStyleSheet(button_style)
    gaze_btn.clicked.connect(lambda: app._show_gaze_reminder(10))
    layout.addWidget(gaze_btn)

    # 设置按钮
    settings_btn = QPushButton("⚙️ 打开设置")
    settings_btn.setStyleSheet(button_style)
    settings_btn.clicked.connect(app._show_settings)
    layout.addWidget(settings_btn)

    layout.addStretch()

    # 底部说明
    footer_label = QLabel("所有按钮已启用呼吸感设计风格 ✨")
    footer_label.setStyleSheet(f"""
        font-size: {DesignTokens.TYPOGRAPHY.TEXT_SM}pt;
        color: {DesignTokens.COLOR.TEXT_TERTIARY};
        padding: {DesignTokens.SPACING.SM}px;
    """)
    footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(footer_label)

    test_window.show()

    # 启动应用（但不启动定时器，因为我们在测试）
    # app.reminder_engine.start_all()  # 注释掉自动启动

    print("=" * 50)
    print("测试模式已启动")
    print("=" * 50)
    print(f"系统托盘可用: {app.tray_icon is not None}")
    print(f"活跃提醒数: {len(app.reminder_engine.get_active_reminders())}")
    print("=" * 50)
    print("\n点击测试窗口中的按钮来测试各种提醒功能\n")

    qt_app.exec()
    app.stop()


def test_exercise(app):
    """测试运动提醒"""
    from src.models.repositories import ExerciseRepository
    exercises = ExerciseRepository.get_random_exercises(1)
    exercise_list = [
        {"id": ex.id, "name": ex.name, "duration": ex.duration_seconds, "met": ex.met_value}
        for ex in exercises
    ]
    app._show_exercise_reminder(exercise_list)


if __name__ == '__main__':
    main()
