# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SWMM_Performance_GUI_V2VDNLay.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QDateTimeEdit,
    QDoubleSpinBox, QFormLayout, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 550)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(600, 550))
        MainWindow.setMaximumSize(QSize(600, 550))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)

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

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetMinimumSize)
        self.Input_table = QTableWidget(self.widget)
        if (self.Input_table.columnCount() < 3):
            self.Input_table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.Input_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.Input_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.Input_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.Input_table.setObjectName(u"Input_table")
        self.Input_table.setMinimumSize(QSize(0, 100))
        self.Input_table.verticalHeader().setCascadingSectionResizes(True)

        self.horizontalLayout_5.addWidget(self.Input_table)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.addRow_button = QPushButton(self.widget)
        self.addRow_button.setObjectName(u"addRow_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.addRow_button.sizePolicy().hasHeightForWidth())
        self.addRow_button.setSizePolicy(sizePolicy2)

        self.verticalLayout_6.addWidget(self.addRow_button)

        self.delRow_button = QPushButton(self.widget)
        self.delRow_button.setObjectName(u"delRow_button")
        sizePolicy2.setHeightForWidth(self.delRow_button.sizePolicy().hasHeightForWidth())
        self.delRow_button.setSizePolicy(sizePolicy2)

        self.verticalLayout_6.addWidget(self.delRow_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)


        self.horizontalLayout_5.addLayout(self.verticalLayout_6)

        self.horizontalLayout_5.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.NodeList_label = QLabel(self.widget)
        self.NodeList_label.setObjectName(u"NodeList_label")

        self.horizontalLayout_4.addWidget(self.NodeList_label)

        self.NodeList_checkBox = QCheckBox(self.widget)
        self.NodeList_checkBox.setObjectName(u"NodeList_checkBox")

        self.horizontalLayout_4.addWidget(self.NodeList_checkBox)

        self.NodeList_Filepath = QLineEdit(self.widget)
        self.NodeList_Filepath.setObjectName(u"NodeList_Filepath")
        self.NodeList_Filepath.setEnabled(False)
        self.NodeList_Filepath.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.NodeList_Filepath)

        self.NodeList_Search = QToolButton(self.widget)
        self.NodeList_Search.setObjectName(u"NodeList_Search")
        self.NodeList_Search.setEnabled(False)
        self.NodeList_Search.setAutoRaise(False)

        self.horizontalLayout_4.addWidget(self.NodeList_Search)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addWidget(self.widget)

        self.widget1 = QWidget(self.centralwidget)
        self.widget1.setObjectName(u"widget1")
        sizePolicy1.setHeightForWidth(self.widget1.sizePolicy().hasHeightForWidth())
        self.widget1.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget1)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy1.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy1)
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
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)

        self.FloodVolume_checkbox = QCheckBox(self.widget_10)
        self.FloodVolume_checkbox.setObjectName(u"FloodVolume_checkbox")
        self.FloodVolume_checkbox.setChecked(True)
        self.FloodVolume_checkbox.setTristate(False)

        self.horizontalLayout_9.addWidget(self.FloodVolume_checkbox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)


        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.widget_10)

        self.MinorThreshold_label = QLabel(self.widget_8)
        self.MinorThreshold_label.setObjectName(u"MinorThreshold_label")
        self.MinorThreshold_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.MinorThreshold_label)

        self.FloodVolume_label = QLabel(self.widget_8)
        self.FloodVolume_label.setObjectName(u"FloodVolume_label")
        self.FloodVolume_label.setAlignment(Qt.AlignCenter)

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.FloodVolume_label)


        self.verticalLayout_4.addLayout(self.formLayout_4)


        self.horizontalLayout.addWidget(self.widget_8)


        self.verticalLayout_2.addWidget(self.widget1)

        self.widget_12 = QWidget(self.centralwidget)
        self.widget_12.setObjectName(u"widget_12")
        sizePolicy1.setHeightForWidth(self.widget_12.sizePolicy().hasHeightForWidth())
        self.widget_12.setSizePolicy(sizePolicy1)
        self.verticalLayout_5 = QVBoxLayout(self.widget_12)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.label_5 = QLabel(self.widget_12)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setFont(font)
        self.label_5.setScaledContents(False)

        self.verticalLayout_5.addWidget(self.label_5)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignCenter)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(6)
        self.AllNodesPlot_label = QLabel(self.widget_12)
        self.AllNodesPlot_label.setObjectName(u"AllNodesPlot_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.AllNodesPlot_label)

        self.AllNodesPlot_checkBox = QCheckBox(self.widget_12)
        self.AllNodesPlot_checkBox.setObjectName(u"AllNodesPlot_checkBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.AllNodesPlot_checkBox.sizePolicy().hasHeightForWidth())
        self.AllNodesPlot_checkBox.setSizePolicy(sizePolicy3)
        self.AllNodesPlot_checkBox.setIconSize(QSize(16, 16))
        self.AllNodesPlot_checkBox.setTristate(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.AllNodesPlot_checkBox)

        self.WeightedSystemPlot_label = QLabel(self.widget_12)
        self.WeightedSystemPlot_label.setObjectName(u"WeightedSystemPlot_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.WeightedSystemPlot_label)

        self.WeightedSystemPlot_checkBox = QCheckBox(self.widget_12)
        self.WeightedSystemPlot_checkBox.setObjectName(u"WeightedSystemPlot_checkBox")
        sizePolicy3.setHeightForWidth(self.WeightedSystemPlot_checkBox.sizePolicy().hasHeightForWidth())
        self.WeightedSystemPlot_checkBox.setSizePolicy(sizePolicy3)
        self.WeightedSystemPlot_checkBox.setChecked(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.WeightedSystemPlot_checkBox)

        self.WeightNodesResilience_label = QLabel(self.widget_12)
        self.WeightNodesResilience_label.setObjectName(u"WeightNodesResilience_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.WeightNodesResilience_label)

        self.WeightNodesResilience_checkBox = QCheckBox(self.widget_12)
        self.WeightNodesResilience_checkBox.setObjectName(u"WeightNodesResilience_checkBox")
        sizePolicy3.setHeightForWidth(self.WeightNodesResilience_checkBox.sizePolicy().hasHeightForWidth())
        self.WeightNodesResilience_checkBox.setSizePolicy(sizePolicy3)
        self.WeightNodesResilience_checkBox.setChecked(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.WeightNodesResilience_checkBox)


        self.verticalLayout_5.addLayout(self.formLayout)


        self.verticalLayout_2.addWidget(self.widget_12)

        self.widget_7 = QWidget(self.centralwidget)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy1.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy1)
        self.horizontalLayout_10 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(6, 6, 6, 6)
        self.textEdit = QTextEdit(self.widget_7)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy4)
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
        sizePolicy1.setHeightForWidth(self.widget2.sizePolicy().hasHeightForWidth())
        self.widget2.setSizePolicy(sizePolicy1)
        self.horizontalLayout_11 = QHBoxLayout(self.widget2)
        self.horizontalLayout_11.setSpacing(6)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.footer_left_label = QLabel(self.widget2)
        self.footer_left_label.setObjectName(u"footer_left_label")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.footer_left_label.sizePolicy().hasHeightForWidth())
        self.footer_left_label.setSizePolicy(sizePolicy5)
        self.footer_left_label.setOpenExternalLinks(True)

        self.horizontalLayout_11.addWidget(self.footer_left_label)

        self.footer_right_label = QLabel(self.widget2)
        self.footer_right_label.setObjectName(u"footer_right_label")
        sizePolicy5.setHeightForWidth(self.footer_right_label.sizePolicy().hasHeightForWidth())
        self.footer_right_label.setSizePolicy(sizePolicy5)
        self.footer_right_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.footer_right_label)


        self.verticalLayout_2.addWidget(self.widget2)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.StartingDate, self.EndDate)
        QWidget.setTabOrder(self.EndDate, self.MinorThreshold)
        QWidget.setTabOrder(self.MinorThreshold, self.textEdit)
        QWidget.setTabOrder(self.textEdit, self.logBox)
        QWidget.setTabOrder(self.logBox, self.runButton)
        QWidget.setTabOrder(self.runButton, self.closeButton)

        self.retranslateUi(MainWindow)
        self.NodeList_checkBox.toggled.connect(self.NodeList_Filepath.setEnabled)
        self.NodeList_checkBox.toggled.connect(self.NodeList_Search.setEnabled)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">Minor system performance resilience tool</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"SWMM Files", None))
        ___qtablewidgetitem = self.Input_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"ID label", None));
        ___qtablewidgetitem1 = self.Input_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"RPT File", None));
        ___qtablewidgetitem2 = self.Input_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"OUT File", None));
        self.addRow_button.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.delRow_button.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.NodeList_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Text file where each line corresponds to the nodes to be included in the analysis.</p><p>If not provided, all nodes from SWMM report are considered.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.NodeList_label.setText(QCoreApplication.translate("MainWindow", u"Node Filter:", None))
        self.NodeList_checkBox.setText("")
#if QT_CONFIG(tooltip)
        self.NodeList_Filepath.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.NodeList_Filepath.setText("")
        self.NodeList_Filepath.setPlaceholderText("")
        self.NodeList_Search.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Analysis period", None))
        self.studyNameLabel_2.setText(QCoreApplication.translate("MainWindow", u"Starting date:", None))
        self.StartingDate.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd/MM/yyyy HH:mm:ss", None))
        self.studyDirectoryLabel_2.setText(QCoreApplication.translate("MainWindow", u"Ending date:", None))
        self.EndDate.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd/MM/yyyy HH:mm:ss", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.MinorThreshold.setSuffix(QCoreApplication.translate("MainWindow", u" meters", None))
        self.FloodVolume_checkbox.setText("")
#if QT_CONFIG(tooltip)
        self.MinorThreshold_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Depth above node elevation that defines the failure depth for Flooding Resilience calculation.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.MinorThreshold_label.setText(QCoreApplication.translate("MainWindow", u"Minor system flooding threshold:", None))
#if QT_CONFIG(tooltip)
        self.FloodVolume_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Check if flooded volume in each node is to be used at Flooding Resilience calculation.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.FloodVolume_label.setText(QCoreApplication.translate("MainWindow", u"Use flood volume:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Output figures", None))
        self.AllNodesPlot_label.setText(QCoreApplication.translate("MainWindow", u"Resilience Nodes Performance:", None))
        self.WeightedSystemPlot_label.setText(QCoreApplication.translate("MainWindow", u"Weighted System Resilience Performance:", None))
        self.WeightNodesResilience_label.setText(QCoreApplication.translate("MainWindow", u"Weight vs Nodes Resilience:", None))
        self.textEdit.setPlaceholderText("")
        self.logBox.setText(QCoreApplication.translate("MainWindow", u"Print log file", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"Run!", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.footer_left_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:7pt;\">Developed by Jo\u00e3o Barreiro </span><a href=\"mailto:joao.barreiro@tecnico.ulisboa.pt\"><span style=\" font-size:7pt; text-decoration: underline; color:#0000ff;\">(joao.barreiro@tecnico.ulisboa.pt)</span></a></p></body></html>", None))
        self.footer_right_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:7pt;\">Instituto Superior T\u00e9cnico - University of Lisbon</span></p></body></html>", None))
    # retranslateUi

