"""
Grade Helper – PySide6 UI
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QLabel, QFrame,
    QHeaderView, QAbstractItemView, QSizePolicy, QMessageBox,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices



class GradeHelperWindow(QMainWindow):

    

    def __init__(self):

        super().__init__()
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.sel_row = 0

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
        self.btn_pick.clicked.connect(self.load_file)
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
        self.table.cellClicked.connect(self.id_choose)

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
        self.btn_add_selected.clicked.connect(self.grade_updater1)

        self.btn_add_all = QPushButton("Apply to All")
        self.btn_add_all.setObjectName("btn_secondary")
        self.btn_add_all.setCursor(Qt.PointingHandCursor)
        self.btn_add_all.setToolTip("Add bonus points to all students")
        self.btn_add_all.clicked.connect(self.grade_updater2)

        bonus_layout.addWidget(self.btn_add_selected)
        bonus_layout.addWidget(self.btn_add_all)

        layout.addWidget(bonus_container)

        # --- Bottom action bar ---
        self.btn_save = QPushButton("Save && Open in Excel")
        self.btn_save.setObjectName("btn_primary")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setFixedHeight(42)
        layout.addWidget(self.btn_save)
        self.btn_save.clicked.connect(self.saver)

    def spin_bonus_step_down(self):
        self.spin_bonus.stepDown()

    def spin_bonus_step_up(self):
        self.spin_bonus.stepUp()

    def load_file(self):
        with open('grades.csv', 'r') as f:
            next(f)
            for line in f:
                student_id, grade = line.strip().split(',')
                self.student_ids.append(int(student_id))
                self.original_grades.append(int(grade))
                self.corrected_grades.append(int(grade))

            student_all = []
            for row in range(len(self.student_ids)):
                student_all.append((self.student_ids[row],self.original_grades[row],self.original_grades[row]))
        for row, values in enumerate(student_all):
            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def id_choose(self, row, col):
        self.sel_row = row

    def grade_updater1(self):
        new_grade = self.corrected_grades[self.sel_row] + self.spin_bonus.value()
        if new_grade >= 100:
            new_grade = 100
        self.corrected_grades[self.sel_row] = new_grade
        self.table.setItem(self.sel_row, 2, QTableWidgetItem(str(new_grade)))

    def grade_updater2(self):
        for s in range(len(self.corrected_grades)):
            new_grade = self.corrected_grades[s] + self.spin_bonus.value()
            if new_grade >= 100:
                new_grade = 100
            self.corrected_grades[s] = new_grade
            self.table.setItem(s, 2, QTableWidgetItem(str(new_grade)))

    def saver(self):
        output_path = os.path.abspath('data_updated.csv')
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            f.write('ID, New Grade\n')
            for student in range(len(self.student_ids)):
                f.write(
                    f'{self.student_ids[student]}, '
                    f'{self.corrected_grades[student]}\n'
                )

        QDesktopServices.openUrl(QUrl.fromLocalFile(output_path))


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
