from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog, QSpacerItem, QSizePolicy, QDialog, QLabel, 
                               QMessageBox, QFrame, QFormLayout, QLineEdit, QCheckBox, QRadioButton, QLabel, QButtonGroup, QComboBox, QTableView, QMenu,
                               QStyledItemDelegate, QHeaderView
                               )

from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtGui import QAction

from M_IndicatorsSelection import (IndicatorsSelection, flatten_dict)
from M_OperateDatabases import updateB1Table

from W_SetupWindow import Ui_SetupWindow
from M_Fonts import MyFont

import pandas as pd

import re

class Ui_PerformanceSetup(QMainWindow):
    
    windowClosed = Signal()
    
    def __init__(self,
                 IndicatorsClassesLibrary: pd.DataFrame,
                 IndicatorsLibrary: pd.DataFrame,
                 ScenarioSetup: pd.DataFrame,
                 IndicatorsSetup: pd.DataFrame,
                 Answers_Database: QSqlDatabase):
        super().__init__()
        self.ui = Ui_SetupWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Performace Setup")
        
        self.indicators_classes = IndicatorsClassesLibrary.copy(deep=True)
        self.indicators_library = IndicatorsLibrary.copy(deep=True)
        self.scenario_setup = ScenarioSetup             #changes commited within the class will reflect on the original database
        self.indicators_setup = IndicatorsSetup         #changes commited within the class will reflect on the original database
        
        self.answers_db = Answers_Database
    
        if not self.answers_db.isValid():
            QMessageBox.critical(self, "Database Error", "Invalid database connection.")
            return
        if not self.answers_db.isOpen():
            if not self.answers_db.open():
                QMessageBox.critical(self, "Database Error", "Failed to open the database in Ui_PerformanceSetup.")
                return
  
        # Set top labels font
        self.ui.scenarios_label.setFont(MyFont(12, True))
        self.ui.indicators_label.setFont(MyFont(12, True))
        
        # Set scoll layouts
        scenarios_scroll_widget = QWidget()
        indicators_scroll_widget = QWidget()
        
        self.scenarios_scroll_layout = QVBoxLayout(scenarios_scroll_widget)
        self.scenarios_scroll_layout.setSpacing(0)
        self.scenarios_scroll_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.indicators_scroll_layout = QVBoxLayout(indicators_scroll_widget)
        self.indicators_scroll_layout.setSpacing(0)
        self.indicators_scroll_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Create a scroll area for scenarios and indicators layouts
        self.ui.scenarios_scroll_area.setWidget(scenarios_scroll_widget)
        self.ui.scenarios_scroll_area.setWidgetResizable(True)
        self.ui.scenarios_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.scenarios_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.scenarios_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.scenarios_scroll_area.setFrameShape(QFrame.StyledPanel)
        
        self.ui.indicators_scroll_area.setWidget(indicators_scroll_widget)
        self.ui.indicators_scroll_area.setWidgetResizable(True)
        self.ui.indicators_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.indicators_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.indicators_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.indicators_scroll_area.setFrameShape(QFrame.StyledPanel)

        self.existing_scenarios = self.scenario_setup.index.tolist()
        self.selected_indicators = load_selected_indicators(self.indicators_setup)
        self.classes_widgets = {}
        
        '''
        Deal with Scenarios
        '''
        # Load existing scenarios from the database to self.existing_scenarios and create respective custom expandable widgets
        self.load_scenarios_setup()
        
        #Set add scenario button action
        self.ui.add_scenario_button.clicked.connect(self.add_scenario)
        
        '''
        Deal with Indicators
        '''
        # Load exisiting classes of the database to self.classes_widgets and create respective custom expandable widgets
        # do not forget the deaulft widget of "No indicators selected within this category"
        self.load_classes_setup()
               
        # Verify which class has selected indicators and which indicators selected within each class
        # show widget of selecteced indicators and hide the others by calling the self.classes_widgets .show() or .hide()
        # this function is also called when the user closes the indicators selection window
        self.set_selected_indicators()
                
        #Set indicator button action
        self.ui.add_indicator_button.clicked.connect(self.set_indicators)

    def set_indicators(self):
        self.IndicatorsSelectionWindow = IndicatorsSelection(self.indicators_classes,
                                                        self.indicators_library,
                                                        self.indicators_setup,
                                                        self.answers_db)
        self.IndicatorsSelectionWindow.windowClosed.connect(self.filter_selected_indicators)
        self.IndicatorsSelectionWindow.show()
        
    def add_scenario(self):
        while True:
            new_label, ok = QInputDialog.getText(self, "Add scenario", "New scenario name:")
            AnswerValidation, message = ValidateAnswerText(new_label, self.existing_scenarios)
            if ok:
                if AnswerValidation:
                    expandable_element = ExpandableScenarioSetup(label_text = new_label, Performance_setup = self)
                    
                    self.AddScenarioToDatabase(new_label)                   
                    
                    # Connect the custom signal to update the scenario data in the database
                    expandable_element.formFieldTextChanged.connect(self.updateDatabaseField)
                    
                    # Connect the removedElement signal to the removeScenarioFromDatabase method
                    expandable_element.removedElement.connect(self.removeScenarioFromDatabase)
                    
                    # Connect the custom signal to update the scenario name in the database
                    expandable_element.changedLabel.connect(self.updateScenarioOfTable)                   

                    self.scenarios_scroll_layout.insertWidget(self.scenarios_scroll_layout.count() - 1, expandable_element)
                    
                    break       
                else:
                    warning_dialog = WarningDialog(f'{message}')
                    warning_dialog.exec()
            else:
                break       

    def load_scenarios_setup(self):      
        query = QSqlQuery(self.answers_db)
        
        if query.exec("SELECT * FROM ScenarioSetup"):
            while query.next():
                scenario_id = query.value(0)
                scenario_name = query.value(1)
                system_config = query.value(2)
                rainfall = query.value(3)
                outfall = query.value(4)
                comment = query.value(5)

                self.existing_scenarios.append(scenario_name)
                
                expandable_element = ExpandableScenarioSetup(label_text = scenario_name, Performance_setup = self)
                
                # Connect the custom signal to update the database
                expandable_element.formFieldTextChanged.connect(self.updateDatabaseField)
                
                # Connect the removedElement signal to the removeScenarioFromDatabase method
                expandable_element.removedElement.connect(self.removeScenarioFromDatabase)
                
                # Connect the custom signal to update the scenario name in the database
                expandable_element.changedLabel.connect(self.updateScenarioOfTable)     

                # Loop through the form field labels and set the existing data
                for label, data in [("System configuration:", system_config),
                                    ("Rainfall:", rainfall),
                                    ("Outfall conditions:", outfall),
                                    ("Comments:", comment)]:
                    if label in expandable_element.form_fields:
                        expandable_element.form_fields[label].setText(data)
    
                self.scenarios_scroll_layout.insertWidget(self.scenarios_scroll_layout.count() - 1, expandable_element)

        else:
            error_message = query.lastError().text()
            print(f"Query execution failed: {error_message} in load_existing_scenarios")            

    def load_classes_setup(self):

        for class_id, setting in self.indicators_classes.iterrows():
            class_name = setting['IndicatorClassName']
            
            expandable_element = ExpandableClassSetup(label_text = class_name, Performance_setup = self)
            self.classes_widgets[class_id] = expandable_element
            
            SRP_check = False
            
            for indicator_id, indicator in self.indicators_setup.iterrows():
                indicator_class_id = re.sub(r'\d', '', indicator_id)
                                
                if indicator_class_id == class_id:
                    indicator_widget = self.create_indicators_setup_widgets(indicator_id)
                    if SRP_check == False or indicator_class_id != "SRP":
                        self.classes_widgets[class_id].properties_layout.addWidget(indicator_widget)
                    if indicator_class_id == "SRP":
                        SRP_check = True
                    # If one of SRP indicators is selected, only show the unit info once (evit repeating)
                    # if indicator_id in ["SRP1", "SRP2", "SRP3"]:
                    #     break   
            
            # Add widget to layout
            self.indicators_scroll_layout.insertWidget(self.indicators_scroll_layout.count() - 1, expandable_element)
                      
    def create_indicators_setup_widgets(self, indicator_id):
        indicator_widget = QWidget()
        indicator_widget.setObjectName(indicator_id)
        indicator_layout = QVBoxLayout(indicator_widget)
        indicator_layout.setContentsMargins(0, 0, 0, 0)
        
        referece_text = self.indicators_library.at[indicator_id, "Reference"]
        indicator_text = f'Methodology: {referece_text}'
        indicator_label = QLabel(indicator_text)
        indicator_label.setFont(MyFont(10, True))
        indicator_layout.addWidget(indicator_label)
        
        possible_units = self.indicators_library.at[indicator_id, "PossibleUnits"].split("; ")
        
        unit_layout = QHBoxLayout()
        indicator_layout.addLayout(unit_layout)

        #set the model
        model = QSqlTableModel(db = self.answers_db)
        model.setTable("IndicatorsSetup")
        model.select()
        
        # Find the corresponding unit in the model
        model_column_name = "SelectedUnit"
                            
        if len(possible_units) > 1:
            unit_text = 'Select the data unit:'
            unit_label = QLabel(unit_text)
            unit_layout.addWidget(unit_label)
            
            unit_combo_box = QComboBox()
            
            unit_combo_box.addItems(possible_units)
            
            model_row = find_model_row(model, 'IndicatorID', indicator_id)
            
            if model_row >= 0:
                # Get the unit value from the model
                initial_unit_value = model.data(model.index(model_row, model.fieldIndex(model_column_name)))
                if initial_unit_value and initial_unit_value in possible_units:
                    initial_index = possible_units.index(initial_unit_value)
                    unit_combo_box.setCurrentIndex(initial_index)
                else:
                    update_model(indicator_id, possible_units[0], model, model_column_name)

            unit_combo_box.currentIndexChanged.connect(lambda index: update_model(indicator_id, possible_units[index], model, model_column_name))
            unit_layout.addWidget(unit_combo_box)
            
        else:
            update_model(indicator_id, possible_units[0], model, model_column_name)
            unit_text = f'Data unit: {possible_units[0]}'
            unit_label = QLabel(unit_text)
            unit_layout.addWidget(unit_label)   
                
        if indicator_id in ["P1", "P2", "V1"]:
            pass
        elif indicator_id in ["B1"]:
            CustomBuilding = B1UsesSetupTable(self.answers_db)
            indicator_layout.addWidget(CustomBuilding)
            # CustomWaterHeigts = B1WaterHeightsSetupTable(self.answers_db)
            # indicator_layout.addWidget(CustomWaterHeigts)
        elif indicator_id in ["SRP1", "SRP2", "SRP3"]:
            pass
            
        return indicator_widget               

    def set_selected_indicators(self):
        self.indicators_classes.sort_values(by = "Order")
        
        SRP_control = False

        for class_id, _ in self.indicators_classes.iterrows():
            
            layout = self.classes_widgets[class_id].properties_layout
                        
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget().objectName() in flatten_dict(self.selected_indicators):
                    item.widget().show()
                    
                    if item.widget().objectName() in ["SRP1", "SRP2", "SRP3"] and not SRP_control:
                        SRP_control = True
                    elif item.widget().objectName() in ["SRP1", "SRP2", "SRP3"] and SRP_control:
                        item.widget().hide()                        
                else:
                    item.widget().hide()
            
            if class_id not in self.selected_indicators.keys():
                self.classes_widgets[class_id].default_label.show()     
                   
    def filter_selected_indicators(self, indicators_setup: pd.DataFrame):
    
        self.indicators_setup = indicators_setup
        self.selected_indicators = load_selected_indicators(indicators_setup)

        self.indicators_classes.sort_values(by = "Order")
        
        SRP_control = False

        for class_id, _ in self.indicators_classes.iterrows():
            
            layout = self.classes_widgets[class_id].properties_layout
                        
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget().objectName() in flatten_dict(self.selected_indicators):
                    item.widget().show()
                    
                    if item.widget().objectName() in ["SRP1", "SRP2", "SRP3"] and not SRP_control:
                        SRP_control = True
                    elif item.widget().objectName() in ["SRP1", "SRP2", "SRP3"] and SRP_control:
                        item.widget().hide()                        
                else:
                    item.widget().hide()
            
            if class_id not in self.selected_indicators.keys():
                self.classes_widgets[class_id].default_label.show()        

    
    def AddScenarioToDatabase(self, scenario_name):
        # Insert a new scenario into the database
        query = QSqlQuery(self.answers_db)
        
        if query.exec(f"INSERT INTO ScenarioSetup (ScenarioName) VALUES ('{scenario_name}')"):
            self.answers_db.commit()  # Commit changes
            self.existing_scenarios.append(scenario_name)
        else:
            error_message = query.lastError().text()
            print(f"Query execution failed: {error_message}")
            print(f"Database error type: {query.lastError().type()}")
            print(f"Database error driver text: {query.lastError().driverText()}")
            print(f"Database error database text: {query.lastError().databaseText()}")

    def updateDatabaseField(self, label, text):
        db_column = ""
        if label == "Rainfall:":
            db_column = "ScenarioRainfall"
        elif label == "System configuration:":
            db_column = "ScenarioSystemConfig"
        elif label == "Outfall conditions:":
            db_column = "ScenarioOutfall"
        elif label == "Comments:":
            db_column = "ScenarioComment"
        
        if db_column != "":
            scenario_name = self.sender().label.text()  # Get the scenario name from the element
            query = QSqlQuery(self.answers_db)
            query.prepare(f"UPDATE ScenarioSetup SET {db_column} = ? WHERE ScenarioName = ?")
            query.addBindValue(text)
            query.addBindValue(scenario_name)
            if query.exec():
                self.answers_db.commit()  # Commit changes
            else:
                error_message = query.lastError().text()
                print(f"Query execution failed: {error_message} in updateDatabaseField")

    def removeScenarioFromDatabase(self, scenario_name):
        # Remove existing scenario from the database
        query = QSqlQuery(self.answers_db)
        if query.exec(f"DELETE FROM ScenarioSetup WHERE ScenarioName = '{scenario_name}'"):
            self.answers_db.commit()  # Commit changes
            self.existing_scenarios.remove(scenario_name)
        else:
            error_message = query.lastError().text()
            print(f"Query execution failed: {error_message} in removeScenarioFromDatabase")
            
    def updateScenarioOfTable(self, old_label, new_label):
        query_ID = QSqlQuery(self.answers_db)
        query_ID.prepare("SELECT ScenarioID FROM ScenarioSetup WHERE ScenarioName = ?")
        query_ID.addBindValue(old_label)
        query_ID.exec()
        
        if query_ID.next():
            scenario_id = query_ID.value(0)
            
            query_update = QSqlQuery(self.answers_db)
            query_update.prepare(f"UPDATE ScenarioSetup SET ScenarioName = ? WHERE ScenarioID = ?")
            query_update.addBindValue(new_label)
            query_update.addBindValue(scenario_id)
            query_update.exec()         
    
    def closeEvent(self, event):
        updateB1Table(self.answers_db)
        self.windowClosed.emit()
        event.accept()      

                                             
def ValidateAnswerText(text: str, list: list):
    if not text.strip():
        message = "Scenario name must not be empty!"
        return False, message
    elif not re.match(r'^[a-zA-Z0-9_]+$', text.strip()):
        message = "Scenario name must not have special characters!"
        return False, message
    elif text in list:
        message = "Scenario name must be unique!"
        return False, message
    else:
        message = "OK!"
        return True, message
        
class ExpandableScenarioSetup(QWidget):
    formFieldTextChanged = Signal(str, str)  # Pass two strings: the label and the new text
    removedElement = Signal(str)
    changedLabel = Signal(str, str)
    
    def __init__(self,  label_text: str, Performance_setup: Ui_PerformanceSetup):
        super().__init__()
        self.performance_setup = Performance_setup
        self.setup_ui(label_text)
        self.expanded = False

    def setup_ui(self, label_text):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a frame for the header labels and a simple horizontal line
        header_frame = QFrame(self)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Create a horizontal layout for the header labels (self.label, self.edit_label, self.expand_label)
        header_labels_layout = QHBoxLayout()

        # Create a label for the element's text (self.label)
        self.label = QLabel(label_text, self)
        self.label.setFont(MyFont(10, True))

        # Create a horizontal spacer to push self.label to the left
        label_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Create a delete button for the element (only visible when expanded)
        delete_label = QLabel("❌", self)
        delete_label.setAlignment(Qt.AlignCenter)
        delete_label.setCursor(Qt.PointingHandCursor)
        delete_label.mousePressEvent = self.delete_element
        
        # Create a label for the ✏️ button (self.edit_label)
        edit_label = QLabel("✏️", self)
        edit_label.setAlignment(Qt.AlignCenter)
        edit_label.setCursor(Qt.PointingHandCursor)
        edit_label.mousePressEvent = self.edit_label_text

        # Create a label for the expand/collapse arrow (self.expand_label)
        self.expand_label = QLabel("▼", self)  # Use ▼ for down arrow and ▲ for up arrow
        self.expand_label.setAlignment(Qt.AlignCenter)
        self.expand_label.setCursor(Qt.PointingHandCursor)
        self.expand_label.mousePressEvent = self.toggle_properties

        # Add the labels to the header_labels_layout
        header_labels_layout.addWidget(self.label)
        header_labels_layout.addItem(label_spacer)
        header_labels_layout.addWidget(delete_label)
        header_labels_layout.addWidget(edit_label)
        header_labels_layout.addWidget(self.expand_label)

        header_layout.addLayout(header_labels_layout)

        # Create a simple horizontal line
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        header_layout.addWidget(line)

        layout.addWidget(header_frame)

        # Create a widget for the expandable properties (e.g., labels and input fields)
        self.properties_widget = QWidget(self)
        self.properties_layout = QFormLayout(self.properties_widget)

        # Add labels and input fields for the form
        labels = ["Rainfall:", "System configuration:", "Outfall conditions:", "Comments:"]
        self.form_fields = {}

        for label_text in labels:
            label = QLabel(label_text, self)
            input_field = QLineEdit(self)
            self.form_fields[label_text] = input_field
            self.form_fields[label_text].textChanged.connect(lambda text, label_text = label_text: self.formFieldTextChanged.emit(label_text, text))
            self.properties_layout.addRow(label, input_field)

        self.properties_layout.setVerticalSpacing(5)  # Adjust vertical spacing as needed
        self.properties_widget.hide()
        
        header_layout.addWidget(self.properties_widget)

        layout.addWidget(header_frame)
        
    def updateDatabase(self, label_text):
        scenario_name = self.label.text()
        
        if label_text == "Rainfall:":
            table_col = "ScenarioRainfall"
        elif label_text == "System configuration:":
            table_col = "ScenarioSystemConfig"
        elif label_text == "Outfall conditions:":
            table_col = "ScenarioOutfall"
        elif label_text == "Comments:":
            table_col = "ScenarioComment"
        
        # Update the "ScenarioRainfall" column in the database
        query = QSqlQuery(self)
        query.prepare(f"UPDATE ScenarioSetup SET {table_col} = ? WHERE ScenarioName = ?")
        query.addBindValue(label_text)
        query.addBindValue(scenario_name)
        query.exec()
        
    def toggle_properties(self, event):
        self.expanded = not self.expanded
        self.properties_widget.setVisible(self.expanded)
        if self.expanded:
            self.expand_label.setText("▲")  # Change to up arrow when expanded
        else:
            self.expand_label.setText("▼")  # Change to down arrow when collapsed

    def edit_label_text(self, event):
        while True:
            new_label, ok = QInputDialog.getText(self, "Edit scenario name", "Enter scenario name:")
            TextValidation, message = ValidateAnswerText(new_label, self.performance_setup.existing_scenarios)
            if ok:
                if TextValidation:
                    old_scenario_name = self.label.text()
                    self.performance_setup.existing_scenarios.remove(old_scenario_name)
                    
                    self.performance_setup.existing_scenarios.append(new_label)
                    self.label.setText(new_label)
                    
                    self.changedLabel.emit(old_scenario_name, new_label)                  
                    break
                
                else:
                    warning_dialog = WarningDialog(f'{message}')
                    warning_dialog.exec()
            else:
                break

    def delete_element(self, event):
        # Show a confirmation dialog
        confirmation = QMessageBox.question(
            self,
            "Delete scenario",
            f"Are you sure you want to delete the scenario '{self.label.text()}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        # If the user confirms the deletion, remove the element
        if confirmation == QMessageBox.Yes:
            self.removedElement.emit(self.label.text())
            self.performance_setup.scenarios_scroll_layout.removeWidget(self)
            self.deleteLater()

class ExpandableClassSetup(QWidget):
    formFieldTextChanged = Signal(str, str)  # Pass two strings: the label and the new text
    removedElement = Signal(str)
    changedLabel = Signal(str, str)
    
    def __init__(self,  label_text: str, Performance_setup: Ui_PerformanceSetup):
        super().__init__()
        self.performance_setup = Performance_setup
        self.setup_ui(label_text)
        self.expanded = False

    def setup_ui(self, label_text):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a frame for the header labels and a simple horizontal line
        header_frame = QFrame(self)
        Main_layout = QVBoxLayout(header_frame)
        Main_layout.setContentsMargins(0, 0, 0, 0)
        Main_layout.setSpacing(0)

        # Create a horizontal layout for the header labels (self.label, self.edit_label, self.expand_label)
        header_labels_layout = QHBoxLayout()

        # Create a label for the element's text (self.label)
        self.label = QLabel(label_text, self)
        self.label.setFont(MyFont(10, True))

        # Create a horizontal spacer to push self.label to the left
        label_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Create a label for the expand/collapse arrow (self.expand_label)
        self.expand_label = QLabel("▼", self)  # Use ▼ for down arrow and ▲ for up arrow
        self.expand_label.setAlignment(Qt.AlignCenter)
        self.expand_label.setCursor(Qt.PointingHandCursor)
        self.expand_label.mousePressEvent = self.toggle_properties

        # Add the labels to the header_labels_layout
        header_labels_layout.addWidget(self.label)
        header_labels_layout.addItem(label_spacer)
        
        header_labels_layout.addWidget(self.expand_label)

        Main_layout.addLayout(header_labels_layout)

        # Create a simple horizontal line
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        Main_layout.addWidget(line)

        layout.addWidget(header_frame)

        # Create a widget for the expandable properties
        self.properties_widget = QWidget(self)
        self.properties_layout = QVBoxLayout(self.properties_widget)
        self.properties_layout.setContentsMargins(0, 0, 0, 0)
        
        self.default_label = QLabel("No performance indicator selected within this class.", self)
        self.default_label.setObjectName("DefaultLabel")
        self.properties_layout.addWidget(self.default_label)
        self.default_label.hide()

        self.properties_layout.setSpacing(5)  # Adjust vertical spacing as needed
        self.properties_widget.hide()
        
        Main_layout.addWidget(self.properties_widget)

        layout.addWidget(header_frame)
        
    def updateDatabase(self, label_text):
        scenario_name = self.label.text()
        
        if label_text == "Rainfall:":
            table_col = "ScenarioRainfall"
        elif label_text == "System configuration:":
            table_col = "ScenarioSystemConfig"
        elif label_text == "Outfall conditions:":
            table_col = "ScenarioOutfall"
        elif label_text == "Comments:":
            table_col = "ScenarioComment"
        
        # Update the "ScenarioRainfall" column in the database
        query = QSqlQuery(self)
        query.prepare(f"UPDATE ScenarioSetup SET {table_col} = ? WHERE ScenarioName = ?")
        query.addBindValue(label_text)
        query.addBindValue(scenario_name)
        query.exec()
        
    def toggle_properties(self, event):
        self.expanded = not self.expanded
        self.properties_widget.setVisible(self.expanded)
        if self.expanded:
            self.expand_label.setText("▲")  # Change to up arrow when expanded
        else:
            self.expand_label.setText("▼")  # Change to down arrow when collapsed

class WarningDialog(QDialog):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Warning")
        layout = QVBoxLayout(self)
        label = QLabel(f"{text}", self)
        layout.addWidget(label)

        button_container = QWidget(self)  # Create a container for the button
        button_layout = QHBoxLayout(button_container)  # Create a layout for the button container

        ok_button = QPushButton("OK", self)
        ok_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set size policy for the button
        ok_button.clicked.connect(self.accept)

        button_layout.addWidget(ok_button)
        layout.addWidget(button_container)  # Add the button container to the main layout

class B1UsesSetupTable(QTableView):
    def __init__(self, answers_db: QSqlDatabase):
        super().__init__()
        self.answer_db = answers_db
        
        #self.verifyDatabaseTable()
        # Create models for tables
        self.createTable_UserUses()

    def createTable_UserUses(self):
        # Ensure that the database connection is open before creating the model
        if not self.answer_db.isOpen():
            QMessageBox.critical(self, "Database Error", "ANSWERS_DB is not open. - B1UsesSetup")
            return

        # Define and set the model for UserUses_Table
        self.user_uses_model = QSqlTableModel(db = self.answer_db)
        self.user_uses_model.setTable("B1UsesSetup")
        self.user_uses_model.setEditStrategy(QSqlTableModel.OnFieldChange)

       # Fetch the data from the table
        if not self.user_uses_model.select():
            QMessageBox.critical(self, "Database Error", "Failed to fetch data from the table B1UsesSetup.")
            return

        self.user_uses_model.setHeaderData(0, Qt.Horizontal, "Custom building use")
        self.user_uses_model.setHeaderData(1, Qt.Horizontal, "Total size")
        self.user_uses_model.setHeaderData(2, Qt.Horizontal, "Methodology corresponding use")

        self.setModel(self.user_uses_model)
        self.resizeColumnsToContents()
        self.setEditTriggers(QTableView.AllEditTriggers)

        # Set the delegate for the third column to use ComboBox
        self.setItemDelegate(B1ComboBoxDelegate(self))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Create context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        table = self.sender()  # Identify the table that triggered the event

        if table == self:
            model = self.user_uses_model
            add_label = "Add New Use"
            remove_label = "Remove Current Use"
        else:
            return

        global_pos = table.viewport().mapToGlobal(pos)
        self.clicked_index = table.indexAt(pos)

        context_menu = QMenu(self)
        add_new_use_action = QAction(add_label, self)
        remove_current_use_action = QAction(remove_label, self)

        context_menu.addAction(add_new_use_action)
        context_menu.addAction(remove_current_use_action)

        # Connect context menu actions to slots
        add_new_use_action.triggered.connect(lambda: self.addNewRow())
        remove_current_use_action.triggered.connect(lambda: self.removeCurrentRow())

        context_menu.exec(global_pos)

    def addNewRow(self):
        # Add a new row to the table
        row = self.user_uses_model.rowCount()

        record = self.user_uses_model.record()
        record.setValue("CostumUse", "Edit here...")

        #self.user_uses_model.insertRow(row)
        self.user_uses_model.insertRecord(row, record)

        #self.user_uses_model.submitAll()

        self.reset()
        self.user_uses_model.select()
        
    def removeCurrentRow(self):
        # Remove the current row from the table
        current_row = self.clicked_index.row()
        if current_row >= 0:
            self.user_uses_model.removeRow(current_row)
        self.user_uses_model.select()

    # def verifyDatabaseTable(self):
    #     """criar tabela na database se não existir B1UsesSetup que vai ter apenas uma linha com as colunas:
    #         CustomUses : lista separada por ; com os tipos de edificio introduzidos pelo utilizador
    #         Residential, Commercial, Industrial (onde serão colocados os tipos definidos pelo utilizador corresponde)
    #         WaterDepths: lista separada por ; com os valores de profundidade de agua introduzidos pelo utilizador
    #     """
    #     if not self.answer_db.isOpen():
    #         QMessageBox.critical(None, "Database Error", "ANSWERS_DB is not open.")
    #     else:
    #         # Criar a tabela se ela não existir
    #         query = QSqlQuery(self.answer_db)
    #         if not query.exec("CREATE TABLE IF NOT EXISTS B1UsesSetup ("
    #                 "CostumUse TEXT, "
    #                 "TotalSize NUMERIC, "
    #                 "MethodologyClass TEXT)"
    #             ):
    #             print(f"Failed to create table B1Settings. {query.lastError().text()}")

class B1ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.options = ["Residential", "Commercial", "Industrial"]

    def createEditor(self, parent, option, index):
        if index.column() == 2:  # Only create an editor for the third column
            editor = QComboBox(parent)
            editor.addItems(self.options)
            return editor
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        if index.column() == 2:  # Set the current index of the ComboBox based on the item data
            current_data = index.data(Qt.DisplayRole)
            if current_data in self.options:
                editor.setCurrentIndex(self.options.index(current_data))
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if index.column() == 2:  # Set the item data based on the current index of the ComboBox
            model.setData(index, editor.currentText(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)

    # def sizeHint(self, option, index):
    #     if index.column() == 2:  # Adjust the size hint for the ComboBox in the third column
    #         return QSize(100, 30)
    #     return super().sizeHint(option, index)

def load_selected_indicators(IndicatorsSetup: pd.DataFrame):
    selected_indicators = {}
    
    selected_df = IndicatorsSetup[IndicatorsSetup["SelectedState"] == 1]
    
    for indicator_id, indicator in selected_df.iterrows():
        class_id = re.sub(r'\d', '', indicator_id)
        if class_id not in selected_indicators:
            selected_indicators[class_id] = []
        selected_indicators[class_id].append(indicator_id)
        
    return selected_indicators

def update_model(IndicatorID, content, model, model_column):
    
    model_row = find_model_row(model, 'IndicatorID', IndicatorID)
    
    if model_row >= 0:
        model.setData(model.index(model_row, model.fieldIndex(model_column)), content)
        model.submitAll()

def find_model_row(model, model_column_name, search_name):
    # Find the row in the model where the model_column_name value is equal to search_name
    row = -1
    for i in range(model.rowCount()):
        if model.data(model.index(i, model.fieldIndex(model_column_name))) == search_name:
            row = i
            break
    return row   