import sys
import random
import math
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QDialog, QListWidget, QHBoxLayout, QMessageBox, QWidget, QInputDialog, QGraphicsView, QGraphicsScene, QGraphicsTextItem
)

class CoupleWishGameUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.general_wheel = []
        self.specialized_wheel = {"girl": [], "boy": []}
        self.credits = {"girl": 100, "boy": 100}

        self.setWindowTitle("Couple Wish Game")
        self.setGeometry(200, 200, 600, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Header
        self.title_label = QLabel("Couple Wish Game")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # Credits Display
        self.credit_label = QLabel(self.get_credits_display())
        self.credit_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.credit_label)

        # Buttons
        self.add_general_button = QPushButton("Add to General Wheel")
        self.add_special_button = QPushButton("Add to Specialized Wheel")
        self.spin_general_button = QPushButton("Spin General Wheel")
        self.spin_special_button = QPushButton("Spin Specialized Wheel")
        self.view_wheel_button = QPushButton("View Wheel Contents")

        self.add_general_button.clicked.connect(self.add_to_general_wheel)
        self.add_special_button.clicked.connect(self.add_to_specialized_wheel)
        self.spin_general_button.clicked.connect(lambda: self.spin_wheel("general"))
        self.spin_special_button.clicked.connect(lambda: self.spin_wheel("specialized"))
        self.view_wheel_button.clicked.connect(self.view_wheel_contents)

        layout.addWidget(self.add_general_button)
        layout.addWidget(self.add_special_button)
        layout.addWidget(self.spin_general_button)
        layout.addWidget(self.spin_special_button)
        layout.addWidget(self.view_wheel_button)

        # Wheel Display
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(400, 400)
        layout.addWidget(self.view)

        # Set Main Layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def get_credits_display(self):
        return f"Girl's Credits: {self.credits['girl']} | Boy's Credits: {self.credits['boy']}"

    def add_to_general_wheel(self):
        if len(self.general_wheel) >= 20:
            QMessageBox.warning(self, "Error", "The General Wheel is full!")
            return

        text, ok = self.get_input_dialog("Enter a demand for the General Wheel:")
        if ok and text.strip():
            if text in self.general_wheel:
                QMessageBox.warning(self, "Error", "This demand already exists in the General Wheel.")
            else:
                self.general_wheel.append(text.strip())
                QMessageBox.information(self, "Success", f"Demand '{text}' added to the General Wheel.")

    def add_to_specialized_wheel(self):
        person, ok = self.get_input_dialog("Enter 'girl' or 'boy' to select the Specialized Wheel:")
        if ok and person in self.specialized_wheel:
            if len(self.specialized_wheel[person]) >= 10:
                QMessageBox.warning(self, "Error", f"The Specialized Wheel for {person.capitalize()} is full!")
                return

            text, ok = self.get_input_dialog(f"Enter a demand for the Specialized Wheel ({person}):")
            if ok and text.strip():
                if text in self.specialized_wheel[person]:
                    QMessageBox.warning(self, "Error", f"This demand already exists in the Specialized Wheel for {person}.")
                else:
                    self.specialized_wheel[person].append(text.strip())
                    QMessageBox.information(self, "Success", f"Demand '{text}' added to the Specialized Wheel for {person.capitalize()}.")
        else:
            QMessageBox.warning(self, "Error", "Invalid person. Please enter 'girl' or 'boy'.")

    def spin_wheel(self, wheel_type):
        # Ask who is spinning the wheel
        spinner, ok = QInputDialog.getText (self, "Spinner Selection", "Who is spinning the wheel? (girl/boy)")
        if not ok or spinner not in ["girl", "boy"]:
            QMessageBox.warning(self, "Error", "Invalid selection. Please enter 'girl' or 'boy'.")
            return

        if wheel_type == "general":
            cost = 15
            wheel = self.general_wheel
        else:
            cost = 25
            wheel = self.specialized_wheel.get(spinner, [])
            if not wheel:
                QMessageBox.warning(self, "Error", f"The Specialized Wheel for {spinner.capitalize()} is empty!")
                return

        # Check if the spinner has enough credits
        if self.credits[spinner] < cost:
            QMessageBox.warning(self, "Error", f"{spinner.capitalize()} does not have enough credits to spin!")
            return

        # Spin the wheel
        selected = random.choice(wheel)
        wheel.remove(selected)
        self.credits[spinner] -= cost
        self.credit_label.setText(self.get_credits_display())
        QMessageBox.information(self, "Result", f"{spinner.capitalize()} spun the wheel and got: {selected}")

    def view_wheel_contents(self):
        message = f"General Wheel: {', '.join(self.general_wheel) or 'None'}\n\n"
        for person, wheel in self.specialized_wheel.items():
            message += f"{person.capitalize()} Specialized Wheel: {', '.join(wheel) or 'None'}\n"
        QMessageBox.information(self, "Wheel Contents", message)

    def get_input_dialog(self, prompt):
        dialog = QInputDialog(self)
        text, ok = dialog.getText(self, "Input", prompt)
        return text, ok

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoupleWishGameUI()
    window.show()
    sys.exit(app.exec_())