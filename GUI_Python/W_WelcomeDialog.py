# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WelcomeDialogmFkXMd.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import GUI_Python.resources_rc

class Ui_WelcomeDialog(object):
    def setupUi(self, WelcomeDialog):
        if not WelcomeDialog.objectName():
            WelcomeDialog.setObjectName(u"WelcomeDialog")
        WelcomeDialog.resize(730, 500)
        WelcomeDialog.setMinimumSize(QSize(730, 500))
        WelcomeDialog.setMaximumSize(QSize(730, 500))
        icon = QIcon()
        icon.addFile(u":/icon/icons/RESILISTORM_mini.png", QSize(), QIcon.Normal, QIcon.Off)
        WelcomeDialog.setWindowIcon(icon)
        WelcomeDialog.setStyleSheet(u"QDialog {\n"
"border-radius: 20px\n"
"}")
        WelcomeDialog.setSizeGripEnabled(False)
        WelcomeDialog.setModal(False)
        self.horizontalLayout_2 = QHBoxLayout(WelcomeDialog)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.label = QLabel(WelcomeDialog)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u":/icon/icons/RESILISTORM_Welcome.gif"))
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.widget = QWidget(WelcomeDialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.NewButton = QPushButton(self.widget)
        self.NewButton.setObjectName(u"NewButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NewButton.sizePolicy().hasHeightForWidth())
        self.NewButton.setSizePolicy(sizePolicy)
        self.NewButton.setMinimumSize(QSize(300, 50))
        self.NewButton.setMaximumSize(QSize(250, 50))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.NewButton.setFont(font)
        self.NewButton.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icon/icons/city-building.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.NewButton.setIcon(icon1)
        self.NewButton.setIconSize(QSize(20, 30))
        self.NewButton.setFlat(False)

        self.verticalLayout.addWidget(self.NewButton, 0, Qt.AlignHCenter)

        self.LoadButton = QPushButton(self.widget)
        self.LoadButton.setObjectName(u"LoadButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.LoadButton.sizePolicy().hasHeightForWidth())
        self.LoadButton.setSizePolicy(sizePolicy1)
        self.LoadButton.setMinimumSize(QSize(300, 50))
        self.LoadButton.setMaximumSize(QSize(250, 50))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.LoadButton.setFont(font1)
        icon2 = QIcon()
        icon2.addFile(u":/icon/icons/data-transfer-upload-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.LoadButton.setIcon(icon2)
        self.LoadButton.setIconSize(QSize(20, 30))

        self.verticalLayout.addWidget(self.LoadButton, 0, Qt.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.horizontalLayout_2.addWidget(self.widget)

        self.horizontalLayout_2.setStretch(0, 1)

        self.retranslateUi(WelcomeDialog)

        self.NewButton.setDefault(False)


        QMetaObject.connectSlotsByName(WelcomeDialog)
    # setupUi

    def retranslateUi(self, WelcomeDialog):
        WelcomeDialog.setWindowTitle(QCoreApplication.translate("WelcomeDialog", u"Dialog", None))
        self.label.setText("")
        self.NewButton.setText(QCoreApplication.translate("WelcomeDialog", u"Create resilience study directory", None))
        self.LoadButton.setText(QCoreApplication.translate("WelcomeDialog", u"Load resilience study directory", None))
    # retranslateUi

