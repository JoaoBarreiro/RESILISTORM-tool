# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetupWindow_V3HQyIVH.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_SetupWindow(object):
    def setupUi(self, SetupWindow):
        if not SetupWindow.objectName():
            SetupWindow.setObjectName(u"SetupWindow")
        SetupWindow.setWindowModality(Qt.WindowModal)
        SetupWindow.setEnabled(True)
        SetupWindow.resize(800, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SetupWindow.sizePolicy().hasHeightForWidth())
        SetupWindow.setSizePolicy(sizePolicy)
        SetupWindow.setMinimumSize(QSize(800, 500))
        SetupWindow.setMaximumSize(QSize(800, 500))
        
        self.centralwidget = QWidget(SetupWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(9, 10, 781, 481))
        self.main_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.scenarios_layout = QVBoxLayout()
        self.scenarios_layout.setSpacing(5)
        self.scenarios_layout.setObjectName(u"scenarios_layout")
        self.scenarios_layout.setContentsMargins(5, -1, 5, -1)
        self.scenarios_label = QLabel(self.horizontalLayoutWidget)
        self.scenarios_label.setObjectName(u"scenarios_label")
        self.scenarios_label.setAlignment(Qt.AlignCenter)

        self.scenarios_layout.addWidget(self.scenarios_label)

        self.scenario_button_layout = QHBoxLayout()
        self.scenario_button_layout.setSpacing(0)
        self.scenario_button_layout.setObjectName(u"scenario_button_layout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.scenario_button_layout.addItem(self.horizontalSpacer_2)

        self.add_scenario_button = QPushButton(self.horizontalLayoutWidget)
        self.add_scenario_button.setObjectName(u"add_scenario_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_scenario_button.sizePolicy().hasHeightForWidth())
        self.add_scenario_button.setSizePolicy(sizePolicy1)
        self.add_scenario_button.setMinimumSize(QSize(0, 0))
        self.add_scenario_button.setMaximumSize(QSize(200, 16777215))
        self.add_scenario_button.setFlat(False)

        self.scenario_button_layout.addWidget(self.add_scenario_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.scenario_button_layout.addItem(self.horizontalSpacer)


        self.scenarios_layout.addLayout(self.scenario_button_layout)

        self.scenarios_scroll_area = QScrollArea(self.horizontalLayoutWidget)
        self.scenarios_scroll_area.setObjectName(u"scenarios_scroll_area")
        self.scenarios_scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 376, 423))
        self.scenarios_scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.scenarios_layout.addWidget(self.scenarios_scroll_area)


        self.main_layout.addLayout(self.scenarios_layout)

        self.line = QFrame(self.horizontalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.main_layout.addWidget(self.line)

        self.indicators_layout = QVBoxLayout()
        self.indicators_layout.setSpacing(5)
        self.indicators_layout.setObjectName(u"indicators_layout")
        self.indicators_layout.setContentsMargins(5, -1, 5, -1)
        self.indicators_label = QLabel(self.horizontalLayoutWidget)
        self.indicators_label.setObjectName(u"indicators_label")
        self.indicators_label.setAlignment(Qt.AlignCenter)

        self.indicators_layout.addWidget(self.indicators_label)

        self.indicator_button_layout = QHBoxLayout()
        self.indicator_button_layout.setSpacing(0)
        self.indicator_button_layout.setObjectName(u"indicator_button_layout")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.indicator_button_layout.addItem(self.horizontalSpacer_4)

        self.add_indicator_button = QPushButton(self.horizontalLayoutWidget)
        self.add_indicator_button.setObjectName(u"add_indicator_button")
        sizePolicy1.setHeightForWidth(self.add_indicator_button.sizePolicy().hasHeightForWidth())
        self.add_indicator_button.setSizePolicy(sizePolicy1)
        self.add_indicator_button.setMinimumSize(QSize(0, 0))
        self.add_indicator_button.setMaximumSize(QSize(200, 16777215))

        self.indicator_button_layout.addWidget(self.add_indicator_button)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.indicator_button_layout.addItem(self.horizontalSpacer_3)


        self.indicators_layout.addLayout(self.indicator_button_layout)

        self.indicators_scroll_area = QScrollArea(self.horizontalLayoutWidget)
        self.indicators_scroll_area.setObjectName(u"indicators_scroll_area")
        self.indicators_scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 376, 423))
        self.indicators_scroll_area.setWidget(self.scrollAreaWidgetContents_2)

        self.indicators_layout.addWidget(self.indicators_scroll_area)


        self.main_layout.addLayout(self.indicators_layout)

        SetupWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SetupWindow)

        QMetaObject.connectSlotsByName(SetupWindow)
    # setupUi

    def retranslateUi(self, SetupWindow):
        SetupWindow.setWindowTitle(QCoreApplication.translate("SetupWindow", u"MainWindow", None))
        self.scenarios_label.setText(QCoreApplication.translate("SetupWindow", u"Scenarios setup", None))
        self.add_scenario_button.setText(QCoreApplication.translate("SetupWindow", u"\u2795 Add new scenario", None))
        self.indicators_label.setText(QCoreApplication.translate("SetupWindow", u"Performance indicators setup", None))
        self.add_indicator_button.setText(QCoreApplication.translate("SetupWindow", u"\u2795 Add new indicator", None))
    # retranslateUi

