# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SWMM_Performance_GUIEKRywt.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateTimeEdit, QDoubleSpinBox,
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 414)
        MainWindow.setMinimumSize(QSize(600, 350))
        MainWindow.setMaximumSize(QSize(600, 414))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
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
        self.RPT_label = QLabel(self.widget)
        self.RPT_label.setObjectName(u"RPT_label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.RPT_label)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.RPT_Filepath = QLineEdit(self.widget_3)
        self.RPT_Filepath.setObjectName(u"RPT_Filepath")
        self.RPT_Filepath.setEnabled(True)
        self.RPT_Filepath.setClearButtonEnabled(True)

        self.horizontalLayout_5.addWidget(self.RPT_Filepath)

        self.RPT_Search = QToolButton(self.widget_3)
        self.RPT_Search.setObjectName(u"RPT_Search")
        self.RPT_Search.setAutoRaise(False)

        self.horizontalLayout_5.addWidget(self.RPT_Search)


        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.widget_3)

        self.OUT_label = QLabel(self.widget)
        self.OUT_label.setObjectName(u"OUT_label")
        self.OUT_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.OUT_label)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.OUT_Filepath = QLineEdit(self.widget_2)
        self.OUT_Filepath.setObjectName(u"OUT_Filepath")
        self.OUT_Filepath.setEnabled(True)
        self.OUT_Filepath.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.OUT_Filepath)

        self.OUT_Search = QToolButton(self.widget_2)
        self.OUT_Search.setObjectName(u"OUT_Search")
        self.OUT_Search.setAutoRaise(False)

        self.horizontalLayout_3.addWidget(self.OUT_Search)


        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.widget_2)

        self.NodeList_label = QLabel(self.widget)
        self.NodeList_label.setObjectName(u"NodeList_label")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.NodeList_label)

        self.widget_11 = QWidget(self.widget)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.NodeList_checkBox = QCheckBox(self.widget_11)
        self.NodeList_checkBox.setObjectName(u"NodeList_checkBox")

        self.horizontalLayout_4.addWidget(self.NodeList_checkBox)

        self.horizontalSpacer = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.NodeList_Filepath = QLineEdit(self.widget_11)
        self.NodeList_Filepath.setObjectName(u"NodeList_Filepath")
        self.NodeList_Filepath.setEnabled(False)
        self.NodeList_Filepath.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.NodeList_Filepath)

        self.NodeList_Search = QToolButton(self.widget_11)
        self.NodeList_Search.setObjectName(u"NodeList_Search")
        self.NodeList_Search.setEnabled(False)
        self.NodeList_Search.setAutoRaise(False)

        self.horizontalLayout_4.addWidget(self.NodeList_Search)


        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.widget_11)


        self.verticalLayout.addLayout(self.formLayout_2)


        self.verticalLayout_2.addWidget(self.widget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_4 = QWidget(self.centralwidget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 9)
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
        self.EndDate.setMinimumDate(QDate(1753, 9, 14))

        self.horizontalLayout_6.addWidget(self.EndDate)


        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.widget_5)


        self.verticalLayout_3.addLayout(self.formLayout_3)


        self.horizontalLayout.addWidget(self.widget_4)

        self.widget_8 = QWidget(self.centralwidget)
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
        self.studyNameLabel_3 = QLabel(self.widget_8)
        self.studyNameLabel_3.setObjectName(u"studyNameLabel_3")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.studyNameLabel_3)

        self.widget_9 = QWidget(self.widget_8)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.MinorThreshold = QDoubleSpinBox(self.widget_9)
        self.MinorThreshold.setObjectName(u"MinorThreshold")
        self.MinorThreshold.setSingleStep(0.100000000000000)
        self.MinorThreshold.setValue(0.200000000000000)

        self.horizontalLayout_8.addWidget(self.MinorThreshold)


        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.widget_9)

        self.widget_10 = QWidget(self.widget_8)
        self.widget_10.setObjectName(u"widget_10")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontalLayout_9.addItem(self.verticalSpacer_3)


        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.widget_10)


        self.verticalLayout_4.addLayout(self.formLayout_4)


        self.horizontalLayout.addWidget(self.widget_8)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.widget_7 = QWidget(self.centralwidget)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.textEdit = QTextEdit(self.widget_7)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(True)
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.horizontalLayout_10.addWidget(self.textEdit)

        self.logBox = QCheckBox(self.widget_7)
        self.logBox.setObjectName(u"logBox")
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

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.footer_left_label = QLabel(self.centralwidget)
        self.footer_left_label.setObjectName(u"footer_left_label")
        self.footer_left_label.setOpenExternalLinks(True)

        self.horizontalLayout_11.addWidget(self.footer_left_label)

        self.footer_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.footer_horizontalSpacer)

        self.footer_right_label = QLabel(self.centralwidget)
        self.footer_right_label.setObjectName(u"footer_right_label")

        self.horizontalLayout_11.addWidget(self.footer_right_label)


        self.verticalLayout_2.addLayout(self.horizontalLayout_11)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.RPT_Filepath, self.RPT_Search)
        QWidget.setTabOrder(self.RPT_Search, self.OUT_Filepath)
        QWidget.setTabOrder(self.OUT_Filepath, self.OUT_Search)
        QWidget.setTabOrder(self.OUT_Search, self.NodeList_checkBox)
        QWidget.setTabOrder(self.NodeList_checkBox, self.NodeList_Filepath)
        QWidget.setTabOrder(self.NodeList_Filepath, self.NodeList_Search)
        QWidget.setTabOrder(self.NodeList_Search, self.StartingDate)
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
        self.RPT_label.setText(QCoreApplication.translate("MainWindow", u"RPT File:", None))
#if QT_CONFIG(tooltip)
        self.RPT_Filepath.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.RPT_Filepath.setInputMask("")
        self.RPT_Filepath.setText("")
        self.RPT_Search.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.OUT_label.setText(QCoreApplication.translate("MainWindow", u"OUT File:", None))
#if QT_CONFIG(tooltip)
        self.OUT_Filepath.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.OUT_Filepath.setText("")
        self.OUT_Search.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.NodeList_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Text file where each line corresponds to the nodes to be included in the analysis.</p><p>If not provided, all nodes are considered.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.NodeList_label.setText(QCoreApplication.translate("MainWindow", u"Node Report List:", None))
        self.NodeList_checkBox.setText("")
#if QT_CONFIG(tooltip)
        self.NodeList_Filepath.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.NodeList_Filepath.setText("")
        self.NodeList_Filepath.setPlaceholderText("")
        self.NodeList_Search.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Analysis period", None))
        self.studyNameLabel_2.setText(QCoreApplication.translate("MainWindow", u"Starting date:", None))
        self.StartingDate.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd/MM/yyyy HH:mm:ss", None))
        self.studyDirectoryLabel_2.setText(QCoreApplication.translate("MainWindow", u"Ending date:", None))
        self.EndDate.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd/MM/yyyy HH:mm:ss", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Flooding thresholds", None))
        self.studyNameLabel_3.setText(QCoreApplication.translate("MainWindow", u"Minor system:", None))
        self.MinorThreshold.setSuffix(QCoreApplication.translate("MainWindow", u" meters", None))
        self.textEdit.setPlaceholderText("")
        self.logBox.setText(QCoreApplication.translate("MainWindow", u"Print log file", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"Run!", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.footer_left_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:7pt;\">Developed by Jo\u00e3o Barreiro </span><a href=\"mailto:joao.barreiro@tecnico.ulisboa.pt\"><span style=\" font-size:7pt; text-decoration: underline; color:#0000ff;\">(joao.barreiro@tecnico.ulisboa.pt)</span></a></p></body></html>", None))
        self.footer_right_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:7pt;\">Instituto Superior T\u00e9cnico - University of Lisbon</span></p></body></html>", None))
    # retranslateUi

