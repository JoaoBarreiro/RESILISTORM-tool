from operator import index
from pyexpat import model
import sys
import os
import pandas as pd
import numpy as np
from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton, QTreeWidget, QTreeWidgetItem,
                            QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton, QWidget,
                            QCheckBox, QLabel, QTextEdit, QStackedWidget, QLineEdit, QComboBox,
                            QScrollArea, QSizePolicy, QLayout, QFrame, QSpacerItem, QFileDialog, QTableView, QDialogButtonBox,
                            QMessageBox, QDialog, QStyledItemDelegate, QHeaderView, QListView, QMenu)
from PySide6.QtCore import Qt, QFile, QTextStream, Signal, QObject, Slot
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlRelationalTableModel, QSqlRelation
from PySide6.QtGui import QFont, QStandardItemModel, QStandardItem, QValidator, QIntValidator, QAction

from W_MainPage_V5_ui import Ui_MainWindow
from W_SetupWindow_ui import Ui_ScenarioSetup
from W_WelcomeWindow_ui import Ui_WelcomeWindow

from functools import partial

import atexit
import resources_rc
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from HorizontalBarPlot import MultiBarGraphWidget
from CircularPlotAnimated import CircularGraphWidget
from HorizontalScatterPlot import ScatterPlotWidget
from HazardClasses import ClassHazards, BuildingHazard

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, options, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.options = options


    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        if index.column() == 0:
            # Configure the editor for column 0 (Hazard Name)
            editor.addItems(self.options["Hazard Name"])
        elif index.column() == 1:
            # Configure the editor for column 1 (Unit of hazard classification)
            editor.addItems(self.options["Unit of hazard classification"])
        # Add conditions for other columns if needed
        return editor


    def setEditorData(self, editor, index):
        # Set the current value of the editor based on the model's data
        value = index.model().data(index, Qt.EditRole)
        editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        # Update the model's data when the editor value changes
        model.setData(index, editor.currentText(), Qt.EditRole)

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

class PerformanceSqlTableModel(QSqlTableModel):

    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 0:  # Make the first column read-only
            flags &= ~Qt.ItemFlag.ItemIsEditable
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
        self.ui = Ui_ScenarioSetup()
        self.ui.setupUi(self)
        
        #Set the headers
        if SetupTable == "HazardSetup":
            Label = "HAZARD SETUP"
            self.setWindowTitle("Hazard Setup Window")
        elif SetupTable == "ScenarioSetup":
            Label = "SCENARIO SETUP"
            self.setWindowTitle("Scenario Setup Window")

        self.SetupOption = SetupTable

        Label_font = QFont()
        Label_font.setPointSize(12)  # Set the font size explicitly
        Label_font.setBold(True)
        Label_font.setFixedPitch(True)  # Prevent font size resizing

        self.ui.SetupLabel.setText(Label)
        self.ui.SetupLabel.setFont(Label_font)

        self.populate_table(SetupTable)

        #Customize the TableView
        self.ui.SetupTableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.ui.SetupTableView.verticalHeader().setDefaultAlignment(Qt.AlignLeft)

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

            delegate = ComboBoxDelegate({"Hazard Name": fetch_from_database(REFUSS_DB, "HazardLibrary")["ShowName"],
                                         "Unit of hazard classification": ["%", "Area"]
                                         }
                                        )
            self.ui.SetupTableView.setItemDelegate(delegate)

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

class TableViewUpdater(QObject):
     updateTableViews = Signal()

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

        # Set associated function to buttons
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

        # Set menu actions
        self.ui.actionSave.triggered.connect(self.savefile)
        self.ui.actionSave_As.triggered.connect(self.savefile)
        self.ui.actionLoad.triggered.connect(self.loadfile)

        dimensions, objectives, criteria, metrics, metric_options = self.fetch_REFUSS_Database()

        # Populate the Tree Widgets with the Objectives and Criteria
        self.ui.Functional_list = self.findChild(QTreeWidget, "Functional_list")
        self.ui.Performance_list = self.findChild(QTreeWidget, "Performance_list")

        # Populate the dimension trees
        self.populate_dimension_tree(self.ui.Functional_list, 1)  # Assuming dimension 1 corresponds to Functional_list
        self.populate_dimension_tree(self.ui.Performance_list, 2)  # Assuming dimension 2 corresponds to Performance_list

        self.ui.Functional_list.setRootIsDecorated(False)
        self.ui.Performance_list.setItemsExpandable(False)

        # Expand tree widgets by default
        expand_all_tree_items(self.ui.Functional_list)
        expand_all_tree_items(self.ui.Performance_list)

        #Clean default MainWidgets pages
        CleanStackedWidget(self.ui.Functional_MainWidget)
        CleanStackedWidget(self.ui.Performance_MainWidget)

        # Connect the signals from the TreeWidgets to navigate through the pages
        self.ui.Functional_list.itemClicked.connect(self.on_tree_item_clicked)
        self.ui.Performance_list.itemClicked.connect(self.on_tree_item_clicked)

        # If new anaylisis makes sure to delete its answers is saving over existing database
        verify_AnswersDatabase()
        if Status == "New":
            FillNewAnswersDatabase(metrics)

        # Populate the Functional_MainWidget and Performance_MainWidget metrics from REFUSS_DB
        self.populate_with_objective_pages(objectives)
        self.populate_with_criterion_pages(criteria, metrics, metric_options)

        # Load available functional answers from ANSWERS_DB into the GUI
        load_answers(self.ui.Functional_MainWidget)
        
        # Load HazardTables from ANSWERS_DB into the GUI
        updateHazardTableViews(self.ui.Performance_MainWidget)

        # Performance Dimension buttons
        self.ui.HazardSU_btn.clicked.connect(partial(self.OpenSetupWindow, "HazardSetup"))
        self.ui.ScenarioSU_btn.clicked.connect(partial(self.OpenSetupWindow,"ScenarioSetup"))

    def OpenSetupWindow(self, SetupTable):
        self.setupwindow = SetupWindow(SetupTable)
        self.setupwindow.windowClosed.connect(self.onSetupWindowClosed)
        self.setupwindow.setWindowModality(Qt.WindowModal)
        self.setupwindow.setWindowFlags(self.setupwindow.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setupwindow.show()

    def onSetupWindowClosed(self, SetupTable):
        updatePerformanceTablesViews(self.models, self.table_views)
        updateHazardTableViews(self.ui.Performance_MainWidget)


        """
        # def updateHazardTableViews(QStackedWidget):

        #     self.NrHazards = countDatabaseRows(ANSWERS_DB, "HazardSetup")
        #     self.NrScenarios = countDatabaseRows(ANSWERS_DB, "ScenarioSetup")

        #     if self.NrHazards > 0 and self.NrScenarios > 0:
        #         query = QSqlQuery(ANSWERS_DB)
        #         if query.exec("SELECT HazardName, HazardClasses FROM HazardSetup"):
        #             self.hazard_data = []  # List to store hazard data

        #             # Create the QVBoxLayout for the scroll widget
        #             scroll_layout = QVBoxLayout()

        #             # Create the QWidget as the content widget for the scroll area
        #             scroll_widget = QWidget()
        #             scroll_widget.setLayout(scroll_layout)

        #             # Create a QScrollArea
        #             scroll_area = QScrollArea()
        #             scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget -> texto não corta
        #             scroll_area.setStyleSheet("QScrollArea { border: none; }")
        #             scroll_area.setWidget(scroll_widget)

        #             #Iterate over each hazard:
        #             while query.next():
        #                 hazard_name = str(query.value("HazardName"))
        #                 nr_classes = int(query.value("HazardClasses"))

        #                 # Check if the hazard already exists in the hazard data
        #                 hazard_exists = False
        #                 for existing_hazard_name, existing_model, existing_classes in self.hazard_data:
        #                     if hazard_name == existing_hazard_name:
        #                         hazard_exists = True
        #                         # Update the existing hazard model
        #                         existing_model.setTable("HazardAnswers")
        #                         existing_model.setFilter(f"HazardName = '{hazard_name}'")
        #                         existing_model.select()
        #                         # Update other properties of the hazard model if needed
        #                         break

        #                 if not hazard_exists:
        #                     # Create a new model for the new hazard
        #                     new_model = PerformanceSqlTableModel(db=ANSWERS_DB)
        #                     new_model.setTable("HazardAnswers")
        #                     new_model.setFilter(f"HazardName = '{hazard_name}'")
        #                     new_model.select()

        #                     # Set the ScenarioNames as row headers
        #                     new_model.setHeaderData(0, Qt.Vertical, "Scenario")

        #                     # Create a new QTableView for the new hazard
        #                     new_table_view = QTableView()
        #                     new_table_view.setModel(new_model)
        #                     # Customize the appearance of the new QTableView

        #                     # Find the index of the column that matches the HazardName
        #                     hazard_name_column_index = -1
        #                     for i in range(new_model.columnCount()):
        #                         column_name = new_model.headerData(i, Qt.Horizontal)
        #                         if column_name == "HazardName":
        #                             hazard_name_column_index = i
        #                             break

        #                     # Hide the HazardName column
        #                     if hazard_name_column_index != -1:
        #                         new_table_view.setColumnHidden(hazard_name_column_index, True)

        #                     # Remove the unwanted columns from the view
        #                     for i in reversed(range(new_model.columnCount())):
        #                         column_name = new_model.headerData(i, Qt.Horizontal)
        #                         if column_name.startswith("Class"):
        #                             class_number = int(column_name[5:])  # Extract the class number from the column name
        #                             if class_number > nr_classes:
        #                                 new_table_view.hideColumn(i)

        #                     # Set the EditStrategy of the model
        #                     new_model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        #                     Hazard_font = QFont()
        #                     Hazard_font.setPointSize(10)
        #                     Hazard_font.setBold(True)
        #                     Hazard_font.setFixedPitch(True)

        #                     # Create the QLabel for the hazard name
        #                     label = QLabel()
        #                     hazard_name_query = QSqlQuery(ANSWERS_DB)
        #                     hazard_name_query.prepare("SELECT HazardName FROM HazardSetup WHERE HazardName = :hazard_name")
        #                     hazard_name_query.bindValue(":hazard_name", hazard_name)
        #                     if hazard_name_query.exec() and hazard_name_query.next():
        #                         hazard_name = hazard_name_query.value(0)
        #                         label.setText(hazard_name)
        #                     else:
        #                         # Handle error or default label text
        #                         label.setText("Unknown Hazard")

        #                     label.setFont(Hazard_font)

        #                     # Create the QVBoxLayout for the block
        #                     hazard_block = QVBoxLayout()
        #                     hazard_block.setContentsMargins(0,0,0,0)
        #                     hazard_block.setSpacing(2)

        #                     # Add the QLabel and QTableView to the block_layout
        #                     hazard_block.addWidget(label)
        #                     hazard_block.addWidget(new_table_view, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        #                     #Add metric comment to block_layour
        #                     Comment_font = QFont()
        #                     Comment_font.setPointSize(10)  # Set the font size explicitly
        #                     Comment_font.setBold(False)
        #                     Comment_font.setFixedPitch(True)  # Prevent font size resizing

        #                     metric_comment_label = QLabel(f"\n Comment: ")
        #                     metric_comment_label.setFont(Comment_font)
        #                     metric_comment_label.setWordWrap(True)  # Enable word wrapping
        #                     metric_comment = QTextEdit()
        #                     metric_comment.setAcceptRichText(True)
        #                     metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
        #                     metric_comment.setFixedHeight(60)
        #                     metric_comment.setFont(Comment_font)
        #                     metric_comment.setStyleSheet("background-color: white;")

        #                     hazard_block.addWidget(metric_comment_label)
        #                     hazard_block.addWidget(metric_comment)

        #                     # Add the block_widget to the scroll_layout within the scroll area
        #                     scroll_layout.addLayout(hazard_block)

        #                     vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
        #                     scroll_layout.addItem(vertical_spacer)

        #                     # Store the new hazard data in the list
        #                     self.hazard_data.append((hazard_name, new_model, nr_classes))
        #         else:
        #             print(f"Error retrieving hazards: {query.lastError().text()}")

        #         # Find the index of the page with the desired pageName
        #         index = -1
        #         for i in range(self.ui.Performance_MainWidget.count()):
        #             page = self.ui.Performance_MainWidget.widget(i)
        #             if page.property("pageName") == "2.2.1":
        #                 index = i
        #                 break

        #         # Check if the page was found
        #         if index != -1:
        #             # Access the desired page
        #             page = self.ui.Performance_MainWidget.widget(index)

        #             # Access the scroll_layout within the page
        #             scroll_layout = page.layout().itemAt(1).widget().widget().layout()

        #             # Set the scroll area as the central widget of the page
        #             page.layout().itemAt(1).widget().setWidget(scroll_area)

        #         else:
        #             print("Page with pageName '2.2.1' not found.")

        #     return
        """
            
    def populate_with_objective_pages(self, objectives):

        Dimensions = ["Functional", "Performance"]

        for index, objective in objectives.iterrows():
            objective_id = objective["ObjectiveID"]
            objective_name = objective["ObjectiveName"]
            objective_description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."  # Replace with actual description

            page = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"Objective : {objective_id}"))
            layout.addWidget(QLabel(f"Objective Name: {objective_name}"))
            layout.addWidget(QLabel(f"Objective Description: {objective_description}"))

            #add spacer at the bottom
            vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addItem(vertical_spacer)

            page.setLayout(layout)

            page.setProperty("pageName", objective_id)

            if objective_id[0] == '1':
                self.ui.Functional_MainWidget.addWidget(page)
            elif objective_id[0] == '2':
                self.ui.Performance_MainWidget.addWidget(page)

    def populate_with_criterion_pages(self, criteria, metrics, metric_options):

        #Set criterion font
        Criterion_font = QFont()
        Criterion_font.setPointSize(12)
        Criterion_font.setBold(True)
        Criterion_font.setFixedPitch(True)

        self.models = []
        self.table_views = []

        criteria_sorted = criteria.sort_values(by = "CriteriaID", ascending = True)

        for index, criterion in criteria_sorted.iterrows():
            criterion_id = criterion["CriteriaID"]
            criterion_name = criterion["CriteriaName"]
            criterion_metrics = metrics[metrics['CriteriaID'] == criterion_id]

            if criterion_id.startswith('1'):
                Dimension = "F"
            else:
                Dimension = "P"

            criterion_id_label = Dimension + '.' + criterion_id[2:]

            Criterion_label = QLabel(f"Criterion {criterion_id_label}: {criterion_name}")
            Criterion_label.setFont(Criterion_font)
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
                answer_options = metric_options[metric_options["MetricID"] == metric_id]

                #add metric block to layout
                if metric_id[0] == '1':
                    metric_block = FunctionalMetricBlock(metric_id, metric_name, metric_question, answer_type, answer_options)
                elif metric_id[0] == '2':
                    metric_block, model, table_view = PerformanceMetricBlock(metric_id, metric_name, metric_question)
                    self.models.append(model)
                    self.table_views.append(table_view)
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

            page.setProperty("pageName", criterion_id)

            if Dimension == "F":
                self.ui.Functional_MainWidget.addWidget(page)
            elif Dimension == "P":
                self.ui.Performance_MainWidget.addWidget(page)

    def on_tree_item_clicked(self, item):
        tree_widget = self.sender()

        if tree_widget.indexOfTopLevelItem(item) == -1:
            # Second-level item selected
            self.navigate_to_page(item)
        else:
            # First-level item selected
            self.navigate_to_page(item)

    def navigate_to_page(self, item):
        item_id = item.data(0, Qt.UserRole)

        if item_id[0] == '1':
            self.access_page_by_name(self.ui.Functional_MainWidget, item_id)
        elif item_id[0] == '2':
            self.access_page_by_name(self.ui.Performance_MainWidget, item_id)

    def access_page_by_name(self, stacked_widget, page_name):
        for index in range(stacked_widget.count()):
            page = stacked_widget.widget(index)
            if page.property("pageName") == page_name:
                stacked_widget.setCurrentIndex(index)
                return True  # Page found and set as current
        return False  # Page not found

    def populate_dimension_tree(self, tree_widget, dimension_id):
        # Fetch objectives and criteria for the given dimension from the database
        objectives = self.fetch_objectives(dimension_id)
        criteria = self.fetch_criteria(dimension_id)

        # Clear the tree widget
        tree_widget.clear()

        Objective_font = QFont()
        Objective_font.setPointSize(9)  # Set the font size explicitly
        Objective_font.setBold(True)

        # Populate the tree widget with objectives and criteria
        for objective in objectives:
            objective_item = QTreeWidgetItem([f"{objective[1]} - {objective[2]}"])
            objective_item.setData(0, Qt.UserRole, objective[0])  # Store the ObjectiveID as data
            objective_item.setFont(0,Objective_font)
            tree_widget.addTopLevelItem(objective_item)

            for criterion in criteria:
                if criterion[0] == objective[0]:  # Check if the Criterion belongs to the Objective
                    criterion_item = QTreeWidgetItem([f"{objective[1]}.{criterion[2]} - {criterion[3]}"])
                    criterion_item.setData(0, Qt.UserRole, criterion[1])  # Store the CriterionID as data
                    objective_item.addChild(criterion_item)

    def fetch_REFUSS_Database(self):

        query = QSqlQuery(REFUSS_DB)

        dimension_query = ("SELECT * FROM Dimensions", "Dimensions")
        objectives_query = ("SELECT * FROM Objectives", "Objectives")
        criteria_query = ("SELECT * FROM Criteria", "Criteria")
        metrics_query = ("SELECT * FROM Metrics", "Metrics")
        metrics_options_query = ("SELECT * FROM MetricsOptions", "MetricsOptions")

        all_queries = [dimension_query,
                       objectives_query,
                       criteria_query,
                       metrics_query,
                       metrics_options_query]

        Results = []

        for option in all_queries:
            query.prepare(option[0])
            if query.exec():
                column_names = [query.record().fieldName(i) for i in range(query.record().count())]
                df = pd.DataFrame(columns=column_names)
                while query.next():
                    row_data = [query.value(i) for i in range(query.record().count())]
                    df.loc[len(df)] = row_data
                Results.append(df)
            else:
                error_message = query.lastError().text()
                print(f"Query execution failed: {error_message}")
                Results.append(None)

        return Results[0], Results[1], Results[2], Results[3], Results[4]

    def fetch_objectives(self, dimension_id):
        query = QSqlQuery(REFUSS_DB)
        query.prepare("SELECT ObjectiveID, ObjectiveSubID, ObjectiveName FROM Objectives WHERE DimensionID = ?")
        query.addBindValue(dimension_id)
        query.exec()

        objectives = []
        while query.next():
            objective_id = query.value(0)
            objective_subid = query.value(1)
            objective_name = query.value(2)
            objectives.append((objective_id, objective_subid, objective_name))
        return objectives

    def fetch_criteria(self, dimension_id):
        query = QSqlQuery(REFUSS_DB)
        query.prepare("""
            SELECT Objectives.ObjectiveID, Criteria.CriteriaID, Criteria.CriteriaSubID, Criteria.CriteriaName
            FROM Objectives
            JOIN Criteria ON Objectives.ObjectiveID = Criteria.ObjectiveID
            WHERE Objectives.DimensionID = ?
        """)
        query.addBindValue(dimension_id)
        query.exec()
        criteria = []
        while query.next():
            objective_id = query.value(0)
            criteria_id = query.value(1)
            criteria_subid = query.value(2)
            criteria_name = query.value(3)
            criteria.append((objective_id, criteria_id, criteria_subid, criteria_name))

        #self.cursor.execute(query, (dimension_id,))
        #criteria = self.cursor.fetchall()
        return criteria

    def fetch_all_criteria(self):
        query = QSqlQuery(REFUSS_DB)
        query.prepare("SELECT CriteriaID, CriteriaName FROM Criteria")
        query.exec()
        criteria = []
        while query.next():
            criteria_id = query.value(0)
            criteria_name = query.value(1)
            criteria.append((criteria_id, criteria_name))

        # self.cursor.execute(query)
        # criteria = self.cursor.fetchall()
        return criteria

    def fetch_criterion_details(self, criterion_id):
        query = QSqlQuery(REFUSS_DB)
        query.prepare("SELECT * FROM Criteria WHERE CriteriaID = ?")
        query.addBindValue(criterion_id)
        query.exec()
        if query.next():
            criterion = query.record()
            # Process the criterion record as needed
            return criterion
        # self.cursor.execute(query, (criterion_id,))
        # criterion = self.cursor.fetchone()
        return None

    def fetch_metrics(self, criterion_id):
        query = QSqlQuery(REFUSS_DB)
        query.prepare("""
            SELECT MetricID, MetricSubID, MetricName, MetricQuestion, Answer_Type
            FROM Metrics
            WHERE CriteriaID = ?
        """)
        metrics = []
        while query.next():
            metric_id = query.value(0)
            metric_subid = query.value(1)
            metric_name = query.value(2)
            metric_question = query.value(3)
            answer_type = query.value(4)
            metrics.append((metric_id, metric_subid, metric_name, metric_question, answer_type))

        # self.cursor.execute(query, (criterion_id,))
        # metrics = self.cursor.fetchall()
        return metrics

    def save_answers(self):

        Criteria_labels = ["Criterion F", "Criterion P"]
        Metric_labels = ["F", "P"]

        # Iterate over the Funcitonal pages
        for page_index in range(1, self.ui.Functional_MainWidget.count()):
            page_widget = self.ui.Functional_MainWidget.widget(page_index)
            page_layout = page_widget.layout()

        # Get the 1st label text and verify if it is a criterion page!
            page_widgets = getWidgetsFromLayout(page_layout)
            first_widget_label = page_widgets[0].text()

            if first_widget_label.startswith("Criterion"): #Page is a Criterion page:
                criteria_id = page_widget.property("pageName")

                #Access Page layout:
                # for index, i in enumerate(Criteria_labels): #Get the critera id (1st widget)
                #     if first_widget_label.startswith(i):
                #         criteria_id = first_widget_label.replace(i, str(index+1)).split(": ")[0]
                #         break

                #Access scroll area layout:
                scroll_area = page_widgets[1]
                scroll_widget = scroll_area.widget()
                scroll_widget_layout = scroll_widget.layout()

                #Iterate over each Metric Block in the scroll area layout:
                for index in range(scroll_widget_layout.count() - 1): #-1 to not iterate on QSpacerItem
                    #Access the metric block
                    metric_block = scroll_widget_layout.itemAt(index)
                    #Get Widgets within the block: metric label, metric question, "Comment:" and metris comment
                    metric_block_widgets = getWidgetsFromLayout(metric_block)

                    metric_label = metric_block_widgets[0].text()
                    for index, i in enumerate(Metric_labels):
                        if metric_label.startswith(i):
                            metric_id = metric_label.replace(i, str(index+1)).split(": ")[0]
                            break

                    comment = metric_block_widgets[-1].toPlainText()

                    if criteria_id[0] == '1':
                        #Access layout of metric answers
                        metric_block_answers_layout = getLayoutsFromLayout(metric_block)[0]
                        answer_options_layout_widgets = getWidgetsFromLayout(metric_block_answers_layout)

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

                        self.save_answer_to_database(metric_id, answer, comment)

    def clean_answers_from_AnswersDatabase(self):
        query = QSqlQuery(ANSWERS_DB)

        # Clean existing contents of the answers table
        query.exec("DELETE FROM MetricAnswers")

    def save_answer_to_database(self, metricID, new_answer, newcomment):

        query = QSqlQuery(ANSWERS_DB)
        query.prepare("UPDATE MetricAnswers SET answer = :answer, comment = :comment WHERE metricID = :metricID")
        query.bindValue(":metricID", metricID)
        query.bindValue(":answer", new_answer)
        query.bindValue(":comment", newcomment)
        query.exec()

    #Define functions to button behaviour:
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

        verify_AnswersDatabase()

        self.save_answers()
        return

    def loadfile(self):
        loadfile, _ = QFileDialog.getOpenFileName(self, 'Open File',dir = os.getcwd(), filter = '*.db')
        if loadfile:
            # ANSWERS_DB = loadfile
            load_answers(self.ui.Functional_MainWidget)
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
        self.UpdateDashboardPage()

    def closeEvent(self, event):
        super().closeEvent(event)



    def UpdateDashboardPage(self):

        #Get the all the data from answers and tables
        Objectives = fetch_from_database(REFUSS_DB, "Objectives")

        Metrics = fetch_from_database(REFUSS_DB, "Metrics")
        MetricsOptions =fetch_from_database(REFUSS_DB, "MetricsOptions")

        ScenarioSetup = fetch_from_database(ANSWERS_DB, "ScenarioSetup")
        ScenarioMetrics = fetch_from_database(ANSWERS_DB, "ScenarioMetrics")
        MetricsAnswers = fetch_from_database(ANSWERS_DB, "MetricAnswers")
        
        HazardLibrary = fetch_from_database(REFUSS_DB, "HazardLibrary")
        HazardSetup = fetch_from_database(ANSWERS_DB, "HazardSetup")
        HazardAnswers = fetch_from_database(ANSWERS_DB, "HazardAnswers")


        #TREAT FUNCTIONAL DATA
        Objectives = Objectives[Objectives["DimensionID"] == 1]

        ObjectivesID_List = (Objectives["ObjectiveID"].str.split(".").str[1] + " - " + Objectives["ObjectiveName"]).tolist()

        self.ObjectivesCompletness = Calculate_Completness(MetricsAnswers)

        self.ResilienceFunctionalRating, self.FunctionalObjectivesRating, self.FunctionalCriteriaRating = Calculate_FunctionalMetricsRating(Metrics, MetricsOptions, MetricsAnswers)

        updateQComboBox(self.ui.FCR_ComboBox, ObjectivesID_List)

        #UPDATE FUNCTIONAL PLOTS

        #update plot if combo box text is changed
        self.ui.FCR_ComboBox.currentTextChanged.connect(self.updateFCR)

        #initial empty combo box plot
        self.updateFCR()

        
        
        self.plotFunctionals(DataFrame = self.ObjectivesCompletness,
                             xScale = 100,
                             dataColumn = "MeanAnswerStatus",
                             yPrefix = "Obj. ",
                             DestinyWidget = self.ui.FDC_Widget)

        self.plotFunctionals(DataFrame = self.FunctionalObjectivesRating,
                             xScale = 1,
                             dataColumn = "MeanAnswerScores",
                             yPrefix = "Obj. ",
                             DestinyWidget = self.ui.FOR_Widget)

        self.plotResilienceCircle(round(self.ResilienceFunctionalRating.loc['1', "MeanResilience"], 2),
                                  DestinyWidget = self.ui.FRR_Widget)

        # PLOT EMPTY PERFROMANCE PLOTS:

        self.Scenarios_List = ScenarioMetrics["ScenarioName"].tolist()

        updateQComboBox(self.ui.PSS_ComboBox, self.Scenarios_List)

        self.ScenarioList_model = QStandardItemModel()
        self.ui.PSS_ScenarioList.setModel(self.ScenarioList_model)
        self.baseline_scenario = None
        
        #Rename ScenarioMetrics to match the rest
        new_column_names = {"M2111": "P.1.1.1",
                            "M2112": "P1.1.2",
                            "M2121": "P.1.2.1"
                            }  
        
        ScenarioMetrics.rename(columns=new_column_names, inplace=True)
        ScenarioMetrics.set_index("ScenarioName", inplace = True)
        
        PerformanceConsequencesRating = Caculate_PerformanceConsequencesRating(HazardLibrary, HazardSetup, HazardAnswers)
        
        self.PerformancePlots = []
        
        self.SPR_plot = self.plotPerformances(DataFrame = ScenarioMetrics, xScale = 1, DestinyWidget = self.ui.SPR_Widget)
        self.PerformancePlots.append(self.SPR_plot)
        
        self.SCR_plot = self.plotPerformances(DataFrame = PerformanceConsequencesRating, xScale = 1, DestinyWidget = self.ui.SCR_Widget)
        self.PerformancePlots.append(self.SCR_plot)
        
        self.ui.PSS_ComboBox.currentTextChanged.connect(self.onPSSComboBoxTextChanged)

        self.ScenarioList_model.dataChanged.connect(self.updateScatterVisibility)
        
        

    def onPSSComboBoxTextChanged(self):
        
        #If a baseline scenario already exists
        if self.baseline_scenario: 
            # Get the items that are selected on the QListView           
            self.additional_scenarios = getQListSelection(self.ScenarioList_model) 
            
            for plot in self.PerformancePlots:
                #turn off the current baseline scenario
                plot.update_series_visibility(self.baseline_scenario, False)                           
                if self.additional_scenarios:                                                   #if other scenarios are activated
                    for additional_scenario in self.additional_scenarios:
                        plot.update_series_visibility(additional_scenario, False)        #turn off those scenarios

        new_baseline_scenario = self.ui.PSS_ComboBox.currentText()                       #set the new baseline scenario from the ComboBox text
        if new_baseline_scenario:                                                           #update the items to be shown on the QListView
            updateQListView(ListView=self.ui.PSS_ScenarioList,
                            Model=self.ScenarioList_model,
                            Data=self.Scenarios_List,
                            Exclude=new_baseline_scenario)
            for plot in self.PerformancePlots:
                plot.update_series_visibility(new_baseline_scenario, True)             #activate the nre baseline scenario on the plot
                plot.set_baseline_scenario(new_baseline_scenario)                      #give to the plot class the name of the baseline scenario

            # Store the new baseline scenario for the next update
            self.baseline_scenario = new_baseline_scenario                          #set the current baselinescenario from the new value for future changes

    def updateScatterVisibility(self, index):
        # Get the item from the model using the index
        item = self.ScenarioList_model.itemFromIndex(index)
        if not item:
            return

        # Get the series name and its new check state
        series_name = item.text()
        visibility = item.checkState() == Qt.Checked

        # Call the ScatterPlotWidget method to update the series visibility
        for plot in self.PerformancePlots:
            plot.update_series_visibility(series_name, visibility)

            if visibility == False:
                plot.clear_hlines_and_texts(series_name)

        # self.SPR_plot.canvas.draw()

    def plotFunctionals(self, DataFrame = pd.DataFrame, xScale = 100 or 1, dataColumn = str, yPrefix = str, DestinyWidget = QWidget):
        
        Categories = DataFrame.index.tolist()
        Categories = [yPrefix + element for element in Categories]

        if xScale == 100:
            Values = round(DataFrame[dataColumn], 0).astype(int).tolist()
        elif xScale == 1:
            Values = round(DataFrame[dataColumn].astype(float), 2).tolist()

        Graph_plotter = MultiBarGraphWidget(Categories, Values, xScale)

        layout = DestinyWidget.layout()
        if layout is None:
            layout = QVBoxLayout()
            DestinyWidget.setLayout(layout)
        else:
            layout.itemAt(0).widget().deleteLater()
            layout.itemAt(0).widget().setParent(None)

        layout.addWidget(Graph_plotter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
    def updateFCR(self):
        selected_text = self.ui.FCR_ComboBox.currentText()
        ObjectiveID = selected_text.split(" - ")[0]

        showing_FunctionalCriteriaRating = self.FunctionalCriteriaRating[self.FunctionalCriteriaRating.index.str.split(".").str[0] == ObjectiveID]

        self.plotFunctionals(DataFrame = showing_FunctionalCriteriaRating,
                             xScale = 1,
                             dataColumn = "MeanAnswerScores",
                             yPrefix = f"Crit. ",
                             DestinyWidget = self.ui.FCR_Widget)

        return

    def plotResilienceCircle(self, ResilienceValue: float, DestinyWidget: QWidget):

        Res_plotter = CircularGraphWidget(ResilienceValue)

        #Res_plotter.animateWedge()

        layout = DestinyWidget.layout()

        if layout is None:
            layout = QVBoxLayout()
            DestinyWidget.setLayout(layout)
        else:
            layout.itemAt(0).widget().deleteLater()

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(Res_plotter)
        

        return
        
    def plotPerformances(self, DataFrame:pd.DataFrame, xScale: int, DestinyWidget: QWidget,):
        
        ScatterPlotter = ScatterPlotWidget(DataFrame, xScale)

        layout = DestinyWidget.layout()
        
        if layout is None:
            layout = QVBoxLayout()
        else:
            # Remove any existing widget in the DestinyWidget
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        layout.addWidget(ScatterPlotter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        DestinyWidget.setLayout(layout)

        return ScatterPlotter

def updatePerformanceTablesViews(self, modelslist_list, tableviews_list):
    for tableview, model in zip(tableviews_list, modelslist_list):
        model.select()
    return


def updateQListView(ListView = QListView, Model = QStandardItemModel, Data = list, Exclude = None):

    Model.clear()
    # Check if the model is empty
    if Model.rowCount() == 0:
        # Populate the model with data
        for item in Data:
            if item != Exclude:
                item = QStandardItem(item)
                item.setCheckable(True)
                item.setCheckState(Qt.Unchecked)
                Model.appendRow(item)

    ListView.setModel(Model)

    ListView.show()

    return

def getQListSelection(QListModel):
    # Get the number of items in the table model
    num_items = QListModel.rowCount()

    # Iterate through the items and get the text of the checked items
    SelectedItems = []
    for row in range(num_items):
        item = QListModel.item(row)
        if item and item.checkState() == Qt.Checked:
            SelectedItems.append(item.text())

    return SelectedItems

def updateQComboBox(ComboBox = QComboBox, Data = list):

    ComboBox.clear()
    ComboBox.addItems(Data)

    return


def Caculate_PerformanceConsequencesRating(HazardLibrary: pd.DataFrame, HazardSetup: pd.DataFrame, HazardAnswers: pd.DataFrame):
    
    HazardAnswers.set_index("HazardName", inplace = True)
    HazardLibrary.set_index("ShowName", inplace = True)
    HazardSetup.set_index("HazardName", inplace = True)
    
    AvailableHazards = HazardAnswers.index.unique().tolist()
    AvailableScenarios = HazardAnswers["ScenarioName"].unique().tolist()
    
    AvailabeHazardsID = HazardLibrary.loc[HazardLibrary.index.isin(AvailableHazards), "ID"].tolist()
    
    PerformanceConsequenceRating = pd.DataFrame(columns = AvailableHazards, index = AvailableScenarios)
    
    for Hazard, row in HazardAnswers.iterrows():
        HazardID = HazardLibrary.loc[Hazard, "ID"]
        HazardUnit = HazardSetup.loc[Hazard, "HazardUnit"]
        NrClasses = HazardLibrary.loc[Hazard, "NrClasses"]
        
        row_Scenario = row[0]
        if HazardUnit == "%":
            AnswerType = 1
        elif HazardUnit == "Area":
            AnswerType = 2
        
        if HazardID in ["V1", "P1"]:
            classValues = row[1:1+NrClasses].astype(float).tolist()
            HazardResilience = ClassHazards(classValues, AnswerType, HazardID).calculateHazard()
            
        PerformanceConsequenceRating.loc[row_Scenario, Hazard] = HazardResilience
    
    column_names = dict(zip(AvailableHazards,AvailabeHazardsID))
    
    PerformanceConsequenceRating = PerformanceConsequenceRating.rename(columns = column_names)
            
    return PerformanceConsequenceRating

def Calculate_FunctionalMetricsRating(Metrics: pd.DataFrame, MetricsOptions: pd.DataFrame, MetricsAnswers:pd.DataFrame):

    def singlechoicescore(AnswerIndex = int, OptionsNumber = int):

        score = min(1, AnswerIndex/(OptionsNumber - 1))

        return round(score, 2)

    def multiplechoisescore(AnswersIndexes = list, OptionsNumber = int):

        if 0 in AnswersIndexes:
            score = 0
        else:
            score = len(AnswersIndexes)/(OptionsNumber - 1)   # -1 to not count the option index 0 (No, None, etc.)
        return round(score, 2)

    Metrics.set_index("MetricID", inplace = True)
    MetricsAnswers.set_index("metricID", inplace = True)
    MetricsOptions.set_index("MetricID", inplace = True)

    MetricsOptionsNumber = pd.DataFrame(index = Metrics.index, columns=['OptionsNumber'])

    for MetricID, row in MetricsOptions.iterrows():
        OptionsNr = 0
        for column_name, value in row.items():
            if value:
                OptionsNr += 1
        MetricsOptionsNumber.loc[MetricID, "OptionsNumber"] = OptionsNr

    MetricScore_df = pd.DataFrame(index = Metrics.index, columns=['AnswerScore'])

    for MetricID, row in MetricsAnswers.iterrows():
        answer_nr_options = MetricsOptionsNumber.loc[MetricID, "OptionsNumber"]
        if not row["answer"]:
            score = 0
        else:
            if Metrics.loc[MetricID, "Answer_Type"] == "Single choice":
                    answer_index = int(row["answer"].split("_")[0])
                    score = singlechoicescore(answer_index, answer_nr_options)

            elif Metrics.loc[MetricID, "Answer_Type"] == "Multiple choice":
                answer_indexes = []
                for answer in row["answer"].split(";"):
                    answer_indexes.append(int(answer.split("_")[0]))
                score = multiplechoisescore(answer_indexes, answer_nr_options)

        MetricScore_df.loc[MetricID, "AnswerScore"] = score

    df = pd.DataFrame(MetricScore_df)

    # Extract the Dimension and Objective from the MetricID
    df['Dimension'] = df.index.str.split('.').str[0]
    df['Objective'] = df.index.str.split('.').str[1]
    df['Criteria'] = df.index.str.split('.').str[1] + '.' + df.index.str.split('.').str[2]

    # Filter the dataframe for Dimension 1
    Functional_df = df[df['Dimension'] == '1']

    DimensionResileinceSummary_df = Functional_df.groupby('Dimension').agg({
        'AnswerScore': ['count', 'sum', 'mean']
    })

    DimensionResileinceSummary_df.columns = ['Count', 'SumAnswerScores', 'MeanResilience']

    # Group by Objective and calculate the summary statistics
    ObjectivesSummary_df = Functional_df.groupby('Objective').agg({
        'AnswerScore': ['count', 'sum', 'mean']
    })

    ObjectivesSummary_df.columns = ['Count', 'SumAnswerScores', 'MeanAnswerScores']

    # Group by Criteria and calculate the summary statistics
    CriteriaSummary_df = Functional_df.groupby('Criteria').agg({
        'AnswerScore': ['count', 'sum', 'mean']
    })

    CriteriaSummary_df.columns = ['Count', 'SumAnswerScores', 'MeanAnswerScores']

    return DimensionResileinceSummary_df, ObjectivesSummary_df, CriteriaSummary_df

def Calculate_Completness(MetricsAnswersDataFrame):

    MetricAnswerStatus_df = pd.DataFrame(columns=['MetricID', 'AnswerStatus'])

    for index, row in MetricsAnswersDataFrame.iterrows():
        if row["answer"]:
            MetricAnswerStatus_df.loc[len(MetricAnswerStatus_df)] = [row["metricID"], 1]
        else:
            MetricAnswerStatus_df.loc[len(MetricAnswerStatus_df)] = [row["metricID"], 0]

    df = pd.DataFrame(MetricAnswerStatus_df)

    # Extract the Dimension and Objective from the MetricID
    df['Dimension'] = df['MetricID'].str.split('.').str[0]
    df['Objective'] = df['MetricID'].str.split('.').str[1]

    # Filter the dataframe for Dimension 1
    filtered_df = df[df['Dimension'] == '1']

    # Group by Objective and calculate the summary statistics
    summary_df = filtered_df.groupby('Objective').agg({
        'MetricID': 'count',
        'AnswerStatus': ['sum', 'mean']
    })

    # Rename the columns
    summary_df.columns = ['Count', 'TotalAnswerStatus', 'MeanAnswerStatus']
    summary_df["MeanAnswerStatus"] = summary_df["MeanAnswerStatus"] * 100

    #print(summary_df)

    return summary_df

def countDatabaseRows(Database, TableName):

    query = QSqlQuery(Database)
    query.prepare(f"SELECT COUNT(*) FROM {TableName}")
    if query.exec():
        if query.next():
            row_count = query.value(0)
        return row_count
    return False

def FillNewAnswersDatabase(metrics):

    # Clean existing contents of the answers table
    tables = ANSWERS_DB.tables()
    query = QSqlQuery(ANSWERS_DB)
    for table in tables:
        query.exec(f"DELETE FROM {table}")

    query.clear()

    query = QSqlQuery(ANSWERS_DB)
    query.prepare("INSERT INTO MetricAnswers (criteriaID, metricID) VALUES (:value1, :value2)")

    MetricsID = metrics["MetricID"]
    CriteriaID = metrics["CriteriaID"]

    for metric, criteria in zip(MetricsID, CriteriaID):
        query.bindValue(":value1", criteria)
        query.bindValue(":value2", metric)
        query.exec()

    return

def fetch_from_database(Database, TableName):

    if not Database.isOpen():
        print("Failed to connect to the database.")
        sys.exit(1)

    query = QSqlQuery(Database)
    query.exec(f"SELECT * FROM {TableName}")

    # Create a pandas DataFrame to store the fetched data
    columns = []
    rows = []
    record = query.record()
    for i in range(record.count()):
        columns.append(record.fieldName(i))
    while query.next():
        row = [query.value(i) for i in range(record.count())]
        rows.append(row)
    df = pd.DataFrame(rows, columns=columns)

    return df

def fetch_functional_answers_from_database():

    query = QSqlQuery(ANSWERS_DB)

    # Implement the logic to fetch metrics for the given criterion from the database
    query.prepare("SELECT metricID, answer, comment FROM MetricAnswers")
    query.exec()

    rows = []
    while query.next():
        metricID = query.value(0)
        answer = query.value(1)
        comment = query.value(2)
        rows.append((metricID, answer, comment))

    answers_from_database = {}
    for row in rows:
        metricID, answer, comment = row
        if metricID in answers_from_database:
            answers_from_database[metricID].append([answer, comment])
        else:
            answers_from_database[metricID] = [answer, comment]

    return answers_from_database

def load_answers(Widget):

    answers_from_database = fetch_functional_answers_from_database()

    # Iterate over the pages
    for page_index in range(1, Widget.count()):
        page_widget = Widget.widget(page_index)
        page_layout = page_widget.layout()

    # Get the 1st label text and verify if it is a criterion page!
        page_widgets = getWidgetsFromLayout(page_layout)
        first_widget_label = page_widgets[0].text()

        Criteria_labels = ["Criterion F", "Criterion P"]
        Metric_labels = ["F", "P"]

        if first_widget_label.startswith("Criterion"): #Page is a Criterion page:
            #Access Page layout:
            for index, i in enumerate(Criteria_labels): #Get the critera id (1st widget)
                if first_widget_label.startswith(i):
                    criteria_id = first_widget_label.replace(i, str(index+1)).split(": ")[0]
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
                metric_block_widgets = getWidgetsFromLayout(metric_block)

                metric_label = metric_block_widgets[0].text()
                for index, i in enumerate(Metric_labels):
                    if metric_label.startswith(i):
                        metric_id = metric_label.replace(i, str(index+1)).split(": ")[0]
                        break

                if metric_id[0] == '1':
                    #Assign comment form answers
                    comment = answers_from_database[metric_id][1]
                    metric_block_widgets[-1].setText(comment)

                    #Access layout of metric answers
                    metric_block_answers_layout = getLayoutsFromLayout(metric_block)[0]
                    answer_options_layout_widgets = getWidgetsFromLayout(metric_block_answers_layout)

                    # Check the type of answer options
                    if isinstance(answer_options_layout_widgets[0], QLineEdit):  # Open answer question
                        answer = answers_from_database[metric_id][0]
                        answer_options_layout_widgets[0].setText(answer)

                    # Open answer question
                    elif isinstance(answer_options_layout_widgets[0], QRadioButton):  # Single choice question
                        answer = answers_from_database[metric_id][0].split('_')[0]
                        if answer != '':
                            for position, radio in enumerate(answer_options_layout_widgets):
                                if position == int(answer):
                                    radio.setChecked(True)

                    elif isinstance(answer_options_layout_widgets[0], QCheckBox):  # Multiple choice question
                        answers = []
                        for element in answers_from_database[metric_id][0].split(';'):
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

    MetricID_font = QFont()
    MetricID_font.setPointSize(10)  # Set the font size explicitly
    MetricID_font.setBold(True)
    MetricID_font.setFixedPitch(True)  # Prevent font size resizing

    MetricLabels_font = QFont()
    MetricLabels_font.setPointSize(10)  # Set the font size explicitly
    MetricLabels_font.setBold(False)
    MetricLabels_font.setFixedPitch(True)  # Prevent font size resizing


    # Create the widgets for the metric block (e.g., labels, answer widget)
    if metric_id.startswith('1'):
        Dimension = "F"
    else:
        Dimension = "P"
    metric_id_label = Dimension + '.' + metric_id[2:]


    metric_id_label = QLabel(f"{metric_id_label}: {metric_name}")
    metric_id_label.setFont(MetricID_font)
    metric_id_label.setWordWrap(True)  # Enable word wrapping

    metric_question_label = QLabel(f"Question: {metric_question}")
    metric_question_label.setFont(MetricLabels_font)
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
                        option_radio.setFont(MetricLabels_font)
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
                        option_checkbox.setFont(MetricLabels_font)
                        checkbox_group.addButton(option_checkbox)
                        OptionsLayout.addWidget(option_checkbox)
                        #Metric_block.addWidget(option_checkbox)

        elif answer_type == "Open":
            line_edit = QLineEdit()
            line_edit.setFont(MetricLabels_font)
            #Metric_block.addWidget(line_edit)
            OptionsLayout.addWidget(line_edit)
        else:
            return None  # Return None for unsupported answer types

        Metric_block.addLayout(OptionsLayout)

    #Add metric comment
    metric_comment_label = QLabel(f"\n Comment: ")
    metric_comment_label.setFont(MetricLabels_font)
    metric_comment_label.setWordWrap(True)  # Enable word wrapping
    metric_comment = QTextEdit()
    metric_comment.setAcceptRichText(True)
    metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
    metric_comment.setFixedHeight(60)
    metric_comment.setFont(MetricLabels_font)
    metric_comment.setStyleSheet("background-color: white;")

    Metric_block.addWidget(metric_comment_label)
    Metric_block.addWidget(metric_comment)

    # Connect signals and slots to handle selection within the metric block
    if answer_type == "Single choice":
        radio_group.buttonClicked.connect(lambda: handleSingleChoiceSelection(radio_group))
    elif answer_type == "Multiple choice":
        for i in range(Metric_block.count() - 1):  # Exclude the comment widgets
            widget = Metric_block.itemAt(i).widget()
            if isinstance(widget, QCheckBox):
                widget.clicked.connect(lambda: handleMultipleChoiceSelection(Metric_block))

    return Metric_block

def PerformanceMetricBlock(metric_id, metric_name, metric_question):

    MetricID_font = QFont()
    MetricID_font.setPointSize(10)  # Set the font size explicitly
    MetricID_font.setBold(True)
    MetricID_font.setFixedPitch(True)  # Prevent font size resizing

    MetricLabels_font = QFont()
    MetricLabels_font.setPointSize(10)  # Set the font size explicitly
    MetricLabels_font.setBold(False)
    MetricLabels_font.setFixedPitch(True)  # Prevent font size resizing

    # Create the widgets for the metric block (e.g., labels, answer widget)
    if metric_id.startswith('1'):
        Dimension = "F"
    else:
        Dimension = "P"
    metric_id_label = Dimension + '.' + metric_id[2:]

    metric_id_label = QLabel(f"{metric_id_label}: {metric_name}")
    metric_id_label.setFont(MetricID_font)

    metric_question_label = QLabel(f"Question: {metric_question}")
    metric_question_label.setFont(MetricLabels_font)
    metric_question_label.setWordWrap(True)  # Enable word wrapping

    # Create the layout for the metric block
    Metric_block = QVBoxLayout()
    Metric_block.setContentsMargins(0,0,0,0)
    Metric_block.setSpacing(2)

    Metric_block.addWidget(metric_id_label)
    Metric_block.addWidget(metric_question_label)

    if Dimension == "P":
        Setup_model = PerformanceSqlTableModel(db = ANSWERS_DB)
        Setup_model.setTable("ScenarioMetrics")

        # Set the columns to be displayed
        indicator_column_name = f"M{metric_id.replace('.', '')}"
        table_index = get_column_index(Setup_model, indicator_column_name)

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
        Setup_model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        # Create a QTableView and set the model
        table_view = QTableView()
        table_view.setModel(Setup_model)

        # Reset the view to reflect the changes
        #table_view.reset()

        # Set the delegate for the "Answer" column
        delegate = DecimalZeroOneDelegate()
        table_view.setItemDelegate(delegate)

        table_view.setStyleSheet("background-color: white;padding: 0px; margin: 0px;")

        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        table_view.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        Metric_block.addWidget(table_view, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    #Add metric comment
    metric_comment_label = QLabel(f"\n Comment: ")
    metric_comment_label.setFont(MetricLabels_font)
    metric_comment_label.setWordWrap(True)  # Enable word wrapping
    metric_comment = QTextEdit()
    metric_comment.setAcceptRichText(True)
    metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
    metric_comment.setFixedHeight(60)
    metric_comment.setFont(MetricLabels_font)
    metric_comment.setStyleSheet("background-color: white;")

    Metric_block.addWidget(metric_comment_label)
    Metric_block.addWidget(metric_comment)

    return Metric_block, Setup_model, table_view

def handleSingleChoiceSelection(button_group):
    selected_button = button_group.checkedButton()
    for button in button_group.buttons():
        if button != selected_button:
            button.setChecked(False)

def handleMultipleChoiceSelection(layout):
    selected_checkboxes = [widget for widget in getWidgetsFromLayout(layout) if isinstance(widget, QCheckBox) and widget.isChecked()]
    for widget in getWidgetsFromLayout(layout):
        if isinstance(widget, QCheckBox) and widget not in selected_checkboxes:
            widget.setChecked(False)

def expand_all_tree_items(tree_widget):
    def expand_recursive(item):
        item.setExpanded(True)
        for i in range(item.childCount()):
            child_item = item.child(i)
            expand_recursive(child_item)

    for i in range(tree_widget.topLevelItemCount()):
        top_level_item = tree_widget.topLevelItem(i)
        expand_recursive(top_level_item)

def getWidgetsFromLayout(layout):
    widgets = []
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget:
            widgets.append(widget)
    return widgets

def getLayoutsFromLayout(layout):
    layouts = []
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if isinstance(item.layout(), QVBoxLayout) or isinstance(item.layout(), QHBoxLayout):
            layouts.append(item.layout())
    return layouts

def updateHazardTableViews(StackedWidget):

    NrHazards = countDatabaseRows(ANSWERS_DB, "HazardSetup")
    NrScenarios = countDatabaseRows(ANSWERS_DB, "ScenarioSetup")

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
                    new_model = PerformanceSqlTableModel(db=ANSWERS_DB)
                    new_model.setTable("HazardAnswers")
                    new_model.setFilter(f"HazardName = '{hazard_name}'")
                    new_model.select()

                    # Set the ScenarioNames as row headers
                    new_model.setHeaderData(0, Qt.Vertical, "Scenario")

                    # Create a new QTableView for the new hazard
                    new_table_view = QTableView()
                    new_table_view.setModel(new_model)
                    # Customize the appearance of the new QTableView

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
                            class_number = int(column_name[5:])  # Extract the class number from the column name
                            if class_number > nr_classes:
                                new_table_view.hideColumn(i)

                    # Set the EditStrategy of the model
                    new_model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

                    Hazard_font = QFont()
                    Hazard_font.setPointSize(10)
                    Hazard_font.setBold(True)
                    Hazard_font.setFixedPitch(True)

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

                    label.setFont(Hazard_font)

                    # Create the QVBoxLayout for the block
                    hazard_block = QVBoxLayout()
                    hazard_block.setContentsMargins(0,0,0,0)
                    hazard_block.setSpacing(2)

                    # Add the QLabel and QTableView to the block_layout
                    hazard_block.addWidget(label)
                    hazard_block.addWidget(new_table_view, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

                    #Add metric comment to block_layour
                    Comment_font = QFont()
                    Comment_font.setPointSize(10)  # Set the font size explicitly
                    Comment_font.setBold(False)
                    Comment_font.setFixedPitch(True)  # Prevent font size resizing

                    metric_comment_label = QLabel(f"\n Comment: ")
                    metric_comment_label.setFont(Comment_font)
                    metric_comment_label.setWordWrap(True)  # Enable word wrapping
                    metric_comment = QTextEdit()
                    metric_comment.setAcceptRichText(True)
                    metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
                    metric_comment.setFixedHeight(60)
                    metric_comment.setFont(Comment_font)
                    metric_comment.setStyleSheet("background-color: white;")

                    hazard_block.addWidget(metric_comment_label)
                    hazard_block.addWidget(metric_comment)

                    # Add the block_widget to the scroll_layout within the scroll area
                    scroll_layout.addLayout(hazard_block)

                    vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
                    scroll_layout.addItem(vertical_spacer)

                    # Store the new hazard data in the list
                    hazard_data.append((hazard_name, new_model, nr_classes))
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

    return

def verify_AnswersDatabase():

    query = QSqlQuery(ANSWERS_DB)

    ######### QUERIES TO CREATE TABLES ##################

    if not query.exec("CREATE TABLE IF NOT EXISTS MetricAnswers ("
               "criteriaID TEXT, "
               "metricID TEXT PRIMARY KEY, "
               "answer TEXT, "
               "comment TEXT)"
               ):
        print(f"Error creating MetricAnswers table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS HazardSetup ("
               "HazardName TEXT PRIMARY KEY , "
               "HazardUnit TEXT, "
               "HazardComment TEXT)"
               ):
        print(f"Error creating HazardSetup table: {query.lastError().text()}")

    # if not query.exec("CREATE TABLE IF NOT EXISTS HazardSetup ("
    #            "HazardName TEXT PRIMARY KEY , "
    #            "HazardClasses INTEGER, "
    #            "HazardUnit TEXT, "
    #            "HazardComment TEXT)"
    #            ):
    #     print(f"Error creating HazardSetup table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS ScenarioSetup ("
               "ScenarioName TEXT PRIMARY KEY, "
               "ScenarioSystemConfig TEXT, "
               "ScenarioRainfall TEXT, "
               "ScenarioOutfall TEXT, "
               "ScenarioComment TEXT)"
               ):
        print(f"Error creating ScenarioSetup table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS ScenarioMetrics ("
               "ScenarioName TEXT PRIMARY KEY, "
               "M2111 TEXT, "
               "M2112 TEXT, "
               "M2121 TEXT, "
               "FOREIGN KEY (ScenarioName) REFERENCES ScenarioSetup (ScenarioName) ON DELETE CASCADE ON UPDATE CASCADE)"
               ):
        print(f"Error creating ScenarioMetrics table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS HazardAnswers ("
            "HazardName TEXT, "
            "ScenarioName TEXT, "
            "FOREIGN KEY (HazardName) REFERENCES HazardSetup (HazardName) ON DELETE CASCADE ON UPDATE CASCADE,"
            "FOREIGN KEY (ScenarioName) REFERENCES ScenarioSetup (ScenarioName) ON DELETE CASCADE ON UPDATE CASCADE)"
            ):
        print(f"Error creating HazardAnswers table: {query.lastError().text()}")

    for i in range(1, 11):
        query.exec(f"ALTER TABLE HazardAnswers ADD COLUMN Class{i} TEXT")


    ######### QUERIES TO UPDATE TABLES ##################

    query.exec("DROP TRIGGER IF EXISTS Upload_ScenarioName_at_ScenarioMetrics")
    if not query.exec("""
        CREATE TRIGGER Upload_ScenarioName_at_ScenarioMetrics
        AFTER INSERT ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            INSERT INTO ScenarioMetrics (ScenarioName) VALUES (NEW.ScenarioName);
        END
    """):
        print(f"Error Upload_ScenarioName_at_ScenarioMetrics: {query.lastError().text()}")

    query.exec("DROP TRIGGER IF EXISTS Update_ScenarioName")
    if not query.exec("""
        CREATE TRIGGER Update_ScenarioName
        AFTER UPDATE OF ScenarioName ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            UPDATE ScenarioMetrics
            SET ScenarioName = NEW.ScenarioName
            WHERE ScenarioName = OLD.ScenarioName;

            UPDATE HazardAnswers
            SET ScenarioName = NEW.ScenarioName
            WHERE ScenarioName = OLD.ScenarioName;
        END
    """):
        print(f"Error Update_ScenarioName: {query.lastError().text()}")

    query.exec("DROP TRIGGER IF EXISTS Update_HazardName")
    if not query.exec("""
        CREATE TRIGGER Update_HazardName
        AFTER UPDATE OF HazardName ON HazardSetup
        FOR EACH ROW
        BEGIN
            UPDATE HazardAnswers
            SET HazardName = NEW.HazardName
            WHERE HazardName = OLD.HazardName;
        END
    """):
        print(f"Error Update_ScenarioName: {query.lastError().text()}")


    query.exec("DROP TRIGGER IF EXISTS Delete_Scenario")
    if not query.exec("""
        CREATE TRIGGER Delete_Scenario
        AFTER DELETE ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            DELETE FROM ScenarioMetrics
            WHERE ScenarioName = OLD.ScenarioName;

            DELETE FROM HazardAnswers
            WHERE ScenarioName = OLD.ScenarioName;
        END
    """):
        print(f"Error Delete_Scenario: {query.lastError().text()}")

    query.exec("DROP TRIGGER IF EXISTS Delete_Hazard")
    if not query.exec("""
        CREATE TRIGGER IF NOT EXISTS Delete_Hazard
        AFTER DELETE ON HazardSetup
        BEGIN
            DELETE FROM HazardAnswers
            WHERE HazardName = OLD.HazardName;
        END;
    """):
        print(f"Error Delete_Hazard: {query.lastError().text()}")


    ######### QUERIES FOR HAZARD ANSWERS TABLE UPDATE ##################

    query.exec("DROP TRIGGER IF EXISTS Insert_HazardAnswers_from_HazardSetup")
    if not query.exec("""
        CREATE TRIGGER IF NOT EXISTS Insert_HazardAnswers_from_HazardSetup
        AFTER INSERT ON HazardSetup
        BEGIN
            INSERT INTO HazardAnswers (HazardName, ScenarioName)
                SELECT NEW.HazardName, ScenarioName
                FROM ScenarioSetup;
        END;
    """):
        print(f"Error Insert_HazardAnswers_from_HazardSetup: {query.lastError().text()}")

    query.exec("DROP TRIGGER IF EXISTS Insert_HazardAnswers_from_ScenarioSetup")
    if not query.exec("""
        CREATE TRIGGER IF NOT EXISTS Insert_HazardAnswers_from_ScenarioSetup
        AFTER INSERT ON ScenarioSetup
        BEGIN
            INSERT INTO HazardAnswers (HazardName, ScenarioName)
                SELECT HazardName, NEW.ScenarioName
                FROM HazardSetup;
        END;
    """):
        print(f"Error Insert_HazardAnswers_from_ScenarioSetup: {query.lastError().text()}")

    ANSWERS_DB.commit()

def get_column_index(model, column_name):
    for i in range(model.columnCount()):
        if model.headerData(i, Qt.Horizontal) == column_name:
            return i
    return -1

def establishDatabaseConnections(REFUSSDatabasePath, AnswersDatabasePath):
    #REFUSS_DB = QSqlDatabase.addDatabase("QSQLITE", "Connection1")
    REFUSS_DB.setDatabaseName(REFUSSDatabasePath)
    if not REFUSS_DB.open():
        print(f"Error: Failed to open {REFUSSDatabasePath}")

    #ANSWERS_DB = QSqlDatabase.addDatabase("QSQLITE", "Connection2")
    ANSWERS_DB.setDatabaseName(AnswersDatabasePath)
    if not ANSWERS_DB.open():
        print(f"Error: Failed to open {AnswersDatabasePath}")
    return

def closeDatabaseConnections():
    if REFUSS_DB.isOpen():
        REFUSS_DB.close()
    if ANSWERS_DB.isOpen():
        ANSWERS_DB.close()

def CleanStackedWidget(QStackedWidget):
    #Remove all existing pages from the stacked widget
    while QStackedWidget.count() > 0:
        widget = QStackedWidget.widget(0)
        QStackedWidget.removeWidget(widget)

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

    establishDatabaseConnections(REFUSSDatabasePath, AnswersDatabasePath)

    MainPage = MainWindow(Status)
    #Set initial size of the main window
    MainPage.resize(1280, 720)
    MainPage.show()

    atexit.register(closeDatabaseConnections)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()