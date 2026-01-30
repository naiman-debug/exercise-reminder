# -*- coding: utf-8 -*-
"""
动作库管理界面

提供动作的增删改查功能
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLabel, QComboBox, QSpinBox,
    QDoubleSpinBox, QLineEdit, QDialog, QDialogButtonBox,
    QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from ...models.repositories import ExerciseRepository


class ExerciseEditDialog(QDialog):
    """
    动作编辑对话框

    用于新增或编辑动作
    """

    # 信号：数据已更改
    data_changed = Signal()

    def __init__(self, exercise_id: int = None, parent=None):
        """
        初始化对话框

        Args:
            exercise_id: 动作ID（None表示新增）
            parent: 父窗口
        """
        super().__init__(parent)
        self.exercise_id = exercise_id
        self.setup_ui()

        # 如果是编辑模式，加载数据
        if self.exercise_id is not None:
            self._load_exercise_data()

    def setup_ui(self):
        """设置UI"""
        title = "编辑动作" if self.exercise_id else "新增动作"
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 动作名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("动作名称："))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("如：开合跳")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # 动作分类
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("动作分类："))
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "低强度",
            "中等强度",
            "中高强度",
            "小器械"
        ])
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)

        # 时长
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("时长（秒）："))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(10, 300)
        self.duration_spin.setValue(30)
        self.duration_spin.setSuffix(" 秒")
        duration_layout.addWidget(self.duration_spin)
        duration_layout.addStretch()
        layout.addLayout(duration_layout)

        # MET值
        met_layout = QHBoxLayout()
        met_layout.addWidget(QLabel("MET值："))
        self.met_spin = QDoubleSpinBox()
        self.met_spin.setRange(1.0, 20.0)
        self.met_spin.setSingleStep(0.5)
        self.met_spin.setValue(5.0)
        met_layout.addWidget(self.met_spin)

        # MET参考按钮
        met_ref_btn = QPushButton("参考")
        met_ref_btn.setFixedWidth(60)
        met_ref_btn.clicked.connect(self._show_met_reference)
        met_layout.addWidget(met_ref_btn)
        met_layout.addStretch()
        layout.addLayout(met_layout)

        # 说明
        hint_label = QLabel(
            "MET值参考：低强度 3.5 | 中等强度 5.0 | 中高强度 7.0 | 小器械 4.0"
        )
        hint_label.setStyleSheet("color: #757575; font-size: 11pt;")
        hint_label.setWordWrap(True)
        layout.addWidget(hint_label)

        layout.addStretch()

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.ok_btn = QPushButton("确定")
        self.ok_btn.setMinimumWidth(100)
        self.ok_btn.clicked.connect(self._on_ok)
        btn_layout.addWidget(self.ok_btn)

        cancel_btn = QPushButton("取消")
        cancel_btn.setMinimumWidth(100)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _load_exercise_data(self):
        """加载动作数据"""
        exercise = ExerciseRepository.get_by_id(self.exercise_id)
        if exercise:
            self.name_input.setText(exercise.name)
            self.duration_spin.setValue(exercise.duration_seconds)
            self.met_spin.setValue(exercise.met_value)

            # 设置分类
            index = self.category_combo.findText(exercise.category)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)

    def _show_met_reference(self):
        """显示MET值参考"""
        QMessageBox.information(
            self,
            "MET 值参考",
            """常用动作 MET 值参考：

低强度（约 3.5）：
- 原地踏步
- 靠墙静蹲
- 手臂画圈

中等强度（约 5.0）：
- 开合跳
- 自重深蹲
- 高抬腿

中高强度（约 7.0）：
- 简化波比跳
- 登山跑

小器械（约 4.0）：
- 哑铃推举
- 弹力绳划船

MET值越高，消耗热量越多。"""
        )

    def _on_ok(self):
        """确定按钮点击"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "验证失败", "请输入动作名称")
            return

        category = self.category_combo.currentText()
        duration = self.duration_spin.value()
        met = self.met_spin.value()

        if self.exercise_id:
            # 更新
            ExerciseRepository.update(
                self.exercise_id,
                name=name,
                duration_seconds=duration,
                met_value=met,
                category=category
            )
        else:
            # 新增
            ExerciseRepository.create(name, duration, met, category)

        self.data_changed.emit()
        self.accept()

    def get_data(self) -> dict:
        """获取输入的数据"""
        return {
            "name": self.name_input.text().strip(),
            "category": self.category_combo.currentText(),
            "duration_seconds": self.duration_spin.value(),
            "met_value": self.met_spin.value()
        }


class ExerciseLibraryWidget(QWidget):
    """
    动作库管理组件

    显示动作列表，提供增删改功能
    """

    # 信号：数据已更改
    data_changed = Signal()

    # 预定义分类
    CATEGORIES = ["低强度", "中等强度", "中高强度", "小器械"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_filter = "全部"
        self.setup_ui()
        self._load_data()

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # 标题栏
        title_layout = QHBoxLayout()

        title_label = QLabel("动作库管理")
        title_font = QFont("Microsoft YaHei UI", 14, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)

        title_layout.addStretch()

        # 筛选下拉框
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("筛选："))
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("全部")
        for category in self.CATEGORIES:
            self.filter_combo.addItem(category)
        self.filter_combo.currentTextChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()

        # 新增按钮
        self.add_btn = QPushButton("新增动作")
        self.add_btn.setMinimumWidth(100)
        self.add_btn.clicked.connect(self._on_add_exercise)
        filter_layout.addWidget(self.add_btn)

        layout.addLayout(title_layout)
        layout.addLayout(filter_layout)

        # 动作表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["动作名称", "分类", "时长(秒)", "MET值", "操作"])

        # 设置表格属性
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)

        # 设置样式
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background-color: #FFFFFF;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #E0E0E0;
                font-weight: bold;
            }
        """)

        layout.addWidget(self.table)

        # 统计信息
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color: #757575; font-size: 11pt;")
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def _load_data(self):
        """加载数据"""
        # 清空表格
        self.table.setRowCount(0)

        # 获取数据
        if self.current_filter == "全部":
            exercises = ExerciseRepository.get_all()
        else:
            exercises = ExerciseRepository.get_by_category(self.current_filter)

        # 填充表格
        self.table.setRowCount(len(exercises))
        for row, exercise in enumerate(exercises):
            # 动作名称
            name_item = QTableWidgetItem(exercise.name)
            self.table.setItem(row, 0, name_item)

            # 分类
            category_item = QTableWidgetItem(exercise.category)
            self.table.setItem(row, 1, category_item)

            # 时长
            duration_item = QTableWidgetItem(str(exercise.duration_seconds))
            duration_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, duration_item)

            # MET值
            met_item = QTableWidgetItem(str(exercise.met_value))
            met_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, met_item)

            # 操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.addStretch()

            edit_btn = QPushButton("编辑")
            edit_btn.setFixedWidth(60)
            edit_btn.clicked.connect(lambda checked, ex_id=exercise.id: self._on_edit_exercise(ex_id))
            btn_layout.addWidget(edit_btn)

            delete_btn = QPushButton("删除")
            delete_btn.setFixedWidth(60)
            delete_btn.clicked.connect(lambda checked, ex_id=exercise.id: self._on_delete_exercise(ex_id))
            btn_layout.addWidget(delete_btn)

            self.table.setCellWidget(row, 4, btn_widget)

        # 更新统计
        self.stats_label.setText(f"共 {len(exercises)} 个动作")

    def _on_filter_changed(self, text: str):
        """筛选条件改变"""
        self.current_filter = text
        self._load_data()

    def _on_add_exercise(self):
        """新增动作"""
        dialog = ExerciseEditDialog(parent=self)
        dialog.data_changed.connect(self._load_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_data()
            self.data_changed.emit()

    def _on_edit_exercise(self, exercise_id: int):
        """编辑动作"""
        dialog = ExerciseEditDialog(exercise_id, parent=self)
        dialog.data_changed.connect(self._load_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_data()
            self.data_changed.emit()

    def _on_delete_exercise(self, exercise_id: int):
        """删除动作"""
        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除这个动作吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if ExerciseRepository.delete(exercise_id):
                self._load_data()
                self.data_changed.emit()
            else:
                QMessageBox.warning(self, "删除失败", "删除动作失败，请重试")

    def refresh(self):
        """刷新数据"""
        self._load_data()
