# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewStudyDialogEKYpwE.ui'
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
    QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_NewStudyDialog(object):
    def setupUi(self, NewStudyDialog):
        if not NewStudyDialog.objectName():
            NewStudyDialog.setObjectName(u"NewStudyDialog")
        NewStudyDialog.resize(456, 122)
        NewStudyDialog.setMinimumSize(QSize(456, 122))
        NewStudyDialog.setMaximumSize(QSize(456, 122))
        NewStudyDialog.setModal(False)
        self.verticalLayout_2 = QVBoxLayout(NewStudyDialog)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(NewStudyDialog)
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
        self.studyNameLabel = QLabel(self.widget)
        self.studyNameLabel.setObjectName(u"studyNameLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.studyNameLabel)

        self.studyNameLineEdit = QLineEdit(self.widget)
        self.studyNameLineEdit.setObjectName(u"studyNameLineEdit")
        self.studyNameLineEdit.setMaxLength(15)
        self.studyNameLineEdit.setFrame(True)
        self.studyNameLineEdit.setEchoMode(QLineEdit.Normal)
        self.studyNameLineEdit.setClearButtonEnabled(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.studyNameLineEdit)

        self.studyDirectoryLabel = QLabel(self.widget)
        self.studyDirectoryLabel.setObjectName(u"studyDirectoryLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.studyDirectoryLabel)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.studyDirectoryLineEdit = QLineEdit(self.widget_2)
        self.studyDirectoryLineEdit.setObjectName(u"studyDirectoryLineEdit")
        self.studyDirectoryLineEdit.setEnabled(True)
        self.studyDirectoryLineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.studyDirectoryLineEdit)

        self.toolButton = QToolButton(self.widget_2)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setAutoRaise(False)

        self.horizontalLayout_3.addWidget(self.toolButton)


        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.widget_2)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(NewStudyDialog)

        QMetaObject.connectSlotsByName(NewStudyDialog)
    # setupUi

    def retranslateUi(self, NewStudyDialog):
        NewStudyDialog.setWindowTitle(QCoreApplication.translate("NewStudyDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("NewStudyDialog", u"Set new analysis", None))
        self.studyNameLabel.setText(QCoreApplication.translate("NewStudyDialog", u"New stury name:", None))
#if QT_CONFIG(tooltip)
        self.studyNameLineEdit.setToolTip(QCoreApplication.translate("NewStudyDialog", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.studyNameLineEdit.setWhatsThis(QCoreApplication.translate("NewStudyDialog", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.studyNameLineEdit.setInputMask("")
        self.studyNameLineEdit.setPlaceholderText(QCoreApplication.translate("NewStudyDialog", u"No spaces or special characters allowed!", None))
        self.studyDirectoryLabel.setText(QCoreApplication.translate("NewStudyDialog", u"New study directory:", None))
#if QT_CONFIG(tooltip)
        self.studyDirectoryLineEdit.setToolTip(QCoreApplication.translate("NewStudyDialog", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton.setText(QCoreApplication.translate("NewStudyDialog", u"...", None))
    # retranslateUi

