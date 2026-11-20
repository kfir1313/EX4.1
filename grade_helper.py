"""
Grade Helper – PySide6 UI (layout only)
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QSpinBox, QLabel, QFrame,
    QHeaderView, QAbstractItemView, QSizePolicy,
)
from PySide6.QtCore import Qt


class GradeHelperWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Helper")
        self.resize(720, 800)
        self.setMinimumSize(640, 680)

        # --- Central widget & main layout ---
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        # --- Header section ---
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        self.title_label = QLabel("Grade Management")
        self.title_label.setObjectName("title_label")
        header_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Select a grade sheet to view records, apply adjustments, and export.")
        self.subtitle_label.setObjectName("subtitle_label")
        header_layout.addWidget(self.subtitle_label)

        layout.addLayout(header_layout)

        # --- File selection card ---
        file_container = QFrame()
        file_container.setObjectName("file_card")
        file_layout = QHBoxLayout(file_container)
        file_layout.setContentsMargins(12, 10, 12, 10)
        file_layout.setSpacing(12)

        file_desc = QLabel("Source File:")
        file_desc.setObjectName("field_label")
        file_layout.addWidget(file_desc)

        self.file_label = QLabel("No file selected — choose a CSV file to load")
        self.file_label.setObjectName("file_label")
        file_layout.addWidget(self.file_label, 1)

        self.btn_pick = QPushButton("Browse...")
        self.btn_pick.setObjectName("btn_secondary")
        self.btn_pick.setCursor(Qt.PointingHandCursor)
        file_layout.addWidget(self.btn_pick)

        layout.addWidget(file_container)

        # --- Table Section ---
        table_container = QFrame()
        table_container.setObjectName("table_card")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(1, 1, 1, 1)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["Student ID", "Original Grade", "Corrected Grade"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        table_layout.addWidget(self.table)

        layout.addWidget(table_container, 1)

        # --- Bonus Controls Card ---
        bonus_container = QFrame()
        bonus_container.setObjectName("bonus_card")
        bonus_layout = QHBoxLayout(bonus_container)
        bonus_layout.setContentsMargins(16, 12, 16, 12)
        bonus_layout.setSpacing(14)

        bonus_label = QLabel("Bonus Points:")
        bonus_label.setObjectName("field_label")
        bonus_layout.addWidget(bonus_label)

        # Stepper group
        stepper_layout = QHBoxLayout()
        stepper_layout.setSpacing(4)

        self.btn_spin_minus = QPushButton("−")
        self.btn_spin_minus.setObjectName("btn_stepper")
        self.btn_spin_minus.setCursor(Qt.PointingHandCursor)
        self.btn_spin_minus.clicked.connect(self.spin_bonus_step_down)

        self.spin_bonus = QSpinBox()
        self.spin_bonus.setRange(-100, 100)
        self.spin_bonus.setValue(0)
        self.spin_bonus.setAlignment(Qt.AlignCenter)
        self.spin_bonus.setFixedHeight(34)
        self.spin_bonus.setFixedWidth(70)

        self.btn_spin_plus = QPushButton("+")
        self.btn_spin_plus.setObjectName("btn_stepper")
        self.btn_spin_plus.setCursor(Qt.PointingHandCursor)
        self.btn_spin_plus.clicked.connect(self.spin_bonus_step_up)

        stepper_layout.addWidget(self.btn_spin_minus)
        stepper_layout.addWidget(self.spin_bonus)
        stepper_layout.addWidget(self.btn_spin_plus)

        bonus_layout.addLayout(stepper_layout)
        bonus_layout.addStretch()

        self.btn_add_selected = QPushButton("Apply to Selected")
        self.btn_add_selected.setObjectName("btn_secondary")
        self.btn_add_selected.setCursor(Qt.PointingHandCursor)
        self.btn_add_selected.setToolTip("Add bonus points to selected rows only")

        self.btn_add_all = QPushButton("Apply to All")
        self.btn_add_all.setObjectName("btn_secondary")
        self.btn_add_all.setCursor(Qt.PointingHandCursor)
        self.btn_add_all.setToolTip("Add bonus points to all students")

        bonus_layout.addWidget(self.btn_add_selected)
        bonus_layout.addWidget(self.btn_add_all)

        layout.addWidget(bonus_container)

        # --- Bottom action bar ---
        self.btn_save = QPushButton("Save && Open in Excel")
        self.btn_save.setObjectName("btn_primary")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setFixedHeight(42)
        layout.addWidget(self.btn_save)

    def spin_bonus_step_down(self):
        self.spin_bonus.stepDown()

    def spin_bonus_step_up(self):
        self.spin_bonus.stepUp()


def load_stylesheet(app: QApplication):
    """Load the QSS stylesheet from the same directory as this script."""
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    load_stylesheet(app)
    window = GradeHelperWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
