from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog, QSpacerItem, QSizePolicy, QDialog, QLabel, 
                               QScrollArea, QMessageBox, QFrame, QFormLayout, QLineEdit, QCheckBox, QRadioButton, QLabel, QButtonGroup
                               )

from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from functools import partial

from M_Fonts import MyFont

import sys
import re

class IndicatorsSelection(QMainWindow):
    def __init__(self, refuss_db, answer_db):
        super().__init__()
        self.refuss_db = refuss_db
        self.answer_db = answer_db

        self.radio_button_groups = {}  # Dictionary to manage radio button groups for each class
                
        self.selected_indicators = self.load_selected_indicators()  
               
        self.setWindowModality(Qt.WindowModal) 
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Performance Indicators Selection")
                        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
                
        # Create the UI elements and check if indicators are already selected
        
        # Fetch data from IndicatorsClasses and IndicatorsLibrary tables
        query_class = QSqlQuery(self.refuss_db)
        query_class.exec("SELECT * FROM IndicatorsClasses")

        while query_class.next():
            class_id = query_class.value(0)
            class_name = query_class.value(1)
            exclusive = query_class.value(2)
            
            label = QLabel(class_name)
            label.setFont(MyFont(10, True))
            layout.addWidget(label)

            if class_id not in self.selected_indicators:
                self.selected_indicators[class_id] = []

            # Create a frame to group the radio buttons and checkboxes
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            frame.setObjectName(class_name)
            #frame.setFrameShadow(QFrame.Raised)
            frame.setStyleSheet("background-color: rgb(255, 255, 255);")
            
            # Create a layout for the frame
            frame_layout = QVBoxLayout(frame)
            
            if exclusive == 'YES':    
                # Create a button group to manage radio buttons for each class
                button_group = QButtonGroup()
                button_group.setObjectName(class_name)
                button_group.setExclusive(False)
    
            self.radio_button_groups[class_name] = button_group       
            
            query_indicator = QSqlQuery(self.refuss_db)
            query_indicator.exec(f"SELECT * FROM IndicatorsLibrary WHERE IndicatorClass='{class_name}'")        
                  
            while query_indicator.next():
                indicator_id = query_indicator.value(0)
                indicator_name = query_indicator.value(4)

                if exclusive == 'YES':
                    radiobutton = QRadioButton(text = indicator_name, parent = frame)
                    radiobutton.setProperty("indicator_id", indicator_id)  # Set the IndicatorID property          
                    
                    radiobutton.clicked.connect(self.handle_radio_clicked)
                          
                    radiobutton.toggled.connect(lambda checked, id=indicator_id, class_id = class_id: self.handle_indicator_selection(id, checked, class_id))
                                                   
                    button_group.addButton(radiobutton)
                    frame_layout.addWidget(radiobutton)

                    # Check if the indicator is previously selected and set the radio button accordingly
                    if indicator_id in self.selected_indicators[class_id]:
                        radiobutton.setChecked(True)
                    
                else:
                    checkbox = QCheckBox(text = indicator_name, parent = frame)
                    checkbox.setProperty("indicator_id", indicator_id)  # Set the IndicatorID property
                    checkbox.stateChanged.connect(lambda state, id=indicator_id, class_id = class_id: self.handle_indicator_selection(id, state == 2, class_id))

                    frame_layout.addWidget(checkbox)
                    
                    # Check if the indicator is previously selected and set the checkbox accordingly
                    if indicator_id in self.selected_indicators[class_id]:
                        checkbox.setChecked(True)       
            
            layout.addWidget(frame)                              
            
    def handle_radio_clicked(self):
        sender = self.sender()
        button_group = self.radio_button_groups.get(sender.parent().objectName())  # Get the button group of the sender
        if sender.isChecked():
            # Uncheck all other radio buttons in the same group
            for button in button_group.buttons():
                if button is not sender:
                    button.setChecked(False)
                               
    def handle_indicator_selection(self, indicator_id, selected, class_id):
        if selected:
            if indicator_id not in self.selected_indicators[class_id]:
                self.selected_indicators[class_id].append(indicator_id)

        else:
            if indicator_id in self.selected_indicators[class_id]:
                self.selected_indicators[class_id].remove(indicator_id)
            
    def load_selected_indicators(self):
        selected_indicators = {}
        
        query = QSqlQuery(self.answer_db)
        query.exec("SELECT IndicatorID FROM IndicatorsSetup")

        while query.next():
            indicator_id = query.value(0)
            class_id = re.sub(r'\d', '', indicator_id)
            if class_id not in selected_indicators:
                selected_indicators[class_id] = []

            selected_indicators[class_id].append(query.value(0))

        return selected_indicators
 

    def closeEvent(self, event):
        # Perform add/delete operations in the ANSWERS_DB IndicatorsSetup table when the Settings window is closed
        self.update_indicators_in_answers_db()
        print(self.selected_indicators)
        event.accept()

    def update_indicators_in_answers_db(self):
            
        try:
            query = QSqlQuery(self.answer_db)
            query.exec("SELECT IndicatorID FROM IndicatorsSetup")
            existing_ids = set()
            while query.next():
                existing_ids.add(query.value(0))

            # Delete rows for deselected indicators
            for indicator in existing_ids:
                if indicator not in flatten_dict(self.selected_indicators):
                    query.exec(f"DELETE FROM IndicatorsSetup WHERE IndicatorID = '{indicator}'")
            
            # Add rows for new selecetd indicators
            for indicator in flatten_dict(self.selected_indicators):
                if indicator not in existing_ids:
                    if not query.exec(f"INSERT INTO IndicatorsSetup (IndicatorID) VALUES ('{indicator}')"):
                        print(query.lastQuery())
                        print("Error:", query.lastError().text())
                        
            # Commit the changes
            self.answer_db.transaction()
            if self.answer_db.commit():
                print("Update successful")
            else:
                print("Commit failed", self.answer_db.lastError().text())

        except Exception as e:
            print("Error:", str(e))
            
def flatten_dict(dict):
    flattened_list = [item for sublist in dict.values() for item in sublist]    
    return flattened_list
