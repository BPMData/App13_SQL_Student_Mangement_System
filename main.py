from PyQt6.QtWidgets import QApplication, QVBoxLayout, QDataWidgetMapper, \
    QToolTip, QLabel, QWidget, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import pandas as pd
import re
import sys
import sqlite3

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
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self, database):
        connection = sqlite3.connect(database)
        query = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_index, whole_row in enumerate(query):
            self.table.insertRow(row_index)
            for column_index, cell_contents in enumerate(whole_row):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(cell_contents)))
                print("this is the row data", whole_row)
                print("this is the column data", cell_contents)
        connection.close()


app = QApplication(sys.argv)
sms = MainWindow()
sms.show()
sms.load_data("database.db")
sys.exit(app.exec())