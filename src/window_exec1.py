# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window_exec1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(917, 538)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(50, 90, 171, 41))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(570, 60, 311, 391))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(290, 10, 271, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(50, 50, 51, 31))
        self.label_2.setObjectName("label_2")
        self.historyDate = QtWidgets.QDateEdit(Form)
        self.historyDate.setGeometry(QtCore.QRect(99, 50, 121, 31))
        self.historyDate.setObjectName("historyDate")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.pushButton_click)
        self.historyDate.dateChanged['QDate'].connect(Form.date_init)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "获取历史数据"))
        self.label.setText(_translate("Form", "股票分析工具"))
        self.label_2.setText(_translate("Form", "日期"))
