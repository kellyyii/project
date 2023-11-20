import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget,  QScrollArea
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream, QPropertyAnimation
from PyQt5 import QtGui, QtCore
import pyodbc
from ui import Ui_MainWindow
#Test Change in Git
# Setting to connect SQL Server
driver = "{ODBC Driver 17 for SQL Server}"
server = "LALALA"
database = "SQL_test"
username = "sa"
password = "wl8933SK"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(100, 100, 1200, 800)

        #self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        #self.ui.home_btn_2.setChecked(True)
        
        #Top
        self.ui.menu_button.clicked.connect(lambda: self.slideLeftMenu())
        self.ui.Refresh_button.clicked.connect(lambda: self.refresh())
        self.ui.Update_button.clicked.connect(lambda: self.update())
        self.ui.Add_button.clicked.connect(lambda: self.add())
        self.ui.setting_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.SettingPage))

        #Menu
        self.ui.student_record_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.SRecordPage))
        self.ui.class_record_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.CRecordPage))
        self.ui.year_record_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.YRecordPage))
        self.ui.menu_logout_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.LoginPage))
        
        #SPage
        self.ui.Sedit_button.clicked.connect(lambda: self.SMenu())

        self.populate_table()

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
        sql = "Insert into Table_1 (Name) Values ('')"
        cursor.execute(sql)
        cursor.commit()
        # Clear the table
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        # Repopulate the table
        self.populate_table()
        print("The table is refleshed!")
        
    def update(self):
        # Get the number of rows and columns in the table
        row_count = self.ui.tableWidget.rowCount()
        column_count = self.ui.tableWidget.columnCount()

        # Connect to the database
        conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
        cursor = conn.cursor()

        # Get column names
        column_names = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(column_count-1)]

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
            print(values)
            # Update the row in the database
            # Assuming the first column is the ID column
            sql = "UPDATE Table_1 SET " + ", ".join(f"{name} = ?" for name in column_names[1:]) + " WHERE " + column_names[0] + " = ?"
            cursor.execute(sql, *(values[1:] + [values[0]]))
            sql = "DELETE FROM Table_1 WHERE Name = 'del'"
            cursor.execute(sql)
            cursor.commit()
        
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

    def populate_table(self):
        conn = pyodbc.connect("DRIVER="+driver+";SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)
        cursor = conn.cursor()
        table_name = "Table_1"
        sql = f"SELECT * FROM {table_name} where SID LIKE '%"+mysid+"%'"
        #sql = f"SELECT * FROM {table_name}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        column_count = len(cursor.description)
        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.setColumnCount(column_count)
        
        # Put Label Names to Table
        column_names = [column[0] for column in cursor.description]
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)
        
        # Input SQL value to Table Cell
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget.setItem(i, j, item)
        self.ui.tableWidget.resizeColumnsToContents()
        
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
