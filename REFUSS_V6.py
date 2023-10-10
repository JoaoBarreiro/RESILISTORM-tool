from operator import index
import sys
import os
import pandas as pd
from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton, QTreeWidget, QTreeWidgetItem,
                            QVBoxLayout, QButtonGroup, QRadioButton, QWidget,
                            QCheckBox, QLabel, QTextEdit, QStackedWidget, QLineEdit, QComboBox,
                            QScrollArea, QSizePolicy, QSpacerItem, QFileDialog, QTableView, QDialogButtonBox,
                            QMessageBox, QDialog, QStyledItemDelegate, QHeaderView, QMenu, QAbstractItemView,
                            QAbstractScrollArea, QStyleOptionButton, QStyle)
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtGui import QStandardItemModel, QValidator, QIntValidator, QAction

from W_MainPage_V5 import Ui_MainWindow
from W_SetupWindow_ui import Ui_HazardSetup
from W_WelcomeWindow import Ui_WelcomeWindow
from W_HazardB1 import Ui_SettingB1
from M_PerformanceSetup import Ui_ScenarioSetup

import M_OperateDatabases
import M_Operate_GUI_Elements
import M_PlotGraphs
import M_ResilienceCalculus
from M_Fonts import MyFont

from functools import partial

import atexit

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

class HazardSetupDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HazardSetupDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        
        #set the spacial case for the "Buildings Damage (B1)" hazard
        if index.column() == 1 and index.sibling(index.row(), 0).data() == "Buildings Damage (B1)":
            # Use the custom button-like delegate for column 1 when the text in column 0 is "Buildings Damage (B1)"
            editor = QPushButton("Setup", parent)
            editor.clicked.connect(self.openB1SetupWindow)  # Connect the button click to a custom slot
            return editor
        
        # Create a QComboBox editor for column 0 and 1 and its options
        elif index.column() in (0,1):
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

    def openB1SetupWindow(self):
        self.B1SetupWindow = B1SettingWindow()
        #self.B1SetupWindow.windowClosed.connect(self.onSetupWindowClosed)
        self.B1SetupWindow.setWindowModality(Qt.WindowModal)
        self.B1SetupWindow.setWindowFlags(self.B1SetupWindow.windowFlags() | Qt.WindowStaysOnTopHint)
        self.B1SetupWindow.show()        

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

class B1SettingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B1 Setting Window")
        self.ui = Ui_SettingB1()
        self.ui.setupUi(self)
        
        self.verifyDatabaseTable()
        
        # Create models for tables
        self.createTable_UserUses()

    def createTable_UserUses(self):
        # Ensure that the database connection is open before creating the model
        if not ANSWERS_DB.isOpen():
            QMessageBox.critical(self, "Database Error", "ANSWERS_DB is not open.")
            return
        
        # Define and set the model for UserUses_Table
        self.user_uses_model = QSqlTableModel(db = ANSWERS_DB)
        self.user_uses_model.setTable("B1Setup")
        self.user_uses_model.setEditStrategy(QSqlTableModel.OnFieldChange)
       
       # Fetch the data from the table
        if not self.user_uses_model.select():
            QMessageBox.critical(self, "Database Error", "Failed to fetch data from the table B1Setup.")
            return      
        
        self.user_uses_model.setHeaderData(0, Qt.Horizontal, "Custom building use")
        self.user_uses_model.setHeaderData(1, Qt.Horizontal, "Total size")
        self.user_uses_model.setHeaderData(2, Qt.Horizontal, "Methodology corresponding use")
                
        self.ui.UserUses_Table.setModel(self.user_uses_model)
        self.ui.UserUses_Table.resizeColumnsToContents()
        self.ui.UserUses_Table.setEditTriggers(QTableView.AllEditTriggers)
        
        # Set the delegate for the third column to use ComboBox
        self.ui.UserUses_Table.setItemDelegate(B1ComboBoxDelegate(self))
        self.ui.UserUses_Table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
        # Create context menu
        self.ui.UserUses_Table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.UserUses_Table.customContextMenuRequested.connect(self.showContextMenu)
        
        self.ui.Close_Button.clicked.connect(self.closeB1SettingWindow)
    
    def closeB1SettingWindow(self):
        confirm_dialog = QMessageBox.question(self, "Confirmation", "Do you want to close the window?", QMessageBox.Yes | QMessageBox.No)
        if confirm_dialog == QMessageBox.Yes:
            self.user_uses_model.select()
            self.close()

    def showContextMenu(self, pos):
        table = self.sender()  # Identify the table that triggered the event

        if table == self.ui.UserUses_Table:
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

        self.ui.UserUses_Table.reset()

    def removeCurrentRow(self):
        # Remove the current row from the table
        current_row = self.clicked_index.row()
        if current_row >= 0:
            self.user_uses_model.removeRow(current_row)
        self.user_uses_model.select()
        
    def verifyDatabaseTable(self):
        """criar tabela na database se não existir B1HazardSetup que vai ter apenas uma linha com as colunas:
            CustomUses : lista separada por ; com os tipos de edificio introduzidos pelo utilizador
            Residential, Commercial, Industrial (onde serão colocados os tipos definidos pelo utilizador corresponde)
            WaterDepths: lista separada por ; com os valores de profundidade de agua introduzidos pelo utilizador
        """    
        if not ANSWERS_DB.isOpen():
            QMessageBox.critical(None, "Database Error", "ANSWERS_DB is not open.")
        else:
            # Criar a tabela se ela não existir
            query = QSqlQuery(ANSWERS_DB)
            if not query.exec("CREATE TABLE IF NOT EXISTS B1Setup ("
                    "CostumUse TEXT, "
                    "TotalSize NUMERIC, "
                    "MethodologyClass TEXT)"
                ):
                print(f"Failed to create table B1Settings. {query.lastError().text()}")             

# class TableViewUpdater(QObject):
#      updateTableViews = Signal()

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
        self.dimensions, self.objectives, self.criteria, self.metrics, self.metric_options = M_OperateDatabases.getREFUSSDatabase(REFUSS_DB)

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

        # Populate the Functional_MainWidget and Performance_MainWidget metrics from REFUSS_DB
        self.populate_with_objective_pages()
        self.populate_with_criterion_pages()
        
        """
        Address Status (New or Old)
        """
        M_OperateDatabases.verifyAnswersDatabase(ANSWERS_DB)
        if Status == "New":
            # If new anaylisis, makes sure to delete its existing answers and save over existing database
            M_OperateDatabases.FillNewAnswersDatabase(ANSWERS_DB, self.metrics)
        if Status == "Old":
            # If old analysis, load available functional answers from ANSWERS_DB into the GUI
            load_FunctionalAnswers(self.ui.Functional_MainWidget)    
        
        """
        Load Performance and Hazard Tables with data from the ANSWERS_DB
        """   
        # Load Performance Tables from ANSWERS_DB into the GUI
        M_Operate_GUI_Elements.updatePerformanceTablesViews(self.PerformanceModels)
        
        # Load Hazard Tables from ANSWERS_DB into the GUI
        updateHazardTableViews(self.ui.Performance_MainWidget)

        # Performance Dimension buttons
        self.ui.HazardSU_btn.clicked.connect(partial(self.OpenSetupWindow, "HazardSetup"))
        self.ui.ScenarioSU_btn.clicked.connect(self.OpenScenarioSetup)

    def OpenSetupWindow(self, SetupTable):
        self.setupwindow = SetupWindow(SetupTable)
        self.setupwindow.windowClosed.connect(self.onSetupWindowClosed)
        self.setupwindow.setWindowModality(Qt.WindowModal)
        self.setupwindow.setWindowFlags(self.setupwindow.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setupwindow.show()
    
    def OpenScenarioSetup(self):
        self.ScenarioSetupWindow = Ui_ScenarioSetup(ANSWERS_DB)
        self.ScenarioSetupWindow.windowClosed.connect(self.onSetupWindowClosed)
        self.ScenarioSetupWindow.setWindowModality(Qt.WindowModal)
        #self.ScenarioSetupWindow.setWindowFlags(self.ScenarioSetupWindow.windowFlags() | Qt.WindowStaysOnTopHint)
        self.ScenarioSetupWindow.show()       

    def onSetupWindowClosed(self):
        M_Operate_GUI_Elements.updatePerformanceTablesViews(self.PerformanceModels)
        updateHazardTableViews(self.ui.Performance_MainWidget)

    def populate_with_objective_pages(self):
        """
        Populates the main widgets with objective pages based on the objectives retrived from the REFUSS_DB.

        """

        # Iterate over objectives
        for index, objective in self.objectives.iterrows():
            objective_id = objective["ObjectiveID"]
            objective_name = objective["ObjectiveName"]
            objective_description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."  # Replace with actual description

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
            if objective_id[0] == '1':
                self.ui.Functional_MainWidget.addWidget(page)
            elif objective_id[0] == '2':
                self.ui.Performance_MainWidget.addWidget(page)

    def populate_with_criterion_pages(self):
        """
        Populates the UI with criterion pages based on the criteria, metrics, and metric options retrieved from the REFUSS_DB.
        
        """
        
        #self.PerformanceModels is a list of the  
        self.PerformanceModels = []

        criteria_sorted = self.criteria.sort_values(by = "CriteriaID", ascending = True)

        for index, criterion in criteria_sorted.iterrows():
            criterion_id = criterion["CriteriaID"]
            criterion_name = criterion["CriteriaName"]
            criterion_metrics = self.metrics[self.metrics['CriteriaID'] == criterion_id]

            #Get the dimension based on the first character of the criterion_id
            if criterion_id.startswith('1'):
                Dimension = "F"
            else:
                Dimension = "P"

            #Generate the criterion label and assign the font and properties of the label
            Criterion_id_label = f"{Dimension}{criterion_id[2:]}"
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

            for index, metric in criterion_metrics_sorted.iterrows():
                metric_id = metric["MetricID"]
                metric_name = metric["MetricName"]
                metric_question = metric["MetricQuestion"]
                answer_type = metric["Answer_Type"]
                answer_options = self.metric_options[self.metric_options["MetricID"] == metric_id]

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
            page.setProperty("pageName", criterion_id)

            # Add the page to the corresponding main widget based on the dimension
            if Dimension == "F":
                self.ui.Functional_MainWidget.addWidget(page)
            elif Dimension == "P":
                self.ui.Performance_MainWidget.addWidget(page)

    def navigate_to_page(self, item):
        """
        Navigates to the page based on the item selected.

        Args:
            item: The selected item.

        Returns:
            None
        """
        item_id = item.data(0, Qt.UserRole)

        if item_id[0] == '1':
            M_Operate_GUI_Elements.access_page_by_name(self.ui.Functional_MainWidget, item_id)
        elif item_id[0] == '2':
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

        # Populate the tree widget with objectives and criteria
        for _, objective in self.objectives[self.objectives["DimensionID"] == dimension_id].iterrows():
            # Create an objective item with the objective name and description
            objective_item = QTreeWidgetItem([f"{objective['ObjectiveSubID']} - {objective['ObjectiveName']}"])
            objective_ID = objective["ObjectiveID"]
            objective_item.setData(0, Qt.UserRole, objective_ID)  # Store the ObjectiveID as data
            objective_item.setFont(0, MyFont(9, True))
            tree_widget.addTopLevelItem(objective_item)
            

            for _, criterion in self.criteria[self.criteria["ObjectiveID"] == objective_ID].iterrows():
                # Create a criterion item with the criterion name and description
                criterion_item = QTreeWidgetItem([f"{objective['ObjectiveSubID']}.{criterion['CriteriaSubID']} - {criterion['CriteriaName']}"])
                criterion_item.setData(0, Qt.UserRole, criterion['CriteriaID'])  # Store the CriterionID as data
                objective_item.addChild(criterion_item)

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

    ##################Define functions to button behaviour:
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
        self.ui.BodyWidget.setCurrentIndex(5)
        self.ui.TitlesWidget.setCurrentIndex(5)
        self.savefile()
        self.UpdateDashboardPage()

    def closeEvent(self, event):
        super().closeEvent(event)

    def UpdateDashboardPage(self):

        #Get the all the data from answers and tables and do some compatibilizations
        #Add ShortLabel and FullLabel to Objectives 
        Objectives = M_OperateDatabases.fetch_table_from_database(REFUSS_DB, "Objectives")
        Objectives["DimensionID"] = Objectives["DimensionID"].astype(int)
        Objectives["ObjectiveSubID"] = Objectives["ObjectiveSubID"].astype(int)
        Objectives["ShortLabel"] = ''
        Objectives["FullLabel"] = ''
        
        for index, row in Objectives.iterrows():
            if row["DimensionID"] == 1:
                DimensionLetter = "F"
            elif row["DimensionID"] == 2:
                DimensionLetter = "P"
            Objectives.at[index, "ShortLabel"] = f"Obj. {DimensionLetter}{row['ObjectiveSubID']}"
            Objectives.at[index,"FullLabel"] = f"{Objectives.at[index,'ShortLabel']} - {row['ObjectiveName']}"

        #Add ShortLabel and FullLabel to Criteria 
        Criteria = M_OperateDatabases.fetch_table_from_database(REFUSS_DB, "Criteria")
        Criteria["CriteriaSubID"] = Criteria["CriteriaSubID"].astype(int)
        Criteria["ObjectiveID"] = Criteria["ObjectiveID"].astype(str)
        Criteria["ShortLabel"] = ''
        Criteria["FullLabel"] = ''
        for index, row in Criteria.iterrows():
            Dimension = row["ObjectiveID"].split(".")[0]
            Objective = row["ObjectiveID"].split(".")[1]
            if Dimension == "1":
                DimensionLetter = "F"
            elif Dimension == "2":
                DimensionLetter = "P"
            Criteria.at[index,"ShortLabel"] = f"Crit. {DimensionLetter}{Objective}.{row['CriteriaSubID']}"
            Criteria.at[index,"FullLabel"] = f"{Criteria.at[index, 'ShortLabel']} - {row['CriteriaName']}"


        Metrics = M_OperateDatabases.fetch_table_from_database(REFUSS_DB, "Metrics")
        MetricsOptions = M_OperateDatabases.fetch_table_from_database(REFUSS_DB, "MetricsOptions")

        ScenarioSetup = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "ScenarioSetup")
        ScenarioMetrics = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "ScenarioMetrics")
        MetricsAnswers = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "MetricAnswers")
        
        HazardLibrary = M_OperateDatabases.fetch_table_from_database(REFUSS_DB, "HazardLibrary")
        HazardSetup = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "HazardSetup")
        HazardAnswers = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "HazardAnswers")

        #TREAT FUNCTIONAL DATA
        #1.FILTER OBJECETIVES TO GET ONLY FUNCTIONAL DIMENSION!
        Objectives = Objectives[Objectives["DimensionID"] == 1]
        
        # Calculate the FunctionalMetrics Answers completnesss
        ObjectivesCompletnessSummary = M_ResilienceCalculus.Calculate_Completness(MetricsAnswers)
        
        # Prepare ObjectivesCompletnessSummary to plot
        ObjectivesCompletness = pd.merge(Objectives, ObjectivesCompletnessSummary, left_on='ObjectiveSubID', right_on = "Objective", how='inner')
        ObjectivesCompletness = ObjectivesCompletness[['ShortLabel', 'FullLabel', 'ObjectiveSubID', 'ObjectiveID', 'Count', 'TotalAnswerStatus', 'MeanAnswerStatus']]

        # Calculate the FunctionalDimensionRating, FunctionalObjectivesRating and FunctionalCriteriaRating
        FunctionalDimensionRating, FunctionalObjectivesRating, FunctionalCriteriaRating = M_ResilienceCalculus.Calculate_FunctionalMetricsRating(Metrics, MetricsOptions, MetricsAnswers)

        # Prepare FunctionalObjectivesRating to plot
        FunctionalObjectivesRating["Objective"] = FunctionalObjectivesRating["Objective"].astype(int)
        FunctionalObjectivesRating = pd.merge(Objectives, FunctionalObjectivesRating, left_on='ObjectiveSubID', right_on = "Objective", how='inner')
        FunctionalObjectivesRating = FunctionalObjectivesRating[['ShortLabel', 'FullLabel', 'ObjectiveSubID', 'ObjectiveID', 'Count', 'SumAnswerScores', 'MeanAnswerScores']]

        # Prepare FunctionalCriteraRating to plot
        for index, row in FunctionalCriteriaRating.iterrows():
            FunctionalCriteriaRating.at[index, "Criterira"] = f"1.{row['Criteria']}"
        
        FunctionalCriteriaRating = pd.merge(Criteria, FunctionalCriteriaRating, left_on='CriteriaID', right_on = "Criterira", how='inner')
        FunctionalCriteriaRating = FunctionalCriteriaRating[['ShortLabel', 'FullLabel', 'CriteriaID', 'CriteriaSubID', 'Count', 'SumAnswerScores', 'MeanAnswerScores']]
        
        self.FunctionalCriteriaRating = FunctionalCriteriaRating

        # Set the FCR_ComboBox options
        ObjectivesID_List = ("F" + Objectives["ObjectiveID"].str.split(".").str[1] + " - " + Objectives["ObjectiveName"]).tolist()
        M_Operate_GUI_Elements.updateQComboBox(self.ui.FCR_ComboBox, ObjectivesID_List)
        
        # Plot the empty FCR plot at the begining
        #self.updateFCR()
        
        #Plot the FunctionalDimensionCompletness
        M_PlotGraphs.plotHorizontalBars(DataFrame = ObjectivesCompletness,
                             labelColumn = "FullLabel",
                             dataColumn = "MeanAnswerStatus",
                             xScale = 100,
                             DestinyWidget = self.ui.FDC_Widget,
                             MultiBar = False)

        #Plot the FunctionalObjectivesRating
        M_PlotGraphs.plotHorizontalBars(DataFrame = FunctionalObjectivesRating,
                             labelColumn = "FullLabel",
                             dataColumn = "MeanAnswerScores",
                             xScale = 1,
                             DestinyWidget = self.ui.FOR_Widget,
                             MultiBar = False)
        
        #update FCR plot if FCR_ComboBox if new objective is selected
        self.ui.FCR_ComboBox.currentTextChanged.connect(self.updateFCR)
                
        #Plot the FunctionalDimensionRating
        M_PlotGraphs.plotResilienceCircle(round(FunctionalDimensionRating.loc[FunctionalDimensionRating['Dimension'] == '1', 'MeanResilience'][0],2),
                                  DestinyWidget = self.ui.FRR_Widget)

        # PLOT EMPTY PERFROMANCE PLOTS:

        self.Scenarios_List = ScenarioMetrics["ScenarioName"].tolist()

        M_Operate_GUI_Elements.updateQComboBox(self.ui.PSS_ComboBox, self.Scenarios_List)
        
        self.baseline_scenario = None
        
        self.ScenarioList_model = QStandardItemModel()
        self.ui.PSS_ScenarioList.setModel(self.ScenarioList_model)
        
        #Rename ScenarioMetrics to match the rest
        new_column_names = {"M2111": "P1.1.1",
                            "M2112": "P1.1.2",
                            "M2121": "P1.2.1"
                            }  
        
        ScenarioMetrics.rename(columns=new_column_names, inplace=True)
        ScenarioMetrics.set_index("ScenarioName", inplace = True)
        
        PerformanceConsequencesRating = M_ResilienceCalculus.Caculate_PerformanceConsequencesRating(HazardLibrary, HazardSetup, HazardAnswers)
        
        #Create a list of plots to be updated on the run when the Scenario selection changes
        self.PerformancePlots = []
        
        self.SPR_plot = M_PlotGraphs.plotPerformances(DataFrame = ScenarioMetrics,
                                              xScale = 1,
                                              DestinyWidget = self.ui.SPR_Widget)
        
        self.PerformancePlots.append(self.SPR_plot)
        
        self.SCR_plot = M_PlotGraphs.plotPerformances(DataFrame = PerformanceConsequencesRating,
                                              xScale = 1,
                                              DestinyWidget = self.ui.SCR_Widget)
        self.PerformancePlots.append(self.SCR_plot)
        
        
        #Calculate each Scenario Resilience has the average of all performance and hazard metrics
        ScenariosPerformanceResilience = pd.merge(ScenarioMetrics, PerformanceConsequencesRating, left_index=True, right_index=True).astype(float).mean(axis=1)
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
        if new_baseline_scenario:                                                           #update the items to be shown on the QListView
            M_Operate_GUI_Elements.updateQListView(ListView = self.ui.PSS_ScenarioList,
                            Model = self.ScenarioList_model,
                            Data = self.Scenarios_List,
                            Exclude = new_baseline_scenario)
            for plot in self.PerformancePlots:
                plot.update_series_visibility(new_baseline_scenario, True)              #activate the new baseline scenario on the plot
                plot.set_baseline_scenario(new_baseline_scenario)                       #give to the plot class the name of the baseline scenario

            # Store the new baseline scenario for the next update
            self.baseline_scenario = new_baseline_scenario                              #set the current baselinescenario from the new value for future changes

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
            ObjectiveID = selected_text.split(" - ")[0].split("F")[1]
            showing_FunctionalCriteriaRating = self.FunctionalCriteriaRating[self.FunctionalCriteriaRating["CriteriaID"].str.startswith(f"1.{ObjectiveID}")]
            showing_FunctionalCriteriaRating.reset_index(inplace = True)
            
            M_PlotGraphs.plotHorizontalBars(DataFrame = showing_FunctionalCriteriaRating,
                                labelColumn = "FullLabel",
                                dataColumn = "MeanAnswerScores",
                                xScale = 1,
                                DestinyWidget = self.ui.FCR_Widget,                             
                                MultiBar = False)

        else:
            noob = pd.DataFrame([], columns=['Column1'])
            
            M_PlotGraphs.plotHorizontalBars(DataFrame = noob,
                    xScale = 1,
                    labelColumn = '',
                    dataColumn = "Column1",
                    DestinyWidget = self.ui.FCR_Widget,                             
                    MultiBar = True)      

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
            Options = Options.values.tolist()[0]

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
        Setup_model.setTable("ScenarioMetrics")

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

    REFUSSDatabasePath = 'database\REFUSS_V0.db'
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