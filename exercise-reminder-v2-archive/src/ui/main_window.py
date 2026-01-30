# -*- coding: utf-8 -*-
"""
主窗口 - 灵动休息健康助手

呼吸感设计 - 柔和有机主义风格
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QScrollArea
)
from PySide6.QtCore import Qt, QTimer
from .design.tokens import DesignTokens
from ..utils.logger import get_logger

logger = get_logger("main_window")


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("初始化主窗口")

        # 窗口设置
        self.setWindowTitle("🏠 灵动休息健康助手")
        self.resize(900, 550)
        self.setMinimumSize(900, 550)

        # 刷新定时器（30秒）
        self.refresh_interval = 30000
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_data)

        # 应用设计系统样式
        DesignTokens.apply_stylesheet(self, "all")

        # UI 组件引用
        self.goal_progress_widget = None
        self.activity_list_widget = None
        self.quick_actions_widget = None
        self.action_library_button = None
        self.settings_button = None
        self.user_info_button = None
        self.basic_settings_button = None

        # 数据显示组件引用
        self.progress_label = None
        self.progress_bar_fill = None
        self.streak_label = None
        self.activity_list_container = None
        self.empty_label = None

        self.setup_ui()
        self.refresh_data()  # 初始加载数据
        self.refresh_timer.start(self.refresh_interval)

    def setup_ui(self):
        """设置 UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(
            DesignTokens.SPACING.LG,
            DesignTokens.SPACING.LG,
            DesignTokens.SPACING.LG,
            DesignTokens.SPACING.LG
        )
        main_layout.setSpacing(DesignTokens.SPACING.LG)

        # 目标进度模块
        self.goal_progress_widget = self._create_goal_progress_module()
        main_layout.addWidget(self.goal_progress_widget)

        # 活动详情模块
        self.activity_list_widget = self._create_activity_list_module()
        main_layout.addWidget(self.activity_list_widget)

        # 快速操作模块
        self.quick_actions_widget = self._create_quick_actions_module()
        main_layout.addWidget(self.quick_actions_widget)

        # 自动刷新提示
        refresh_label = QLabel("自动刷新: 每 30 秒")
        refresh_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_XS}pt;
            color: {DesignTokens.COLOR.TEXT_TERTIARY};
        """)
        refresh_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(refresh_label)

    def _create_goal_progress_module(self) -> QFrame:
        """创建目标进度模块"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.LG}px;
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD
        )

        # 标题
        title = QLabel("🎯 今日目标进度")
        title.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_LG}pt;
            font-weight: 600;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        layout.addWidget(title)

        # 进度标签（保存引用以便更新）
        self.progress_label = QLabel("运动热量目标：0/300 千卡 (0%)")
        self.progress_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        layout.addWidget(self.progress_label)

        # 进度条背景
        progress_bar_bg = QFrame()
        progress_bar_bg.setFixedHeight(8)
        progress_bar_bg.setStyleSheet(f"""
            QFrame {{
                background-color: #E0E0E0;
                border-radius: 4px;
            }}
        """)
        layout.addWidget(progress_bar_bg)

        # 进度条填充（保存引用以便更新宽度）
        self.progress_bar_fill = QFrame(progress_bar_bg)
        self.progress_bar_fill.setFixedHeight(8)
        self.progress_bar_fill.setFixedWidth(0)
        self.progress_bar_fill.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.PRIMARY_SOLID};
                border-radius: 4px;
            }}
        """)

        # 打卡天数（保存引用）
        self.streak_label = QLabel("🔥 连续打卡：0 天")
        self.streak_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            color: {DesignTokens.COLOR.SUCCESS};
        """)
        layout.addWidget(self.streak_label)

        return frame

    def _create_activity_list_module(self) -> QFrame:
        """创建活动列表模块"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.LG}px;
            }}
        """)
        frame.setMinimumHeight(200)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD
        )

        # 标题
        title = QLabel("📋 今日活动详情")
        title.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_LG}pt;
            font-weight: 600;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        layout.addWidget(title)

        # 活动列表（滚动区域）
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self.activity_list_container = QWidget()
        list_layout = QVBoxLayout(self.activity_list_container)

        # 占位内容（保存引用）
        self.empty_label = QLabel("今天还没有活动记录")
        self.empty_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_SM}pt;
            color: {DesignTokens.COLOR.TEXT_TERTIARY};
        """)
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        list_layout.addWidget(self.empty_label)
        list_layout.addStretch()

        scroll.setWidget(self.activity_list_container)
        layout.addWidget(scroll)

        return frame

    def _create_quick_actions_module(self) -> QFrame:
        """创建快速操作模块"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.BG_CARD};
                border-radius: {DesignTokens.RADIUS.LG}px;
            }}
        """)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD,
            DesignTokens.SPACING.MD
        )

        # 四个快速操作按钮
        self.action_library_button = self._create_action_button("🏋️ 动作库")
        self.settings_button = self._create_action_button("⚙️ 参数设置")
        self.user_info_button = self._create_action_button("👤 用户信息")
        self.basic_settings_button = self._create_action_button("🔧 基础设置")

        # 连接按钮点击信号
        self.action_library_button.clicked.connect(self._show_action_library)
        self.settings_button.clicked.connect(self._show_settings)
        self.user_info_button.clicked.connect(self._show_user_info)
        self.basic_settings_button.clicked.connect(self._show_basic_settings)

        layout.addWidget(self.action_library_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.user_info_button)
        layout.addWidget(self.basic_settings_button)

        return frame

    def _create_action_button(self, text: str) -> QPushButton:
        """创建操作按钮"""
        button = QPushButton(text)
        button.setFixedSize(160, 50)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: #F5F5F5;
                color: {DesignTokens.COLOR.TEXT_PRIMARY};
                border: none;
                border-radius: {DesignTokens.RADIUS.SM}px;
                font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            }}
            QPushButton:hover {{
                background-color: {DesignTokens.COLOR.PRIMARY_LIGHT};
            }}
        """)
        return button

    def refresh_data(self):
        """刷新数据 - 从数据库获取并更新 UI"""
        from datetime import date

        logger.debug("刷新主窗口数据")

        try:
            from ..models.repositories import ActivityRepository, SettingRepository

            # 1. 刷新今日目标进度
            today_calories = ActivityRepository.get_calories_by_date(date.today())
            daily_goal = SettingRepository.get_int("daily_calorie_goal", 300)
            self._update_goal_progress(today_calories, daily_goal)

            # 2. 刷新今日活动列表
            activities = ActivityRepository.get_activities_by_date(date.today())
            self._update_activity_list(activities)

        except Exception as e:
            logger.error(f"刷新数据失败: {e}")

    def _update_goal_progress(self, current: float, goal: int):
        """更新目标进度显示"""
        percent = int((current / goal) * 100) if goal > 0 else 0
        percent = min(100, max(0, percent))  # 限制在 0-100

        # 更新进度文字
        self.progress_label.setText(f"运动热量目标：{int(current)}/{goal} 千卡 ({percent}%)")

        # 更新进度条宽度
        parent_width = self.progress_bar_fill.parent().width()
        fill_width = int(parent_width * percent / 100)
        self.progress_bar_fill.setFixedWidth(fill_width)

        # 打卡天数暂不实现
        self.streak_label.setText("🔥 连续打卡：-- 天")

    def _update_activity_list(self, activities):
        """更新今日活动列表"""
        # 清空现有列表
        layout = self.activity_list_container.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 如果没有活动，显示空状态
        if not activities:
            layout.addWidget(self.empty_label)
            layout.addStretch()
            return

        # 按时间倒序显示
        for activity in reversed(activities):
            activity_item = self._create_activity_item(activity)
            layout.addWidget(activity_item)

        layout.addStretch()

    def _create_activity_item(self, activity) -> QFrame:
        """创建单个活动项"""
        from datetime import datetime

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DesignTokens.COLOR.BG_SECONDARY};
                border-radius: {DesignTokens.RADIUS.SM}px;
                padding: {DesignTokens.SPACING.XS}px;
            }}
        """)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(
            DesignTokens.SPACING.SM,
            DesignTokens.SPACING.XS,
            DesignTokens.SPACING.SM,
            DesignTokens.SPACING.XS
        )

        # 时间标签
        time_str = activity.timestamp.strftime("%H:%M")
        time_label = QLabel(f"[ 今天 {time_str} ]")
        time_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_SM}pt;
            color: {DesignTokens.COLOR.TEXT_SECONDARY};
        """)
        layout.addWidget(time_label)

        # 图标和活动描述
        icon, desc = self._format_activity_description(activity)
        activity_label = QLabel(f"{icon} {desc}")
        activity_label.setStyleSheet(f"""
            font-size: {DesignTokens.TYPOGRAPHY.TEXT_BASE}pt;
            color: {DesignTokens.COLOR.TEXT_PRIMARY};
        """)
        layout.addWidget(activity_label)

        layout.addStretch()

        return frame

    def _format_activity_description(self, activity) -> tuple:
        """格式化活动描述为 (图标, 描述文字)"""
        activity_type = activity.activity_type
        duration = activity.duration_seconds

        if activity_type == "stand":
            minutes = duration / 60
            return "🧍", f"站立 {minutes:.1f} 分钟"
        elif activity_type == "exercise":
            minutes = duration / 60
            # ActivityLog 没有 notes 属性，使用默认名称
            return "🏃", f"运动 ({minutes:.0f}分钟)"
        elif activity_type == "gaze":
            minutes = duration / 60
            return "👁️", f"远眺 {minutes:.1f} 分钟"
        else:
            return "📋", f"{activity_type} ({duration}秒)"

    def _show_action_library(self):
        """显示动作库"""
        logger.info("打开动作库")
        from src.ui.dialogs.action_library_dialog import ActionLibraryDialog
        dialog = ActionLibraryDialog(self)
        dialog.exec()

    def _show_settings(self):
        """显示参数设置"""
        logger.info("打开参数设置")
        from src.ui.settings.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        dialog.exec()

    def _show_user_info(self):
        """显示用户信息"""
        logger.info("打开用户信息")
        from src.ui.dialogs.user_info_dialog import UserInfoDialog
        dialog = UserInfoDialog(self)
        dialog.exec()

    def _show_basic_settings(self):
        """显示基础设置"""
        logger.info("打开基础设置")
        from src.ui.dialogs.basic_settings_dialog import BasicSettingsDialog
        dialog = BasicSettingsDialog(self)
        dialog.exec()

    def closeEvent(self, event):
        """窗口关闭事件"""
        logger.info("主窗口关闭")
        self.refresh_timer.stop()
        event.accept()
