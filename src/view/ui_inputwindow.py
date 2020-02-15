# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'inputwindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(852, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.help_btn = QPushButton(self.centralwidget)
        self.help_btn.setObjectName(u"help_btn")
        self.help_btn.setMinimumSize(QSize(25, 25))
        self.help_btn.setMaximumSize(QSize(25, 25))
        self.help_btn.setStyleSheet(u"QPushButton {\n"
"    qproperty-icon: url(src/view/images/help.svg);\n"
"}")
        self.help_btn.setIconSize(QSize(23, 23))

        self.verticalLayout.addWidget(self.help_btn)

        self.tab_bar = QTabWidget(self.centralwidget)
        self.tab_bar.setObjectName(u"tab_bar")
        self.tab_bar.setStyleSheet(u"#scrollAreaContentsBranch {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.single_tab = QWidget()
        self.single_tab.setObjectName(u"single_tab")
        self.verticalLayout_2 = QVBoxLayout(self.single_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.single_tab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"#scrollAreaContentsSingle {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContentsSingle = QWidget()
        self.scrollAreaContentsSingle.setObjectName(u"scrollAreaContentsSingle")
        self.scrollAreaContentsSingle.setGeometry(QRect(0, 0, 808, 431))
        self.scrollAreaContentsSingle.setAutoFillBackground(False)
        self.scrollAreaContentsSingle.setStyleSheet(u"#scrollAreaWidgetContents {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.deduction_single_left = QTextEdit(self.scrollAreaContentsSingle)
        self.deduction_single_left.setObjectName(u"deduction_single_left")
        self.deduction_single_left.setGeometry(QRect(225, 135, 165, 200))
        self.deduction_single_left.setStyleSheet(u"")
        self.deduction_single_right = QTextEdit(self.scrollAreaContentsSingle)
        self.deduction_single_right.setObjectName(u"deduction_single_right")
        self.deduction_single_right.setGeometry(QRect(410, 135, 165, 200))
        self.deduction_single_right.setStyleSheet(u"")
        self.scrollArea.setWidget(self.scrollAreaContentsSingle)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.tab_bar.addTab(self.single_tab, "")
        self.branch_tab = QWidget()
        self.branch_tab.setObjectName(u"branch_tab")
        self.verticalLayout_3 = QVBoxLayout(self.branch_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea_2 = QScrollArea(self.branch_tab)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaContentsBranch = QWidget()
        self.scrollAreaContentsBranch.setObjectName(u"scrollAreaContentsBranch")
        self.scrollAreaContentsBranch.setGeometry(QRect(0, 0, 808, 431))
        self.scrollAreaContentsBranch.setStyleSheet(u"#scrollAreaWidgetContentsBranch {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.deduction_branch_ll = QTextEdit(self.scrollAreaContentsBranch)
        self.deduction_branch_ll.setObjectName(u"deduction_branch_ll")
        self.deduction_branch_ll.setGeometry(QRect(35, 185, 165, 200))
        self.deduction_branch_ll.setStyleSheet(u"")
        self.deduction_branch_lr = QTextEdit(self.scrollAreaContentsBranch)
        self.deduction_branch_lr.setObjectName(u"deduction_branch_lr")
        self.deduction_branch_lr.setGeometry(QRect(220, 185, 165, 200))
        self.deduction_branch_lr.setStyleSheet(u"")
        self.deduction_branch_rl = QTextEdit(self.scrollAreaContentsBranch)
        self.deduction_branch_rl.setObjectName(u"deduction_branch_rl")
        self.deduction_branch_rl.setGeometry(QRect(425, 185, 165, 200))
        self.deduction_branch_rl.setStyleSheet(u"")
        self.deduction_branch_rr = QTextEdit(self.scrollAreaContentsBranch)
        self.deduction_branch_rr.setObjectName(u"deduction_branch_rr")
        self.deduction_branch_rr.setGeometry(QRect(610, 185, 165, 200))
        self.deduction_branch_rr.setStyleSheet(u"")
        self.scrollArea_2.setWidget(self.scrollAreaContentsBranch)

        self.verticalLayout_3.addWidget(self.scrollArea_2)

        self.tab_bar.addTab(self.branch_tab, "")

        self.verticalLayout.addWidget(self.tab_bar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ok_btn = QPushButton(self.centralwidget)
        self.ok_btn.setObjectName(u"ok_btn")

        self.horizontalLayout.addWidget(self.ok_btn)

        self.cancel_btn = QPushButton(self.centralwidget)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout.addWidget(self.cancel_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 852, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tab_bar.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Enter Deduction", None))
        self.help_btn.setText("")
        self.tab_bar.setTabText(self.tab_bar.indexOf(self.single_tab), QCoreApplication.translate("MainWindow", u"Single", None))
        self.tab_bar.setTabText(self.tab_bar.indexOf(self.branch_tab), QCoreApplication.translate("MainWindow", u"Branch", None))
        self.ok_btn.setText(QCoreApplication.translate("MainWindow", u"Ok", None))
        self.cancel_btn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
    # retranslateUi

