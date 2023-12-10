from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog, QSpacerItem, QSizePolicy, QDialog, QLabel, 
                               QScrollArea, QMessageBox, QFrame, QFormLayout, QLineEdit, QCheckBox, QRadioButton, QLabel, QButtonGroup
                               )

from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from functools import partial

from M_Fonts import MyFont


import M_OperateDatabases
import pandas as pd

import sys
import re

class IndicatorsSelection(QMainWindow):
    
    windowClosed = Signal(pd.DataFrame)
    
    def __init__(self,
                 IndicatorsClassesLibrary: pd.DataFrame,
                 IndicatorsLibrary: pd.DataFrame,
                 IndicatorsSetup: pd.DataFrame,
                 answers_db: QSqlDatabase):
        super().__init__()
        self.indicators_classes_library = IndicatorsClassesLibrary
        self.indicators_library = IndicatorsLibrary
        self.indicators_setup = IndicatorsSetup.copy(deep = True)
        self.answers_db = answers_db

        self.radio_button_groups = {}  # Dictionary to manage radio button groups for each class
                
        self.selected_indicators = load_selected_indicators(self.indicators_setup)  
               
        self.setWindowModality(Qt.WindowModal) 
        self.init_ui()

    def init_ui(self):
        # self.setWindowTitle("Performance Indicators Selection")
                        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
                              
        # Create the UI elements and check if indicators are already selected               
        for class_id, class_prop in self.indicators_classes_library.iterrows():
            class_name = class_prop['IndicatorClassName']
            exclusive = class_prop['Exclusive']
            
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
            
            for indicator_id, indicator in self.indicators_library.iterrows():
                
                if indicator["IndicatorClass"] == class_name:
                
                    indicator_name = indicator["ShowName"]

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
 
    def closeEvent(self, event):
        # Perform add/delete operations in the ANSWERS_DB IndicatorsSetup table when the Settings window is closed
        self.update_indicators_state()
        print(self.selected_indicators)
        self.windowClosed.emit(self.indicators_setup)
        event.accept()

    def update_indicators_state(self):
            
        try:
            query = QSqlQuery(self.answers_db)

            selected_ids = flatten_dict(self.selected_indicators)
            # Create a dictionary where keys are IndicatorIDs and values are 'True' or 'False'
            selected_states = {indicator_id: 1 if indicator_id in selected_ids else 0 for indicator_id in self.indicators_library.index.to_list()}

            # Execute the SQL UPDATE statement for each IndicatorID
            for indicator_id, selected_state in selected_states.items():
                query.prepare("UPDATE IndicatorsSetup SET SelectedState = :selectedState WHERE IndicatorID = :indicatorID")
                query.bindValue(":selectedState", selected_state)
                query.bindValue(":indicatorID", indicator_id)
                if not query.exec():
                    print("Update failed:", query.lastError().text())
                    break

            self.answers_db.transaction()
            if self.answers_db.commit():
                print("Update successful")
            else:
                print("Commit failed", self.answers_db.lastError().text())

        except Exception as e:
            print("Error:", str(e))        

        for indicator_id, indicator in self.indicators_setup.iterrows():
            if indicator_id in flatten_dict(self.selected_indicators):
                self.indicators_setup.at[indicator_id, "SelectedState"] = 1
            else:
                self.indicators_setup.at[indicator_id, "SelectedState"] = 0
        
        print(self.indicators_setup)
        
def load_selected_indicators(IndicatorsSetup: pd.DataFrame):
    selected_indicators = {}
    
    selected_df = IndicatorsSetup[IndicatorsSetup["SelectedState"] == 1]
    
    for indicator_id, indicator in selected_df.iterrows():
        class_id = re.sub(r'\d', '', indicator_id)
        if class_id not in selected_indicators:
            selected_indicators[class_id] = []
        selected_indicators[class_id].append(indicator_id)


    return selected_indicators
 
def flatten_dict(dict):
    flattened_list = [item for sublist in dict.values() for item in sublist]    
    return flattened_list