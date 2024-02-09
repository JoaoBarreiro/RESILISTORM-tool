# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SOL_tool_GUIxndFSN.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDateTimeEdit, QDoubleSpinBox, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QTextEdit,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 500)
        MainWindow.setMinimumSize(QSize(600, 500))
        MainWindow.setMaximumSize(QSize(600, 500))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label_4)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout_2.setFormAlignment(Qt.AlignCenter)
        self.formLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.DepthFile_label = QLabel(self.widget)
        self.DepthFile_label.setObjectName(u"DepthFile_label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.DepthFile_label)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.DepthFile_Filepath = QLineEdit(self.widget_3)
        self.DepthFile_Filepath.setObjectName(u"DepthFile_Filepath")
        self.DepthFile_Filepath.setEnabled(True)
        self.DepthFile_Filepath.setClearButtonEnabled(True)

        self.horizontalLayout_5.addWidget(self.DepthFile_Filepath)

        self.DepthFile_Search = QToolButton(self.widget_3)
        self.DepthFile_Search.setObjectName(u"DepthFile_Search")
        self.DepthFile_Search.setAutoRaise(False)

        self.horizontalLayout_5.addWidget(self.DepthFile_Search)


        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.widget_3)

        self.VelocityFile_label = QLabel(self.widget)
        self.VelocityFile_label.setObjectName(u"VelocityFile_label")
        self.VelocityFile_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.VelocityFile_label)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.VelocityFile_Filepath = QLineEdit(self.widget_2)
        self.VelocityFile_Filepath.setObjectName(u"VelocityFile_Filepath")
        self.VelocityFile_Filepath.setEnabled(False)
        self.VelocityFile_Filepath.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.VelocityFile_Filepath)

        self.VelocityFile_Search = QToolButton(self.widget_2)
        self.VelocityFile_Search.setObjectName(u"VelocityFile_Search")
        self.VelocityFile_Search.setEnabled(False)
        self.VelocityFile_Search.setAutoRaise(False)

        self.horizontalLayout_3.addWidget(self.VelocityFile_Search)


        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.widget_2)

        self.MeshFile_label = QLabel(self.widget)
        self.MeshFile_label.setObjectName(u"MeshFile_label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.MeshFile_label)

        self.widget_16 = QWidget(self.widget)
        self.widget_16.setObjectName(u"widget_16")
        self.horizontalLayout_14 = QHBoxLayout(self.widget_16)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.MeshFile_Filepath = QLineEdit(self.widget_16)
        self.MeshFile_Filepath.setObjectName(u"MeshFile_Filepath")
        self.MeshFile_Filepath.setEnabled(True)
        self.MeshFile_Filepath.setClearButtonEnabled(True)

        self.horizontalLayout_14.addWidget(self.MeshFile_Filepath)

        self.MeshFile_Search = QToolButton(self.widget_16)
        self.MeshFile_Search.setObjectName(u"MeshFile_Search")
        self.MeshFile_Search.setAutoRaise(False)

        self.horizontalLayout_14.addWidget(self.MeshFile_Search)


        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.widget_16)


        self.verticalLayout.addLayout(self.formLayout_2)


        self.verticalLayout_2.addWidget(self.widget)

        self.widget1 = QWidget(self.centralwidget)
        self.widget1.setObjectName(u"widget1")
        sizePolicy.setHeightForWidth(self.widget1.sizePolicy().hasHeightForWidth())
        self.widget1.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.widget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget1)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.label_2 = QLabel(self.widget_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_3.addWidget(self.label_2)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout_3.setFormAlignment(Qt.AlignCenter)
        self.formLayout_3.setVerticalSpacing(6)
        self.studyNameLabel_2 = QLabel(self.widget_4)
        self.studyNameLabel_2.setObjectName(u"studyNameLabel_2")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.studyNameLabel_2)

        self.widget_6 = QWidget(self.widget_4)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.StartingDate = QDateTimeEdit(self.widget_6)
        self.StartingDate.setObjectName(u"StartingDate")
        self.StartingDate.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.StartingDate)


        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.widget_6)

        self.studyDirectoryLabel_2 = QLabel(self.widget_4)
        self.studyDirectoryLabel_2.setObjectName(u"studyDirectoryLabel_2")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.studyDirectoryLabel_2)

        self.widget_5 = QWidget(self.widget_4)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.EndDate = QDateTimeEdit(self.widget_5)
        self.EndDate.setObjectName(u"EndDate")
        self.EndDate.setAlignment(Qt.AlignCenter)
        self.EndDate.setMinimumDate(QDate(1753, 9, 14))

        self.horizontalLayout_6.addWidget(self.EndDate)


        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.widget_5)


        self.verticalLayout_3.addLayout(self.formLayout_3)


        self.horizontalLayout.addWidget(self.widget_4)

        self.line_3 = QFrame(self.widget1)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.widget_8 = QWidget(self.widget1)
        self.widget_8.setObjectName(u"widget_8")
        self.verticalLayout_4 = QVBoxLayout(self.widget_8)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_3 = QLabel(self.widget_8)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_4.addWidget(self.label_3)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout_4.setFormAlignment(Qt.AlignCenter)
        self.formLayout_4.setVerticalSpacing(6)
        self.widget_9 = QWidget(self.widget_8)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.MinorThreshold = QDoubleSpinBox(self.widget_9)
        self.MinorThreshold.setObjectName(u"MinorThreshold")
        self.MinorThreshold.setAlignment(Qt.AlignCenter)
        self.MinorThreshold.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.MinorThreshold.setSingleStep(0.100000000000000)
        self.MinorThreshold.setValue(0.150000000000000)

        self.horizontalLayout_8.addWidget(self.MinorThreshold)


        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.widget_9)

        self.widget_10 = QWidget(self.widget_8)
        self.widget_10.setObjectName(u"widget_10")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.MajorThreshold = QDoubleSpinBox(self.widget_10)
        self.MajorThreshold.setObjectName(u"MajorThreshold")
        self.MajorThreshold.setAlignment(Qt.AlignCenter)
        self.MajorThreshold.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.MajorThreshold.setSingleStep(0.100000000000000)
        self.MajorThreshold.setValue(0.300000000000000)

        self.horizontalLayout_9.addWidget(self.MajorThreshold)


        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.widget_10)

        self.MinorThreshold_label = QLabel(self.widget_8)
        self.MinorThreshold_label.setObjectName(u"MinorThreshold_label")
        self.MinorThreshold_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.MinorThreshold_label)

        self.MajorThreshold_label = QLabel(self.widget_8)
        self.MajorThreshold_label.setObjectName(u"MajorThreshold_label")
        self.MajorThreshold_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.MajorThreshold_label)


        self.verticalLayout_4.addLayout(self.formLayout_4)


        self.horizontalLayout.addWidget(self.widget_8)


        self.verticalLayout_2.addWidget(self.widget1)

        self.widget_12 = QWidget(self.centralwidget)
        self.widget_12.setObjectName(u"widget_12")
        sizePolicy.setHeightForWidth(self.widget_12.sizePolicy().hasHeightForWidth())
        self.widget_12.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.widget_12)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.label_5 = QLabel(self.widget_12)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFont(font)
        self.label_5.setScaledContents(False)

        self.verticalLayout_5.addWidget(self.label_5)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignCenter)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(6)
        self.SFP_label = QLabel(self.widget_12)
        self.SFP_label.setObjectName(u"SFP_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.SFP_label)

        self.SFP_checkBox = QCheckBox(self.widget_12)
        self.SFP_checkBox.setObjectName(u"SFP_checkBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.SFP_checkBox.sizePolicy().hasHeightForWidth())
        self.SFP_checkBox.setSizePolicy(sizePolicy1)
        self.SFP_checkBox.setIconSize(QSize(16, 16))
        self.SFP_checkBox.setChecked(True)
        self.SFP_checkBox.setTristate(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.SFP_checkBox)

        self.IHP_label = QLabel(self.widget_12)
        self.IHP_label.setObjectName(u"IHP_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.IHP_label.sizePolicy().hasHeightForWidth())
        self.IHP_label.setSizePolicy(sizePolicy2)
        self.IHP_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.IHP_label)

        self.IHV_label = QLabel(self.widget_12)
        self.IHV_label.setObjectName(u"IHV_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.IHV_label)

        self.IHV_checkBox = QCheckBox(self.widget_12)
        self.IHV_checkBox.setObjectName(u"IHV_checkBox")
        sizePolicy1.setHeightForWidth(self.IHV_checkBox.sizePolicy().hasHeightForWidth())
        self.IHV_checkBox.setSizePolicy(sizePolicy1)
        self.IHV_checkBox.setChecked(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.IHV_checkBox)

        self.widget_11 = QWidget(self.widget_12)
        self.widget_11.setObjectName(u"widget_11")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy3)
        self.horizontalLayout_4 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.IHP_checkBox = QCheckBox(self.widget_11)
        self.IHP_checkBox.setObjectName(u"IHP_checkBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.IHP_checkBox.sizePolicy().hasHeightForWidth())
        self.IHP_checkBox.setSizePolicy(sizePolicy4)
        self.IHP_checkBox.setChecked(True)

        self.horizontalLayout_4.addWidget(self.IHP_checkBox)

        self.UHP_comboBox = QComboBox(self.widget_11)
        self.UHP_comboBox.addItem("")
        self.UHP_comboBox.addItem("")
        self.UHP_comboBox.setObjectName(u"UHP_comboBox")
        self.UHP_comboBox.setEnabled(True)
        sizePolicy.setHeightForWidth(self.UHP_comboBox.sizePolicy().hasHeightForWidth())
        self.UHP_comboBox.setSizePolicy(sizePolicy)
        self.UHP_comboBox.setFrame(True)

        self.horizontalLayout_4.addWidget(self.UHP_comboBox)

        self.horizontalLayout_4.setStretch(1, 1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.widget_11)


        self.verticalLayout_5.addLayout(self.formLayout)


        self.verticalLayout_2.addWidget(self.widget_12)

        self.widget_7 = QWidget(self.centralwidget)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.horizontalLayout_10 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(6, 6, 6, 6)
        self.textEdit = QTextEdit(self.widget_7)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy5)
        self.textEdit.setMinimumSize(QSize(0, 80))
        self.textEdit.setMaximumSize(QSize(16777215, 80))
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.horizontalLayout_10.addWidget(self.textEdit)

        self.logBox = QCheckBox(self.widget_7)
        self.logBox.setObjectName(u"logBox")
        self.logBox.setEnabled(False)
        self.logBox.setIconSize(QSize(16, 16))
        self.logBox.setChecked(True)
        self.logBox.setTristate(False)

        self.horizontalLayout_10.addWidget(self.logBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.runButton = QPushButton(self.widget_7)
        self.runButton.setObjectName(u"runButton")

        self.horizontalLayout_2.addWidget(self.runButton)

        self.closeButton = QPushButton(self.widget_7)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_2.addWidget(self.closeButton)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.widget_7)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.widget2 = QWidget(self.centralwidget)
        self.widget2.setObjectName(u"widget2")
        sizePolicy.setHeightForWidth(self.widget2.sizePolicy().hasHeightForWidth())
        self.widget2.setSizePolicy(sizePolicy)
        self.horizontalLayout_11 = QHBoxLayout(self.widget2)
        self.horizontalLayout_11.setSpacing(6)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.footer_left_label = QLabel(self.widget2)
        self.footer_left_label.setObjectName(u"footer_left_label")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.footer_left_label.sizePolicy().hasHeightForWidth())
        self.footer_left_label.setSizePolicy(sizePolicy6)
        self.footer_left_label.setOpenExternalLinks(True)

        self.horizontalLayout_11.addWidget(self.footer_left_label)

        self.footer_right_label = QLabel(self.widget2)
        self.footer_right_label.setObjectName(u"footer_right_label")
        sizePolicy6.setHeightForWidth(self.footer_right_label.sizePolicy().hasHeightForWidth())
        self.footer_right_label.setSizePolicy(sizePolicy6)
        self.footer_right_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.footer_right_label)


        self.verticalLayout_2.addWidget(self.widget2)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.MeshFile_Filepath, self.MeshFile_Search)
        QWidget.setTabOrder(self.MeshFile_Search, self.DepthFile_Filepath)
        QWidget.setTabOrder(self.DepthFile_Filepath, self.DepthFile_Search)
        QWidget.setTabOrder(self.DepthFile_Search, self.VelocityFile_Filepath)
        QWidget.setTabOrder(self.VelocityFile_Filepath, self.VelocityFile_Search)
        QWidget.setTabOrder(self.VelocityFile_Search, self.StartingDate)
        QWidget.setTabOrder(self.StartingDate, self.EndDate)
        QWidget.setTabOrder(self.EndDate, self.MinorThreshold)
        QWidget.setTabOrder(self.MinorThreshold, self.MajorThreshold)
        QWidget.setTabOrder(self.MajorThreshold, self.SFP_checkBox)
        QWidget.setTabOrder(self.SFP_checkBox, self.IHP_checkBox)
        QWidget.setTabOrder(self.IHP_checkBox, self.UHP_comboBox)
        QWidget.setTabOrder(self.UHP_comboBox, self.IHV_checkBox)
        QWidget.setTabOrder(self.IHV_checkBox, self.textEdit)
        QWidget.setTabOrder(self.textEdit, self.logBox)
        QWidget.setTabOrder(self.logBox, self.runButton)
        QWidget.setTabOrder(self.runButton, self.closeButton)

        self.retranslateUi(MainWindow)
        self.IHP_checkBox.toggled.connect(self.UHP_comboBox.setEnabled)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">Major system performance resilience tool</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Simulation files", None))
        self.DepthFile_label.setText(QCoreApplication.translate("MainWindow", u"Depth file (*.sol)", None))
#if QT_CONFIG(tooltip)
        self.DepthFile_Filepath.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.DepthFile_Filepath.setInputMask("")
        self.DepthFile_Filepath.setText("")
        self.DepthFile_Search.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.VelocityFile_label.setText(QCoreApplication.translate("MainWindow", u"Velocity file (*.sol)", None))
#if QT_CONFIG(tooltip)
        self.VelocityFile_Filepath.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.VelocityFile_Filepath.setText("")
        self.VelocityFile_Search.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.MeshFile_label.setText(QCoreApplication.translate("MainWindow", u"2D Mesh file (*2.dm)", None))
#if QT_CONFIG(tooltip)
        self.MeshFile_Filepath.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.MeshFile_Filepath.setInputMask("")
        self.MeshFile_Filepath.setText("")
        self.MeshFile_Search.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Analysis period", None))
        self.studyNameLabel_2.setText(QCoreApplication.translate("MainWindow", u"Starting date:", None))
        self.StartingDate.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd/MM/yyyy HH:mm:ss", None))
        self.studyDirectoryLabel_2.setText(QCoreApplication.translate("MainWindow", u"Ending date:", None))
        self.EndDate.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd/MM/yyyy HH:mm:ss", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.MinorThreshold.setSuffix(QCoreApplication.translate("MainWindow", u" meters", None))
        self.MajorThreshold.setSuffix(QCoreApplication.translate("MainWindow", u" meters", None))
#if QT_CONFIG(tooltip)
        self.MinorThreshold_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Depth above node elevation that defines the failure depth for Flooding Resilience calculation.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.MinorThreshold_label.setText(QCoreApplication.translate("MainWindow", u"Minor system flooding threshold:", None))
#if QT_CONFIG(tooltip)
        self.MajorThreshold_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Depth above node elevation that defines the failure depth for Flooding Resilience calculation.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.MajorThreshold_label.setText(QCoreApplication.translate("MainWindow", u"Major system flooding threshold:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Output results", None))
        self.SFP_label.setText(QCoreApplication.translate("MainWindow", u"Surface flooding performance", None))
        self.IHP_label.setText(QCoreApplication.translate("MainWindow", u"Indicator of Hazard to Pedestrians (IHP)", None))
        self.IHV_label.setText(QCoreApplication.translate("MainWindow", u"Indicator of Hazard to Vehicles (IHV)", None))
        self.UHP_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Defra, 2005", None))
        self.UHP_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Martinez, 2017", None))

        self.textEdit.setPlaceholderText("")
        self.logBox.setText(QCoreApplication.translate("MainWindow", u"Print log file", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"Run!", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.footer_left_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:7pt;\">Developed by Jo\u00e3o Barreiro </span><a href=\"mailto:joao.barreiro@tecnico.ulisboa.pt\"><span style=\" font-size:7pt; text-decoration: underline; color:#0000ff;\">(joao.barreiro@tecnico.ulisboa.pt)</span></a></p></body></html>", None))
        self.footer_right_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:7pt;\">Instituto Superior T\u00e9cnico - University of Lisbon</span></p></body></html>", None))
    # retranslateUi

