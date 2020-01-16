# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'concep1.ui'
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
        MainWindow.resize(800, 630)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalGroupBox = QGroupBox(self.centralwidget)
        self.horizontalGroupBox.setObjectName(u"horizontalGroupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButton_4 = QRadioButton(self.horizontalGroupBox)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setMinimumSize(QSize(0, 0))
        self.radioButton_4.setChecked(True)

        self.horizontalLayout_2.addWidget(self.radioButton_4)

        self.radioButton_3 = QRadioButton(self.horizontalGroupBox)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.radioButton_3)

        self.radioButton_2 = QRadioButton(self.horizontalGroupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.radioButton_2)

        self.radioButton = QRadioButton(self.horizontalGroupBox)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_2.addWidget(self.radioButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.horizontalGroupBox)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.automatic_radio_btn = QRadioButton(self.groupBox)
        self.automatic_radio_btn.setObjectName(u"automatic_radio_btn")
        self.automatic_radio_btn.setMinimumSize(QSize(100, 0))
        self.automatic_radio_btn.setChecked(False)

        self.horizontalLayout.addWidget(self.automatic_radio_btn)

        self.manual_radio_btn = QRadioButton(self.groupBox)
        self.manual_radio_btn.setObjectName(u"manual_radio_btn")
        self.manual_radio_btn.setMinimumSize(QSize(70, 0))
        self.manual_radio_btn.setChecked(True)

        self.horizontalLayout.addWidget(self.manual_radio_btn)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(20, 20))
        self.pushButton.setMaximumSize(QSize(20, 20))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    border-image: url(help.svg) 5 5 5 5 stretch stretch;\n"
"    background-repeat: no-repeat;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-image: url(help_hovered.png);\n"
"    background-repeat: no-repeat;\n"
"}")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 755, 500))
        self.scrollAreaWidgetContents.setMinimumSize(QSize(500, 500))
        self.scrollAreaWidgetContents.setStyleSheet(u"#scrollAreaWidgetContents {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.pushButton_2 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(5, 5, 31, 28))
        self.pushButton_2.setStyleSheet(u"#pushButton_2 {\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border-color: rgba(255, 255, 255, 0);\n"
"	color: rgba(255, 255, 255, 0);\n"
"	qproperty-icon: url(stornieren.svg);\n"
"}")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tableaux Prover", None))
#if QT_CONFIG(tooltip)
        self.radioButton_4.setToolTip(QCoreApplication.translate("MainWindow", u"Propositional Logic", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"PL", None))
#if QT_CONFIG(tooltip)
        self.radioButton_3.setToolTip(QCoreApplication.translate("MainWindow", u"First Order Predicate Logic", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"FOPL", None))
#if QT_CONFIG(tooltip)
        self.radioButton_2.setToolTip(QCoreApplication.translate("MainWindow", u"Intuitionistic Propositional Logic", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"IPL", None))
#if QT_CONFIG(tooltip)
        self.radioButton.setToolTip(QCoreApplication.translate("MainWindow", u"Intuitionistic First Order Predicate Logic", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"IFOPL", None))
        self.automatic_radio_btn.setText(QCoreApplication.translate("MainWindow", u"Automatic", None))
        self.manual_radio_btn.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
#if QT_CONFIG(tooltip)
        self.pushButton.setToolTip(QCoreApplication.translate("MainWindow", u"Show difference between Automatic and Manual.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton.setText("")
#if QT_CONFIG(tooltip)
        self.scrollArea.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_2.setText("")
    # retranslateUi

