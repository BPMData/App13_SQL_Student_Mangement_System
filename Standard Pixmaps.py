from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QStyle, QMainWindow, QApplication
import sys

# https://doc.qt.io/qt-6/qstyle.html#StandardPixmap-enum
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calcuator")
        self.setWindowTitle("Delete Student Record")

        pixmap = self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon).pixmap(16, 16)
        self.setWindowIcon(QIcon(pixmap))

app = QApplication(sys.argv)
sms = MainWindow()

sms.show()
sys.exit(app.exec())