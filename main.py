from PyQt6.QtWidgets import QApplication, QVBoxLayout, QDataWidgetMapper, \
    QToolTip, QLabel, QWidget, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import pandas as pd
import re
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole) # This line isn't actually necessary but I thought it was interesting.

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Student_ID", "Name", "Course", "Mobile_Number"))
        self.setCentralWidget(self.table)

    def load_data(self):
        pass


app = QApplication(sys.argv)
sms = MainWindow()
sms.show()
sys.exit(app.exec())