from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog, QSpacerItem, QSizePolicy, QDialog, QLabel, 
                               QMessageBox, QFrame, QFormLayout, QLineEdit, QCheckBox, QRadioButton, QLabel, QButtonGroup, QComboBox, QTableView, QMenu,
                               QStyledItemDelegate, QHeaderView, QDoubleSpinBox, QGroupBox, QScrollArea
                               )

from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtGui import QAction

from M_IndicatorsSelection import (IndicatorsSelection, flatten_dict)
from M_OperateDatabases import fetch_table_from_database
from M_Operate_GUI_Elements import ExpandableSimpleElement, NotExpandableSimpleElement

from W_WeightSetup import Ui_WeightWindow
from M_Fonts import MyFont

class Ui_WeightSetup(QMainWindow):
    
    windowClosed = Signal()
    
    def __init__(self, AnswersDatabase: QSqlDatabase):
        super().__init__()
        self.ui = Ui_WeightWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Weight Setup")
        
        self.answers_db = AnswersDatabase
        
        self.dimensions = fetch_table_from_database(self.answers_db, "DimensionsWeight")
        self.dimensions.set_index("DimensionID", inplace=True)
        self.objectives = fetch_table_from_database(self.answers_db, "ObjectivesWeight")
        self.objectives.set_index("ObjectiveID", inplace=True)
        self.criteria = fetch_table_from_database(self.answers_db, "CriteriaWeight")
        self.criteria.set_index("CriteriaID", inplace=True)
        
        self.create_ui_elements()
        
    def create_ui_elements(self):
        self.load_weights()
        
        '''
        Deal with Dimensions Weights
        '''
        # Create a scroll area
        dimensions_scroll_area = QScrollArea()
        dimensions_scroll_area.setWidgetResizable(True)
        dimensions_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        dimensions_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Create a widget to contain the layout
        dimensions_scroll_widget = QWidget()
        dimensions_scroll_area.setWidget(dimensions_scroll_widget)
        
        dimensions_layout = QVBoxLayout()
        dimensions_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        dimensions_scroll_widget.setLayout(dimensions_layout)
        
        objectives_scroll_area = QScrollArea()
        objectives_scroll_area.setWidgetResizable(True)
        objectives_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        objectives_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        objectives_scroll_widget = QWidget()
        objectives_scroll_area.setWidget(objectives_scroll_widget)
        
        global_objectives_layout = QVBoxLayout(objectives_scroll_widget)
        global_objectives_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        criteria_scroll_area = QScrollArea()
        criteria_scroll_area.setWidgetResizable(True)
        criteria_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        criteria_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        criteria_scroll_widget = QWidget()
        criteria_scroll_area.setWidget(criteria_scroll_widget)

        global_criteria_layout = QVBoxLayout(criteria_scroll_widget)
        global_criteria_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.dimensions_spin_dict = {}
        self.objectives_spin_dict = {}
        self.criteria_spin_dict = {}
        
        for dimensionID, prop in self.dimensions.iterrows():           
            dimension_layout = QHBoxLayout()
            
            dimension_text = f'{dimensionID}. {prop["DimensionName"]}'
            dimension_label = QLabel(dimension_text)
            dimension_label.setFont(MyFont(10, True))
            
            dimension_spinbox = QDoubleSpinBox()
            
            dimension_spinbox.setAlignment(Qt.AlignHCenter)
            dimension_spinbox.minimum = 0
            dimension_spinbox.maximum = 1
            dimension_spinbox.setSingleStep(0.05)
            dimension_spinbox.setValue(prop["Weight"])

            dimension_layout.addWidget(dimension_label)
            dimension_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
            dimension_layout.addWidget(dimension_spinbox)
            
            dimensions_layout.insertLayout(dimensions_layout.count() - 1, dimension_layout)
            
            self.dimensions_spin_dict[dimensionID] = dimension_spinbox
            self.objectives_spin_dict[dimensionID] = {}
            self.criteria_spin_dict[dimensionID] = {}
            
            '''
            Deal with Objectives Weights
            '''
            Dimension_objective_element = NotExpandableSimpleElement(dimension_text)
            global_objectives_layout.insertWidget(global_objectives_layout.count()-1, Dimension_objective_element)           
            Dimension_objective_element.content_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

            Dimension_criteria_element = NotExpandableSimpleElement(dimension_text)
            Dimension_criteria_element.content_layout.setContentsMargins(10, 0, 0, 0)
            global_criteria_layout.insertWidget(global_criteria_layout.count()-1, Dimension_criteria_element)
            Dimension_criteria_element.content_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

            objectives_filtered = self.objectives[self.objectives.index.str.startswith(f'{dimensionID}.')]
            
            for ObjectiveID, prop in objectives_filtered.iterrows():
                objective_layout = QHBoxLayout()
                
                objective_text = f'Obj. {ObjectiveID}. {prop["ObjectiveName"]}'
                objective_label = QLabel(objective_text)
                
                objective_spinbox = QDoubleSpinBox()
                objective_spinbox.setAlignment(Qt.AlignHCenter)
                objective_spinbox.minimum = 0
                objective_spinbox.maximum = 1
                objective_spinbox.setSingleStep(0.05)
                objective_spinbox.setValue(prop["Weight"])
                
                objective_layout.addWidget(objective_label)
                objective_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
                objective_layout.addWidget(objective_spinbox)
                
                Dimension_objective_element.content_layout.insertLayout(Dimension_objective_element.content_layout.count() - 1, objective_layout)
                
                self.objectives_spin_dict[dimensionID][ObjectiveID] = objective_spinbox
                self.criteria_spin_dict[dimensionID][ObjectiveID] = {}
                
                '''
                Deal with Criteria Weights
                '''
                Criteria_objective_element = ExpandableSimpleElement(objective_text)
                Dimension_criteria_element.content_layout.insertWidget(Dimension_criteria_element.content_layout.count()-1, Criteria_objective_element)
    
                criteria_filtered = self.criteria[self.criteria.index.str.startswith(f'{ObjectiveID}.')]
                
                for criteriaID, prop in criteria_filtered.iterrows():
                    criterion_layout = QHBoxLayout()
                    
                    criteria_text = f'{criteriaID}.{prop["CriteriaName"]}'
                    criteria_label = QLabel(criteria_text)
                    
                    criteria_spinbox = QDoubleSpinBox()
                    criteria_spinbox.setAlignment(Qt.AlignHCenter)
                    criteria_spinbox.minimum = 0
                    criteria_spinbox.maximum = 1
                    criteria_spinbox.setSingleStep(0.05)
                    criteria_spinbox.setValue(prop["Weight"])
                    
                    criterion_layout.addWidget(criteria_label)
                    criterion_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
                    criterion_layout.addWidget(criteria_spinbox)
                    
                    Criteria_objective_element.content_layout.insertLayout(Criteria_objective_element.content_layout.count()-1, criterion_layout)

                    self.criteria_spin_dict[dimensionID][ObjectiveID][criteriaID] = criteria_spinbox
   

        self.ui.Dimensions_tab.setLayout(dimensions_layout)
        self.ui.Objectives_tab.setLayout(global_objectives_layout)
        self.ui.Criteria_tab.setLayout(global_criteria_layout)

    def load_weights(self):
        if not self.answers_db.isValid():
            QMessageBox.critical(self, "Database Error", "Invalid database connection.")
            return
        if not self.answers_db.isOpen():
            if not self.answers_db.open():
                QMessageBox.critical(self, "Database Error", "Failed to open the database in WeightSetup.")
                return
        
        self.DimensionsWeights = fetch_table_from_database(self.answers_db, "DimensionsWeight")
        self.DimensionsWeights.set_index("DimensionID")
        self.ObjectivesWeights = fetch_table_from_database(self.answers_db, "ObjectivesWeight")
        self.ObjectivesWeights.set_index("ObjectiveID")
        self.CriteriaWeights = fetch_table_from_database(self.answers_db, "CriteriaWeight")
        self.CriteriaWeights.set_index("CriteriaID")
        
    def closeEvent(self, event):
        self.windowClosed.emit()
        if self.verify_spinbox_sum():
            self.update_weights_database()
            event.accept()
        else:
            event.ignore()
    
    def verify_spinbox_sum(self):
        
        dimension_sum = 0
        for dim_id, dim_w in self.dimensions_spin_dict.items():
            dimension_sum += round(dim_w.value(), 3)

            if self.objectives_spin_dict[dim_id]:
                objectives_sum = 0
            for obj_id, obj_w in self.objectives_spin_dict[dim_id].items():
                objectives_sum += round(obj_w.value(), 3)

                if self.criteria_spin_dict[dim_id][obj_id]:
                    criteria_sum = 0
                    for crit_id, crit_w in self.criteria_spin_dict[dim_id][obj_id].items():
                        if crit_w:
                            criteria_sum += round(crit_w.value(), 3)

                    if criteria_sum < 0.99 or criteria_sum > 1:
                        self.message_box("Criteria Weight Error", f"Sum of Criteria weights in Obj. {obj_id} must be 1.")
                        return False

            if objectives_sum < 0.99 or objectives_sum > 1:
                self.message_box("Objectives Weight Error", f"Sum of Objectives weights in Dim. {dim_id} must be 1.")
                return False

        if dimension_sum < 0.99 or dimension_sum > 1:
            self.message_box("Dimension Weight Error", "Sum of Dimensions weights must be 1.")
            return False
        
        return True
    
    def message_box(self, title, text):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        ok_button = msg_box.button(QMessageBox.Ok)
        ok_button.clicked.connect(msg_box.accept)
        
        msg_box.setWindowModality(Qt.ApplicationModal)
        msg_box.exec()
    
    def update_weights_database(self):
        
        query = QSqlQuery(db = self.answers_db)
        query.prepare(f"UPDATE DimensionsWeight SET Weight = ? WHERE DimensionID = ?")
        
        for dim_id, dim_w in self.dimensions_spin_dict.items():
            query.addBindValue(dim_w.value())
            query.addBindValue(dim_id)
            if not query.exec():
                print(f"Did not commit changes in Dimension Weights.")
            else:
                print(f"Changes in Dimension Weights commited.")
            
        query.prepare(f"UPDATE ObjectivesWeight SET Weight = ? WHERE ObjectiveID = ?")
        
        for dim_id, dim_obj in self.objectives_spin_dict.items():
            for obj_id, obj_w in dim_obj.items():
                query.addBindValue(obj_w.value())
                query.addBindValue(obj_id)
                if not query.exec():
                    print(f"Did not commit changes in Objective Weights.")
                else:
                    print(f"Changes in Objective Weights commited.")
                
        query.prepare(f"UPDATE CriteriaWeight SET Weight = ? WHERE CriteriaID = ?")
        
        for dim_id, dim_obj in self.criteria_spin_dict.items():
            for obj_id, obj_crit in dim_obj.items():
                for crit_id, crit_w in obj_crit.items():
                    query.addBindValue(crit_w.value())
                    query.addBindValue(crit_id)
                    if not query.exec():
                        print(f"Did not commit changes in Criteria Weights.")
                    else:
                        print(f"Changes changes in Criteria Weights commited.")