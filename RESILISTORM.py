import sys
import os
import shutil
import atexit
import pandas as pd

from PySide6.QtWidgets import (QMainWindow, QApplication, QTreeWidget, QTreeWidgetItem,
                            QVBoxLayout, QButtonGroup, QRadioButton, QWidget,
                            QCheckBox, QLabel, QTextEdit, QStackedWidget, QLineEdit,
                            QScrollArea, QSizePolicy, QSpacerItem,  QTableView, 
                             QDialog, QStyledItemDelegate, QHeaderView,  QAbstractItemView,
                            QAbstractScrollArea,   QFrame 
                            )
from PySide6.QtCore import Qt, Signal, QAbstractTableModel, QCoreApplication
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtGui import QValidator

from GUI_Python.W_MainPage_V7 import Ui_MainWindow

from M_WelcomeDialog import WelcomeDialog

from C_STUDY import STUDY

import M_OperateDatabases
import M_Operate_GUI_Elements
import M_PlotGraphs

import M_SituationManager
import M_WeightSetup
import M_PerformanceSetup

from M_Fonts import MyFont

class GeneralizedIndicatorModel(QAbstractTableModel):
    def __init__(self, database, indicators, rain_id, column_names, row_names=None):
        super(GeneralizedIndicatorModel, self).__init__()
        self.database = database
        self.indicators = indicators  # List of indicator IDs
        self.rain_id = rain_id
        self.column_names = column_names
        self.row_names = row_names if isinstance(row_names, dict) else {indicator: indicator for indicator in self.indicators}
        # self.row_names = row_names if row_names and len(row_names) == len(indicators) else indicators
        self.dirty = False
        self.data_dict = self.fetch_data()  # {(indicator_id, rain_id): {column_name: value}}
        #self.fetch_data()

    def fetch_data(self):
        data_dict = {}
        for indicator_id in self.indicators:
            table_name = indicator_id  # Use IndicatorID as the table name
            query = QSqlQuery(self.database)
            if query.exec(f"SELECT * FROM {table_name} WHERE RainfallID = {self.rain_id}"):
                while query.next():
                    record = query.record()
                    for column_name in self.column_names:
                        value = record.value(column_name)
                        data_dict[(indicator_id, self.rain_id)] = data_dict.get((indicator_id, self.rain_id), {})
                        data_dict[(indicator_id, self.rain_id)][column_name] = value
            else:
                print("Query execution failed in fetch_data:", query.lastError().text())
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
            value = self.data_dict.get((indicator_id, self.rain_id), {}).get(column_name, "")
            return value if role == Qt.DisplayRole else str(value)
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                indicator_id = self.indicators[section]
                return str(self.row_names.get(indicator_id, indicator_id))
                # return str(self.row_names[section])
            elif orientation == Qt.Horizontal:
                return str(self.column_names[section])
        return None

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            indicator_id = self.indicators[index.row()]
            column_name = self.column_names[index.column()]

            key = (indicator_id, self.rain_id)

            if key not in self.data_dict.keys():
                self.data_dict[key] = {}  # Create a dictionary for the indicator/scenario pair


            table_name = indicator_id  # Use IndicatorID as the table name
            # Start the transaction
            self.database.transaction()

            query = QSqlQuery(self.database)
            if not query.exec(f"UPDATE {table_name} SET '{column_name}' = {float(value)} WHERE RainfallID = {self.rain_id}"):
                print("Query execution failed in setData:", query.lastError().text())
                # Handle update failure
                self.database.rollback()
                return False

            if not self.database.commit():
                print(f'Error on database commitment for table {table_name}')
                error = self.database.lastError().text()
                print(f'Database error details: {error}')
                return False

            key = (indicator_id, self.rain_id)

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
                            new_value = self.data_dict.get((indicator_id, self.rain_id), {}).get(column_name)
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
                            query.addBindValue(self.rain_id)
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

class MainWindow(QMainWindow):
    
    updateWeights = Signal()
    updateStudy = Signal()
    
    def __init__(self, STUDY: STUDY):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("RESILISTROM tool - V0")

        self.STUDY = STUDY

        self.set_inital_view()
        self.set_menu_buttons_behaviour()
        self.set_functional_treewidget()
        self.set_functional_mainwidget()
        self.set_analysis_manager()
        self.set_performance_rainfall_combobox()
        self.set_dashboard_functionalcriteria_combobox()
        
        self.initialize_performance_variables()
     
    def set_inital_view(self):  
        # Set initial view of the window
        self.ui.LeftMenuFrame.setHidden(True)
        self.ui.menu_btn.setChecked(True)
        self.ui.menu_btn_2.setChecked(True)
        self.ui.home_btn_2.setChecked(True)
        self.BodyWidget_index = 0
        self.ui.BodyWidget.setCurrentIndex(self.BodyWidget_index)
        # RECEIVE SIGNAL WHEN CHANGING BODY WIDGET, namely ANALYSIS MANAGER
        self.ui.BodyWidget.currentChanged.connect(self.update_study)
    
    def set_menu_buttons_behaviour(self):
        # Set associated function to left menu buttons
        self.ui.home_btn.clicked.connect(self.home_btn_toggled)
        self.ui.home_btn_2.clicked.connect(self.home_btn_toggled)

        self.ui.profile_btn.clicked.connect(self.profile_btn_toggled)
        self.ui.profile_btn_2.clicked.connect(self.profile_btn_toggled)

        self.ui.analysis_btn.clicked.connect(self.analysis_btn_toggled)
        self.ui.analysis_btn_2.clicked.connect(self.analysis_btn_toggled)

        self.ui.functional_btn.clicked.connect(self.functional_btn_toggled)
        self.ui.functional_btn_2.clicked.connect(self.functional_btn_toggled)

        self.ui.performance_btn.clicked.connect(self.performance_btn_toggled)
        self.ui.performance_btn_2.clicked.connect(self.performance_btn_toggled)

        self.ui.dashboard_btn.clicked.connect(self.dashboard_btn_toggled) 
        self.ui.dashboard_btn_2.clicked.connect(self.dashboard_btn_toggled)

    def set_functional_treewidget(self):
        """
        SET FUNCTIONAL TREE WIDGET
        """
        # Define and populate the Tree Widgets with the Objectives and Criteria
        self.ui.Functional_list = self.findChild(QTreeWidget, "Functional_list")

        self.populate_functional_tree(self.ui.Functional_list)
        
        # Romeve small arrow on the left of the tree widget parent item
        self.ui.Functional_list.setRootIsDecorated(False)

        # Expand tree widgets by default
        M_Operate_GUI_Elements.expand_all_tree_items(self.ui.Functional_list)

        # Connect the signals from the TreeWidgets to navigate through the pages
        self.ui.Functional_list.itemClicked.connect(self.navigate_to_page)

    def set_functional_mainwidget(self):
        """
        SET MAIN FUNCTIONAL WIDGET
        """
        #Clean default MainWidgets pages
        M_Operate_GUI_Elements.CleanStackedWidget(self.ui.Functional_MainWidget)

        # Populate the Functional_MainWidget with objectives and criteria from RESILISTORM_DB
        self.populate_Functional_objective_pages()

        self.FunctionalMetricBlocks = {}
        self.populate_Functional_criterion_pages()

    def set_analysis_manager(self):
        """
        SET ANALYSIS MANAGER
        """
        
        # SET SITUATION MANAGER
        self.SituationSetup = M_SituationManager.ListEditor(self.ui.Situation_setup_Content_WidgetLayout,
                                                           self.STUDY.Study_db)
        self.SituationGenerator = M_SituationManager.SituationGenerator(self.ui.Situation_generator_Content_WidgetLayout,
                                                                       self.SituationSetup,
                                                                       self.STUDY.Study_db)
        
        #update_situation_comboboxb based on the changes in the SituationGenerator
        self.SituationGenerator.situationModified.connect(self.update_modified_situation)  
   
        self.update_situation_combobox_list()
        self.ui.Situation_selection_Combobox.currentTextChanged.connect(self.set_selected_situation)

        # SET WEIGHT SETUP
        self.WeightsSetup = M_WeightSetup.WeightSetup(self.STUDY.Study_db)
        self.ui.Manager_Page2_Layout.addWidget(self.WeightsSetup)
        
        self.manager_tab = self.ui.Manager_TabWidget.currentWidget()
        self.ui.Manager_TabWidget.currentChanged.connect(self.weight_setup_verifier)
        
        # SET PERFORMANCE SETUP
        self.get_study_IndicatorsSetup()

        self.Indicators_selector_Widget = M_PerformanceSetup.IndicatorsSelection(self.STUDY.IndicatorsClassesLibrary,
                                                                                 self.STUDY.IndicatorsLibrary,
                                                                                 self.STUDY.IndicatorsSetup,
                                                                                 self.STUDY.Study_db)

        self.ui.Indicators_selector_FrameLayout.addWidget(self.Indicators_selector_Widget)

        self.Indicators_properties_Widget = M_PerformanceSetup.PerformanceSetup(self.STUDY.Methodology_db,
                                                                                self.STUDY.Study_db,
                                                                                self.Indicators_selector_Widget)

        self.ui.Indicators_setup_FrameLayout.addWidget(self.Indicators_properties_Widget)
        
        self.Indicators_properties_Widget.CustomBuilding.building_uses_modified.connect(self.update_buidling_uses)


        # Initialize current situation as empty situation
        self.set_selected_situation() # to get the initial situation selected in the combobox, i.e., None -> can only be called after setting the functional widget
     
    def initialize_performance_variables(self):
        """
        INITIALIZE PERFORMANCE RELATED VARIABLES        
        """
        # The scenario pages layout will have a widget for all the possible Classes and Indicators
        # If the Class has a selected indicator the respective Widget of the class is shown,
            # otherwise it is hidden
        # If the indicator within a given class is selected, the respective widget is shown,
            # otherwise it is hidden
        # When calculating Performance Resilience, only selceted indicators must be considered

        # Initialize dictionary containing as keys the IndicatorsClasses from the ConsequencesLibrary
            # and as values the selected IndicatorsIDs of each class (generaly, classes only allow 1 indicator)
            # Updated when the IndicatorSelection window is closed
        self.selected_indicators = self.Indicators_selector_Widget.selected_indicators

        # Initialize dictionary containg as keys the scenarioIDs
            # and as values a dict containing the IndicatorIDs as keys and
            # the respective models as value, to be later accessed and easily updated
        # Created when initializing the GUI and updated a new scenario is created/deleted
        self.scenario_models = {}

        # Initialize dictionary containing as keys the ScenarioIDs
            # and as values a dict containing the IndicatorIDs as keys
            # and the respective widget,  to be later accessed and allow to hide/show the widgets
            # according to the selected IndicatorIDs
            # e.g. {'ScenarioID1': {'IndicatorID1': widget1, 'Indicatorweight_setup_verifierself.ID2': widget2, etc.}}
        # Created when initializing the GUI and updated when selected_indicators changes
            # by showing/hiding the widgets of the selected/deselected indicators
        self.scenario_pages = {}

    def set_performance_rainfall_combobox(self):
        # Populate the Performance_MainWidget with rainfall-RP from ANSWERS_DB
        self.ui.Rainfall_selection_ComboBox.currentTextChanged.connect(self.update_performance_page)

    def set_dashboard_functionalcriteria_combobox(self):
        #Set the Objectives list into the Functional Criteira Rating Combobox
        functional_objectives = self.STUDY.objectives[self.STUDY.objectives["DimensionID"]==1]
        ObjectivesID_List = ("S" + functional_objectives["ObjectiveSubID"].astype(str) + " - " + functional_objectives["ObjectiveName"]).tolist()
        M_Operate_GUI_Elements.updateQComboBox(self.ui.FCR_ComboBox, ObjectivesID_List)
        
        #Update Functional Criteria Rating plot when FCR_ComboBox changes
        self.ui.FCR_ComboBox.currentTextChanged.connect(self.updateFCR)        

    def weight_setup_verifier(self):

        if self.manager_tab == 1:
            result = self.WeightsSetup.on_tab_changed()
            if result == False:
                # Disconnect the signal temporarily
                self.ui.Manager_TabWidget.currentChanged.disconnect(self.weight_setup_verifier)
                self.ui.Manager_TabWidget.setCurrentIndex(self.manager_tab)
                # Reconnect the signal
                self.ui.Manager_TabWidget.currentChanged.connect(self.weight_setup_verifier)
                return False
            else:
                self.STUDY.update_weights_from_database()
        else:
            self.manager_tab = self.ui.Manager_TabWidget.currentIndex()

    def update_study(self):
        self.STUDY.update_situations_from_database()
        self.STUDY.update_indicators_from_database()
        if self.BodyWidget_previous_index == 2:  #if from Analysis Manager
            check_weights = self.WeightsSetup.on_tab_changed()
            if check_weights == False:
                # Disconnect the signal temporarily
                self.ui.Manager_TabWidget.currentChanged.disconnect(self.weight_setup_verifier)
                self.ui.BodyWidget.currentChanged.disconnect(self.update_study)
                # Change the pages without triggering the signals
                self.ui.analysis_btn.click()
                self.ui.Manager_TabWidget.setCurrentIndex(1)
                self.manager_tab = self.ui.Manager_TabWidget.currentIndex()
                # Reconnect the signal
                self.ui.BodyWidget.currentChanged.connect(self.update_study)
                self.ui.Manager_TabWidget.currentChanged.connect(self.weight_setup_verifier)
            else:
                self.STUDY.update_weights_from_database()
        else:
            self.STUDY.update_weights_from_database()   

    """    # def load_existing_situations(self):
    #     existing_situations = {}
        
    #     for index, row in self.SituationGenerator.get_situations().iterrows():
    #         situation = M_SituationManager.Situation()
    #         situation.update(self.SituationGenerator, row["SituationID"])
    #         existing_situations[situation.id] = situation
        
    #     return existing_situations"""

    def update_buidling_uses(self, old_value, new_value):
        for _, situation in self.STUDY.Situations.items():
            M_OperateDatabases.establishDatabaseConnections([(self.STUDY.Temp_db, situation.db_path)])
            
            M_OperateDatabases.updateB1TableUses(self.STUDY.Temp_db,
                                                 self.STUDY.Study_db,
                                                 situation,
                                                 old_value,
                                                 new_value)
           
            self.STUDY.Temp_db.close()
        
    def get_study_IndicatorsSetup(self):
        self.STUDY.update_indicators_setup()

    def populate_Functional_objective_pages(self):
        """
        Populates the main widgets with objective pages based on the objectives retrived from the RESILISTORM_DB.

        """

        # Iterate over objectives
        for objective_id, objective in self.STUDY.objectives.iterrows():
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

    def populate_Functional_criterion_pages(self):
        """
        Populates the UI with criterion pages based on the criteria, metrics, and metric options retrieved from the RESILISTORM_DB.

        """
        criteria_sorted = self.STUDY.criteria.sort_values(by = "CriteriaID", ascending = True)

        for criteriaID, criterion in criteria_sorted.iterrows():
            criterion_name = criterion["CriteriaName"]
            criterion_metrics = self.STUDY.metrics[self.STUDY.metrics['CriteriaID'] == criteriaID]

            #Get the dimension based on the first character of the criterion_id
            if criteriaID.startswith('1'):
                Dimension = "S"

                #Generate the criterion label and assign the font and properties of the label
                Criterion_id_label = f"{Dimension}{criteriaID[2:]}"
                Criterion_label = QLabel(f"Criterion {Criterion_id_label}: {criterion_name}")
                Criterion_label.setFont(MyFont(12, True))
                Criterion_label.setWordWrap(True)  # Enable word wrapping
                Criterion_label.setFixedHeight(50)
                Criterion_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

                # Create the criterion main widget
                page = QFrame()

                #Create a QVBoxLayout for the main widget
                page_layout = QVBoxLayout(page)
                page_layout.setContentsMargins(10, 0, 0, 0)
                page_layout.setSpacing(0)  # Set the spacing to 0 or a smaller value

                # Create a QWidget as the content widget for the scroll area
                scroll_widget = QWidget()
                # Create a QVBoxLayout for the scroll widget
                scroll_layout = QVBoxLayout(scroll_widget)
                scroll_layout.setContentsMargins(0, 0, 10, 0)
                scroll_layout.setSpacing(25)

                #Create a QScrollArea
                scroll_area = QScrollArea()
                scroll_area.setWidget(scroll_widget)
                scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget -> texto não corta
                #scroll_area.setStyleSheet("QScrollArea { border: none; background-color: rgb(236, 246, 239);}")
                scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                # Populate the scroll layout with the metric "normal" blocks
                criterion_metrics_sorted = criterion_metrics.sort_values(by = "MetricID", ascending = True)

                for metric_id, metric in criterion_metrics_sorted.iterrows():
                    metric_name = metric["MetricName"]
                    metric_question = metric["MetricQuestion"]

                    #add metric block to respective layout
                    if metric_id[0] == '1':
                        metric_block = FunctionalMetricWidget(metric_id, self.STUDY.metrics, self.STUDY.metric_options)
                        self.FunctionalMetricBlocks[metric_id] = metric_block
                    # elif metric_id[0] == '2':
                    #     metric_block, model, table_view = PerformanceMetricBlock(metric_id, metric_name, metric_question)
                    #     self.PerformanceModels.append((model, table_view))

                    scroll_layout.addWidget(metric_block)

                #add spacer at the bottom of the metrics
                scroll_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

                # Add the desired widgets, inluding the scrool area, to the main layout
                page_layout.addWidget(Criterion_label)
                page_layout.addWidget(scroll_area)
                page_layout.setStretch(0, 0)
                page_layout.setStretch(1, 1)

                # Set the property for the page
                page.setProperty("pageName", criteriaID)

                self.ui.Functional_MainWidget.addWidget(page)

    def populate_Performance_pages(self):
       
        M_Operate_GUI_Elements.CleanStackedWidget(self.ui.Performance_MainWidget)       #LIMPAR PAGES EXISTENTES

        if self.selected_situation_id and self.STUDY.Situations[self.selected_situation_id].rainfall:
            for rainfall_year in self.STUDY.Situations[self.selected_situation_id].rainfall:
                self.scenario_models[rainfall_year] = {}

                # Create the main widget
                page = QFrame()
                #Create a QVBoxLayout for the main widget
                page_layout = QVBoxLayout(page)
                #page.setStyleSheet("border: 1px solid #000;")

                page_layout.setContentsMargins(10, 0, 0, 0)
                page_layout.setSpacing(0)  # Set the spacing to 0 or a smaller value

                # Create a QWidget as the content widget for the scroll area
                scroll_widget = QWidget()

                # Create a QVBoxLayout for the scroll widget
                scroll_layout = QVBoxLayout(scroll_widget)
                scroll_layout.setContentsMargins(0, 0, 10, 0)
                scroll_layout.setSpacing(25)

                #Create a QScrollArea
                scroll_area = QScrollArea()
                scroll_area.setWidget(scroll_widget)
                scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget -> texto não corta
                scroll_area.setStyleSheet("QScrollArea { border: none; }")
                scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

                # ADD LABEL COM O SCENARIO_NAME
                top_label = QLabel(f"Rainfall: {rainfall_year} year-return period")
                top_label.setFont(MyFont(12, True))
                top_label.setFixedHeight(50)

                page_layout.addWidget(top_label)
                page_layout.addWidget(scroll_area)

                for class_id, class_prop in self.STUDY.IndicatorsClassesLibrary.iterrows():
                    if class_id in self.STUDY.Selected_indicators["IndicatorClass"].values:
                        class_name = class_prop[ 'IndicatorClassName']
                        class_widget = M_Operate_GUI_Elements.NotExpandableSimpleElement(f"{class_name}")
                        class_widget.setObjectName(f"class_{class_id}")

                        scroll_layout.addWidget(class_widget)

                        class_excluxive = class_prop['Exclusive']
                        if class_excluxive == 'NO':
                            indicators_ids = tuple(self.STUDY.Selected_indicators[self.STUDY.Selected_indicators["IndicatorClass"] == class_id].index)

                            methodology = self.STUDY.IndicatorsLibrary.at[indicators_ids[0], 'Reference']
                            reference_label = QLabel(f"Methodology: {methodology}")

                            selected_unit = self.STUDY.IndicatorsSetup.at[indicators_ids[0], 'SelectedUnit']
                            unit_label = QLabel(f"Data unit: {selected_unit}")

                            scenario_model = GeneralizedIndicatorModel(ANSWERS_DB, indicators_ids, rainfall_year, ['Value'], {"SRP1": "Node surcharge",
                                                                                                                              "SRP2":"Node flooding",
                                                                                                                              "SRP3": "Surface Flooding"})

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
                            for indicator_id, indicator in self.STUDY.IndicatorsSetup.iterrows():
                                if indicator_id  in self.selected_indicators[class_id]:
                                    methodology = self.STUDY.IndicatorsLibrary.at[indicator_id, 'Reference']
                                    reference_label = QLabel(f"Methodology: {methodology}")
                                    unit_label = QLabel(f"Data unit: {indicator['SelectedUnit']}")

                                    scenario_model = QSqlTableModel(db = ANSWERS_DB)
                                    scenario_model.setTable(indicator_id)
                                    scenario_model.setEditStrategy(QSqlTableModel.OnFieldChange)
                                    scenario_model.setFilter(f"RainfallID = '{rainfall_year}'")
                                    scenario_model.select()

                                    # Associa o modelo a um nome específico para acessá-lo posteriormente
                                    self.scenario_models[rainfall_year][indicator_id] = scenario_model

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
                page.setProperty("pageName", f"Rainfall{rainfall_year}")
                self.ui.Performance_MainWidget.addWidget(page)
                self.scenario_pages[rainfall_year] = page

    """def create_model(self, scenario_id, model_name, table_name, filter_condition):
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
    """

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
        elif item_id.startswith("Rainfall"):
            M_Operate_GUI_Elements.access_page_by_name(self.ui.Performance_MainWidget, item_id)

    def populate_functional_tree(self, tree_widget: QTreeWidget):
        """
        Populate the given tree widget with objectives and criteria for the given dimension.

        Args:
            tree_widget (QTreeWidget): The tree widget to populate.
            dimension_id (int): The ID of the dimension to fetch objectives and criteria for.
        """

        # Clear the tree widget
        tree_widget.clear()

        # Populate the tree widget with objectives and criteria
        for objectiveID, objective in self.STUDY.objectives[self.STUDY.objectives["DimensionID"] == 1].iterrows():
            # Create an objective item with the objective name and description
            objective_item = QTreeWidgetItem([f"{objective['ObjectiveSubID']} - {objective['ObjectiveName']}"])
            objective_item.setData(0, Qt.UserRole, objectiveID)  # Store the ObjectiveID as data
            objective_item.setFont(0, MyFont(9, True))
            tree_widget.addTopLevelItem(objective_item)

            for criteriaID, criterion in self.STUDY.criteria[self.STUDY.criteria["ObjectiveID"] == objectiveID].iterrows():
                # Create a criterion item with the criterion name and description
                criterion_item = QTreeWidgetItem([f"{objective['ObjectiveSubID']}.{criterion['CriteriaSubID']} - {criterion['CriteriaName']}"])
                criterion_item.setData(0, Qt.UserRole, criteriaID)  # Store the CriterionID as data
                objective_item.addChild(criterion_item)

    def clean_FunctionalAnswers(self):   
        
        for metric_id, metric_block in self.FunctionalMetricBlocks.items():
            options_layout = M_Operate_GUI_Elements.getWidgetsFromLayout(metric_block.OptionsLayout)
            metric_block.metric_comment.setText('')
            metric_block.metric_comment.setEnabled(False)

            for item in options_layout:
                item.setEnabled(False)
                if metric_block.answer_type == ("Single choice" or "Multiple choice"):
                    item.setChecked(False)
                elif metric_block.answer_type == "Open":
                    item.setText('')

    def update_FunctionalAnswers(self, state):

        for metric_id, metric_block in self.FunctionalMetricBlocks.items():
            options_layout = M_Operate_GUI_Elements.getWidgetsFromLayout(metric_block.OptionsLayout)
            
            if state == False:   # Disable widgets/items and clean answers
                metric_block.metric_comment.setText('')
                metric_block.metric_comment.setEnabled(False)                
                for index, item in enumerate(options_layout):
                    item.setEnabled(False)
                    if metric_block.answer_type == "Single choice" or metric_block.answer_type == "Multiple choice":
                        item.setChecked(False)
                    elif metric_block.answer_type == "Open":
                        item.setText('')
                        
            elif state == True:  # Enable widgets/items and load answers
                # Get the answer(s) from the database
                answers_from_database = M_OperateDatabases.fetch_table_from_database(ANSWERS_DB, "MetricAnswers")
                answers_from_database = answers_from_database.set_index("metricID")

                # "Translate" the answers depending on answer's type 
                comment = answers_from_database.at[metric_id, "comment"]
                if metric_block.answer_type == "Single choice":
                    text = answers_from_database.at[metric_id, "answer"].split('_')[0]
                    if text:
                        answer = [int(text)]
                    else:
                        answer = []
                elif metric_block.answer_type == "Multiple choice":
                    answer = []
                    for element in answers_from_database.at[metric_id, "answer"].split(';'):
                        if element != '':
                            answer.append(int(element.split('_')[0]))
                elif metric_block.answer_type == "Open":
                    answer = answers_from_database.at[metric_id, "answer"]                
                # Update the widgets with the answers
                metric_block.metric_comment.setPlainText(comment)
                metric_block.metric_comment.setEnabled(True)
                for index, item in enumerate(options_layout):
                    item.setEnabled(state)
                    if metric_block.answer_type == "Open":
                        item.setEnabled(True)
                        item.setText(answer)
                    elif metric_block.answer_type == "Single choice" or metric_block.answer_type == "Multiple choice":
                        if index in answer:
                            item.setChecked(True)
                        else:
                            item.setChecked(False)

    '''DEFINE FUNCTIONS FOR BUTTONS BEHAVIOR'''
    def home_btn_toggled(self):
        self.BodyWidget_previous_index = self.ui.BodyWidget.currentIndex()
        self.ui.BodyWidget.setCurrentIndex(0)

    def profile_btn_toggled(self):
        self.BodyWidget_previous_index = self.ui.BodyWidget.currentIndex()
        self.ui.BodyWidget.setCurrentIndex(1)

    def analysis_btn_toggled(self):
        self.BodyWidget_previous_index = self.ui.BodyWidget.currentIndex()
        self.ui.BodyWidget.setCurrentIndex(2)
        self.ui.Manager_TabWidget.setCurrentIndex(0)
        self.manager_tab = self.ui.Manager_TabWidget.currentIndex()

    def functional_btn_toggled(self):
        self.BodyWidget_previous_index = self.ui.BodyWidget.currentIndex()
        self.ui.BodyWidget.setCurrentIndex(3)

    def performance_btn_toggled(self):
        self.BodyWidget_previous_index = self.ui.BodyWidget.currentIndex()
        if self.ui.BodyWidget.currentIndex() != 4:
            self.ui.BodyWidget.setCurrentIndex(4)
            self.STUDY.update_study_from_AnalysisManager()
            self.get_study_IndicatorsSetup()
            self.populate_Performance_pages()

    def dashboard_btn_toggled(self):
        self.BodyWidget_previous_index = self.ui.BodyWidget.currentIndex()
        if self.ui.BodyWidget.currentIndex() != 5:
            self.ui.BodyWidget.setCurrentIndex(5)
            self.get_study_IndicatorsSetup()
            self.STUDY.update_study_from_AnalysisManager()
            self.STUDY.calculate_ratings()
            self.PlotDashboardPage()

    def update_modified_situation(self,
                                  type: str,   #'new', 'update' or 'delete'
                                  situation_id: int):
        # Update STUDY Situations based on database
        self.STUDY.update_situations_from_database()
        #Update specific Situation
        self.STUDY.update_situation_from_SituationGenerator(type, situation_id)
        #update self.ui.Situation_selection_Combobox items
        self.update_situation_combobox_list()

    def update_situation_combobox_list(self):
        self.ui.Situation_selection_Combobox.clear()
        self.ui.Situation_selection_Combobox.addItem("None")
        self.ui.Situation_selection_Combobox.addItems(self.SituationGenerator.get_situations_table()["SituationName"])
 
    def update_rainfall_combobox(self):
        self.ui.Rainfall_selection_ComboBox.clear()
        if self.selected_situation_id and self.STUDY.Situations[self.selected_situation_id].rainfall:
            self.ui.Rainfall_selection_ComboBox.setEnabled(True)
            for rain in self.STUDY.Situations[self.selected_situation_id].rainfall:
                self.ui.Rainfall_selection_ComboBox.addItem(str(rain))
            self.ui.Rainfall_selection_ComboBox.setCurrentIndex(0)
            self.ui.Performance_MainWidget.setCurrentIndex(0)
        elif not self.selected_situation_id:
            self.ui.Rainfall_selection_ComboBox.setEnabled(False)

    def set_selected_situation(self):
        from C_SITUATION  import SITUATION
        
        if self.ui.Situation_selection_Combobox.currentIndex() >= 1: #index 0 is "None"
            selected_situation_name = self.ui.Situation_selection_Combobox.currentText()
            for situation_id, situation in self.STUDY.Situations.items():
                if situation.name == selected_situation_name:
                    self.selected_situation_id = situation_id
            situation_state = True
            
        else:
            # Close the connection with current ANSWRS_DB
            if ANSWERS_DB.isOpen():
                ANSWERS_DB.close()
            self.selected_situation_id = -1
            self.STUDY.Situations[self.selected_situation_id] = SITUATION(self.STUDY.Study_path)  #Set an empty situation
            situation_state = False
    
        # Establish the connection with ANSWRS_DB, even if Situation is empty/none
        M_OperateDatabases.establishDatabaseConnections([(ANSWERS_DB, self.STUDY.Situations[self.selected_situation_id].db_path)])        
        print(f"Selected situation is {self.STUDY.Situations[self.selected_situation_id].name}")
        
        self.update_FunctionalAnswers(situation_state)
        self.update_rainfall_combobox()
        self.populate_Performance_pages()
        
        if self.ui.BodyWidget.currentIndex() == 5:
            self.PlotDashboardPage()        

    def update_performance_page(self):
        current_rainfall_index = self.ui.Rainfall_selection_ComboBox.currentIndex()
        self.ui.Performance_MainWidget.setCurrentIndex(current_rainfall_index)

    def PlotDashboardPage(self):
        ''' PLOT FUNCTIONAL RESULTS '''
        #Plot the Functional Objectives Completness
        M_PlotGraphs.plotHorizontalFunctionalBars(
            DataFrame = self.STUDY.Situations[self.selected_situation_id].functional_objectives_completeness,
            labelColumn = "FullLabel",
            DestinyWidget = self.ui.FOC_Plot,
            Type = "Completness")

        #Plot the Functional Objectives Rating
        M_PlotGraphs.plotHorizontalFunctionalBars(
            DataFrame = self.STUDY.Situations[self.selected_situation_id].functional_objectives_rating,
            labelColumn = "FullLabel",
            DestinyWidget = self.ui.FOR_Plot,
            Type = "Rating")
        
        #Functional Criteria Rating is plotted in the updateFCR function upon selection on combobox

        ''' PLOT PERFORMANCE RESULTS '''
        M_PlotGraphs.plotPerformances(
            DataFrame       = self.STUDY.Situations[self.selected_situation_id].system_performance_rating,
            Legend          = self.STUDY.IndicatorsLibrary,
            DestinyWidget   = self.ui.PSR_Plot)

        M_PlotGraphs.plotPerformances(
            DataFrame       = self.STUDY.Situations[self.selected_situation_id].system_consequences_rating,
            Legend          = self.STUDY.IndicatorsLibrary,
            DestinyWidget   = self.ui.PCR_Plot)

        ''' PLOT OVERALL RESULTS '''
        #Plot the Functional Dimension Rating
        M_PlotGraphs.plotResilienceCircle(
            DataFrame       = self.STUDY.Situations[self.selected_situation_id].functional_rating,
            DestinyWidget   = self.ui.OFR_Plot)    
 
        #Plot the Perforamnce Dimension Rating
        M_PlotGraphs.plotResilienceCircle(
            DataFrame       = self.STUDY.Situations[self.selected_situation_id].performance_rating,
            DestinyWidget   = self.ui.OPR_Plot) 
        
        #Plot the Overall Rating
        M_PlotGraphs.plotResilienceCircle(
            DataFrame       = self.STUDY.Situations[self.selected_situation_id].overall_rating,
            DestinyWidget   = self.ui.ORR_Plot)
        
    def updateFCR(self):
        selected_text = self.ui.FCR_ComboBox.currentText()

        if selected_text != '':
            ObjectiveID = f'1.{selected_text.split(" - ")[0].split("S")[1]}'
            showing_FunctionalCriteriaRating = self.STUDY.Situations[self.selected_situation_id].functional_criteria_rating[self.STUDY.Situations[self.selected_situation_id].functional_criteria_rating["ObjectiveID"]==ObjectiveID]

            M_PlotGraphs.plotHorizontalFunctionalBars(
                DataFrame       = showing_FunctionalCriteriaRating,
                labelColumn     = "FullLabel",
                DestinyWidget   = self.ui.FCR_Plot,
                Type            = "Rating")

    def closeEvent(self, Event):
        atexit.register(M_OperateDatabases.closeDatabaseConnections, [RESILISTORM_DB, STUDY_DB, ANSWERS_DB])
        super().closeEvent(Event)
                    
class FunctionalMetricWidget(QWidget):
    def __init__(self,
                 metric_id: str,
                 metrics: pd.DataFrame,
                 metrics_options: pd.DataFrame):
        super().__init__()

        self.metric_id = metric_id
        self.metric_name = metrics.at[metric_id, "MetricName"]
        self.metric_question = metrics.at[metric_id, "MetricQuestion"]
        self.answer_type = metrics.at[metric_id, "AnswerType"]
        self.answer_options = metrics_options.loc[metric_id]

        # Create the widgets for the metric block (e.g., labels, answer widget)
        if metric_id.startswith('1'):
            self.dimension = "S"
        else:
            self.dimension = "P"

        self.setup_ui()

    def setup_ui(self):
        metric_id_label = f"{self.dimension}{self.metric_id[2:]}"

        metric_id_label = QLabel(f"{metric_id_label}: {self.metric_name}")
        metric_id_label.setFont(MyFont(10, True))
        metric_id_label.setWordWrap(True)  # Enable word wrapping

        metric_question_label = QLabel(f"Question: {self.metric_question}")
        metric_question_label.setFont(MyFont(10, False))
        metric_question_label.setWordWrap(True)  # Enable word wrapping

        # Create the layout for the metric block
        Metric_block = QVBoxLayout(self)
        Metric_block.setContentsMargins(0,0,0,0)
        Metric_block.setSpacing(2)

        Metric_block.addWidget(metric_id_label)
        Metric_block.addWidget(metric_question_label)

        # Logic to create the appropriate answer widget based on the answer type
        if self.dimension == "S":
            OptionsWidget = QWidget()
            self.OptionsLayout = QVBoxLayout(OptionsWidget)
            self.OptionsLayout.setSpacing(0)

            if self.answer_type == "Single choice" or self.answer_type == "Multiple choice":
                Options = self.answer_options.filter(regex='^Opt')
                Options = Options.values.tolist()

                if self.answer_type == "Single choice":
                    self.radio_group = QButtonGroup()
                    self.radio_group.setExclusive(False)        #Allows the button to be deselected if selected

                    # Add the answer options as radio buttons to the layout
                    for index, option in enumerate(Options):
                        if option != '':
                            option_radio = QRadioButton(option)
                            option_radio.setFont(MyFont(10, False))
                            self.radio_group.addButton(option_radio, index)
                            self.OptionsLayout.addWidget(option_radio)
                    self.radio_group.buttonClicked.connect(self.handleSingleChoiceSelection)

                elif self.answer_type == "Multiple choice":
                    self.checkbox_group = QButtonGroup()
                    self.checkbox_group.setExclusive(False)
                    # Add the answer options as checkboxes to the layout
                    for index, option in enumerate(Options):
                        if option != '':
                            option_checkbox = QCheckBox(option)
                            option_checkbox.setFont(MyFont(10, False))
                            self.checkbox_group.addButton(option_checkbox, index)
                            self.OptionsLayout.addWidget(option_checkbox)
                    self.checkbox_group.buttonClicked.connect(self.handleMultipleChoiceSelection)
            elif self.answer_type == "Open":
                open_answer = QLineEdit()
                open_answer.setFont(MyFont(10, False))
                self.OptionsLayout.addWidget(self.open_answer)
                open_answer.textEdited.connect(self.handleOpenAnswerChange)

            Metric_block.addWidget(OptionsWidget)

        #Add metric comment
        metric_comment_label = QLabel(f"Comment: ")
        metric_comment_label.setFont(MyFont(10, False))
        metric_comment_label.setWordWrap(True)  # Enable word wrapping
        self.metric_comment = QTextEdit()
        self.metric_comment.setAcceptRichText(True)
        self.metric_comment.setLineWrapMode(QTextEdit.WidgetWidth)
        self.metric_comment.setFixedHeight(60)
        self.metric_comment.setFont(MyFont(10, False))
        self.metric_comment.setStyleSheet('QTextEdit {background-color: white; border: 0px solid #000000; border-radius: 10px}')
        self.metric_comment.textChanged.connect(self.handleCommentEdit)

        Metric_block.addWidget(metric_comment_label)
        Metric_block.addWidget(self.metric_comment)
    def handleSingleChoiceSelection(self, buttonClicked):
        # Unselect all other radio buttons different than the clicked one
        for button in self.radio_group.buttons():
            if button != buttonClicked:
                button.setChecked(False)

        # Save answer to ANSWERS_DB
        comment = self.metric_comment.toPlainText()
        if buttonClicked == self.radio_group.checkedButton():
            index = str(self.radio_group.id(buttonClicked))
            text = buttonClicked.text()
            answer = '_'.join([index, text])
            M_OperateDatabases.save_answer_to_AnswersDatabase(ANSWERS_DB, self.metric_id, answer, comment)
        elif self.radio_group.checkedButton() is None:
            M_OperateDatabases.save_answer_to_AnswersDatabase(ANSWERS_DB, self.metric_id, '', comment)

    def handleMultipleChoiceSelection(self):
        answers = []
        comment = self.metric_comment.toPlainText()
        for checkbox in self.checkbox_group.buttons():
            index = str(self.checkbox_group.id(checkbox))
            text = checkbox.text()
            if checkbox.isChecked():
                answers.append('_'.join([index, text]))
        answer = ';'.join(x for x in answers)
        M_OperateDatabases.save_answer_to_AnswersDatabase(ANSWERS_DB, self.metric_id, answer, comment)

    def handleOpenAnswerChange(self, LineEdit):
        comment = self.metric_comment.toPlainText()
        answer = LineEdit.text()
        M_OperateDatabases.save_answer_to_AnswersDatabase(ANSWERS_DB, self.metric_id, answer, comment)

    def handleCommentEdit(self):
        comment = self.metric_comment.toPlainText()
        M_OperateDatabases.save_comment_to_AnswersDatabase(ANSWERS_DB, self.metric_id, comment)

def PerformanceMetricBlock(metric_id, metric_name, metric_question):

    # Create the widgets for the metric block (e.g., labels, answer widget)
    if metric_id.startswith('1'):
        Dimension = "S"
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

"""def updateHazardTableViews(StackedWidget: QStackedWidget):

    NrHazards = M_OperateDatabases.countDatabaseRows(ANSWERS_DB, "HazardSetup")
    NrScenarios = M_OperateDatabases.countDatabaseRows(ANSWERS_DB, "ScenarioSetup")

    if NrHazards > 0 and NrScenarios > 0:
        queryAnswers = QSqlQuery(ANSWERS_DB)
        queryLibrary = QSqlQuery(RESILISTORM_DB)

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
            print("Page with pageName '2.2.1' not found.")"""

"""def copy_and_rename_file(source_file, destination_directory, new_file_name):
    shutil.copy2(source_file, destination_directory)
    new_file_path = os.path.join(destination_directory, new_file_name)
    os.rename(os.path.join(destination_directory, os.path.basename(source_file)), new_file_path)

    return new_file_path"""

def main():   
    global RESILISTORM_DB, STUDY_DB, ANSWERS_DB, temp_DB

    app = QApplication(sys.argv)

    WelcomePage = WelcomeDialog()
    Welcome_result = WelcomePage.exec()

    if Welcome_result == QDialog.Accepted:

        RESILISTORM_DB = QSqlDatabase.addDatabase("QSQLITE", "Connection1")
        STUDY_DB = QSqlDatabase.addDatabase("QSQLITE", "Connection2")
        ANSWERS_DB = QSqlDatabase.addDatabase("QSQLITE", "Connection3")
        temp_DB = QSqlDatabase.addDatabase("QSQLITE", "TemporaryConnection")
       
        Study = STUDY(WelcomeDialog = WelcomePage,
                Methodolohy_Database = RESILISTORM_DB,
                Study_Database = STUDY_DB,
                Temp_Database = temp_DB)

        MainPage = MainWindow(Study)

        #Set initial size of the main window
        MainPage.resize(1280, 720)
        MainPage.show()
        
        sys.exit(app.exec())

    else:
        QCoreApplication.quit()

if __name__ == '__main__':
    main()