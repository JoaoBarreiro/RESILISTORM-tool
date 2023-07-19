# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainPage_V4JosGzH.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QListView,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTabWidget,
    QTableWidget, QTableWidgetItem, QToolBox, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.resize(1280, 828)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1280, 720))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(u":/icon/icons/REFUSS LOGO.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        MainWindow.setIconSize(QSize(25, 25))
        MainWindow.setToolButtonStyle(Qt.ToolButtonTextOnly)
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
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.Org0_TopREFUSS = QWidget(self.centralwidget)
        self.Org0_TopREFUSS.setObjectName(u"Org0_TopREFUSS")
        self.Org0_TopREFUSS.setStyleSheet(u"background-color: #FBC156;")
        self.horizontalLayout = QHBoxLayout(self.Org0_TopREFUSS)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.REFUSS2_label = QLabel(self.Org0_TopREFUSS)
        self.REFUSS2_label.setObjectName(u"REFUSS2_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.REFUSS2_label.sizePolicy().hasHeightForWidth())
        self.REFUSS2_label.setSizePolicy(sizePolicy1)
        self.REFUSS2_label.setMinimumSize(QSize(0, 0))
        self.REFUSS2_label.setTextFormat(Qt.AutoText)
        self.REFUSS2_label.setScaledContents(True)
        self.REFUSS2_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.REFUSS2_label.setWordWrap(True)
        self.REFUSS2_label.setIndent(0)
        self.REFUSS2_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

        self.gridLayout_7.addWidget(self.REFUSS2_label, 0, 1, 1, 1)

        self.REFUSS_label = QLabel(self.Org0_TopREFUSS)
        self.REFUSS_label.setObjectName(u"REFUSS_label")
        self.REFUSS_label.setScaledContents(True)
        self.REFUSS_label.setAlignment(Qt.AlignCenter)
        self.REFUSS_label.setWordWrap(False)
        self.REFUSS_label.setIndent(0)

        self.gridLayout_7.addWidget(self.REFUSS_label, 0, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_7)


        self.verticalLayout_5.addWidget(self.Org0_TopREFUSS)

        self.Org1_TopBar = QHBoxLayout()
        self.Org1_TopBar.setSpacing(0)
        self.Org1_TopBar.setObjectName(u"Org1_TopBar")
        self.MenuWidget = QWidget(self.centralwidget)
        self.MenuWidget.setObjectName(u"MenuWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.MenuWidget.sizePolicy().hasHeightForWidth())
        self.MenuWidget.setSizePolicy(sizePolicy2)
        self.MenuWidget.setMinimumSize(QSize(50, 0))
        self.MenuWidget.setMaximumSize(QSize(50, 16777215))
        self.MenuWidget.setStyleSheet(u"background-color: rgba(251, 193, 86, 100)")
        self.verticalLayout_3 = QVBoxLayout(self.MenuWidget)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.menu_btn = QPushButton(self.MenuWidget)
        self.menu_btn.setObjectName(u"menu_btn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.menu_btn.sizePolicy().hasHeightForWidth())
        self.menu_btn.setSizePolicy(sizePolicy3)
        self.menu_btn.setMinimumSize(QSize(40, 40))
        self.menu_btn.setMaximumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.menu_btn.setFont(font)
        self.menu_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: #526D82;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/icon/icons/menu.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_btn.setIcon(icon6)
        self.menu_btn.setIconSize(QSize(25, 25))
        self.menu_btn.setCheckable(True)
        self.menu_btn.setChecked(False)
        self.menu_btn.setAutoExclusive(False)

        self.verticalLayout_3.addWidget(self.menu_btn, 0, Qt.AlignTop)


        self.Org1_TopBar.addWidget(self.MenuWidget)

        self.MenuWidget_2 = QWidget(self.centralwidget)
        self.MenuWidget_2.setObjectName(u"MenuWidget_2")
        sizePolicy2.setHeightForWidth(self.MenuWidget_2.sizePolicy().hasHeightForWidth())
        self.MenuWidget_2.setSizePolicy(sizePolicy2)
        self.MenuWidget_2.setMinimumSize(QSize(270, 0))
        self.MenuWidget_2.setStyleSheet(u"background-color: rgba(251, 193, 86, 100)")
        self.verticalLayout_2 = QVBoxLayout(self.MenuWidget_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.menu_btn_2 = QPushButton(self.MenuWidget_2)
        self.menu_btn_2.setObjectName(u"menu_btn_2")
        sizePolicy3.setHeightForWidth(self.menu_btn_2.sizePolicy().hasHeightForWidth())
        self.menu_btn_2.setSizePolicy(sizePolicy3)
        self.menu_btn_2.setMinimumSize(QSize(260, 40))
        self.menu_btn_2.setMaximumSize(QSize(0, 0))
        self.menu_btn_2.setFont(font)
        self.menu_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(82, 109, 130, 255), stop:1 rgba(221, 230, 237, 255));\n"
"}\n"
"")
        icon7 = QIcon()
        icon7.addFile(u":/icon/icons/left_arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_btn_2.setIcon(icon7)
        self.menu_btn_2.setIconSize(QSize(25, 25))
        self.menu_btn_2.setCheckable(True)
        self.menu_btn_2.setChecked(False)
        self.menu_btn_2.setAutoExclusive(False)
        self.menu_btn_2.setAutoDefault(False)
        self.menu_btn_2.setFlat(False)

        self.verticalLayout_2.addWidget(self.menu_btn_2, 0, Qt.AlignVCenter)


        self.Org1_TopBar.addWidget(self.MenuWidget_2)

        self.TitlesWidget = QStackedWidget(self.centralwidget)
        self.TitlesWidget.setObjectName(u"TitlesWidget")
        sizePolicy.setHeightForWidth(self.TitlesWidget.sizePolicy().hasHeightForWidth())
        self.TitlesWidget.setSizePolicy(sizePolicy)
        self.TitlesWidget.setMinimumSize(QSize(0, 40))
        self.TitlesWidget.setLineWidth(0)
        self.Page0_Home_2 = QWidget()
        self.Page0_Home_2.setObjectName(u"Page0_Home_2")
        self.Page0_Home_2.setStyleSheet(u"background-color: #C5DFF8")
        self.gridLayout_16 = QGridLayout(self.Page0_Home_2)
        self.gridLayout_16.setSpacing(0)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.H_Label = QLabel(self.Page0_Home_2)
        self.H_Label.setObjectName(u"H_Label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.H_Label.sizePolicy().hasHeightForWidth())
        self.H_Label.setSizePolicy(sizePolicy4)
        self.H_Label.setMinimumSize(QSize(0, 50))
        self.H_Label.setMaximumSize(QSize(16777215, 16777215))
        self.H_Label.setStyleSheet(u"background-color: #7895CB;")
        self.H_Label.setAlignment(Qt.AlignCenter)

        self.gridLayout_16.addWidget(self.H_Label, 0, 0, 1, 1)

        self.TitlesWidget.addWidget(self.Page0_Home_2)
        self.Page1_UProfile_2 = QWidget()
        self.Page1_UProfile_2.setObjectName(u"Page1_UProfile_2")
        self.Page1_UProfile_2.setStyleSheet(u"background-color: #fcfce8;")
        self.gridLayout_19 = QGridLayout(self.Page1_UProfile_2)
        self.gridLayout_19.setSpacing(5)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.UP_Label = QLabel(self.Page1_UProfile_2)
        self.UP_Label.setObjectName(u"UP_Label")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.UP_Label.sizePolicy().hasHeightForWidth())
        self.UP_Label.setSizePolicy(sizePolicy5)
        self.UP_Label.setMinimumSize(QSize(0, 0))
        self.UP_Label.setMaximumSize(QSize(16777215, 50))
        self.UP_Label.setStyleSheet(u"background-color: #fde968;")
        self.UP_Label.setAlignment(Qt.AlignCenter)

        self.gridLayout_19.addWidget(self.UP_Label, 0, 0, 1, 1)

        self.TitlesWidget.addWidget(self.Page1_UProfile_2)
        self.Page2_SWProfile_2 = QWidget()
        self.Page2_SWProfile_2.setObjectName(u"Page2_SWProfile_2")
        self.Page2_SWProfile_2.setStyleSheet(u"background-color: #e7fcfe;")
        self.gridLayout_21 = QGridLayout(self.Page2_SWProfile_2)
        self.gridLayout_21.setSpacing(5)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.UP_Label_2 = QLabel(self.Page2_SWProfile_2)
        self.UP_Label_2.setObjectName(u"UP_Label_2")
        sizePolicy.setHeightForWidth(self.UP_Label_2.sizePolicy().hasHeightForWidth())
        self.UP_Label_2.setSizePolicy(sizePolicy)
        self.UP_Label_2.setMinimumSize(QSize(0, 0))
        self.UP_Label_2.setMaximumSize(QSize(16777215, 50))
        self.UP_Label_2.setStyleSheet(u"background-color: #71c7ec;")
        self.UP_Label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_21.addWidget(self.UP_Label_2, 0, 0, 1, 1)

        self.TitlesWidget.addWidget(self.Page2_SWProfile_2)
        self.Page3_Functional_2 = QWidget()
        self.Page3_Functional_2.setObjectName(u"Page3_Functional_2")
        self.Page3_Functional_2.setStyleSheet(u"background-color: rgb(228, 247, 233)")
        self.Page3_Functional_4 = QGridLayout(self.Page3_Functional_2)
        self.Page3_Functional_4.setSpacing(5)
        self.Page3_Functional_4.setObjectName(u"Page3_Functional_4")
        self.Page3_Functional_4.setContentsMargins(0, 0, 0, 0)
        self.FD_Label = QLabel(self.Page3_Functional_2)
        self.FD_Label.setObjectName(u"FD_Label")
        sizePolicy.setHeightForWidth(self.FD_Label.sizePolicy().hasHeightForWidth())
        self.FD_Label.setSizePolicy(sizePolicy)
        self.FD_Label.setMinimumSize(QSize(0, 0))
        self.FD_Label.setMaximumSize(QSize(16777215, 50))
        self.FD_Label.setStyleSheet(u"background-color: #C1D0B5;")
        self.FD_Label.setAlignment(Qt.AlignCenter)

        self.Page3_Functional_4.addWidget(self.FD_Label, 0, 0, 1, 1)

        self.TitlesWidget.addWidget(self.Page3_Functional_2)
        self.Page4_Performance_2 = QWidget()
        self.Page4_Performance_2.setObjectName(u"Page4_Performance_2")
        self.Page4_Performance_2.setStyleSheet(u"background-color: #FFF3E2;")
        self.Page4_Performance_4 = QGridLayout(self.Page4_Performance_2)
        self.Page4_Performance_4.setSpacing(5)
        self.Page4_Performance_4.setObjectName(u"Page4_Performance_4")
        self.Page4_Performance_4.setContentsMargins(0, 0, 0, 0)
        self.PD_Label = QLabel(self.Page4_Performance_2)
        self.PD_Label.setObjectName(u"PD_Label")
        sizePolicy.setHeightForWidth(self.PD_Label.sizePolicy().hasHeightForWidth())
        self.PD_Label.setSizePolicy(sizePolicy)
        self.PD_Label.setMinimumSize(QSize(0, 0))
        self.PD_Label.setMaximumSize(QSize(16777215, 50))
        self.PD_Label.setStyleSheet(u"background-color: #FA9884;")
        self.PD_Label.setAlignment(Qt.AlignCenter)

        self.Page4_Performance_4.addWidget(self.PD_Label, 0, 0, 1, 1)

        self.TitlesWidget.addWidget(self.Page4_Performance_2)
        self.Page5_Dashboard_2 = QWidget()
        self.Page5_Dashboard_2.setObjectName(u"Page5_Dashboard_2")
        self.Page5_Dashboard_2.setStyleSheet(u"background-color: rgb(218, 238, 236)")
        self.gridLayout_25 = QGridLayout(self.Page5_Dashboard_2)
        self.gridLayout_25.setSpacing(5)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(0, 0, 0, 0)
        self.PD_Label_5 = QLabel(self.Page5_Dashboard_2)
        self.PD_Label_5.setObjectName(u"PD_Label_5")
        sizePolicy.setHeightForWidth(self.PD_Label_5.sizePolicy().hasHeightForWidth())
        self.PD_Label_5.setSizePolicy(sizePolicy)
        self.PD_Label_5.setMinimumSize(QSize(0, 0))
        self.PD_Label_5.setMaximumSize(QSize(16777215, 50))
        self.PD_Label_5.setStyleSheet(u"background-color: #569DAA;")
        self.PD_Label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.PD_Label_5, 0, 0, 1, 1)

        self.TitlesWidget.addWidget(self.Page5_Dashboard_2)

        self.Org1_TopBar.addWidget(self.TitlesWidget)


        self.verticalLayout_5.addLayout(self.Org1_TopBar)

        self.Org2_Body = QHBoxLayout()
        self.Org2_Body.setSpacing(0)
        self.Org2_Body.setObjectName(u"Org2_Body")
        self.LeftMenuWidget = QWidget(self.centralwidget)
        self.LeftMenuWidget.setObjectName(u"LeftMenuWidget")
        sizePolicy2.setHeightForWidth(self.LeftMenuWidget.sizePolicy().hasHeightForWidth())
        self.LeftMenuWidget.setSizePolicy(sizePolicy2)
        self.LeftMenuWidget.setMinimumSize(QSize(50, 0))
        self.LeftMenuWidget.setMaximumSize(QSize(50, 16777215))
        self.LeftMenuWidget.setStyleSheet(u"background-color: rgba(251, 193, 86, 100)")
        self.LeftMenuWidget.setInputMethodHints(Qt.ImhNone)
        self.verticalLayout_10 = QVBoxLayout(self.LeftMenuWidget)
        self.verticalLayout_10.setSpacing(10)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(5, 10, 5, 10)
        self.home_btn = QPushButton(self.LeftMenuWidget)
        self.home_btn.setObjectName(u"home_btn")
        sizePolicy3.setHeightForWidth(self.home_btn.sizePolicy().hasHeightForWidth())
        self.home_btn.setSizePolicy(sizePolicy3)
        self.home_btn.setMinimumSize(QSize(40, 40))
        self.home_btn.setMaximumSize(QSize(0, 0))
        self.home_btn.setFont(font)
        self.home_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"    padding: 0;  /* Remove any padding */\n"
"    margin: 0;  /* Remove any margin */\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: #7895CB;\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u":/icon/icons/house-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.home_btn.setIcon(icon8)
        self.home_btn.setIconSize(QSize(25, 25))
        self.home_btn.setCheckable(True)
        self.home_btn.setChecked(False)
        self.home_btn.setAutoExclusive(True)

        self.verticalLayout_10.addWidget(self.home_btn, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_3)

        self.urbanprofile_btn = QPushButton(self.LeftMenuWidget)
        self.urbanprofile_btn.setObjectName(u"urbanprofile_btn")
        sizePolicy3.setHeightForWidth(self.urbanprofile_btn.sizePolicy().hasHeightForWidth())
        self.urbanprofile_btn.setSizePolicy(sizePolicy3)
        self.urbanprofile_btn.setMinimumSize(QSize(40, 40))
        self.urbanprofile_btn.setMaximumSize(QSize(0, 0))
        self.urbanprofile_btn.setFont(font)
        self.urbanprofile_btn.setAcceptDrops(False)
        self.urbanprofile_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 2px solid black;\n"
"\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: #FFFDE968;\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u":/icon/icons/city-building.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.urbanprofile_btn.setIcon(icon9)
        self.urbanprofile_btn.setIconSize(QSize(25, 25))
        self.urbanprofile_btn.setCheckable(True)
        self.urbanprofile_btn.setAutoExclusive(True)
        self.urbanprofile_btn.setFlat(False)

        self.verticalLayout_10.addWidget(self.urbanprofile_btn, 0, Qt.AlignVCenter)

        self.stormprofile_btn = QPushButton(self.LeftMenuWidget)
        self.stormprofile_btn.setObjectName(u"stormprofile_btn")
        sizePolicy3.setHeightForWidth(self.stormprofile_btn.sizePolicy().hasHeightForWidth())
        self.stormprofile_btn.setSizePolicy(sizePolicy3)
        self.stormprofile_btn.setMinimumSize(QSize(40, 40))
        self.stormprofile_btn.setMaximumSize(QSize(0, 0))
        self.stormprofile_btn.setFont(font)
        self.stormprofile_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: #FF71C7EC;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u":/icon/icons/manhole_cover-48_44623.png", QSize(), QIcon.Normal, QIcon.Off)
        self.stormprofile_btn.setIcon(icon10)
        self.stormprofile_btn.setIconSize(QSize(25, 25))
        self.stormprofile_btn.setCheckable(True)
        self.stormprofile_btn.setAutoExclusive(True)

        self.verticalLayout_10.addWidget(self.stormprofile_btn, 0, Qt.AlignVCenter)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_5)

        self.functional_btn = QPushButton(self.LeftMenuWidget)
        self.functional_btn.setObjectName(u"functional_btn")
        sizePolicy3.setHeightForWidth(self.functional_btn.sizePolicy().hasHeightForWidth())
        self.functional_btn.setSizePolicy(sizePolicy3)
        self.functional_btn.setMinimumSize(QSize(40, 40))
        self.functional_btn.setMaximumSize(QSize(0, 0))
        self.functional_btn.setFont(font)
        self.functional_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: #FFC1D0B5;\n"
"\n"
"}")
        icon11 = QIcon()
        icon11.addFile(u":/icon/icons/settings-13-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.functional_btn.setIcon(icon11)
        self.functional_btn.setIconSize(QSize(25, 25))
        self.functional_btn.setCheckable(True)
        self.functional_btn.setChecked(False)
        self.functional_btn.setAutoExclusive(True)

        self.verticalLayout_10.addWidget(self.functional_btn, 0, Qt.AlignVCenter)

        self.performance_btn = QPushButton(self.LeftMenuWidget)
        self.performance_btn.setObjectName(u"performance_btn")
        sizePolicy3.setHeightForWidth(self.performance_btn.sizePolicy().hasHeightForWidth())
        self.performance_btn.setSizePolicy(sizePolicy3)
        self.performance_btn.setMinimumSize(QSize(40, 40))
        self.performance_btn.setMaximumSize(QSize(0, 0))
        self.performance_btn.setFont(font)
        self.performance_btn.setAcceptDrops(True)
        self.performance_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: #FFFA9884;\n"
"}")
        icon12 = QIcon()
        icon12.addFile(u":/icon/icons/rain-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.performance_btn.setIcon(icon12)
        self.performance_btn.setIconSize(QSize(25, 25))
        self.performance_btn.setCheckable(True)
        self.performance_btn.setAutoExclusive(True)

        self.verticalLayout_10.addWidget(self.performance_btn, 0, Qt.AlignVCenter)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_10)

        self.dashboard_btn = QPushButton(self.LeftMenuWidget)
        self.dashboard_btn.setObjectName(u"dashboard_btn")
        sizePolicy3.setHeightForWidth(self.dashboard_btn.sizePolicy().hasHeightForWidth())
        self.dashboard_btn.setSizePolicy(sizePolicy3)
        self.dashboard_btn.setMinimumSize(QSize(40, 40))
        self.dashboard_btn.setMaximumSize(QSize(0, 0))
        self.dashboard_btn.setFont(font)
        self.dashboard_btn.setAcceptDrops(True)
        self.dashboard_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: #FF569DAA;\n"
"}")
        icon13 = QIcon()
        icon13.addFile(u":/icon/icons/dashboard-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.dashboard_btn.setIcon(icon13)
        self.dashboard_btn.setIconSize(QSize(25, 25))
        self.dashboard_btn.setCheckable(True)
        self.dashboard_btn.setAutoExclusive(True)

        self.verticalLayout_10.addWidget(self.dashboard_btn, 0, Qt.AlignVCenter)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_7)


        self.Org2_Body.addWidget(self.LeftMenuWidget)

        self.LeftMenuWidget_2 = QWidget(self.centralwidget)
        self.LeftMenuWidget_2.setObjectName(u"LeftMenuWidget_2")
        sizePolicy2.setHeightForWidth(self.LeftMenuWidget_2.sizePolicy().hasHeightForWidth())
        self.LeftMenuWidget_2.setSizePolicy(sizePolicy2)
        self.LeftMenuWidget_2.setMinimumSize(QSize(270, 0))
        self.LeftMenuWidget_2.setStyleSheet(u"background-color: rgba(251, 193, 86, 100)")
        self.verticalLayout_9 = QVBoxLayout(self.LeftMenuWidget_2)
        self.verticalLayout_9.setSpacing(10)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 10, 5, 10)
        self.home_btn_2 = QPushButton(self.LeftMenuWidget_2)
        self.home_btn_2.setObjectName(u"home_btn_2")
        sizePolicy3.setHeightForWidth(self.home_btn_2.sizePolicy().hasHeightForWidth())
        self.home_btn_2.setSizePolicy(sizePolicy3)
        self.home_btn_2.setMinimumSize(QSize(260, 40))
        self.home_btn_2.setMaximumSize(QSize(0, 0))
        self.home_btn_2.setFont(font)
        self.home_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(120, 149, 203, 255), stop:1 rgba(197, 223, 248, 255));\n"
"}\n"
"")
        self.home_btn_2.setIcon(icon8)
        self.home_btn_2.setIconSize(QSize(25, 25))
        self.home_btn_2.setCheckable(True)
        self.home_btn_2.setChecked(False)
        self.home_btn_2.setAutoExclusive(True)
        self.home_btn_2.setAutoDefault(False)
        self.home_btn_2.setFlat(False)

        self.verticalLayout_9.addWidget(self.home_btn_2, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer)

        self.urbanprofile_btn_2 = QPushButton(self.LeftMenuWidget_2)
        self.urbanprofile_btn_2.setObjectName(u"urbanprofile_btn_2")
        sizePolicy3.setHeightForWidth(self.urbanprofile_btn_2.sizePolicy().hasHeightForWidth())
        self.urbanprofile_btn_2.setSizePolicy(sizePolicy3)
        self.urbanprofile_btn_2.setMinimumSize(QSize(260, 40))
        self.urbanprofile_btn_2.setMaximumSize(QSize(0, 0))
        self.urbanprofile_btn_2.setFont(font)
        self.urbanprofile_btn_2.setAcceptDrops(False)
        self.urbanprofile_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(253, 233, 104, 255), stop:1 rgba(252, 252, 232, 255));\n"
"}\n"
"")
        self.urbanprofile_btn_2.setIcon(icon9)
        self.urbanprofile_btn_2.setIconSize(QSize(25, 25))
        self.urbanprofile_btn_2.setCheckable(True)
        self.urbanprofile_btn_2.setAutoExclusive(True)
        self.urbanprofile_btn_2.setFlat(False)

        self.verticalLayout_9.addWidget(self.urbanprofile_btn_2, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.stormprofile_btn_2 = QPushButton(self.LeftMenuWidget_2)
        self.stormprofile_btn_2.setObjectName(u"stormprofile_btn_2")
        sizePolicy3.setHeightForWidth(self.stormprofile_btn_2.sizePolicy().hasHeightForWidth())
        self.stormprofile_btn_2.setSizePolicy(sizePolicy3)
        self.stormprofile_btn_2.setMinimumSize(QSize(260, 40))
        self.stormprofile_btn_2.setMaximumSize(QSize(0, 0))
        self.stormprofile_btn_2.setFont(font)
        self.stormprofile_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"  \n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(113, 199, 236, 255), stop:1 rgba(231, 252, 254, 255));\n"
"}\n"
"")
        self.stormprofile_btn_2.setIcon(icon10)
        self.stormprofile_btn_2.setIconSize(QSize(25, 25))
        self.stormprofile_btn_2.setCheckable(True)
        self.stormprofile_btn_2.setAutoExclusive(True)

        self.verticalLayout_9.addWidget(self.stormprofile_btn_2, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_4)

        self.functional_btn_2 = QPushButton(self.LeftMenuWidget_2)
        self.functional_btn_2.setObjectName(u"functional_btn_2")
        sizePolicy3.setHeightForWidth(self.functional_btn_2.sizePolicy().hasHeightForWidth())
        self.functional_btn_2.setSizePolicy(sizePolicy3)
        self.functional_btn_2.setMinimumSize(QSize(260, 40))
        self.functional_btn_2.setMaximumSize(QSize(0, 0))
        self.functional_btn_2.setFont(font)
        self.functional_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	 background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(193, 208, 181, 255), stop:1 rgba(228, 247, 233, 255));\n"
"}\n"
"\\")
        self.functional_btn_2.setIcon(icon11)
        self.functional_btn_2.setIconSize(QSize(25, 25))
        self.functional_btn_2.setCheckable(True)
        self.functional_btn_2.setChecked(False)
        self.functional_btn_2.setAutoExclusive(True)

        self.verticalLayout_9.addWidget(self.functional_btn_2, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.performance_btn_2 = QPushButton(self.LeftMenuWidget_2)
        self.performance_btn_2.setObjectName(u"performance_btn_2")
        sizePolicy3.setHeightForWidth(self.performance_btn_2.sizePolicy().hasHeightForWidth())
        self.performance_btn_2.setSizePolicy(sizePolicy3)
        self.performance_btn_2.setMinimumSize(QSize(260, 40))
        self.performance_btn_2.setMaximumSize(QSize(0, 0))
        self.performance_btn_2.setFont(font)
        self.performance_btn_2.setAcceptDrops(True)
        self.performance_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(250, 152, 132, 255), stop:1 rgba(255, 243, 226, 255));\n"
"}\n"
"")
        self.performance_btn_2.setIcon(icon12)
        self.performance_btn_2.setIconSize(QSize(25, 25))
        self.performance_btn_2.setCheckable(True)
        self.performance_btn_2.setAutoExclusive(True)

        self.verticalLayout_9.addWidget(self.performance_btn_2, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_8)

        self.dashboard_btn_2 = QPushButton(self.LeftMenuWidget_2)
        self.dashboard_btn_2.setObjectName(u"dashboard_btn_2")
        sizePolicy3.setHeightForWidth(self.dashboard_btn_2.sizePolicy().hasHeightForWidth())
        self.dashboard_btn_2.setSizePolicy(sizePolicy3)
        self.dashboard_btn_2.setMinimumSize(QSize(260, 40))
        self.dashboard_btn_2.setMaximumSize(QSize(0, 0))
        self.dashboard_btn_2.setFont(font)
        self.dashboard_btn_2.setAcceptDrops(True)
        self.dashboard_btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"	Text-align:left;\n"
"    border-radius: 20px;\n"
"	padding-left: 10px;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    \n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(86, 157, 170, 255), stop:1 rgba(218, 238, 236, 255));\n"
"}\n"
"")
        self.dashboard_btn_2.setIcon(icon13)
        self.dashboard_btn_2.setIconSize(QSize(25, 25))
        self.dashboard_btn_2.setCheckable(True)
        self.dashboard_btn_2.setAutoExclusive(True)

        self.verticalLayout_9.addWidget(self.dashboard_btn_2, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_6)


        self.Org2_Body.addWidget(self.LeftMenuWidget_2)

        self.BodyWidget = QStackedWidget(self.centralwidget)
        self.BodyWidget.setObjectName(u"BodyWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.BodyWidget.sizePolicy().hasHeightForWidth())
        self.BodyWidget.setSizePolicy(sizePolicy6)
        self.BodyWidget.setStyleSheet(u"background-color: rgb(218, 238, 236)")
        self.BodyWidget.setLineWidth(0)
        self.Page0_Home = QWidget()
        self.Page0_Home.setObjectName(u"Page0_Home")
        self.gridLayout_2 = QGridLayout(self.Page0_Home)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Home_Back_Widget = QWidget(self.Page0_Home)
        self.Home_Back_Widget.setObjectName(u"Home_Back_Widget")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.Home_Back_Widget.sizePolicy().hasHeightForWidth())
        self.Home_Back_Widget.setSizePolicy(sizePolicy7)
        self.Home_Back_Widget.setStyleSheet(u"background-color: #C5DFF8")
        self.gridLayout_12 = QGridLayout(self.Home_Back_Widget)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(5, 5, 5, 5)
        self.Home_Label2 = QLabel(self.Home_Back_Widget)
        self.Home_Label2.setObjectName(u"Home_Label2")
        self.Home_Label2.setAlignment(Qt.AlignJustify|Qt.AlignTop)
        self.Home_Label2.setWordWrap(True)

        self.gridLayout_12.addWidget(self.Home_Label2, 1, 0, 1, 1)

        self.Home_Label1 = QLabel(self.Home_Back_Widget)
        self.Home_Label1.setObjectName(u"Home_Label1")
        self.Home_Label1.setAlignment(Qt.AlignJustify|Qt.AlignTop)
        self.Home_Label1.setWordWrap(True)

        self.gridLayout_12.addWidget(self.Home_Label1, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.Home_Back_Widget, 0, 0, 1, 1)

        self.BodyWidget.addWidget(self.Page0_Home)
        self.Page1_UProfile = QWidget()
        self.Page1_UProfile.setObjectName(u"Page1_UProfile")
        self.Page1_UProfile.setStyleSheet(u"background-color: #fcfce8;")
        self.gridLayout_4 = QGridLayout(self.Page1_UProfile)
        self.gridLayout_4.setSpacing(5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.UP_Back_Widget = QWidget(self.Page1_UProfile)
        self.UP_Back_Widget.setObjectName(u"UP_Back_Widget")
        self.UP_Back_Widget.setStyleSheet(u"background-color: #fcfce8;")
        self.gridLayout_6 = QGridLayout(self.UP_Back_Widget)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(10, 10, 10, 10)
        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_16, 1, 0, 1, 1)

        self.UP_ToolBox = QToolBox(self.UP_Back_Widget)
        self.UP_ToolBox.setObjectName(u"UP_ToolBox")
        self.UP_ToolBox.setStyleSheet(u"QToolBox::tab {\n"
"	background-color: rgb(255, 255, 255);\n"
"	border-radius: 12px;	\n"
"	border: 2px solid black;\n"
"	}\n"
"\n"
"QToolBox::tab::selected {\n"
"    background-color: rgb(253, 233, 104);\n"
"	font: 700 9pt \"Segoe UI\";\n"
"}\n"
"\n"
"")
        self.Domain_Box = QWidget()
        self.Domain_Box.setObjectName(u"Domain_Box")
        self.Domain_Box.setGeometry(QRect(0, 0, 177, 250))
        self.verticalLayout_12 = QVBoxLayout(self.Domain_Box)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.StudyName_Form_3 = QFormLayout()
        self.StudyName_Form_3.setObjectName(u"StudyName_Form_3")
        self.StudyName_Form_3.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.StudyName_Form_3.setHorizontalSpacing(5)
        self.StudyName_Form_3.setVerticalSpacing(5)
        self.StudyName_Form_3.setContentsMargins(0, -1, -1, -1)
        self.studyNameLabel_3 = QLabel(self.Domain_Box)
        self.studyNameLabel_3.setObjectName(u"studyNameLabel_3")
        self.studyNameLabel_3.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")

        self.StudyName_Form_3.setWidget(0, QFormLayout.LabelRole, self.studyNameLabel_3)

        self.studyNameLineEdit_3 = QLineEdit(self.Domain_Box)
        self.studyNameLineEdit_3.setObjectName(u"studyNameLineEdit_3")
        self.studyNameLineEdit_3.setStyleSheet(u"background-color: white;")

        self.StudyName_Form_3.setWidget(0, QFormLayout.FieldRole, self.studyNameLineEdit_3)

        self.Location_Label_2 = QLabel(self.Domain_Box)
        self.Location_Label_2.setObjectName(u"Location_Label_2")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.Location_Label_2.sizePolicy().hasHeightForWidth())
        self.Location_Label_2.setSizePolicy(sizePolicy8)
        self.Location_Label_2.setMaximumSize(QSize(16777215, 15))
        self.Location_Label_2.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")
        self.Location_Label_2.setTextFormat(Qt.AutoText)
        self.Location_Label_2.setMargin(0)

        self.StudyName_Form_3.setWidget(1, QFormLayout.LabelRole, self.Location_Label_2)

        self.countryLabel_6 = QLabel(self.Domain_Box)
        self.countryLabel_6.setObjectName(u"countryLabel_6")
        self.countryLabel_6.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")

        self.StudyName_Form_3.setWidget(2, QFormLayout.LabelRole, self.countryLabel_6)

        self.countryLineEdit_6 = QLineEdit(self.Domain_Box)
        self.countryLineEdit_6.setObjectName(u"countryLineEdit_6")
        self.countryLineEdit_6.setStyleSheet(u"background-color: white;")

        self.StudyName_Form_3.setWidget(2, QFormLayout.FieldRole, self.countryLineEdit_6)

        self.regionLabel_4 = QLabel(self.Domain_Box)
        self.regionLabel_4.setObjectName(u"regionLabel_4")
        self.regionLabel_4.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")

        self.StudyName_Form_3.setWidget(3, QFormLayout.LabelRole, self.regionLabel_4)

        self.regionLineEdit_4 = QLineEdit(self.Domain_Box)
        self.regionLineEdit_4.setObjectName(u"regionLineEdit_4")
        self.regionLineEdit_4.setStyleSheet(u"background-color: white;")

        self.StudyName_Form_3.setWidget(3, QFormLayout.FieldRole, self.regionLineEdit_4)

        self.cityLabel_4 = QLabel(self.Domain_Box)
        self.cityLabel_4.setObjectName(u"cityLabel_4")
        self.cityLabel_4.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")

        self.StudyName_Form_3.setWidget(4, QFormLayout.LabelRole, self.cityLabel_4)

        self.cityLineEdit_4 = QLineEdit(self.Domain_Box)
        self.cityLineEdit_4.setObjectName(u"cityLineEdit_4")
        self.cityLineEdit_4.setStyleSheet(u"background-color: white;")

        self.StudyName_Form_3.setWidget(4, QFormLayout.FieldRole, self.cityLineEdit_4)

        self.Catchment_Label_2 = QLabel(self.Domain_Box)
        self.Catchment_Label_2.setObjectName(u"Catchment_Label_2")
        self.Catchment_Label_2.setMaximumSize(QSize(16777215, 15))
        self.Catchment_Label_2.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);\n"
"\n"
"border: 2px;\n"
"border-bottom-color: rgb(255, 170, 0);")
        self.Catchment_Label_2.setTextFormat(Qt.RichText)

        self.StudyName_Form_3.setWidget(5, QFormLayout.LabelRole, self.Catchment_Label_2)

        self.nameLabel_2 = QLabel(self.Domain_Box)
        self.nameLabel_2.setObjectName(u"nameLabel_2")
        self.nameLabel_2.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")

        self.StudyName_Form_3.setWidget(6, QFormLayout.LabelRole, self.nameLabel_2)

        self.nameLineEdit_2 = QLineEdit(self.Domain_Box)
        self.nameLineEdit_2.setObjectName(u"nameLineEdit_2")
        self.nameLineEdit_2.setStyleSheet(u"background-color: white")
        self.nameLineEdit_2.setDragEnabled(True)
        self.nameLineEdit_2.setClearButtonEnabled(False)

        self.StudyName_Form_3.setWidget(6, QFormLayout.FieldRole, self.nameLineEdit_2)

        self.areaM2Label_2 = QLabel(self.Domain_Box)
        self.areaM2Label_2.setObjectName(u"areaM2Label_2")
        self.areaM2Label_2.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")

        self.StudyName_Form_3.setWidget(7, QFormLayout.LabelRole, self.areaM2Label_2)

        self.areaM2LineEdit_2 = QLineEdit(self.Domain_Box)
        self.areaM2LineEdit_2.setObjectName(u"areaM2LineEdit_2")
        self.areaM2LineEdit_2.setStyleSheet(u"background-color: white")

        self.StudyName_Form_3.setWidget(7, QFormLayout.FieldRole, self.areaM2LineEdit_2)

        self.averageSlopeLabel_2 = QLabel(self.Domain_Box)
        self.averageSlopeLabel_2.setObjectName(u"averageSlopeLabel_2")
        self.averageSlopeLabel_2.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")

        self.StudyName_Form_3.setWidget(8, QFormLayout.LabelRole, self.averageSlopeLabel_2)

        self.averageSlopeLineEdit_2 = QLineEdit(self.Domain_Box)
        self.averageSlopeLineEdit_2.setObjectName(u"averageSlopeLineEdit_2")
        self.averageSlopeLineEdit_2.setStyleSheet(u"background-color: white")

        self.StudyName_Form_3.setWidget(8, QFormLayout.FieldRole, self.averageSlopeLineEdit_2)


        self.verticalLayout_12.addLayout(self.StudyName_Form_3)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_9)

        self.UP_ToolBox.addItem(self.Domain_Box, u"DOMAIN")
        self.Population_Box = QWidget()
        self.Population_Box.setObjectName(u"Population_Box")
        self.Population_Box.setGeometry(QRect(0, 0, 215, 250))
        self.verticalLayout_13 = QVBoxLayout(self.Population_Box)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.Age_Layout_5 = QFormLayout()
        self.Age_Layout_5.setObjectName(u"Age_Layout_5")
        self.Age_Layout_5.setRowWrapPolicy(QFormLayout.DontWrapRows)
        self.Age_Layout_5.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Age_Layout_5.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.Age_Layout_5.setHorizontalSpacing(5)
        self.Age_Layout_5.setVerticalSpacing(5)
        self.Age_Layout_5.setContentsMargins(0, -1, -1, -1)
        self.age0Label_5 = QLabel(self.Population_Box)
        self.age0Label_5.setObjectName(u"age0Label_5")

        self.Age_Layout_5.setWidget(2, QFormLayout.LabelRole, self.age0Label_5)

        self.age14LineEdit_5 = QLineEdit(self.Population_Box)
        self.age14LineEdit_5.setObjectName(u"age14LineEdit_5")
        self.age14LineEdit_5.setStyleSheet(u"background-color: white")

        self.Age_Layout_5.setWidget(2, QFormLayout.FieldRole, self.age14LineEdit_5)

        self.age15LAbel_5 = QLabel(self.Population_Box)
        self.age15LAbel_5.setObjectName(u"age15LAbel_5")

        self.Age_Layout_5.setWidget(3, QFormLayout.LabelRole, self.age15LAbel_5)

        self.age15LineEdit_5 = QLineEdit(self.Population_Box)
        self.age15LineEdit_5.setObjectName(u"age15LineEdit_5")
        self.age15LineEdit_5.setStyleSheet(u"background-color: white")

        self.Age_Layout_5.setWidget(3, QFormLayout.FieldRole, self.age15LineEdit_5)

        self.age25Lbael_5 = QLabel(self.Population_Box)
        self.age25Lbael_5.setObjectName(u"age25Lbael_5")

        self.Age_Layout_5.setWidget(4, QFormLayout.LabelRole, self.age25Lbael_5)

        self.age25LineEdit_5 = QLineEdit(self.Population_Box)
        self.age25LineEdit_5.setObjectName(u"age25LineEdit_5")
        self.age25LineEdit_5.setStyleSheet(u"background-color: white")

        self.Age_Layout_5.setWidget(4, QFormLayout.FieldRole, self.age25LineEdit_5)

        self.age65Label_5 = QLabel(self.Population_Box)
        self.age65Label_5.setObjectName(u"age65Label_5")

        self.Age_Layout_5.setWidget(5, QFormLayout.LabelRole, self.age65Label_5)

        self.age65LineEdit_5 = QLineEdit(self.Population_Box)
        self.age65LineEdit_5.setObjectName(u"age65LineEdit_5")
        self.age65LineEdit_5.setStyleSheet(u"background-color: white")

        self.Age_Layout_5.setWidget(5, QFormLayout.FieldRole, self.age65LineEdit_5)

        self.Gender_Label_5 = QLabel(self.Population_Box)
        self.Gender_Label_5.setObjectName(u"Gender_Label_5")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.Gender_Label_5.sizePolicy().hasHeightForWidth())
        self.Gender_Label_5.setSizePolicy(sizePolicy9)
        self.Gender_Label_5.setMaximumSize(QSize(16777215, 15))
        self.Gender_Label_5.setStyleSheet(u"background-color: ")
        self.Gender_Label_5.setTextFormat(Qt.RichText)
        self.Gender_Label_5.setScaledContents(False)

        self.Age_Layout_5.setWidget(1, QFormLayout.LabelRole, self.Gender_Label_5)

        self.Age_Label_5 = QLabel(self.Population_Box)
        self.Age_Label_5.setObjectName(u"Age_Label_5")
        sizePolicy9.setHeightForWidth(self.Age_Label_5.sizePolicy().hasHeightForWidth())
        self.Age_Label_5.setSizePolicy(sizePolicy9)
        self.Age_Label_5.setMaximumSize(QSize(16777215, 15))
        self.Age_Label_5.setTextFormat(Qt.RichText)

        self.Age_Layout_5.setWidget(6, QFormLayout.LabelRole, self.Age_Label_5)

        self.inhabitantsLabel_4 = QLabel(self.Population_Box)
        self.inhabitantsLabel_4.setObjectName(u"inhabitantsLabel_4")

        self.Age_Layout_5.setWidget(0, QFormLayout.LabelRole, self.inhabitantsLabel_4)

        self.inhabitantsLineEdit_4 = QLineEdit(self.Population_Box)
        self.inhabitantsLineEdit_4.setObjectName(u"inhabitantsLineEdit_4")
        self.inhabitantsLineEdit_4.setStyleSheet(u"background-color: white")

        self.Age_Layout_5.setWidget(0, QFormLayout.FieldRole, self.inhabitantsLineEdit_4)

        self.maleLabel_7 = QLabel(self.Population_Box)
        self.maleLabel_7.setObjectName(u"maleLabel_7")

        self.Age_Layout_5.setWidget(7, QFormLayout.LabelRole, self.maleLabel_7)

        self.maleLineEdit_7 = QLineEdit(self.Population_Box)
        self.maleLineEdit_7.setObjectName(u"maleLineEdit_7")
        self.maleLineEdit_7.setStyleSheet(u"background-color: white")

        self.Age_Layout_5.setWidget(7, QFormLayout.FieldRole, self.maleLineEdit_7)

        self.femaleLabel_13 = QLabel(self.Population_Box)
        self.femaleLabel_13.setObjectName(u"femaleLabel_13")

        self.Age_Layout_5.setWidget(8, QFormLayout.LabelRole, self.femaleLabel_13)

        self.femaleLabel_14 = QLineEdit(self.Population_Box)
        self.femaleLabel_14.setObjectName(u"femaleLabel_14")
        self.femaleLabel_14.setStyleSheet(u"background-color: white")

        self.Age_Layout_5.setWidget(8, QFormLayout.FieldRole, self.femaleLabel_14)


        self.verticalLayout_13.addLayout(self.Age_Layout_5)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_13)

        self.UP_ToolBox.addItem(self.Population_Box, u"POPULATION")
        self.Climate_Box = QWidget()
        self.Climate_Box.setObjectName(u"Climate_Box")
        self.Climate_Box.setGeometry(QRect(0, 0, 359, 154))
        self.verticalLayout_14 = QVBoxLayout(self.Climate_Box)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.Koppen_Form = QFormLayout()
        self.Koppen_Form.setObjectName(u"Koppen_Form")
        self.Koppen_Form.setHorizontalSpacing(5)
        self.Koppen_Form.setVerticalSpacing(5)
        self.KoppenLabel = QLabel(self.Climate_Box)
        self.KoppenLabel.setObjectName(u"KoppenLabel")

        self.Koppen_Form.setWidget(0, QFormLayout.LabelRole, self.KoppenLabel)

        self.KoppenLineEdit = QLineEdit(self.Climate_Box)
        self.KoppenLineEdit.setObjectName(u"KoppenLineEdit")
        sizePolicy10 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.KoppenLineEdit.sizePolicy().hasHeightForWidth())
        self.KoppenLineEdit.setSizePolicy(sizePolicy10)
        self.KoppenLineEdit.setStyleSheet(u"background-color: white")

        self.Koppen_Form.setWidget(0, QFormLayout.FieldRole, self.KoppenLineEdit)


        self.verticalLayout_14.addLayout(self.Koppen_Form)

        self.Weather_Layout = QGridLayout()
        self.Weather_Layout.setObjectName(u"Weather_Layout")
        self.Weather_Layout.setHorizontalSpacing(5)
        self.Weather_Layout.setVerticalSpacing(0)
        self.Rainfall_Layout_3 = QFormLayout()
        self.Rainfall_Layout_3.setObjectName(u"Rainfall_Layout_3")
        self.Rainfall_Layout_3.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.Rainfall_Layout_3.setRowWrapPolicy(QFormLayout.DontWrapRows)
        self.Rainfall_Layout_3.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Rainfall_Layout_3.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Rainfall_Layout_3.setHorizontalSpacing(5)
        self.Rainfall_Layout_3.setVerticalSpacing(5)
        self.Rainfall_Layout_3.setContentsMargins(0, -1, 0, -1)
        self.Rainfall_Label_3 = QLabel(self.Climate_Box)
        self.Rainfall_Label_3.setObjectName(u"Rainfall_Label_3")
        sizePolicy9.setHeightForWidth(self.Rainfall_Label_3.sizePolicy().hasHeightForWidth())
        self.Rainfall_Label_3.setSizePolicy(sizePolicy9)
        self.Rainfall_Label_3.setMaximumSize(QSize(16777215, 15))
        self.Rainfall_Label_3.setStyleSheet(u"background-color: ")
        self.Rainfall_Label_3.setLineWidth(5)
        self.Rainfall_Label_3.setTextFormat(Qt.RichText)
        self.Rainfall_Label_3.setScaledContents(False)

        self.Rainfall_Layout_3.setWidget(0, QFormLayout.LabelRole, self.Rainfall_Label_3)

        self.RmaxMonthlyMeanLabel_3 = QLabel(self.Climate_Box)
        self.RmaxMonthlyMeanLabel_3.setObjectName(u"RmaxMonthlyMeanLabel_3")
        sizePolicy11 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.RmaxMonthlyMeanLabel_3.sizePolicy().hasHeightForWidth())
        self.RmaxMonthlyMeanLabel_3.setSizePolicy(sizePolicy11)

        self.Rainfall_Layout_3.setWidget(1, QFormLayout.LabelRole, self.RmaxMonthlyMeanLabel_3)

        self.RmaxMonthlyMeanLineEdit_3 = QLineEdit(self.Climate_Box)
        self.RmaxMonthlyMeanLineEdit_3.setObjectName(u"RmaxMonthlyMeanLineEdit_3")
        sizePolicy.setHeightForWidth(self.RmaxMonthlyMeanLineEdit_3.sizePolicy().hasHeightForWidth())
        self.RmaxMonthlyMeanLineEdit_3.setSizePolicy(sizePolicy)
        self.RmaxMonthlyMeanLineEdit_3.setMinimumSize(QSize(0, 0))
        self.RmaxMonthlyMeanLineEdit_3.setStyleSheet(u"background-color: white;")

        self.Rainfall_Layout_3.setWidget(1, QFormLayout.FieldRole, self.RmaxMonthlyMeanLineEdit_3)

        self.RannualMeanLabel_3 = QLabel(self.Climate_Box)
        self.RannualMeanLabel_3.setObjectName(u"RannualMeanLabel_3")
        sizePolicy11.setHeightForWidth(self.RannualMeanLabel_3.sizePolicy().hasHeightForWidth())
        self.RannualMeanLabel_3.setSizePolicy(sizePolicy11)

        self.Rainfall_Layout_3.setWidget(2, QFormLayout.LabelRole, self.RannualMeanLabel_3)

        self.RannualMeanLineEdit_3 = QLineEdit(self.Climate_Box)
        self.RannualMeanLineEdit_3.setObjectName(u"RannualMeanLineEdit_3")
        sizePolicy.setHeightForWidth(self.RannualMeanLineEdit_3.sizePolicy().hasHeightForWidth())
        self.RannualMeanLineEdit_3.setSizePolicy(sizePolicy)
        self.RannualMeanLineEdit_3.setStyleSheet(u"background-color: white;")

        self.Rainfall_Layout_3.setWidget(2, QFormLayout.FieldRole, self.RannualMeanLineEdit_3)

        self.RminMonthlyMeanLabel_3 = QLabel(self.Climate_Box)
        self.RminMonthlyMeanLabel_3.setObjectName(u"RminMonthlyMeanLabel_3")
        sizePolicy11.setHeightForWidth(self.RminMonthlyMeanLabel_3.sizePolicy().hasHeightForWidth())
        self.RminMonthlyMeanLabel_3.setSizePolicy(sizePolicy11)

        self.Rainfall_Layout_3.setWidget(3, QFormLayout.LabelRole, self.RminMonthlyMeanLabel_3)

        self.RminMonthlyMeanLineEdit_3 = QLineEdit(self.Climate_Box)
        self.RminMonthlyMeanLineEdit_3.setObjectName(u"RminMonthlyMeanLineEdit_3")
        sizePolicy.setHeightForWidth(self.RminMonthlyMeanLineEdit_3.sizePolicy().hasHeightForWidth())
        self.RminMonthlyMeanLineEdit_3.setSizePolicy(sizePolicy)

        self.Rainfall_Layout_3.setWidget(3, QFormLayout.FieldRole, self.RminMonthlyMeanLineEdit_3)


        self.Weather_Layout.addLayout(self.Rainfall_Layout_3, 0, 1, 1, 1)

        self.Temperature_Layout_5 = QFormLayout()
        self.Temperature_Layout_5.setObjectName(u"Temperature_Layout_5")
        self.Temperature_Layout_5.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Temperature_Layout_5.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Temperature_Layout_5.setHorizontalSpacing(5)
        self.Temperature_Layout_5.setVerticalSpacing(5)
        self.Temperature_Layout_5.setContentsMargins(0, -1, -1, -1)
        self.Temperature_Label_5 = QLabel(self.Climate_Box)
        self.Temperature_Label_5.setObjectName(u"Temperature_Label_5")
        sizePolicy9.setHeightForWidth(self.Temperature_Label_5.sizePolicy().hasHeightForWidth())
        self.Temperature_Label_5.setSizePolicy(sizePolicy9)
        self.Temperature_Label_5.setMaximumSize(QSize(16777215, 15))
        self.Temperature_Label_5.setTextFormat(Qt.RichText)

        self.Temperature_Layout_5.setWidget(0, QFormLayout.LabelRole, self.Temperature_Label_5)

        self.TmaxMonthlyMeanLabel_4 = QLabel(self.Climate_Box)
        self.TmaxMonthlyMeanLabel_4.setObjectName(u"TmaxMonthlyMeanLabel_4")
        sizePolicy11.setHeightForWidth(self.TmaxMonthlyMeanLabel_4.sizePolicy().hasHeightForWidth())
        self.TmaxMonthlyMeanLabel_4.setSizePolicy(sizePolicy11)

        self.Temperature_Layout_5.setWidget(1, QFormLayout.LabelRole, self.TmaxMonthlyMeanLabel_4)

        self.TmaxMonthlyMeanLineEdit_4 = QLineEdit(self.Climate_Box)
        self.TmaxMonthlyMeanLineEdit_4.setObjectName(u"TmaxMonthlyMeanLineEdit_4")
        sizePolicy.setHeightForWidth(self.TmaxMonthlyMeanLineEdit_4.sizePolicy().hasHeightForWidth())
        self.TmaxMonthlyMeanLineEdit_4.setSizePolicy(sizePolicy)
        self.TmaxMonthlyMeanLineEdit_4.setMinimumSize(QSize(24, 0))
        self.TmaxMonthlyMeanLineEdit_4.setStyleSheet(u"background-color: white")

        self.Temperature_Layout_5.setWidget(1, QFormLayout.FieldRole, self.TmaxMonthlyMeanLineEdit_4)

        self.TannualMeanLabel_4 = QLabel(self.Climate_Box)
        self.TannualMeanLabel_4.setObjectName(u"TannualMeanLabel_4")

        self.Temperature_Layout_5.setWidget(2, QFormLayout.LabelRole, self.TannualMeanLabel_4)

        self.TannualMeanEditLabel_4 = QLineEdit(self.Climate_Box)
        self.TannualMeanEditLabel_4.setObjectName(u"TannualMeanEditLabel_4")
        sizePolicy.setHeightForWidth(self.TannualMeanEditLabel_4.sizePolicy().hasHeightForWidth())
        self.TannualMeanEditLabel_4.setSizePolicy(sizePolicy)
        self.TannualMeanEditLabel_4.setStyleSheet(u"background-color: white")

        self.Temperature_Layout_5.setWidget(2, QFormLayout.FieldRole, self.TannualMeanEditLabel_4)

        self.TminMonthlyMeanLabel_4 = QLabel(self.Climate_Box)
        self.TminMonthlyMeanLabel_4.setObjectName(u"TminMonthlyMeanLabel_4")
        sizePolicy11.setHeightForWidth(self.TminMonthlyMeanLabel_4.sizePolicy().hasHeightForWidth())
        self.TminMonthlyMeanLabel_4.setSizePolicy(sizePolicy11)

        self.Temperature_Layout_5.setWidget(3, QFormLayout.LabelRole, self.TminMonthlyMeanLabel_4)

        self.TminMonthlyMeanLineEdit_4 = QLineEdit(self.Climate_Box)
        self.TminMonthlyMeanLineEdit_4.setObjectName(u"TminMonthlyMeanLineEdit_4")
        sizePolicy.setHeightForWidth(self.TminMonthlyMeanLineEdit_4.sizePolicy().hasHeightForWidth())
        self.TminMonthlyMeanLineEdit_4.setSizePolicy(sizePolicy)
        self.TminMonthlyMeanLineEdit_4.setStyleSheet(u"background-color: white")

        self.Temperature_Layout_5.setWidget(3, QFormLayout.FieldRole, self.TminMonthlyMeanLineEdit_4)


        self.Weather_Layout.addLayout(self.Temperature_Layout_5, 0, 0, 1, 1)


        self.verticalLayout_14.addLayout(self.Weather_Layout)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_14)

        self.UP_ToolBox.addItem(self.Climate_Box, u"CLIMATE AND WEATHER")
        self.Built_Box = QWidget()
        self.Built_Box.setObjectName(u"Built_Box")
        self.Built_Box.setGeometry(QRect(0, 0, 274, 176))
        self.verticalLayout_15 = QVBoxLayout(self.Built_Box)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.Built_Form = QFormLayout()
        self.Built_Form.setObjectName(u"Built_Form")
        self.imperviousAreaLabel_2 = QLabel(self.Built_Box)
        self.imperviousAreaLabel_2.setObjectName(u"imperviousAreaLabel_2")

        self.Built_Form.setWidget(0, QFormLayout.LabelRole, self.imperviousAreaLabel_2)

        self.imperviousAreaLineEdit_2 = QLineEdit(self.Built_Box)
        self.imperviousAreaLineEdit_2.setObjectName(u"imperviousAreaLineEdit_2")
        self.imperviousAreaLineEdit_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.Built_Form.setWidget(0, QFormLayout.FieldRole, self.imperviousAreaLineEdit_2)


        self.verticalLayout_15.addLayout(self.Built_Form)

        self.Infras_Label = QLabel(self.Built_Box)
        self.Infras_Label.setObjectName(u"Infras_Label")
        sizePolicy8.setHeightForWidth(self.Infras_Label.sizePolicy().hasHeightForWidth())
        self.Infras_Label.setSizePolicy(sizePolicy8)
        self.Infras_Label.setMaximumSize(QSize(16777215, 15))
        self.Infras_Label.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);\n"
"Qlabel{font-size: 5 px}")
        self.Infras_Label.setTextFormat(Qt.RichText)
        self.Infras_Label.setMargin(0)

        self.verticalLayout_15.addWidget(self.Infras_Label)

        self.Infras_Table = QTableWidget(self.Built_Box)
        if (self.Infras_Table.columnCount() < 2):
            self.Infras_Table.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.Infras_Table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.Infras_Table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.Infras_Table.setObjectName(u"Infras_Table")
        sizePolicy12 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.Infras_Table.sizePolicy().hasHeightForWidth())
        self.Infras_Table.setSizePolicy(sizePolicy12)
        self.Infras_Table.setStyleSheet(u"background-color: white")
        self.Infras_Table.setAutoScrollMargin(10)
        self.Infras_Table.setAlternatingRowColors(False)
        self.Infras_Table.setShowGrid(True)
        self.Infras_Table.setRowCount(0)
        self.Infras_Table.setColumnCount(2)
        self.Infras_Table.horizontalHeader().setCascadingSectionResizes(False)
        self.Infras_Table.horizontalHeader().setMinimumSectionSize(25)
        self.Infras_Table.horizontalHeader().setDefaultSectionSize(90)
        self.Infras_Table.horizontalHeader().setHighlightSections(True)
        self.Infras_Table.horizontalHeader().setProperty("showSortIndicator", False)
        self.Infras_Table.horizontalHeader().setStretchLastSection(False)
        self.Infras_Table.verticalHeader().setCascadingSectionResizes(False)
        self.Infras_Table.verticalHeader().setMinimumSectionSize(20)
        self.Infras_Table.verticalHeader().setProperty("showSortIndicator", False)
        self.Infras_Table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_15.addWidget(self.Infras_Table)

        self.pushButton_3 = QPushButton(self.Built_Box)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"background-color: white")

        self.verticalLayout_15.addWidget(self.pushButton_3)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_15.addItem(self.verticalSpacer_15)

        self.UP_ToolBox.addItem(self.Built_Box, u"BUILT ENVIRONMENT")

        self.gridLayout_6.addWidget(self.UP_ToolBox, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.UP_Back_Widget, 0, 1, 1, 1)

        self.BodyWidget.addWidget(self.Page1_UProfile)
        self.Page2_SWProfile = QWidget()
        self.Page2_SWProfile.setObjectName(u"Page2_SWProfile")
        self.Page2_SWProfile.setStyleSheet(u"background-color: #e7fcfe;")
        self.gridLayout_9 = QGridLayout(self.Page2_SWProfile)
        self.gridLayout_9.setSpacing(5)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.SWP_Back_Widget = QGridLayout()
        self.SWP_Back_Widget.setSpacing(0)
        self.SWP_Back_Widget.setObjectName(u"SWP_Back_Widget")
        self.SWP_Back_Widget.setContentsMargins(10, 10, 10, 10)
        self.SW_ToolBox = QToolBox(self.Page2_SWProfile)
        self.SW_ToolBox.setObjectName(u"SW_ToolBox")
        self.SW_ToolBox.setStyleSheet(u"QToolBox::tab {\n"
"	background-color: rgb(255, 255, 255);\n"
"	border-radius: 12px;	\n"
"	border: 2px solid black;\n"
"	}\n"
"\n"
"QToolBox::tab::selected {\n"
"    background-color: rgb(113, 199, 236);\n"
"	font: 700 9pt \"Segoe UI\";\n"
"}\n"
"")
        self.Service_Box = QWidget()
        self.Service_Box.setObjectName(u"Service_Box")
        self.Service_Box.setGeometry(QRect(0, 0, 209, 209))
        self.verticalLayout = QVBoxLayout(self.Service_Box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Service_Form = QFormLayout()
        self.Service_Form.setObjectName(u"Service_Form")
        self.Service_Form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.Service_Form.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Service_Form.setFormAlignment(Qt.AlignCenter)
        self.Service_Form.setHorizontalSpacing(6)
        self.Service_Form.setVerticalSpacing(2)
        self.Service_Form.setContentsMargins(0, -1, -1, -1)
        self.TotalLine_8 = QLabel(self.Service_Box)
        self.TotalLine_8.setObjectName(u"TotalLine_8")

        self.Service_Form.setWidget(4, QFormLayout.LabelRole, self.TotalLine_8)

        self.TotalLineEdit_8 = QLineEdit(self.Service_Box)
        self.TotalLineEdit_8.setObjectName(u"TotalLineEdit_8")
        self.TotalLineEdit_8.setStyleSheet(u"background-color: white")

        self.Service_Form.setWidget(4, QFormLayout.FieldRole, self.TotalLineEdit_8)

        self.ExecLine_8 = QLabel(self.Service_Box)
        self.ExecLine_8.setObjectName(u"ExecLine_8")

        self.Service_Form.setWidget(5, QFormLayout.LabelRole, self.ExecLine_8)

        self.ManageLine_8 = QLabel(self.Service_Box)
        self.ManageLine_8.setObjectName(u"ManageLine_8")

        self.Service_Form.setWidget(6, QFormLayout.LabelRole, self.ManageLine_8)

        self.ManageLineEdit_8 = QLineEdit(self.Service_Box)
        self.ManageLineEdit_8.setObjectName(u"ManageLineEdit_8")
        self.ManageLineEdit_8.setStyleSheet(u"background-color: white")

        self.Service_Form.setWidget(6, QFormLayout.FieldRole, self.ManageLineEdit_8)

        self.OperationalLine_8 = QLabel(self.Service_Box)
        self.OperationalLine_8.setObjectName(u"OperationalLine_8")

        self.Service_Form.setWidget(7, QFormLayout.LabelRole, self.OperationalLine_8)

        self.OperationalLineEdit_8 = QLineEdit(self.Service_Box)
        self.OperationalLineEdit_8.setObjectName(u"OperationalLineEdit_8")
        self.OperationalLineEdit_8.setStyleSheet(u"background-color: white")

        self.Service_Form.setWidget(7, QFormLayout.FieldRole, self.OperationalLineEdit_8)

        self.ExexLineEdit_8 = QLineEdit(self.Service_Box)
        self.ExexLineEdit_8.setObjectName(u"ExexLineEdit_8")
        self.ExexLineEdit_8.setStyleSheet(u"background-color: white")

        self.Service_Form.setWidget(5, QFormLayout.FieldRole, self.ExexLineEdit_8)

        self.Human_Label_7 = QLabel(self.Service_Box)
        self.Human_Label_7.setObjectName(u"Human_Label_7")
        sizePolicy8.setHeightForWidth(self.Human_Label_7.sizePolicy().hasHeightForWidth())
        self.Human_Label_7.setSizePolicy(sizePolicy8)
        self.Human_Label_7.setMaximumSize(QSize(16777215, 15))
        self.Human_Label_7.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")
        self.Human_Label_7.setTextFormat(Qt.RichText)
        self.Human_Label_7.setMargin(0)

        self.Service_Form.setWidget(3, QFormLayout.LabelRole, self.Human_Label_7)

        self.swCoverageLabel_8 = QLabel(self.Service_Box)
        self.swCoverageLabel_8.setObjectName(u"swCoverageLabel_8")
        self.swCoverageLabel_8.setAcceptDrops(False)
        self.swCoverageLabel_8.setTextFormat(Qt.RichText)

        self.Service_Form.setWidget(2, QFormLayout.LabelRole, self.swCoverageLabel_8)

        self.swCoverageLineEdit_8 = QLineEdit(self.Service_Box)
        self.swCoverageLineEdit_8.setObjectName(u"swCoverageLineEdit_8")
        self.swCoverageLineEdit_8.setStyleSheet(u"background-color: white")

        self.Service_Form.setWidget(2, QFormLayout.FieldRole, self.swCoverageLineEdit_8)

        self.utilityTypeLabel_8 = QLabel(self.Service_Box)
        self.utilityTypeLabel_8.setObjectName(u"utilityTypeLabel_8")

        self.Service_Form.setWidget(1, QFormLayout.LabelRole, self.utilityTypeLabel_8)

        self.utilityTypeLineEdit_8 = QLineEdit(self.Service_Box)
        self.utilityTypeLineEdit_8.setObjectName(u"utilityTypeLineEdit_8")
        self.utilityTypeLineEdit_8.setStyleSheet(u"background-color: white")

        self.Service_Form.setWidget(1, QFormLayout.FieldRole, self.utilityTypeLineEdit_8)

        self.utilityNameLabel_8 = QLabel(self.Service_Box)
        self.utilityNameLabel_8.setObjectName(u"utilityNameLabel_8")

        self.Service_Form.setWidget(0, QFormLayout.LabelRole, self.utilityNameLabel_8)

        self.utilityNameLineEdit_8 = QLineEdit(self.Service_Box)
        self.utilityNameLineEdit_8.setObjectName(u"utilityNameLineEdit_8")
        self.utilityNameLineEdit_8.setStyleSheet(u"background-color: white")

        self.Service_Form.setWidget(0, QFormLayout.FieldRole, self.utilityNameLineEdit_8)


        self.verticalLayout.addLayout(self.Service_Form)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_11)

        self.SW_ToolBox.addItem(self.Service_Box, u"SERVICE MANAGEMENT")
        self.Minor_Box = QWidget()
        self.Minor_Box.setObjectName(u"Minor_Box")
        self.Minor_Box.setGeometry(QRect(0, 0, 274, 305))
        self.verticalLayout_4 = QVBoxLayout(self.Minor_Box)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.Minor_Form = QFormLayout()
        self.Minor_Form.setObjectName(u"Minor_Form")
        self.Minor_Form.setFormAlignment(Qt.AlignCenter)
        self.Minor_Form.setVerticalSpacing(2)
        self.Minor_Form.setContentsMargins(0, -1, -1, -1)
        self.separativeLengthKmLabel_7 = QLabel(self.Minor_Box)
        self.separativeLengthKmLabel_7.setObjectName(u"separativeLengthKmLabel_7")

        self.Minor_Form.setWidget(2, QFormLayout.LabelRole, self.separativeLengthKmLabel_7)

        self.separativeLengthKmLineEdit_7 = QLineEdit(self.Minor_Box)
        self.separativeLengthKmLineEdit_7.setObjectName(u"separativeLengthKmLineEdit_7")
        self.separativeLengthKmLineEdit_7.setStyleSheet(u"background-color: white")

        self.Minor_Form.setWidget(2, QFormLayout.FieldRole, self.separativeLengthKmLineEdit_7)

        self.combinedLengthKmLabel_7 = QLabel(self.Minor_Box)
        self.combinedLengthKmLabel_7.setObjectName(u"combinedLengthKmLabel_7")

        self.Minor_Form.setWidget(3, QFormLayout.LabelRole, self.combinedLengthKmLabel_7)

        self.combinedLengthKmLineEdit_7 = QLineEdit(self.Minor_Box)
        self.combinedLengthKmLineEdit_7.setObjectName(u"combinedLengthKmLineEdit_7")
        self.combinedLengthKmLineEdit_7.setStyleSheet(u"background-color: white")

        self.Minor_Form.setWidget(3, QFormLayout.FieldRole, self.combinedLengthKmLineEdit_7)

        self.averageDiameterMmLabel_7 = QLabel(self.Minor_Box)
        self.averageDiameterMmLabel_7.setObjectName(u"averageDiameterMmLabel_7")

        self.Minor_Form.setWidget(4, QFormLayout.LabelRole, self.averageDiameterMmLabel_7)

        self.averageDiameterMmLineEdit_7 = QLineEdit(self.Minor_Box)
        self.averageDiameterMmLineEdit_7.setObjectName(u"averageDiameterMmLineEdit_7")
        self.averageDiameterMmLineEdit_7.setStyleSheet(u"background-color: white")

        self.Minor_Form.setWidget(4, QFormLayout.FieldRole, self.averageDiameterMmLineEdit_7)

        self.averageAgeYearsLabel_7 = QLabel(self.Minor_Box)
        self.averageAgeYearsLabel_7.setObjectName(u"averageAgeYearsLabel_7")

        self.Minor_Form.setWidget(5, QFormLayout.LabelRole, self.averageAgeYearsLabel_7)

        self.averageAgeYearsLineEdit_7 = QLineEdit(self.Minor_Box)
        self.averageAgeYearsLineEdit_7.setObjectName(u"averageAgeYearsLineEdit_7")
        self.averageAgeYearsLineEdit_7.setStyleSheet(u"background-color: white")

        self.Minor_Form.setWidget(5, QFormLayout.FieldRole, self.averageAgeYearsLineEdit_7)

        self.numberOfOutfallsLabel_7 = QLabel(self.Minor_Box)
        self.numberOfOutfallsLabel_7.setObjectName(u"numberOfOutfallsLabel_7")

        self.Minor_Form.setWidget(6, QFormLayout.LabelRole, self.numberOfOutfallsLabel_7)

        self.numberOfOutfallsLineEdit_7 = QLineEdit(self.Minor_Box)
        self.numberOfOutfallsLineEdit_7.setObjectName(u"numberOfOutfallsLineEdit_7")
        self.numberOfOutfallsLineEdit_7.setStyleSheet(u"background-color: white")

        self.Minor_Form.setWidget(6, QFormLayout.FieldRole, self.numberOfOutfallsLineEdit_7)

        self.Age_Label_14 = QLabel(self.Minor_Box)
        self.Age_Label_14.setObjectName(u"Age_Label_14")
        sizePolicy9.setHeightForWidth(self.Age_Label_14.sizePolicy().hasHeightForWidth())
        self.Age_Label_14.setSizePolicy(sizePolicy9)
        self.Age_Label_14.setMaximumSize(QSize(16777215, 15))
        self.Age_Label_14.setTextFormat(Qt.RichText)

        self.Minor_Form.setWidget(1, QFormLayout.LabelRole, self.Age_Label_14)

        self.conveyanceTypeLabel_7 = QLabel(self.Minor_Box)
        self.conveyanceTypeLabel_7.setObjectName(u"conveyanceTypeLabel_7")

        self.Minor_Form.setWidget(0, QFormLayout.LabelRole, self.conveyanceTypeLabel_7)

        self.conveyanceTypeComboBox_7 = QComboBox(self.Minor_Box)
        self.conveyanceTypeComboBox_7.addItem("")
        self.conveyanceTypeComboBox_7.addItem("")
        self.conveyanceTypeComboBox_7.addItem("")
        self.conveyanceTypeComboBox_7.setObjectName(u"conveyanceTypeComboBox_7")
        self.conveyanceTypeComboBox_7.setStyleSheet(u"background-color: white")
        self.conveyanceTypeComboBox_7.setFrame(True)

        self.Minor_Form.setWidget(0, QFormLayout.FieldRole, self.conveyanceTypeComboBox_7)


        self.verticalLayout_4.addLayout(self.Minor_Form)

        self.SpecEq_Label = QLabel(self.Minor_Box)
        self.SpecEq_Label.setObjectName(u"SpecEq_Label")
        sizePolicy9.setHeightForWidth(self.SpecEq_Label.sizePolicy().hasHeightForWidth())
        self.SpecEq_Label.setSizePolicy(sizePolicy9)
        self.SpecEq_Label.setMaximumSize(QSize(16777215, 15))
        self.SpecEq_Label.setTextFormat(Qt.RichText)

        self.verticalLayout_4.addWidget(self.SpecEq_Label)

        self.Infras_Table_2 = QTableWidget(self.Minor_Box)
        if (self.Infras_Table_2.columnCount() < 2):
            self.Infras_Table_2.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.Infras_Table_2.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.Infras_Table_2.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        self.Infras_Table_2.setObjectName(u"Infras_Table_2")
        sizePolicy12.setHeightForWidth(self.Infras_Table_2.sizePolicy().hasHeightForWidth())
        self.Infras_Table_2.setSizePolicy(sizePolicy12)
        self.Infras_Table_2.setStyleSheet(u"background-color: white")
        self.Infras_Table_2.setAutoScrollMargin(10)
        self.Infras_Table_2.setAlternatingRowColors(False)
        self.Infras_Table_2.setShowGrid(True)
        self.Infras_Table_2.setRowCount(0)
        self.Infras_Table_2.setColumnCount(2)
        self.Infras_Table_2.horizontalHeader().setCascadingSectionResizes(False)
        self.Infras_Table_2.horizontalHeader().setMinimumSectionSize(25)
        self.Infras_Table_2.horizontalHeader().setDefaultSectionSize(90)
        self.Infras_Table_2.horizontalHeader().setHighlightSections(True)
        self.Infras_Table_2.horizontalHeader().setProperty("showSortIndicator", False)
        self.Infras_Table_2.horizontalHeader().setStretchLastSection(False)
        self.Infras_Table_2.verticalHeader().setCascadingSectionResizes(False)
        self.Infras_Table_2.verticalHeader().setMinimumSectionSize(20)
        self.Infras_Table_2.verticalHeader().setProperty("showSortIndicator", False)
        self.Infras_Table_2.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_4.addWidget(self.Infras_Table_2)

        self.Infras_Button = QPushButton(self.Minor_Box)
        self.Infras_Button.setObjectName(u"Infras_Button")
        self.Infras_Button.setStyleSheet(u"background-color: #F5F5F5")

        self.verticalLayout_4.addWidget(self.Infras_Button)

        self.SW_ToolBox.addItem(self.Minor_Box, u"MINOR SYSTEM")
        self.Major_Box = QWidget()
        self.Major_Box.setObjectName(u"Major_Box")
        self.Major_Box.setGeometry(QRect(0, 0, 289, 161))
        self.verticalLayout_6 = QVBoxLayout(self.Major_Box)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.Temperature_Layout_7 = QFormLayout()
        self.Temperature_Layout_7.setObjectName(u"Temperature_Layout_7")
        self.Temperature_Layout_7.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Temperature_Layout_7.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Temperature_Layout_7.setHorizontalSpacing(25)
        self.Temperature_Layout_7.setVerticalSpacing(2)
        self.Temperature_Layout_7.setContentsMargins(0, -1, -1, -1)
        self.curbHeightLanel_5 = QLabel(self.Major_Box)
        self.curbHeightLanel_5.setObjectName(u"curbHeightLanel_5")

        self.Temperature_Layout_7.setWidget(2, QFormLayout.LabelRole, self.curbHeightLanel_5)

        self.curbHeightLineEdit_5 = QLineEdit(self.Major_Box)
        self.curbHeightLineEdit_5.setObjectName(u"curbHeightLineEdit_5")
        self.curbHeightLineEdit_5.setStyleSheet(u"background-color: white;")

        self.Temperature_Layout_7.setWidget(2, QFormLayout.FieldRole, self.curbHeightLineEdit_5)

        self.buildingHeightLabel_5 = QLabel(self.Major_Box)
        self.buildingHeightLabel_5.setObjectName(u"buildingHeightLabel_5")

        self.Temperature_Layout_7.setWidget(3, QFormLayout.LabelRole, self.buildingHeightLabel_5)

        self.buildingHeightLineEdit_5 = QLineEdit(self.Major_Box)
        self.buildingHeightLineEdit_5.setObjectName(u"buildingHeightLineEdit_5")
        self.buildingHeightLineEdit_5.setStyleSheet(u"background-color: white;")

        self.Temperature_Layout_7.setWidget(3, QFormLayout.FieldRole, self.buildingHeightLineEdit_5)

        self.streetWidthLabel_5 = QLabel(self.Major_Box)
        self.streetWidthLabel_5.setObjectName(u"streetWidthLabel_5")

        self.Temperature_Layout_7.setWidget(4, QFormLayout.LabelRole, self.streetWidthLabel_5)

        self.streetWidthLineEdit_5 = QLineEdit(self.Major_Box)
        self.streetWidthLineEdit_5.setObjectName(u"streetWidthLineEdit_5")
        self.streetWidthLineEdit_5.setStyleSheet(u"background-color: white;")

        self.Temperature_Layout_7.setWidget(4, QFormLayout.FieldRole, self.streetWidthLineEdit_5)

        self.streetLongSlopeMMLabel_5 = QLabel(self.Major_Box)
        self.streetLongSlopeMMLabel_5.setObjectName(u"streetLongSlopeMMLabel_5")

        self.Temperature_Layout_7.setWidget(5, QFormLayout.LabelRole, self.streetLongSlopeMMLabel_5)

        self.streetLongSlopeMMLineEdit_5 = QLineEdit(self.Major_Box)
        self.streetLongSlopeMMLineEdit_5.setObjectName(u"streetLongSlopeMMLineEdit_5")

        self.Temperature_Layout_7.setWidget(5, QFormLayout.FieldRole, self.streetLongSlopeMMLineEdit_5)

        self.Temperature_Label_7 = QLabel(self.Major_Box)
        self.Temperature_Label_7.setObjectName(u"Temperature_Label_7")
        sizePolicy9.setHeightForWidth(self.Temperature_Label_7.sizePolicy().hasHeightForWidth())
        self.Temperature_Label_7.setSizePolicy(sizePolicy9)
        self.Temperature_Label_7.setMaximumSize(QSize(16777215, 15))
        self.Temperature_Label_7.setTextFormat(Qt.RichText)

        self.Temperature_Layout_7.setWidget(1, QFormLayout.LabelRole, self.Temperature_Label_7)

        self.lengthAlternativeLabel_5 = QLabel(self.Major_Box)
        self.lengthAlternativeLabel_5.setObjectName(u"lengthAlternativeLabel_5")
        sizePolicy11.setHeightForWidth(self.lengthAlternativeLabel_5.sizePolicy().hasHeightForWidth())
        self.lengthAlternativeLabel_5.setSizePolicy(sizePolicy11)
        self.lengthAlternativeLabel_5.setAcceptDrops(True)

        self.Temperature_Layout_7.setWidget(0, QFormLayout.LabelRole, self.lengthAlternativeLabel_5)

        self.lengthAlternativeLineEdit_5 = QLineEdit(self.Major_Box)
        self.lengthAlternativeLineEdit_5.setObjectName(u"lengthAlternativeLineEdit_5")
        sizePolicy.setHeightForWidth(self.lengthAlternativeLineEdit_5.sizePolicy().hasHeightForWidth())
        self.lengthAlternativeLineEdit_5.setSizePolicy(sizePolicy)
        self.lengthAlternativeLineEdit_5.setMinimumSize(QSize(0, 0))
        self.lengthAlternativeLineEdit_5.setMaximumSize(QSize(16777215, 16777215))
        self.lengthAlternativeLineEdit_5.setAcceptDrops(False)
        self.lengthAlternativeLineEdit_5.setStyleSheet(u"background-color: white")

        self.Temperature_Layout_7.setWidget(0, QFormLayout.FieldRole, self.lengthAlternativeLineEdit_5)


        self.verticalLayout_6.addLayout(self.Temperature_Layout_7)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_12)

        self.SW_ToolBox.addItem(self.Major_Box, u"MAJOR SYSTEM")
        self.NBS_Box = QWidget()
        self.NBS_Box.setObjectName(u"NBS_Box")
        self.NBS_Box.setGeometry(QRect(0, 0, 274, 146))
        self.verticalLayout_7 = QVBoxLayout(self.NBS_Box)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.ExistingNBS_Labael_8 = QLabel(self.NBS_Box)
        self.ExistingNBS_Labael_8.setObjectName(u"ExistingNBS_Labael_8")
        sizePolicy8.setHeightForWidth(self.ExistingNBS_Labael_8.sizePolicy().hasHeightForWidth())
        self.ExistingNBS_Labael_8.setSizePolicy(sizePolicy8)
        self.ExistingNBS_Labael_8.setMaximumSize(QSize(16777215, 15))
        self.ExistingNBS_Labael_8.setStyleSheet(u"background-color: rgba(0, 0, 0, 0)")
        self.ExistingNBS_Labael_8.setTextFormat(Qt.RichText)
        self.ExistingNBS_Labael_8.setMargin(0)

        self.verticalLayout_7.addWidget(self.ExistingNBS_Labael_8)

        self.NBS_TAble_8 = QTableWidget(self.NBS_Box)
        if (self.NBS_TAble_8.columnCount() < 3):
            self.NBS_TAble_8.setColumnCount(3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.NBS_TAble_8.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.NBS_TAble_8.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.NBS_TAble_8.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        self.NBS_TAble_8.setObjectName(u"NBS_TAble_8")
        sizePolicy12.setHeightForWidth(self.NBS_TAble_8.sizePolicy().hasHeightForWidth())
        self.NBS_TAble_8.setSizePolicy(sizePolicy12)
        self.NBS_TAble_8.setStyleSheet(u"background-color: white")
        self.NBS_TAble_8.setAutoScrollMargin(10)
        self.NBS_TAble_8.setAlternatingRowColors(False)
        self.NBS_TAble_8.setShowGrid(True)
        self.NBS_TAble_8.setRowCount(0)
        self.NBS_TAble_8.setColumnCount(3)
        self.NBS_TAble_8.horizontalHeader().setMinimumSectionSize(26)
        self.NBS_TAble_8.horizontalHeader().setDefaultSectionSize(85)
        self.NBS_TAble_8.horizontalHeader().setHighlightSections(True)
        self.NBS_TAble_8.horizontalHeader().setProperty("showSortIndicator", True)
        self.NBS_TAble_8.verticalHeader().setMinimumSectionSize(20)
        self.NBS_TAble_8.verticalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout_7.addWidget(self.NBS_TAble_8)

        self.NBS_Button_8 = QPushButton(self.NBS_Box)
        self.NBS_Button_8.setObjectName(u"NBS_Button_8")
        self.NBS_Button_8.setStyleSheet(u"background-color: #F5F5F5")

        self.verticalLayout_7.addWidget(self.NBS_Button_8)

        self.verticalSpacer_17 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_17)

        self.SW_ToolBox.addItem(self.NBS_Box, u"NATURE BASED SOLUTIONS")

        self.SWP_Back_Widget.addWidget(self.SW_ToolBox, 0, 0, 1, 1)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.SWP_Back_Widget.addItem(self.verticalSpacer_18, 1, 0, 1, 1)


        self.gridLayout_9.addLayout(self.SWP_Back_Widget, 0, 0, 1, 1)

        self.BodyWidget.addWidget(self.Page2_SWProfile)
        self.Page3_Functional = QWidget()
        self.Page3_Functional.setObjectName(u"Page3_Functional")
        self.Page3_Functional.setStyleSheet(u"background-color: rgb(228, 247, 233)")
        self.horizontalLayout_4 = QHBoxLayout(self.Page3_Functional)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.Functional_LeftWidget = QVBoxLayout()
        self.Functional_LeftWidget.setObjectName(u"Functional_LeftWidget")
        self.Functional_list = QTreeWidget(self.Page3_Functional)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.Functional_list.setHeaderItem(__qtreewidgetitem)
        self.Functional_list.setObjectName(u"Functional_list")
        sizePolicy3.setHeightForWidth(self.Functional_list.sizePolicy().hasHeightForWidth())
        self.Functional_list.setSizePolicy(sizePolicy3)
        self.Functional_list.setMinimumSize(QSize(340, 400))
        self.Functional_list.setMaximumSize(QSize(340, 400))
        self.Functional_list.setStyleSheet(u"background-color: rgba(255, 255, 255, 100)")
        self.Functional_list.setFrameShape(QFrame.Box)
        self.Functional_list.setFrameShadow(QFrame.Plain)
        self.Functional_list.setLineWidth(1)
        self.Functional_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.Functional_list.setProperty("showDropIndicator", False)
        self.Functional_list.setIndentation(10)
        self.Functional_list.setItemsExpandable(True)
        self.Functional_list.setHeaderHidden(True)
        self.Functional_list.setColumnCount(1)
        self.Functional_list.header().setVisible(False)

        self.Functional_LeftWidget.addWidget(self.Functional_list)

        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Functional_LeftWidget.addItem(self.verticalSpacer_21)


        self.horizontalLayout_4.addLayout(self.Functional_LeftWidget)

        self.Functional_MainWidget = QStackedWidget(self.Page3_Functional)
        self.Functional_MainWidget.setObjectName(u"Functional_MainWidget")
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
        self.Page4_Performance.setStyleSheet(u"background-color: #FFF3E2;")
        self.horizontalLayout_5 = QHBoxLayout(self.Page4_Performance)
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.Performance_LeftWidget = QVBoxLayout()
        self.Performance_LeftWidget.setSpacing(5)
        self.Performance_LeftWidget.setObjectName(u"Performance_LeftWidget")
        self.Performance_LeftWidget.setContentsMargins(0, 0, 0, 0)
        self.Performance_list = QTreeWidget(self.Page4_Performance)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.Performance_list.setHeaderItem(__qtreewidgetitem1)
        self.Performance_list.setObjectName(u"Performance_list")
        sizePolicy3.setHeightForWidth(self.Performance_list.sizePolicy().hasHeightForWidth())
        self.Performance_list.setSizePolicy(sizePolicy3)
        self.Performance_list.setMinimumSize(QSize(340, 400))
        self.Performance_list.setMaximumSize(QSize(340, 400))
        self.Performance_list.setStyleSheet(u"background-color: rgba(255, 255, 255, 100)")
        self.Performance_list.setFrameShape(QFrame.Panel)
        self.Performance_list.setFrameShadow(QFrame.Plain)
        self.Performance_list.setLineWidth(1)
        self.Performance_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.Performance_list.setProperty("showDropIndicator", False)
        self.Performance_list.setIndentation(10)
        self.Performance_list.setItemsExpandable(True)
        self.Performance_list.setHeaderHidden(True)
        self.Performance_list.setColumnCount(1)
        self.Performance_list.header().setVisible(False)

        self.Performance_LeftWidget.addWidget(self.Performance_list)

        self.verticalSpacer_38 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Performance_LeftWidget.addItem(self.verticalSpacer_38)

        self.ScenarioSU_btn = QPushButton(self.Page4_Performance)
        self.ScenarioSU_btn.setObjectName(u"ScenarioSU_btn")
        sizePolicy3.setHeightForWidth(self.ScenarioSU_btn.sizePolicy().hasHeightForWidth())
        self.ScenarioSU_btn.setSizePolicy(sizePolicy3)
        self.ScenarioSU_btn.setMinimumSize(QSize(170, 30))
        self.ScenarioSU_btn.setMaximumSize(QSize(16777215, 16777215))
        self.ScenarioSU_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: #e7fcfe;\n"
"    border-radius: 15px;\n"
"	font: 700 9pt \"Segoe UI\";\n"
"	border: 1px solid black;\n"
"}\n"
"")
        icon14 = QIcon()
        icon14.addFile(u":/icon/icons/settings-12-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.ScenarioSU_btn.setIcon(icon14)

        self.Performance_LeftWidget.addWidget(self.ScenarioSU_btn, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.HazardSU_btn = QPushButton(self.Page4_Performance)
        self.HazardSU_btn.setObjectName(u"HazardSU_btn")
        sizePolicy3.setHeightForWidth(self.HazardSU_btn.sizePolicy().hasHeightForWidth())
        self.HazardSU_btn.setSizePolicy(sizePolicy3)
        self.HazardSU_btn.setMinimumSize(QSize(170, 30))
        self.HazardSU_btn.setMaximumSize(QSize(16777215, 16777215))
        self.HazardSU_btn.setStyleSheet(u"QPushButton {\n"
"    background-color: #ffb8b8;\n"
"    border-radius: 15px;\n"
"	font: 700 9pt \"Segoe UI\";\n"
"	border: 1px solid black;\n"
"}\n"
"")
        icon15 = QIcon()
        icon15.addFile(u":/icon/icons/alert-64.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.HazardSU_btn.setIcon(icon15)

        self.Performance_LeftWidget.addWidget(self.HazardSU_btn, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_37 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Performance_LeftWidget.addItem(self.verticalSpacer_37)


        self.horizontalLayout_5.addLayout(self.Performance_LeftWidget)

        self.Performance_MainWidget = QStackedWidget(self.Page4_Performance)
        self.Performance_MainWidget.setObjectName(u"Performance_MainWidget")
        self.default_16 = QWidget()
        self.default_16.setObjectName(u"default_16")
        self.Performance_MainWidget.addWidget(self.default_16)
        self.default_17 = QWidget()
        self.default_17.setObjectName(u"default_17")
        self.Performance_MainWidget.addWidget(self.default_17)

        self.horizontalLayout_5.addWidget(self.Performance_MainWidget)

        self.BodyWidget.addWidget(self.Page4_Performance)
        self.Page5_Dashboard = QWidget()
        self.Page5_Dashboard.setObjectName(u"Page5_Dashboard")
        self.gridLayout_3 = QGridLayout(self.Page5_Dashboard)
        self.gridLayout_3.setSpacing(5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.Dashboard_Layout = QGridLayout()
        self.Dashboard_Layout.setSpacing(5)
        self.Dashboard_Layout.setObjectName(u"Dashboard_Layout")
        self.Dashboard_Layout.setSizeConstraint(QLayout.SetFixedSize)
        self.Dashboard_Layout.setContentsMargins(5, -1, 4, -1)
        self.PSS = QVBoxLayout()
        self.PSS.setSpacing(2)
        self.PSS.setObjectName(u"PSS")
        self.label_12 = QLabel(self.Page5_Dashboard)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"padding: 5px")
        self.label_12.setAlignment(Qt.AlignCenter)
        self.label_12.setWordWrap(True)

        self.PSS.addWidget(self.label_12)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.Page5_Dashboard)
        self.label_4.setObjectName(u"label_4")
        sizePolicy11.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy11)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.PSS_ComboBox = QComboBox(self.Page5_Dashboard)
        self.PSS_ComboBox.setObjectName(u"PSS_ComboBox")
        sizePolicy10.setHeightForWidth(self.PSS_ComboBox.sizePolicy().hasHeightForWidth())
        self.PSS_ComboBox.setSizePolicy(sizePolicy10)
        self.PSS_ComboBox.setMinimumSize(QSize(0, 0))
        self.PSS_ComboBox.setMaximumSize(QSize(16777215, 16777215))
        self.PSS_ComboBox.setAutoFillBackground(False)
        self.PSS_ComboBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.PSS_ComboBox.setFrame(True)

        self.horizontalLayout_3.addWidget(self.PSS_ComboBox)

        self.horizontalLayout_3.setStretch(1, 1)

        self.PSS.addLayout(self.horizontalLayout_3)

        self.PSS_ScenarioList = QListView(self.Page5_Dashboard)
        self.PSS_ScenarioList.setObjectName(u"PSS_ScenarioList")
        sizePolicy13 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.PSS_ScenarioList.sizePolicy().hasHeightForWidth())
        self.PSS_ScenarioList.setSizePolicy(sizePolicy13)
        self.PSS_ScenarioList.setMinimumSize(QSize(0, 0))
        self.PSS_ScenarioList.setMaximumSize(QSize(16777215, 16777215))
        self.PSS_ScenarioList.setStyleSheet(u"font: 9pt \"Segoe UI\";")
        self.PSS_ScenarioList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.PSS_ScenarioList.setProperty("showDropIndicator", False)
        self.PSS_ScenarioList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.PSS_ScenarioList.setUniformItemSizes(True)
        self.PSS_ScenarioList.setWordWrap(True)

        self.PSS.addWidget(self.PSS_ScenarioList)

        self.PSS.setStretch(2, 1)

        self.Dashboard_Layout.addLayout(self.PSS, 1, 0, 1, 1)

        self.FRR = QVBoxLayout()
        self.FRR.setSpacing(2)
        self.FRR.setObjectName(u"FRR")
        self.label_11 = QLabel(self.Page5_Dashboard)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"padding: 5px")
        self.label_11.setAlignment(Qt.AlignCenter)
        self.label_11.setWordWrap(True)

        self.FRR.addWidget(self.label_11)

        self.FRR_Widget = QWidget(self.Page5_Dashboard)
        self.FRR_Widget.setObjectName(u"FRR_Widget")

        self.FRR.addWidget(self.FRR_Widget)

        self.FRR.setStretch(1, 1)

        self.Dashboard_Layout.addLayout(self.FRR, 0, 3, 1, 1)

        self.SCR = QVBoxLayout()
        self.SCR.setSpacing(2)
        self.SCR.setObjectName(u"SCR")
        self.label_14 = QLabel(self.Page5_Dashboard)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"padding: 5px")
        self.label_14.setAlignment(Qt.AlignCenter)
        self.label_14.setWordWrap(True)

        self.SCR.addWidget(self.label_14)

        self.SCR_Widget = QWidget(self.Page5_Dashboard)
        self.SCR_Widget.setObjectName(u"SCR_Widget")

        self.SCR.addWidget(self.SCR_Widget)

        self.SCR.setStretch(1, 1)

        self.Dashboard_Layout.addLayout(self.SCR, 1, 2, 1, 1)

        self.FOR = QVBoxLayout()
        self.FOR.setSpacing(2)
        self.FOR.setObjectName(u"FOR")
        self.label_2 = QLabel(self.Page5_Dashboard)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"padding: 5px")
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(True)

        self.FOR.addWidget(self.label_2)

        self.FOR_Widget = QWidget(self.Page5_Dashboard)
        self.FOR_Widget.setObjectName(u"FOR_Widget")

        self.FOR.addWidget(self.FOR_Widget)

        self.FOR.setStretch(1, 1)

        self.Dashboard_Layout.addLayout(self.FOR, 0, 1, 1, 1)

        self.FCR = QVBoxLayout()
        self.FCR.setSpacing(2)
        self.FCR.setObjectName(u"FCR")
        self.label_10 = QLabel(self.Page5_Dashboard)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"padding: 5px")
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_10.setWordWrap(True)

        self.FCR.addWidget(self.label_10)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.Page5_Dashboard)
        self.label_3.setObjectName(u"label_3")
        sizePolicy11.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy11)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.FCR_ComboBox = QComboBox(self.Page5_Dashboard)
        self.FCR_ComboBox.setObjectName(u"FCR_ComboBox")
        sizePolicy10.setHeightForWidth(self.FCR_ComboBox.sizePolicy().hasHeightForWidth())
        self.FCR_ComboBox.setSizePolicy(sizePolicy10)
        self.FCR_ComboBox.setMinimumSize(QSize(0, 0))
        self.FCR_ComboBox.setMaximumSize(QSize(16777215, 16777215))
        self.FCR_ComboBox.setAutoFillBackground(False)
        self.FCR_ComboBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.FCR_ComboBox.setFrame(True)

        self.horizontalLayout_2.addWidget(self.FCR_ComboBox)

        self.horizontalLayout_2.setStretch(1, 1)

        self.FCR.addLayout(self.horizontalLayout_2)

        self.FCR_Widget = QWidget(self.Page5_Dashboard)
        self.FCR_Widget.setObjectName(u"FCR_Widget")

        self.FCR.addWidget(self.FCR_Widget)

        self.FCR.setStretch(2, 1)

        self.Dashboard_Layout.addLayout(self.FCR, 0, 2, 1, 1)

        self.SPR = QVBoxLayout()
        self.SPR.setSpacing(2)
        self.SPR.setObjectName(u"SPR")
        self.label_13 = QLabel(self.Page5_Dashboard)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"padding: 5px")
        self.label_13.setAlignment(Qt.AlignCenter)
        self.label_13.setWordWrap(True)

        self.SPR.addWidget(self.label_13)

        self.SPR_Widget = QWidget(self.Page5_Dashboard)
        self.SPR_Widget.setObjectName(u"SPR_Widget")

        self.SPR.addWidget(self.SPR_Widget)

        self.SPR.setStretch(1, 1)

        self.Dashboard_Layout.addLayout(self.SPR, 1, 1, 1, 1)

        self.PRR = QVBoxLayout()
        self.PRR.setSpacing(2)
        self.PRR.setObjectName(u"PRR")
        self.label_15 = QLabel(self.Page5_Dashboard)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"padding: 5px")
        self.label_15.setAlignment(Qt.AlignCenter)
        self.label_15.setWordWrap(True)

        self.PRR.addWidget(self.label_15)

        self.PRR_Widget = QWidget(self.Page5_Dashboard)
        self.PRR_Widget.setObjectName(u"PRR_Widget")

        self.PRR.addWidget(self.PRR_Widget)

        self.PRR.setStretch(1, 1)

        self.Dashboard_Layout.addLayout(self.PRR, 1, 3, 1, 1)

        self.FDC = QVBoxLayout()
        self.FDC.setSpacing(2)
        self.FDC.setObjectName(u"FDC")
        self.label = QLabel(self.Page5_Dashboard)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"padding: 5px")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.FDC.addWidget(self.label)

        self.FDC_Widget = QWidget(self.Page5_Dashboard)
        self.FDC_Widget.setObjectName(u"FDC_Widget")
        self.FDC_Widget.setLayoutDirection(Qt.LeftToRight)
        self.FDC_Widget.setStyleSheet(u"")

        self.FDC.addWidget(self.FDC_Widget)

        self.FDC.setStretch(1, 1)

        self.Dashboard_Layout.addLayout(self.FDC, 0, 0, 1, 1)

        self.Dashboard_Layout.setRowStretch(0, 1)
        self.Dashboard_Layout.setRowStretch(1, 1)
        self.Dashboard_Layout.setColumnStretch(1, 1)
        self.Dashboard_Layout.setColumnStretch(2, 1)
        self.Dashboard_Layout.setColumnStretch(3, 1)

        self.gridLayout_3.addLayout(self.Dashboard_Layout, 0, 0, 1, 1)

        self.BodyWidget.addWidget(self.Page5_Dashboard)

        self.Org2_Body.addWidget(self.BodyWidget)


        self.verticalLayout_5.addLayout(self.Org2_Body)

        self.Org3_Footer = QVBoxLayout()
        self.Org3_Footer.setSpacing(0)
        self.Org3_Footer.setObjectName(u"Org3_Footer")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.Org3_Footer.addWidget(self.line)

        self.Footer_content = QHBoxLayout()
        self.Footer_content.setObjectName(u"Footer_content")
        self.left_label = QLabel(self.centralwidget)
        self.left_label.setObjectName(u"left_label")
        self.left_label.setOpenExternalLinks(True)

        self.Footer_content.addWidget(self.left_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.Footer_content.addItem(self.horizontalSpacer)

        self.right_label = QLabel(self.centralwidget)
        self.right_label.setObjectName(u"right_label")

        self.Footer_content.addWidget(self.right_label)


        self.Org3_Footer.addLayout(self.Footer_content)


        self.verticalLayout_5.addLayout(self.Org3_Footer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 22))
        self.menuFile_F = QMenu(self.menubar)
        self.menuFile_F.setObjectName(u"menuFile_F")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile_F.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile_F.addAction(self.actionSave_As)
        self.menuFile_F.addAction(self.actionSave)
        self.menuFile_F.addAction(self.actionLoad)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionManual)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)
        self.menu_btn.clicked.connect(self.menu_btn_2.toggle)
        self.menu_btn_2.clicked.connect(self.menu_btn.toggle)
        self.home_btn.clicked.connect(self.home_btn_2.toggle)
        self.home_btn_2.clicked.connect(self.home_btn.toggle)
        self.urbanprofile_btn.clicked.connect(self.urbanprofile_btn_2.toggle)
        self.urbanprofile_btn_2.clicked.connect(self.urbanprofile_btn.toggle)
        self.stormprofile_btn.clicked.connect(self.stormprofile_btn_2.toggle)
        self.stormprofile_btn_2.clicked.connect(self.stormprofile_btn.toggle)
        self.functional_btn.clicked.connect(self.functional_btn_2.toggle)
        self.functional_btn_2.clicked.connect(self.functional_btn.toggle)
        self.performance_btn.clicked.connect(self.performance_btn_2.toggle)
        self.performance_btn_2.clicked.connect(self.performance_btn.toggle)
        self.dashboard_btn.clicked.connect(self.dashboard_btn_2.toggle)
        self.dashboard_btn_2.clicked.connect(self.dashboard_btn.toggle)
        self.menu_btn_2.clicked.connect(self.LeftMenuWidget_2.hide)
        self.menu_btn_2.clicked["bool"].connect(self.MenuWidget_2.hide)
        self.menu_btn.clicked.connect(self.LeftMenuWidget_2.show)
        self.menu_btn.clicked.connect(self.MenuWidget_2.show)
        self.menu_btn.clicked.connect(self.LeftMenuWidget.hide)
        self.menu_btn.clicked.connect(self.MenuWidget.hide)
        self.menu_btn_2.clicked.connect(self.LeftMenuWidget.show)
        self.menu_btn_2.clicked.connect(self.MenuWidget.show)

        self.menu_btn_2.setDefault(False)
        self.TitlesWidget.setCurrentIndex(5)
        self.home_btn_2.setDefault(False)
        self.BodyWidget.setCurrentIndex(5)
        self.UP_ToolBox.setCurrentIndex(0)
        self.UP_ToolBox.layout().setSpacing(10)
        self.SW_ToolBox.setCurrentIndex(2)
        self.SW_ToolBox.layout().setSpacing(10)
        self.Functional_MainWidget.setCurrentIndex(1)
        self.Performance_MainWidget.setCurrentIndex(0)


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
        self.REFUSS2_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">RESILIENCE FRAMEWORK FOR URBAN STORMWATER SERVICES</span></p></body></html>", None))
        self.REFUSS_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700;\">REFUSS</span></p></body></html>", None))
        self.menu_btn.setText("")
        self.menu_btn_2.setText(QCoreApplication.translate("MainWindow", u"MENU", None))
        self.H_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">- HOME -</span></p></body></html>", None))
        self.UP_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">- URBAN PROFILE -</span></p></body></html>", None))
        self.UP_Label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">- STORMWATER PROFILE -</span></p></body></html>", None))
        self.FD_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">- FUNCTIONAL DIMENSION -</span></p></body></html>", None))
        self.PD_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">- PERFORMANCE DIMENSION -</span></p></body></html>", None))
        self.PD_Label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">- RESILIENCE DASHBOARD -</span></p></body></html>", None))
        self.home_btn.setText("")
        self.urbanprofile_btn.setText("")
        self.stormprofile_btn.setText("")
        self.functional_btn.setText("")
        self.performance_btn.setText("")
        self.dashboard_btn.setText("")
        self.home_btn_2.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        self.urbanprofile_btn_2.setText(QCoreApplication.translate("MainWindow", u"URBAN PROFILE", None))
        self.stormprofile_btn_2.setText(QCoreApplication.translate("MainWindow", u"STORMWATER PROFILE", None))
        self.functional_btn_2.setText(QCoreApplication.translate("MainWindow", u"FUNCTIONAL DIMENSION", None))
        self.performance_btn_2.setText(QCoreApplication.translate("MainWindow", u"PERFORMANCE DIMENSION", None))
        self.dashboard_btn_2.setText(QCoreApplication.translate("MainWindow", u"RESILIENCE DASHBOARD", None))
        self.Home_Label2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">This tool aims at helping stormwater management bodies to assess and taccke factors that limit their resilience, following the </span><span style=\" font-size:14pt; font-weight:700;\">Resilience Framework for Urban Stormwater Systems!</span><br/></p></body></html>", None))
        self.Home_Label1.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">This tool aims at helping stormwater management bodies to assess and taccke factors that limit their resilience, following the </span><span style=\" font-size:14pt; font-weight:700;\">Resilience Framework for Urban Stormwater Systems!</span><br/></p></body></html>", None))
        self.studyNameLabel_3.setText(QCoreApplication.translate("MainWindow", u"Study name", None))
        self.Location_Label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">LOCATION</span></p></body></html>", None))
        self.countryLabel_6.setText(QCoreApplication.translate("MainWindow", u"Country", None))
        self.regionLabel_4.setText(QCoreApplication.translate("MainWindow", u"Region", None))
        self.cityLabel_4.setText(QCoreApplication.translate("MainWindow", u"City", None))
        self.Catchment_Label_2.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">CACTHMENT</span></p></body></html>", None))
        self.nameLabel_2.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.areaM2Label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Area (m<span style=\" vertical-align:super;\">2</span>)</p></body></html>", None))
        self.averageSlopeLabel_2.setText(QCoreApplication.translate("MainWindow", u"Average Slope (%)", None))
        self.UP_ToolBox.setItemText(self.UP_ToolBox.indexOf(self.Domain_Box), QCoreApplication.translate("MainWindow", u"DOMAIN", None))
        self.age0Label_5.setText(QCoreApplication.translate("MainWindow", u"0 - 14", None))
        self.age15LAbel_5.setText(QCoreApplication.translate("MainWindow", u"15 - 24", None))
        self.age25Lbael_5.setText(QCoreApplication.translate("MainWindow", u"25 - 64", None))
        self.age65Label_5.setText(QCoreApplication.translate("MainWindow", u"+ 65", None))
        self.Gender_Label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">GENDER DISTRIBUTION</span></p></body></html>", None))
        self.Age_Label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">AGE DISTRIBUTION</span></p></body></html>", None))
        self.inhabitantsLabel_4.setText(QCoreApplication.translate("MainWindow", u"Inhabitants", None))
        self.maleLabel_7.setText(QCoreApplication.translate("MainWindow", u"Male", None))
        self.femaleLabel_13.setText(QCoreApplication.translate("MainWindow", u"Female", None))
        self.UP_ToolBox.setItemText(self.UP_ToolBox.indexOf(self.Population_Box), QCoreApplication.translate("MainWindow", u"POPULATION", None))
        self.KoppenLabel.setText(QCoreApplication.translate("MainWindow", u"K\u00f6ppen class.", None))
        self.Rainfall_Label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">RAINFALL</span></p></body></html>", None))
        self.RmaxMonthlyMeanLabel_3.setText(QCoreApplication.translate("MainWindow", u"Max. monthly mean", None))
        self.RannualMeanLabel_3.setText(QCoreApplication.translate("MainWindow", u"Annual mean", None))
        self.RminMonthlyMeanLabel_3.setText(QCoreApplication.translate("MainWindow", u"Min. monthly mean", None))
        self.RminMonthlyMeanLineEdit_3.setStyleSheet(QCoreApplication.translate("MainWindow", u"background-color: white;", None))
        self.Temperature_Label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700;\">TEMPERATURE</span></p></body></html>", None))
        self.TmaxMonthlyMeanLabel_4.setText(QCoreApplication.translate("MainWindow", u"Max. monthly mean", None))
        self.TannualMeanLabel_4.setText(QCoreApplication.translate("MainWindow", u"Annual mean", None))
        self.TminMonthlyMeanLabel_4.setText(QCoreApplication.translate("MainWindow", u"Min. monthly mean", None))
        self.UP_ToolBox.setItemText(self.UP_ToolBox.indexOf(self.Climate_Box), QCoreApplication.translate("MainWindow", u"CLIMATE AND WEATHER", None))
        self.imperviousAreaLabel_2.setText(QCoreApplication.translate("MainWindow", u"Impervious area (%)", None))
#if QT_CONFIG(whatsthis)
        self.Infras_Label.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.Infras_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">URBAN INFRASTRUCTURES</span></p></body></html>", None))
        ___qtablewidgetitem = self.Infras_Table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Infrastructure", None));
        ___qtablewidgetitem1 = self.Infras_Table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"#", None));
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.UP_ToolBox.setItemText(self.UP_ToolBox.indexOf(self.Built_Box), QCoreApplication.translate("MainWindow", u"BUILT ENVIRONMENT", None))
        self.TotalLine_8.setText(QCoreApplication.translate("MainWindow", u"Total number", None))
        self.ExecLine_8.setText(QCoreApplication.translate("MainWindow", u"Executive members", None))
        self.ManageLine_8.setText(QCoreApplication.translate("MainWindow", u"Management members", None))
        self.OperationalLine_8.setText(QCoreApplication.translate("MainWindow", u"Operational members", None))
        self.Human_Label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">HUMAN RESOURCES</span></p></body></html>", None))
        self.swCoverageLabel_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>SW coverage area (m<span style=\" vertical-align:super;\">2</span>)</p></body></html>", None))
        self.utilityTypeLabel_8.setText(QCoreApplication.translate("MainWindow", u"Utility type", None))
        self.utilityNameLabel_8.setText(QCoreApplication.translate("MainWindow", u"Utility name", None))
        self.SW_ToolBox.setItemText(self.SW_ToolBox.indexOf(self.Service_Box), QCoreApplication.translate("MainWindow", u"SERVICE MANAGEMENT", None))
        self.separativeLengthKmLabel_7.setText(QCoreApplication.translate("MainWindow", u"Separative length (km)", None))
        self.combinedLengthKmLabel_7.setText(QCoreApplication.translate("MainWindow", u"Combined length (km)", None))
        self.averageDiameterMmLabel_7.setText(QCoreApplication.translate("MainWindow", u"Average diameter (mm)", None))
        self.averageAgeYearsLabel_7.setText(QCoreApplication.translate("MainWindow", u"Average age (years)", None))
        self.numberOfOutfallsLabel_7.setText(QCoreApplication.translate("MainWindow", u"Number of outfalls", None))
        self.Age_Label_14.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">PROPERTIES</span></p></body></html>", None))
        self.conveyanceTypeLabel_7.setText(QCoreApplication.translate("MainWindow", u"Conveyance type", None))
        self.conveyanceTypeComboBox_7.setItemText(0, QCoreApplication.translate("MainWindow", u"Separative", None))
        self.conveyanceTypeComboBox_7.setItemText(1, QCoreApplication.translate("MainWindow", u"Combined", None))
        self.conveyanceTypeComboBox_7.setItemText(2, QCoreApplication.translate("MainWindow", u"Mixed", None))

        self.conveyanceTypeComboBox_7.setCurrentText("")
        self.conveyanceTypeComboBox_7.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select type...", None))
        self.SpecEq_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">SPECIAL EQUIPMENT</span></p></body></html>", None))
        ___qtablewidgetitem2 = self.Infras_Table_2.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Infrastructure", None));
        ___qtablewidgetitem3 = self.Infras_Table_2.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"#", None));
        self.Infras_Button.setText(QCoreApplication.translate("MainWindow", u"Add urban infrastrcuture", None))
        self.SW_ToolBox.setItemText(self.SW_ToolBox.indexOf(self.Minor_Box), QCoreApplication.translate("MainWindow", u"MINOR SYSTEM", None))
        self.curbHeightLanel_5.setText(QCoreApplication.translate("MainWindow", u"Curb height (m)", None))
        self.buildingHeightLabel_5.setText(QCoreApplication.translate("MainWindow", u"Building entrace height (m)", None))
        self.streetWidthLabel_5.setText(QCoreApplication.translate("MainWindow", u"Street width (m)", None))
        self.streetLongSlopeMMLabel_5.setText(QCoreApplication.translate("MainWindow", u"Street long. slope (m/m)", None))
        self.streetLongSlopeMMLineEdit_5.setStyleSheet(QCoreApplication.translate("MainWindow", u"background-color: white;", None))
        self.Temperature_Label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">AVERAGE STREET SECTION</span></p></body></html>", None))
        self.lengthAlternativeLabel_5.setText(QCoreApplication.translate("MainWindow", u"Lenght of alternative flow path (km)", None))
        self.SW_ToolBox.setItemText(self.SW_ToolBox.indexOf(self.Major_Box), QCoreApplication.translate("MainWindow", u"MAJOR SYSTEM", None))
#if QT_CONFIG(whatsthis)
        self.ExistingNBS_Labael_8.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.ExistingNBS_Labael_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">EXISTING NBS</span></p></body></html>", None))
        ___qtablewidgetitem4 = self.NBS_TAble_8.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Infrastructure", None));
        ___qtablewidgetitem5 = self.NBS_TAble_8.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"#", None));
        ___qtablewidgetitem6 = self.NBS_TAble_8.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Unit", None));
        self.NBS_Button_8.setText(QCoreApplication.translate("MainWindow", u"Add NBS", None))
        self.SW_ToolBox.setItemText(self.SW_ToolBox.indexOf(self.NBS_Box), QCoreApplication.translate("MainWindow", u"NATURE BASED SOLUTIONS", None))
        self.ScenarioSU_btn.setText(QCoreApplication.translate("MainWindow", u"SCENARIO SET-UP", None))
        self.HazardSU_btn.setText(QCoreApplication.translate("MainWindow", u"HAZARD SET-UP", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"PERFROMANCE SCENARIOS SELECTION", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Baseline scenario:</span></p></body></html>", None))
        self.PSS_ComboBox.setCurrentText("")
        self.PSS_ComboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select baseline scenario...", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"FUNCTIONAL RESILIENCE RATING", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"SYSTEM CONSEQUENCES RATING", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"FUNCTIONAL OBJECTIVES RATING", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"FUNCTIONAL CRITERIA RATING", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Objective:</span></p></body></html>", None))
        self.FCR_ComboBox.setCurrentText("")
        self.FCR_ComboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select objective...", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"SYSTEM PERFORMANCE RATING", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"PERFORMANCE RESILIENCE RATING", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"FUNCTIONAL DIMENSION COMPLETNESS", None))
        self.left_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Developed by Jo\u00e3o Barreiro (<a href=\"mailto:joao.barreiro@tecnico.ulisboa.pt\"><span style=\" text-decoration: underline; color:#0000ff;\">joao.barreiro@tecnico.ulisboa.pt)</span></a></p></body></html>", None))
        self.right_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">Instituto Superior T\u00e9cnico</p></body></html>", None))
        self.menuFile_F.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

