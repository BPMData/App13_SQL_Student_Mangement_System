import sqlite3
import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget,\
    QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, QPushButton, QComboBox, \
    QAbstractItemView, QToolBar, QStatusBar, QLabel, QMessageBox, QStyle, QGridLayout
import mysql.connector

class DatabaseConnection:
    def __init__(self,  password, host="localhost", user="root", database="school"):
        self.host = host
        self.user = user
        self.password = os.getenv(password)
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        return connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 300)

        self.buttons_added = False


        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        find_menu = self.menuBar().addMenu("&Find")

        add_student_action = QAction(QIcon('icons/icons/add.png'), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.about)



        search_action = QAction(QIcon('icons/icons/search.png'), "Search", self)
        search_action.triggered.connect(self.search)
        find_menu.addAction(search_action)



        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Student_ID", "Name", "Course", "Mobile_Number"))
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger(0)) # Edits to the table directly won't actually take efect, so we disable the ability to think you're doing it.
        # self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior(1)) #Whoops this interferes with the edit functionality.
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        # global buttons_added Alternate_solution
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)


        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Third solution
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    # noinspection PyUnresolvedReferences
    def load_data(self, database):
        connection = DatabaseConnection('MySQL_Root').connect()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students")
            query = cursor.fetchall()
            self.table.setRowCount(0)
            for row_index, whole_row in enumerate(query):
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

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About this App")

        content = """
        This application was made to demonstrate how to use Python to create 
        a graphical user interface that can read and edit an SQL database.
        This app uses SQlite3.
        """
        self.setText(content)
        pixmap = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion).pixmap(16, 16)
        self.setWindowIcon(QIcon(pixmap))
        self.setIcon(QMessageBox.Icon.Information)


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Record")
        self.setFixedWidth(200)

        pixmap = self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon).pixmap(16, 16)
        self.setWindowIcon(QIcon(pixmap))
        layout = QGridLayout()

        row_index = sms.table.currentRow()
        self.student_id = int(sms.table.item(row_index, 0).text())
        student_name = sms.table.item(row_index, 1).text()
        student_course = sms.table.item(row_index, 2).text()
        student_mobile = sms.table.item(row_index, 3).text()

        self.warning = QLabel("Are you ABSOLUTELY SURE you want to delete this student entirely from the records?")
        self.warning.setWordWrap(True)
        self.warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.warning, 0, 0, 1,2) # Add warning at row 0, column 0, make it 1 row high, 2 columns wide

        # Add a save button
        save_button = QPushButton("Yes, I'm sure.")
        save_button.clicked.connect(self.delete_student)  # This will close the dialog.
        layout.addWidget(save_button, 1, 0)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)  # This will close the dialog.
        layout.addWidget(cancel_button, 1, 1)

        self.setLayout(layout)

    def delete_student(self):
        connection = DatabaseConnection('MySQL_Root').connect()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE id = %s",
                           (self.student_id, ))
            connection.commit()
            cursor.close()
            connection.close()
            sms.load_data("database.db")

            msg = QMessageBox()
            msg.setWindowTitle("Update Status")
            pixmap3 = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton).pixmap(16, 16)
            msg.setWindowIcon(QIcon(pixmap3))
            msg.setText("That kid's gone!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            self.close()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.setWindowTitle("Edit Student Data")
        layout = QVBoxLayout()

# Here's the part I didn't know how to do - access table data

        row_index = sms.table.currentRow()
        self.student_id = int(sms.table.item(row_index, 0).text())
        student_name = sms.table.item(row_index, 1).text()
        student_course = sms.table.item(row_index, 2).text()
        student_mobile = sms.table.item(row_index, 3).text()
        print(row_index, student_mobile, self.student_id, student_course, student_name)

        self.student_name = QLineEdit(student_name)
        layout.addWidget(self.student_name)

        self.course_choice = QComboBox()
        courses = ["Astronomy", "Biology", "Math", "Physics"]
        self.course_choice.addItems(courses)
        self.course_choice.setCurrentText(student_course)
        layout.addWidget(self.course_choice)

        # Add mobile number
        self.phone_number = QLineEdit(student_mobile)
        self.phone_number.setPlaceholderText("Contact Number")
        layout.addWidget(self.phone_number)

        # Add a save button
        save_button = QPushButton("Edit Student Data")
        save_button.clicked.connect(self.edit_student)  # This will close the dialog.
        layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)  # This will close the dialog.
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def edit_student(self):
        name = self.student_name.text()
        course = self.course_choice.itemText(self.course_choice.currentIndex())
        mobile = self.phone_number.text()
        connection = DatabaseConnection('MySQL_Root').connect()
        with connection.cursor() as cursor:
            # noinspection PyUnresolvedReferences
            cursor.execute("UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s",
                           (name, course, mobile, self.student_id))
            connection.commit()
            cursor.close()
            connection.close()
            sms.load_data("database.db")

            msg = QMessageBox()
            msg.setWindowTitle("Update Status")
            msg.setText("Changes saved successfully!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()

            self.close()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_choice = QComboBox()
        courses = ["Astronomy", "Biology", "Math", "Physics"]
        self.course_choice.addItems(courses)
        layout.addWidget(self.course_choice)

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
        connection = DatabaseConnection('MySQL_Root').connect()
        with connection.cursor() as cursor:
            # noinspection PyUnresolvedReferences
            cursor.execute("INSERT INTO students (name,course, mobile) VALUES (%s, %s, %s)",
                           (name, course, mobile))
            connection.commit()
            cursor.close()
            connection.close()
            sms.load_data("database.db")

            msg = QMessageBox()
            msg.setWindowTitle("Update Status")
            msg.setText("Student record saved successfully!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()

            self.close()

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
        connection = DatabaseConnection('MySQL_Root').connect()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students WHERE UPPER(name) LIKE UPPER(%s)", ('%'+ name + '%',))
            query = cursor.fetchall()
            rows = list(query)
            print(rows)
            items = sms.table.findItems(name, Qt.MatchFlag.MatchContains)
            for item in items:
                row = item.row()
                for column in range(sms.table.columnCount()):
                    sms.table.item(row, column).setSelected(True)
            cursor.close()
            connection.close()
            self.close()




app = QApplication(sys.argv)
sms = MainWindow()
sms.load_data("database.db")
sms.show()
sys.exit(app.exec())