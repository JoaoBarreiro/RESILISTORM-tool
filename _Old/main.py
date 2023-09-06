import sys
import os
import pandas as pd
from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton, QTreeWidget, QTreeWidgetItem,
                            QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton, QWidget,
                            QCheckBox, QLabel, QTextEdit, QStackedWidget, QLineEdit, QComboBox,
                            QScrollArea, QSizePolicy, QLayout, QFrame, QSpacerItem, QFileDialog, QTableView, QDialogButtonBox,
                            QMessageBox, QDialog, QStyledItemDelegate, QHeaderView)
from PySide6.QtCore import Qt, QFile, QTextStream, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtGui import QFont, QStandardItemModel, QStandardItem, QValidator, QIntValidator
import sqlite3
#from MainPage_ui import Ui_MainWindow
from MainPage_V3_ui import Ui_MainWindow
from W_SetupWindow_ui import Ui_ScenarioSetup
from W_WelcomeWindow_ui import Ui_WelcomeWindow
from functools import partial
import atexit
import resources_rc


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

class MetricsSqlTableModel(QSqlTableModel):
    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 0:  # Make the first column read-only
            flags &= ~Qt.ItemFlag.ItemIsEditable
        return flags

class HazardSetupSqlTableModel(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.column() == 1 and role == Qt.ItemDataRole.DisplayRole:
            value = super().data(index, role)
            return str(value) if value is not None else ""
        return super().data(index, role)

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.column() == 1 and role == Qt.ItemDataRole.EditRole:
            try:
                # Attempt to convert the value to an integer
                value = int(value)
                if value < 1 or value > 10:
                    # Value is outside the allowed range, return False to indicate failure
                    return False
            except ValueError:
                # Value is not a valid integer, return False to indicate failure
                return False

        # Call the base class setData() to perform the default behavior
        return super().setData(index, value, role)

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
        self.setWindowTitle("Welcome!")
        
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
        self.setWindowTitle("")
            
        #Set the headers
        if SetupTable == "HazardSetup":
            Label = "Hazard Setup"
        elif SetupTable == "ScenarioSetup":
            Label = "Scenario Setup"     
        
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
        #self.ui.buttonBox.accepted.connect(self.save_changes)
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
            headers = ["Hazard Name", "Number of hazard classes", "Unit of hazard classification", "Comment"]
        elif SetupCase == "ScenarioSetup":
            headers = ["Scenario Name", "System config.", "Rainfall", "Outfall Cond.", "Comment"]

        for i, header in enumerate(headers):
            self.model.setHeaderData(i, Qt.Horizontal, header)

        self.ui.SetupTableView.setModel(self.model)
        self.ui.SetupTableView.resizeColumnsToContents()
        self.ui.SetupTableView.setEditTriggers(QTableView.AllEditTriggers)
        
        # Create the delegate and apply it to the second column
        if SetupCase == "HazardSetup":
            delegate = IntRangeDelegate()
            self.ui.SetupTableView.setItemDelegateForColumn(1, delegate)


    def add_row(self):  
        # Get the number of rows in the model
        num_rows = self.model.rowCount()

        # Insert a new empty record at the end of the model
        record = self.model.record()
        record.setValue("ScenarioName", "NewScenario")
        self.model.insertRecord(num_rows, record)
        # Optional: Scroll to the newly added row
        self.ui.SetupTableView.scrollToBottom()
    
    def delete_row(self):
        # Get the selected row indatabasedices
        selection_model = self.ui.SetupTableView.selectionModel()
        selected_rows = selection_model.selectedRows()

        # Confirm deletion with the user
        reply = QMessageBox.question(self, "Delete Row", "Are you sure you want to delete the selected hazard?", QMessageBox.Yes | QMessageBox.No)
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

        # def save_changes(self):
        #     # Validate column values
        #     if self.SetupTableCase == "HazardSetup":
        #         for row in range(self.model.rowCount()):
        #             index = self.model.index(row, 1)  # Column index 1
        #             value = index.data()
        #             if not isinstance(value, int):
        #                 QMessageBox.warning(self, "Validation Error", "Number of hazard classes must be an integer!", QMessageBox.Ok)
        #                 return
            
        #     # Submit changes to the database
        #     if self.model.submitAll():
        #         QMessageBox.information(self, "Information", "Changes saved successfully!", QMessageBox.Ok)
        #         self.db.close()
        #         self.close()
        #     else:
        #         QMessageBox.critical(self, "Error", "Failed to save changes to the database.") 
    
    def closeSetupWindow(self):
        confirm_dialog = QMessageBox.question(self, "Confirmation", "Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if confirm_dialog == QMessageBox.Yes:     
            self.windowClosed.emit(self.SetupOption) 
            self.close()

class MainWindow(QMainWindow):
    def __init__(self, Status):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("REFUSS - V0")
        self.ui.home_btn.setChecked(True)

        # Set associated function to buttons
        self.ui.home_btn.clicked.connect(self.home_btn_toggled)
        self.ui.profile_btn.clicked.connect(self.profile_btn_toggled)
        self.ui.functional_btn.clicked.connect(self.functional_btn_toggled)
        self.ui.performance_btn.clicked.connect(self.performance_btn_toggled)
        self.ui.dashboard_btn.clicked.connect(self.dashboard_btn_toggled)
        
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
        
        # Expand tree widgets by default
        expand_all_tree_items(self.ui.Functional_list)
        expand_all_tree_items(self.ui.Performance_list)
        
        # Connect the signals from the TreeWidgets to navigate through the pages
        self.ui.Functional_list.itemClicked.connect(self.on_tree_item_clicked)
        self.ui.Performance_list.itemClicked.connect(self.on_tree_item_clicked)
        
        # # Remove all existing widgets from the stacked widget
        # while self.ui.MainWidget.count() > 0:
        #     widget = self.ui.MainWidget.widget(0) 
        #     self.ui.MainWidget.removeWidget(widget)      
        # # # # # # # # # # # # # # # # # # #
               
        # Populate the MainWidget with pages Objectives and criteria
        self.populate_with_objective_pages(objectives)
        self.populate_with_criterion_pages(criteria, metrics, metric_options)
        
        # Populate the MainWidget with the answers in the database
        if Status == "New":
            verify_AnswersDatabase()
        elif Status == "Old":
            load_answers(self.ui.MainWidget) 
                
        # Performance Dimension buttons
        self.ui.HazardSU_btn.clicked.connect(partial(self.OpenSetupWindow, "HazardSetup"))
        self.ui.ScenarioSU_btn.clicked.connect(partial(self.OpenSetupWindow,"ScenarioSetup"))

    def OpenSetupWindow(self, SetupTable):
        self.setupwindow = SetupWindow(SetupTable)
        self.setupwindow.windowClosed.connect(self.onSecondaryWindowClosed)
        self.setupwindow.setWindowModality(Qt.WindowModal)
        self.setupwindow.setWindowFlags(self.setupwindow.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setupwindow.show()
        
    def onSecondaryWindowClosed(self, SetupTable):
        # Call your function or perform any actions you want here
        self.updatePerformanceTables(self.models, self.table_views)

    def populate_with_objective_pages(self, objectives):
                
        for index, objective in objectives.iterrows():
            objective_id = objective["ObjectiveID"]
            objective_name = objective["ObjectiveName"]
            objective_description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."  # Replace with actual description

            page = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"Objective ID: {objective_id}"))
            layout.addWidget(QLabel(f"Objective Name: {objective_name}"))
            layout.addWidget(QLabel(f"Objective Description: {objective_description}"))
            page.setLayout(layout)

            self.ui.MainWidget.addWidget(page)
            page.setProperty("pageName", objective_id)

    def populate_with_criterion_pages(self, criteria, metrics, metric_options):
        
        #Set criterion font
        Criterion_font = QFont()
        Criterion_font.setPointSize(12) 
        Criterion_font.setFixedPitch(True) 
        
        self.models = []
        self.table_views = []
        
        for index, criterion in criteria.iterrows():
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
                
            # Populate the scroll layout with the metric blocks
            for index, metric in criterion_metrics.iterrows():               
                metric_id = metric["MetricID"]
                metric_name = metric["MetricName"]
                metric_question = metric["MetricQuestion"]
                answer_type = metric["Answer_Type"]
                answer_options = metric_options[metric_options["MetricID"] == metric_id]
                
                #add metric block to layout
                if metric_id[0] == '1':
                    metric_block = FunctionalMetricBlock(metric_id, metric_name, metric_question, answer_type, answer_options, ANSWERS_DB)
                elif metric_id[0] == '2':
                    metric_block, model, table_view = PerformanceMetricBlock(metric_id, metric_name, metric_question, answer_type, answer_options, ANSWERS_DB)
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
            
            self.ui.MainWidget.addWidget(page)
            
            page.setProperty("pageName", criterion_id)
                               
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

        self.access_page_by_name(self.ui.MainWidget, item_id)
        
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

        # Populate the tree widget with objectives and criteria
        for objective in objectives:
            objective_item = QTreeWidgetItem([f"{objective[1]} - {objective[2]}"])
            objective_item.setData(0, Qt.UserRole, objective[0])  # Store the ObjectiveID as data
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
        # self.cursor.execute(query, (dimension_id,))
        # objectives = self.cursor.fetchall()
        query.bindValue(0, dimension_id)
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
        query.bindValue(0, dimension_id)
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
        query.bindValue(0, criterion_id)
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
        
        self.clean_answers_from_database()
        
        # Iterate over the pages
        for page_index in range(5, self.ui.MainWidget.count()):
            page_widget = self.ui.MainWidget.widget(page_index)
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
                         
                                
                        self.save_answer_to_database(criteria_id, metric_id, answer, comment)       

    def clean_answers_from_database(self):
        
        # if not ANSWERS_DB.isOpen():
        #     if not ANSWERS_DB.open():
        #         print(f"Failed to open {ANSWERS_DB} connection")
        
        query = QSqlQuery(ANSWERS_DB)
        
        # Clean existing contents of the answers table
        query.exec("DELETE FROM MetricAnswers")
        
    def save_answer_to_database(self, criterionID, metricID, answer, comment):
        
        # if not ANSWERS_DB.isOpen():
        #     if not ANSWERS_DB.open():
        #         print(f"Failed to open {ANSWERS_DB} connection")
                        
        query = QSqlQuery(ANSWERS_DB)
        
        # # Clean existing contents of the answers table
        # query.exec("DELETE FROM MetricAnswers")
        
        # Insert current selected answers into the table
        query.prepare("INSERT INTO MetricAnswers (criteriaID, metricID, answer, comment) VALUES (?, ?, ?, ?)")
        query.addBindValue(criterionID)
        query.addBindValue(metricID)
        query.addBindValue(answer)
        query.addBindValue(comment)
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
            load_answers(self.ui.MainWidget)
        return
    
    def home_btn_toggled(self):
        self.ui.MainWidget.setCurrentIndex(0)
        self.ui.LeftWidget.hide()
        #self.ui.LeftWidget.setHidden(True)
    
    def profile_btn_toggled(self):
        self.ui.MainWidget.setCurrentIndex(1)
        self.ui.LeftWidget.hide()
        #self.ui.LeftWidget.setHidden(True)

    def functional_btn_toggled(self):
        self.ui.MainWidget.setCurrentIndex(2)
        #self.ui.LeftWidget.setHidden(False)
        self.ui.LeftWidget.show()
        self.ui.LeftWidget.setCurrentIndex(0)
    
    def performance_btn_toggled(self):
        self.ui.MainWidget.setCurrentIndex(3)
        self.ui.LeftWidget.show()
        self.ui.LeftWidget.setCurrentIndex(1)
        #self.updatePerformanceTables()
    
    def dashboard_btn_toggled(self):
        self.ui.MainWidget.setCurrentIndex(4)
        self.ui.LeftWidget.hide()
        #self.ui.LeftWidget.setHidden(True)

    def closeEvent(self, event):
        super().closeEvent(event)

    def updatePerformanceTables(self, modelslist_list, tableviews_list):
        for tableview, model in zip(tableviews_list, modelslist_list):
            model.select()
            #tableview.resizeColumnsToContents()
        return

def load_answers(Widget):
    
    def fetch_answers_from_database():
        
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
    
    answers_from_database = fetch_answers_from_database()

    # Iterate over the pages
    for page_index in range(5, Widget.count()):   #From 0 to 4 are default pages! (home, profile, dashboard, funtional)
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

def FunctionalMetricBlock(metric_id, metric_name, metric_question, answer_type, answer_options, ANSWERS_DB):     
    
    Metric_font = QFont()
    Metric_font.setPointSize(10)  # Set the font size explicitly
    Metric_font.setFixedPitch(True)  # Prevent font size resizing

    # Create the widgets for the metric block (e.g., labels, answer widget)
    if metric_id.startswith('1'):
        Dimension = "F"
    else:
        Dimension = "P"
    metric_id_label = Dimension + '.' + metric_id[2:]
    
    metric_id_label = QLabel(f"{metric_id_label}: {metric_name}")
    metric_id_label.setFont(Metric_font)
    metric_id_label.setWordWrap(True)  # Enable word wrapping
    
    metric_question_label = QLabel(f"Question: {metric_question}")
    metric_question_label.setFont(Metric_font)
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
                # Add the answer options as radio buttons to the layout
                for option in Options:
                    if option != '':
                        option_radio = QRadioButton(option)
                        option_radio.setFont(Metric_font)
                        radio_group.addButton(option_radio)
                        #Metric_block.addWidget(option_radio)
                        OptionsLayout.addWidget(option_radio)
                
            elif answer_type == "Multiple choice":
                checkbox_group = QButtonGroup()
                # Add the answer options as checkboxes to the layout
                for option in Options:
                    if option != '':
                        option_checkbox = QCheckBox(option)
                        option_checkbox.setFont(Metric_font)
                        checkbox_group.addButton(option_checkbox)
                        OptionsLayout.addWidget(option_checkbox)
                        #Metric_block.addWidget(option_checkbox)
            
        elif answer_type == "Open":
            line_edit = QLineEdit()
            line_edit.setFont(Metric_font)
            #Metric_block.addWidget(line_edit)
            OptionsLayout.addWidget(line_edit)
        else:
            return None  # Return None for unsupported answer types   
    
        Metric_block.addLayout(OptionsLayout)

    #Add metric comment
    metric_comment_label = QLabel(f"\n Comment: ")
    metric_comment_label.setFont(Metric_font)
    metric_comment_label.setWordWrap(True)  # Enable word wrapping
    metric_comment = QTextEdit()
    metric_comment.setAcceptRichText(True)
    metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
    metric_comment.setFixedHeight(60)
    metric_comment.setFont(Metric_font)
    
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

def PerformanceMetricBlock(metric_id, metric_name, metric_question, answer_type, answer_options, AnswersDatabase): 
    
    Metric_font = QFont()
    Metric_font.setPointSize(10)  # Set the font size explicitly
    Metric_font.setFixedPitch(True)  # Prevent font size resizing

    # Create the widgets for the metric block (e.g., labels, answer widget)
    if metric_id.startswith('1'):
        Dimension = "F"
    else:
        Dimension = "P"
    metric_id_label = Dimension + '.' + metric_id[2:]
    
    metric_id_label = QLabel(f"{metric_id_label}: {metric_name}")
    metric_id_label.setFont(Metric_font)
    metric_id_label.setWordWrap(True)  # Enable word wrapping
    
    metric_question_label = QLabel(f"Question: {metric_question}")
    metric_question_label.setFont(Metric_font)
    metric_question_label.setWordWrap(True)  # Enable word wrapping
    
    # Create the layout for the metric block
    Metric_block = QVBoxLayout()
    Metric_block.setContentsMargins(0,0,0,0)
    Metric_block.setSpacing(2)
    
    Metric_block.addWidget(metric_id_label)
    Metric_block.addWidget(metric_question_label)      

    if Dimension == "P":      
        Setup_model = MetricsSqlTableModel(db = ANSWERS_DB)
        Setup_model.setTable("ScenarioMetrics")
        Setup_model.select()
        
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
        
        # Set the second column to be editable
        Setup_model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
                
        # Create a QTableView and set the model
        table_view = QTableView()
        table_view.setModel(Setup_model)
        
        # Set the delegate for the "Answer" column
        delegate = DecimalZeroOneDelegate()
        table_view.setItemDelegate(delegate)

        # Set the column widths
        # table_view.setColumnWidth(0, 200)
        # table_view.setColumnWidth(1, 200)
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        Metric_block.addWidget(table_view)
    
    #Add metric comment
    metric_comment_label = QLabel(f"\n Comment: ")
    metric_comment_label.setFont(Metric_font)
    metric_comment_label.setWordWrap(True)  # Enable word wrapping
    metric_comment = QTextEdit()
    metric_comment.setAcceptRichText(True)
    metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
    metric_comment.setFixedHeight(60)
    metric_comment.setFont(Metric_font)
    
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

def verify_AnswersDatabase():

    query = QSqlQuery(ANSWERS_DB)

    # Create the tables if they don't exist
    query.exec("CREATE TABLE IF NOT EXISTS MetricAnswers ("
               "criteriaID TEXT, "
               "metricID TEXT, "
               "answer TEXT, "
               "comment TEXT)"
               )
    
    query.exec("CREATE TABLE IF NOT EXISTS HazardSetup ("
               "HazardName TEXT, "
               "HazardClasses INTEGER, "
               "HazardUnit TEXT, "
               "HazardComment TEXT)"
               )
    
    query.exec("CREATE TABLE IF NOT EXISTS ScenarioSetup ("
               "ScenarioName TEXT PRIMARY KEY, "
               "ScenarioSystemConfig TEXT, "
               "ScenarioRainfall TEXT, "
               "ScenarioOutfall TEXT, "
               "ScenarioComment TEXT)"
               )

    query.exec("CREATE TABLE IF NOT EXISTS ScenarioMetrics ("
               "ScenarioName TEXT PRIMARY KEY, "
               "M2111 TEXT, "
               "M2112 TEXT, "
               "M2121 TEXT, "
               "FOREIGN KEY (ScenarioName) REFERENCES ScenarioSetup (ScenarioName) ON DELETE CASCADE ON UPDATE CASCADE)"
               )
    
    # TABBLE HazardName tem de ser criada dependendo do número de hazards e de cenários! Diria uma tabela por hazard com os cenérios em coluna e a perigosidade em linha.
    # tem de ser fora daqui!
    
    query.exec("DROP TRIGGER IF EXISTS update_scenario_metrics")

    # Create the trigger for updating ScenarioMetrics on ScenarioSetup update
    query.exec("""
        CREATE TRIGGER update_scenario_metrics
        AFTER UPDATE OF ScenarioName ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            UPDATE ScenarioMetrics
            SET ScenarioName = NEW.ScenarioName
            WHERE ScenarioMetrics.ScenarioName = OLD.ScenarioName;
        END
    """)

    query.exec("DROP TRIGGER IF EXISTS delete_scenario_metrics")

    # Create the trigger for deleting ScenarioMetrics on ScenarioSetup delete
    query.exec("""
        CREATE TRIGGER delete_scenario_metrics
        AFTER DELETE ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            DELETE FROM ScenarioMetrics
            WHERE ScenarioMetrics.ScenarioName = OLD.ScenarioName;
        END
    """)

    query.exec("DROP TRIGGER IF EXISTS insert_scenario_metrics")

    # Create the trigger for inserting ScenarioMetrics on ScenarioSetup insert
    query.exec("""
        CREATE TRIGGER insert_scenario_metrics
        AFTER INSERT ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            INSERT INTO ScenarioMetrics (ScenarioName) VALUES (NEW.ScenarioName);
        END
    """)
    
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
    MainPage.show()
    
    atexit.register(closeDatabaseConnections)
    
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()