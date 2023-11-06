from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QCheckBox, QStackedWidget, QListView,
                                QComboBox, QTreeWidgetItem, QWidget, QInputDialog, QSpacerItem,
                                QSizePolicy, QLabel, QMessageBox, QFrame, QFormLayout,QLineEdit,
                                QPushButton, QLayout)

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (QStandardItemModel, QStandardItem)
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from M_Fonts import MyFont


def CleanStackedWidget(QStackedWidget):
    #Remove all existing pages from the stacked widget
    while QStackedWidget.count() > 0:
        widget = QStackedWidget.widget(0)
        QStackedWidget.removeWidget(widget)
        
def getLayoutsFromLayout(layout):
    layouts = []
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if isinstance(item.layout(), QVBoxLayout) or isinstance(item.layout(), QHBoxLayout):
            layouts.append(item.layout())
    return layouts

def getWidgetsFromLayout(layout):
    widgets = []
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget:
            widgets.append(widget)
    return widgets

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

def access_page_by_name(stacked_widget: QStackedWidget, page_name: str):
    """
    Accesses a page in a stacked widget by its name.

    Args:
        stacked_widget: The stacked widget containing the pages.
        page_name (str): The name of the page to be accessed.

    """
    # Iterate over each page in the stacked widget
    for index in range(stacked_widget.count()):
        page = stacked_widget.widget(index)
        # Check if the page name matches the desired page name
        if page.property("pageName") == page_name:
            # Set the current page to the found page
            stacked_widget.setCurrentIndex(index)
            break
            

############### QList OPERATIONS ###############
     
def updateQListView(ListView: QListView, Model: QStandardItemModel, Data: list, Exclude=None):
    """
    Update a QListView with the provided data.

    Args:
        ListView (QListView): The QListView to be updated.
        Model (QStandardItemModel): The model for the QListView.
        Data (list): The data to populate the model.
        Exclude (Any, optional): An item to exclude from the data. Defaults to None.
    """

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
    
def getQListSelection(QListModel: QStandardItemModel):
    """
    Get the list of text of the checked items in the QListModel.

    Args:
        QListModel: The QListModel object containing the items.

    Returns:
        A list of text of the checked items.
    """
    
    # Get the number of items in the table model
    num_items = QListModel.rowCount()

    selected_items = []
    for row in range(num_items):
        item = QListModel.item(row)
        if item and item.checkState() == Qt.Checked:
            selected_items.append(item.text())

    return selected_items


################################################

def updatePerformanceTablesViews(PerformanceTableData):
    """
    Updates the views for the performance tables.

    Args:
        PerformanceTableData (list): A list of tuples containing the model and
            its data for updating the views.
    """
    
    for model, _ in PerformanceTableData:
        model.select()
        
def updateQComboBox(ComboBox: QComboBox, Data: list):
    """
    Clears the given QComboBox and adds the items from the provided list.

    Parameters:
        ComboBox (QComboBox): The QComboBox to update.
        Data (list): The list of items to add to the QComboBox.
    """

    ComboBox.clear()
    ComboBox.addItems(Data)


"""
CLASSES - SPECIAL ELEMENTS
"""
class DatabaseItem(QTreeWidgetItem):
    def __init__(self, db_row_id, column_name, parent=None):
        super(DatabaseItem, self).__init__(parent)

        self.db_row_id = db_row_id
        self.column_name = column_name

class NotExpandableSimpleElement(QWidget):

    def __init__(self, label_text = ""):
        super().__init__()
        self.expanded = True
        self.label_text = label_text
        
        #self.setStyleSheet("border: 1px solid #BB0A21;") 
               
        self.setup_ui()

    def setup_ui(self):
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        '''Create header of the expandable element'''
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Create a horizontal layout for the header of the expandable element
        header_labels_layout = QHBoxLayout()

        # Create a label for the element's text label
        label = QLabel(self.label_text)
        label.setFont(MyFont(10, True))
        label.setMargin(0)
        

        # Create a horizontal spacer to push self.label to the left
        label_h_spacer = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Add the labels to the header_labels_layout
        header_labels_layout.addWidget(label)
        header_labels_layout.addItem(label_h_spacer)

        # Add the header labels layout to the header_layout
        header_layout.addLayout(header_labels_layout)

        # Create a simple horizontal line and add to header_layout
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        header_layout.addWidget(line)

        self.layout.addLayout(header_layout)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(4,0,4,0)
        self.content_layout.setSpacing(4)
        self.layout.addLayout(self.content_layout)          
       
class ExpandableSimpleElement(QFrame):

    def __init__(self, label_text = ""):
        super().__init__()
        self.expanded = True
        self.label_text = label_text
        
        #self.setStyleSheet("border: 1px solid #BB0A21;") 
               
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        '''Create header of the expandable element'''
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Create a horizontal layout for the header of the expandable element
        header_labels_layout = QHBoxLayout()

        # Create a label for the element's text label
        label = QLabel(self.label_text)
        label.setFont(MyFont(10, True))

        # Create a horizontal spacer to push self.label to the left
        label_h_spacer = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Create a label for the expand/collapse arrow (self.expand_label)
        self.expand_label = QLabel("▲")  # Use ▼ for down arrow and ▲ for up arrow
        self.expand_label.setAlignment(Qt.AlignCenter)
        self.expand_label.setCursor(Qt.PointingHandCursor)
        self.expand_label.mousePressEvent = self.toggle_properties

        # Add the labels to the header_labels_layout
        header_labels_layout.addWidget(label)
        header_labels_layout.addItem(label_h_spacer)
        header_labels_layout.addWidget(self.expand_label)

        # Add the header labels layout to the header_layout
        header_layout.addLayout(header_labels_layout)

        # Create a simple horizontal line and add to header_layout
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        header_layout.addWidget(line)

        self.layout.addLayout(header_layout)
        
        '''Create content layout of the expandable element'''
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(4,0,4,0)
        self.layout.addLayout(self.content_layout)

        # self.layout.addItem(QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
            
    def toggle_properties(self, event):
        self.expanded = not self.expanded
        #self.content_widget.setVisible(self.expanded)
        if self.expanded:
            self.expand_label.setText("▲")  # Change to up arrow when expanded
        else:
            self.expand_label.setText("▼")  # Change to down arrow when collapsed

        for i in range(self.content_layout.count()):
            item = self.content_layout.itemAt(i)
            if isinstance(item.layout(), QVBoxLayout) or isinstance(item.layout(), QHBoxLayout):
                layout = item.layout()
                for j in range(layout.count()):
                    widget = layout.itemAt(j).widget()
                    if widget:
                        widget.setVisible(self.expanded)
            elif isinstance(item.widget(), QWidget):
                item.widget().setVisible(self.expanded)
                        