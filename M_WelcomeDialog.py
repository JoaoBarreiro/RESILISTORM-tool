import sys
import os
import shutil
import re

from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton, QTreeWidget, QTreeWidgetItem,
                            QVBoxLayout, QButtonGroup, QRadioButton, QWidget,
                            QCheckBox, QLabel, QTextEdit, QStackedWidget, QLineEdit, QComboBox,
                            QScrollArea, QSizePolicy, QSpacerItem, QFileDialog, QTableView, QDialogButtonBox,
                            QMessageBox, QDialog, QStyledItemDelegate, QHeaderView, QMenu, QAbstractItemView,
                            QAbstractScrollArea, QStyleOptionButton, QStyle, QTableWidgetItem, QFrame, QHBoxLayout, QLayout)
from PySide6.QtCore import Qt, Signal, QEvent, QAbstractTableModel, QModelIndex, QCoreApplication

from W_WelcomeDialog import Ui_WelcomeDialog
from W_NewStudyDialog import Ui_NewStudyDialog

class NewStudyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NewStudyDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("New study setup")

        self.directory_label = ''
        self.name_label = ''
        
        self.ui.toolButton.clicked.connect(self.selectStudyDirectory)

        self.ui.buttonBox.accepted.connect(self.verifyInputs)
        
    def selectStudyDirectory(self):
        self.directory_label = QFileDialog.getExistingDirectory(self, "Select Study Directory")
        self.ui.studyDirectoryLineEdit.setText(self.directory_label)
    
    def verifyInputs(self):
        self.name_label = self.ui.studyNameLineEdit.text().strip()
        
        #Verify input conditions
        if self.name_label == "":
            QMessageBox.critical(self, "Error", "Study name cannot be empty!")
            return
        elif not re.match(r'^[a-zA-Z0-9_]+$', self.name_label):
            QMessageBox.critical(self, "Error", "Study name contains invalid characters!")
            return
        if not self.directory_label:
            QMessageBox.critical(self, "Error", "Study directory cannot be empty!")
            return
        
        study_name = self.name_label
        study_home_directory = self.directory_label
        study_directory = os.path.join(study_home_directory, study_name)
        
        # Verify if the study directory already exists
        if os.path.exists(study_directory):     #if it does, prompt the use about it and if Yes clear its contents
            prompt = QMessageBox.question(self, "Study directory already exists!", "The study directory already exists. Proceeding will delete all its contents and create a new analyis. \nAre you sure you want to proceed?")
            if prompt == QMessageBox.Yes:
                shutil.rmtree(study_directory)   #removes the folder
            else:
                return
        
        #creates the folder
        os.makedirs(study_directory) 
       
        self.study_name = self.name_label
        self.study_home_directory = self.directory_label
        self.study_directory = os.path.join(self.study_home_directory, self.study_name)
        
        QMessageBox.information(self, "Success!", "New study directory created!")
        
        self.close()

    def closeEvent(self, event):
        self.reject()
        self.close()                         

                
class WelcomeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WelcomeDialog()
        self.ui.setupUi(self)
       # self.setWindowTitle("RESILISTORM")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)

        self.ui.NewButton.clicked.connect(self.newStudy)
        self.ui.LoadButton.clicked.connect(self.loadStudy)
        self.ui.buttonBox.rejected.connect(self.reject)

    def newStudy(self):
        
        StudySetupWindow = NewStudyDialog()
        StudySetupWindow.exec()   
        
        self.study_name = StudySetupWindow.study_name
        self.study_directory = StudySetupWindow.study_directory
        
        self.accept()
        self.status = "New"
        
        self.close()

    def loadStudy(self):
        while True:
            load_path = QFileDialog.getExistingDirectory(self, "Load study directory", dir = os.getcwd())
            if load_path:
                self.study_name = find_file_with_suffix(load_path, "-STUDY.db")
                if not self.study_name:
                    QMessageBox.critical(self, "Error", "No study found in the selected directory!")
                else:
                    self.accept()  # Accept the dialog and return the load path
                    self.study_directory = load_path
                    self.status = "Old"
                    self.close()
                    break
            else:
                break
    
    def closeEvent(self, event):
        self.reject()
        self.close()     

def find_file_with_suffix(folder, suffix):
    for filename in os.listdir(folder):
        if filename.endswith(suffix):
            file_name = filename.split(suffix)[0]
            return file_name