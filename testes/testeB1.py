from PyQt6.QtWidgets import QMainWindow, QApplication, QTableView, QMenu, QAction, QMessageBox
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

class B1SettingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B1 Setting Window")

        self.ui = Ui_SettingB1()
        self.ui.setupUi(self)

        self.createTable_UserUses()

    def createTable_UserUses(self):
        self.user_uses_model = QSqlTableModel(self)
        self.user_uses_model.setTable("UserUses")
        self.user_uses_model.select()

        self.ui.UserUses_Table.setModel(self.user_uses_model)

        # Set up the context menu for the UserUses_Table
        self.ui.UserUses_Table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.UserUses_Table.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, position):
        # Create the context menu
        context_menu = QMenu(self)
        add_action = context_menu.addAction("Add new use")
        remove_action = context_menu.addAction("Remove current use")

        # Show the context menu at the specified position
        action = context_menu.exec_(self.ui.UserUses_Table.viewport().mapToGlobal(position))

        # Handle the selected action
        if action == add_action:
            self.addNewRow()
        elif action == remove_action:
            self.removeCurrentRow()

    def addNewRow(self):
        row = self.user_uses_model.rowCount()
        self.user_uses_model.insertRow(row)

    def removeCurrentRow(self):
        current_row = self.ui.UserUses_Table.currentIndex().row()
        if current_row >= 0:
            self.user_uses_model.removeRow(current_row)
            self.user_uses_model.select()

# Exemplo de inicialização da janela B1SettingWindow
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = B1SettingWindow()
    window.show()
    sys.exit(app.exec())
