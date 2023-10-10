from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QCheckBox, QStackedWidget, QListView,
                                QComboBox, QTreeWidgetItem, QWidget, QInputDialog, QSpacerItem,
                                QSizePolicy, QLabel, QMessageBox, QFrame, QFormLayout,QLineEdit,
                                QPushButton)

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
        
class ExpandableSimpleElement(QWidget):
    formFieldTextChanged = Signal(str, str)  # Pass two strings: the label and the new text
    removedElement = Signal(str)
    changedLabel = Signal(str, str)
    
    def __init__(self, label_text = ""):
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
        self.content_layout = QFormLayout(self.content_widget)

        self.content_layout.setVerticalSpacing(5)  # Adjust vertical spacing as needed
        #self.content_widget.hide()
        
        header_layout.addWidget(self.content_widget)

        # Create a layout for the delete button and spacer
        header_button_layout = QHBoxLayout()
        header_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        header_layout.addLayout(header_button_layout)

        #self.layout.addWidget(header_frame)
            
    def toggle_properties(self, event):
        self.expanded = not self.expanded
        self.content_widget.setVisible(self.expanded)
        if self.expanded:
            self.expand_label.setText("▲")  # Change to up arrow when expanded
        else:
            self.expand_label.setText("▼")  # Change to down arrow when collapsed