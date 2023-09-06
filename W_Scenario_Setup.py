from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog, QSpacerItem, QSizePolicy, QDialog, QLabel, QScrollArea, QMessageBox, QFrame, QFormLayout, QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from functools import partial

from M_Fonts import MyFont

import re

class ExpandableElement(QWidget):
    formFieldTextChanged = Signal(str, str)  # Pass two strings: the label and the new text
    removedElement = Signal(str)
    changedLabel = Signal(str, str)
    
    def __init__(self, parent = None, default_label = "", ui_scenario_setup_instance = None):
        super().__init__(parent)
        self.ui_scenario_setup_instance = ui_scenario_setup_instance
        self.setup_ui(default_label)
        self.expanded = False

    def setup_ui(self, default_label):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create a frame for the header labels and a simple horizontal line
        header_frame = QFrame(self)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Create a horizontal layout for the header labels (self.label, self.edit_label, self.expand_label)
        header_labels_layout = QHBoxLayout()

        # Create a label for the element's text (self.label)
        self.label = QLabel(default_label, self)
        self.label.setFont(MyFont(10, True))

        # Create a horizontal spacer to push self.label to the left
        label_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Create a label for the ✏️ button (self.edit_label)
        self.edit_label = QLabel("✏️", self)
        self.edit_label.setAlignment(Qt.AlignCenter)
        self.edit_label.setCursor(Qt.PointingHandCursor)
        self.edit_label.mousePressEvent = self.edit_label_text

        # Create a label for the expand/collapse arrow (self.expand_label)
        self.expand_label = QLabel("▼", self)  # Use ▼ for down arrow and ▲ for up arrow
        self.expand_label.setAlignment(Qt.AlignCenter)
        self.expand_label.setCursor(Qt.PointingHandCursor)
        self.expand_label.mousePressEvent = self.toggle_properties

        # Add the labels to the header_labels_layout
        header_labels_layout.addWidget(self.label)
        header_labels_layout.addItem(label_spacer)
        header_labels_layout.addWidget(self.edit_label)
        header_labels_layout.addWidget(self.expand_label)

        header_layout.addLayout(header_labels_layout)

        # Create a simple horizontal line
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        header_layout.addWidget(line)

        self.layout.addWidget(header_frame)

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

        # Create a delete button for the element (only visible when expanded)
        self.delete_button = QPushButton("❌ Delete scenario", self)  # Symbol ❌ added
        self.delete_button.clicked.connect(self.delete_element)
        self.delete_button.hide()

        # Create a layout for the delete button and spacer
        header_button_layout = QHBoxLayout()
        header_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        header_button_layout.addWidget(self.delete_button)

        header_layout.addLayout(header_button_layout)

        self.layout.addWidget(header_frame)
        
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
            self.delete_button.show()
        else:
            self.expand_label.setText("▼")  # Change to down arrow when collapsed
            self.delete_button.hide()

    def edit_label_text(self, event):
        while True:
            new_label, ok = QInputDialog.getText(self, "Edit scenario name", "Enter new scenario name:")
            TextValidation, message = self.ui_scenario_setup_instance.ValidateAnswerText(new_label)
            if ok:
                if TextValidation:
                    old_scenario_name = self.label.text()
                    self.label.setText(new_label)
                    
                    self.changedLabel.emit(old_scenario_name, new_label)                  
                    break
                
                else:
                    warning_dialog = WarningDialog(f'{message}')
                    warning_dialog.exec()
            else:
                break

    def delete_element(self):
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

class Ui_ScenarioSetup(QMainWindow):
    
    windowClosed = Signal()
    
    def __init__(self, AnswersDatabase: QSqlDatabase):
        super().__init__()
        self.init_ui()
        self.setFixedSize(400, 500)

        # Initialize the database connection
        self.db = AnswersDatabase
        if not self.db.open():
            QMessageBox.critical(self, "Database Error", "Failed to open the database.")
            return
        
        # Create a QSqlTableModel
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("ScenarioSetup")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)        
       
        # Fetch the data from the table
        if not self.model.select():
            QMessageBox.critical(self, "Database Error", "Failed to fetch data from the table.")
            return
        # Load existing scenarios from the database
        self.load_existing_scenarios()
         
    def init_ui(self):
        
        self.setWindowTitle("Scenario set-up")
        
        # Create a central widget to hold the content
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a layout for the central widget
        self.layout = QVBoxLayout(central_widget)
        
        # Create a layout for the button
        button_layout = QHBoxLayout()
        
        # Add Element button to respective layout   
        add_element_button = QPushButton("➕ Add new scenario", central_widget)
        add_element_button.clicked.connect(self.add_element)
        button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(add_element_button)
        button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)
        
        # Define the layout for the scenarios (expandable elements)
        scenarios_container = QWidget()
        self.scenarios_layout = QVBoxLayout(scenarios_container)
        self.scenarios_layout.setSpacing(0)  # Adjust the spacing between elements
        
        # Create a scroll area for scenarios
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidget(scenarios_container)
        scroll_area.setFrameShape(QFrame.StyledPanel)
 
        # Add the scroll area to the layout
        self.layout.addWidget(scroll_area)
        
    def add_element(self):
        while True:
            new_label, ok = QInputDialog.getText(self, "Add scenario", "New scenario name:")
            AnswerValidation, message = self.ValidateAnswerText(new_label)
            if ok:
                if AnswerValidation:
                    expandable_element = ExpandableElement(default_label=new_label, ui_scenario_setup_instance=self)
                    self.AddScenarioToTable(new_label)                   
                    
                    # Connect the custom signal to update the scenario data in the database
                    expandable_element.formFieldTextChanged.connect(self.updateDatabaseField)
                    
                    # Connect the removedElement signal to the removeScenarioOfTable method
                    expandable_element.removedElement.connect(self.removeScenarioOfTable)
                    
                    # Connect the custom signal to update the scenario name in the database
                    expandable_element.changedLabel.connect(self.updateScenarioOfTable)                   
               
                    # Remove any existing vertical spacer (if present) before adding the new element
                    if self.scenarios_layout.count() >= 1:
                        item = self.scenarios_layout.itemAt(self.scenarios_layout.count() - 1)
                        self.scenarios_layout.removeItem(item)
                    
                    self.scenarios_layout.addWidget(expandable_element)
                    
                    # Add vertical spacer below the last added element
                    self.scenarios_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
                    break       
                else:
                    warning_dialog = WarningDialog(f'{message}')
                    warning_dialog.exec()
            else:
                break

    def load_existing_scenarios(self):
        query = QSqlQuery(self.db)
        query.prepare("SELECT ScenarioName, ScenarioSystemConfig, ScenarioRainfall, ScenarioOutfall, ScenarioComment FROM ScenarioSetup")
        query.exec_()

        while query.next():
            scenario_name = query.value(0)
            system_config = query.value(1)
            rainfall = query.value(2)
            outfall = query.value(3)
            comment = query.value(4)
        
            expandable_element = ExpandableElement(default_label=scenario_name, ui_scenario_setup_instance=self)
            
            # Connect the custom signal to update the database
            expandable_element.formFieldTextChanged.connect(self.updateDatabaseField)
            
            # Connect the removedElement signal to the removeScenarioOfTable method
            expandable_element.removedElement.connect(self.removeScenarioOfTable)
            
            # Connect the custom signal to update the scenario name in the database
            expandable_element.changedLabel.connect(self.updateScenarioOfTable)     

            # Loop through the form field labels and set the existing data
            for label, data in [("System configuration:", system_config),
                                ("Rainfall:", rainfall),
                                ("Outfall conditions:", outfall),
                                ("Comments:", comment)]:
                if label in expandable_element.form_fields:
                    expandable_element.form_fields[label].setText(data)

           
            # Remove any existing vertical spacer (if present) before adding the new element
            if self.scenarios_layout.count() >= 1:
                item = self.scenarios_layout.itemAt(self.scenarios_layout.count() - 1)
                self.scenarios_layout.removeItem(item)
            
            self.scenarios_layout.addWidget(expandable_element)
            
            # Add vertical spacer below the last added element
            self.scenarios_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def scenario_name_exists(self, scenario_name):
        # Check if a ScenarioName already exists in the database
        query = QSqlQuery(self.db)
        query.prepare("SELECT ScenarioName FROM ScenarioSetup WHERE ScenarioName = ?")
        query.addBindValue(scenario_name)
        query.exec()
        return query.next()

    def AddScenarioToTable(self, scenario_name):
        # Insert a new scenario into the database
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO ScenarioSetup (ScenarioName, ScenarioSystemConfig, ScenarioRainfall, ScenarioOutfall, ScenarioComment) "
                    "VALUES (?, '', '', '', '')")
        query.addBindValue(scenario_name)
        query.exec()

    def removeScenarioOfTable(self, scenario_name):
        # Remove existing scenario from the database
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM ScenarioSetup WHERE ScenarioName = ?")
        query.addBindValue(scenario_name)
        query.exec()       
    
    def updateScenarioOfTable(self, old_label, new_label):
        query = QSqlQuery(self.db)
        query.prepare(f"UPDATE ScenarioSetup SET ScenarioName = ? WHERE ScenarioName = ?")
        query.addBindValue(new_label)
        query.addBindValue(old_label)
        query.exec()         

    def ValidateAnswerText(self, text: str):
        if not text.strip():
            message = "Scenario name must not be empty!"
            return False, message
        elif not re.match(r'^[a-zA-Z0-9_]+$', text.strip()):
            message = "Scenario name must not have special characters!"
            return False, message
        elif self.scenario_name_exists(text):
            message = "Scenario name must be unique!"
            return False, message
        else:
            message = "OK!"
            return True, message

    # Define a single slot to update the database based on the label and text
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
        
        if db_column == "":
            return False
        else:
            scenario_name = self.sender().label.text()  # Get the scenario name from the element
            query = QSqlQuery(self.db)
            query.prepare(f"UPDATE ScenarioSetup SET {db_column} = ? WHERE ScenarioName = ?")
            query.addBindValue(text)
            query.addBindValue(scenario_name)
            query.exec() 
            
    def closeEvent(self, event):
        self.windowClosed.emit()
        event.accept()   
        
if __name__ == "__main__":
    app = QApplication([])
    main_window = Ui_ScenarioSetup()
    main_window.setFixedSize(400, 500)
    main_window.show()
    app.exec()