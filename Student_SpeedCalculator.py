import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox



class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()

        #ChatGPT Suggestion:
        self.avg_speed = ""
        self.closer = ""

        self.setWindowTitle("Speed Calcuator")
        grid = QGridLayout()

        # Create widgets
        dist_label = QLabel("Distance: ")
        self.dist_line_edit = QLineEdit()

        self.combo = QComboBox()
        self.combo.addItems(['Freedom (Miles)', 'Communist (KM)'])
        # ChatGPT Suggestion
        self.combo.currentIndexChanged.connect(self.update_closer)


        time_label = QLabel("Time (hours):")
        self.time_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Speed")
        calculate_button.clicked.connect(self.calculate_speed)
        self.output_label = QLabel("")


        #ChatGPT suggestion
        self.dist_line_edit.textChanged.connect(self.validate_input)
        self.time_line_edit.textChanged.connect(self.validate_input)
        # End

        # Add widgets to grid layout
        grid.addWidget(dist_label, 0, 0)
        grid.addWidget(self.dist_line_edit, 0, 1)
        grid.addWidget(self.combo, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2) # Tells the grid layout to add the button on the 2nd row, in the
        # first (0th) column, make the button 1 row high and 2 columns wide.
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_speed(self):
        # You can solve this here, you don't need to check constantly
        try:
            dist = float(self.dist_line_edit.text())
            time = float(self.time_line_edit.text())
            self.avg_speed = dist/time

            if self.combo.currentText() == 'Freedom (Miles)':
                closer = "Miles Prower"
            if self.combo.currentText() == 'Communist (KM)':
                closer = "km/h"

            self.output_label.setText(f"Average Speed is: {self.avg_speed} {self.closer}.")
        except ValueError:
            self.output_label.setText("Please enter a number in both fields.")

    def validate_input(self):
        if self.dist_line_edit.text() and self.time_line_edit.text():
            try:
                float(self.dist_line_edit.text())
                float(self.time_line_edit.text())
            except ValueError:
                self.output_label.setText("Please enter a number in both fields.")

    def update_closer(self):
        if self.combo.currentText() == 'Freedom (Miles)':
            self.closer = "Miles Prower"
        if self.combo.currentText() == 'Communist (KM)':
            self.closer = "km/h"
        self.output_label.setText(f"Average Speed is: {self.avg_speed} {self.closer}.")


app = QApplication(sys.argv)
app.setStyle('Fusion')
# app.setStyleSheet(qdarkstyle.load_stylesheet())

speed_calculator = SpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())



