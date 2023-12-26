# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainPage_V7DRkVHD.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QFormLayout, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStackedWidget,
    QTabWidget, QTableWidget, QTableWidgetItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)
import GUI_Python.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.resize(1284, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1280, 720))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setContextMenuPolicy(Qt.DefaultContextMenu)
        MainWindow.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(u":/icon/icons/REFUSS LOGO.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QScrollBar:vertical {\n"
"	background: none;\n"
"    width: 10px;\n"
"    }\n"
"QScrollBar::handle:vertical {\n"
"     background: #D3D3D3;\n"
"    border-radius: 5px;\n"
"    }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"   background: none;\n"
"    }")
        MainWindow.setIconSize(QSize(25, 25))
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        icon1 = QIcon()
        icon1.addFile(u":/icon/icons/save-as-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave_As.setIcon(icon1)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        icon2 = QIcon()
        icon2.addFile(u":/icon/icons/save-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setShortcutVisibleInContextMenu(True)
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        icon3 = QIcon()
        icon3.addFile(u":/icon/icons/data-transfer-upload-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionLoad.setIcon(icon3)
        self.actionManual = QAction(MainWindow)
        self.actionManual.setObjectName(u"actionManual")
        icon4 = QIcon()
        icon4.addFile(u":/icon/icons/book-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionManual.setIcon(icon4)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        icon5 = QIcon()
        icon5.addFile(u":/icon/icons/info-2-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAbout.setIcon(icon5)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.Org0_TopREFUSS = QWidget(self.centralwidget)
        self.Org0_TopREFUSS.setObjectName(u"Org0_TopREFUSS")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Org0_TopREFUSS.sizePolicy().hasHeightForWidth())
        self.Org0_TopREFUSS.setSizePolicy(sizePolicy1)
        self.Org0_TopREFUSS.setMinimumSize(QSize(0, 60))
        self.Org0_TopREFUSS.setMaximumSize(QSize(16777215, 60))
        self.Org0_TopREFUSS.setStyleSheet(u"/*background-color: #fdcb6e;*/\n"
" border-radius: 20px")
        self.horizontalLayout = QHBoxLayout(self.Org0_TopREFUSS)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.Org0_TopREFUSS)
        self.label_5.setObjectName(u"label_5")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy2)
        self.label_5.setMinimumSize(QSize(50, 50))
        self.label_5.setMaximumSize(QSize(50, 50))
        self.label_5.setPixmap(QPixmap(u":/icon/icons/RESILISTORM_mini.png"))
        self.label_5.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_5)

        self.widget_3 = QWidget(self.Org0_TopREFUSS)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_6 = QVBoxLayout(self.widget_3)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.REFUSS2_label = QLabel(self.widget_3)
        self.REFUSS2_label.setObjectName(u"REFUSS2_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.REFUSS2_label.sizePolicy().hasHeightForWidth())
        self.REFUSS2_label.setSizePolicy(sizePolicy3)
        self.REFUSS2_label.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setFamilies([u"Brandon Grotesque Black"])
        font.setItalic(True)
        self.REFUSS2_label.setFont(font)
        self.REFUSS2_label.setStyleSheet(u"")
        self.REFUSS2_label.setTextFormat(Qt.RichText)
        self.REFUSS2_label.setScaledContents(True)
        self.REFUSS2_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.REFUSS2_label.setWordWrap(True)
        self.REFUSS2_label.setIndent(0)
        self.REFUSS2_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

        self.verticalLayout_6.addWidget(self.REFUSS2_label)

        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setFamilies([u"Brandon Grotesque Light"])
        font1.setPointSize(9)
        font1.setItalic(True)
        self.label_4.setFont(font1)
        self.label_4.setTextFormat(Qt.RichText)

        self.verticalLayout_6.addWidget(self.label_4)

        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 1)

        self.horizontalLayout.addWidget(self.widget_3)


        self.verticalLayout_5.addWidget(self.Org0_TopREFUSS)

        self.Org1_Body = QHBoxLayout()
        self.Org1_Body.setSpacing(10)
        self.Org1_Body.setObjectName(u"Org1_Body")
        self.Org1_Body.setContentsMargins(0, 0, -1, -1)
        self.LeftMenu = QHBoxLayout()
        self.LeftMenu.setSpacing(0)
        self.LeftMenu.setObjectName(u"LeftMenu")
        self.LeftMenuFrame = QFrame(self.centralwidget)
        self.LeftMenuFrame.setObjectName(u"LeftMenuFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.LeftMenuFrame.sizePolicy().hasHeightForWidth())
        self.LeftMenuFrame.setSizePolicy(sizePolicy4)
        self.LeftMenuFrame.setMinimumSize(QSize(0, 0))
        self.LeftMenuFrame.setMaximumSize(QSize(50, 16777215))
        self.LeftMenuFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 20px")
        self.LeftMenuFrame.setInputMethodHints(Qt.ImhNone)
        self.verticalLayout_10 = QVBoxLayout(self.LeftMenuFrame)
        self.verticalLayout_10.setSpacing(5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(5, 10, 5, 10)
        self.menu_btn = QPushButton(self.LeftMenuFrame)
        self.menu_btn.setObjectName(u"menu_btn")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.menu_btn.sizePolicy().hasHeightForWidth())
        self.menu_btn.setSizePolicy(sizePolicy5)
        self.menu_btn.setMinimumSize(QSize(20, 20))
        self.menu_btn.setMaximumSize(QSize(20, 20))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.menu_btn.setFont(font2)
        self.menu_btn.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 255, 255);\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"	/*border: 2px solid black;*/\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(221, 230, 237, 255)\n"
"}")
        self.menu_btn.setText(u"")
        icon6 = QIcon()
        icon6.addFile(u":/icon/icons/right_arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_btn.setIcon(icon6)
        self.menu_btn.setIconSize(QSize(15, 15))
        self.menu_btn.setCheckable(True)
        self.menu_btn.setChecked(False)
        self.menu_btn.setAutoExclusive(False)
        self.menu_btn.setAutoDefault(False)
        self.menu_btn.setFlat(False)

        self.verticalLayout_10.addWidget(self.menu_btn, 0, Qt.AlignHCenter)

        self.widget = QWidget(self.LeftMenuFrame)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_32 = QVBoxLayout(self.widget)
        self.verticalLayout_32.setSpacing(5)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.verticalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.home_btn = QPushButton(self.widget)
        self.home_btn.setObjectName(u"home_btn")
        sizePolicy5.setHeightForWidth(self.home_btn.sizePolicy().hasHeightForWidth())
        self.home_btn.setSizePolicy(sizePolicy5)
        self.home_btn.setMinimumSize(QSize(40, 40))
        self.home_btn.setMaximumSize(QSize(40, 40))
        self.home_btn.setFont(font2)
        self.home_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"    padding: 0;  /* Remove any padding */\n"
"    margin: 0;  /* Remove any margin */\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: rgba(197, 223, 248, 255);\n"
"	border: 2px solid black;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(197, 223, 248, 255);\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u":/icon/icons/house-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.home_btn.setIcon(icon7)
        self.home_btn.setIconSize(QSize(20, 20))
        self.home_btn.setCheckable(True)
        self.home_btn.setChecked(False)
        self.home_btn.setAutoExclusive(True)

        self.verticalLayout_32.addWidget(self.home_btn)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_32.addItem(self.verticalSpacer_12)

        self.profile_btn = QPushButton(self.widget)
        self.profile_btn.setObjectName(u"profile_btn")
        sizePolicy5.setHeightForWidth(self.profile_btn.sizePolicy().hasHeightForWidth())
        self.profile_btn.setSizePolicy(sizePolicy5)
        self.profile_btn.setMinimumSize(QSize(40, 40))
        self.profile_btn.setMaximumSize(QSize(40, 40))
        self.profile_btn.setFont(font2)
        self.profile_btn.setAcceptDrops(False)
        self.profile_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 0px solid black;\n"
"	padding-left: 0px;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: rgba(252, 252, 232, 255);\n"
"	border: 2px solid black;\n"
"}QPushButton:hover {\n"
"    background-color: rgba(252, 252, 232, 255)\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u":/icon/icons/city-building.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.profile_btn.setIcon(icon8)
        self.profile_btn.setIconSize(QSize(20, 20))
        self.profile_btn.setCheckable(True)
        self.profile_btn.setAutoExclusive(True)
        self.profile_btn.setFlat(False)

        self.verticalLayout_32.addWidget(self.profile_btn)

        self.analysis_btn = QPushButton(self.widget)
        self.analysis_btn.setObjectName(u"analysis_btn")
        sizePolicy5.setHeightForWidth(self.analysis_btn.sizePolicy().hasHeightForWidth())
        self.analysis_btn.setSizePolicy(sizePolicy5)
        self.analysis_btn.setMinimumSize(QSize(40, 40))
        self.analysis_btn.setMaximumSize(QSize(40, 40))
        self.analysis_btn.setFont(font2)
        self.analysis_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color:rgba(245, 245, 245, 255);\n"
"	border: 2px solid black;\n"
"}QPushButton:hover {\n"
"    background-color:rgba(245, 245, 245, 255)\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u":/icon/icons/icons8-settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.analysis_btn.setIcon(icon9)
        self.analysis_btn.setIconSize(QSize(20, 20))
        self.analysis_btn.setCheckable(True)
        self.analysis_btn.setChecked(False)
        self.analysis_btn.setAutoExclusive(True)

        self.verticalLayout_32.addWidget(self.analysis_btn)

        self.verticalSpacer_7 = QSpacerItem(20, 128, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_32.addItem(self.verticalSpacer_7)

        self.functional_btn = QPushButton(self.widget)
        self.functional_btn.setObjectName(u"functional_btn")
        sizePolicy5.setHeightForWidth(self.functional_btn.sizePolicy().hasHeightForWidth())
        self.functional_btn.setSizePolicy(sizePolicy5)
        self.functional_btn.setMinimumSize(QSize(40, 40))
        self.functional_btn.setMaximumSize(QSize(40, 40))
        self.functional_btn.setFont(font2)
        self.functional_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: rgba(228, 247, 233, 255);\n"
"	border: 2px solid black;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(228, 247, 233, 255)\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u":/icon/icons/settings-13-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.functional_btn.setIcon(icon10)
        self.functional_btn.setIconSize(QSize(20, 20))
        self.functional_btn.setCheckable(True)
        self.functional_btn.setChecked(False)
        self.functional_btn.setAutoExclusive(True)

        self.verticalLayout_32.addWidget(self.functional_btn)

        self.performance_btn = QPushButton(self.widget)
        self.performance_btn.setObjectName(u"performance_btn")
        sizePolicy5.setHeightForWidth(self.performance_btn.sizePolicy().hasHeightForWidth())
        self.performance_btn.setSizePolicy(sizePolicy5)
        self.performance_btn.setMinimumSize(QSize(40, 40))
        self.performance_btn.setMaximumSize(QSize(40, 40))
        self.performance_btn.setFont(font2)
        self.performance_btn.setAcceptDrops(True)
        self.performance_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: rgba(255, 243, 226, 255);\n"
"	border: 2px solid black;\n"
"}QPushButton:hover {\n"
"    background-color: rgba(255, 243, 226, 255)\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        icon11 = QIcon()
        icon11.addFile(u":/icon/icons/rain-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.performance_btn.setIcon(icon11)
        self.performance_btn.setIconSize(QSize(20, 20))
        self.performance_btn.setCheckable(True)
        self.performance_btn.setAutoExclusive(True)

        self.verticalLayout_32.addWidget(self.performance_btn)

        self.dashboard_btn = QPushButton(self.widget)
        self.dashboard_btn.setObjectName(u"dashboard_btn")
        sizePolicy5.setHeightForWidth(self.dashboard_btn.sizePolicy().hasHeightForWidth())
        self.dashboard_btn.setSizePolicy(sizePolicy5)
        self.dashboard_btn.setMinimumSize(QSize(40, 40))
        self.dashboard_btn.setMaximumSize(QSize(40, 40))
        self.dashboard_btn.setFont(font2)
        self.dashboard_btn.setAcceptDrops(True)
        self.dashboard_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: rgba(218, 238, 236, 255);\n"
"	border: 2px solid black;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(218, 238, 236, 255)\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        icon12 = QIcon()
        icon12.addFile(u":/icon/icons/dashboard-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.dashboard_btn.setIcon(icon12)
        self.dashboard_btn.setIconSize(QSize(20, 20))
        self.dashboard_btn.setCheckable(True)
        self.dashboard_btn.setAutoExclusive(True)

        self.verticalLayout_32.addWidget(self.dashboard_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_32.addItem(self.verticalSpacer)


        self.verticalLayout_10.addWidget(self.widget)


        self.LeftMenu.addWidget(self.LeftMenuFrame)

        self.LeftMenuFrame_2 = QFrame(self.centralwidget)
        self.LeftMenuFrame_2.setObjectName(u"LeftMenuFrame_2")
        sizePolicy4.setHeightForWidth(self.LeftMenuFrame_2.sizePolicy().hasHeightForWidth())
        self.LeftMenuFrame_2.setSizePolicy(sizePolicy4)
        self.LeftMenuFrame_2.setMinimumSize(QSize(270, 0))
        self.LeftMenuFrame_2.setMaximumSize(QSize(270, 16777215))
        font3 = QFont()
        font3.setFamilies([u"Roboto"])
        font3.setBold(True)
        self.LeftMenuFrame_2.setFont(font3)
        self.LeftMenuFrame_2.setStyleSheet(u"QFrame#LeftMenuFrame_2 {\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_9 = QVBoxLayout(self.LeftMenuFrame_2)
        self.verticalLayout_9.setSpacing(5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 10, 5, 10)
        self.menu_btn_2 = QPushButton(self.LeftMenuFrame_2)
        self.menu_btn_2.setObjectName(u"menu_btn_2")
        sizePolicy5.setHeightForWidth(self.menu_btn_2.sizePolicy().hasHeightForWidth())
        self.menu_btn_2.setSizePolicy(sizePolicy5)
        self.menu_btn_2.setMinimumSize(QSize(20, 20))
        self.menu_btn_2.setMaximumSize(QSize(20, 20))
        self.menu_btn_2.setFont(font2)
#if QT_CONFIG(statustip)
        self.menu_btn_2.setStatusTip(u"")
#endif // QT_CONFIG(statustip)
        self.menu_btn_2.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 255, 255);\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"	/*border: 2px solid black;*/\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(221, 230, 237, 255)\n"
"}")
        icon13 = QIcon()
        icon13.addFile(u":/icon/icons/left_arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_btn_2.setIcon(icon13)
        self.menu_btn_2.setIconSize(QSize(15, 15))
        self.menu_btn_2.setCheckable(True)
        self.menu_btn_2.setChecked(False)
        self.menu_btn_2.setAutoExclusive(False)
        self.menu_btn_2.setAutoDefault(False)
        self.menu_btn_2.setFlat(False)

        self.verticalLayout_9.addWidget(self.menu_btn_2, 0, Qt.AlignLeft)

        self.widget_2 = QWidget(self.LeftMenuFrame_2)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_31 = QVBoxLayout(self.widget_2)
        self.verticalLayout_31.setSpacing(5)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.home_btn_2 = QPushButton(self.widget_2)
        self.home_btn_2.setObjectName(u"home_btn_2")
        sizePolicy5.setHeightForWidth(self.home_btn_2.sizePolicy().hasHeightForWidth())
        self.home_btn_2.setSizePolicy(sizePolicy5)
        self.home_btn_2.setMinimumSize(QSize(260, 40))
        self.home_btn_2.setMaximumSize(QSize(260, 40))
        self.home_btn_2.setFont(font2)
        self.home_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10 px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(197, 223, 248, 255), stop:1 rgba(120, 149, 203, 255));\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(197, 223, 248, 255), stop:1 rgba(120, 149, 203, 255));\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}\n"
"")
        self.home_btn_2.setIcon(icon7)
        self.home_btn_2.setIconSize(QSize(20, 20))
        self.home_btn_2.setCheckable(True)
        self.home_btn_2.setChecked(False)
        self.home_btn_2.setAutoExclusive(True)
        self.home_btn_2.setAutoDefault(False)
        self.home_btn_2.setFlat(False)

        self.verticalLayout_31.addWidget(self.home_btn_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_31.addItem(self.verticalSpacer_2)

        self.profile_btn_2 = QPushButton(self.widget_2)
        self.profile_btn_2.setObjectName(u"profile_btn_2")
        sizePolicy5.setHeightForWidth(self.profile_btn_2.sizePolicy().hasHeightForWidth())
        self.profile_btn_2.setSizePolicy(sizePolicy5)
        self.profile_btn_2.setMinimumSize(QSize(260, 40))
        self.profile_btn_2.setMaximumSize(QSize(260, 40))
        self.profile_btn_2.setFont(font2)
        self.profile_btn_2.setAcceptDrops(False)
        self.profile_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10 px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(252, 252, 232, 255), stop:1 rgba(253, 233, 104, 255));\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(252, 252, 232, 255), stop:1 rgba(253, 233, 104, 255));\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}\n"
"")
        self.profile_btn_2.setIcon(icon8)
        self.profile_btn_2.setIconSize(QSize(20, 20))
        self.profile_btn_2.setCheckable(True)
        self.profile_btn_2.setAutoExclusive(True)
        self.profile_btn_2.setFlat(False)

        self.verticalLayout_31.addWidget(self.profile_btn_2)

        self.analysis_btn_2 = QPushButton(self.widget_2)
        self.analysis_btn_2.setObjectName(u"analysis_btn_2")
        sizePolicy5.setHeightForWidth(self.analysis_btn_2.sizePolicy().hasHeightForWidth())
        self.analysis_btn_2.setSizePolicy(sizePolicy5)
        self.analysis_btn_2.setMinimumSize(QSize(260, 40))
        self.analysis_btn_2.setMaximumSize(QSize(260, 40))
        self.analysis_btn_2.setFont(font2)
        self.analysis_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	 background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(145, 145, 145, 255), stop:0 rgba(245, 245, 245, 255));\n"
"	border: 2px solid black;\n"
"}\n"
"QPushButton:hover {\n"
"	 background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(145, 145, 145, 255), stop:0 rgba(245, 245, 245, 255));\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        self.analysis_btn_2.setIcon(icon9)
        self.analysis_btn_2.setIconSize(QSize(20, 20))
        self.analysis_btn_2.setCheckable(True)
        self.analysis_btn_2.setChecked(False)
        self.analysis_btn_2.setAutoExclusive(True)

        self.verticalLayout_31.addWidget(self.analysis_btn_2)

        self.Situation_selection_Layout = QHBoxLayout()
        self.Situation_selection_Layout.setSpacing(5)
        self.Situation_selection_Layout.setObjectName(u"Situation_selection_Layout")
        self.Situation_selection_Layout.setContentsMargins(10, -1, -1, -1)
        self.Situation_selection_Label = QLabel(self.widget_2)
        self.Situation_selection_Label.setObjectName(u"Situation_selection_Label")
        font4 = QFont()
        font4.setBold(True)
        self.Situation_selection_Label.setFont(font4)

        self.Situation_selection_Layout.addWidget(self.Situation_selection_Label)

        self.Situation_selection_Combobox = QComboBox(self.widget_2)
        self.Situation_selection_Combobox.setObjectName(u"Situation_selection_Combobox")
        self.Situation_selection_Combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.Situation_selection_Layout.addWidget(self.Situation_selection_Combobox)

        self.Situation_selection_Layout.setStretch(1, 1)

        self.verticalLayout_31.addLayout(self.Situation_selection_Layout)

        self.verticalSpacer_14 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_31.addItem(self.verticalSpacer_14)

        self.functional_btn_2 = QPushButton(self.widget_2)
        self.functional_btn_2.setObjectName(u"functional_btn_2")
        sizePolicy5.setHeightForWidth(self.functional_btn_2.sizePolicy().hasHeightForWidth())
        self.functional_btn_2.setSizePolicy(sizePolicy5)
        self.functional_btn_2.setMinimumSize(QSize(260, 40))
        self.functional_btn_2.setMaximumSize(QSize(260, 40))
        self.functional_btn_2.setFont(font2)
        self.functional_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	 background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(193, 208, 181, 255), stop:0 rgba(228, 247, 233, 255));\n"
"	border: 2px solid black;\n"
"}\n"
"QPushButton:hover	 {\n"
"	 background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(193, 208, 181, 255), stop:0 rgba(228, 247, 233, 255));\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        self.functional_btn_2.setIcon(icon10)
        self.functional_btn_2.setIconSize(QSize(20, 20))
        self.functional_btn_2.setCheckable(True)
        self.functional_btn_2.setChecked(False)
        self.functional_btn_2.setAutoExclusive(True)

        self.verticalLayout_31.addWidget(self.functional_btn_2)

        self.performance_btn_2 = QPushButton(self.widget_2)
        self.performance_btn_2.setObjectName(u"performance_btn_2")
        sizePolicy5.setHeightForWidth(self.performance_btn_2.sizePolicy().hasHeightForWidth())
        self.performance_btn_2.setSizePolicy(sizePolicy5)
        self.performance_btn_2.setMinimumSize(QSize(260, 40))
        self.performance_btn_2.setMaximumSize(QSize(260, 40))
        self.performance_btn_2.setFont(font2)
        self.performance_btn_2.setAcceptDrops(True)
        self.performance_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(250, 152, 132, 255), stop:0 rgba(255, 243, 226, 255));\n"
"	border: 2px solid black;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(250, 152, 132, 255), stop:0 rgba(255, 243, 226, 255));\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        self.performance_btn_2.setIcon(icon11)
        self.performance_btn_2.setIconSize(QSize(20, 20))
        self.performance_btn_2.setCheckable(True)
        self.performance_btn_2.setAutoExclusive(True)

        self.verticalLayout_31.addWidget(self.performance_btn_2)

        self.dashboard_btn_2 = QPushButton(self.widget_2)
        self.dashboard_btn_2.setObjectName(u"dashboard_btn_2")
        sizePolicy5.setHeightForWidth(self.dashboard_btn_2.sizePolicy().hasHeightForWidth())
        self.dashboard_btn_2.setSizePolicy(sizePolicy5)
        self.dashboard_btn_2.setMinimumSize(QSize(260, 40))
        self.dashboard_btn_2.setMaximumSize(QSize(260, 40))
        self.dashboard_btn_2.setFont(font2)
        self.dashboard_btn_2.setAcceptDrops(True)
        self.dashboard_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 0px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(86, 157, 170, 255), stop:0 rgba(218, 238, 236, 255));\n"
"	border: 2px solid black;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(86, 157, 170, 255), stop:0 rgba(218, 238, 236, 255));\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid;\n"
"	border-color: rgb(200, 200, 200);\n"
"}")
        self.dashboard_btn_2.setIcon(icon12)
        self.dashboard_btn_2.setIconSize(QSize(20, 20))
        self.dashboard_btn_2.setCheckable(True)
        self.dashboard_btn_2.setAutoExclusive(True)

        self.verticalLayout_31.addWidget(self.dashboard_btn_2)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_31.addItem(self.verticalSpacer_8)


        self.verticalLayout_9.addWidget(self.widget_2)


        self.LeftMenu.addWidget(self.LeftMenuFrame_2)


        self.Org1_Body.addLayout(self.LeftMenu)

        self.BodyWidget = QStackedWidget(self.centralwidget)
        self.BodyWidget.setObjectName(u"BodyWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.BodyWidget.sizePolicy().hasHeightForWidth())
        self.BodyWidget.setSizePolicy(sizePolicy6)
        self.Page0_Home = QWidget()
        self.Page0_Home.setObjectName(u"Page0_Home")
        self.verticalLayout_2 = QVBoxLayout(self.Page0_Home)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 0, 0, 5)
        self.Home_Top_Widget = QWidget(self.Page0_Home)
        self.Home_Top_Widget.setObjectName(u"Home_Top_Widget")
        self.Home_Top_Widget.setMinimumSize(QSize(0, 50))
        self.Home_Top_Widget.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout_3 = QVBoxLayout(self.Home_Top_Widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.Home_Top_Widget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background-color: #7895CB;\n"
"border-top-left-radius: 20px;\n"
"border-top-right-radius: 20px;\n"
"")
        self.label.setTextFormat(Qt.RichText)

        self.verticalLayout_3.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.Home_Top_Widget)

        self.Home_Content_Widget = QWidget(self.Page0_Home)
        self.Home_Content_Widget.setObjectName(u"Home_Content_Widget")
        self.Home_Content_Widget.setStyleSheet(u"background-color: #C5DFF8;\n"
"border-bottom-right-radius: 20px;\n"
"border-bottom-left-radius: 20px;")
        self.verticalLayout = QVBoxLayout(self.Home_Content_Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.Home_Label1 = QLabel(self.Home_Content_Widget)
        self.Home_Label1.setObjectName(u"Home_Label1")
        self.Home_Label1.setAlignment(Qt.AlignJustify|Qt.AlignTop)
        self.Home_Label1.setWordWrap(True)

        self.verticalLayout.addWidget(self.Home_Label1)

        self.Resilience2 = QWidget(self.Home_Content_Widget)
        self.Resilience2.setObjectName(u"Resilience2")
        self.horizontalLayout_3 = QHBoxLayout(self.Resilience2)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.Home_Label1_2 = QLabel(self.Resilience2)
        self.Home_Label1_2.setObjectName(u"Home_Label1_2")
        self.Home_Label1_2.setAlignment(Qt.AlignJustify|Qt.AlignTop)
        self.Home_Label1_2.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.Home_Label1_2)

        self.label_2 = QLabel(self.Resilience2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setPixmap(QPixmap(u":/images/images/Asset 1.png"))
        self.label_2.setScaledContents(False)

        self.horizontalLayout_3.addWidget(self.label_2, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.horizontalLayout_3.setStretch(0, 1)

        self.verticalLayout.addWidget(self.Resilience2)

        self.verticalLayout.setStretch(1, 1)

        self.verticalLayout_2.addWidget(self.Home_Content_Widget)

        self.BodyWidget.addWidget(self.Page0_Home)
        self.Page1_Profile = QWidget()
        self.Page1_Profile.setObjectName(u"Page1_Profile")
        self.horizontalLayout_7 = QHBoxLayout(self.Page1_Profile)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.Col1 = QWidget(self.Page1_Profile)
        self.Col1.setObjectName(u"Col1")
        sizePolicy6.setHeightForWidth(self.Col1.sizePolicy().hasHeightForWidth())
        self.Col1.setSizePolicy(sizePolicy6)
        self.Col1.setStyleSheet(u"")
        self.verticalLayout_11 = QVBoxLayout(self.Col1)
        self.verticalLayout_11.setSpacing(10)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.Domain_Frame = QFrame(self.Col1)
        self.Domain_Frame.setObjectName(u"Domain_Frame")
        self.Domain_Frame.setStyleSheet(u"QFrame{\n"
"background-color: #FFFADD;\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_14 = QVBoxLayout(self.Domain_Frame)
        self.verticalLayout_14.setSpacing(10)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(10, 10, 10, 10)
        self.Domain_Label = QLabel(self.Domain_Frame)
        self.Domain_Label.setObjectName(u"Domain_Label")
        self.Domain_Label.setEnabled(True)
        self.Domain_Label.setMinimumSize(QSize(0, 20))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(10)
        self.Domain_Label.setFont(font5)
        self.Domain_Label.setStyleSheet(u"background-color: #ffcc33;	\n"
"border-radius: 10px")

        self.verticalLayout_14.addWidget(self.Domain_Label)

        self.widget_34 = QWidget(self.Domain_Frame)
        self.widget_34.setObjectName(u"widget_34")
        self.verticalLayout_29 = QVBoxLayout(self.widget_34)
        self.verticalLayout_29.setSpacing(2)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(1, 1, 1, 1)
        self.Domain_Form = QFormLayout()
        self.Domain_Form.setObjectName(u"Domain_Form")
        self.Domain_Form.setHorizontalSpacing(5)
        self.Domain_Form.setVerticalSpacing(5)
        self.Location_Label = QLabel(self.widget_34)
        self.Location_Label.setObjectName(u"Location_Label")
        font6 = QFont()
        font6.setFamilies([u"Segoe UI Variable Text Semiligh"])
        font6.setBold(True)
        self.Location_Label.setFont(font6)
        self.Location_Label.setTextFormat(Qt.PlainText)

        self.Domain_Form.setWidget(2, QFormLayout.LabelRole, self.Location_Label)

        self.Country_Label = QLabel(self.widget_34)
        self.Country_Label.setObjectName(u"Country_Label")

        self.Domain_Form.setWidget(3, QFormLayout.LabelRole, self.Country_Label)

        self.Country__LineEdit = QLineEdit(self.widget_34)
        self.Country__LineEdit.setObjectName(u"Country__LineEdit")
        self.Country__LineEdit.setStyleSheet(u"background-color: white")
        self.Country__LineEdit.setAlignment(Qt.AlignCenter)

        self.Domain_Form.setWidget(3, QFormLayout.FieldRole, self.Country__LineEdit)

        self.City_Label = QLabel(self.widget_34)
        self.City_Label.setObjectName(u"City_Label")

        self.Domain_Form.setWidget(4, QFormLayout.LabelRole, self.City_Label)

        self.City__LineEdit = QLineEdit(self.widget_34)
        self.City__LineEdit.setObjectName(u"City__LineEdit")
        self.City__LineEdit.setStyleSheet(u"background-color: white")
        self.City__LineEdit.setAlignment(Qt.AlignCenter)

        self.Domain_Form.setWidget(4, QFormLayout.FieldRole, self.City__LineEdit)

        self.Cat_Label = QLabel(self.widget_34)
        self.Cat_Label.setObjectName(u"Cat_Label")
        self.Cat_Label.setFont(font6)
        self.Cat_Label.setTextFormat(Qt.PlainText)

        self.Domain_Form.setWidget(5, QFormLayout.LabelRole, self.Cat_Label)

        self.CatName_Label = QLabel(self.widget_34)
        self.CatName_Label.setObjectName(u"CatName_Label")

        self.Domain_Form.setWidget(6, QFormLayout.LabelRole, self.CatName_Label)

        self.CatName_LineEdit = QLineEdit(self.widget_34)
        self.CatName_LineEdit.setObjectName(u"CatName_LineEdit")
        self.CatName_LineEdit.setStyleSheet(u"background-color: white")
        self.CatName_LineEdit.setAlignment(Qt.AlignCenter)

        self.Domain_Form.setWidget(6, QFormLayout.FieldRole, self.CatName_LineEdit)

        self.CatArea_Label = QLabel(self.widget_34)
        self.CatArea_Label.setObjectName(u"CatArea_Label")

        self.Domain_Form.setWidget(7, QFormLayout.LabelRole, self.CatArea_Label)

        self.CatArea_LineEdit = QLineEdit(self.widget_34)
        self.CatArea_LineEdit.setObjectName(u"CatArea_LineEdit")
        self.CatArea_LineEdit.setStyleSheet(u"background-color: white")
        self.CatArea_LineEdit.setFrame(True)
        self.CatArea_LineEdit.setAlignment(Qt.AlignCenter)

        self.Domain_Form.setWidget(7, QFormLayout.FieldRole, self.CatArea_LineEdit)

        self.CatImp_Label = QLabel(self.widget_34)
        self.CatImp_Label.setObjectName(u"CatImp_Label")

        self.Domain_Form.setWidget(8, QFormLayout.LabelRole, self.CatImp_Label)

        self.CatImp_LineEdit = QLineEdit(self.widget_34)
        self.CatImp_LineEdit.setObjectName(u"CatImp_LineEdit")
        self.CatImp_LineEdit.setStyleSheet(u"background-color: white")
        self.CatImp_LineEdit.setAlignment(Qt.AlignCenter)

        self.Domain_Form.setWidget(8, QFormLayout.FieldRole, self.CatImp_LineEdit)

        self.CatSlope_Label = QLabel(self.widget_34)
        self.CatSlope_Label.setObjectName(u"CatSlope_Label")

        self.Domain_Form.setWidget(9, QFormLayout.LabelRole, self.CatSlope_Label)

        self.CatSlope_LineEdit = QLineEdit(self.widget_34)
        self.CatSlope_LineEdit.setObjectName(u"CatSlope_LineEdit")
        self.CatSlope_LineEdit.setStyleSheet(u"background-color: white")
        self.CatSlope_LineEdit.setAlignment(Qt.AlignCenter)

        self.Domain_Form.setWidget(9, QFormLayout.FieldRole, self.CatSlope_LineEdit)

        self.StudyName_Label = QLabel(self.widget_34)
        self.StudyName_Label.setObjectName(u"StudyName_Label")

        self.Domain_Form.setWidget(1, QFormLayout.LabelRole, self.StudyName_Label)

        self.StudyName_LineEdit = QLineEdit(self.widget_34)
        self.StudyName_LineEdit.setObjectName(u"StudyName_LineEdit")
        self.StudyName_LineEdit.setStyleSheet(u"")
        self.StudyName_LineEdit.setAlignment(Qt.AlignCenter)

        self.Domain_Form.setWidget(1, QFormLayout.FieldRole, self.StudyName_LineEdit)

        self.Study_Label = QLabel(self.widget_34)
        self.Study_Label.setObjectName(u"Study_Label")
        self.Study_Label.setFont(font6)

        self.Domain_Form.setWidget(0, QFormLayout.LabelRole, self.Study_Label)


        self.verticalLayout_29.addLayout(self.Domain_Form)


        self.verticalLayout_14.addWidget(self.widget_34)


        self.verticalLayout_11.addWidget(self.Domain_Frame)

        self.Population_Frame = QFrame(self.Col1)
        self.Population_Frame.setObjectName(u"Population_Frame")
        self.Population_Frame.setStyleSheet(u"QFrame{\n"
"background-color: #FFFADD;\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_15 = QVBoxLayout(self.Population_Frame)
        self.verticalLayout_15.setSpacing(10)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.Population_Label = QLabel(self.Population_Frame)
        self.Population_Label.setObjectName(u"Population_Label")
        self.Population_Label.setMinimumSize(QSize(0, 20))
        font7 = QFont()
        font7.setPointSize(10)
        self.Population_Label.setFont(font7)
        self.Population_Label.setStyleSheet(u"background-color: #ffcc33;	\n"
"border-radius: 10px")

        self.verticalLayout_15.addWidget(self.Population_Label)

        self.Gender_Widget = QWidget(self.Population_Frame)
        self.Gender_Widget.setObjectName(u"Gender_Widget")
        self.verticalLayout_4 = QVBoxLayout(self.Gender_Widget)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(1, 1, 1, 1)
        self.Gender_Label = QLabel(self.Gender_Widget)
        self.Gender_Label.setObjectName(u"Gender_Label")
        self.Gender_Label.setFont(font6)
        self.Gender_Label.setTextFormat(Qt.PlainText)

        self.verticalLayout_4.addWidget(self.Gender_Label)

        self.GenderContent_Widget = QWidget(self.Gender_Widget)
        self.GenderContent_Widget.setObjectName(u"GenderContent_Widget")
        self.horizontalLayout_8 = QHBoxLayout(self.GenderContent_Widget)
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(1, 1, 1, 1)
        self.GenderPlot_Widget = QWidget(self.GenderContent_Widget)
        self.GenderPlot_Widget.setObjectName(u"GenderPlot_Widget")

        self.horizontalLayout_8.addWidget(self.GenderPlot_Widget)

        self.Gender_Form = QFormLayout()
        self.Gender_Form.setObjectName(u"Gender_Form")
        self.Gender_Form.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Male_Label = QLabel(self.GenderContent_Widget)
        self.Male_Label.setObjectName(u"Male_Label")

        self.Gender_Form.setWidget(0, QFormLayout.LabelRole, self.Male_Label)

        self.Male_LineEdit = QLineEdit(self.GenderContent_Widget)
        self.Male_LineEdit.setObjectName(u"Male_LineEdit")
        self.Male_LineEdit.setStyleSheet(u"background-color: white")
        self.Male_LineEdit.setAlignment(Qt.AlignCenter)

        self.Gender_Form.setWidget(0, QFormLayout.FieldRole, self.Male_LineEdit)

        self.Female_Label = QLabel(self.GenderContent_Widget)
        self.Female_Label.setObjectName(u"Female_Label")

        self.Gender_Form.setWidget(1, QFormLayout.LabelRole, self.Female_Label)

        self.Female_LineEdit = QLineEdit(self.GenderContent_Widget)
        self.Female_LineEdit.setObjectName(u"Female_LineEdit")
        self.Female_LineEdit.setStyleSheet(u"background-color: white")
        self.Female_LineEdit.setAlignment(Qt.AlignCenter)

        self.Gender_Form.setWidget(1, QFormLayout.FieldRole, self.Female_LineEdit)

        self.Other_Label = QLabel(self.GenderContent_Widget)
        self.Other_Label.setObjectName(u"Other_Label")

        self.Gender_Form.setWidget(2, QFormLayout.LabelRole, self.Other_Label)

        self.Other_LineEdit = QLineEdit(self.GenderContent_Widget)
        self.Other_LineEdit.setObjectName(u"Other_LineEdit")
        self.Other_LineEdit.setStyleSheet(u"background-color: white")
        self.Other_LineEdit.setAlignment(Qt.AlignCenter)

        self.Gender_Form.setWidget(2, QFormLayout.FieldRole, self.Other_LineEdit)


        self.horizontalLayout_8.addLayout(self.Gender_Form)


        self.verticalLayout_4.addWidget(self.GenderContent_Widget)


        self.verticalLayout_15.addWidget(self.Gender_Widget)

        self.verticalSpacer_11 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_15.addItem(self.verticalSpacer_11)

        self.Age_Widget = QWidget(self.Population_Frame)
        self.Age_Widget.setObjectName(u"Age_Widget")
        self.verticalLayout_16 = QVBoxLayout(self.Age_Widget)
        self.verticalLayout_16.setSpacing(2)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(1, 1, 1, 1)
        self.Age_Label = QLabel(self.Age_Widget)
        self.Age_Label.setObjectName(u"Age_Label")
        self.Age_Label.setFont(font6)
        self.Age_Label.setTextFormat(Qt.PlainText)

        self.verticalLayout_16.addWidget(self.Age_Label)

        self.widget_11 = QWidget(self.Age_Widget)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(1, 1, 1, 1)
        self.AgePlot_Widget = QWidget(self.widget_11)
        self.AgePlot_Widget.setObjectName(u"AgePlot_Widget")

        self.horizontalLayout_9.addWidget(self.AgePlot_Widget)

        self.Age_Form = QFormLayout()
        self.Age_Form.setObjectName(u"Age_Form")
        self.Age_Form.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Age1_Label = QLabel(self.widget_11)
        self.Age1_Label.setObjectName(u"Age1_Label")

        self.Age_Form.setWidget(0, QFormLayout.LabelRole, self.Age1_Label)

        self.Age1_LineEdit = QLineEdit(self.widget_11)
        self.Age1_LineEdit.setObjectName(u"Age1_LineEdit")
        self.Age1_LineEdit.setStyleSheet(u"background-color: white")
        self.Age1_LineEdit.setAlignment(Qt.AlignCenter)

        self.Age_Form.setWidget(0, QFormLayout.FieldRole, self.Age1_LineEdit)

        self.Age2_Label = QLabel(self.widget_11)
        self.Age2_Label.setObjectName(u"Age2_Label")

        self.Age_Form.setWidget(1, QFormLayout.LabelRole, self.Age2_Label)

        self.Age2_LineEdit = QLineEdit(self.widget_11)
        self.Age2_LineEdit.setObjectName(u"Age2_LineEdit")
        self.Age2_LineEdit.setStyleSheet(u"background-color: white")
        self.Age2_LineEdit.setAlignment(Qt.AlignCenter)

        self.Age_Form.setWidget(1, QFormLayout.FieldRole, self.Age2_LineEdit)

        self.Age3_Label = QLabel(self.widget_11)
        self.Age3_Label.setObjectName(u"Age3_Label")

        self.Age_Form.setWidget(2, QFormLayout.LabelRole, self.Age3_Label)

        self.Age3_LineEdit = QLineEdit(self.widget_11)
        self.Age3_LineEdit.setObjectName(u"Age3_LineEdit")
        self.Age3_LineEdit.setStyleSheet(u"background-color: white")
        self.Age3_LineEdit.setAlignment(Qt.AlignCenter)

        self.Age_Form.setWidget(2, QFormLayout.FieldRole, self.Age3_LineEdit)

        self.Age4_Label = QLabel(self.widget_11)
        self.Age4_Label.setObjectName(u"Age4_Label")

        self.Age_Form.setWidget(3, QFormLayout.LabelRole, self.Age4_Label)

        self.Age4_LineEdit = QLineEdit(self.widget_11)
        self.Age4_LineEdit.setObjectName(u"Age4_LineEdit")
        self.Age4_LineEdit.setStyleSheet(u"background-color: white")
        self.Age4_LineEdit.setAlignment(Qt.AlignCenter)

        self.Age_Form.setWidget(3, QFormLayout.FieldRole, self.Age4_LineEdit)


        self.horizontalLayout_9.addLayout(self.Age_Form)


        self.verticalLayout_16.addWidget(self.widget_11)


        self.verticalLayout_15.addWidget(self.Age_Widget)

        self.verticalLayout_15.setStretch(1, 1)
        self.verticalLayout_15.setStretch(3, 1)

        self.verticalLayout_11.addWidget(self.Population_Frame)


        self.horizontalLayout_7.addWidget(self.Col1)

        self.horizontalSpacer_2 = QSpacerItem(47, 581, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.Col2 = QWidget(self.Page1_Profile)
        self.Col2.setObjectName(u"Col2")
        sizePolicy6.setHeightForWidth(self.Col2.sizePolicy().hasHeightForWidth())
        self.Col2.setSizePolicy(sizePolicy6)
        self.verticalLayout_12 = QVBoxLayout(self.Col2)
        self.verticalLayout_12.setSpacing(10)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.Climate_Frame = QFrame(self.Col2)
        self.Climate_Frame.setObjectName(u"Climate_Frame")
        self.Climate_Frame.setStyleSheet(u"QFrame{\n"
"background-color: #FFFADD;\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_34 = QVBoxLayout(self.Climate_Frame)
        self.verticalLayout_34.setSpacing(10)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(10, 10, 10, 10)
        self.Climate_Label = QLabel(self.Climate_Frame)
        self.Climate_Label.setObjectName(u"Climate_Label")
        self.Climate_Label.setMinimumSize(QSize(0, 20))
        self.Climate_Label.setFont(font7)
        self.Climate_Label.setStyleSheet(u"background-color: #ffcc33;	\n"
"border-radius: 10px")

        self.verticalLayout_34.addWidget(self.Climate_Label)

        self.Temperature_Widget = QWidget(self.Climate_Frame)
        self.Temperature_Widget.setObjectName(u"Temperature_Widget")
        self.verticalLayout_36 = QVBoxLayout(self.Temperature_Widget)
        self.verticalLayout_36.setSpacing(2)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(1, 1, 1, 1)
        self.Temperature_Label = QLabel(self.Temperature_Widget)
        self.Temperature_Label.setObjectName(u"Temperature_Label")
        self.Temperature_Label.setFont(font6)
        self.Temperature_Label.setTextFormat(Qt.PlainText)

        self.verticalLayout_36.addWidget(self.Temperature_Label)

        self.TemperatureContent_Widget = QWidget(self.Temperature_Widget)
        self.TemperatureContent_Widget.setObjectName(u"TemperatureContent_Widget")
        self.TemperatureContent_ = QHBoxLayout(self.TemperatureContent_Widget)
        self.TemperatureContent_.setSpacing(5)
        self.TemperatureContent_.setObjectName(u"TemperatureContent_")
        self.TemperatureContent_.setContentsMargins(1, 1, 1, 1)
        self.Temperature_Picture = QLabel(self.TemperatureContent_Widget)
        self.Temperature_Picture.setObjectName(u"Temperature_Picture")
        self.Temperature_Picture.setPixmap(QPixmap(u":/Profiles/icons/icons8-thermometer-60.png"))
        self.Temperature_Picture.setScaledContents(False)

        self.TemperatureContent_.addWidget(self.Temperature_Picture)

        self.Temperature_Form = QFormLayout()
        self.Temperature_Form.setObjectName(u"Temperature_Form")
        self.Temperature_Form.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Temperature_Form.setVerticalSpacing(5)
        self.TempMonthMax_Label = QLabel(self.TemperatureContent_Widget)
        self.TempMonthMax_Label.setObjectName(u"TempMonthMax_Label")

        self.Temperature_Form.setWidget(0, QFormLayout.LabelRole, self.TempMonthMax_Label)

        self.TempMonthMax_LineEdit = QLineEdit(self.TemperatureContent_Widget)
        self.TempMonthMax_LineEdit.setObjectName(u"TempMonthMax_LineEdit")
        self.TempMonthMax_LineEdit.setStyleSheet(u"background-color: white")
        self.TempMonthMax_LineEdit.setAlignment(Qt.AlignCenter)

        self.Temperature_Form.setWidget(0, QFormLayout.FieldRole, self.TempMonthMax_LineEdit)

        self.TempMonthMean_Label = QLabel(self.TemperatureContent_Widget)
        self.TempMonthMean_Label.setObjectName(u"TempMonthMean_Label")

        self.Temperature_Form.setWidget(1, QFormLayout.LabelRole, self.TempMonthMean_Label)

        self.TempMonthMean_LineEdit = QLineEdit(self.TemperatureContent_Widget)
        self.TempMonthMean_LineEdit.setObjectName(u"TempMonthMean_LineEdit")
        self.TempMonthMean_LineEdit.setStyleSheet(u"background-color: white")
        self.TempMonthMean_LineEdit.setAlignment(Qt.AlignCenter)

        self.Temperature_Form.setWidget(1, QFormLayout.FieldRole, self.TempMonthMean_LineEdit)

        self.TempMonthlyMin_Label = QLabel(self.TemperatureContent_Widget)
        self.TempMonthlyMin_Label.setObjectName(u"TempMonthlyMin_Label")

        self.Temperature_Form.setWidget(2, QFormLayout.LabelRole, self.TempMonthlyMin_Label)

        self.TempMonthlyMin_LineEdit = QLineEdit(self.TemperatureContent_Widget)
        self.TempMonthlyMin_LineEdit.setObjectName(u"TempMonthlyMin_LineEdit")
        self.TempMonthlyMin_LineEdit.setStyleSheet(u"background-color: white")
        self.TempMonthlyMin_LineEdit.setAlignment(Qt.AlignCenter)

        self.Temperature_Form.setWidget(2, QFormLayout.FieldRole, self.TempMonthlyMin_LineEdit)


        self.TemperatureContent_.addLayout(self.Temperature_Form)

        self.TemperatureContent_.setStretch(1, 1)

        self.verticalLayout_36.addWidget(self.TemperatureContent_Widget)


        self.verticalLayout_34.addWidget(self.Temperature_Widget)

        self.verticalSpacer_13 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_34.addItem(self.verticalSpacer_13)

        self.Rainfall_Widget = QWidget(self.Climate_Frame)
        self.Rainfall_Widget.setObjectName(u"Rainfall_Widget")
        self.verticalLayout_37 = QVBoxLayout(self.Rainfall_Widget)
        self.verticalLayout_37.setSpacing(2)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(1, 1, 1, 1)
        self.Rainfall_Label = QLabel(self.Rainfall_Widget)
        self.Rainfall_Label.setObjectName(u"Rainfall_Label")
        self.Rainfall_Label.setFont(font6)
        self.Rainfall_Label.setTextFormat(Qt.PlainText)

        self.verticalLayout_37.addWidget(self.Rainfall_Label)

        self.RainfallContent_Widget = QWidget(self.Rainfall_Widget)
        self.RainfallContent_Widget.setObjectName(u"RainfallContent_Widget")
        self.horizontalLayout_14 = QHBoxLayout(self.RainfallContent_Widget)
        self.horizontalLayout_14.setSpacing(5)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(1, 1, 1, 1)
        self.Rainfall_Picture = QLabel(self.RainfallContent_Widget)
        self.Rainfall_Picture.setObjectName(u"Rainfall_Picture")
        self.Rainfall_Picture.setPixmap(QPixmap(u":/Profiles/icons/rain-64.ico"))
        self.Rainfall_Picture.setScaledContents(False)

        self.horizontalLayout_14.addWidget(self.Rainfall_Picture)

        self.Rainfall_Form = QFormLayout()
        self.Rainfall_Form.setObjectName(u"Rainfall_Form")
        self.Rainfall_Form.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Rainfall_Form.setVerticalSpacing(5)
        self.RainAnnualMean_Label = QLabel(self.RainfallContent_Widget)
        self.RainAnnualMean_Label.setObjectName(u"RainAnnualMean_Label")

        self.Rainfall_Form.setWidget(0, QFormLayout.LabelRole, self.RainAnnualMean_Label)

        self.RainAnnualMean_LineEdit = QLineEdit(self.RainfallContent_Widget)
        self.RainAnnualMean_LineEdit.setObjectName(u"RainAnnualMean_LineEdit")
        self.RainAnnualMean_LineEdit.setStyleSheet(u"background-color: white")
        self.RainAnnualMean_LineEdit.setAlignment(Qt.AlignCenter)

        self.Rainfall_Form.setWidget(0, QFormLayout.FieldRole, self.RainAnnualMean_LineEdit)

        self.RainMonthMax_Label = QLabel(self.RainfallContent_Widget)
        self.RainMonthMax_Label.setObjectName(u"RainMonthMax_Label")

        self.Rainfall_Form.setWidget(1, QFormLayout.LabelRole, self.RainMonthMax_Label)

        self.RainMonthMax_LineEdit = QLineEdit(self.RainfallContent_Widget)
        self.RainMonthMax_LineEdit.setObjectName(u"RainMonthMax_LineEdit")
        self.RainMonthMax_LineEdit.setStyleSheet(u"background-color: white")
        self.RainMonthMax_LineEdit.setAlignment(Qt.AlignCenter)

        self.Rainfall_Form.setWidget(1, QFormLayout.FieldRole, self.RainMonthMax_LineEdit)

        self.RainMonthMean_Label = QLabel(self.RainfallContent_Widget)
        self.RainMonthMean_Label.setObjectName(u"RainMonthMean_Label")

        self.Rainfall_Form.setWidget(2, QFormLayout.LabelRole, self.RainMonthMean_Label)

        self.RainMonthMean_LineEdit = QLineEdit(self.RainfallContent_Widget)
        self.RainMonthMean_LineEdit.setObjectName(u"RainMonthMean_LineEdit")
        self.RainMonthMean_LineEdit.setStyleSheet(u"background-color: white")
        self.RainMonthMean_LineEdit.setAlignment(Qt.AlignCenter)

        self.Rainfall_Form.setWidget(2, QFormLayout.FieldRole, self.RainMonthMean_LineEdit)


        self.horizontalLayout_14.addLayout(self.Rainfall_Form)


        self.verticalLayout_37.addWidget(self.RainfallContent_Widget)


        self.verticalLayout_34.addWidget(self.Rainfall_Widget)


        self.verticalLayout_12.addWidget(self.Climate_Frame)

        self.NBS_Frame = QFrame(self.Col2)
        self.NBS_Frame.setObjectName(u"NBS_Frame")
        self.NBS_Frame.setStyleSheet(u"QFrame{\n"
"background-color: #FFFADD;\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_53 = QVBoxLayout(self.NBS_Frame)
        self.verticalLayout_53.setSpacing(10)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.verticalLayout_53.setContentsMargins(10, 10, 10, 10)
        self.NBS_Label = QLabel(self.NBS_Frame)
        self.NBS_Label.setObjectName(u"NBS_Label")
        self.NBS_Label.setMinimumSize(QSize(0, 20))
        self.NBS_Label.setFont(font7)
        self.NBS_Label.setStyleSheet(u"background-color: #ffcc33;	\n"
"border-radius: 10px")

        self.verticalLayout_53.addWidget(self.NBS_Label)

        self.NBS_Widget = QWidget(self.NBS_Frame)
        self.NBS_Widget.setObjectName(u"NBS_Widget")
        self.verticalLayout_54 = QVBoxLayout(self.NBS_Widget)
        self.verticalLayout_54.setSpacing(2)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.verticalLayout_54.setContentsMargins(1, 1, 1, 1)
        self.NBS_Label_2 = QLabel(self.NBS_Widget)
        self.NBS_Label_2.setObjectName(u"NBS_Label_2")
        self.NBS_Label_2.setFont(font6)
        self.NBS_Label_2.setTextFormat(Qt.PlainText)

        self.verticalLayout_54.addWidget(self.NBS_Label_2)

        self.NBS_Table = QTableWidget(self.NBS_Widget)
        if (self.NBS_Table.columnCount() < 2):
            self.NBS_Table.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.NBS_Table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.NBS_Table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.NBS_Table.setObjectName(u"NBS_Table")
        sizePolicy7 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.NBS_Table.sizePolicy().hasHeightForWidth())
        self.NBS_Table.setSizePolicy(sizePolicy7)
        self.NBS_Table.setStyleSheet(u"")
        self.NBS_Table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.NBS_Table.setAutoScrollMargin(10)
        self.NBS_Table.setAlternatingRowColors(True)
        self.NBS_Table.setShowGrid(True)
        self.NBS_Table.setGridStyle(Qt.SolidLine)
        self.NBS_Table.setSortingEnabled(False)
        self.NBS_Table.setCornerButtonEnabled(True)
        self.NBS_Table.setRowCount(0)
        self.NBS_Table.setColumnCount(2)
        self.NBS_Table.horizontalHeader().setVisible(True)
        self.NBS_Table.horizontalHeader().setCascadingSectionResizes(False)
        self.NBS_Table.horizontalHeader().setMinimumSectionSize(30)
        self.NBS_Table.horizontalHeader().setDefaultSectionSize(100)
        self.NBS_Table.horizontalHeader().setHighlightSections(True)
        self.NBS_Table.horizontalHeader().setProperty("showSortIndicator", False)
        self.NBS_Table.horizontalHeader().setStretchLastSection(True)
        self.NBS_Table.verticalHeader().setVisible(False)
        self.NBS_Table.verticalHeader().setMinimumSectionSize(20)
        self.NBS_Table.verticalHeader().setHighlightSections(False)
        self.NBS_Table.verticalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout_54.addWidget(self.NBS_Table, 0, Qt.AlignHCenter)


        self.verticalLayout_53.addWidget(self.NBS_Widget)


        self.verticalLayout_12.addWidget(self.NBS_Frame)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_6)


        self.horizontalLayout_7.addWidget(self.Col2)

        self.horizontalSpacer_3 = QSpacerItem(47, 581, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.Col3 = QWidget(self.Page1_Profile)
        self.Col3.setObjectName(u"Col3")
        sizePolicy6.setHeightForWidth(self.Col3.sizePolicy().hasHeightForWidth())
        self.Col3.setSizePolicy(sizePolicy6)
        self.Col3.setStyleSheet(u"")
        self.verticalLayout_56 = QVBoxLayout(self.Col3)
        self.verticalLayout_56.setSpacing(10)
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")
        self.verticalLayout_56.setContentsMargins(0, 0, 0, 0)
        self.Service_Frame = QFrame(self.Col3)
        self.Service_Frame.setObjectName(u"Service_Frame")
        self.Service_Frame.setStyleSheet(u"QFrame{\n"
"background-color: rgb(246, 252, 255);\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_48 = QVBoxLayout(self.Service_Frame)
        self.verticalLayout_48.setSpacing(10)
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.verticalLayout_48.setContentsMargins(10, 10, 10, 10)
        self.Service_Label = QLabel(self.Service_Frame)
        self.Service_Label.setObjectName(u"Service_Label")
        self.Service_Label.setMinimumSize(QSize(0, 20))
        self.Service_Label.setFont(font7)
        self.Service_Label.setStyleSheet(u"background-color: #71C7EC;	\n"
"border-radius: 10px")

        self.verticalLayout_48.addWidget(self.Service_Label)

        self.Utility_Widget = QWidget(self.Service_Frame)
        self.Utility_Widget.setObjectName(u"Utility_Widget")
        self.verticalLayout_66 = QVBoxLayout(self.Utility_Widget)
        self.verticalLayout_66.setSpacing(2)
        self.verticalLayout_66.setObjectName(u"verticalLayout_66")
        self.verticalLayout_66.setContentsMargins(1, 1, 1, 1)
        self.label_47 = QLabel(self.Utility_Widget)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font6)
        self.label_47.setTextFormat(Qt.PlainText)

        self.verticalLayout_66.addWidget(self.label_47)

        self.Utility_Forrm = QFormLayout()
        self.Utility_Forrm.setObjectName(u"Utility_Forrm")
        self.Utility_Forrm.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Utility_Forrm.setHorizontalSpacing(5)
        self.Utility_Forrm.setVerticalSpacing(5)
        self.UtilityName_Label = QLabel(self.Utility_Widget)
        self.UtilityName_Label.setObjectName(u"UtilityName_Label")

        self.Utility_Forrm.setWidget(0, QFormLayout.LabelRole, self.UtilityName_Label)

        self.UtilityName_LineEdit = QLineEdit(self.Utility_Widget)
        self.UtilityName_LineEdit.setObjectName(u"UtilityName_LineEdit")
        self.UtilityName_LineEdit.setStyleSheet(u"background-color: white")
        self.UtilityName_LineEdit.setAlignment(Qt.AlignCenter)

        self.Utility_Forrm.setWidget(0, QFormLayout.FieldRole, self.UtilityName_LineEdit)

        self.UtilityType_Label = QLabel(self.Utility_Widget)
        self.UtilityType_Label.setObjectName(u"UtilityType_Label")

        self.Utility_Forrm.setWidget(1, QFormLayout.LabelRole, self.UtilityType_Label)

        self.UtilityType_ComboBox = QComboBox(self.Utility_Widget)
        self.UtilityType_ComboBox.addItem("")
        self.UtilityType_ComboBox.addItem("")
        self.UtilityType_ComboBox.addItem("")
        self.UtilityType_ComboBox.setObjectName(u"UtilityType_ComboBox")
        self.UtilityType_ComboBox.setEditable(False)
        self.UtilityType_ComboBox.setFrame(True)

        self.Utility_Forrm.setWidget(1, QFormLayout.FieldRole, self.UtilityType_ComboBox)


        self.verticalLayout_66.addLayout(self.Utility_Forrm)


        self.verticalLayout_48.addWidget(self.Utility_Widget)


        self.verticalLayout_56.addWidget(self.Service_Frame)

        self.Drainage_Frame = QFrame(self.Col3)
        self.Drainage_Frame.setObjectName(u"Drainage_Frame")
        self.Drainage_Frame.setStyleSheet(u"QFrame{\n"
"background-color: rgb(246, 252, 255);\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_57 = QVBoxLayout(self.Drainage_Frame)
        self.verticalLayout_57.setSpacing(10)
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.verticalLayout_57.setContentsMargins(10, 10, 10, 10)
        self.Drainage_Label = QLabel(self.Drainage_Frame)
        self.Drainage_Label.setObjectName(u"Drainage_Label")
        self.Drainage_Label.setMinimumSize(QSize(0, 20))
        self.Drainage_Label.setFont(font7)
        self.Drainage_Label.setStyleSheet(u"background-color: #71C7EC;\n"
"border-radius: 10px")

        self.verticalLayout_57.addWidget(self.Drainage_Label)

        self.Minor_Widget = QWidget(self.Drainage_Frame)
        self.Minor_Widget.setObjectName(u"Minor_Widget")
        self.verticalLayout_69 = QVBoxLayout(self.Minor_Widget)
        self.verticalLayout_69.setSpacing(2)
        self.verticalLayout_69.setObjectName(u"verticalLayout_69")
        self.verticalLayout_69.setContentsMargins(1, 1, 1, 1)
        self.Minor_Label = QLabel(self.Minor_Widget)
        self.Minor_Label.setObjectName(u"Minor_Label")
        self.Minor_Label.setFont(font6)
        self.Minor_Label.setStyleSheet(u"")
        self.Minor_Label.setTextFormat(Qt.PlainText)

        self.verticalLayout_69.addWidget(self.Minor_Label)

        self.Minor_Form = QFormLayout()
        self.Minor_Form.setObjectName(u"Minor_Form")
        self.Minor_Form.setFormAlignment(Qt.AlignCenter)
        self.Minor_Form.setVerticalSpacing(5)
        self.Minor_Form.setContentsMargins(0, 0, 0, 0)
        self.Type_Label = QLabel(self.Minor_Widget)
        self.Type_Label.setObjectName(u"Type_Label")

        self.Minor_Form.setWidget(0, QFormLayout.LabelRole, self.Type_Label)

        self.SepLenght_Label = QLabel(self.Minor_Widget)
        self.SepLenght_Label.setObjectName(u"SepLenght_Label")

        self.Minor_Form.setWidget(1, QFormLayout.LabelRole, self.SepLenght_Label)

        self.SepLenght_LineEdit = QLineEdit(self.Minor_Widget)
        self.SepLenght_LineEdit.setObjectName(u"SepLenght_LineEdit")
        self.SepLenght_LineEdit.setStyleSheet(u"background-color: white")
        self.SepLenght_LineEdit.setAlignment(Qt.AlignCenter)

        self.Minor_Form.setWidget(1, QFormLayout.FieldRole, self.SepLenght_LineEdit)

        self.CombLenght_Label = QLabel(self.Minor_Widget)
        self.CombLenght_Label.setObjectName(u"CombLenght_Label")

        self.Minor_Form.setWidget(2, QFormLayout.LabelRole, self.CombLenght_Label)

        self.CombLenght_LineEdit = QLineEdit(self.Minor_Widget)
        self.CombLenght_LineEdit.setObjectName(u"CombLenght_LineEdit")
        self.CombLenght_LineEdit.setStyleSheet(u"background-color: white")
        self.CombLenght_LineEdit.setAlignment(Qt.AlignCenter)

        self.Minor_Form.setWidget(2, QFormLayout.FieldRole, self.CombLenght_LineEdit)

        self.Diameter_Label = QLabel(self.Minor_Widget)
        self.Diameter_Label.setObjectName(u"Diameter_Label")

        self.Minor_Form.setWidget(3, QFormLayout.LabelRole, self.Diameter_Label)

        self.Diameter_LineEdit = QLineEdit(self.Minor_Widget)
        self.Diameter_LineEdit.setObjectName(u"Diameter_LineEdit")
        self.Diameter_LineEdit.setStyleSheet(u"background-color: white")
        self.Diameter_LineEdit.setAlignment(Qt.AlignCenter)

        self.Minor_Form.setWidget(3, QFormLayout.FieldRole, self.Diameter_LineEdit)

        self.Age_Label_2 = QLabel(self.Minor_Widget)
        self.Age_Label_2.setObjectName(u"Age_Label_2")

        self.Minor_Form.setWidget(4, QFormLayout.LabelRole, self.Age_Label_2)

        self.Age_LineEdit = QLineEdit(self.Minor_Widget)
        self.Age_LineEdit.setObjectName(u"Age_LineEdit")
        self.Age_LineEdit.setStyleSheet(u"background-color: white")
        self.Age_LineEdit.setAlignment(Qt.AlignCenter)

        self.Minor_Form.setWidget(4, QFormLayout.FieldRole, self.Age_LineEdit)

        self.Outfall_Label = QLabel(self.Minor_Widget)
        self.Outfall_Label.setObjectName(u"Outfall_Label")

        self.Minor_Form.setWidget(5, QFormLayout.LabelRole, self.Outfall_Label)

        self.Outfalls_LineEdit = QLineEdit(self.Minor_Widget)
        self.Outfalls_LineEdit.setObjectName(u"Outfalls_LineEdit")
        self.Outfalls_LineEdit.setStyleSheet(u"background-color: white")
        self.Outfalls_LineEdit.setAlignment(Qt.AlignCenter)

        self.Minor_Form.setWidget(5, QFormLayout.FieldRole, self.Outfalls_LineEdit)

        self.Receiver_Label = QLabel(self.Minor_Widget)
        self.Receiver_Label.setObjectName(u"Receiver_Label")
        self.Receiver_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.Minor_Form.setWidget(6, QFormLayout.LabelRole, self.Receiver_Label)

        self.Receiver_Widget = QWidget(self.Minor_Widget)
        self.Receiver_Widget.setObjectName(u"Receiver_Widget")
        self.verticalLayout_8 = QVBoxLayout(self.Receiver_Widget)
        self.verticalLayout_8.setSpacing(1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.Receiver_Sea = QCheckBox(self.Receiver_Widget)
        self.Receiver_Sea.setObjectName(u"Receiver_Sea")

        self.verticalLayout_8.addWidget(self.Receiver_Sea)

        self.Receiver_Estuary = QCheckBox(self.Receiver_Widget)
        self.Receiver_Estuary.setObjectName(u"Receiver_Estuary")

        self.verticalLayout_8.addWidget(self.Receiver_Estuary)

        self.Receiver_River = QCheckBox(self.Receiver_Widget)
        self.Receiver_River.setObjectName(u"Receiver_River")

        self.verticalLayout_8.addWidget(self.Receiver_River)

        self.Receiver_Other = QCheckBox(self.Receiver_Widget)
        self.Receiver_Other.setObjectName(u"Receiver_Other")

        self.verticalLayout_8.addWidget(self.Receiver_Other)


        self.Minor_Form.setWidget(6, QFormLayout.FieldRole, self.Receiver_Widget)

        self.Type_ComboBox = QComboBox(self.Minor_Widget)
        self.Type_ComboBox.addItem("")
        self.Type_ComboBox.addItem("")
        self.Type_ComboBox.addItem("")
        self.Type_ComboBox.setObjectName(u"Type_ComboBox")
        self.Type_ComboBox.setEditable(False)
        self.Type_ComboBox.setFrame(True)

        self.Minor_Form.setWidget(0, QFormLayout.FieldRole, self.Type_ComboBox)


        self.verticalLayout_69.addLayout(self.Minor_Form)


        self.verticalLayout_57.addWidget(self.Minor_Widget)

        self.SpecialEq_Widget = QWidget(self.Drainage_Frame)
        self.SpecialEq_Widget.setObjectName(u"SpecialEq_Widget")
        self.verticalLayout_68 = QVBoxLayout(self.SpecialEq_Widget)
        self.verticalLayout_68.setSpacing(2)
        self.verticalLayout_68.setObjectName(u"verticalLayout_68")
        self.verticalLayout_68.setContentsMargins(1, 1, 1, 1)
        self.SpecialEq_Label = QLabel(self.SpecialEq_Widget)
        self.SpecialEq_Label.setObjectName(u"SpecialEq_Label")
        self.SpecialEq_Label.setFont(font6)
        self.SpecialEq_Label.setTextFormat(Qt.PlainText)
        self.SpecialEq_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_68.addWidget(self.SpecialEq_Label)

        self.SpecialEq_Table = QTableWidget(self.SpecialEq_Widget)
        if (self.SpecialEq_Table.columnCount() < 2):
            self.SpecialEq_Table.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.SpecialEq_Table.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.SpecialEq_Table.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        self.SpecialEq_Table.setObjectName(u"SpecialEq_Table")
        sizePolicy7.setHeightForWidth(self.SpecialEq_Table.sizePolicy().hasHeightForWidth())
        self.SpecialEq_Table.setSizePolicy(sizePolicy7)
        self.SpecialEq_Table.setStyleSheet(u"")
        self.SpecialEq_Table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.SpecialEq_Table.setAutoScrollMargin(10)
        self.SpecialEq_Table.setAlternatingRowColors(True)
        self.SpecialEq_Table.setShowGrid(True)
        self.SpecialEq_Table.setGridStyle(Qt.SolidLine)
        self.SpecialEq_Table.setSortingEnabled(False)
        self.SpecialEq_Table.setCornerButtonEnabled(True)
        self.SpecialEq_Table.setRowCount(0)
        self.SpecialEq_Table.setColumnCount(2)
        self.SpecialEq_Table.horizontalHeader().setVisible(True)
        self.SpecialEq_Table.horizontalHeader().setCascadingSectionResizes(False)
        self.SpecialEq_Table.horizontalHeader().setMinimumSectionSize(30)
        self.SpecialEq_Table.horizontalHeader().setDefaultSectionSize(100)
        self.SpecialEq_Table.horizontalHeader().setHighlightSections(True)
        self.SpecialEq_Table.horizontalHeader().setProperty("showSortIndicator", False)
        self.SpecialEq_Table.horizontalHeader().setStretchLastSection(True)
        self.SpecialEq_Table.verticalHeader().setVisible(False)
        self.SpecialEq_Table.verticalHeader().setMinimumSectionSize(20)
        self.SpecialEq_Table.verticalHeader().setHighlightSections(False)
        self.SpecialEq_Table.verticalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout_68.addWidget(self.SpecialEq_Table)


        self.verticalLayout_57.addWidget(self.SpecialEq_Widget)

        self.verticalSpacer_10 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_57.addItem(self.verticalSpacer_10)


        self.verticalLayout_56.addWidget(self.Drainage_Frame)


        self.horizontalLayout_7.addWidget(self.Col3)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 1)
        self.horizontalLayout_7.setStretch(2, 1)
        self.horizontalLayout_7.setStretch(3, 1)
        self.horizontalLayout_7.setStretch(4, 1)
        self.BodyWidget.addWidget(self.Page1_Profile)
        self.Page2_Manager = QWidget()
        self.Page2_Manager.setObjectName(u"Page2_Manager")
        self.verticalLayout_20 = QVBoxLayout(self.Page2_Manager)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.Manager_TabWidget = QTabWidget(self.Page2_Manager)
        self.Manager_TabWidget.setObjectName(u"Manager_TabWidget")
        sizePolicy6.setHeightForWidth(self.Manager_TabWidget.sizePolicy().hasHeightForWidth())
        self.Manager_TabWidget.setSizePolicy(sizePolicy6)
        self.Manager_TabWidget.setFocusPolicy(Qt.NoFocus)
        self.Manager_TabWidget.setStyleSheet(u"")
        self.Manager_TabWidget.setTabPosition(QTabWidget.North)
        self.Manager_Page1 = QWidget()
        self.Manager_Page1.setObjectName(u"Manager_Page1")
        self.verticalLayout_19 = QVBoxLayout(self.Manager_Page1)
        self.verticalLayout_19.setSpacing(5)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(10, 10, 10, 10)
        self.Situation_setup_Frame = QFrame(self.Manager_Page1)
        self.Situation_setup_Frame.setObjectName(u"Situation_setup_Frame")
        sizePolicy6.setHeightForWidth(self.Situation_setup_Frame.sizePolicy().hasHeightForWidth())
        self.Situation_setup_Frame.setSizePolicy(sizePolicy6)
        self.Situation_setup_Frame.setFocusPolicy(Qt.NoFocus)
        self.Situation_setup_Frame.setStyleSheet(u"QFrame#Situation_setup_Frame {\n"
"background-color: #FFFADD;\n"
"border-radius: 20px\n"
"}\n"
"\n"
"QFrame QListView{\n"
"/*background-color: rgb(255, 255, 255);\n"
"border-radius: 0px*/\n"
"}\n"
"\n"
"")
        self.verticalLayout_47 = QVBoxLayout(self.Situation_setup_Frame)
        self.verticalLayout_47.setSpacing(10)
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.verticalLayout_47.setContentsMargins(10, 10, 10, 10)
        self.Situation_setup_LabelFrame = QFrame(self.Situation_setup_Frame)
        self.Situation_setup_LabelFrame.setObjectName(u"Situation_setup_LabelFrame")
        self.Situation_setup_LabelFrame.setMinimumSize(QSize(0, 20))
        self.Situation_setup_LabelFrame.setStyleSheet(u"background-color: #ffcc33;	\n"
"border-radius: 10px")
        self.Situation_setup_LabelFrame.setFrameShape(QFrame.NoFrame)
        self.Situation_setup_LabelFrame.setFrameShadow(QFrame.Raised)
        self.Situation_setup_LabelFrame.setLineWidth(4)
        self.Situation_setup_LabelFrame.setMidLineWidth(4)
        self.horizontalLayout_17 = QHBoxLayout(self.Situation_setup_LabelFrame)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(10, 0, 10, 0)
        self.Situation_setup_Label = QLabel(self.Situation_setup_LabelFrame)
        self.Situation_setup_Label.setObjectName(u"Situation_setup_Label")
        self.Situation_setup_Label.setEnabled(True)
        self.Situation_setup_Label.setMinimumSize(QSize(0, 0))
        self.Situation_setup_Label.setFont(font5)
        self.Situation_setup_Label.setStyleSheet(u"")

        self.horizontalLayout_17.addWidget(self.Situation_setup_Label)

        self.horizontalLayout_17.setStretch(0, 1)

        self.verticalLayout_47.addWidget(self.Situation_setup_LabelFrame)

        self.Situation_setup_Content_Widget = QWidget(self.Situation_setup_Frame)
        self.Situation_setup_Content_Widget.setObjectName(u"Situation_setup_Content_Widget")
        self.Situation_setup_Content_WidgetLayout = QHBoxLayout(self.Situation_setup_Content_Widget)
        self.Situation_setup_Content_WidgetLayout.setSpacing(10)
        self.Situation_setup_Content_WidgetLayout.setObjectName(u"Situation_setup_Content_WidgetLayout")
        self.Situation_setup_Content_WidgetLayout.setContentsMargins(1, 1, 1, 1)

        self.verticalLayout_47.addWidget(self.Situation_setup_Content_Widget)

        self.verticalLayout_47.setStretch(1, 1)

        self.verticalLayout_19.addWidget(self.Situation_setup_Frame)

        self.Situation_generator_Frame = QFrame(self.Manager_Page1)
        self.Situation_generator_Frame.setObjectName(u"Situation_generator_Frame")
        sizePolicy6.setHeightForWidth(self.Situation_generator_Frame.sizePolicy().hasHeightForWidth())
        self.Situation_generator_Frame.setSizePolicy(sizePolicy6)
        self.Situation_generator_Frame.setFocusPolicy(Qt.NoFocus)
        self.Situation_generator_Frame.setStyleSheet(u"QFrame#Situation_generator_Frame{\n"
"background-color: #FFFADD;\n"
"border-radius: 20px\n"
"}\n"
"\n"
"QFrame QListView{\n"
"/*background-color: rgb(255, 255, 255);\n"
"border-radius: 10px*/\n"
"}\n"
"\n"
"QFrame QTableView{\n"
"\n"
"}\n"
"")
        self.verticalLayout_46 = QVBoxLayout(self.Situation_generator_Frame)
        self.verticalLayout_46.setSpacing(10)
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.verticalLayout_46.setContentsMargins(10, 10, 10, 10)
        self.Situation_generator_LabelFrame = QFrame(self.Situation_generator_Frame)
        self.Situation_generator_LabelFrame.setObjectName(u"Situation_generator_LabelFrame")
        self.Situation_generator_LabelFrame.setMinimumSize(QSize(0, 20))
        self.Situation_generator_LabelFrame.setStyleSheet(u"background-color: #ffcc33;	\n"
"border-radius: 10px")
        self.Situation_generator_LabelFrame.setFrameShape(QFrame.NoFrame)
        self.Situation_generator_LabelFrame.setFrameShadow(QFrame.Raised)
        self.Situation_generator_LabelFrame.setLineWidth(4)
        self.Situation_generator_LabelFrame.setMidLineWidth(4)
        self.horizontalLayout_15 = QHBoxLayout(self.Situation_generator_LabelFrame)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(10, 0, 10, 0)
        self.Situation_generator_Label = QLabel(self.Situation_generator_LabelFrame)
        self.Situation_generator_Label.setObjectName(u"Situation_generator_Label")
        self.Situation_generator_Label.setEnabled(True)
        self.Situation_generator_Label.setMinimumSize(QSize(0, 0))
        self.Situation_generator_Label.setFont(font5)
        self.Situation_generator_Label.setStyleSheet(u"")

        self.horizontalLayout_15.addWidget(self.Situation_generator_Label)

        self.horizontalLayout_15.setStretch(0, 1)

        self.verticalLayout_46.addWidget(self.Situation_generator_LabelFrame)

        self.Situation_generator_Content_Widget = QWidget(self.Situation_generator_Frame)
        self.Situation_generator_Content_Widget.setObjectName(u"Situation_generator_Content_Widget")
        self.Situation_generator_Content_WidgetLayout = QHBoxLayout(self.Situation_generator_Content_Widget)
        self.Situation_generator_Content_WidgetLayout.setSpacing(10)
        self.Situation_generator_Content_WidgetLayout.setObjectName(u"Situation_generator_Content_WidgetLayout")
        self.Situation_generator_Content_WidgetLayout.setContentsMargins(1, 1, 1, 1)

        self.verticalLayout_46.addWidget(self.Situation_generator_Content_Widget)

        self.verticalLayout_46.setStretch(1, 1)

        self.verticalLayout_19.addWidget(self.Situation_generator_Frame)

        self.Manager_TabWidget.addTab(self.Manager_Page1, "")
        self.Manager_Page2 = QWidget()
        self.Manager_Page2.setObjectName(u"Manager_Page2")
        self.Manager_Page2_Layout = QVBoxLayout(self.Manager_Page2)
        self.Manager_Page2_Layout.setObjectName(u"Manager_Page2_Layout")
        self.Manager_TabWidget.addTab(self.Manager_Page2, "")
        self.Manager_Page3 = QWidget()
        self.Manager_Page3.setObjectName(u"Manager_Page3")
        self.horizontalLayout_5 = QHBoxLayout(self.Manager_Page3)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.Indicators_selector_Frame = QFrame(self.Manager_Page3)
        self.Indicators_selector_Frame.setObjectName(u"Indicators_selector_Frame")
        self.Indicators_selector_Frame.setFrameShape(QFrame.StyledPanel)
        self.Indicators_selector_Frame.setFrameShadow(QFrame.Raised)
        self.Indicators_selector_FrameLayout = QVBoxLayout(self.Indicators_selector_Frame)
        self.Indicators_selector_FrameLayout.setObjectName(u"Indicators_selector_FrameLayout")

        self.horizontalLayout_5.addWidget(self.Indicators_selector_Frame)

        self.Indicators_setup_Frame = QFrame(self.Manager_Page3)
        self.Indicators_setup_Frame.setObjectName(u"Indicators_setup_Frame")
        sizePolicy.setHeightForWidth(self.Indicators_setup_Frame.sizePolicy().hasHeightForWidth())
        self.Indicators_setup_Frame.setSizePolicy(sizePolicy)
        self.Indicators_setup_Frame.setFrameShape(QFrame.StyledPanel)
        self.Indicators_setup_Frame.setFrameShadow(QFrame.Raised)
        self.Indicators_setup_FrameLayout = QVBoxLayout(self.Indicators_setup_Frame)
        self.Indicators_setup_FrameLayout.setObjectName(u"Indicators_setup_FrameLayout")

        self.horizontalLayout_5.addWidget(self.Indicators_setup_Frame)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 2)
        self.Manager_TabWidget.addTab(self.Manager_Page3, "")

        self.verticalLayout_20.addWidget(self.Manager_TabWidget)

        self.BodyWidget.addWidget(self.Page2_Manager)
        self.Page3_Functional = QWidget()
        self.Page3_Functional.setObjectName(u"Page3_Functional")
        self.horizontalLayout_4 = QHBoxLayout(self.Page3_Functional)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.Functional_LeftWidget = QWidget(self.Page3_Functional)
        self.Functional_LeftWidget.setObjectName(u"Functional_LeftWidget")
        self.Functional_LeftWidget_Layout = QVBoxLayout(self.Functional_LeftWidget)
        self.Functional_LeftWidget_Layout.setSpacing(5)
        self.Functional_LeftWidget_Layout.setObjectName(u"Functional_LeftWidget_Layout")
        self.Functional_LeftWidget_Layout.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.Functional_LeftWidget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"QFrame {\n"
"background-color: rgba(255, 255, 255, 255);\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_17 = QVBoxLayout(self.frame_5)
        self.verticalLayout_17.setSpacing(5)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(10, 10, 10, 10)
        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_17.addWidget(self.label_3)

        self.Functional_list = QTreeWidget(self.frame_5)
        self.Functional_list.setObjectName(u"Functional_list")
        sizePolicy5.setHeightForWidth(self.Functional_list.sizePolicy().hasHeightForWidth())
        self.Functional_list.setSizePolicy(sizePolicy5)
        self.Functional_list.setMinimumSize(QSize(340, 400))
        self.Functional_list.setMaximumSize(QSize(340, 400))
        self.Functional_list.setFrameShape(QFrame.Box)
        self.Functional_list.setFrameShadow(QFrame.Plain)
        self.Functional_list.setLineWidth(1)
        self.Functional_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.Functional_list.setProperty("showDropIndicator", False)
        self.Functional_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.Functional_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.Functional_list.setIndentation(10)
        self.Functional_list.setItemsExpandable(True)
        self.Functional_list.setAnimated(True)
        self.Functional_list.setWordWrap(True)
        self.Functional_list.setHeaderHidden(True)
        self.Functional_list.setColumnCount(1)
        self.Functional_list.header().setVisible(False)

        self.verticalLayout_17.addWidget(self.Functional_list)


        self.Functional_LeftWidget_Layout.addWidget(self.frame_5)

        self.verticalSpacer_39 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Functional_LeftWidget_Layout.addItem(self.verticalSpacer_39)


        self.horizontalLayout_4.addWidget(self.Functional_LeftWidget)

        self.Functional_MainWidget = QStackedWidget(self.Page3_Functional)
        self.Functional_MainWidget.setObjectName(u"Functional_MainWidget")
        self.Functional_MainWidget.setStyleSheet(u"background-color: rgb(236, 246, 239);\n"
"border: 0px solid #000000;\n"
"border-radius: 20px;\n"
"\n"
"")
        self.Functional_MainWidget.setLineWidth(0)
        self.default_8 = QWidget()
        self.default_8.setObjectName(u"default_8")
        self.Functional_MainWidget.addWidget(self.default_8)
        self.default_9 = QWidget()
        self.default_9.setObjectName(u"default_9")
        self.Functional_MainWidget.addWidget(self.default_9)

        self.horizontalLayout_4.addWidget(self.Functional_MainWidget)

        self.BodyWidget.addWidget(self.Page3_Functional)
        self.Page4_Performance = QWidget()
        self.Page4_Performance.setObjectName(u"Page4_Performance")
        self.verticalLayout_7 = QVBoxLayout(self.Page4_Performance)
        self.verticalLayout_7.setSpacing(10)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.Page4_Performance)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_13 = QVBoxLayout(self.widget_4)
        self.verticalLayout_13.setSpacing(5)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.Performance_TopWidget = QWidget(self.widget_4)
        self.Performance_TopWidget.setObjectName(u"Performance_TopWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.Performance_TopWidget)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Rainfall_selection_Label = QLabel(self.Performance_TopWidget)
        self.Rainfall_selection_Label.setObjectName(u"Rainfall_selection_Label")
        self.Rainfall_selection_Label.setFont(font4)

        self.horizontalLayout_2.addWidget(self.Rainfall_selection_Label)

        self.Rainfall_selection_ComboBox = QComboBox(self.Performance_TopWidget)
        self.Rainfall_selection_ComboBox.setObjectName(u"Rainfall_selection_ComboBox")
        self.Rainfall_selection_ComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_2.addWidget(self.Rainfall_selection_ComboBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_13.addWidget(self.Performance_TopWidget)

        self.Performance_MainWidget = QStackedWidget(self.widget_4)
        self.Performance_MainWidget.setObjectName(u"Performance_MainWidget")
        self.Performance_MainWidget.setStyleSheet(u"background-color: rgb(255, 251, 245);\n"
"border: 0px solid #000000; /* Set a border for visibility */\n"
" border-radius: 20px;\n"
"")
        self.default_16 = QWidget()
        self.default_16.setObjectName(u"default_16")
        self.Performance_MainWidget.addWidget(self.default_16)
        self.default_17 = QWidget()
        self.default_17.setObjectName(u"default_17")
        self.Performance_MainWidget.addWidget(self.default_17)

        self.verticalLayout_13.addWidget(self.Performance_MainWidget)

        self.verticalLayout_13.setStretch(1, 1)

        self.verticalLayout_7.addWidget(self.widget_4)

        self.BodyWidget.addWidget(self.Page4_Performance)
        self.Page5_Dashboard = QWidget()
        self.Page5_Dashboard.setObjectName(u"Page5_Dashboard")
        self.verticalLayout_18 = QVBoxLayout(self.Page5_Dashboard)
        self.verticalLayout_18.setSpacing(10)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.Dashboard_scrollArea = QScrollArea(self.Page5_Dashboard)
        self.Dashboard_scrollArea.setObjectName(u"Dashboard_scrollArea")
        self.Dashboard_scrollArea.setFrameShadow(QFrame.Raised)
        self.Dashboard_scrollArea.setLineWidth(0)
        self.Dashboard_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.Dashboard_scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.Dashboard_scrollArea.setWidgetResizable(True)
        self.Dashboard_scrollArea.setAlignment(Qt.AlignCenter)
        self.Dashboard_WidgetContents = QWidget()
        self.Dashboard_WidgetContents.setObjectName(u"Dashboard_WidgetContents")
        self.Dashboard_WidgetContents.setGeometry(QRect(0, 0, 918, 920))
        self.verticalLayout_44 = QVBoxLayout(self.Dashboard_WidgetContents)
        self.verticalLayout_44.setSpacing(10)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.verticalLayout_44.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.Overall_Frame = QFrame(self.Dashboard_WidgetContents)
        self.Overall_Frame.setObjectName(u"Overall_Frame")
        self.Overall_Frame.setMinimumSize(QSize(0, 300))
        self.Overall_Frame.setStyleSheet(u"QFrame {\n"
"background-color: rgb(246, 252, 255);\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_27 = QVBoxLayout(self.Overall_Frame)
        self.verticalLayout_27.setSpacing(5)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(10, 10, 10, 10)
        self.Overall_Label = QLabel(self.Overall_Frame)
        self.Overall_Label.setObjectName(u"Overall_Label")
        self.Overall_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_27.addWidget(self.Overall_Label)

        self.Overall_Content_Widget = QWidget(self.Overall_Frame)
        self.Overall_Content_Widget.setObjectName(u"Overall_Content_Widget")
        self.Overall_HLayout_2 = QHBoxLayout(self.Overall_Content_Widget)
        self.Overall_HLayout_2.setSpacing(5)
        self.Overall_HLayout_2.setObjectName(u"Overall_HLayout_2")
        self.Overall_HLayout_2.setContentsMargins(1, 1, 1, 1)
        self.OFR_Widget = QWidget(self.Overall_Content_Widget)
        self.OFR_Widget.setObjectName(u"OFR_Widget")
        self.verticalLayout_22 = QVBoxLayout(self.OFR_Widget)
        self.verticalLayout_22.setSpacing(2)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.OFR_Label = QLabel(self.OFR_Widget)
        self.OFR_Label.setObjectName(u"OFR_Label")
        self.OFR_Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_22.addWidget(self.OFR_Label)

        self.OFR_Plot = QWidget(self.OFR_Widget)
        self.OFR_Plot.setObjectName(u"OFR_Plot")

        self.verticalLayout_22.addWidget(self.OFR_Plot)

        self.verticalLayout_22.setStretch(1, 1)

        self.Overall_HLayout_2.addWidget(self.OFR_Widget)

        self.OPR_Widget = QWidget(self.Overall_Content_Widget)
        self.OPR_Widget.setObjectName(u"OPR_Widget")
        self.verticalLayout_23 = QVBoxLayout(self.OPR_Widget)
        self.verticalLayout_23.setSpacing(2)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.OPR_Label = QLabel(self.OPR_Widget)
        self.OPR_Label.setObjectName(u"OPR_Label")
        self.OPR_Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_23.addWidget(self.OPR_Label)

        self.OPR_Plot = QWidget(self.OPR_Widget)
        self.OPR_Plot.setObjectName(u"OPR_Plot")

        self.verticalLayout_23.addWidget(self.OPR_Plot)

        self.verticalLayout_23.setStretch(1, 1)

        self.Overall_HLayout_2.addWidget(self.OPR_Widget)

        self.ORR_Widget = QWidget(self.Overall_Content_Widget)
        self.ORR_Widget.setObjectName(u"ORR_Widget")
        self.verticalLayout_24 = QVBoxLayout(self.ORR_Widget)
        self.verticalLayout_24.setSpacing(2)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.ORR_Label = QLabel(self.ORR_Widget)
        self.ORR_Label.setObjectName(u"ORR_Label")
        self.ORR_Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_24.addWidget(self.ORR_Label)

        self.ORR_Plot = QWidget(self.ORR_Widget)
        self.ORR_Plot.setObjectName(u"ORR_Plot")

        self.verticalLayout_24.addWidget(self.ORR_Plot)

        self.verticalLayout_24.setStretch(1, 1)

        self.Overall_HLayout_2.addWidget(self.ORR_Widget)

        self.Overall_HLayout_2.setStretch(0, 1)
        self.Overall_HLayout_2.setStretch(1, 1)
        self.Overall_HLayout_2.setStretch(2, 1)

        self.verticalLayout_27.addWidget(self.Overall_Content_Widget)


        self.verticalLayout_44.addWidget(self.Overall_Frame)

        self.Functional_Frame = QFrame(self.Dashboard_WidgetContents)
        self.Functional_Frame.setObjectName(u"Functional_Frame")
        self.Functional_Frame.setMinimumSize(QSize(0, 300))
        self.Functional_Frame.setStyleSheet(u"QFrame {\n"
"background-color: rgb(236, 246, 239);\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_39 = QVBoxLayout(self.Functional_Frame)
        self.verticalLayout_39.setSpacing(5)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(10, 10, 10, 10)
        self.Overall_Label_3 = QLabel(self.Functional_Frame)
        self.Overall_Label_3.setObjectName(u"Overall_Label_3")
        self.Overall_Label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_39.addWidget(self.Overall_Label_3)

        self.Functional_Content_Widget = QWidget(self.Functional_Frame)
        self.Functional_Content_Widget.setObjectName(u"Functional_Content_Widget")
        self.Functional_HLayout = QHBoxLayout(self.Functional_Content_Widget)
        self.Functional_HLayout.setSpacing(5)
        self.Functional_HLayout.setObjectName(u"Functional_HLayout")
        self.Functional_HLayout.setContentsMargins(1, 1, 1, 1)
        self.FCR_Widget = QWidget(self.Functional_Content_Widget)
        self.FCR_Widget.setObjectName(u"FCR_Widget")
        self.verticalLayout_30 = QVBoxLayout(self.FCR_Widget)
        self.verticalLayout_30.setSpacing(2)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.label_13 = QLabel(self.FCR_Widget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_30.addWidget(self.label_13)

        self.FCR_ComboBox = QComboBox(self.FCR_Widget)
        self.FCR_ComboBox.setObjectName(u"FCR_ComboBox")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.FCR_ComboBox.sizePolicy().hasHeightForWidth())
        self.FCR_ComboBox.setSizePolicy(sizePolicy8)
        self.FCR_ComboBox.setMinimumSize(QSize(0, 0))
        self.FCR_ComboBox.setMaximumSize(QSize(16777215, 16777215))
        self.FCR_ComboBox.setAutoFillBackground(False)
        self.FCR_ComboBox.setInsertPolicy(QComboBox.InsertAtBottom)
        self.FCR_ComboBox.setFrame(True)
        self.FCR_ComboBox.setModelColumn(0)

        self.verticalLayout_30.addWidget(self.FCR_ComboBox)

        self.FCR_Plot = QWidget(self.FCR_Widget)
        self.FCR_Plot.setObjectName(u"FCR_Plot")

        self.verticalLayout_30.addWidget(self.FCR_Plot)

        self.verticalLayout_30.setStretch(2, 1)

        self.Functional_HLayout.addWidget(self.FCR_Widget)

        self.FOC_Widget = QWidget(self.Functional_Content_Widget)
        self.FOC_Widget.setObjectName(u"FOC_Widget")
        self.verticalLayout_38 = QVBoxLayout(self.FOC_Widget)
        self.verticalLayout_38.setSpacing(2)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.FOC_Label = QLabel(self.FOC_Widget)
        self.FOC_Label.setObjectName(u"FOC_Label")
        self.FOC_Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_38.addWidget(self.FOC_Label)

        self.FOC_Plot = QWidget(self.FOC_Widget)
        self.FOC_Plot.setObjectName(u"FOC_Plot")

        self.verticalLayout_38.addWidget(self.FOC_Plot)

        self.verticalLayout_38.setStretch(1, 1)

        self.Functional_HLayout.addWidget(self.FOC_Widget)

        self.FOR_Widget = QWidget(self.Functional_Content_Widget)
        self.FOR_Widget.setObjectName(u"FOR_Widget")
        self.verticalLayout_33 = QVBoxLayout(self.FOR_Widget)
        self.verticalLayout_33.setSpacing(2)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.FOR_Label = QLabel(self.FOR_Widget)
        self.FOR_Label.setObjectName(u"FOR_Label")
        self.FOR_Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_33.addWidget(self.FOR_Label)

        self.FOR_Plot = QWidget(self.FOR_Widget)
        self.FOR_Plot.setObjectName(u"FOR_Plot")

        self.verticalLayout_33.addWidget(self.FOR_Plot)

        self.verticalLayout_33.setStretch(1, 1)

        self.Functional_HLayout.addWidget(self.FOR_Widget)

        self.Functional_HLayout.setStretch(0, 1)
        self.Functional_HLayout.setStretch(1, 1)
        self.Functional_HLayout.setStretch(2, 1)

        self.verticalLayout_39.addWidget(self.Functional_Content_Widget)


        self.verticalLayout_44.addWidget(self.Functional_Frame)

        self.Performance_Frame = QFrame(self.Dashboard_WidgetContents)
        self.Performance_Frame.setObjectName(u"Performance_Frame")
        self.Performance_Frame.setMinimumSize(QSize(0, 300))
        self.Performance_Frame.setStyleSheet(u"QFrame {\n"
"background-color: rgb(255, 251, 245);\n"
"border-radius: 20px\n"
"}")
        self.verticalLayout_43 = QVBoxLayout(self.Performance_Frame)
        self.verticalLayout_43.setSpacing(5)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.verticalLayout_43.setContentsMargins(10, 10, 10, 10)
        self.Performance_Label = QLabel(self.Performance_Frame)
        self.Performance_Label.setObjectName(u"Performance_Label")
        self.Performance_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_43.addWidget(self.Performance_Label)

        self.Performance_Content_Widget = QWidget(self.Performance_Frame)
        self.Performance_Content_Widget.setObjectName(u"Performance_Content_Widget")
        self.Overall_HLayout_4 = QHBoxLayout(self.Performance_Content_Widget)
        self.Overall_HLayout_4.setSpacing(15)
        self.Overall_HLayout_4.setObjectName(u"Overall_HLayout_4")
        self.Overall_HLayout_4.setContentsMargins(1, 1, 1, 1)
        self.PSR_Widget = QWidget(self.Performance_Content_Widget)
        self.PSR_Widget.setObjectName(u"PSR_Widget")
        self.verticalLayout_40 = QVBoxLayout(self.PSR_Widget)
        self.verticalLayout_40.setSpacing(2)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.PSR_Label = QLabel(self.PSR_Widget)
        self.PSR_Label.setObjectName(u"PSR_Label")
        self.PSR_Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_40.addWidget(self.PSR_Label)

        self.PSR_Plot = QWidget(self.PSR_Widget)
        self.PSR_Plot.setObjectName(u"PSR_Plot")

        self.verticalLayout_40.addWidget(self.PSR_Plot)

        self.verticalLayout_40.setStretch(1, 1)

        self.Overall_HLayout_4.addWidget(self.PSR_Widget)

        self.PCR_Widget = QWidget(self.Performance_Content_Widget)
        self.PCR_Widget.setObjectName(u"PCR_Widget")
        self.verticalLayout_41 = QVBoxLayout(self.PCR_Widget)
        self.verticalLayout_41.setSpacing(2)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.PCR_Label = QLabel(self.PCR_Widget)
        self.PCR_Label.setObjectName(u"PCR_Label")
        self.PCR_Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_41.addWidget(self.PCR_Label)

        self.PCR_Plot = QWidget(self.PCR_Widget)
        self.PCR_Plot.setObjectName(u"PCR_Plot")

        self.verticalLayout_41.addWidget(self.PCR_Plot)

        self.verticalLayout_41.setStretch(1, 1)

        self.Overall_HLayout_4.addWidget(self.PCR_Widget)

        self.Overall_HLayout_4.setStretch(0, 1)
        self.Overall_HLayout_4.setStretch(1, 1)

        self.verticalLayout_43.addWidget(self.Performance_Content_Widget)


        self.verticalLayout_44.addWidget(self.Performance_Frame)

        self.Dashboard_scrollArea.setWidget(self.Dashboard_WidgetContents)

        self.verticalLayout_18.addWidget(self.Dashboard_scrollArea)

        self.BodyWidget.addWidget(self.Page5_Dashboard)

        self.Org1_Body.addWidget(self.BodyWidget)


        self.verticalLayout_5.addLayout(self.Org1_Body)

        self.Org2_Footer = QHBoxLayout()
        self.Org2_Footer.setSpacing(0)
        self.Org2_Footer.setObjectName(u"Org2_Footer")
        self.footer_left_label = QLabel(self.centralwidget)
        self.footer_left_label.setObjectName(u"footer_left_label")
        self.footer_left_label.setOpenExternalLinks(True)

        self.Org2_Footer.addWidget(self.footer_left_label, 0, Qt.AlignBottom)

        self.footer_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.Org2_Footer.addItem(self.footer_horizontalSpacer)

        self.footer_right_label = QLabel(self.centralwidget)
        self.footer_right_label.setObjectName(u"footer_right_label")

        self.Org2_Footer.addWidget(self.footer_right_label, 0, Qt.AlignBottom)


        self.verticalLayout_5.addLayout(self.Org2_Footer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1284, 22))
        self.menuFile_F = QMenu(self.menubar)
        self.menuFile_F.setObjectName(u"menuFile_F")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile_F.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile_F.addAction(self.actionSave)
        self.menuFile_F.addAction(self.actionSave_As)
        self.menuFile_F.addAction(self.actionLoad)
        self.menuHelp.addAction(self.actionManual)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addSeparator()

        self.retranslateUi(MainWindow)
        self.menu_btn.clicked.connect(self.LeftMenuFrame_2.show)
        self.menu_btn.clicked.connect(self.LeftMenuFrame.hide)
        self.menu_btn_2.clicked.connect(self.LeftMenuFrame.show)
        self.menu_btn_2.clicked.connect(self.LeftMenuFrame_2.hide)
        self.home_btn.clicked.connect(self.home_btn_2.toggle)
        self.home_btn_2.clicked.connect(self.home_btn.toggle)
        self.profile_btn.clicked.connect(self.profile_btn_2.toggle)
        self.profile_btn_2.clicked.connect(self.profile_btn.toggle)
        self.analysis_btn.clicked.connect(self.analysis_btn_2.toggle)
        self.analysis_btn_2.clicked.connect(self.analysis_btn.toggle)
        self.functional_btn.clicked.connect(self.functional_btn_2.toggle)
        self.functional_btn_2.clicked.connect(self.functional_btn.toggle)
        self.performance_btn.clicked.connect(self.performance_btn_2.toggle)
        self.performance_btn_2.clicked.connect(self.performance_btn.toggle)
        self.dashboard_btn.clicked.connect(self.dashboard_btn_2.toggle)
        self.dashboard_btn_2.clicked.connect(self.dashboard_btn.toggle)

        self.menu_btn_2.setDefault(False)
        self.home_btn_2.setDefault(False)
        self.BodyWidget.setCurrentIndex(5)
        self.Manager_TabWidget.setCurrentIndex(0)
        self.Functional_MainWidget.setCurrentIndex(0)
        self.Performance_MainWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
        self.actionSave_As.setIconText(QCoreApplication.translate("MainWindow", u"Save As", None))
#if QT_CONFIG(shortcut)
        self.actionSave_As.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
#if QT_CONFIG(shortcut)
        self.actionLoad.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label_5.setText("")
        self.REFUSS2_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:22pt; color:#0f75bc;\">RESILISTORM</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; color:#0f75bc;\">Resilience Framework for Urban Stormwater Services</span></p></body></html>", None))
        self.home_btn.setText("")
        self.profile_btn.setText("")
        self.analysis_btn.setText("")
        self.functional_btn.setText("")
        self.performance_btn.setText("")
        self.dashboard_btn.setText("")
        self.menu_btn_2.setText("")
        self.home_btn_2.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        self.profile_btn_2.setText(QCoreApplication.translate("MainWindow", u"STUDY PROFILE", None))
        self.analysis_btn_2.setText(QCoreApplication.translate("MainWindow", u"ANALYSIS MANAGER", None))
        self.Situation_selection_Label.setText(QCoreApplication.translate("MainWindow", u"Select situation:", None))
        self.Situation_selection_Combobox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"None", None))
        self.functional_btn_2.setText(QCoreApplication.translate("MainWindow", u"STRATEGIC DIMENSION", None))
        self.performance_btn_2.setText(QCoreApplication.translate("MainWindow", u"PERFORMANCE DIMENSION", None))
        self.dashboard_btn_2.setText(QCoreApplication.translate("MainWindow", u"RESILIENCE DASHBOARD", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">HOME</span></p></body></html>", None))
        self.Home_Label1.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">What is urban resilience?</span></p><p><span style=\" font-size:11pt;\">\u00abUrban resilience refers to the ability of an urban system - and all its constituent socio\u2011ecological and socio-technical networks across temporal and spatial scales - to maintain or rapidly return to desired functions in the face of a disturbance, to adapt to change, and to quickly transform systems that limit current or future adaptive capacity.\u00bb</span></p><p align=\"right\"><span style=\" font-size:10pt;\">Meerow et al. (2016)</span></p></body></html>", None))
        self.Home_Label1_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Why addressing the resilience of urban stormwater services?</span></p><p align=\"justify\"><span style=\" font-size:11pt;\">As urban service, stormwater systems have a clear main objective: to properly deal with water volumes originated from precipitation with no negative consequences to the population, goods, and services. For that reason, urban stormwater services can be considered as an impact driven service since they are purposefully designed to deal with weather related events \u2013 namely rainfalls \u2013 and to minimize its consequences .</span></p><p align=\"justify\"><span style=\" font-size:11pt;\">The resilience approach represents a paradigm shift from conventional \u201cfail\u2011safe\u201d approaches to a holistic \u201csafe-to-fail\u201d view that accepts, anticipates, and plans for failure under exceptional conditions, enhancing the ability to cope with and recover from flooding, especially when considering future risks a"
                        "nd related uncertainties.</span></p></body></html>", None))
        self.label_2.setText("")
        self.Domain_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">DOMAIN</span></p></body></html>", None))
        self.Location_Label.setText(QCoreApplication.translate("MainWindow", u"Location", None))
        self.Country_Label.setText(QCoreApplication.translate("MainWindow", u"Country", None))
        self.City_Label.setText(QCoreApplication.translate("MainWindow", u"City", None))
        self.Cat_Label.setText(QCoreApplication.translate("MainWindow", u"Catchment", None))
        self.CatName_Label.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.CatArea_Label.setText(QCoreApplication.translate("MainWindow", u"Area (ha)", None))
        self.CatArea_LineEdit.setInputMask("")
        self.CatArea_LineEdit.setText("")
        self.CatImp_Label.setText(QCoreApplication.translate("MainWindow", u"Imp. area (%)", None))
        self.CatSlope_Label.setText(QCoreApplication.translate("MainWindow", u"Av. slope (%)", None))
        self.StudyName_Label.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.Study_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Study</p></body></html>", None))
        self.Population_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">POPULATION</span></p></body></html>", None))
        self.Gender_Label.setText(QCoreApplication.translate("MainWindow", u"Gender distribution", None))
        self.Male_Label.setText(QCoreApplication.translate("MainWindow", u"Male", None))
        self.Female_Label.setText(QCoreApplication.translate("MainWindow", u"Female", None))
        self.Other_Label.setText(QCoreApplication.translate("MainWindow", u"Other", None))
        self.Age_Label.setText(QCoreApplication.translate("MainWindow", u"Age distribution", None))
        self.Age1_Label.setText(QCoreApplication.translate("MainWindow", u"0 - 14", None))
        self.Age2_Label.setText(QCoreApplication.translate("MainWindow", u"15 - 24", None))
        self.Age3_Label.setText(QCoreApplication.translate("MainWindow", u"25 - 64", None))
        self.Age4_Label.setText(QCoreApplication.translate("MainWindow", u"+ 65", None))
        self.Climate_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">CLIMATE AND WEATHER</span></p></body></html>", None))
        self.Temperature_Label.setText(QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.Temperature_Picture.setText("")
        self.TempMonthMax_Label.setText(QCoreApplication.translate("MainWindow", u"Monthly max.", None))
        self.TempMonthMean_Label.setText(QCoreApplication.translate("MainWindow", u"Monthly mean", None))
        self.TempMonthlyMin_Label.setText(QCoreApplication.translate("MainWindow", u"Monthly min.", None))
        self.Rainfall_Label.setText(QCoreApplication.translate("MainWindow", u"Rainfall", None))
        self.Rainfall_Picture.setText("")
        self.RainAnnualMean_Label.setText(QCoreApplication.translate("MainWindow", u"Annual mean", None))
        self.RainMonthMax_Label.setText(QCoreApplication.translate("MainWindow", u"Monthly max.", None))
        self.RainMonthMean_Label.setText(QCoreApplication.translate("MainWindow", u"Monthly mean", None))
        self.NBS_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">NATURE-BASED SOLUTIONS</span></p></body></html>", None))
        self.NBS_Label_2.setText(QCoreApplication.translate("MainWindow", u"Existing NBS", None))
        ___qtablewidgetitem = self.NBS_Table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"NBS", None));
        ___qtablewidgetitem1 = self.NBS_Table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Characteristic", None));
        self.Service_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">SERVICE IDENTIFICATION</span></p></body></html>", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Stormwater utility", None))
        self.UtilityName_Label.setText(QCoreApplication.translate("MainWindow", u"Utility name", None))
        self.UtilityType_Label.setText(QCoreApplication.translate("MainWindow", u"Utility type", None))
        self.UtilityType_ComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Municipal department", None))
        self.UtilityType_ComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Public company", None))
        self.UtilityType_ComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Private company", None))

        self.UtilityType_ComboBox.setCurrentText("")
        self.UtilityType_ComboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select utility type...", None))
        self.Drainage_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">DRAINAGE SYSTEM</span></p></body></html>", None))
        self.Minor_Label.setText(QCoreApplication.translate("MainWindow", u"Minor system conveyance", None))
        self.Type_Label.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.SepLenght_Label.setText(QCoreApplication.translate("MainWindow", u"Separative length (km)", None))
        self.CombLenght_Label.setText(QCoreApplication.translate("MainWindow", u"Combined length (km)", None))
        self.Diameter_Label.setText(QCoreApplication.translate("MainWindow", u"Average diameter (mm)", None))
        self.Age_Label_2.setText(QCoreApplication.translate("MainWindow", u"Average age (years)", None))
        self.Outfall_Label.setText(QCoreApplication.translate("MainWindow", u"Number of outfalls", None))
        self.Receiver_Label.setText(QCoreApplication.translate("MainWindow", u"Outfall(s) discharge to", None))
        self.Receiver_Sea.setText(QCoreApplication.translate("MainWindow", u"Sea", None))
        self.Receiver_Estuary.setText(QCoreApplication.translate("MainWindow", u"Estuary", None))
        self.Receiver_River.setText(QCoreApplication.translate("MainWindow", u"River", None))
        self.Receiver_Other.setText(QCoreApplication.translate("MainWindow", u"Other(s)", None))
        self.Type_ComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Separative", None))
        self.Type_ComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Combined", None))
        self.Type_ComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Mixed", None))

        self.Type_ComboBox.setCurrentText("")
        self.Type_ComboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select conveynace type...", None))
        self.SpecialEq_Label.setText(QCoreApplication.translate("MainWindow", u"Special Equipment", None))
        ___qtablewidgetitem2 = self.SpecialEq_Table.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Equipment", None));
        ___qtablewidgetitem3 = self.SpecialEq_Table.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Characteristic", None));
        self.Situation_setup_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">SITUATION SETUP</span></p></body></html>", None))
        self.Situation_generator_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">SITUATION GENERATOR</span></p></body></html>", None))
        self.Manager_TabWidget.setTabText(self.Manager_TabWidget.indexOf(self.Manager_Page1), QCoreApplication.translate("MainWindow", u"Situation Manager", None))
        self.Manager_TabWidget.setTabText(self.Manager_TabWidget.indexOf(self.Manager_Page2), QCoreApplication.translate("MainWindow", u"Weight Setup", None))
        self.Manager_TabWidget.setTabText(self.Manager_TabWidget.indexOf(self.Manager_Page3), QCoreApplication.translate("MainWindow", u"Performance Setup", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Objective </span>/ Criteria</p></body></html>", None))
        ___qtreewidgetitem = self.Functional_list.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"1", None));
        self.Rainfall_selection_Label.setText(QCoreApplication.translate("MainWindow", u"Select rainfall return period:", None))
        self.Rainfall_selection_ComboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"None", None))
        self.Overall_Label.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700;\">RESILIENCE RATING</span></p></body></html>", None))
        self.OFR_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">FUNCTIONAL RATING</span></p></body></html>", None))
        self.OPR_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">PERFORMANCE RATING</span></p></body></html>", None))
        self.ORR_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">URBAN STORMWATER RESILIENCE INDEX</span></p></body></html>", None))
        self.Overall_Label_3.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700; color:#b0bea5;\">STRATEGIC DIMENSION</span></p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">CRITERIA RATING</span></p></body></html>", None))
        self.FCR_ComboBox.setCurrentText("")
        self.FCR_ComboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select objective...", None))
        self.FOC_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">OBJECTIVE ANSWERS' COMPLETNESS</span></p></body></html>", None))
        self.FOR_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">OBJECTIVES RATING</span></p></body></html>", None))
        self.Performance_Label.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700; color:#fa9884;\">PERFORMANCE DIMENSION</span></p></body></html>", None))
        self.PSR_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">SYSTEM RATING</span></p></body></html>", None))
        self.PCR_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">CONSEQUENCES RATING</span></p></body></html>", None))
        self.footer_left_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:7pt;\">Developed by Jo\u00e3o Barreiro </span><a href=\"mailto:joao.barreiro@tecnico.ulisboa.pt\"><span style=\" font-size:7pt; text-decoration: underline; color:#0000ff;\">(joao.barreiro@tecnico.ulisboa.pt)</span></a></p></body></html>", None))
        self.footer_right_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:7pt;\">Instituto Superior T\u00e9cnico - University of Lisbon</span></p></body></html>", None))
        self.menuFile_F.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

