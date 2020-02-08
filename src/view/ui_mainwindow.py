# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
        self.logic_type_gb = QGroupBox(self.centralwidget)
        self.logic_type_gb.setObjectName(u"logic_type_gb")
        self.horizontalLayout_2 = QHBoxLayout(self.logic_type_gb)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pl_radio_btn = QRadioButton(self.logic_type_gb)
        self.pl_radio_btn.setObjectName(u"pl_radio_btn")
        self.pl_radio_btn.setMinimumSize(QSize(0, 0))
        self.pl_radio_btn.setChecked(True)

        self.horizontalLayout_2.addWidget(self.pl_radio_btn)

        self.fopl_radio_btn = QRadioButton(self.logic_type_gb)
        self.fopl_radio_btn.setObjectName(u"fopl_radio_btn")
        self.fopl_radio_btn.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.fopl_radio_btn)

        self.ipl_radio_btn = QRadioButton(self.logic_type_gb)
        self.ipl_radio_btn.setObjectName(u"ipl_radio_btn")
        self.ipl_radio_btn.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.ipl_radio_btn)

        self.ifopl_radio_btn = QRadioButton(self.logic_type_gb)
        self.ifopl_radio_btn.setObjectName(u"ifopl_radio_btn")

        self.horizontalLayout_2.addWidget(self.ifopl_radio_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.logic_type_gb)

        self.calc_mode_gb = QGroupBox(self.centralwidget)
        self.calc_mode_gb.setObjectName(u"calc_mode_gb")
        self.horizontalLayout = QHBoxLayout(self.calc_mode_gb)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.automatic_radio_btn = QRadioButton(self.calc_mode_gb)
        self.automatic_radio_btn.setObjectName(u"automatic_radio_btn")
        self.automatic_radio_btn.setMinimumSize(QSize(100, 0))
        self.automatic_radio_btn.setChecked(True)

        self.horizontalLayout.addWidget(self.automatic_radio_btn)

        self.manual_radio_btn = QRadioButton(self.calc_mode_gb)
        self.manual_radio_btn.setObjectName(u"manual_radio_btn")
        self.manual_radio_btn.setMinimumSize(QSize(70, 0))
        self.manual_radio_btn.setChecked(False)

        self.horizontalLayout.addWidget(self.manual_radio_btn)

        self.help_button = QPushButton(self.calc_mode_gb)
        self.help_button.setObjectName(u"help_button")
        self.help_button.setMinimumSize(QSize(25, 25))
        self.help_button.setMaximumSize(QSize(25, 25))
        self.help_button.setStyleSheet(u"QPushButton {\n"
"    qproperty-icon: url(src/view/images/help.svg);\n"
"}")
        self.help_button.setAutoDefault(False)
        self.help_button.setFlat(False)

        self.horizontalLayout.addWidget(self.help_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.calc_mode_gb)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 763, 500))
        self.scrollAreaWidgetContents.setMinimumSize(QSize(500, 500))
        self.scrollAreaWidgetContents.setStyleSheet(u"#scrollAreaWidgetContents {\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.reset_btn = QPushButton(self.scrollAreaWidgetContents)
        self.reset_btn.setObjectName(u"reset_btn")
        self.reset_btn.setGeometry(QRect(5, 5, 31, 28))
        self.reset_btn.setStyleSheet(u"#reset_btn {\n"
"	qproperty-icon: url(src/view/images/stornieren.svg);\n"
"}")
        self.inital_right_exprs_text_edit = QTextEdit(self.scrollAreaWidgetContents)
        self.inital_right_exprs_text_edit.setObjectName(u"inital_right_exprs_text_edit")
        self.inital_right_exprs_text_edit.setGeometry(QRect(385, 85, 165, 200))
        self.inital_left_exprs_text_edit = QTextEdit(self.scrollAreaWidgetContents)
        self.inital_left_exprs_text_edit.setObjectName(u"inital_left_exprs_text_edit")
        self.inital_left_exprs_text_edit.setGeometry(QRect(200, 85, 165, 200))
        self.inital_left_exprs_text_edit.setStyleSheet(u"")
        self.start_calc_btn = QPushButton(self.scrollAreaWidgetContents)
        self.start_calc_btn.setObjectName(u"start_calc_btn")
        self.start_calc_btn.setGeometry(QRect(335, 310, 80, 25))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.help_button.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tableaux Prover", None))
#if QT_CONFIG(tooltip)
        self.pl_radio_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Propositional Logic", None))
#endif // QT_CONFIG(tooltip)
        self.pl_radio_btn.setText(QCoreApplication.translate("MainWindow", u"PL", None))
#if QT_CONFIG(tooltip)
        self.fopl_radio_btn.setToolTip(QCoreApplication.translate("MainWindow", u"First Order Predicate Logic", None))
#endif // QT_CONFIG(tooltip)
        self.fopl_radio_btn.setText(QCoreApplication.translate("MainWindow", u"FOPL", None))
#if QT_CONFIG(tooltip)
        self.ipl_radio_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Intuitionistic Propositional Logic", None))
#endif // QT_CONFIG(tooltip)
        self.ipl_radio_btn.setText(QCoreApplication.translate("MainWindow", u"IPL", None))
#if QT_CONFIG(tooltip)
        self.ifopl_radio_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Intuitionistic First Order Predicate Logic", None))
#endif // QT_CONFIG(tooltip)
        self.ifopl_radio_btn.setText(QCoreApplication.translate("MainWindow", u"IFOPL", None))
        self.automatic_radio_btn.setText(QCoreApplication.translate("MainWindow", u"Automatic", None))
        self.manual_radio_btn.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
#if QT_CONFIG(tooltip)
        self.help_button.setToolTip(QCoreApplication.translate("MainWindow", u"Show difference between Automatic and Manual.", None))
#endif // QT_CONFIG(tooltip)
        self.help_button.setText("")
#if QT_CONFIG(tooltip)
        self.scrollArea.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.reset_btn.setText("")
        self.start_calc_btn.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
    # retranslateUi

