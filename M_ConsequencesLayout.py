from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QCheckBox, QStackedWidget, QListView,
                                QComboBox, QTreeWidgetItem, QWidget, QInputDialog, QSpacerItem,
                                QSizePolicy, QLabel, QMessageBox, QFrame, QFormLayout,QLineEdit,
                                QPushButton, QTableView)

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (QStandardItemModel, QStandardItem)
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from M_Fonts import MyFont

import pandas as pd
 
class PerformanceBlock(QWidget):
    
    newModel = Signal(str, QSqlTableModel) # utilizado para atualiar o dicionario  self.scenario_models em MainWindow
    newWidget = Signal(str, QWidget) # utilizado para atualizar o dicionario  self.scenario_widgets em MainWindow
    
    def __init__(self,
                 Answers_Database: QSqlDatabase,
                 ScenarioID: str,
                 IndicatorID: str,
                 ConsequencesLibrary: pd.DataFrame):
        
        self.database = Answers_Database
        self.ScenarioID = ScenarioID
        self.IndicatorID = IndicatorID
        self.ConsequencesLibrary = ConsequencesLibrary

        indicator_label = f"{ConsequencesLibrary[IndicatorID]['IndicatorClass']} - {ConsequencesLibrary[IndicatorID]['Reference']}"
        
        self.Block = ExpandableSimpleElement(indicator_label)
        
        self.newWidget.emit(self.Block.content_widget) #widget do conteúdo
        
        table_name = f"{self.IndicatorID}"
        model_name = table_name
        
        self.table, self.model = self.simple_indicator_model()
        
        
    def set_indicator_content(self):
        
        # Create description element
        ind_description = "TESTING DESCRIPTION"
        ind_description_label = QLabel(ind_description, self)
        ind_description_label.setFont(MyFont(10, False))
        
        # Define specific elements for each indicator, as needed
        if self.IndicatorID == "P1":
            pass
        elif self.IndicatorID == "P2":
            pass
        elif self.IndicatorID == "V1":
            pass
        elif self.IndicatorID == "B1":
            pass        
        
        #elif IndicatorID == "newIndicator":
        #    pass
        
    def simple_indicator_model(self):
        model = QSqlTableModel(db = self.database)
        model.setTable(self.IndicatorID)
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.setFilter(f"ScenarioID = '{self.ScenarioID}'")
        model.select()
        
        table_view = QTableView()
        table_view.setModel(model)
        
        self.newModel.emit(model)
        return table_view, model
        
class ExpandableSimpleElement(QWidget):

    def __init__(self, label_text: str):
        super().__init__()
        self.expanded = True
        self.label_text = label_text
        
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create a frame for the header labels and a simple horizontal line
        header_frame = QFrame(self)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Create a horizontal layout for the header labels (self.label, self.edit_label, self.expand_label)
        header_labels_layout = QHBoxLayout()

        # Create a label for the element's text (self.label_text)
        self.label = QLabel(self.label_text, self)
        self.label.setFont(MyFont(10, True))

        # Create a horizontal spacer to push self.label to the left
        label_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Create a label for the expand/collapse arrow (self.expand_label)
        self.expand_label = QLabel("▲", self)  # Use ▼ for down arrow and ▲ for up arrow
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

        self.layout.addWidget(header_frame)

        # Create a widget for the expandable content (e.g., labels and input fields)
        self.content_widget = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0,0,0,0)
        
        header_layout.addWidget(self.content_widget)

        #self.layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            
    def toggle_properties(self, event):
        self.expanded = not self.expanded
        self.content_widget.setVisible(self.expanded)
        if self.expanded:
            self.expand_label.setText("▲")  # Change to up arrow when expanded
        else:
            self.expand_label.setText("▼")  # Change to down arrow when collapsed
        self.expanded = not self.expanded
        self.content_widget.setVisible(self.expanded)
        if self.expanded:
            self.expand_label.setText("▲")  # Change to up arrow when expanded
        else:
            self.expand_label.setText("▼")  # Change to down arrow when collapsed