from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QMessageBox
from PyQt5.QtGui import *
import sys

from database import Database

db = Database()
db.create_database()
db.load()


class MenuWindow(QtWidgets.QWidget):
    def __init__(self):
        self.user_window = AddUserWindow()
        db.create_database()
        db.load()
        super(MenuWindow, self).__init__()
        self.setWindowTitle("License Count")
        self.software_choices = db.show_software()
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('lclogo.png').scaled(150, 150, QtCore.Qt.KeepAspectRatio))

        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.label)

        self.go_to_add_software_button = QtWidgets.QPushButton(self)
        self.go_to_add_software_button.setText("Add/Delete Software")
        self.go_to_add_software_button.clicked.connect(self.go_to_add_software)
        layout.addWidget(self.go_to_add_software_button)

        self.go_to_add_user_button = QtWidgets.QPushButton(self)
        self.go_to_add_user_button.setText("Add/Delete User")
        self.go_to_add_user_button.clicked.connect(self.go_to_add_user)
        layout.addWidget(self.go_to_add_user_button)

        self.quit_button = QtWidgets.QPushButton(self)
        self.quit_button.setText("Quit")
        self.quit_button.clicked.connect(self.quit)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)
        self.show()

    def go_to_add_software(self):
        self.software_window = AddSoftwareWindow()

    def go_to_add_user(self):
        self.user_window = AddUserWindow()

    def quit(self):
        self.destroy(sys.exit())


class AddSoftwareWindow(QtWidgets.QWidget):
    def __init__(self):
        super(AddSoftwareWindow, self).__init__()

        self.setWindowTitle("Add/Delete Software")

        self.update()

        self.software_choices = db.show_software()
        self.software_combobox = QComboBox(self)
        self.software_combobox.addItems(self.software_choices)

        layout = QtWidgets.QGridLayout()

        self.software_delete_label = QtWidgets.QLabel(self)
        self.software_delete_label.setText("Delete Software")
        self.software_delete_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.software_delete_label)

        layout.addWidget(self.software_combobox)

        self.delete_button = QtWidgets.QPushButton(self)
        self.delete_button.setText("Delete")
        self.delete_button.clicked.connect(self.delete_software_popups)
        layout.addWidget(self.delete_button)

        self.software_add_label = QtWidgets.QLabel(self)
        self.software_add_label.setText("Add Software")
        self.software_add_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.software_add_label)

        self.software_name_label = QtWidgets.QLabel(self)
        self.software_name_label.setText("Software name")
        layout.addWidget(self.software_name_label)

        self.software_name_input = QtWidgets.QLineEdit()
        layout.addWidget(self.software_name_input)

        self.license_allowance_label = QtWidgets.QLabel(self)
        self.license_allowance_label.setText("License Allowance")
        layout.addWidget(self.license_allowance_label)

        self.license_allowance_input = QtWidgets.QLineEdit()
        layout.addWidget(self.license_allowance_input)

        self.add_software_button = QtWidgets.QPushButton(self)
        self.add_software_button.setText("Add")
        self.add_software_button.clicked.connect(self.add_software)
        layout.addWidget(self.add_software_button)

        self.go_back_button = QtWidgets.QPushButton(self)
        self.go_back_button.setText("Go Back")
        self.go_back_button.clicked.connect(self.quit)
        layout.addWidget(self.go_back_button)

        self.setLayout(layout)
        self.show()

    def delete_software_popups(self):
        if self.software_combobox.currentText() == "":
            error_msgbox = QMessageBox()
            error_msgbox.setIcon(QMessageBox.Information)
            error_msgbox.setWindowTitle("Delete Software")
            error_msgbox.setText("No software available")
            error_msgbox.setStandardButtons(QMessageBox.Ok)
            error_msgbox.exec()
        else:
            delete_msgbox = QMessageBox()
            delete_msgbox.setWindowTitle("Delete Software")
            delete_msgbox.setText(
                "Are you sure you want to delete " + self.software_combobox.currentText() + "? (All users will be deleted.)")
            delete_msgbox.setIcon(QMessageBox.Warning)
            delete_msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            delete_msgbox.setDefaultButton(QMessageBox.Yes)
            delete_msgbox.buttonClicked.connect(self.delete_software)
            delete_msgbox.exec_()

    def delete_software(self, i):
        if i.text() == "&Yes":
            db.delete_software(self.software_combobox.currentText())
            deleted_msgbox = QMessageBox()
            deleted_msgbox.setIcon(QMessageBox.Information)
            deleted_msgbox.setWindowTitle("Delete Software")
            deleted_msgbox.setText(self.software_combobox.currentText() + " has been deleted")
            deleted_msgbox.setStandardButtons(QMessageBox.Ok)
            deleted_msgbox.exec()
            text = self.software_combobox.currentIndex()
            self.software_combobox.removeItem(text)
        else:
            pass

    def add_software(self):
        if self.software_name_input.text() == "":
            error_msgbox = QMessageBox()
            error_msgbox.setIcon(QMessageBox.Information)
            error_msgbox.setWindowTitle("Add Software")
            error_msgbox.setText("Please enter a software")
            error_msgbox.setStandardButtons(QMessageBox.Ok)
            error_msgbox.exec()
        elif self.software_name_input.text() in db.show_software():
            error_msgbox = QMessageBox()
            error_msgbox.setIcon(QMessageBox.Information)
            error_msgbox.setWindowTitle("Add Software")
            error_msgbox.setText("Duplicate Software Added")
            error_msgbox.setStandardButtons(QMessageBox.Ok)
            error_msgbox.exec()
        else:
            db.add_software(self.software_name_input.text(), self.license_allowance_input.text())
            confirm_msgbox = QMessageBox()
            confirm_msgbox.setIcon(QMessageBox.Information)
            confirm_msgbox.setWindowTitle("Add Software")
            confirm_msgbox.setText(self.software_name_input.text() + " has been added")
            confirm_msgbox.setStandardButtons(QMessageBox.Ok)
            confirm_msgbox.exec()
            text = self.software_name_input.text()
            self.software_combobox.addItem(text)

    def quit(self):
        self.destroy()


class AddUserWindow(QtWidgets.QWidget):
    def __init__(self):
        super(AddUserWindow, self).__init__()

        self.setWindowTitle("Add/Delete User")

        self.software_choices = db.show_software()
        self.software_combobox = QComboBox(self)
        self.software_combobox.addItems(self.software_choices)

        self.current = MenuWindow.current_software(self)

        layout = QtWidgets.QGridLayout()

        self.select_software_label = QtWidgets.QLabel(self)
        self.select_software_label.setText("Select Software")
        self.select_software_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.select_software_label)

        layout.addWidget(self.software_combobox)

        self.delete_user_button = QtWidgets.QPushButton(self)
        self.delete_user_button.setText("Delete A User")
        self.delete_user_button.clicked.connect(self.software_users)
        layout.addWidget(self.delete_user_button)

        self.employee_name_label = QtWidgets.QLabel(self)
        self.employee_name_label.setText("Employee Name")
        self.employee_name_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.employee_name_label)

        self.employee_name_input = QtWidgets.QLineEdit()
        layout.addWidget(self.employee_name_input)

        self.submit_user_button = QtWidgets.QPushButton(self)
        self.submit_user_button.setText("Submit")
        self.submit_user_button.clicked.connect(self.submit)
        layout.addWidget(self.submit_user_button)

        self.go_back_button = QtWidgets.QPushButton(self)
        self.go_back_button.setText("Go Back")
        self.go_back_button.clicked.connect(self.quit)
        layout.addWidget(self.go_back_button)

        self.setLayout(layout)
        self.show()

    def software_users(self):
        if self.software_combobox.currentText() == "":
            error_msgbox = QMessageBox()
            error_msgbox.setIcon(QMessageBox.Information)
            error_msgbox.setWindowTitle("Delete User")
            error_msgbox.setText("No software available")
            error_msgbox.setStandardButtons(QMessageBox.Ok)
            error_msgbox.exec()
        else:
            self.software_window = DeleteUserWindow(self.software_combobox.currentText())

    def submit(self):
        if self.software_combobox.currentText() == "" and self.employee_name_input != "":
            error_msgbox = QMessageBox()
            error_msgbox.setIcon(QMessageBox.Information)
            error_msgbox.setWindowTitle("Add User")
            error_msgbox.setText("No Software available to add users to")
            error_msgbox.setStandardButtons(QMessageBox.Ok)
            error_msgbox.exec()
        elif self.employee_name_input.text() == "":
            error_msgbox = QMessageBox()
            error_msgbox.setIcon(QMessageBox.Information)
            error_msgbox.setWindowTitle("Add User")
            error_msgbox.setText("Please enter a name")
            error_msgbox.setStandardButtons(QMessageBox.Ok)
            error_msgbox.exec()
        elif self.employee_name_input.text() in db.show_users(self.software_combobox.currentText()):
            duplicate_msgbox = QMessageBox()
            duplicate_msgbox.setIcon(QMessageBox.Warning)
            duplicate_msgbox.setWindowTitle("Add User")
            duplicate_msgbox.setText("Duplicate Name Entered!")
            duplicate_msgbox.setStandardButtons(QMessageBox.Ok)
            duplicate_msgbox.exec()
        else:
            db.add_user(self.software_combobox.currentText(), self.employee_name_input.text())
            user_added_msgbox = QMessageBox()
            user_added_msgbox.setIcon(QMessageBox.Information)
            user_added_msgbox.setWindowTitle("Add User")
            user_added_msgbox.setText("User Added")
            user_added_msgbox.setStandardButtons(QMessageBox.Ok)
            user_added_msgbox.exec()

    def quit(self):
        self.destroy()


class DeleteUserWindow(QtWidgets.QWidget):
    def __init__(self, software):
        super(DeleteUserWindow, self).__init__()

        self.setWindowTitle("Delete User")

        self.software = software

        layout = QtWidgets.QGridLayout()

        self.software_name_label = QtWidgets.QLabel(self)
        self.software_name_label.setText(self.software)
        self.software_name_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.software_name_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.software_name_label)

        self.license_allowance_label = QtWidgets.QLabel(self)
        self.license_allowance_label.setText("Licenses Left")
        self.license_allowance_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.license_allowance_label)

        self.default_allowance = db.show_licenses(self.software)
        self.active_allowance = db.remaining_licenses(self.software)
        self.remaining_licenses = self.default_allowance - self.active_allowance

        self.license_left_label = QtWidgets.QLabel(self)
        self.license_left_label.setText(str(self.remaining_licenses))
        self.license_left_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.license_left_label)

        self.delete_user_label = QtWidgets.QLabel(self)
        self.delete_user_label.setText("Delete User")
        self.delete_user_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.delete_user_label)

        self.name_choices = db.show_users(self.software)
        self.user_combobox = QComboBox(self)
        self.user_combobox.addItems(self.name_choices)
        layout.addWidget(self.user_combobox)

        self.delete_button = QtWidgets.QPushButton(self)
        self.delete_button.setText("Delete")
        self.delete_button.clicked.connect(self.delete_user_msgbox)
        layout.addWidget(self.delete_button)

        self.go_back_button = QtWidgets.QPushButton(self)
        self.go_back_button.setText("Go Back")
        self.go_back_button.clicked.connect(self.quit)
        layout.addWidget(self.go_back_button)

        self.setLayout(layout)
        self.show()

    def delete_user_msgbox(self):
        if self.user_combobox.currentText() == "":
            error_msgbox = QMessageBox()
            error_msgbox.setIcon(QMessageBox.Information)
            error_msgbox.setWindowTitle("Delete User")
            error_msgbox.setText("No Users available")
            error_msgbox.setStandardButtons(QMessageBox.Ok)
            error_msgbox.exec()
        else:
            delete_msgbox = QMessageBox()
            delete_msgbox.setWindowTitle("Delete User")
            delete_msgbox.setText(
                "Are you sure you want to delete " + self.user_combobox.currentText() + "?")
            delete_msgbox.setIcon(QMessageBox.Warning)
            delete_msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            delete_msgbox.setDefaultButton(QMessageBox.Yes)
            delete_msgbox.buttonClicked.connect(self.delete_user)
            delete_msgbox.exec_()

    def delete_user(self, i):
        if i.text() == "&Yes":
            db.delete_user(self.user_combobox.currentText())
            confirm_msgbox = QMessageBox()
            confirm_msgbox.setIcon(QMessageBox.Information)
            confirm_msgbox.setWindowTitle("Delete User")
            confirm_msgbox.setText(self.user_combobox.currentText() + " has been deleted")
            confirm_msgbox.setStandardButtons(QMessageBox.Ok)
            confirm_msgbox.exec()
            text = self.user_combobox.currentIndex()
            self.user_combobox.removeItem(text)
        else:
            pass

    def quit(self):
        self.destroy()


app = QApplication(sys.argv)
my_gui = MenuWindow()
sys.exit(app.exec())
