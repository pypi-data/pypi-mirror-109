# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainMFwnbj.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

import icons_rc

class Ui_MainDis(object):
    def setupUi(self, MainDis):
        if MainDis.objectName():
            MainDis.setObjectName(u"MainDis")
        MainDis.resize(397, 179)
        MainDis.setStyleSheet(u"font: 12pt \"Tahoma\";\n"
"border-color: rgb(85, 255, 0);\n"
"\n"
"background-color: rgb(9,5,13);\n"
"color: rgb(255,255,255);")
        self.centralwidget = QWidget(MainDis)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"\n"
"QToolBox{\n"
"	\n"
"	background-color: rgb(24,24,36);\n"
"	text-align: left;\n"
"\n"
"}\n"
"\n"
"QToolBox::tab{\n"
"	\n"
"	border-radius: 5px;\n"
"	background-color: rgb(17,16,26);\n"
"	text-align: left;\n"
"\n"
"}\n"
"")
        self.FrameMain = QFrame(self.centralwidget)
        self.FrameMain.setObjectName(u"FrameMain")
        self.FrameMain.setGeometry(QRect(3, 2, 396, 179))
        self.FrameMain.setFrameShape(QFrame.Box)
        self.FrameMain.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.FrameMain)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.fr_Measure = QFrame(self.FrameMain)
        self.fr_Measure.setObjectName(u"fr_Measure")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_Measure.sizePolicy().hasHeightForWidth())
        self.fr_Measure.setSizePolicy(sizePolicy)
        self.fr_Measure.setMinimumSize(QSize(395, 0))
        self.fr_Measure.setMaximumSize(QSize(0, 16777215))
        self.fr_Measure.setFrameShape(QFrame.StyledPanel)
        self.fr_Measure.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.fr_Measure)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.fr_Measure)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_5)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(self.frame_5)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.lbuplimit1 = QLabel(self.frame_5)
        self.lbuplimit1.setObjectName(u"lbuplimit1")

        self.horizontalLayout.addWidget(self.lbuplimit1)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.lbvalue = QLabel(self.frame_5)
        self.lbvalue.setObjectName(u"lbvalue")
        font = QFont()
        font.setFamily(u"Tahoma")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbvalue.setFont(font)
        self.lbvalue.setStyleSheet(u"color: rgb(115, 185, 255); \n"
"padding: 0px;\n"
"background-color: none;\n"
"border: 3px solid rgb(230,5,64);\n"
"border-radius: 10px;")
        self.lbvalue.setAlignment(Qt.AlignCenter)
        self.lbvalue.setIndent(-1)

        self.verticalLayout_4.addWidget(self.lbvalue)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.lbDlimit1 = QLabel(self.frame_5)
        self.lbDlimit1.setObjectName(u"lbDlimit1")

        self.verticalLayout.addWidget(self.lbDlimit1, 0, Qt.AlignTop)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btnKetNoi = QPushButton(self.frame_5)
        self.btnKetNoi.setObjectName(u"btnKetNoi")
        self.btnKetNoi.setStyleSheet(u"border: 1px solid rgb(230,5,64);\n"
"border-radius: 5px;")
        icon = QIcon()
        icon.addFile(u":/icons/check-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnKetNoi.setIcon(icon)
        self.btnKetNoi.setIconSize(QSize(16, 22))

        self.horizontalLayout_3.addWidget(self.btnKetNoi)

        self.btnThoat = QPushButton(self.frame_5)
        self.btnThoat.setObjectName(u"btnThoat")
        self.btnThoat.setStyleSheet(u"border: 1px solid rgb(230,5,64);\n"
"border-radius: 5px;")
        icon1 = QIcon()
        icon1.addFile(u":/icons/wifi-off.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnThoat.setIcon(icon1)
        self.btnThoat.setIconSize(QSize(16, 22))

        self.horizontalLayout_3.addWidget(self.btnThoat)

        self.cb1 = QComboBox(self.frame_5)
        self.cb1.setObjectName(u"cb1")
        self.cb1.setStyleSheet(u"background-color: rgrgb(85, 255, 255);\n"
"border-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(255, 255, 255, 255), stop:0.2 rgba(255, 176, 176, 167), stop:0.3 rgba(255, 151, 151, 92), stop:0.4 rgba(255, 125, 125, 51), stop:0.5 rgba(255, 76, 76, 205), stop:0.52 rgba(255, 76, 76, 205), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 255, 255, 0));\n"
"\n"
"")

        self.horizontalLayout_3.addWidget(self.cb1)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)


        self.horizontalLayout_5.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.fr_Measure)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_6)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.Thuoc2 = QFrame(self.frame_6)
        self.Thuoc2.setObjectName(u"Thuoc2")
        self.Thuoc2.setFrameShape(QFrame.StyledPanel)
        self.Thuoc2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.Thuoc2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.label_7 = QLabel(self.Thuoc2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_6.addWidget(self.label_7)

        self.lbuplimit2 = QLabel(self.Thuoc2)
        self.lbuplimit2.setObjectName(u"lbuplimit2")

        self.horizontalLayout_6.addWidget(self.lbuplimit2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.lbvalue_2 = QLabel(self.Thuoc2)
        self.lbvalue_2.setObjectName(u"lbvalue_2")
        self.lbvalue_2.setFont(font)
        self.lbvalue_2.setStyleSheet(u"color: rgb(115, 185, 255); \n"
"padding: 0px;\n"
"background-color: none;\n"
"border: 3px solid rgb(230,5,64);\n"
"border-radius: 10px;")
        self.lbvalue_2.setAlignment(Qt.AlignCenter)
        self.lbvalue_2.setIndent(-1)

        self.verticalLayout_3.addWidget(self.lbvalue_2)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.lbDlimit2 = QLabel(self.Thuoc2)
        self.lbDlimit2.setObjectName(u"lbDlimit2")

        self.verticalLayout_11.addWidget(self.lbDlimit2, 0, Qt.AlignTop)


        self.verticalLayout_3.addLayout(self.verticalLayout_11)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btnKetNoi_2 = QPushButton(self.Thuoc2)
        self.btnKetNoi_2.setObjectName(u"btnKetNoi_2")
        self.btnKetNoi_2.setStyleSheet(u"border: 1px solid rgb(230,5,64);\n"
"border-radius: 5px;")
        self.btnKetNoi_2.setIcon(icon)
        self.btnKetNoi_2.setIconSize(QSize(16, 22))

        self.horizontalLayout_4.addWidget(self.btnKetNoi_2)

        self.btnThoat_2 = QPushButton(self.Thuoc2)
        self.btnThoat_2.setObjectName(u"btnThoat_2")
        self.btnThoat_2.setStyleSheet(u"border: 1px solid rgb(230,5,64);\n"
"border-radius: 5px;")
        self.btnThoat_2.setIcon(icon1)
        self.btnThoat_2.setIconSize(QSize(16, 22))

        self.horizontalLayout_4.addWidget(self.btnThoat_2)

        self.cb2 = QComboBox(self.Thuoc2)
        self.cb2.setObjectName(u"cb2")
        self.cb2.setStyleSheet(u"background-color: rgrgb(85, 255, 255);\n"
"border-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(255, 255, 255, 255), stop:0.2 rgba(255, 176, 176, 167), stop:0.3 rgba(255, 151, 151, 92), stop:0.4 rgba(255, 125, 125, 51), stop:0.5 rgba(255, 76, 76, 205), stop:0.52 rgba(255, 76, 76, 205), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 255, 255, 0));\n"
"\n"
"")

        self.horizontalLayout_4.addWidget(self.cb2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_7.addLayout(self.verticalLayout_3)


        self.verticalLayout_8.addWidget(self.Thuoc2)


        self.horizontalLayout_5.addWidget(self.frame_6)


        self.verticalLayout_9.addWidget(self.fr_Measure)

        self.Fr_button = QFrame(self.FrameMain)
        self.Fr_button.setObjectName(u"Fr_button")
        self.Fr_button.setFrameShape(QFrame.StyledPanel)
        self.Fr_button.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.Fr_button)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.btnMain = QPushButton(self.Fr_button)
        self.btnMain.setObjectName(u"btnMain")
        self.btnMain.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/smartphone.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnMain.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.btnMain)

        self.btnUpdate = QPushButton(self.Fr_button)
        self.btnUpdate.setObjectName(u"btnUpdate")
        icon3 = QIcon()
        icon3.addFile(u":/icons/chrome.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnUpdate.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.btnUpdate)

        self.btnChart = QPushButton(self.Fr_button)
        self.btnChart.setObjectName(u"btnChart")
        icon4 = QIcon()
        icon4.addFile(u":/icons/activity.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnChart.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.btnChart)

        self.btnExit = QPushButton(self.Fr_button)
        self.btnExit.setObjectName(u"btnExit")
        icon5 = QIcon()
        icon5.addFile(u":/icons/power.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnExit.setIcon(icon5)

        self.horizontalLayout_2.addWidget(self.btnExit)

        self.lbsoluong = QLabel(self.Fr_button)
        self.lbsoluong.setObjectName(u"lbsoluong")
        self.lbsoluong.setMinimumSize(QSize(90, 25))
        self.lbsoluong.setMaximumSize(QSize(90, 25))
        self.lbsoluong.setSizeIncrement(QSize(90, 25))

        self.horizontalLayout_2.addWidget(self.lbsoluong)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_9.addWidget(self.Fr_button)

        MainDis.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainDis)

        QMetaObject.connectSlotsByName(MainDis)
    # setupUi

    def retranslateUi(self, MainDis):
        MainDis.setWindowTitle(QCoreApplication.translate("MainDis", u"MainWindow", None))
        self.label_6.setText(QCoreApplication.translate("MainDis", u"Device 1", None))
        self.lbuplimit1.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#55ff00;\">+0.000</span></p></body></html>", None))
        self.lbvalue.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#55ff00;\">00.000</span></p></body></html>", None))
        self.lbDlimit1.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffaa7f;\">-0.000</span></p></body></html>", None))
        self.btnKetNoi.setText("")
        self.btnThoat.setText("")
        self.cb1.setCurrentText("")
        self.label_7.setText(QCoreApplication.translate("MainDis", u"Device 2", None))
        self.lbuplimit2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#55ff00;\">+0.000</span></p></body></html>", None))
        self.lbvalue_2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#55ff00;\">00.000</span></p></body></html>", None))
        self.lbDlimit2.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"right\"><span style=\" color:#ffaa7f;\">-0.000</span></p></body></html>", None))
        self.btnKetNoi_2.setText("")
        self.btnThoat_2.setText("")
        self.cb2.setCurrentText("")
        self.btnMain.setText(QCoreApplication.translate("MainDis", u"Main", None))
        self.btnUpdate.setText(QCoreApplication.translate("MainDis", u"Update", None))
        self.btnChart.setText(QCoreApplication.translate("MainDis", u"Chart", None))
        self.btnExit.setText(QCoreApplication.translate("MainDis", u"Exit", None))
        self.lbsoluong.setText(QCoreApplication.translate("MainDis", u"<html><head/><body><p align=\"center\"><span style=\" color:#0000ff;\">...</span></p></body></html>", None))
    # retranslateUi

