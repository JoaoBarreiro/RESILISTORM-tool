# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerNtQgNe.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_HazardSetup(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(650, 250)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(650, 250))
        MainWindow.setMaximumSize(QSize(650, 250))
        icon = QIcon()
        icon.addFile(u":/icon/icons/REFUSS LOGO.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMinimumSize(QSize(650, 250))
        self.centralwidget.setMaximumSize(QSize(650, 250))
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 3, 651, 251))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.SetupLabel = QLabel(self.widget)
        self.SetupLabel.setObjectName(u"SetupLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.SetupLabel.sizePolicy().hasHeightForWidth())
        self.SetupLabel.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.SetupLabel)

        self.MidHorLayout = QHBoxLayout()
        self.MidHorLayout.setSpacing(5)
        self.MidHorLayout.setObjectName(u"MidHorLayout")
        self.MidHorLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.SetupTableView = QTableView(self.widget)
        self.SetupTableView.setObjectName(u"SetupTableView")
        self.SetupTableView.setFrameShape(QFrame.StyledPanel)

        self.MidHorLayout.addWidget(self.SetupTableView)

        self.ButtonsVerticalLayout = QVBoxLayout()
        self.ButtonsVerticalLayout.setObjectName(u"ButtonsVerticalLayout")
        self.Add_BT = QPushButton(self.widget)
        self.Add_BT.setObjectName(u"Add_BT")

        self.ButtonsVerticalLayout.addWidget(self.Add_BT)

        self.Del_BT = QPushButton(self.widget)
        self.Del_BT.setObjectName(u"Del_BT")
        sizePolicy.setHeightForWidth(self.Del_BT.sizePolicy().hasHeightForWidth())
        self.Del_BT.setSizePolicy(sizePolicy)
        self.Del_BT.setMinimumSize(QSize(0, 0))

        self.ButtonsVerticalLayout.addWidget(self.Del_BT)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ButtonsVerticalLayout.addItem(self.verticalSpacer)

        self.Close_BT = QPushButton(self.widget)
        self.Close_BT.setObjectName(u"Close_BT")
        sizePolicy.setHeightForWidth(self.Close_BT.sizePolicy().hasHeightForWidth())
        self.Close_BT.setSizePolicy(sizePolicy)
        self.Close_BT.setMinimumSize(QSize(0, 0))

        self.ButtonsVerticalLayout.addWidget(self.Close_BT)


        self.MidHorLayout.addLayout(self.ButtonsVerticalLayout)


        self.verticalLayout.addLayout(self.MidHorLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.SetupLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Setup Label</span></p></body></html>", None))
        self.Add_BT.setText(QCoreApplication.translate("MainWindow", u"Add \u2795", None))
        self.Del_BT.setText(QCoreApplication.translate("MainWindow", u"Delete \u2796", None))
        self.Close_BT.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

