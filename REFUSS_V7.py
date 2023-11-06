from operator import index
import sys
import os
import pandas as pd
from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton, QTreeWidget, QTreeWidgetItem,
                            QVBoxLayout, QButtonGroup, QRadioButton, QWidget,
                            QCheckBox, QLabel, QTextEdit, QStackedWidget, QLineEdit, QComboBox,
                            QScrollArea, QSizePolicy, QSpacerItem, QFileDialog, QTableView, QDialogButtonBox,
                            QMessageBox, QDialog, QStyledItemDelegate, QHeaderView, QMenu, QAbstractItemView,
                            QAbstractScrollArea, QStyleOptionButton, QStyle, QTableWidgetItem, QFrame, QHBoxLayout, QLayout)
from PySide6.QtCore import Qt, Signal, QEvent, QAbstractTableModel, QModelIndex
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtGui import QStandardItemModel, QValidator, QIntValidator, QAction

from W_MainPage_V5 import Ui_MainWindow
from W_SetupWindow_ui import Ui_HazardSetup
from W_WelcomeWindow import Ui_WelcomeWindow
from W_B1_Setup import Ui_SettingB1
from M_PerformanceSetup_2 import Ui_PerformanceSetup
from W_SetupWindow import Ui_SetupWindow
from M_WeightSetup import Ui_WeightSetup

import M_OperateDatabases
import M_Operate_GUI_Elements
import M_PlotGraphs
import M_ResilienceCalculus
import M_IndicatorsSelection
import M_HazardClasses

from M_Fonts import MyFont

from functools import partial

import atexit

class HazardSetupDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HazardSetupDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):

        # #set the spacial case for the "Buildings Damage (B1)" hazard
        # if index.column() == 1 and index.sibling(index.row(), 0).data() == "Buildings Damage (B1)":
        #     # Use the custom button-like delegate for column 1 when the text in column 0 is "Buildings Damage (B1)"
        #     editor = QPushButton("Setup", parent)
        #     editor.clicked.connect(self.openB1SetupWindow)  # Connect the button click to a custom slot
        #     return editor

        # Create a QComboBox editor for column 0 and 1 and its options
        if index.column() in (0,1):
            editor = QComboBox(parent)
            if index.column() == 0:
                editor.addItems(M_OperateDatabases.fetch_table_from_database(REFUSS_DB, "HazardLibrary")["ShowName"])
            elif index.column() == 1:
                editor.addItems(["%", "Area"])
            return editor

        # Default case: Use the base editor for other columns (regular text cell)
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        # Set the current value of the editor based on the model's data
        value = index.model().data(index, Qt.EditRole)
        if isinstance(editor, QComboBox):
            editor.setCurrentText(value)
        # No need to handle QPushButton here since we don't use currentText()

    def setModelData(self, editor, model, index):
        if isinstance(editor, QComboBox):
            # Update the model's data when the editor value changes for QComboBoxes
            model.setData(index, editor.currentText(), Qt.EditRole)

    def editorEvent(self, event, model, option, index):
        # Override editorEvent to handle custom button click event
        if event.type() == QEvent.MouseButtonRelease and index.column() == 1 and index.sibling(index.row(), 0).data() == "Buildings Damage (B1)":
            # Custom button was clicked, update the model with "Custom" value
            model.setData(index, "Custom", Qt.EditRole)
            return True  # Return True to indicate that the event has been handled

        return super().editorEvent(event, model, option, index)

    # def openB1SetupWindow(self):
    #     self.B1SetupWindow = B1SettingWindow()
    #     #self.B1SetupWindow.windowClosed.connect(self.onSetupWindowClosed)
    #     self.B1SetupWindow.setWindowModality(Qt.WindowModal)
    #     self.B1SetupWindow.setWindowFlags(self.B1SetupWindow.windowFlags() | Qt.WindowStaysOnTopHint)
    #     self.B1SetupWindow.show()

class GeneralizedIndicatorModel(QAbstractTableModel):
    def __init__(self, database, indicators, scenario_id, column_names, row_names=None):
        super(GeneralizedIndicatorModel, self).__init__()
        self.database = database
        self.indicators = indicators  # List of indicator IDs
        self.scenario_id = scenario_id
        self.column_names = column_names
        self.row_names = row_names if row_names else indicators
        self.dirty = False
        self.data_dict = self.fetch_data()  # {(indicator_id, scenario_id): {column_name: value}}
        #self.fetch_data()
        
    def fetch_data(self):
        data_dict = {}
        for indicator_id in self.indicators:
            table_name = indicator_id  # Use IndicatorID as the table name
            query = QSqlQuery(self.database)
            query.prepare(f"SELECT * FROM {table_name} WHERE ScenarioID = :scenario_id")
            query.bindValue(":scenario_id", self.scenario_id)
            if query.exec():
                while query.next():
                    record = query.record()
                    for column_name in self.column_names:
                        value = record.value(column_name)
                        data_dict[(indicator_id, self.scenario_id)] = data_dict.get((indicator_id, self.scenario_id), {})
                        data_dict[(indicator_id, self.scenario_id)][column_name] = value
            else:
                print("Query execution failed:", query.lastError().text())
                error = self.database.lastError().text()
                print(f'Database error details: {error}')
        return data_dict

        
    def flags(self, index):
        flags = super().flags(index)
        flags |= Qt.ItemIsEditable  # Add the Qt.ItemIsEditable flag
        return flags

    def rowCount(self, parent):
        return len(self.indicators)

    def columnCount(self, parent):
        return len(self.column_names)

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            indicator_id = self.indicators[index.row()]
            column_name = self.column_names[index.column()]
            value = self.data_dict.get((indicator_id, self.scenario_id), {}).get(column_name, "")
            return value if role == Qt.DisplayRole else str(value)
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return str(self.row_names[section])
            elif orientation == Qt.Horizontal:
                return str(self.column_names[section])
        return None

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            indicator_id = self.indicators[index.row()]
            column_name = self.column_names[index.column()]
            
            key = (indicator_id, self.scenario_id)
            
            if key not in self.data_dict.keys():
                self.data_dict[key] = {}  # Create a dictionary for the indicator/scenario pair
                
                
            table_name = indicator_id  # Use IndicatorID as the table name
            # Start the transaction
            self.database.transaction()
            
            query = QSqlQuery(self.database)
            query.prepare(f"UPDATE {table_name} SET `{column_name}` = :value WHERE ScenarioID = :scenario_id")
            query.bindValue(":value", float(value))
            query.bindValue(":scenario_id", self.scenario_id)
            
            if not query.exec():
                print("Query execution failed:", query.lastError().text())
                # Handle update failure
                self.database.rollback()
                return False

            if not self.database.commit():
                print(f'Error on database commitment for table {table_name}')
                error = self.database.lastError().text()
                print(f'Database error details: {error}')
                return False

            key = (indicator_id, self.scenario_id)

            if key not in self.data_dict.keys():
                self.data_dict[key] = {}

            self.data_dict[key][column_name] = value
            self.dirty = True
            self.dataChanged.emit(index, index)
            return True
        return False

    def isDirty(self):
        return self.dirty

    def commit(self):
        if self.dirty:
            if self.database.open():
                self.database.transaction()

                try:
                    for row in range(self.rowCount()):
                        for col in range(1, self.columnCount()):
                            indicator_id = self.indicators[row]
                            column_name = self.column_names[col]
                            new_value = self.data_dict.get((indicator_id, self.scenario_id), {}).get(column_name)
                            table_name = indicator_id

                            query = QSqlQuery(self.database)
                            query.prepare(
                                f"""
                                UPDATE {table_name}
                                SET Value = ?
                                WHERE ScenarioID = ? AND ColumnName = ?
                                """
                            )
                            query.addBindValue(new_value)
                            query.addBindValue(self.scenario_id)
                            query.addBindValue(column_name)

                            if not query.exec():
                                self.database.rollback()
                                return False

                    if not self.database.commit():
                        print(f'Error on database commitment for table {table_name}')
                        return False
                    else:
                        self.dirty = False
                except:
                    self.database.rollback()
                    raise

# Custom Delegate for Button-like Appearance
class ButtonLikeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ButtonLikeDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        # Check if the conditions are met to draw the cell as a button
        if index.column() == 1 and index.sibling(index.row(), 0).data() == "Buildings Damage (B1)":
            # Draw the cell as a button
            button_option = QStyleOptionButton()
            button_option.rect = option.rect
            button_option.state = option.state
            button_option.palette = option.palette
            button_option.text = index.data(Qt.DisplayRole)
            QApplication.style().drawControl(QStyle.CE_PushButton, button_option, painter)
        else:
            # Draw the cell as regular text cell
            super().paint(painter, option, index)

class IntRangeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator = QIntValidator(1, 10, self)

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if index.column() == 1:
            editor.setValidator(self.validator)
        return editor

class DecimalZeroOneDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(FloatValidator(0, 1, 3))  # Adjust the range and precision as needed
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, float(value))

class FloatValidator(QValidator):
    def __init__(self, bottom, top, decimals):
        super().__init__()
        self.bottom = bottom
        self.top = top
        self.decimals = decimals

    def validate(self, input, pos):
        try:
            value = float(input)
            if self.bottom <= value <= self.top:
                return (QValidator.Acceptable, input, pos)
            else:
                return (QValidator.Invalid, input, pos)
        except ValueError:
            return (QValidator.Invalid, input, pos)

    # class PerformanceSqlTableModel(QSqlTableModel):

    #     def flags(self, index):
    #         flags = super().flags(index)
    #         if index.column() == 0:  # Make the first column read-only
    #             flags &= ~Qt.ItemFlag.ItemIsEditable
    #         return flags

class CustomSqlTableModel(QSqlTableModel):
    def __init__(self, column_names, parent=None):
        super().__init__(parent)
        self.column_names = column_names

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section < len(self.column_names):
                return self.column_names[section]
        return QSqlTableModel.headerData(self, section, orientation, role)

class PerformanceSqlTableModel(QSqlTableModel):
    def __init__(self, db=None, non_editable_columns=None):
        if db is not None:
            super().__init__(db=db)
        else:
            super().__init__()
        self.non_editable_columns = non_editable_columns or []

    def flags(self, index):
        flags = super().flags(index)
        if index.column() in self.non_editable_columns:
            flags &= ~Qt.ItemIsEditable
        return flags

class ConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmation")
        self.setModal(True)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        message_label = QLabel("Are you sure?")
        layout.addWidget(message_label)

        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

class WelcomeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WelcomeWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("REFUSS Tool")

        self.ui.NewButton.clicked.connect(self.newAnalysis)
        self.ui.LoadButton.clicked.connect(self.loadAnalysis)

    def newAnalysis(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save New Analysis", dir = os.getcwd(), filter = '*.db')
        if save_path:
            self.accept()  # Accept the dialog and return the save path
            self.fileSelected = save_path
            self.Status = "New"
            self.close()

    def loadAnalysis(self):
        load_path, _ = QFileDialog.getOpenFileName(self, "Load Analysis", dir = os.getcwd(), filter = '*.db')
        if load_path:
            self.accept()  # Accept the dialog and return the load path
            self.fileSelected = load_path
            self.Status = "Old"
            self.close()

class SetupWindow(QMainWindow):

    windowClosed = Signal(str)

    def __init__(self, SetupTable):
        super().__init__()
        self.ui = Ui_HazardSetup()
        self.ui.setupUi(self)

        #Set the headers
        if SetupTable == "HazardSetup":
            Label = "HAZARD SETUP"
            self.setWindowTitle("Hazard Setup Window")
        elif SetupTable == "ScenarioSetup":
            Label = "SCENARIO SETUP"
            self.setWindowTitle("Scenario Setup Window")

        self.SetupOption = SetupTable

        self.ui.SetupLabel.setText(Label)
        self.ui.SetupLabel.setFont(MyFont(12, True))

        self.populate_table(SetupTable)

        #Customize the TableView
        self.ui.SetupTableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.ui.SetupTableView.verticalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.ui.SetupTableView.resizeRowsToContents()

        #Set actions for buttons
        self.ui.Add_BT.clicked.connect(self.add_row)
        self.ui.Del_BT.clicked.connect(self.delete_row)
        self.ui.Close_BT.clicked.connect(self.closeSetupWindow)

    def populate_table(self, SetupCase):
        # Ensure that the database connection is open before creating the model
        if not ANSWERS_DB.isOpen():
            QMessageBox.critical(self, "Database Error", "ANSWERS_DB is not open.")
            return

        # Create a QSqlTableModel
        self.model = QSqlTableModel(db=ANSWERS_DB)
        self.model.setTable(SetupCase)
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        # Fetch the data from the table
        if not self.model.select():
            QMessageBox.critical(self, "Database Error", "Failed to fetch data from the table.")
            return

        # Set the headers
        if SetupCase == "HazardSetup":
            headers = ["Hazard Name", "Unit of hazard classification", "Comment"]

            hazard_delegate = HazardSetupDelegate()

            self.ui.SetupTableView.setItemDelegate(hazard_delegate)

        elif SetupCase == "ScenarioSetup":
            headers = ["Scenario Name", "System config.", "Rainfall", "Outfall Cond.", "Comment"]

        for i, header in enumerate(headers):
            self.model.setHeaderData(i, Qt.Horizontal, header)

        self.ui.SetupTableView.setModel(self.model)
        self.ui.SetupTableView.resizeColumnsToContents()
        self.ui.SetupTableView.setEditTriggers(QTableView.AllEditTriggers)

    def add_row(self):
        # Get the number of rows in the model
        num_rows = self.model.rowCount()

        # Insert a new record at the end of the model
        record = self.model.record()
        if self.SetupOption == "HazardSetup":
            record.setValue("HazardName", "SelectHazard")
        elif self.SetupOption == "ScenarioSetup":
            record.setValue("ScenarioName", "NewScenario")

        self.model.insertRecord(num_rows, record)

        # # Manually update the view to reflect the changes
        # self.model.select()

        # Optional: Scroll to the newly added row
        self.ui.SetupTableView.scrollToBottom()

        # Reset the view to reflect the changes
        self.ui.SetupTableView.reset()

    def delete_row(self):
        # Get the selected row indatabasedices
        selection_model = self.ui.SetupTableView.selectionModel()
        selected_rows = selection_model.selectedRows()

        # Confirm deletion with the user
        if self.SetupOption == "HazardSetup":
            message = "Are you sure you want to delete the selected hazard?"
        elif self.SetupOption == "ScenarioSetup":
            message = "Are you sure you want to delete the selected scenario?"

        reply = QMessageBox.question(self, "Delete Row", f"{message}", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        # Remove the rows from the model
        else:
            for index in selected_rows:
                self.model.removeRow(index.row())

        # Submit changes to the database
        if not self.model.submitAll():
            QMessageBox.critical(self, "Error", "Failed to delete row(s) from the database.")

        # Manually update the view to reflect the changes
        self.model.select()

    def closeSetupWindow(self):
        if self.SetupOption == "HazardSetup":
            # Check if the mandatory column has been filled
            mandatory_column_index = 1  # Number of hazard classes

            for row in range(self.model.rowCount()):
                value = self.model.index(row, mandatory_column_index).data()
                if not value:
                    QMessageBox.critical(self, "Error", "Must select a Hazard Unit!")
                    return

        confirm_dialog = QMessageBox.question(self, "Confirmation", "Do you want to close the window?", QMessageBox.Yes | QMessageBox.No)
        if confirm_dialog == QMessageBox.Yes:
            self.windowClosed.emit(self.SetupOption)
            self.model.select()
            self.close()

    def savechanges(self):
        #self.model.submitAll()
        #self.closeSetupWindow()
        pass

class MainWindow(QMainWindow):
    def __init__(self, Status):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("REFUSS Tool - V0")

        #Set inital MainWindowPage
        self.ui.MenuWidget.setHidden(True)
        self.ui.LeftMenuWidget.setHidden(True)
        self.ui.menu_btn.setChecked(True)
        self.ui.menu_btn_2.setChecked(True)
        self.ui.home_btn_2.setChecked(True)
        self.ui.BodyWidget.setCurrentIndex(0)
        self.ui.TitlesWidget.setCurrentIndex(0)

        # Set associated function to left menu buttons
        self.ui.home_btn.clicked.connect(self.home_btn_toggled)
        self.ui.home_btn_2.clicked.connect(self.home_btn_toggled)
        self.ui.urbanprofile_btn.clicked.connect(self.urbanprofile_btn_toggled)
        self.ui.urbanprofile_btn_2.clicked.connect(self.urbanprofile_btn_toggled)
        self.ui.stormprofile_btn.clicked.connect(self.stormprofile_btn_toggled)
        self.ui.stormprofile_btn_2.clicked.connect(self.stormprofile_btn_toggled)
        self.ui.functional_btn.clicked.connect(self.functional_btn_toggled)
        self.ui.functional_btn_2.clicked.connect(self.functional_btn_toggled)
        self.ui.performance_btn.clicked.connect(self.performance_btn_toggled)
        self.ui.performance_btn_2.clicked.connect(self.performance_btn_toggled)
        self.ui.dashboard_btn.clicked.connect(self.dashboard_btn_toggled)
        self.ui.dashboard_btn_2.clicked.connect(self.dashboard_btn_toggled)

        # Set menubar bar actions
        self.ui.actionSave.triggered.connect(self.savefile)
        self.ui.actionSave_As.triggered.connect(self.savefile)
        self.ui.actionLoad.triggered.connect(self.loadfile)

        # Get tables' content from REFUSS_DB
        refuss_contents = M_OperateDatabases.getREFUSSDatabase(REFUSS_DB)
        self.dimensions = refuss_contents[0]
        self.objectives = refuss_contents[1].set_index("ObjectiveID")
        self.criteria = refuss_contents[2].set_index("CriteriaID")
        self.metrics = refuss_contents[3].set_index("MetricID")
        self.metric_options = refuss_contents[4].set_index("MetricID")
        self.indicators = {'indicators_classes': refuss_contents[5].set_index("IndicatorClassID"),
                           'indicators_library': refuss_contents[6].set_index("IndicatorID")}

        # Verify answers database
        M_OperateDatabases.verifyAnswersDatabase(ANSWERS_DB)
        M_OperateDatabases.setConsequencesTables(REFUSS_DB, ANSWERS_DB)
        
        """
        Set Tree Widgets
        """
        # Define and populate the Tree Widgets with the Objectives and Criteria
        self.ui.Functional_list = self.findChild(QTreeWidget, "Functional_list")
        self.ui.Performance_list = self.findChild(QTreeWidget, "Performance_list")
        self.populate_dimension_tree(self.ui.Functional_list, 1)  # Assuming dimension 1 corresponds to Functional_list
        self.populate_dimension_tree(self.ui.Performance_list, 2)  # Assuming dimension 2 corresponds to Performance_list

        # Romeve small arrow on the left of the tree widget parent item
        self.ui.Functional_list.setRootIsDecorated(False)

        # Do not expand tree widgets parent items when clicking
        self.ui.Performance_list.setItemsExpandable(False)

        # Expand tree widgets by default
        M_Operate_GUI_Elements.expand_all_tree_items(self.ui.Functional_list)
        M_Operate_GUI_Elements.expand_all_tree_items(self.ui.Performance_list)

        # Connect the signals from the TreeWidgets to navigate through the pages
        self.ui.Functional_list.itemClicked.connect(self.navigate_to_page)
        self.ui.Performance_list.itemClicked.connect(self.navigate_to_page)

        """
        Set Main Widgets
        """
        #Clean default MainWidgets pages
        M_Operate_GUI_Elements.CleanStackedWidget(self.ui.Functional_MainWidget)
        M_Operate_GUI_Elements.CleanStackedWidget(self.ui.Performance_MainWidget)

        # Populate the Functional_MainWidget with objectives and criteria from REFUSS_DB
        self.populate_with_objective_pages()
        self.populate_with_criterion_pages()

        """
        Address Status (New or Old)
        """      
        if Status == "New":       
            # If new anaylisis, makes sure to delete its existing answers and save over existing database
            M_OperateDatabases.FillNewAnswersDatabase(ANSWERS_DB, self.metrics)
            M_OperateDatabases.FillNewWeightsDatabase(REFUSS_DB, ANSWERS_DB)
            M_OperateDatabases.createIndicatorsSetup(REFUSS_DB, ANSWERS_DB)
            
        if Status == "Old":
            # Load available functional answers from ANSWERS_DB into the GUI
            load_FunctionalAnswers(self.ui.Functional_MainWidget)

        """
        Initialize Performance/Indicators related global variables
        """
        # The scenario pages layout will have a widget for all the possible Classes and Indicators
        # If the Class has a selected indicator the respective Widget of the class is shown,
            # otherwise it is hidden
        # If the indicator within a given class is selected, the respective widget is shown,
            # otherwise it is hidden
        # When calculating Performance Resilience, only selceted indicators must be considered
        
        self.update_performance_dataframes()
        
        # Initialize dictionary containing as keys the IndicatorsClasses from the ConsequencesLibrary
            # and as values the selected IndicatorsIDs of each class (generaly, classes only allow 1 indicator)
            # Updated when the IndicatorSelection window is closed      
        self.selected_indicators = M_IndicatorsSelection.load_selected_indicators(self.IndicatorsSetup)
        
        # Initialize list to save the existing scanerio IDs
            # Updated when the SETUP window is closed
        self.existing_scenarios = self.ScenarioSetup.index.tolist()

        # Initialize dictionary containg as keys the scenarioIDs
            # and as values a dict containing the IndicatorIDs as keys and
            # the respective models as value, to be later accessed and easily updated
        # Created when initializing the GUI and updated a new scenario is created/deleted
        self.scenario_models = {}

        # Initialize dictionary containing as keys the ScenarioIDs
            # and as values a dict containing the IndicatorIDs as keys
            # and the respective widget,  to be later accessed and allow to hide/show the widgets
            # according to the selected IndicatorIDs
            # e.g. {'ScenarioID1': {'IndicatorID1': widget1, 'IndicatorID2': widget2, etc.}}
        # Created when initializing the GUI and updated when selected_indicators changes
            # by showing/hiding the widgets of the selected/deselected indicators
        self.scenario_pages = {}
        
        # Functional Dimension buttons
        self.ui.WeightsSU_btn.clicked.connect(self.OpenWeightsWindow)
        
        """
        Set Performance/Indicators GUI elements
        """

        # Populate the Performance_MainWidget with scenarios from ANSWERS_DB
        self.populate_scenario_pages()

        # Performance Dimension button
        self.ui.ScenarioSU_btn.clicked.connect(self.OpenSetupWindow)

    def update_performance_dataframes(self):
        self.IndicatorsLibrary = M_OperateDatabases.fetch_table_from_database(REFUSS_DB, "IndicatorsLibrary")
        self.IndicatorsLibrary.set_index("IndicatorID", inplace=True)
        
        self.IndicatorsClassesLibrary = M_OperateDatabases.fetch_table_from_database(REFUSS_DB, "IndicatorsClassesLibrary")
        self.IndicatorsClassesLibrary.set_index("IndicatorClassID", inplace=True)
        
        self.ScenarioSetup = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "ScenarioSetup")
        self.ScenarioSetup.set_index("ScenarioID", inplace=True)
        
        self.IndicatorsSetup = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "IndicatorsSetup")
        self.IndicatorsSetup.set_index("IndicatorID", inplace=True)
        
        self.selected_indicators = M_IndicatorsSelection.load_selected_indicators(self.IndicatorsSetup)        
        
    def OpenSetupWindow(self):
        self.ScenarioSetupWindow = Ui_PerformanceSetup(self.IndicatorsClassesLibrary,
                                                  self.IndicatorsLibrary,
                                                  self.ScenarioSetup,
                                                  self.IndicatorsSetup,
                                                  ANSWERS_DB)
        self.ScenarioSetupWindow.setWindowModality(Qt.WindowModal)
        self.ScenarioSetupWindow.setWindowFlags(self.ScenarioSetupWindow.windowFlags() | Qt.WindowStaysOnTopHint)
        self.ScenarioSetupWindow.windowClosed.connect(self.onSetupWindowClosed)
        self.ScenarioSetupWindow.show()

    def OpenWeightsWindow(self):
        self.WeightsSetupWindow = Ui_WeightSetup(ANSWERS_DB)
        self.WeightsSetupWindow.setWindowModality(Qt.WindowModal)
        self.WeightsSetupWindow.setWindowFlags(self.WeightsSetupWindow.windowFlags() | Qt.WindowStaysOnTopHint)
        #WeightsSetupWindow.windowClosed.connect(self.onSetupWindowClosed)
        self.WeightsSetupWindow.show()

    def onSetupWindowClosed(self):
        self.update_performance_dataframes() #Ensures that the dataframes have the modifications made on the databases
        self.populate_dimension_tree(self.ui.Performance_list, 2)
        self.populate_scenario_pages()
        
    def populate_with_objective_pages(self):
        """
        Populates the main widgets with objective pages based on the objectives retrived from the REFUSS_DB.

        """

        # Iterate over objectives
        for objective_id, objective in self.objectives.iterrows():
            objective_name = objective["ObjectiveName"]
            objective_description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."  # Replace with actual description

            if objective_id[0] == '1':
                # Create a page widget
                page = QWidget()

                # Create a layout for the page
                layout = QVBoxLayout()

                # Add labels to the layout
                layout.addWidget(QLabel(f"Objective : {objective_id}"))
                layout.addWidget(QLabel(f"Objective Name: {objective_name}"))
                layout.addWidget(QLabel(f"Objective Description: {objective_description}"))

                # Add spacer at the bottom
                vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
                layout.addItem(vertical_spacer)

                # Set the layout for the page
                page.setLayout(layout)

                # Set the property for the page
                page.setProperty("pageName", objective_id)

                # Add the page to the corresponding main widget based on the first character of objective_id
                self.ui.Functional_MainWidget.addWidget(page)

            elif objective_id[0] == '2':
                #self.ui.Performance_MainWidget.addWidget(page)
                pass

    def populate_with_criterion_pages(self):
        """
        Populates the UI with criterion pages based on the criteria, metrics, and metric options retrieved from the REFUSS_DB.

        """

        #self.PerformanceModels is a list of the
        self.PerformanceModels = []

        criteria_sorted = self.criteria.sort_values(by = "CriteriaID", ascending = True)

        for criteriaID, criterion in criteria_sorted.iterrows():
            criterion_name = criterion["CriteriaName"]
            criterion_metrics = self.metrics[self.metrics['CriteriaID'] == criteriaID]

            #Get the dimension based on the first character of the criterion_id
            if criteriaID.startswith('1'):
                Dimension = "F"

                #Generate the criterion label and assign the font and properties of the label
                Criterion_id_label = f"{Dimension}{criteriaID[2:]}"
                Criterion_label = QLabel(f"Criterion {Criterion_id_label}: {criterion_name}")
                Criterion_label.setFont(MyFont(12, True))
                Criterion_label.setWordWrap(True)  # Enable word wrapping
                Criterion_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Set the horizontal policy to Expanding

                # Create the criterion main widget
                page = QWidget()

                #Create a QVBoxLayout for the main widget
                layout = QVBoxLayout(page)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)  # Set the spacing to 0 or a smaller value

                #Create a QScrollArea
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget -> texto não corta
                scroll_area.setStyleSheet("QScrollArea { border: none; }")

                # Create a QWidget as the content widget for the scroll area
                scroll_widget = QWidget()

                # Create a QVBoxLayout for the scroll widget
                scroll_layout = QVBoxLayout(scroll_widget)
                scroll_layout.setContentsMargins(2, 2, 2, 2)
                scroll_layout.setSpacing(25)

                # Populate the scroll layout with the metric "normal" blocks
                criterion_metrics_sorted = criterion_metrics.sort_values(by = "MetricID", ascending = True)

                for metric_id, metric in criterion_metrics_sorted.iterrows():
                    metric_name = metric["MetricName"]
                    metric_question = metric["MetricQuestion"]
                    answer_type = metric["Answer_Type"]
                    answer_options = self.metric_options.loc[metric_id]

                    #add metric block to respective layout
                    if metric_id[0] == '1':
                        metric_block = FunctionalMetricBlock(metric_id, metric_name, metric_question, answer_type, answer_options)
                    elif metric_id[0] == '2':
                        metric_block, model, table_view = PerformanceMetricBlock(metric_id, metric_name, metric_question)
                        self.PerformanceModels.append((model, table_view))
                    scroll_layout.addLayout(metric_block)

                #add spacer at the bottom of the metrics
                vertical_spacer2 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
                scroll_layout.addItem(vertical_spacer2)

                # Set the scroll widget as the content widget for the scroll area
                scroll_area.setWidget(scroll_widget)

                # Add the desired widgets, inluding the scrool area, to the main layout
                layout.addWidget(Criterion_label)
                layout.addWidget(scroll_area)
                layout.setStretch(0,1)
                layout.setStretch(1,20)

                # Set the property for the page
                page.setProperty("pageName", criteriaID)

                self.ui.Functional_MainWidget.addWidget(page)
            else:
                Dimension = "P"

    def populate_scenario_pages(self):
        M_Operate_GUI_Elements.CleanStackedWidget(self.ui.Performance_MainWidget)       #LIMPAR PAGES EXISTENTES

        for scenario_id, scenario_setting in self.ScenarioSetup.iterrows():
            self.scenario_models[scenario_id] = {}

            # Create the main widget
            page = QWidget()
            #Create a QVBoxLayout for the main widget
            page_layout = QVBoxLayout(page)
            #page.setStyleSheet("border: 1px solid #000;") 
            
            page_layout.setContentsMargins(0, 0, 0, 0)
            page_layout.setSpacing(0)  # Set the spacing to 0 or a smaller value

            # Create a QWidget as the content widget for the scroll area
            scroll_widget = QWidget()

            # Create a QVBoxLayout for the scroll widget
            scroll_layout = QVBoxLayout(scroll_widget)
            scroll_layout.setContentsMargins(2, 2, 2, 2)
            scroll_layout.setSpacing(5)

            #Create a QScrollArea
            scroll_area = QScrollArea()
            scroll_area.setWidget(scroll_widget)
            scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget -> texto não corta
            scroll_area.setStyleSheet("QScrollArea { border: none; }")
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

            # ADD LABEL COM O SCENARIO_NAME
            scenario_name = scenario_setting["ScenarioName"]
            scenario_label = QLabel(f"Scenario: {scenario_name}")
            scenario_label.setFont(MyFont(12, True))

            page_layout.addWidget(scenario_label)
            page_layout.addWidget(scroll_area)

            for class_id, class_prop in self.IndicatorsClassesLibrary.iterrows():
                if class_id in self.selected_indicators.keys():
                    class_name = class_prop[ 'IndicatorClassName']
                    class_widget = M_Operate_GUI_Elements.NotExpandableSimpleElement(f"{class_name}")
                    class_widget.setObjectName(f"class_{class_id}")

                    scroll_layout.addWidget(class_widget) 
                    
                    class_excluxive = class_prop['Exclusive']
                    if class_excluxive == 'NO':
                        indicators_ids = self.selected_indicators[class_id]            
            
                        methodology = self.IndicatorsLibrary.at[indicators_ids[0], 'Reference']
                        reference_label = QLabel(f"Methodology: {methodology}")
                        
                        selected_unit = self.IndicatorsSetup.at[indicators_ids[0], 'SelectedUnit']
                        unit_label = QLabel(f"Data unit: {selected_unit}")
                                                                    
                        scenario_model = GeneralizedIndicatorModel(ANSWERS_DB, indicators_ids, scenario_id, ['Value'], ["Node surcharge", "Node flooding", "Surface Flooding"])
            
                        scenarios_view = QTableView()
                        scenarios_view.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
                        scenarios_view.setSelectionBehavior(QAbstractItemView.SelectItems)
                        scenarios_view.setSelectionMode(QAbstractItemView.SingleSelection)
                        scenarios_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
                        
                        scenarios_view.setModel(scenario_model)
                        scenarios_view.setObjectName(f"{class_id}")
                        scenarios_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                        
                        scenarios_view.setStyleSheet(
                            "QTableView { background-color: transparent; border: none; spacing: 0px; margin: 0px;}"
                            "QHeaderView::section { background-color: #EDEDED; border: 1 px solid black; }"
                            "QTableView::item { background-color: white; selection-background-color: white; color: black; }"
                            )

                        # Connect to the dataChanged signal
                        scenario_model.dataChanged.connect(lambda topLeft, bottomRight: scenarios_view.viewport().update())
                        # Update the display when data changes
                        scenarios_view.viewport().update()
                        
                        class_widget.content_layout.addWidget(reference_label)
                        class_widget.content_layout.addWidget(unit_label)
                        class_widget.content_layout.addWidget(scenarios_view)
        
                    else: 
                        for indicator_id, indicator in self.IndicatorsSetup.iterrows():
                            if indicator_id  in self.selected_indicators[class_id]:
                                methodology = self.IndicatorsLibrary.at[indicator_id, 'Reference']
                                reference_label = QLabel(f"Methodology: {methodology}")
                                unit_label = QLabel(f"Data unit: {indicator['SelectedUnit']}")

                                scenario_model = QSqlTableModel(db = ANSWERS_DB)
                                scenario_model.setTable(indicator_id)
                                scenario_model.setEditStrategy(QSqlTableModel.OnFieldChange)
                                scenario_model.setFilter(f"ScenarioID = '{scenario_id}'")
                                scenario_model.select()

                                # Associa o modelo a um nome específico para acessá-lo posteriormente
                                self.scenario_models[scenario_id][indicator_id] = scenario_model

                                ''''PRINT MODEL
                                # # Fetch the header data (column names)
                                # header_data = [model.headerData(i, Qt.Horizontal) for i in range(model.columnCount())]
                                # # Print the column names
                                # print("Column Names:", header_data)
                                # # Fetch and print the data
                                # for row in range(model.rowCount()):
                                #     row_data = [model.data(model.index(row, col), Qt.DisplayRole) for col in range(model.columnCount())]
                                #     print(f"Row {row + 1}: {row_data}")
                                '''
                                
                                scenarios_view = QTableView()
                                scenarios_view.setModel(scenario_model)
                                scenarios_view.setObjectName(f"{indicator_id}")
                                scenarios_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

                                scenarios_view.setColumnHidden(0, True) # Hide first column (ScenarioID)
                                scenarios_view.setStyleSheet(
                                    "QTableView { background-color: transparent; border: none; spacing: 0px; margin: 0px;}"
                                    "QHeaderView::section { background-color: #EDEDED; border: 1 px solid black; }"
                                    "QTableView::item { background-color: white; selection-background-color: white; color: black; }")
                                scenarios_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                                scenarios_view.resizeRowsToContents()
                                scenarios_view.verticalHeader().setVisible(False)    # Hide the vertical header (row indexes)
                                                        
                                class_widget.content_layout.addWidget(reference_label)
                                class_widget.content_layout.addWidget(unit_label)
                                class_widget.content_layout.addWidget(scenarios_view)

            scroll_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
            page.setProperty("pageName", f"Scenario{scenario_id}")
            self.ui.Performance_MainWidget.addWidget(page)
            self.scenario_pages[scenario_id] = page

    def create_model(self, scenario_id, model_name, table_name, filter_condition):
        # Cria uma instância do QSqlTableModel
        model = QSqlTableModel()

        # Define a tabela da base de dados que o modelo deve representar
        model.setTable(table_name)

        # Define a estratégia de edição para o modelo (opcional)
        model.setEditStrategy(QSqlTableModel.OnFieldChange)

        # Aplica um filtro ao modelo para exibir apenas as linhas que atendem à condição
        model.setFilter(filter_condition)

        # Carrega os dados da tabela com base no filtro
        model.select()

        # Associa o modelo a um nome específico para acessá-lo posteriormente
        self.scenario_models[scenario_id][model_name] = model

        # Cria uma QTableView para exibir os dados do modelo
        view = QTableView()
        view.setModel(model)

        return view

    def navigate_to_page(self, item):
        """
        Navigates to the page based on the item selected.

        Args:
            item: The selected item.

        Returns:
            None
        """
        item_id = item.data(0, Qt.UserRole)

        if item_id.startswith("1"):
            M_Operate_GUI_Elements.access_page_by_name(self.ui.Functional_MainWidget, item_id)
        elif item_id.startswith("Scenario"):
            M_Operate_GUI_Elements.access_page_by_name(self.ui.Performance_MainWidget, item_id)

    def populate_dimension_tree(self, tree_widget: QTreeWidget, dimension_id: int):
        """
        Populate the given tree widget with objectives and criteria for the given dimension.

        Args:
            tree_widget (QTreeWidget): The tree widget to populate.
            dimension_id (int): The ID of the dimension to fetch objectives and criteria for.
        """

        # Clear the tree widget
        tree_widget.clear()

        if dimension_id == 1:
            # Populate the tree widget with objectives and criteria
            for objectiveID, objective in self.objectives[self.objectives["DimensionID"] == dimension_id].iterrows():
                # Create an objective item with the objective name and description
                objective_item = QTreeWidgetItem([f"{objective['ObjectiveSubID']} - {objective['ObjectiveName']}"])
                objective_item.setData(0, Qt.UserRole, objectiveID)  # Store the ObjectiveID as data
                objective_item.setFont(0, MyFont(9, True))
                tree_widget.addTopLevelItem(objective_item)


                for criteriaID, criterion in self.criteria[self.criteria["ObjectiveID"] == objectiveID].iterrows():
                    # Create a criterion item with the criterion name and description
                    criterion_item = QTreeWidgetItem([f"{objective['ObjectiveSubID']}.{criterion['CriteriaSubID']} - {criterion['CriteriaName']}"])
                    criterion_item.setData(0, Qt.UserRole, criteriaID)  # Store the CriterionID as data
                    objective_item.addChild(criterion_item)

        elif dimension_id == 2:
            # Populate the tree widget with scenarios
            query = QSqlQuery("SELECT ScenarioID, ScenarioName FROM ScenarioSetup ORDER BY ScenarioID", ANSWERS_DB)

            while query.next():
                scenario_id = query.value(0)
                scenario_name = query.value(1)

                scenario_item = M_Operate_GUI_Elements.DatabaseItem(scenario_id, "ScenarioName")
                scenario_item.setData(0, Qt.UserRole, f"Scenario{scenario_id}")
                scenario_item.setText(0, scenario_name)
                scenario_item.setFont(0, MyFont(9, True))
                tree_widget.addTopLevelItem(scenario_item)

            query.finish()

    def save_answers(self):
        """
        Save answers from the UI to the database.
        """

        # Define criteria and metric labels
        Criteria_labels = ["Criterion F", "Criterion P"]
        Metric_labels = ["F", "P"]

        # Iterate over the Functional Dimension pages
        for page_index in range(1, self.ui.Functional_MainWidget.count()):
            page_widget = self.ui.Functional_MainWidget.widget(page_index)
            page_layout = page_widget.layout()

            # Get the 1st label text and verify if it is a criterion page
            page_widgets = M_Operate_GUI_Elements.getWidgetsFromLayout(page_layout)
            first_widget_label = page_widgets[0].text()

            if first_widget_label.startswith("Criterion"): #Page is a Criterion page:
                criteria_id = page_widget.property("pageName")

                #Access scroll area layout:
                scroll_area = page_widgets[1]
                scroll_widget = scroll_area.widget()
                scroll_widget_layout = scroll_widget.layout()

                #Iterate over each Metric Block in the scroll area layout:
                for index in range(scroll_widget_layout.count() - 1): #-1 to not iterate on QSpacerItem
                    #Access the metric block
                    metric_block = scroll_widget_layout.itemAt(index)
                    #Get Widgets within the block: metric label, metric question, "Comment:" and metris comment
                    metric_block_widgets = M_Operate_GUI_Elements.getWidgetsFromLayout(metric_block)

                    metric_label = metric_block_widgets[0].text()
                    for index, i in enumerate(Metric_labels):
                        if metric_label.startswith(i):
                            metric_id = metric_label.replace(i, f"{str(index+1)}.").split(": ")[0]
                            break

                    comment = metric_block_widgets[-1].toPlainText()

                    if criteria_id[0] == '1':
                        #Access layout of metric answers
                        metric_block_answers_layout = M_Operate_GUI_Elements.getLayoutsFromLayout(metric_block)[0]
                        answer_options_layout_widgets = M_Operate_GUI_Elements.getWidgetsFromLayout(metric_block_answers_layout)

                        # Check the type of answer options
                        if isinstance(answer_options_layout_widgets[0], QLineEdit):  # Open answer question
                            answer = answer_options_layout_widgets.text()

                        # Open answer question
                        elif isinstance(answer_options_layout_widgets[0], QRadioButton):  # Single choice question
                            for position, radio in enumerate(answer_options_layout_widgets):
                                    if radio.isChecked():
                                        answer = [str(position), radio.text()]
                                        break
                                    else:
                                        answer = ''
                            answer = '_'.join(answer)

                        elif isinstance(answer_options_layout_widgets[0], QCheckBox):  # Multiple choice question
                            answers = []
                            for position, box in enumerate(answer_options_layout_widgets):
                                if box.isChecked():
                                    answers.append([str(position), box.text()])
                            if answers == []:
                                answer = ''
                            else:
                                answer = ';'.join(['_'.join(x) for x in answers])

                        M_OperateDatabases.save_answer_to_AnswersDatabase(ANSWERS_DB, metric_id, answer, comment)

    ################## Define functions to button behaviour:
    def savefile(self):
        global ANSWERS_DB
        if self.sender().objectName() == 'actionSave_As':
            new_database_file, _ = QFileDialog.getSaveFileName(self, 'Save File As',dir = os.getcwd(), filter = '*.db')
            QSqlDatabase.removeDatabase(ANSWERS_DB.databaseName())
            ANSWERS_DB.close()
            #set a new connection with teh same name
            ANSWERS_DB = QSqlDatabase.addDatabase("QSQLITE", "Connection2")
            ANSWERS_DB.setDatabaseName(new_database_file)
            ANSWERS_DB.open()

        M_OperateDatabases.verifyAnswersDatabase(ANSWERS_DB)
        M_OperateDatabases.setConsequencesTables(REFUSS_DB, ANSWERS_DB)

        self.save_answers()
        return

    def loadfile(self):
        loadfile, _ = QFileDialog.getOpenFileName(self, 'Open File',dir = os.getcwd(), filter = '*.db')
        if loadfile:
            load_FunctionalAnswers(self.ui.Functional_MainWidget)
        return

    def home_btn_toggled(self):
        self.ui.BodyWidget.setCurrentIndex(0)
        self.ui.TitlesWidget.setCurrentIndex(0)

    def urbanprofile_btn_toggled(self):
        self.ui.BodyWidget.setCurrentIndex(1)
        self.ui.TitlesWidget.setCurrentIndex(1)

    def stormprofile_btn_toggled(self):
        self.ui.BodyWidget.setCurrentIndex(2)
        self.ui.TitlesWidget.setCurrentIndex(2)

    def functional_btn_toggled(self):
        self.ui.BodyWidget.setCurrentIndex(3)
        self.ui.TitlesWidget.setCurrentIndex(3)

    def performance_btn_toggled(self):
        self.ui.BodyWidget.setCurrentIndex(4)
        self.ui.TitlesWidget.setCurrentIndex(4)

    def dashboard_btn_toggled(self):
        if self.ui.BodyWidget.currentIndex() != 5:
            self.ui.BodyWidget.setCurrentIndex(5)
            self.ui.TitlesWidget.setCurrentIndex(5)
            self.savefile()
            self.UpdateDashboardPage()

    def closeEvent(self, event):
        super().closeEvent(event)

    def UpdateDashboardPage(self):
        '''
        ADD SOME COLUMNS TO DATAFRAMES FOR FURTHER PLOTING
        '''
        #Get the all the data from answers and tables and do some compatibilizations
        #Add ShortLabel and FullLabel to self.objectives
        self.objectives["ShortLabel"] = ''
        self.objectives["FullLabel"] = ''

        for index, row in self.objectives.iterrows():
            if row["DimensionID"] == 1:
                DimensionLetter = "F"
            elif row["DimensionID"] == 2:
                DimensionLetter = "P"
            self.objectives.at[index, "ShortLabel"] = f"Obj. {DimensionLetter}{row['ObjectiveSubID']}"
            self.objectives.at[index,"FullLabel"] = f"{self.objectives.at[index,'ShortLabel']} - {row['ObjectiveName']}"

        #Add ShortLabel and FullLabel to self.criteria
        self.criteria["ShortLabel"] = ''
        self.criteria["FullLabel"] = ''
        for index, row in self.criteria.iterrows():
            Dimension = row["ObjectiveID"].split(".")[0]
            Objective = row["ObjectiveID"].split(".")[1]
            if Dimension == "1":
                DimensionLetter = "F"
            elif Dimension == "2":
                DimensionLetter = "P"
            self.criteria.at[index,"ShortLabel"] = f"Crit. {DimensionLetter}{Objective}.{row['CriteriaSubID']}"
            self.criteria.at[index,"FullLabel"] = f"{self.criteria.at[index, 'ShortLabel']} - {row['CriteriaName']}"

        MetricsAnswers = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "MetricAnswers")
        MetricsAnswers.set_index("metricID", inplace=True)


        '''
        TREAT FUNCTIONAL DIMENSION DATA
        '''
        # FILTER DATAFRAMES TO GET ONLY FUNCTIONAL DIMENSION
        Functional_Objectives = self.objectives[self.objectives["DimensionID"] == 1]
        Functional_Criteria = self.criteria[self.criteria.index.str.startswith("1.")]
        Functional_Answers = MetricsAnswers[MetricsAnswers.index.str.startswith('1.')]

        # Calculate the Functional Answered Metrics completness
        ObjectivesCompletnessSummary = M_ResilienceCalculus.Calculate_Completness(Functional_Answers)

        # Prepare ObjectivesCompletnessSummary to plot
        ObjectivesCompletness = pd.merge(Functional_Objectives, ObjectivesCompletnessSummary, left_index = True, right_index =True , how='inner')

        # Get the Weigths
        DimensionsWeight = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "DimensionsWeight")
        DimensionsWeight.set_index("DimensionID", inplace=True)
        ObjectivesWeight = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "ObjectivesWeight")
        ObjectivesWeight.set_index("ObjectiveID", inplace=True)
        CriteriaWeight = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "CriteriaWeight")
        CriteriaWeight.set_index("CriteriaID", inplace=True)
        self.Weights = {'Dimensions': DimensionsWeight, 'Objectives': ObjectivesWeight, 'Criteria': CriteriaWeight}
        
        # Calculate the FunctionalDimensionRating, FunctionalObjectivesRating and FunctionalCriteriaRating
        FunctionalDimensionRating, FunctionalObjectivesRating, FunctionalCriteriaRating = M_ResilienceCalculus.Calculate_FunctionalRating(self.Weights, self.metrics, self.metric_options, Functional_Answers)

        '''
        PREPARE FUNCTIONAL RESULTS TO PLOTTING
        '''
        FunctionalObjectivesRating = FunctionalObjectivesRating.join(Functional_Objectives[["ObjectiveName", "ShortLabel", "FullLabel"]].loc[FunctionalObjectivesRating.index], how = "right")

        # Prepare FunctionalCriteraRating to plot
        self.FunctionalCriteriaRating = FunctionalCriteriaRating.join(Functional_Criteria[["CriteriaName", "ShortLabel", "FullLabel"]].loc[FunctionalCriteriaRating.index], how = "right")

        # Set the FCR_ComboBox options
        ObjectivesID_List = ("F" + FunctionalObjectivesRating.index.str.split(".").str[1] + " - " + FunctionalObjectivesRating["ObjectiveName"]).tolist()
        M_Operate_GUI_Elements.updateQComboBox(self.ui.FCR_ComboBox, ObjectivesID_List)

        '''
        PLOT FUNCTIONAL RESULTS
        '''
        #Plot the Functional Objectives Completness
        M_PlotGraphs.plotHorizontalBars2(
            DataFrame = ObjectivesCompletness,
            labelColumn = "FullLabel",
            DestinyWidget = self.ui.FDC_Widget,
            Type = "Completness")

        #Plot the Functional Objectives Rating
        M_PlotGraphs.plotHorizontalBars2(
            DataFrame = FunctionalObjectivesRating,
            labelColumn = "FullLabel",
            DestinyWidget = self.ui.FOR_Widget,
            Type = "Rating")

        #Update Functional Criteria Rating plot when FCR_ComboBox changes
        self.ui.FCR_ComboBox.currentTextChanged.connect(self.updateFCR)

        #Plot the Functional Dimension Rating
        M_PlotGraphs.plotResilienceCircle(
            FunctionalDimensionRating,
                                  DestinyWidget = self.ui.FRR_Widget)

        '''
        PLOT EMPTY PERFORMANCE GRAPHS
        '''
        self.update_performance_dataframes()
         
        self.selected_indicators = M_IndicatorsSelection.load_selected_indicators(self.IndicatorsSetup)

        self.existing_scenarios = self.ScenarioSetup["ScenarioName"].tolist()

        M_Operate_GUI_Elements.updateQComboBox(self.ui.PSS_ComboBox, self.existing_scenarios)

        self.baseline_scenario = None

        self.ScenarioList_model = QStandardItemModel()
        self.ui.PSS_ScenarioList.setModel(self.ScenarioList_model)

        '''
        GET SRP INDICATORS
            ------> Passar para dentro da M_ResilienceCalculus.Caculate_ConsequencesRating
        '''
        SRPRating = pd.DataFrame(columns = self.ScenarioSetup.index.to_list(),
                                 index= self.IndicatorsSetup[self.IndicatorsSetup.index.str.startswith("SRP")].index.to_list())
        
        for ind_id, ind_prop in SRPRating.iterrows():
            IndAns = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, f"{ind_id}")
            IndAns.set_index("ScenarioID", inplace=True)
            for scn_id, value in IndAns.iterrows():
                IndResilience = 0
                if value[0] == '':
                    IndResilience = None
                else:
                    IndResilience = value[0].astype(float)
                SRPRating.loc[ind_id, scn_id] = IndResilience
        SRPRating = SRPRating.T
        
        '''
        CALCULATE CONSEQUENCES INDICATORS
        '''
        PerformanceConsequencesRating = M_ResilienceCalculus.Caculate_ConsequencesRating(
            AnswersDatabase = ANSWERS_DB,
            IndicatorsLibrary = self.IndicatorsLibrary,
            ScenarioSetup = self.ScenarioSetup,
            IndicatorsSetup = self.IndicatorsSetup)

        #Create a list of plots to be updated on the run when the Scenario selection changes
        self.PerformancePlots = []

        self.SPR_plot = M_PlotGraphs.plotPerformances(DataFrame = SRPRating,
                                              xScale = 1,
                                              DestinyWidget = self.ui.SPR_Widget)

        self.PerformancePlots.append(self.SPR_plot)

        self.SCR_plot = M_PlotGraphs.plotPerformances(DataFrame = PerformanceConsequencesRating,
                                              xScale = 1,
                                              DestinyWidget = self.ui.SCR_Widget)
        
        self.PerformancePlots.append(self.SCR_plot)


        #Calculate each Scenario Resilience has the average of all performance and hazard metrics
        ScenariosPerformanceResilience = pd.merge(SRPRating, PerformanceConsequencesRating, left_index=True, right_index=True).astype(float).mean(axis=1)
        ScenariosPerformanceResilience = pd.DataFrame(ScenariosPerformanceResilience, columns=["PerRes"])

        self.ResiliencePlots = []

        self.PRR_plot = M_PlotGraphs.plotSceariosResilience(DataFrame = ScenariosPerformanceResilience,
                                                    xScale = 1,
                                                    DestinyWidget = self.ui.PRR_Widget)
        self.PerformancePlots.append(self.PRR_plot)

        self.ui.PSS_ComboBox.currentTextChanged.connect(self.onPSSComboBoxTextChanged)

        self.ScenarioList_model.dataChanged.connect(self.updatePerformancePlots)

    def onPSSComboBoxTextChanged(self):

        #If a baseline scenario already exists
        if self.baseline_scenario:
            # Get the items that are selected on the QListView
            self.additional_scenarios = M_Operate_GUI_Elements.getQListSelection(self.ScenarioList_model)

            for plot in self.PerformancePlots:
                #turn off the current baseline scenario
                plot.update_series_visibility(self.baseline_scenario, False)
                if self.additional_scenarios:                                               #if other scenarios are activated
                    for additional_scenario in self.additional_scenarios:
                        plot.update_series_visibility(additional_scenario, False)           #turn off those scenarios


        new_baseline_scenario = self.ui.PSS_ComboBox.currentText()                          #set the new baseline scenario from the ComboBox text
        new_baseline_scenario_index = str(self.ScenarioSetup[self.ScenarioSetup['ScenarioName'] == new_baseline_scenario].index[0])
        if new_baseline_scenario:                                                           #update the items to be shown on the QListView
            M_Operate_GUI_Elements.updateQListView(ListView = self.ui.PSS_ScenarioList,
                            Model = self.ScenarioList_model,
                            Data = self.existing_scenarios,
                            Exclude = new_baseline_scenario)
            for plot in self.PerformancePlots:
                plot.update_series_visibility(new_baseline_scenario_index, True)              #activate the new baseline scenario on the plot
                plot.set_baseline_scenario(new_baseline_scenario)                       #give to the plot class the name of the baseline scenario

            # Store the new baseline scenario for the next update
            self.baseline_scenario = new_baseline_scenario_index                              #set the current baselinescenario from the new value for future changes

    def updatePerformancePlots(self, index):
        # Get the item from the model using the index
        item = self.ScenarioList_model.itemFromIndex(index)
        if not item:
            return None

        # Get the series name and its new check state
        series_name = item.text()
        visibility = item.checkState() == Qt.Checked

        # Call the plots methods to update the series visibility
        for plot in self.PerformancePlots:
            plot.update_series_visibility(series_name, visibility)

            if visibility == False:
                plot.clearSelected_lines_and_text()

        # self.SPR_plot.canvas.draw()

    def updateFCR(self):

        selected_text = self.ui.FCR_ComboBox.currentText()

        if selected_text != '':
            ObjectiveID = f'1.{selected_text.split(" - ")[0].split("F")[1]}'
            showing_FunctionalCriteriaRating = self.FunctionalCriteriaRating[self.FunctionalCriteriaRating["ObjectiveID"]==ObjectiveID]
            # showing_FunctionalCriteriaRating.reset_index(inplace = True)
            
            M_PlotGraphs.plotHorizontalBars2(
                DataFrame = showing_FunctionalCriteriaRating,
                labelColumn = "FullLabel",
                DestinyWidget = self.ui.FCR_Widget,
                Type = "Rating")
            
            # M_PlotGraphs.plotHorizontalBars(DataFrame = showing_FunctionalCriteriaRating,
            #                     labelColumn = "FullLabel",
            #                     dataColumn = "MeanAnswerScores",
            #                     xScale = 1,
            #                     DestinyWidget = self.ui.FCR_Widget,
            #                     MultiBar = False)

        # else:
        #     noob = pd.DataFrame([], columns=['Column1'])

        #     M_PlotGraphs.plotHorizontalBars(DataFrame = noob,
        #             xScale = 1,
        #             labelColumn = '',
        #             dataColumn = "Column1",
        #             DestinyWidget = self.ui.FCR_Widget,
        #             MultiBar = True)

def load_FunctionalAnswers(Widget):

    answers_from_database = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "MetricAnswers")

    answers_from_database = answers_from_database.set_index("metricID")

    # Iterate over the pages
    for page_index in range(1, Widget.count()):
        page_widget = Widget.widget(page_index)
        page_layout = page_widget.layout()

    # Get the 1st label text and verify if it is a criterion page!
        page_widgets = M_Operate_GUI_Elements.getWidgetsFromLayout(page_layout)
        first_widget_label = page_widgets[0].text()

        Criteria_labels = ["Criterion F", "Criterion P"]
        Metric_labels = ["F", "P"]

        if first_widget_label.startswith("Criterion"): #Page is a Criterion page:
            #Access Page layout:
            for index, i in enumerate(Criteria_labels): #Get the critera id (1st widget)
                if first_widget_label.startswith(i):
                    criteria_id = first_widget_label.replace(i, f"{str(index+1)}.").split(": ")[0]
                    break

            #Access scroll area layout:
            scroll_area = page_widgets[1]
            scroll_widget = scroll_area.widget()
            scroll_widget_layout = scroll_widget.layout()

            #Iterate over each Metric Block in the scroll area layout:
            for index in range(scroll_widget_layout.count() - 1): #-1 to not iterate on QSpacerItem
                #Access the metric block
                metric_block = scroll_widget_layout.itemAt(index)
                #Get Widgets within the block: metric label, metric question, "Comment:" and metris comment
                metric_block_widgets = M_Operate_GUI_Elements.getWidgetsFromLayout(metric_block)

                metric_label = metric_block_widgets[0].text()
                for index, i in enumerate(Metric_labels):
                    if metric_label.startswith(i):
                        metric_id = metric_label.replace(i, f"{str(index+1)}.").split(": ")[0]
                        break

                if metric_id[0] == '1':
                    #Assign comment from answers
                    comment = answers_from_database.loc[metric_id, "comment"]
                    metric_block_widgets[-1].setText(comment)

                    #Access layout of metric answers
                    metric_block_answers_layout = M_Operate_GUI_Elements.getLayoutsFromLayout(metric_block)[0]
                    answer_options_layout_widgets = M_Operate_GUI_Elements.getWidgetsFromLayout(metric_block_answers_layout)

                    # Check the type of answer options
                    if isinstance(answer_options_layout_widgets[0], QLineEdit):  # Open answer question
                        answer = answers_from_database.loc[metric_id, "answer"]
                        answer_options_layout_widgets[0].setText(answer)

                    # Open answer question
                    elif isinstance(answer_options_layout_widgets[0], QRadioButton):  # Single choice question
                        answer = answers_from_database.loc[metric_id, "answer"].split('_')[0]
                        if answer != '':
                            for position, radio in enumerate(answer_options_layout_widgets):
                                if position == int(answer):
                                    radio.setChecked(True)

                    elif isinstance(answer_options_layout_widgets[0], QCheckBox):  # Multiple choice question
                        answers = []
                        for element in answers_from_database.loc[metric_id, "answer"].split(';'):
                            if element != '':
                                answers.append(int(element.split('_')[0]))
                        for position, box in enumerate(answer_options_layout_widgets):
                            if position in answers:
                                box.setChecked(True)
                            else:
                                box.setChecked(False)

                elif metric_id[0] == '2':
                    pass

def FunctionalMetricBlock(metric_id, metric_name, metric_question, answer_type, answer_options):

    # Create the widgets for the metric block (e.g., labels, answer widget)
    if metric_id.startswith('1'):
        Dimension = "F"
    else:
        Dimension = "P"
    metric_id_label = f"{Dimension}{metric_id[2:]}"


    metric_id_label = QLabel(f"{metric_id_label}: {metric_name}")
    metric_id_label.setFont(MyFont(10, True))
    metric_id_label.setWordWrap(True)  # Enable word wrapping

    metric_question_label = QLabel(f"Question: {metric_question}")
    metric_question_label.setFont(MyFont(10, False))
    metric_question_label.setWordWrap(True)  # Enable word wrapping

    # Create the layout for the metric block
    Metric_block = QVBoxLayout()
    Metric_block.setContentsMargins(0,0,0,0)
    Metric_block.setSpacing(2)

    Metric_block.addWidget(metric_id_label)
    Metric_block.addWidget(metric_question_label)

    # Logic to create the appropriate answer widget based on the answer type
    if Dimension == "F":

        OptionsLayout = QVBoxLayout()
        if answer_type == "Single choice" or answer_type == "Multiple choice":
            Options = answer_options.filter(regex='^Opt')
            Options = Options.values.tolist()

            if answer_type == "Single choice":
                radio_group = QButtonGroup()
                radio_group.setExclusive(False)        #Allows the button to be deselected if selected
                radio_group.buttonClicked.connect(lambda: check_buttons)
                # Add the answer options as radio buttons to the layout
                for option in Options:
                    if option != '':
                        option_radio = QRadioButton(option)
                        option_radio.setFont(MyFont(10, False))
                        radio_group.addButton(option_radio)
                        OptionsLayout.addWidget(option_radio)

                def check_buttons(radioButton):            #when another button is selected, deselects the current selection
                    for button in radio_group.buttons():
                        if button is not radioButton:
                            button.setChecked(False)

            elif answer_type == "Multiple choice":
                checkbox_group = QButtonGroup()
                # Add the answer options as checkboxes to the layout
                for option in Options:
                    if option != '':
                        option_checkbox = QCheckBox(option)
                        option_checkbox.setFont(MyFont(10, False))
                        checkbox_group.addButton(option_checkbox)
                        OptionsLayout.addWidget(option_checkbox)
                        #Metric_block.addWidget(option_checkbox)

        elif answer_type == "Open":
            line_edit = QLineEdit()
            line_edit.setFont(MyFont(10, False))
            #Metric_block.addWidget(line_edit)
            OptionsLayout.addWidget(line_edit)
        else:
            return None  # Return None for unsupported answer types

        Metric_block.addLayout(OptionsLayout)

    #Add metric comment
    metric_comment_label = QLabel(f"\n Comment: ")
    metric_comment_label.setFont(MyFont(10, False))
    metric_comment_label.setWordWrap(True)  # Enable word wrapping
    metric_comment = QTextEdit()
    metric_comment.setAcceptRichText(True)
    metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
    metric_comment.setFixedHeight(60)
    metric_comment.setFont(MyFont(10, False))
    metric_comment.setStyleSheet("background-color: white;")

    Metric_block.addWidget(metric_comment_label)
    Metric_block.addWidget(metric_comment)

    # Connect signals and slots to handle selection within the metric block
    if answer_type == "Single choice":
        radio_group.buttonClicked.connect(lambda: M_Operate_GUI_Elements.handleSingleChoiceSelection(radio_group))
    elif answer_type == "Multiple choice":
        for i in range(Metric_block.count() - 1):  # Exclude the comment widgets
            widget = Metric_block.itemAt(i).widget()
            if isinstance(widget, QCheckBox):
                widget.clicked.connect(lambda: M_Operate_GUI_Elements.handleMultipleChoiceSelection(Metric_block))

    return Metric_block

def PerformanceMetricBlock(metric_id, metric_name, metric_question):

    # Create the widgets for the metric block (e.g., labels, answer widget)
    if metric_id.startswith('1'):
        Dimension = "F"
    else:
        Dimension = "P"

    metric_id_label = f"{Dimension}{metric_id[2:]}"

    metric_id_label = QLabel(f"{metric_id_label}: {metric_name}")
    metric_id_label.setFont(MyFont(10, True))

    metric_question_label = QLabel(f"Question: {metric_question}")
    metric_question_label.setFont(MyFont(10, False))
    metric_question_label.setWordWrap(True)  # Enable word wrapping

    # Create the layout for the metric block
    Metric_block = QVBoxLayout()
    Metric_block.setContentsMargins(0,0,0,0)
    Metric_block.setSpacing(2)

    Metric_block.addWidget(metric_id_label)
    Metric_block.addWidget(metric_question_label)

    if Dimension == "P":
        Setup_model = PerformanceSqlTableModel(db = ANSWERS_DB, non_editable_columns= [0])
        Setup_model.setTable("PerformanceAnswers")

        # Set the columns to be displayed
        indicator_column_name = f"M{metric_id.replace('.', '')}"
        # table_index = get_column_index(Setup_model, indicator_column_name)

        # Remove the unwanted columns from the model
        for i in reversed(range(Setup_model.columnCount())):
            column_name = Setup_model.headerData(i, Qt.Horizontal)
            if column_name != "ScenarioName" and column_name != indicator_column_name:
                Setup_model.removeColumn(i)

        # Set the Headers name
        Setup_model.setHeaderData(0, Qt.Orientation.Horizontal, "Scenario")
        Setup_model.setHeaderData(1, Qt.Orientation.Horizontal, "Answer")

        # Manually update the view to reflect the changes
        Setup_model.select()

        # Set the second column to be editable
        Setup_model.setEditStrategy(PerformanceSqlTableModel.EditStrategy.OnFieldChange)

        # Create a QTableView and set the model
        table_view = QTableView()
        table_view.setModel(Setup_model)

        # Reset the view to reflect the changes
        #table_view.reset()

        # Set the delegate for the "Answer" column
        delegate = DecimalZeroOneDelegate()
        table_view.setItemDelegate(delegate)

        # Hide the vertical header (row indexes)
        table_view.verticalHeader().setVisible(False)

        # Customize the appearance of the new QTableView
        table_view.setStyleSheet(
            "QTableView { background-color: transparent; border: none; color: black}"
            "QHeaderView::section { background-color: #EDEDED; border: 1 px solid black; }"
            "QTableView::item { background-color: white; border: 0 px solid black;}"
            "QTableView::item:selected { background-color: #D3D3D3; }"
            )

        # Set the horizontal stretch factor for the new_table_view
        table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Allow horizontal stretching

        # Set the vertical stretch factor for the new_table_view
        table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scrolling
        table_view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # Smooth scrolling
        table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)  # Adjust the height based on the content

        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        Metric_block.addWidget(table_view, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    #Add metric comment
    metric_comment_label = QLabel(f"\n Comment: ")
    metric_comment_label.setFont(MyFont())
    metric_comment_label.setWordWrap(True)  # Enable word wrapping
    metric_comment = QTextEdit()
    metric_comment.setAcceptRichText(True)
    metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
    metric_comment.setFixedHeight(60)
    metric_comment.setFont(MyFont())
    metric_comment.setStyleSheet("background-color: white;")

    Metric_block.addWidget(metric_comment_label)
    Metric_block.addWidget(metric_comment)

    return Metric_block, Setup_model, table_view

def updateHazardTableViews(StackedWidget: QStackedWidget):

    NrHazards = M_OperateDatabases.countDatabaseRows(ANSWERS_DB, "HazardSetup")
    NrScenarios = M_OperateDatabases.countDatabaseRows(ANSWERS_DB, "ScenarioSetup")

    if NrHazards > 0 and NrScenarios > 0:
        queryAnswers = QSqlQuery(ANSWERS_DB)
        queryLibrary = QSqlQuery(REFUSS_DB)

        if queryAnswers.exec("SELECT HazardName, HazardUnit FROM HazardSetup"):
            hazard_data = []  # List to store hazard data

            # Create the QVBoxLayout for the scroll widget
            scroll_layout = QVBoxLayout()

            # Create the QWidget as the content widget for the scroll area
            scroll_widget = QWidget()
            scroll_widget.setLayout(scroll_layout)

            # Create a QScrollArea
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget -> texto não corta
            scroll_area.setStyleSheet("QScrollArea { border: none; }")
            scroll_area.setWidget(scroll_widget)

            #Iterate over each hazard:
            while queryAnswers.next():
                hazard_name = str(queryAnswers.value("HazardName"))
                if queryLibrary.exec(f"SELECT NrClasses FROM HazardLibrary WHERE ShowName = '{hazard_name}'"):
                    # Assuming ShowName is a unique identifier, use 'fetchOne' to get a single result
                    if queryLibrary.next():
                        nr_classes = int(queryLibrary.value("NrClasses"))

                # Check if the hazard already exists in the hazard data
                hazard_exists = False
                for existing_hazard_name, existing_model, existing_classes in hazard_data:
                    if hazard_name == existing_hazard_name:
                        hazard_exists = True
                        # Update the existing hazard model
                        existing_model.setTable("HazardAnswers")
                        existing_model.setFilter(f"HazardName = '{hazard_name}'")
                        existing_model.select()
                        # Update other properties of the hazard model if needed
                        break

                if not hazard_exists:
                    # Create a new model for the new hazard
                    new_model = PerformanceSqlTableModel(db=ANSWERS_DB, non_editable_columns=[0,1])
                    new_model.setTable("HazardAnswers")
                    new_model.setFilter(f"HazardName = '{hazard_name}'")
                    new_model.select()

                    # Set the 1st Header of the model as "Scenario"
                    new_model.setHeaderData(0, Qt.Vertical, "Scenario")

                    # Create a new QTableView for the new hazard
                    new_table_view = QTableView()
                    new_table_view.setModel(new_model)

                    # Find the index of the column that matches the HazardName
                    hazard_name_column_index = -1
                    for i in range(new_model.columnCount()):
                        column_name = new_model.headerData(i, Qt.Horizontal)
                        if column_name == "HazardName":
                            hazard_name_column_index = i
                            break

                    # Hide the HazardName column
                    if hazard_name_column_index != -1:
                        new_table_view.setColumnHidden(hazard_name_column_index, True)

                    # Remove the unwanted columns from the view
                    for i in reversed(range(new_model.columnCount())):
                        column_name = new_model.headerData(i, Qt.Horizontal)
                        if column_name.startswith("Class"):
                            class_number = int(column_name.split("Class")[1])  # Extract the class number from the column name
                            if class_number > nr_classes:
                                new_table_view.hideColumn(i)

                    # Hide the vertical header (row indexes)
                    new_table_view.verticalHeader().setVisible(False)

                   # Customize the appearance of the new QTableView
                    new_table_view.setStyleSheet(
                        "QTableView { background-color: transparent; border: none; }"
                        "QHeaderView::section { background-color: #EDEDED; border: 1 px solid black; }"
                        "QTableView::item { background-color: white; }"
                        "QTableView::item:selected { background-color: #D3D3D3; color: black }"
                        )

                    if hazard_name == "Buildings Damage (B1)":
                        #delegate for buttons in the cells
                        #each button goes to the
                        pass

                    # Set the EditStrategy of the model
                    new_model.setEditStrategy(PerformanceSqlTableModel.EditStrategy.OnFieldChange)

                    # Set the horizontal stretch factor for the new_table_view
                    new_table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Allow horizontal stretching

                    # Set the vertical stretch factor for the new_table_view
                    new_table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scrolling
                    new_table_view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # Smooth scrolling
                    new_table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)  # Adjust the height based on the content

                    # Create the QLabel for the hazard name
                    label = QLabel()
                    hazard_name_query = QSqlQuery(ANSWERS_DB)
                    hazard_name_query.prepare("SELECT HazardName FROM HazardSetup WHERE HazardName = :hazard_name")
                    hazard_name_query.bindValue(":hazard_name", hazard_name)
                    if hazard_name_query.exec() and hazard_name_query.next():
                        hazard_name = hazard_name_query.value(0)
                        label.setText(hazard_name)
                    else:
                        # Handle error or default label text
                        label.setText("Unknown Hazard")

                    label.setFont(MyFont(10, True))

                    # Create the QVBoxLayout for the block
                    hazard_block = QVBoxLayout()
                    hazard_block.setContentsMargins(0,0,0,0)
                    hazard_block.setSpacing(2)

                    # Add the QLabel and QTableView to the block_layout
                    hazard_block.addWidget(label)
                    hazard_block.addWidget(new_table_view, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

                    metric_comment_label = QLabel(f"\n Comment: ")
                    metric_comment_label.setFont(MyFont())
                    metric_comment_label.setWordWrap(True)  # Enable word wrapping
                    metric_comment = QTextEdit()
                    metric_comment.setAcceptRichText(True)
                    metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
                    metric_comment.setFixedHeight(60)
                    metric_comment.setFont(MyFont())
                    metric_comment.setStyleSheet("background-color: white;")

                    hazard_block.addWidget(metric_comment_label)
                    hazard_block.addWidget(metric_comment)

                    # Add the block_widget to the scroll_layout within the scroll area
                    scroll_layout.addLayout(hazard_block)

                    # Store the new hazard data in the list
                    hazard_data.append((hazard_name, new_model, nr_classes))

            vertical_spacer2 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
            scroll_layout.addItem(vertical_spacer2)
        else:
            print(f"Error retrieving hazards: {queryAnswers.lastError().text()}")

        # Find the index of the page with the desired pageName
        index = -1
        for i in range(StackedWidget.count()):
            page = StackedWidget.widget(i)
            if page.property("pageName") == "2.2.1":
                index = i
                break

        # Check if the page was found
        if index != -1:
            # Access the desired page
            page = StackedWidget.widget(index)

            # Access the scroll_layout within the page
            scroll_layout = page.layout().itemAt(1).widget().widget().layout()

            # Set the scroll area as the central widget of the page
            page.layout().itemAt(1).widget().setWidget(scroll_area)

        else:
            print("Page with pageName '2.2.1' not found.")

def main():
    global REFUSS_DB, ANSWERS_DB

    REFUSS_DB = QSqlDatabase.addDatabase("QSQLITE", "Connection1")
    ANSWERS_DB = QSqlDatabase.addDatabase("QSQLITE", "Connection2")

    app = QApplication(sys.argv)

    WelcomePage = WelcomeWindow()
    WelcomePage.exec()

    REFUSSDatabasePath = 'database\REFUSS_V8.db'
    AnswersDatabasePath = WelcomePage.fileSelected
    Status = WelcomePage.Status

    M_OperateDatabases.establishDatabaseConnections([(REFUSS_DB, REFUSSDatabasePath),
                                                   (ANSWERS_DB, AnswersDatabasePath)
                                                   ])

    MainPage = MainWindow(Status)
    #Set initial size of the main window
    MainPage.resize(1280, 720)
    MainPage.show()

    atexit.register(M_OperateDatabases.closeDatabaseConnections, [REFUSS_DB, ANSWERS_DB])

    sys.exit(app.exec())

if __name__ == '__main__':
    main()