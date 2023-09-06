# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HazardB1WindowtbQvkJ.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)

class Ui_SettingB1(object):
    def setupUi(self, SettingB1):
        if not SettingB1.objectName():
            SettingB1.setObjectName(u"SettingB1")
        SettingB1.resize(560, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingB1.sizePolicy().hasHeightForWidth())
        SettingB1.setSizePolicy(sizePolicy)
        SettingB1.setMinimumSize(QSize(560, 300))
        SettingB1.setMaximumSize(QSize(560, 300))
        SettingB1.setAutoFillBackground(True)
        self.centralwidget = QWidget(SettingB1)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.water_Label_2 = QLabel(self.centralwidget)
        self.water_Label_2.setObjectName(u"water_Label_2")

        self.horizontalLayout_3.addWidget(self.water_Label_2)

        self.horizontalLayout_3.setStretch(0, 2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.UserUses_Table = QTableView(self.centralwidget)
        self.UserUses_Table.setObjectName(u"UserUses_Table")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.UserUses_Table.sizePolicy().hasHeightForWidth())
        self.UserUses_Table.setSizePolicy(sizePolicy1)
        self.UserUses_Table.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked)
        self.UserUses_Table.setDragEnabled(True)
        self.UserUses_Table.setSortingEnabled(True)
        self.UserUses_Table.verticalHeader().setDefaultSectionSize(24)

        self.horizontalLayout_2.addWidget(self.UserUses_Table)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.Close_Button = QPushButton(self.centralwidget)
        self.Close_Button.setObjectName(u"Close_Button")

        self.horizontalLayout_5.addWidget(self.Close_Button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        SettingB1.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingB1)

        QMetaObject.connectSlotsByName(SettingB1)
    # setupUi

    def retranslateUi(self, SettingB1):
        SettingB1.setWindowTitle(QCoreApplication.translate("SettingB1", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("SettingB1", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Setting the damage to buildings according to methodology B1<br/></span><span style=\" font-size:12pt; font-style:italic;\">(Huizinga et al. 2017)</span></p></body></html>", None))
        self.water_Label_2.setText(QCoreApplication.translate("SettingB1", u"<html><head/><body><p><span style=\" font-weight:700;\">Custom buildings uses</span></p></body></html>", None))
        self.Close_Button.setText(QCoreApplication.translate("SettingB1", u"Close", None))
    # retranslateUi

