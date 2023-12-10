from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog, QSpacerItem, QSizePolicy, QDialog, QLabel, 
                               QMessageBox, QFrame, QFormLayout, QLineEdit, QCheckBox, QRadioButton, QLabel, QButtonGroup, QComboBox, QTableView, QMenu,
                               QStyledItemDelegate, QHeaderView, QScrollArea, QAbstractItemView
                               )

from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtGui import QAction

from M_IndicatorsSelection import (IndicatorsSelection, flatten_dict)
from M_OperateDatabases import updateB1TableUses

from W_SetupWindow import Ui_SetupWindow
from M_Fonts import MyFont

import pandas as pd

import re

class IndicatorsSelection(QWidget):
    
    IndicatorsSelectionChanged = Signal(pd.DataFrame)
    
    def __init__(self,
                 IndicatorsClassesLibrary: pd.DataFrame,
                 IndicatorsLibrary: pd.DataFrame,
                 IndicatorsSetup: pd.DataFrame,
                 study_db: QSqlDatabase):
        super().__init__()
        self.indicators_classes_library = IndicatorsClassesLibrary
        self.indicators_library = IndicatorsLibrary
        self.indicators_setup = IndicatorsSetup.copy(deep = True)
        self.study_db = study_db

        self.radio_button_groups = {}  # Dictionary to manage radio button groups for each class
                
        self.selected_indicators = load_selected_indicators(self.indicators_setup)  

        self.init_ui()

    def init_ui(self):                      
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        top_text = "Select performance indicators:"
        top_label = QLabel(top_text)
        top_label.setFont(MyFont(9, True))
        layout.addWidget(top_label)
                         
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
            
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

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
        
        self.update_indicators_state()
        self.IndicatorsSelectionChanged.emit(self.indicators_setup)
        #print(self.selected_indicators)

    def update_indicators_state(self, ):
        try:
            query = QSqlQuery(self.study_db)

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

            self.study_db.transaction()
            if not self.study_db.commit():
                print("Commit failed in update_indicators_state", self.study_db.lastError().text())

        except Exception as e:
            print("Error:", str(e))        

        for indicator_id, indicator in self.indicators_setup.iterrows():
            if indicator_id in flatten_dict(self.selected_indicators):
                self.indicators_setup.at[indicator_id, "SelectedState"] = 1
            else:
                self.indicators_setup.at[indicator_id, "SelectedState"] = 0
        #print(self.indicators_setup)
        
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

class PerformanceSetup(QWidget):
    
    def __init__(self,
                 IndicatorsClassesLibrary: pd.DataFrame,
                 IndicatorsLibrary: pd.DataFrame,
                 IndicatorsSetup: pd.DataFrame,
                 study_db: QSqlDatabase,
                 IndicatorsSelector: IndicatorsSelection):
        super().__init__()

        self.indicators_classes = IndicatorsClassesLibrary.copy(deep=True)
        self.indicators_library = IndicatorsLibrary.copy(deep=True)
        self.indicators_setup = IndicatorsSetup         #changes commited within the class will reflect on the original database
        self.indicator_selector = IndicatorsSelector
        
        self.study_db = study_db
    
        if not self.study_db.isValid():
            QMessageBox.critical(self, "Database Error", "Invalid database connection.")
            return
        if not self.study_db.isOpen():
            if not self.study_db.open():
                QMessageBox.critical(self, "Database Error", "Failed to open the database in Ui_PerformanceSetup.")
                return
        
        #get selected indicators dict
        self.selected_indicators = load_selected_indicators(self.indicators_setup) 
        self.classes_widgets = {}
        
        self.setupUi() 
        
        # Load exisiting classes of the database to self.classes_widgets and create respective custom expandable widgets
        # do not forget the deaulft widget of "No indicators selected within this category"
        self.load_classes_setup()
               
        # Verify which class has selected indicators and which indicators selected within each class
        # show widget of selecteced indicators and hide the others by calling the self.classes_widgets .show() or .hide()
        # this function is also called when the user closes the indicators selection window
        self.filter_selected_indicators()

        self.indicator_selector.IndicatorsSelectionChanged.connect(self.update_indicators_setup)
    
    def setupUi(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        top_text = "Set indicators settings:"
        top_label = QLabel(top_text)
        top_label.setFont(MyFont(9, True))
        layout.addWidget(top_label)
        
        self.scroll_content_widget = QWidget()
        self.indicators_scroll_layout = QVBoxLayout(self.scroll_content_widget) # to add things
        #self.indicators_scroll_layout.setContentsMargins(10, 0, 20, 0)
        self.indicators_scroll_layout.setSpacing(10)
        self.indicators_scroll_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
                
        self.indicators_scroll_area = QScrollArea()
        self.indicators_scroll_area.setWidget(self.scroll_content_widget)
        self.indicators_scroll_area.setWidgetResizable(True)
        self.indicators_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.indicators_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.indicators_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.indicators_scroll_area.setFrameShape(QFrame.StyledPanel)         
    
        layout.addWidget(self.indicators_scroll_area)

    def load_classes_setup(self):

        for class_id, setting in self.indicators_classes.iterrows():
            class_name = setting['IndicatorClassName']
            
            expandable_element = ExpandableClassSetup(label_text = class_name)
            
            SRP_check = False
            
            for indicator_id, indicator in self.indicators_setup.iterrows():
                indicator_class_id = re.sub(r'\d', '', indicator_id)
                                
                if indicator_class_id == class_id:
                    indicator_widget = self.create_indicators_setup_widgets(indicator_id)
                    if SRP_check == False or indicator_class_id != "SRP":
                        expandable_element.properties_layout.addWidget(indicator_widget)
                        self.classes_widgets[class_id] = expandable_element
                    if indicator_class_id == "SRP":
                        SRP_check = True
                    # If one of SRP indicators is selected, only show the unit info once (evit repeating)
                    # if indicator_id in ["SRP1", "SRP2", "SRP3"]:
                    #     break   
            expandable_element.setVisible(True)
            
            # Add widget to layout
            self.indicators_scroll_layout.insertWidget(self.indicators_scroll_layout.count() - 1, expandable_element)

        # debugging purpose - do not delete
        # for i in range(self.indicators_scroll_layout.count()):
        #     element = self.indicators_scroll_layout.itemAt(i)
        #     widget = element.widget()
        #     layout = element.layout()
        #     print(f"Item {i}: Widget - {widget}, Layout - {layout}")           
                 
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
        model = QSqlTableModel(db = self.study_db)
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
            self.CustomBuilding = B1UsesSetupTable(self.study_db)
            indicator_layout.addWidget(self.CustomBuilding)
            # CustomWaterHeigts = B1WaterHeightsSetupTable(self.study_db)
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
                   
    def update_indicators_setup(self, IndicatorsSetup: pd.DataFrame):
        self.indicators_setup = IndicatorsSetup
        self.filter_selected_indicators()
        
    def filter_selected_indicators(self):
        
        self.selected_indicators = load_selected_indicators(self.indicators_setup)

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

class ExpandableClassSetup(QWidget):  
    def __init__(self,  label_text: str):
        super().__init__()
        self.setup_ui(label_text)
        self.expanded = False

    def setup_ui(self, label_text):
        # layout = QVBoxLayout(self)
        # layout.setContentsMargins(0, 0, 0, 0)

        # Create a frame for the header labels and a simple horizontal line
        #Main_frame = QFrame(self)
        Main_layout = QVBoxLayout(self)
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

        # Create a widget for the expandable properties
        self.properties_widget = QWidget(self)
        # self.properties_widget.setVisible(True)
        self.properties_layout = QVBoxLayout(self.properties_widget)
        self.properties_layout.setContentsMargins(0, 0, 0, 0)
        
        self.default_label = QLabel("No performance indicator selected within this class.", self)
        self.default_label.setObjectName("DefaultLabel")
        self.properties_layout.addWidget(self.default_label)
        # self.default_label.setVisible(True)

        self.properties_layout.setSpacing(5)  # Adjust vertical spacing as needed
        
        Main_layout.addWidget(self.properties_widget)
        
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
    
    #SET THESE SIGNALS ON THE MAIN WINDOW TO UPDATE THE B1 TABLES ACCORDINGLY
    building_uses_modified = Signal(str, str)

    def __init__(self, study_db: QSqlDatabase):
        super().__init__()
        self.db = study_db

        # Create models for tables
        self.createTable_UserUses()

    def createTable_UserUses(self):
        # Ensure that the database connection is open before creating the model
        if not self.db.isOpen():
            QMessageBox.critical(self, "Database Error", "ANSWERS_DB is not open. - B1UsesSetup")
            return

        # Define and set the model for UserUses_Table
        self.user_uses_model = QSqlTableModel(db = self.db)
        self.user_uses_model.setTable("B1UsesSetup")
        self.user_uses_model.setEditStrategy(QSqlTableModel.OnManualSubmit)

       # Fetch the data from the table
        if not self.user_uses_model.select():
            QMessageBox.critical(self, "Database Error", "Failed to fetch data from the table B1UsesSetup.")
            return

        self.user_uses_model.setHeaderData(0, Qt.Horizontal, "Custom building use")
        self.user_uses_model.setHeaderData(1, Qt.Horizontal, "Total size")
        self.user_uses_model.setHeaderData(2, Qt.Horizontal, "Methodology corresponding use")

        self.setModel(self.user_uses_model)
        self.resizeColumnsToContents()
        self.resizeColumnsToContents()
        self.setEditTriggers(QTableView.AllEditTriggers)

        # Set the delegate for the third column to use ComboBox
        self.setItemDelegateForColumn(2, B1ComboBoxDelegate(self))
        #self.setItemDelegate(B1ComboBoxDelegate(self))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Create context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
 

        self.user_uses_model.dataChanged.connect(self.handleDataChanged)

    def handleDataChanged(self, top_left, bottom_right, roles):
        # This is called after the user has finished editing a cell
        if top_left.column() == 0:
            row = top_left.row()
            old_value = self.retrieveOldValue(row, "CostumUse")
            new_value = self.user_uses_model.data(top_left, Qt.DisplayRole)
            if old_value != new_value:
                self.user_uses_model.submitAll()
                self.user_uses_model.database().commit() 
                self.building_uses_modified.emit(old_value, new_value)
               
    def retrieveOldValue(self, row, column_name):
        query = QSqlQuery(self.db)
        if query.exec(f"SELECT {column_name} FROM B1UsesSetup WHERE rowid = {row+1}"):
            if query.next():
                return query.value(0)
        return None

    def addNewRow(self):
        # Add a new row to the table
        row = self.user_uses_model.rowCount()

        record = self.user_uses_model.record()
        record.setValue("CostumUse", "Edit here...")

        #self.user_uses_model.insertRow(row)
        self.user_uses_model.insertRecord(row, record)

        #self.user_uses_model.submitAll()
        self.reset()
        self.user_uses_model.submitAll()
        self.user_uses_model.select()
        self.user_uses_model.database().commit() 
        self.building_uses_modified.emit('', record)
   
    def removeCurrentRow(self):
        # Remove the current row from the table
        current_row = self.clicked_index.row()
        old_value = self.user_uses_model.data(self.clicked_index, Qt.DisplayRole)
        if current_row >= 0:
            self.user_uses_model.removeRow(current_row)
        self.user_uses_model.submitAll()
        self.user_uses_model.select()
        self.user_uses_model.database().commit()
        self.building_uses_modified.emit(old_value, '')
   
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
        model.submitAll()
        model.database().commit()
        

    # def sizeHint(self, option, index):
    #     if index.column() == 2:  # Adjust the size hint for the ComboBox in the third column
    #         return QSize(100, 30)
    #     return super().sizeHint(option, index)

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