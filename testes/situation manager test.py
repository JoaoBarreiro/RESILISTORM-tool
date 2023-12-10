from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QWidget, QLineEdit, QTableWidget, QTableWidgetItem,
    QComboBox, QFormLayout, QVBoxLayout, QInputDialog, QHBoxLayout, QAbstractItemView, QMessageBox,
    QDialogButtonBox, QDialog
    )
from PySide6.QtCore import Qt, Signal

class ListEditor(QWidget):
    
    lists_changed = Signal(list, list, list)
    
    def __init__(self):
        super().__init__()

        self.configurations = QListWidget()
        self.scenarios = QListWidget()
        self.return_periods = QListWidget()

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.setup_list_widget(self.configurations, "System Configurations", main_layout)
        self.setup_list_widget(self.scenarios, "Scenario / Time Frame", main_layout)
        self.setup_list_widget(self.return_periods, "Rainfall Return Periods", main_layout)

    def setup_list_widget(self, list_widget, label_text, main_layout):
        add_button = QPushButton("➕")
        add_button.setFixedSize(add_button.minimumSizeHint().height(), add_button.minimumSizeHint().height())
        add_button.clicked.connect(lambda: self.add_item(list_widget))

        remove_button = QPushButton("➖")
        remove_button.setFixedSize(remove_button.minimumSizeHint().height(), remove_button.minimumSizeHint().height())
        remove_button.clicked.connect(lambda: self.remove_item(list_widget))

        up_button = QPushButton("⬆️")
        up_button.setFixedSize(up_button.minimumSizeHint().height(), up_button.minimumSizeHint().height())
        up_button.clicked.connect(lambda: self.move_item(list_widget, -1))

        down_button = QPushButton("⬇️")
        down_button.setFixedSize(down_button.minimumSizeHint().height(), down_button.minimumSizeHint().height())
        down_button.clicked.connect(lambda: self.move_item(list_widget, 1))

        layout = QHBoxLayout()
        layout.addWidget(QLabel(label_text))
        layout.addWidget(list_widget)
        button_layout = QVBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(up_button)
        button_layout.addWidget(down_button)
        layout.addLayout(button_layout)

        main_layout.addLayout(layout)

    def add_item(self, list_widget):
        item_text, ok = QInputDialog.getText(self, "Add Item", "Enter item:")
        if ok and item_text:
            list_widget.addItem(item_text)
            self.update_combobox_items()

    def remove_item(self, list_widget):
        selected_item = list_widget.currentItem()
        if selected_item:
            list_widget.takeItem(list_widget.row(selected_item))
            self.update_combobox_items()

    def move_item(self, list_widget, move_up):
        selected_item = list_widget.currentItem()  # Get the currently selected item
        if selected_item:
            current_row = list_widget.row(selected_item)  # Get the current row of the selected item

            if move_up and current_row > 0:
                # Move the item up
                list_widget.takeItem(current_row)
                list_widget.insertItem(current_row - 1, selected_item)
                list_widget.setCurrentItem(selected_item)  # Reselect the item
            elif not move_up and current_row < list_widget.count() - 1:
                # Move the item down
                list_widget.takeItem(current_row)
                list_widget.insertItem(current_row + 1, selected_item)
                list_widget.setCurrentItem(selected_item)  # Reselect the item
            self.update_combobox_items()

    def update_combobox_items(self):
        self.config_list = self.Qlist_to_list(self.configurations)
        self.scenario_list = self.Qlist_to_list(self.scenarios)
        self.return_period_list = self.Qlist_to_list(self.return_periods)

        self.lists_changed.emit(self.config_list, self.scenario_list, self.return_period_list)

    def Qlist_to_list(self, Qlist):
        return [Qlist.item(i).text() for i in range(Qlist.count())]

class SituationGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.list_editor = None

        self.situation_name_edit = QLineEdit()
        self.situation_config_combobox = QComboBox()
        self.situation_scenario_combobox = QComboBox()
        self.situation_return_period_combobox = QComboBox()

        self.situations_table = QTableWidget()
        self.situations_table.setColumnCount(4)
        self.situations_table.setHorizontalHeaderLabels(["Situation Name", "Configuration", "Scenario", "Return Period"])
        self.situations_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.situations_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.situations_table.horizontalHeader().setSelectionMode(QAbstractItemView.NoSelection)
        

        self.add_situation_button = QPushButton("Add \n Situation")
        self.add_situation_button.clicked.connect(self.add_situation)
        
        self.edit_situation_button = QPushButton("Edit \n Situation")
        self.edit_situation_button.clicked.connect(self.edit_situation)

        self.delete_situation_button = QPushButton("Delete \n Situation")
        self.delete_situation_button.clicked.connect(self.delete_situation)

        self.setup_ui()

    def setup_ui(self):
        configuration_scenario_layout = QFormLayout()
        configuration_scenario_layout.addRow(QLabel("Situation Name:"), self.situation_name_edit)
        configuration_scenario_layout.addRow(QLabel("Select Configuration:"), self.situation_config_combobox)
        configuration_scenario_layout.addRow(QLabel("Select Scenario:"), self.situation_scenario_combobox)
        configuration_scenario_layout.addRow(QLabel("Select Return Period:"), self.situation_return_period_combobox)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.addWidget(self.add_situation_button)
        buttons_layout.addWidget(self.edit_situation_button)
        buttons_layout.addWidget(self.delete_situation_button)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(configuration_scenario_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.situations_table)

    def add_situation(self):
        name = self.situation_name_edit.text()        
        config = self.situation_config_combobox.currentText()
        scenario = self.situation_scenario_combobox.currentText()
        return_period = self.situation_return_period_combobox.currentText()

        verify_dict = {
            "Situation name": name,
            "System configuration": config,
            "Scenario / Time Frame": scenario,
            "Return period": return_period
        }
        
        for key, item in verify_dict.items():
            if item == "":
                QMessageBox.critical(self, "Error", f"{key} cannot be empty!")
                return
            if key == "Situation name":   # Verifies if the name does not exist in the 1st column of the table
                for row in range(self.situations_table.rowCount()):
                    if self.situations_table.item(row, 0).text() == item:
                        QMessageBox.critical(self, "Error", "Situation name already exists, please change!")
                        return
                    
        # Verifies that such situation is not already created
        for row in range(self.situations_table.rowCount()):
            if (
                self.situations_table.item(row, 1).text() == config
                and self.situations_table.item(row, 2).text() == scenario
                and self.situations_table.item(row, 3).text() == return_period
                ):
                QMessageBox.critical(self, "Error", "Situation already exists with the same configuration, scenario, and return period.")
                return              


        row_position = self.situations_table.rowCount()
        self.situations_table.insertRow(row_position)
        self.situations_table.setItem(row_position, 0, QTableWidgetItem(name))
        self.situations_table.setItem(row_position, 1, QTableWidgetItem(config))
        self.situations_table.setItem(row_position, 2, QTableWidgetItem(scenario))
        self.situations_table.setItem(row_position, 3, QTableWidgetItem(return_period))
        
        #Clear the name field
        self.situation_name_edit.setText("")

    def edit_situation(self):
        selected_row = self.situations_table.currentRow()
        if selected_row >= 0:
            name = self.situations_table.item(selected_row, 0).text()
            config = self.situations_table.item(selected_row, 1).text()
            scenario = self.situations_table.item(selected_row, 2).text()
            return_period = self.situations_table.item(selected_row, 3).text()

            current_data = [name, config, scenario, return_period]
            
            dialog = EditSituationDialog(current_data, self.list_editor)
            if dialog.exec() == QDialog.Accepted:
                updated_name = dialog.get_name()
                updated_config = dialog.get_config()
                updated_scenario = dialog.get_scenario()
                updated_return_period = dialog.get_return_period()

                self.situations_table.setItem(selected_row, 0, QTableWidgetItem(updated_name))
                self.situations_table.setItem(selected_row, 1, QTableWidgetItem(updated_config))
                self.situations_table.setItem(selected_row, 2, QTableWidgetItem(updated_scenario))
                self.situations_table.setItem(selected_row, 3, QTableWidgetItem(updated_return_period))

    def delete_situation(self):
        selected_row = self.situations_table.currentRow()
        if selected_row >= 0:
            name = self.situations_table.item(selected_row, 0).text()

            result = QMessageBox.question(self, "Delete Situation", "Deleting the situation will erase all the associated data of the analysis. Are you sure?", QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self.situations_table.removeRow(selected_row)

        
    def update_combobox_items(self, configurations, scenarios, return_periods):
        
        #Update Situation Generator Lits:
        self.situation_config_combobox.clear()
        self.situation_scenario_combobox.clear()
        self.situation_return_period_combobox .clear()

        self.situation_config_combobox.addItems(configurations)
        self.situation_scenario_combobox.addItems(scenarios)
        self.situation_return_period_combobox .addItems(return_periods) 
        
        #Update Situations Table comboboxes:
        row_count = self.situations_table.rowCount()
        for row_index in range(row_count):
            self.update_combobox_items(row_index, configurations, scenarios, return_periods)
            
class EditSituationDialog(QDialog):
    def __init__(self, current_data, ListEditor):
        super().__init__()

        self.setWindowTitle("Edit Situation")

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        name = current_data[0]
        name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.name_edit.setText(name)

        config = current_data[1]
        config_label = QLabel("Configuration:")
        self.config_combo = QComboBox()
        self.config_combo.addItems(list_editor.config_list)
        self.config_combo.setCurrentText(config)

        scenario = current_data[2]
        scenario_label = QLabel("Scenario:")
        self.scenario_combo = QComboBox()
        self.scenario_combo.addItems(list_editor.scenario_list)
        self.scenario_combo.setCurrentText(scenario)

        return_period = current_data[3]
        return_period_label = QLabel("Return Period:")
        self.return_period_combo = QComboBox()
        self.return_period_combo.addItems(list_editor.return_period_list)
        self.return_period_combo.setCurrentText(return_period)

        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(config_label)
        layout.addWidget(self.config_combo)
        layout.addWidget(scenario_label)
        layout.addWidget(self.scenario_combo)
        layout.addWidget(return_period_label)
        layout.addWidget(self.return_period_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def get_name(self):
        return self.name_edit.text()

    def get_config(self):
        return self.config_combo.currentText()

    def get_scenario(self):
        return self.scenario_combo.currentText()

    def get_return_period(self):
        return self.return_period_combo.currentText()


if __name__ == "__main__":
    app = QApplication([])
    
    list_editor = ListEditor()
    shared_table = SituationGenerator()
    shared_table.list_editor = list_editor
    
    list_editor.lists_changed.connect(shared_table.update_combobox_items)

    main_layout = QVBoxLayout()
    main_layout.addWidget(list_editor)
    main_layout.addWidget(shared_table)

    central_widget = QWidget()
    central_widget.setLayout(main_layout)

    main_window = QMainWindow()
    main_window.setCentralWidget(central_widget)
    main_window.setWindowTitle('Situation Editor')
    main_window.setGeometry(100, 100, 800, 600)

    main_window.show()
    app.exec()
