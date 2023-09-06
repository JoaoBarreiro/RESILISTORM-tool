from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QCheckBox, QStackedWidget, QListView,
                                QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import (QStandardItemModel, QStandardItem)

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
