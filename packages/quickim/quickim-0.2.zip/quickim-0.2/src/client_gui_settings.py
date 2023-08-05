# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from config import *


class Ui_Form(object):
    """
    Класс описывающий GUI окна подключения
    """
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.resize(257, 189)
        self.StatusLabel = QtWidgets.QLabel(Form)
        self.StatusLabel.setGeometry(QtCore.QRect(10, 170, 241, 16))
        self.StatusLabel.setObjectName("StatusLabel")
        self.WelcomeLabel = QtWidgets.QLabel(Form)
        self.WelcomeLabel.setGeometry(QtCore.QRect(80, 0, 101, 16))
        self.WelcomeLabel.setObjectName("WelcomeLabel")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 231, 134))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LoginLabel = QtWidgets.QLabel(self.layoutWidget)
        self.LoginLabel.setMaximumSize(QtCore.QSize(50, 16777215))
        self.LoginLabel.setToolTipDuration(-1)
        self.LoginLabel.setObjectName("LoginLabel")
        self.horizontalLayout.addWidget(self.LoginLabel)
        self.LoginLine = QtWidgets.QLineEdit(self.layoutWidget)
        self.LoginLine.setMaximumSize(QtCore.QSize(120, 20))
        self.LoginLine.setObjectName("LoginLine")
        self.horizontalLayout.addWidget(self.LoginLine)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pwdLabel = QtWidgets.QLabel(self.layoutWidget)
        self.pwdLabel.setMaximumSize(QtCore.QSize(50, 50))
        self.pwdLabel.setObjectName("pwdLabel")
        self.horizontalLayout_2.addWidget(self.pwdLabel)
        self.PwdLine = QtWidgets.QLineEdit(self.layoutWidget)
        self.PwdLine.setMaximumSize(QtCore.QSize(120, 20))
        self.PwdLine.setInputMethodHints(
            QtCore.Qt.ImhHiddenText | QtCore.Qt.ImhNoAutoUppercase | QtCore.Qt.ImhNoPredictiveText | QtCore.Qt.ImhSensitiveData)
        self.PwdLine.setText("")
        self.PwdLine.setMaxLength(20)
        self.PwdLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PwdLine.setObjectName("PwdLine")
        self.horizontalLayout_2.addWidget(self.PwdLine)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.PwdSaveCheckBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.PwdSaveCheckBox.setMaximumSize(QtCore.QSize(100, 20))
        self.PwdSaveCheckBox.setObjectName("PwdSaveCheckBox")
        self.verticalLayout.addWidget(self.PwdSaveCheckBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ServAddrLabel = QtWidgets.QLabel(self.layoutWidget)
        self.ServAddrLabel.setMaximumSize(QtCore.QSize(80, 20))
        self.ServAddrLabel.setObjectName("ServAddrLabel")
        self.horizontalLayout_3.addWidget(self.ServAddrLabel)
        self.ServAddrLine = QtWidgets.QLineEdit(self.layoutWidget)
        self.ServAddrLine.setMaximumSize(QtCore.QSize(100, 20))
        self.ServAddrLine.setObjectName("ServAddrLine")
        self.horizontalLayout_3.addWidget(self.ServAddrLine)
        self.ServAddrPort = QtWidgets.QLineEdit(self.layoutWidget)
        self.ServAddrPort.setMaximumSize(QtCore.QSize(35, 20))
        self.ServAddrPort.setMaxLength(5)
        self.ServAddrPort.setObjectName("ServAddrPort")
        self.horizontalLayout_3.addWidget(self.ServAddrPort)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ExitButton = QtWidgets.QPushButton(self.layoutWidget)
        self.ExitButton.setMaximumSize(QtCore.QSize(50, 25))
        self.ExitButton.setObjectName("ExitButton")
        self.horizontalLayout_4.addWidget(self.ExitButton)
        self.ConnectButton = QtWidgets.QPushButton(self.layoutWidget)
        self.ConnectButton.setMaximumSize(QtCore.QSize(16777215, 25))
        self.ConnectButton.setObjectName("ConnectButton")
        self.horizontalLayout_4.addWidget(self.ConnectButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        self.ConnectButton.clicked.connect(self.StatusLabel.update)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Connection"))
        self.StatusLabel.setText(_translate("Form", "Статус: Отключено"))
        self.WelcomeLabel.setText(_translate("Form", "Добро пожаловать! "))
        self.LoginLabel.setText(_translate("Form", "Login:"))
        self.pwdLabel.setText(_translate("Form", "Password:"))
        self.PwdSaveCheckBox.setText(_translate("Form", "Save password"))
        self.ServAddrLabel.setText(_translate("Form", "Server address:"))
        self.ServAddrLine.setText(_translate("Form", "127.0.0.1"))
        self.ServAddrPort.setText(_translate("Form", "7777"))
        self.ExitButton.setText(_translate("Form", "Exit"))
        self.ConnectButton.setText(_translate("Form", "Connect"))


class AddContactDialog(QtWidgets.QDialog):
    """
    Класс описывающий GUI окна добавления контакта
    """
    def __init__(self):
        super(AddContactDialog, self).__init__()
        self.ui = uic.loadUi('add_contact.ui', self)
        self.initUI()

    def initUI(self):
        self.ui.buttonBox.rejected.connect(self.close)


class DelContactDialog(QtWidgets.QDialog):
    """
    Класс описывающий GUI окна удаления контакта
    """
    def __init__(self):
        super(DelContactDialog, self).__init__()
        self.ui = uic.loadUi('del_contact.ui', self)
        self.initUI()

    def initUI(self):
        self.ui.del_form_buttonBox.rejected.connect(self.close)
