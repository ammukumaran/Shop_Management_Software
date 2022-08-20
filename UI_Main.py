import mysql.connector
import sys
from PyQt5.QtCore import QTimer, QEvent, Qt, QSize
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, QtTest, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass",
    database="abcms"
)

mycursor = mydb.cursor()

# mycursor.execute("SHOW TABLES")
#
# for x in mycursor:
#   print(x)

# sql = "INSERT INTO abcustomer (name, phone) VALUES (%s, %s)"
# val = ("Selva", "9000677377")
# mycursor.execute(sql, val)
#
# mydb.commit()

# mycursor.execute("SELECT * FROM abcustomer")
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#   print(x)
ui, _ = loadUiType('MainUI.ui')


class WelcomeScreen(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.login.clicked.connect(self.gotologin)
        # self.create.clicked.connect(self.gotocreate)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.btnLogin.clicked.connect(self.gotologin)
        self.msg = QMessageBox()

    def gotologin(self):
        un = self.lineUser.text()
        pw = self.linePass.text()
        if un == "admin" and pw == 'admin':
            self.tabWidget.tabBar().setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        self.mycursor = mydb.cursor()
        self.btnCustSearch.clicked.connect(self.customerSearch)
        self.btnCustClear.clicked.connect(self.customerClear)
        self.btnNewCust.clicked.connect(self.newCustTab)

        # self.mycursor.execute("SELECT * FROM abcustomer")
        #
        # myresult = self.mycursor.fetchall()
        #
        # for x in myresult:
        #     print(x)

    def newCustTab(self):
        self.tabWidget.setCurrentIndex(2)

    def customerSearch(self):
        self.toolbtnLeft.clicked.connect(self.cusRecLeft)
        self.toolbtnRight.clicked.connect(self.cusRecRight)
        self.toolbtnLeft.setArrowType(Qt.LeftArrow)
        self.toolbtnRight.setArrowType(Qt.RightArrow)
        self.toolbtnLeft.setEnabled(False)
        self.toolbtnRight.setEnabled(False)
        self.navRec=0
        if (self.radiobtnName.isChecked() == True):
            cust = self.lineCustNamePhone.text()
            query = 'SELECT * FROM abcustomer WHERE name LIKE\'' + cust + "%" + "\'"
        if (self.radiobtnPhone.isChecked() == True):
            cust = self.lineCustNamePhone.text()
            query = 'SELECT * FROM abcustomer WHERE phone LIKE\'' + cust + "%" + "\'"
        if cust != "":
            self.mycursor = mydb.cursor()
            # query = 'SELECT * FROM abcustomer WHERE name LIKE\'' + name + "%" + "\'"
            self.mycursor.execute(query)
            self.custResult = self.mycursor.fetchall()
            print(self.custResult)
            if self.custResult:
                self.recCount = 0
                for x in self.custResult:
                    self.recCount += 1
                if self.recCount > 1:
                    self.toolbtnRight.setEnabled(True)
                    self.toolbtnLeft.setEnabled(False)
                    self.msg.setIcon(QMessageBox.Information)
                    self.msg.setText("Total Records found...")
                    self.msg.setInformativeText(str(self.recCount))
                    self.msg.setWindowTitle("Multiple Records Found...")
                    # self.msg.setDetailedText("The details are as follows:")
                    self.msg.setStyleSheet("color:white;background: rgb(200, 0, 0)")
                    self.msg.exec_()
                print(self.custResult[0][0])
                print(self.custResult[0][1])
                self.lblCustDisp.setText(self.custResult[0][0] + " " + self.custResult[0][1])
            else:
                self.lblCustDisp.setText("No Record Found..Try Again...")
        else:
            self.lblCustDisp.setText("No Record Found..Try Again...")

        # if (self.radiobtnPhone.isChecked() == True):
        #     self.mycursor = mydb.cursor()
        #     phone = self.lineCustNamePhone.text()
        #     query = 'SELECT * FROM abcustomer WHERE phone =\'' + phone + "\'"
        #     self.mycursor.execute(query)
        #     myresult = self.mycursor.fetchone()
        #     if myresult:
        #         self.lblCustDisp.setText(myresult[0] + " " + myresult[1])
        #     else:
        #         self.lblCustDisp.setText("No Record Found..Try Again...")

    def customerClear(self):
        self.lblCustDisp.clear()
        self.lineCustNamePhone.clear()
        self.toolbtnLeft.setEnabled(False)
        self.toolbtnRight.setEnabled(False)

    def cusRecLeft(self):
        if (self.navRec > 0):
            self.navRec -= 1
            self.toolbtnRight.setEnabled(True)
            print(self.navRec, self.recCount)
        if self.navRec==0:
            self.toolbtnLeft.setEnabled(False)
        self.lblCustDisp.setText(self.custResult[self.navRec][0] + " " + self.custResult[self.navRec][1])

    def cusRecRight(self):
        if (self.navRec < self.recCount - 1):
            self.toolbtnLeft.setEnabled(True)
            self.navRec += 1
            print(self.navRec, self.recCount)
        if self.navRec==self.recCount - 1:
            self.toolbtnRight.setEnabled(False)
        self.lblCustDisp.setText(self.custResult[self.navRec][0] + " " + self.custResult[self.navRec][1])

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                self.focusNextPrevChild(True)
        return super().event(event)

    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Escape:
            self.close()

# main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = WelcomeScreen()
    w.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
