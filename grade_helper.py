"""
Grade Helper – PySide6 UI (layout only)
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QSpinBox, QLabel, QFrame,
    QHeaderView, QAbstractItemView,
)
from PySide6.QtCore import Qt


class GradeHelperWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Helper")
        self.setMinimumSize(680, 750)

        # --- Central widget & main layout ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # --- Title ---
        self.title_label = QLabel("Grade Helper")
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # --- Separator ---
        sep1 = QFrame()
        sep1.setObjectName("separator")
        sep1.setFrameShape(QFrame.HLine)
        layout.addWidget(sep1)

        # --- File picker row ---
        file_row = QHBoxLayout()
        file_row.setSpacing(10)
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("file_label")
        self.btn_pick = QPushButton("📂  Pick File")
        self.btn_pick.setObjectName("btn_pick")
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(self.btn_pick)
        layout.addLayout(file_row)

        # --- Table ---
        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grade", "Corrected Grade"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # --- Separator ---
        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.HLine)
        layout.addWidget(sep2)

        # --- Bonus controls ---
        bonus_row = QHBoxLayout()
        bonus_row.setSpacing(10)
        bonus_label = QLabel("Bonus Points:")
        bonus_label.setStyleSheet("font-weight: 600;")
        bonus_row.addWidget(bonus_label)

        self.spin_bonus = QSpinBox()
        self.spin_bonus.setRange(-100, 100)
        self.spin_bonus.setValue(0)
        self.spin_bonus.setAlignment(Qt.AlignCenter)
        self.spin_bonus.setMinimumWidth(70)
        self.spin_bonus.setFixedHeight(36)

        self.btn_spin_minus = QPushButton("−")
        self.btn_spin_minus.setObjectName("btn_spin")
        self.btn_spin_minus.clicked.connect(self.spin_bonus.stepDown)

        self.btn_spin_plus = QPushButton("+")
        self.btn_spin_plus.setObjectName("btn_spin")
        self.btn_spin_plus.clicked.connect(self.spin_bonus.stepUp)

        bonus_row.addWidget(self.btn_spin_minus)
        bonus_row.addWidget(self.spin_bonus)
        bonus_row.addWidget(self.btn_spin_plus)

        bonus_row.addStretch()

        self.btn_add_selected = QPushButton("✚  Add to Selected")
        self.btn_add_selected.setObjectName("btn_add_selected")
        self.btn_add_selected.setToolTip("Apply bonus to selected rows only")

        self.btn_add_all = QPushButton("✚  Add to All")
        self.btn_add_all.setObjectName("btn_add_all")
        self.btn_add_all.setToolTip("Apply bonus to every student")

        bonus_row.addWidget(self.btn_add_selected)
        bonus_row.addWidget(self.btn_add_all)
        layout.addLayout(bonus_row)

        # --- Save & open button ---
        self.btn_save = QPushButton("💾  Save && Open in Excel")
        self.btn_save.setObjectName("btn_save")
        layout.addWidget(self.btn_save)


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
