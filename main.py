import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget,  QScrollArea, QMessageBox, QLineEdit
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream, QPropertyAnimation
from PyQt5 import QtGui, QtCore
import pyodbc
from ui import Ui_MainWindow
import time
#Test Change in Git
# Setting to connect SQL Server
driver = "{ODBC Driver 17 for SQL Server}"
server = "223.18.195.32,1433\DESKTOP-AUXISYS\MSSQL2022"
database = "MainDB"
username = "sa"
password = ">>>>>>>>>>>>>>>>>>>>>>>>>>>INPUT THE CORUSE CODE IN UPPERCASE (5 DIGITS)<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"

mysid = "This Place Store the SID of logged In Account"
mypw = "pw"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(100, 100, 1200, 800)

        #self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.Stack.setCurrentIndex(0)
        self.ui.SstackedWidget.setCurrentIndex(2)
        #self.ui.home_btn_2.setChecked(True)
        
        #Top
        self.ui.menu_button.clicked.connect(lambda: self.slideLeftMenu())
        self.ui.Refresh_button.clicked.connect(lambda: self.refresh())
        self.ui.Update_button.clicked.connect(lambda: self.update())
        self.ui.Add_button.clicked.connect(lambda: self.add())
        self.ui.setting_button.clicked.connect(self.tsett)

        #Menu
        self.ui.student_record_button.clicked.connect(self.stdrec)
        self.ui.class_record_button.clicked.connect(self.clsrec)
        self.ui.year_record_button.clicked.connect(self.yrrec)
        self.ui.menu_logout_button.clicked.connect(lambda:self.ui.Stack.setCurrentWidget(self.ui.LoginPage))
                

        #Smenu

        self.ui.Smenu_button.clicked.connect(lambda: self.SslideLeftMenu())
        self.ui.student_info.clicked.connect(self.info)
        self.ui.Chanpw_button_2.clicked.connect(self.chanpw)
        self.ui.assn_button_2.clicked.connect(self.assn)
        self.ui.acd_button_3.clicked.connect(self.acd)
        self.ui.Smenu_logout_button_2.clicked.connect(lambda:self.ui.Stack.setCurrentWidget(self.ui.LoginPage))

        #logout
        self.ui.sleaveButton.clicked.connect(lambda:self.ui.Stack.setCurrentWidget(self.ui.LoginPage))
        self.ui.Logout_bt_2.clicked.connect(lambda:self.ui.Stack.setCurrentWidget(self.ui.LoginPage))
        self.ui.tleaveButton.clicked.connect(lambda:self.ui.Stack.setCurrentWidget(self.ui.LoginPage))
        self.ui.Logout_bt.clicked.connect(lambda:self.ui.Stack.setCurrentWidget(self.ui.LoginPage))
        
        
        #SPage

        self.ui.StudentInfoBt.clicked.connect(self.info)
        self.ui.ChanpwButton.clicked.connect(self.chanpw)
        self.ui.AssnResButton.clicked.connect(self.assn)
        self.ui.acedemicButton.clicked.connect(self.acd)
        self.ui.ssetting_button.clicked.connect(self.sett)
        self.ui.setting_button_2.clicked.connect(self.sett)

        #TPage
        self.ui.tsettings_button.clicked.connect(self.tsett)
        self.ui.StudentsButton_1.clicked.connect(self.stdrec)
        self.ui.clButton.clicked.connect(self.clsrec)
        self.ui.yrButton_2.clicked.connect(self.yrrec)

        #login
        self.ui.tlogin_bt_2.clicked.connect(lambda:self.ui.Stack.setCurrentWidget(self.ui.TeacherLogin_Page))
        self.ui.backbt.clicked.connect(lambda:self.ui.Stack.setCurrentWidget(self.ui.LoginPage))
        self.ui.forget_pw_bt.clicked.connect(self.ForgetPw)
        self.ui.forget_pw_bt_3.clicked.connect(self.ForgetPw)

        #Ssetting
        self.ui.update_button_2.clicked.connect(self.showVersion)
        self.ui.eng_bt.setChecked(True)
        self.ui.cht_bt.clicked.connect(self.funcNo)

        #Tsetting
        self.ui.update_button.clicked.connect(self.showVersion)
        self.ui.eng_bt_2.setChecked(True)
        self.ui.cht_bt_2.clicked.connect(self.funcNo)
        
        #Login Func
        self.ui.Sedit_button.clicked.connect(lambda: self.SMenu())
        self.ui.login_bt.clicked.connect(self.login)
        self.ui.tlogin_bt.clicked.connect(self.tlogin)
        # Connect the change_password method to the change button
        self.ui.Change_bt.clicked.connect(self.change_password)

        #load table
        self.ui.SearchInput.textChanged.connect(self.filter_table)
        self.populate_table()
        self.class_table()
        self.year_table()


    def showVersion(self):
        QMessageBox.warning(self, "Update Checked", "This software is now up-to-date!")

    def funcNo(self):
        QMessageBox.warning(self, "Function Unable", "This function not yet developed!")

    def ForgetPw(self):
        QMessageBox.warning(self, "Help!", "Please contact E-mail: jauyeung@hkmu.edu.hk! or Phone: 3120-2606 ")

    def info(self):
        self.ui.Stack.setCurrentWidget(self.ui.Student)
        self.ui.SstackedWidget.setCurrentIndex(0)
    
    def chanpw(self):
            self.ui.Stack.setCurrentWidget(self.ui.Student)
            self.ui.SstackedWidget.setCurrentIndex(1)

    def assn(self):
            self.ui.Stack.setCurrentWidget(self.ui.Student)
            self.ui.SstackedWidget.setCurrentIndex(2)

    def acd(self):
            self.ui.Stack.setCurrentWidget(self.ui.Student)
            self.ui.SstackedWidget.setCurrentIndex(3)

    def sett(self):
            self.ui.Stack.setCurrentWidget(self.ui.Student)
            self.ui.SstackedWidget.setCurrentIndex(4)
    
    def stdrec(self):
            self.ui.Stack.setCurrentWidget(self.ui.Teacher)
            self.ui.stackedWidget.setCurrentIndex(0)

    def clsrec(self):
            self.ui.Stack.setCurrentWidget(self.ui.Teacher)
            self.ui.stackedWidget.setCurrentIndex(1)

    def yrrec(self):
            self.ui.Stack.setCurrentWidget(self.ui.Teacher)
            self.ui.stackedWidget.setCurrentIndex(2)

    def tsett(self):
            self.ui.Stack.setCurrentWidget(self.ui.Teacher)
            self.ui.stackedWidget.setCurrentIndex(3)

    def refresh(self):
        # Clear the table
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        # Repopulate the table
        self.populate_table()
        
        print("The table is refreshed!")
            
    def add(self):
        conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
        cursor = conn.cursor()
        sql = "Insert into StuRec (SID) Values ('Input SID')"
        cursor.execute(sql)
        cursor.commit()
        # Clear the table
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        # Repopulate the table
        self.populate_table()
        print("The table is refleshed!")
        
    def filter_table(self):
        filter_text = self.ui.SearchInput.text()
        for row in range(self.ui.tableWidget.rowCount()):
            should_show = False
            for column in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.item(row, column)
                if item is not None:
                    if filter_text.lower() in item.text().lower():
                        should_show = True
                        break
            
            self.ui.tableWidget.setRowHidden(row, not should_show)

    def update(self):
        # Get the number of rows and columns in the table
        row_count = self.ui.tableWidget.rowCount()
        column_count = self.ui.tableWidget.columnCount()

        # Connect to the database
        conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
        cursor = conn.cursor()

        # Get column names
        column_names = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(column_count-1)]
        print(column_names[1:])

        # Iterate over each row
        for i in range(row_count):
            # Get the values in the row
            values = []
            for j in range(column_count-1):
                item = self.ui.tableWidget.item(i, j)
                if item is not None:
                    values.append(item.text())
                else:
                    values.append('None')


            try:
                sql = "UPDATE StuRec SET " + ", ".join(f"[{name}] = ?" for name in column_names[1:]) + " WHERE [" + column_names[0] + "] = ?"
                cursor.execute(sql, *(values[1:] + [values[0]]))
                sql = "DELETE FROM StuRec WHERE SID = 'del'"
                cursor.execute(sql)
                cursor.commit()
            except Exception as e:
                crash=["Error on line {}".format(sys.exc_info()[-1].tb_lineno),"\n",e]
                print(crash)
                timeX=str(time.time())
                with open("crash_log/crashlog-"+timeX+".txt","w") as crashLog:
                    for i in crash:
                        i=str(i)
                        crashLog.write(i)
                exit()


            
        
        # Commit the changes and close the connection
        conn.commit()
        print("Change has been made")
        # conn.close()
        # Clear the table
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        
        # Repopulate the table
        self.populate_table()
        print("The table is refreshed!")

    #teacherslide
    def slideLeftMenu(self):
        width = self.ui.Slide_menu_ct.width()
        
        if width ==0:
            newWidth = 200
            self.ui.menu_button.setIcon(QtGui.QIcon(u":/SVG/SVG/menu, more, detail, list, interface.svg"))
        else:
            newWidth = 0
            self.ui.menu_button.setIcon(QtGui.QIcon(u":/SVG/SVG/menu, more, detail, list, interface.svg"))

        self.animation = QPropertyAnimation(self.ui.Slide_menu_ct, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    #studentslide
    def SslideLeftMenu(self):
        width = self.ui.Sside_menu_ct.width()
        
        if width ==0:
            newWidth = 200
            self.ui.Smenu_button.setIcon(QtGui.QIcon(u":/SVG/SVG/menu, more, detail, list, interface.svg"))
        else:
            newWidth = 0
            self.ui.Smenu_button.setIcon(QtGui.QIcon(u":/SVG/SVG/menu, more, detail, list, interface.svg"))

        self.animation = QPropertyAnimation(self.ui.Sside_menu_ct, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def populate_table(self):
        conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
        cursor = conn.cursor()
        table_name = "StuRec"
        #sql = f"SELECT * FROM {table_name} where SID LIKE '%"+mysid+"%'"
        sql = f"SELECT * FROM {table_name}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        column_count = len(cursor.description)
        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.setColumnCount(column_count+1)
        
        # Put Label Names to Table
        column_names = [column[0] for column in cursor.description]
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)

        # Put Label Names to Table
        column_names = [column[0] for column in cursor.description]
        column_names.append("Avg Marks")
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)
        
        # Input SQL value to Table Cell
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget.setItem(i, j, item)


         # Cal Avg Marks
         # Iterate over each row
        row_count = self.ui.tableWidget.rowCount()
        for i in range(row_count):
             # Get the values in the row
            score = []
            for j in range(3,column_count):
                item = self.ui.tableWidget.item(i, j)
                if item is not None:
                    score.append(item.text())
                else:
                    score.append('None')
            print(score)
            try:
                AvgMarks=(float(score[0])+float(score[1]))/2
                self.ui.tableWidget.setItem(i, column_count, QTableWidgetItem(str(AvgMarks)))
                self.ui.label.setText("Total="+str(row_count))
                self.ui.label.adjustSize()
            except Exception as e:
                self.ui.tableWidget.setItem(i, column_count, QTableWidgetItem(str("Error")))
                crash=["Error on line {}".format(sys.exc_info()[-1].tb_lineno),"\n",e]
                print(crash)
                timeX=str(time.time())
                with open("crash_log/crashlog-"+timeX+".txt","w") as crashLog:
                    for i in crash:
                        i=str(i)
                        crashLog.write(i)

        self.ui.tableWidget.setSortingEnabled(True)          
        self.ui.tableWidget.resizeColumnsToContents()

    
    def class_table(self):
        conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
        cursor = conn.cursor()
        table_name = "Class"
        sql = f"SELECT * FROM {table_name}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        column_count = len(cursor.description)
        self.ui.Class_table.setRowCount(len(rows))
        self.ui.Class_table.setColumnCount(column_count)
        
        # Put Label Names to Table
        column_names = [column[0] for column in cursor.description]
        self.ui.Class_table.setHorizontalHeaderLabels(column_names)
        
        # Input SQL value to Table Cell
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.ui.Class_table.setItem(i, j, item)
        self.ui.Class_table.setSortingEnabled(True)    
        self.ui.Class_table.resizeColumnsToContents()
    

    def year_table(self):
        conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
        cursor = conn.cursor()
        table_name = "Year"
        sql = f"SELECT * FROM {table_name}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        column_count = len(cursor.description)
        self.ui.Year_table.setRowCount(len(rows))
        self.ui.Year_table.setColumnCount(column_count)
        
        # Put Label Names to Table
        column_names = [column[0] for column in cursor.description]
        self.ui.Year_table.setHorizontalHeaderLabels(column_names)
        
        # Input SQL value to Table Cell
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.ui.Year_table.setItem(i, j, item)
        self.ui.Year_table.setSortingEnabled(True)    
        self.ui.Year_table.resizeColumnsToContents()

    def login(self):
        conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
        cursor = conn.cursor()

        # Get the entered username and password
        ssid = self.ui.input_usname.text()
        pw = self.ui.input_pw.text()

        # Retrieve the SID and password from the database based on the entered username
        query = "SELECT [Student Name], [Email], [Phone Number], [GPA], [CGPA], SID, pw FROM StuRec WHERE SID = ? AND pw = ?"
        cursor.execute(query, (ssid,pw))
        result = cursor.fetchone()
        
        if result is not None:
            student, email, phone, gpa, cgpa, db_sid, db_pw = result

            student_name = result[0]
            self.ui.SName.setText(student_name)
            self.ui.SName.show()

            self.ui.sssidd.setText(db_sid)
            self.ui.sssidd.show()

            self.ui.emaill.setText(email)
            self.ui.emaill.show()

            self.ui.Phonn.setText(phone)
            self.ui.Phonn.show()

            self.ui.GPPA.setText(gpa)
            self.ui.GPPA.show()

            self.ui.CGGPA.setText(cgpa)
            self.ui.CGGPA.show()

            if db_pw.replace(" ", "") == pw.replace(" ", ""):
                # Login successful
                self.mysid = db_sid  # Set the SID for further use
                self.ui.Stack.setCurrentWidget(self.ui.HomePage_S)
                self.mypw = db_pw
            else:
                # Incorrect password
                QMessageBox.warning(self, "Login Failed", "Incorrect password.")
        else:
            # User not found
            QMessageBox.warning(self, "Login Failed", "User not found.")

    def change_password(self):
        # Get the current SID and password
        current_sid = self.ui.sssidd.text()
        current_pw = self.ui.input_pw.text()

        # Get the new password and retype password
        new_pw = self.ui.newpw.text()
        retype_pw = self.ui.retypepw.text()

        if new_pw == retype_pw:
            conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
            cursor = conn.cursor()

            # Update the password in the database
            update_query = "UPDATE StuRec SET pw = ? WHERE SID = ? AND pw = ?"
            cursor.execute(update_query, (new_pw, current_sid, current_pw))
            conn.commit()

            # Check if the password was successfully updated
            if cursor.rowcount > 0:
                QMessageBox.information(self, "Password Updated", "Password successfully changed.")
                self.ui.input_pw.setText("")  # Clear the current password input
                self.ui.newpw.setText("")  # Clear the new password input
                self.ui.retypepw.setText("")  # Clear the retype password input
            else:
                QMessageBox.warning(self, "Password Update Failed", "Failed to update password.")

            cursor.close()
            conn.close()
        else:
            QMessageBox.warning(self, "Password Update Failed", "New passwords do not match.")

    def tlogin(self):
        conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
        cursor = conn.cursor()

        # Get the entered username and password
        tsid = self.ui.t_user.text()
        tpw = self.ui.t_pw.text()

        # Retrieve the SID and password from the database based on the entered username
        teach_query = "SELECT TID, PW FROM Table_TID WHERE TID = ? AND PW = ?"
        cursor.execute(teach_query, (tsid,tpw))
        tresult = cursor.fetchone()

        
        if tresult is not None:
            db_tid, db_pw = tresult

            if db_tid.replace(" ", "") != tsid.replace(" ", ""):
                QMessageBox.warning(self, "Login Failed", "User not found.")

            elif db_pw.replace(" ", "") == tpw.replace(" ", ""):
                # Login successful
                self.mysid = db_tid  # Set the SID for further use
                self.ui.Stack.setCurrentWidget(self.ui.HomePage_T)
            else:
                # Incorrect password
                QMessageBox.warning(self, "Login Failed", "Incorrect password.")
        else:
            # User not found
            QMessageBox.warning(self, "Login Failed", "Empty Input.")
        
    def SMenu(self):
        width = self.ui.SRecordMenu.width()
        if width ==0:
            newWidth = 200
            self.ui.Sedit_button.setIcon(QtGui.QIcon(u":/SVG/SVG/pen, edit, pencil, write, stationery.svg"))

        else:
            newWidth = 0
            self.ui.Sedit_button.setIcon(QtGui.QIcon(u":/SVG/SVG/pen, edit, pencil, write, stationery.svg"))

        self.animation = QPropertyAnimation(self.ui.SRecordMenu, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())





