# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WelcomeWindowFJWeAQ.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)
import resources_rc

class Ui_WelcomeWindow(object):
    def setupUi(self, WelcomeWindow):
        if not WelcomeWindow.objectName():
            WelcomeWindow.setObjectName(u"WelcomeWindow")
        WelcomeWindow.resize(667, 365)
        icon = QIcon()
        icon.addFile(u":/icon/icons/REFUSS LOGO.ico", QSize(), QIcon.Normal, QIcon.Off)
        WelcomeWindow.setWindowIcon(icon)
        self.verticalLayoutWidget = QWidget(WelcomeWindow)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 641, 348))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u":/icon/icons/REFUSS LOGO.ico"))
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.WelcomeLabel = QLabel(self.verticalLayoutWidget)
        self.WelcomeLabel.setObjectName(u"WelcomeLabel")

        self.verticalLayout.addWidget(self.WelcomeLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.NewButton = QPushButton(self.verticalLayoutWidget)
        self.NewButton.setObjectName(u"NewButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NewButton.sizePolicy().hasHeightForWidth())
        self.NewButton.setSizePolicy(sizePolicy)
        self.NewButton.setMinimumSize(QSize(0, 0))
        self.NewButton.setMaximumSize(QSize(200, 50))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.NewButton.setFont(font)
        self.NewButton.setFlat(False)

        self.horizontalLayout.addWidget(self.NewButton)

        self.LoadButton = QPushButton(self.verticalLayoutWidget)
        self.LoadButton.setObjectName(u"LoadButton")
        sizePolicy.setHeightForWidth(self.LoadButton.sizePolicy().hasHeightForWidth())
        self.LoadButton.setSizePolicy(sizePolicy)
        self.LoadButton.setMinimumSize(QSize(200, 50))
        self.LoadButton.setMaximumSize(QSize(200, 50))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.LoadButton.setFont(font1)

        self.horizontalLayout.addWidget(self.LoadButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(WelcomeWindow)

        self.NewButton.setDefault(False)


        QMetaObject.connectSlotsByName(WelcomeWindow)
    # setupUi

    def retranslateUi(self, WelcomeWindow):
        WelcomeWindow.setWindowTitle(QCoreApplication.translate("WelcomeWindow", u"Dialog", None))
        self.label.setText("")
        self.WelcomeLabel.setText(QCoreApplication.translate("WelcomeWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Welcome to REFUSS Tool!</span></p></body></html>", None))
        self.NewButton.setText(QCoreApplication.translate("WelcomeWindow", u"New resilience analysis", None))
        self.LoadButton.setText(QCoreApplication.translate("WelcomeWindow", u"Load resilience analysis", None))
    # retranslateUi

