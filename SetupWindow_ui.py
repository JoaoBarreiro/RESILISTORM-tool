# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetupWindoweJZKGi.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)

class Ui_ScenarioSetup(object):
    def setupUi(self, ScenarioSetup):
        if not ScenarioSetup.objectName():
            ScenarioSetup.setObjectName(u"ScenarioSetup")
        ScenarioSetup.resize(650, 250)
        self.verticalLayoutWidget_2 = QWidget(ScenarioSetup)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 10, 631, 231))
        self.MainVerticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.MainVerticalLayout.setObjectName(u"MainVerticalLayout")
        self.MainVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.SetupLabel = QLabel(self.verticalLayoutWidget_2)
        self.SetupLabel.setObjectName(u"SetupLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SetupLabel.sizePolicy().hasHeightForWidth())
        self.SetupLabel.setSizePolicy(sizePolicy)

        self.MainVerticalLayout.addWidget(self.SetupLabel)

        self.MidHorLayout = QHBoxLayout()
        self.MidHorLayout.setSpacing(5)
        self.MidHorLayout.setObjectName(u"MidHorLayout")
        self.MidHorLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.SetupTableView = QTableView(self.verticalLayoutWidget_2)
        self.SetupTableView.setObjectName(u"SetupTableView")
        self.SetupTableView.setFrameShape(QFrame.StyledPanel)

        self.MidHorLayout.addWidget(self.SetupTableView)

        self.ButtonsVerticalLayout = QVBoxLayout()
        self.ButtonsVerticalLayout.setObjectName(u"ButtonsVerticalLayout")
        self.Add_BT = QPushButton(self.verticalLayoutWidget_2)
        self.Add_BT.setObjectName(u"Add_BT")

        self.ButtonsVerticalLayout.addWidget(self.Add_BT)

        self.Del_BT = QPushButton(self.verticalLayoutWidget_2)
        self.Del_BT.setObjectName(u"Del_BT")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Del_BT.sizePolicy().hasHeightForWidth())
        self.Del_BT.setSizePolicy(sizePolicy1)
        self.Del_BT.setMinimumSize(QSize(0, 0))

        self.ButtonsVerticalLayout.addWidget(self.Del_BT)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ButtonsVerticalLayout.addItem(self.verticalSpacer)

        self.Save_BT = QPushButton(self.verticalLayoutWidget_2)
        self.Save_BT.setObjectName(u"Save_BT")
        sizePolicy1.setHeightForWidth(self.Save_BT.sizePolicy().hasHeightForWidth())
        self.Save_BT.setSizePolicy(sizePolicy1)
        self.Save_BT.setMinimumSize(QSize(0, 0))

        self.ButtonsVerticalLayout.addWidget(self.Save_BT)

        self.Close_BT = QPushButton(self.verticalLayoutWidget_2)
        self.Close_BT.setObjectName(u"Close_BT")
        sizePolicy1.setHeightForWidth(self.Close_BT.sizePolicy().hasHeightForWidth())
        self.Close_BT.setSizePolicy(sizePolicy1)
        self.Close_BT.setMinimumSize(QSize(0, 0))

        self.ButtonsVerticalLayout.addWidget(self.Close_BT)


        self.MidHorLayout.addLayout(self.ButtonsVerticalLayout)


        self.MainVerticalLayout.addLayout(self.MidHorLayout)

        self.MainVerticalLayout.setStretch(0, 1)
        self.MainVerticalLayout.setStretch(1, 6)

        self.retranslateUi(ScenarioSetup)

        QMetaObject.connectSlotsByName(ScenarioSetup)
    # setupUi

    def retranslateUi(self, ScenarioSetup):
        ScenarioSetup.setWindowTitle(QCoreApplication.translate("ScenarioSetup", u"Dialog", None))
        self.SetupLabel.setText(QCoreApplication.translate("ScenarioSetup", u"<html><head/><body><p><span style=\" font-weight:700;\">Setup Label</span></p></body></html>", None))
        self.Add_BT.setText(QCoreApplication.translate("ScenarioSetup", u"Add \u2795", None))
        self.Del_BT.setText(QCoreApplication.translate("ScenarioSetup", u"Delete \u2796", None))
        self.Save_BT.setText(QCoreApplication.translate("ScenarioSetup", u"Save", None))
        self.Close_BT.setText(QCoreApplication.translate("ScenarioSetup", u"Close", None))
    # retranslateUi

