# Form implementation generated from reading ui file 'calc.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(742, 498)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 30, 511, 421))
        self.listWidget.setObjectName("listWidget")
        self.pushButton_calcukate = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_calcukate.setGeometry(QtCore.QRect(560, 30, 141, 41))
        self.pushButton_calcukate.setObjectName("pushButton_calcukate")
        self.pushButton_back = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(560, 410, 141, 41))
        self.pushButton_back.setObjectName("pushButton_back")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_calcukate.setText(_translate("MainWindow", "Расчитать материал"))
        self.pushButton_back.setText(_translate("MainWindow", "Назад"))
