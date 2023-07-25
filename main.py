import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget,\
    QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, QPushButton, QComboBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 300)


        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        find_menu = self.menuBar().addMenu("&Find")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole) # This line isn't actually necessary but I thought it was interesting.

        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        find_menu.addAction(search_action)



        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Student_ID", "Name", "Course", "Mobile_Number"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    # noinspection PyUnresolvedReferences
    def load_data(self, database):
        connection = sqlite3.connect(database)
        # noinspection PyUnresolvedReferences
        query = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_index, whole_row in enumerate(query):
            self.table.insertRow(row_index)
            for column_index, cell_contents in enumerate(whole_row):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(cell_contents)))
                print("this is the row data", whole_row)
                print("this is the column data", cell_contents)
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()



class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        # self.setFixedWidth(300)
        # self.setFixedHeight(300)
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_choice = QComboBox()
        courses = ["Astronomy", "Biology", "Math", "Physics"]
        self.course_choice.addItems(courses)
        layout.addWidget(self.course_choice)
        # # ChatGPT Suggestion
        # self.combo.currentIndexChanged.connect(self.update_closer)

        # Add mobile number
        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Contact Number")
        layout.addWidget(self.phone_number)

        # Add a save button
        save_button = QPushButton("Insert Student Data")
        save_button.clicked.connect(self.save_student)  # This will close the dialog.
        layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)  # This will close the dialog.
        layout.addWidget(cancel_button)

        self.setLayout(layout)


    def save_student(self):
        name = self.student_name.text()
        course = self.course_choice.itemText(self.course_choice.currentIndex())
        mobile = self.phone_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        # noinspection PyUnresolvedReferences
        cursor.execute("INSERT INTO students (name,course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        sms.load_data("database.db")

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Records")
        self.setFixedWidth(600)
        # self.setFixedHeight(300)
        # self.setFixedSize(300, 100)

        layout = QVBoxLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Name to search for")
        layout.addWidget(self.search_name)

        # self.search_course = QComboBox()
        # courses = ["Astronomy", "Biology", "Math", "Physics"]
        # self.search_course.addItems(courses)
        # layout.addWidget(self.search_course)
        # # # ChatGPT Suggestion
        # # self.combo.currentIndexChanged.connect(self.update_closer)


        # Add a search button
        search_button = QPushButton("Search records")
        search_button.clicked.connect(self.search_records) # This will call the search.
        search_button.clicked.connect(self.close)
        layout.addWidget(search_button)

        # Add a cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)  # This will close the dialog.
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def search_records(self):
        name = self.search_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        query = cursor.execute("SELECT * FROM students WHERE UPPER(name) LIKE UPPER(?)", ('%'+ name + '%',))
        rows = list(query)
        print(rows)
        items = sms.table.findItems(name, Qt.MatchFlag.MatchContains)
        for item in items:
            row = item.row()
            for column in range(sms.table.columnCount()):
                sms.table.item(row, column).setSelected(True)
        cursor.close()
        connection.close()




app = QApplication(sys.argv)
sms = MainWindow()
sms.load_data("database.db")
sms.show()
sys.exit(app.exec())