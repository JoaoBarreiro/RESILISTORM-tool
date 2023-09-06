
pyside6-rcc resources.qrc -o resources_rc.py
    
    
    
"""What isthis?

This was the code for the HazardSetup Table to force the class nr column (index1)
to be an inteer between 1 and 10. Current implementation does no require.
"""

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
    

def on_tree_item_clicked(self, item):
"""
Handle the event when a tree item is clicked.

Args:
    item: The clicked tree item.
"""
tree_widget = self.sender()

if tree_widget.indexOfTopLevelItem(item) == -1:
    # Second-level item selected
    self.navigate_to_page(item)
else:
    # First-level item selected
    self.navigate_to_page(item)