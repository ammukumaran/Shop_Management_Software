import sys
from time import sleep

from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtTest, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap

import sqlite3

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.rights = ""

    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")

        else:
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()
            query = 'SELECT username FROM login_info WHERE username =\'' + user + "\'"
            cur.execute(query)
            if cur.fetchone():
                query = 'SELECT password FROM login_info WHERE username =\'' + user + "\'"
                cur.execute(query)
                result_pass = cur.fetchone()[0]
                query = 'SELECT right FROM login_info WHERE username =\'' + user + "\'"
                cur.execute(query)
                self.rights = cur.fetchone()[0]
                if result_pass == password:
                    self.error.setText("Success")
                    QtTest.QTest.qWait(2000)
                    print("Successfully logged in.")

                    self.gotocreate()

                else:
                    self.error.setText("Invalid username or password")
            else:
                self.error.setText("Invalid username or password")
    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                self.focusNextPrevChild(True)
        return super().event(event)

    def gotocreate(self):
        print("hello")
        main = CreateMainScreen(self.emailfield.text(), self.rights)
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("createacc.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)

    def signupfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0:
            self.error.setText("Please fill in all inputs.")

        elif password != confirmpassword:
            self.error.setText("Passwords do not match.")
        else:
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()

            user_info = [user, password]
            cur.execute('INSERT INTO login_info (username, password) VALUES (?,?)', user_info)

            conn.commit()
            conn.close()

            fillprofile = FillProfileScreen()
            widget.addWidget(fillprofile)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class FillProfileScreen(QDialog):
    def __init__(self):
        super(FillProfileScreen, self).__init__()
        loadUi("fillprofile.ui", self)
        self.image.setPixmap(QPixmap('placeholder.png'))


class CreateMainScreen(QDialog):
    def __init__(self, user, rights):
        super(CreateMainScreen, self).__init__()
        loadUi("Main.ui", self)
        self.user.setText(user)
        self.access.setText(rights)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 250)

        # self.tabWidget

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                self.focusNextPrevChild(True)
        return super().event(event)


# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(968)
widget.setFixedWidth(1280)
widget.setWindowTitle("Akshara Boutique")
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
