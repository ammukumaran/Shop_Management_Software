import mysql.connector
import sys
from PyQt5.QtCore import QTimer, QEvent, Qt, QSize, QDate
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, QtTest, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QMessageBox, QAction
from PyQt5.QtGui import QPixmap, QIcon

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
        home = QAction(QIcon(".\images\home.png"), "new", self)
        self.toolBarMain.addAction(home)
        logout = QAction(QIcon(".\images\logout.png"), "new", self)
        self.toolBarMain.addAction(logout)
        self.recID=0

    def gotologin(self):
        un = self.lineUser.text()
        pw = self.linePass.text()
        if un == "admin" and pw == 'admin':
            self.tabWidget.tabBar().setVisible(True)
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget.setTabVisible(0, False)
        self.mycursor = mydb.cursor()
        self.btnCustSearch.clicked.connect(self.customerSearch)
        self.btnCustClear.clicked.connect(self.customerClear)

        self.btnNewCust.clicked.connect(self.newCustTab)
        self.btnAddCust.clicked.connect(self.addCustomerFunction)
        self.btnModCust.clicked.connect(self.modifyCustomerFunction)
        self.btnDelCust.clicked.connect(self.deleteCustomerFunction)
        self.toolbtnLeft.clicked.connect(self.cusRecLeft)
        self.toolbtnRight.clicked.connect(self.cusRecRight)
        self.toolbtnCustLeft.clicked.connect(self.cusRecLeft)
        self.toolbtnCustRight.clicked.connect(self.cusRecRight)
        self.toolbtnLeft.setEnabled(False)
        self.toolbtnRight.setEnabled(False)
        self.toolbtnCustLeft.setEnabled(False)
        self.toolbtnCustRight.setEnabled(False)
        self.btnCusDatetClear.clicked.connect(self.customerClear)

        # self.mycursor.execute("SELECT * FROM abcustomer")
        #
        # myresult = self.mycursor.fetchall()
        #
        # for x in myresult:
        #     print(x)

    def newCustTab(self):
        self.tabWidget.setCurrentIndex(2)
        self.dtDOB.setDate(QDate.currentDate())

    def customerSearch(self):
        self.navRec = 0
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
                    self.toolbtnCustRight.setEnabled(True)
                    self.toolbtnCustLeft.setEnabled(False)
                    self.msg.setIcon(QMessageBox.Information)
                    self.msg.setText("Total Records found...")
                    self.msg.setInformativeText(str(self.recCount))
                    self.msg.setWindowTitle("Multiple Records Found...")
                    self.msg.setStandardButtons(QMessageBox.Ok)
                    # self.msg.setDetailedText("The details are as follows:")
                    self.msg.setStyleSheet("color:white;background: rgb(200, 0, 0)")
                    self.msg.exec_()
                self.lblCustDisp.setText(self.custResult[0][0] + " | " + self.custResult[0][1])
                self.lineName.setText(self.custResult[0][0])
                self.linePhone.setText(self.custResult[0][1])
                self.lineApt.setText(self.custResult[0][2])
                self.lineCity.setText(self.custResult[0][3])
                self.recID=self.custResult[0][5]
                print(type(self.recID), self.recID)
                if self.custResult[0][4] != None:
                    self.dtDOB.setDate(QtCore.QDate.fromString(self.custResult[0][4], "yyyy-MM-d"))
                else:
                    self.dtDOB.setDate(QtCore.QDate.fromString("1-Jan-2000", "d-MMM-yyyy"))
                self.labelHomeRecord.setText('Record '+str(self.navRec+1)+" of "+str(self.recCount))
                self.labelCustRecord.setText('Record ' + str(self.navRec + 1) + " of " + str(self.recCount))
            else:
                self.lblCustDisp.setText("No Record Found..Try Again...")
                self.labelHomeRecord.setText("")
                self.recID = 0
                self.toolbtnRight.setEnabled(False)
                self.toolbtnLeft.setEnabled(False)
                self.toolbtnCustRight.setEnabled(False)
                self.toolbtnCustLeft.setEnabled(False)
                self.lineName.clear()
                self.linePhone.clear()
                self.lineApt.clear()
                self.lineCity.clear()
                self.lblCustStatus.clear()
                date_str = "1-Jan-2000"
                qdate = QtCore.QDate.fromString(date_str, "d-MMM-yyyy")
                self.dtDOB.setDate(qdate)
                self.navRec = 0
        else:
            self.lblCustDisp.setText("No Record Found..Try Again...")
            self.labelHomeRecord.setText("")
            self.recID = 0
            self.toolbtnRight.setEnabled(False)
            self.toolbtnLeft.setEnabled(False)
            self.toolbtnCustRight.setEnabled(False)
            self.toolbtnCustLeft.setEnabled(False)
            self.lineName.clear()
            self.linePhone.clear()
            self.lineApt.clear()
            self.lineCity.clear()
            self.lblCustStatus.clear()
            date_str = "1-Jan-2000"
            qdate = QtCore.QDate.fromString(date_str, "d-MMM-yyyy")
            self.dtDOB.setDate(qdate)
            self.navRec = 0

    def customerClear(self):
        self.lblCustDisp.clear()
        self.lineCustNamePhone.clear()
        self.toolbtnLeft.setEnabled(False)
        self.toolbtnRight.setEnabled(False)
        self.toolbtnCustLeft.setEnabled(False)
        self.toolbtnCustRight.setEnabled(False)
        self.lineName.clear()
        self.linePhone.clear()
        self.lineApt.clear()
        self.lineCity.clear()
        self.lblCustStatus.clear()
        date_str="1-Jan-2000"
        qdate = QtCore.QDate.fromString(date_str, "d-MMM-yyyy")
        self.dtDOB.setDate(qdate)
        self.navRec = 0
        self.labelHomeRecord.clear()
        self.labelCustRecord.clear()
        self.recID = 0
        print(self.recID)

    def cusRecLeft(self):
        if (self.navRec > 0):
            self.navRec -= 1
            self.toolbtnRight.setEnabled(True)
            self.toolbtnCustRight.setEnabled(True)
            print(self.navRec, self.recCount)
        if self.navRec == 0:
            self.toolbtnLeft.setEnabled(False)
            self.toolbtnCustLeft.setEnabled(False)
        self.lblCustDisp.setText(self.custResult[self.navRec][0] + " | " + self.custResult[self.navRec][1])
        self.lineName.setText(self.custResult[self.navRec][0])
        self.linePhone.setText(self.custResult[self.navRec][1])
        self.lineApt.setText(self.custResult[self.navRec][2])
        self.lineCity.setText(self.custResult[self.navRec][3])
        if self.custResult[self.navRec][4] != None:
            self.dtDOB.setDate(QtCore.QDate.fromString(self.custResult[self.navRec][4], "yyyy-MM-d"))
        else:
            self.dtDOB.setDate(QtCore.QDate.fromString("1-Jan-2000", "d-MMM-yyyy"))
        self.labelHomeRecord.setText('Record ' + str(self.navRec + 1) + " of " + str(self.recCount))
        self.labelCustRecord.setText('Record ' + str(self.navRec + 1) + " of " + str(self.recCount))
        self.recID = self.custResult[self.navRec][5]
        print(self.recID)


    def cusRecRight(self):
        if (self.navRec < self.recCount - 1):
            self.toolbtnLeft.setEnabled(True)
            self.toolbtnCustLeft.setEnabled(True)
            self.navRec += 1
            print(self.navRec, self.recCount)
        if self.navRec == self.recCount - 1:
            self.toolbtnRight.setEnabled(False)
            self.toolbtnCustRight.setEnabled(False)
        self.lblCustDisp.setText(self.custResult[self.navRec][0] + " | " + self.custResult[self.navRec][1])
        self.lineName.setText(self.custResult[self.navRec][0])
        self.linePhone.setText(self.custResult[self.navRec][1])
        self.lineApt.setText(self.custResult[self.navRec][2])
        self.lineCity.setText(self.custResult[self.navRec][3])
        if self.custResult[self.navRec][4] != None:
            self.dtDOB.setDate(QtCore.QDate.fromString(self.custResult[self.navRec][4], "yyyy-MM-d"))
        else:
            self.dtDOB.setDate(QtCore.QDate.fromString("1-Jan-2000", "d-MMM-yyyy"))
        self.labelHomeRecord.setText('Record ' + str(self.navRec + 1) + " of " + str(self.recCount))
        self.labelCustRecord.setText('Record ' + str(self.navRec + 1) + " of " + str(self.recCount))
        self.recID = self.custResult[self.navRec][5]
        print (self.recID)

    def addCustomerFunction(self):
        name = self.lineName.text()
        phone = self.linePhone.text()
        apartment = self.lineApt.text()
        city = self.lineCity.text()
        dob = (self.dtDOB.date().toPyDate()).strftime('%Y-%m-%d')

        if len(name) == 0 or len(phone) == 0:
            # self.error.setText("Please fill in all inputs.")
            pass
        else:
            query = 'SELECT * FROM abcustomer WHERE phone =\'' + phone + "\'"
            self.mycursor.execute(query)
            myresult = self.mycursor.fetchall()
            flag=0
            if myresult:
                record=0
                for x in myresult:
                    record += 1
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.setText("Multiple Record exists. Do you want to add as new entry?")
                self.msg.setInformativeText(str(record)+' records with same phone no')
                self.msg.setWindowTitle("Add Customer Warning")
                # Add buttons and set default
                self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                self.msg.setDefaultButton(QMessageBox.No)
                self.msg.setStyleSheet("color:white;background: rgb(200, 0, 0)")
                btn=self.msg.exec_()
                if self.msg.clickedButton() is self.msg.button(QMessageBox.No):
                    flag=1
            if flag==0:
                print (name,phone,apartment,city,dob)
                user_info = [name,phone,apartment,city,dob]
                self.mycursor.execute("INSERT INTO abcustomer (name,phone,apartment,city,dob) VALUES (%s,%s,%s,%s,%s)",
                                      user_info)
                mydb.commit()
                self.lblCustStatus.setText("Record inserted successfully")

    def modifyCustomerFunction(self):
        name = self.lineName.text()
        phone = self.linePhone.text()
        apartment = self.lineApt.text()
        city = self.lineCity.text()
        dob = (self.dtDOB.date().toPyDate()).strftime('%Y-%m-%d')
        user_info = [name, phone, apartment, city, dob,self.recID]
        print(user_info)
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Are you sure you want to ")
        self.msg.setInformativeText("update?")
        self.msg.setWindowTitle("Modify Customer Warning")
        # Add buttons and set default
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.msg.setDefaultButton(QMessageBox.No)
        self.msg.setStyleSheet("color:white;background: rgb(200, 0, 0)")
        btn = self.msg.exec_()
        if self.msg.clickedButton() is self.msg.button(QMessageBox.Yes):
            self.mycursor.execute("UPDATE abcustomer SET name=%s,phone=%s,apartment=%s,city=%s,dob=%s WHERE cust_id = %s",
                              user_info)
            mydb.commit()
            self.lblCustStatus.setText("Record modified successfully")

    def deleteCustomerFunction(self):
        print(self.recID)
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Are you sure you want to ")
        self.msg.setInformativeText("delete permanently?")
        self.msg.setWindowTitle("Delete Customer Warning")
        # Add buttons and set default
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.msg.setDefaultButton(QMessageBox.No)
        self.msg.setStyleSheet("color:white;background: rgb(200, 0, 0)")
        btn = self.msg.exec_()
        if self.msg.clickedButton() is self.msg.button(QMessageBox.Yes):
            rec = (self.recID,)
            self.mycursor.execute(
                "DELETE FROM abcustomer WHERE cust_id = %s",rec)
            mydb.commit()
            self.lblCustStatus.setText("Record deleted successfully")


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
