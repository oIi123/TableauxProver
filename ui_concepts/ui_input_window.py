# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'concept1_input.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class QString(str):
    pass


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(850, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(20, 20))
        self.pushButton_3.setMaximumSize(QSize(20, 20))
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"    border-image: url(help.svg) 5 5 5 5 stretch stretch;\n"
"    background-repeat: no-repeat;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-image: url(help_hovered.png);\n"
"    background-repeat: no-repeat;\n"
"}")

        self.verticalLayout.addWidget(self.pushButton_3)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"#scrollAreaWidgetContentsSingle {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContentsSingle = QWidget()
        self.scrollAreaWidgetContentsSingle.setObjectName(u"scrollAreaWidgetContentsSingle")
        self.scrollAreaWidgetContentsSingle.setGeometry(QRect(0, 0, 798, 410))
        self.scrollArea.setWidget(self.scrollAreaWidgetContentsSingle)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab, QString())
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea_2 = QScrollArea(self.tab_2)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContentsBranch = QWidget()
        self.scrollAreaWidgetContentsBranch.setObjectName(u"scrollAreaWidgetContentsBranch")
        self.scrollAreaWidgetContentsBranch.setGeometry(QRect(0, 0, 798, 410))
        self.scrollAreaWidgetContentsBranch.setStyleSheet(u"#scrollAreaWidgetContentsBranch {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContentsBranch)

        self.verticalLayout_3.addWidget(self.scrollArea_2)

        self.tabWidget.addTab(self.tab_2, QString())

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 850, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Enter Deduction", None))
        self.pushButton_3.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Single", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Branch", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Ok", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
    # retranslateUi

