import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QAbstractItemView, QStyledItemDelegate, QComboBox
from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex

class CustomUse:
    def __init__(self, name):
        self.name = name

class Scenario:
    def __init__(self, name):
        self.name = name
        self.custom_uses = {}

class ScenarioModel(QAbstractItemModel):
    def __init__(self, root_scenarios):
        super().__init__()
        self.root_scenarios = root_scenarios

    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():
            return self.createIndex(row, column, self.root_scenarios[row])

        parent_item = parent.internalPointer()
        if isinstance(parent_item, Scenario):
            if column == 0:
                return self.createIndex(row, column, list(parent_item.custom_uses.keys())[row])
            elif column == 1:
                custom_use = list(parent_item.custom_uses.keys())[row]
                return self.createIndex(row, column, parent_item.custom_uses[custom_use])

        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        if isinstance(child_item, CustomUse):
            for scenario in self.root_scenarios:
                if child_item in scenario.custom_uses.values():
                    return self.createIndex(self.root_scenarios.index(scenario), 0, scenario)

        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.root_scenarios)

        parent_item = parent.internalPointer()
        if isinstance(parent_item, Scenario):
            return len(parent_item.custom_uses)

        return 0

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            item = index.internalPointer()
            if isinstance(item, Scenario):
                if index.column() == 0:
                    return item.name
            elif isinstance(item, CustomUse):
                if index.column() == 0:
                    return item.name
                elif index.column() == 1:
                    scenario = list(filter(lambda s: item in s.custom_uses.values(), self.root_scenarios))[0]
                    return scenario.custom_uses[item]

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            item = index.internalPointer()
            if isinstance(item, Scenario):
                item.name = value
            elif isinstance(item, CustomUse):
                scenario = list(filter(lambda s: item in s.custom_uses.values(), self.root_scenarios))[0]
                scenario.custom_uses[item] = value

            self.dataChanged.emit(index, index)
            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif index.column() == 1:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scenario Editor")

        scenario1 = Scenario("Scenario 1")
        scenario2 = Scenario("Scenario 2")
        custom_uses = [CustomUse("Residential"), CustomUse("Commercial"), CustomUse("Industrial")]
        scenario1.custom_uses = {custom_uses[0]: 0, custom_uses[1]: 0, custom_uses[2]: 0}
        scenario2.custom_uses = {custom_uses[0]: 0, custom_uses[1]: 0, custom_uses[2]: 0}

        self.root_scenarios = [scenario1, scenario2]
        self.model = ScenarioModel(self.root_scenarios)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.header().setStretchLastSection(False)
        #self.tree_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.setCentralWidget(self.tree_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
