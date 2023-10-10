from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog, QSpacerItem, QSizePolicy, QDialog, QLabel, 
                               QScrollArea, QMessageBox, QFrame, QFormLayout, QLineEdit, QCheckBox, QRadioButton, QLabel, QButtonGroup
                               )

from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from functools import partial

import M_IndicatorsSelection
from W_SetupWindow import Ui_SetupWindow
from M_Fonts import MyFont

import sys
import re

class Ui_PerformanceSetup(QMainWindow):
    
    windowClosed = Signal()
    
    def __init__(self, REFUSS_Database: QSqlDatabase, Answers_Database: QSqlDatabase):
        super().__init__()
        self.ui = Ui_SetupWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Performace Setup")
        
        self.refuss_db = REFUSS_Database
        self.answers_db = Answers_Database
        self.existing_scenarios = []
        self.selected_indicators = None

        if not self.answers_db.isValid():
            QMessageBox.critical(self, "Database Error", "Invalid database connection.")
            return
        if not self.answers_db.isOpen():
            if not self.answers_db.open():
                QMessageBox.critical(self, "Database Error", "Failed to open the database in Ui_PerformanceSetup.")
                return
  
        # Create a QSqlTableModel for scenarios
        self.scenarios_model = QSqlTableModel(self, self.answers_db)
        self.scenarios_model.setTable("ScenarioSetup")
        self.scenarios_model.setEditStrategy(QSqlTableModel.OnFieldChange)  
        # Fetch the data from the table
        if not self.scenarios_model.select():
            QMessageBox.critical(self, "Database Error", "Failed to fetch data from the ScenarioSetup table in Create a QSqlTableModel.")
            return

        # Create a QSqlTableModel for scenarios
        self.indicators_model = QSqlTableModel(self, self.answers_db)
        self.indicators_model.setTable("InsidicatorsSetup")
        self.indicators_model.setEditStrategy(QSqlTableModel.OnFieldChange)  
        # Fetch the data from the table
        if not self.indicators_model.select():
            QMessageBox.critical(self, "Database Error", "Failed to fetch data from the InsidicatorsSetup table in Create a QSqlTableModel.")
            return
        
        # Set top labels font
        self.ui.scenarios_label.setFont(MyFont(12, True))
        self.ui.indicators_label.setFont(MyFont(12, True))
        
        #
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
        self.ui.scenarios_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.scenarios_scroll_area.setFrameShape(QFrame.StyledPanel)
        
        self.ui.indicators_scroll_area.setWidget(indicators_scroll_widget)
        self.ui.indicators_scroll_area.setWidgetResizable(True)
        self.ui.indicators_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.indicators_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.indicators_scroll_area.setFrameShape(QFrame.StyledPanel)
      
        # Load existing scenarios from the database
        self.load_existing_scenarios()
        
        # Load exisiting indicators from the database
        self.load_existing_indicators()
        
        # Populate with indicators classes and default -> se nenhum indicador estiver selecionado mostrar "No indicator of this class is selected."
        self.create_indicators_setup_structure()
        
        # Read the selected indicators, if any, and show respective widgets
        self.update_indicators_setup_structure()
        
        
        #Set add buttons actions
        self.ui.add_scenario_button.clicked.connect(self.add_scenario)
        self.ui.add_indicator_button.clicked.connect(self.add_indicator)
    
    def add_indicator(self):
        
        #verify/test if IndicatorsSelectionWindow must be 'self.'
        IndicatorsSelectionWindow = M_IndicatorsSelection.IndicatorsSelection(self.refuss_db, self.answers_db)
        IndicatorsSelectionWindow.show()
        self.selected_indicators = IndicatorsSelectionWindow.selected_indicators
    
    
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

    def load_existing_scenarios(self):      
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

class ExpandableIndicatorSetup(QWidget):
    formFieldTextChanged = Signal(str, str)  # Pass two strings: the label and the new text
    removedElement = Signal(str)
    changedLabel = Signal(str, str)
    
    def __init__(self,  label_text: str, Indicator_setup: Ui_PerformanceSetup):
        super().__init__()
        self.indicator_setup = Indicator_setup
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
        
        # Create a label for the expand/collapse arrow (self.expand_label)
        self.expand_label = QLabel("▼", self)  # Use ▼ for down arrow and ▲ for up arrow
        self.expand_label.setAlignment(Qt.AlignCenter)
        self.expand_label.setCursor(Qt.PointingHandCursor)
        self.expand_label.mousePressEvent = self.toggle_properties

        # Add the labels to the header_labels_layout
        header_labels_layout.addWidget(self.label)
        header_labels_layout.addItem(label_spacer)
        
        header_labels_layout.addWidget(self.expand_label)

        header_layout.addLayout(header_labels_layout)

        # Create a simple horizontal line
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        header_layout.addWidget(line)

        layout.addWidget(header_frame)

        # Create a widget for the expandable properties (e.g., labels and input fields)
        self.properties_widget = QWidget(self)
        self.properties_layout = QVBoxLayout(self.properties_widget)

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
            new_label, ok = QInputDialog.getText(self, "Edit scenario name", "Enter new scenario name:")
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

