from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QWidget, QLineEdit, QTableWidget, QTableWidgetItem,
    QComboBox, QFormLayout, QVBoxLayout, QInputDialog, QHBoxLayout, QAbstractItemView, QMessageBox,
    QDialogButtonBox, QDialog, QSpacerItem, QSizePolicy, QTableView, QHeaderView
    )
from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery

import os
import re
import pandas as pd

import M_OperateDatabases
from M_Fonts import MyFont

class ListEditor(QWidget):
    
    lists_changed = Signal(list, list, list)
    
    def __init__(self, layout, database):
        super().__init__()
        self.configurations = QListWidget()
        self.scenarios = QListWidget()
        self.return_periods = QListWidget()
        self.main_layout = layout
        self.db = database
        self.setup_ui()

        if not self.db.open():
            QMessageBox.critical(self, "Database Error", "Failed to open the study database in Analysis Manager.")
            return
        
        self.load_from_database()
        
    def setup_ui(self):
        self.setup_list_widget(self.configurations, "System Configurations")
        self.setup_list_widget(self.scenarios, "Scenario / Time Frame (year)")
        self.setup_list_widget(self.return_periods, "Rainfall Return Periods (years)")

    def setup_list_widget(self, list_widget, label_text):
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

        list_layout = QVBoxLayout()
        list_layout.setSpacing(2)
        
        head_layout = QHBoxLayout()
        head_layout.setSpacing(2)
        
        label = QLabel(label_text)
        label.setFont(MyFont(9, True))
        head_layout.addWidget(label)
        head_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        head_layout.addWidget(add_button)
        head_layout.addWidget(remove_button)
        head_layout.addWidget(up_button)
        head_layout.addWidget(down_button)
        
        list_layout.addLayout(head_layout)
        list_layout.addWidget(list_widget)
        
        self.main_layout.addLayout(list_layout)

    def add_item(self, list_widget):
        while True:
            item_text, ok = QInputDialog.getText(self, "Add Item", "Enter item:")
            
            if not ok:
                return
            if item_text == "":
                QMessageBox.critical(self, "Error", "Item cannot be empty!")
            elif not re.match(r'^[a-zA-Z0-9_()]+$', item_text):
                QMessageBox.critical(self, "Error", "Item contains invalid characters!")
            else:
                list_widget.addItem(item_text)
                self.update_combobox_items()
                self.update_database()
                break

    def remove_item(self, list_widget):
        selected_item = list_widget.currentItem()
        if selected_item:
            result = QMessageBox.question(self, "Delete item", "Are you sure you want to delete the selected item?", QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:            
                list_widget.takeItem(list_widget.row(selected_item))
                self.update_combobox_items()
                self.update_database()

    def move_item(self, list_widget, move_up):
        selected_item = list_widget.currentItem()  # Get the currently selected item
        if selected_item:
            current_row = list_widget.row(selected_item)  # Get the current row of the selected item

            if move_up == -1 and current_row > 0:
                # Move the item up
                list_widget.takeItem(current_row)
                list_widget.insertItem(current_row - 1, selected_item)
                list_widget.setCurrentItem(selected_item)  # Reselect the item
            elif move_up == 1 and current_row < list_widget.count() - 1:
                # Move the item down
                list_widget.takeItem(current_row)
                list_widget.insertItem(current_row + 1, selected_item)
                list_widget.setCurrentItem(selected_item)  # Reselect the item
            self.update_combobox_items()
            self.update_database()

    def update_database(self):
        # Convert lists to semicolon-separated strings
        config_str = ';'.join(QList_to_list(self.configurations))
        scenario_str = ';'.join(QList_to_list(self.scenarios))
        return_period_str = ';'.join(QList_to_list(self.return_periods))

        query = QSqlQuery(self.db)
        query.exec("DELETE FROM SituationSetup")  # Clear previous data
        query.prepare("INSERT INTO SituationSetup VALUES (?, ?, ?)")
        query.addBindValue(config_str)
        query.addBindValue(scenario_str)
        query.addBindValue(return_period_str)

        if not query.exec():
            QMessageBox.critical(self, "Database Error", "Failed to update the study database in Analysis Manager.")

    def load_from_database(self):
        query = QSqlQuery(self.db)
        query.exec("select * FROM SituationSetup")
        
        if query.next():
            config_str = query.value(0)
            scenario_str = query.value(1)
            return_period_str = query.value(2)

            self.populate_list_from_str(self.configurations, config_str)
            self.populate_list_from_str(self.scenarios, scenario_str)
            self.populate_list_from_str(self.return_periods, return_period_str)
            
        self.update_combobox_items()
            
    def populate_list_from_str(self, list_widget, data_str):
        items = data_str.split(';')
        for item in items:
            list_widget.addItem(item)

    def update_combobox_items(self):
        self.config_list = QList_to_list(self.configurations)
        self.scenario_list = QList_to_list(self.scenarios)
        self.return_period_list = QList_to_list(self.return_periods)

        self.lists_changed.emit(self.config_list, self.scenario_list, self.return_period_list)

def QList_to_list(Qlist):
    return [Qlist.item(i).text() for i in range(Qlist.count())]

class SituationGenerator(QWidget):
    
    situationsModified = Signal(str, int)  # str: type of modification, int: situation ID

    def __init__(self,
                 target_layout,
                 list_editor,
                 study_database,
                 study_directory,
                 methodology_database):
        super().__init__()

        self.list_editor = list_editor
        self.main_layout = target_layout
        self.study_db = study_database
        #self.directory = study_directory
        #self.methodology_db = methodology_database
        
        self.situation_name_edit = QLineEdit()
        self.situation_config_combobox = QComboBox()
        self.situation_scenario_combobox = QComboBox()
        self.situation_return_period_list = QListWidget()
        self.situation_return_period_list.setSelectionMode(QAbstractItemView.MultiSelection)

        self.situations_model = QSqlTableModel(db = self.study_db)
        self.situations_model.setTable("StudySituations")
        self.situations_model.setEditStrategy(QSqlTableModel.OnFieldChange)
    
        # Set header names
        self.situations_model.setHeaderData(1, Qt.Horizontal, "Situation name")
        self.situations_model.setHeaderData(2, Qt.Horizontal, "System configuration")
        self.situations_model.setHeaderData(3, Qt.Horizontal, "Scenario/Time frame (year)")
        self.situations_model.setHeaderData(4, Qt.Horizontal, "Rainfall return period (years)")

        self.situations_table = QTableView()
        self.situations_table.setModel(self.situations_model)
        self.situations_table.setColumnHidden(0, True)  # Assuming SituationID is at column 0
        self.situations_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.situations_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        header = self.situations_table.horizontalHeader()
        header.setSelectionMode(QAbstractItemView.NoSelection)      
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setFont(MyFont(9, True))
        header.setDefaultAlignment(Qt.AlignLeft)
        
        self.situations_model.select()
        
        self.add_situation_button = QPushButton("➕")
        self.add_situation_button.clicked.connect(self.add_situation)
        
        self.edit_situation_button = QPushButton("✏️")
        self.edit_situation_button.clicked.connect(self.edit_situation)

        self.delete_situation_button = QPushButton("➖")
        self.delete_situation_button.clicked.connect(self.delete_situation)

        self.setup_ui()
        
        #initialize situations
        self.update_Situations()
        
        self.initialize_combo_boxes()
        self.list_editor.lists_changed.connect(self.update_combobox_items)
        
    def setup_ui(self):
        left_col = QVBoxLayout()
        configuration_scenario_layout = QFormLayout()
        configuration_scenario_layout.setContentsMargins(0, 0, 0, 0)
        configuration_scenario_layout.addRow(QLabel("Situation Name:"), self.situation_name_edit)
        configuration_scenario_layout.addRow(QLabel("Select Configuration:"), self.situation_config_combobox)
        configuration_scenario_layout.addRow(QLabel("Select Scenario:"), self.situation_scenario_combobox)
        configuration_scenario_layout.addRow(QLabel("Select Return Period(s):"), self.situation_return_period_list)

        left_col.addLayout(configuration_scenario_layout)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)
        buttons_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(self.add_situation_button)
        buttons_layout.addWidget(self.edit_situation_button)
        buttons_layout.addWidget(self.delete_situation_button)
        
        left_col.addLayout(buttons_layout)
        
        self.main_layout.addLayout(left_col)
        self.main_layout.addWidget(self.situations_table)
        self.main_layout.setStretch(1, 2)

    def update_Situations(self):
        self.Situations = {}
        for index, row in self.get_situations().iterrows():
            situation = Situation()
            situation.update_from_generator(self, row["SituationID"])
            self.Situations[situation.id] = situation
        
    def initialize_combo_boxes(self):
        self.situation_config_combobox.addItems(self.list_editor.config_list)
        self.situation_scenario_combobox.addItems(self.list_editor.scenario_list)
        self.situation_return_period_list.addItems(self.list_editor.return_period_list)

    def add_situation(self):   
        #get values from user input
        name = self.situation_name_edit.text()        
        config = self.situation_config_combobox.currentText()
        scenario = self.situation_scenario_combobox.currentText()
        selected_RT = self.situation_return_period_list.selectedItems()
        selected_RT_text = [item.text() for item in selected_RT]
        return_period = "; ".join(selected_RT_text)

        self.situations_input_verify(name, config, scenario, return_period)

        # #verify values
        # verify_dict = {
        #     "Situation name": name,
        #     "System configuration": config,
        #     "Scenario / Time Frame": scenario,
        #     "Return period": return_period
        # }
        
        # for key, item in verify_dict.items():
        #     if item == "":
        #         QMessageBox.critical(self, "Error", f"{key} cannot be empty!")
        #         return
        #     elif not re.match(r'^[a-zA-Z0-9_()]+$', item) and key != "Return period":
        #         QMessageBox.critical(self, "Error", "Item contains invalid characters!")
        #         return
        #     if key == "Situation name":   # Verifies if the name does not exist in the 1st column of the table
        #         for row in range(self.situations_model.rowCount()):
        #             if self.situations_model.data(self.situations_model.index(row, 1)) == name:
        #                 QMessageBox.critical(self, "Error", "Situation name already exists, please change!")
        #                 return
                    
        # # Verifies that such situation is not already created
        # for row in range(self.situations_model.rowCount()):
        #     if (
        #         self.situations_model.data(self.situations_model.index(row, 2)) == config
        #         and self.situations_model.data(self.situations_model.index(row, 3)) == scenario
        #         and self.situations_model.data(self.situations_model.index(row, 4)) == return_period
        #         ):
        #         QMessageBox.critical(self, "Error", "Situation already exists with the same configuration, scenario, and return period.")
        #         return              

        # Set the values in the model/table and consequently on the database
        row_position = self.situations_model.rowCount()
        self.situations_model.insertRows(row_position, 1)
        self.situations_model.setData(self.situations_model.index(row_position, 1), name)
        self.situations_model.setData(self.situations_model.index(row_position, 2), config)
        self.situations_model.setData(self.situations_model.index(row_position, 3), scenario)
        self.situations_model.setData(self.situations_model.index(row_position, 4), return_period)
        self.situations_model.submitAll()
        
        situation_id = self.situations_model.data(self.situations_model.index(row_position, 0))
        #Clear the name input field
        self.situation_name_edit.setText("")
        
        self.update_Situations()
        self.situationsModified.emit("new", situation_id)

    def edit_situation(self):
        selected_row = self.situations_table.currentIndex().row()
        if selected_row >= 0:
            id = self.situations_model.data(self.situations_model.index(selected_row, 0))
            name = self.situations_model.data(self.situations_model.index(selected_row, 1))
            config = self.situations_model.data(self.situations_model.index(selected_row, 2))
            scenario = self.situations_model.data(self.situations_model.index(selected_row, 3))
            return_period = self.situations_model.data(self.situations_model.index(selected_row, 4))

            current_data = [name, config, scenario, return_period]
            
            dialog = EditSituationDialog(current_data, self.list_editor)
            if dialog.exec() == QDialog.Accepted:
                updated_name = dialog.get_name()
                updated_config = dialog.get_config()
                updated_scenario = dialog.get_scenario()
                updated_return_period = dialog.get_return_period() 

                self.situations_input_verify(updated_name, updated_config, updated_scenario, updated_return_period)

                # Set new data for the edited row
                self.situations_model.setData(self.situations_model.index(selected_row, 1), updated_name)
                self.situations_model.setData(self.situations_model.index(selected_row, 2), updated_config)
                self.situations_model.setData(self.situations_model.index(selected_row, 3), updated_scenario)
                self.situations_model.setData(self.situations_model.index(selected_row, 4), updated_return_period)
                self.situations_model.setData(self.situations_model.index(selected_row, 4), updated_return_period)
                self.situations_model.submitAll()
                
                self.update_Situations()
                self.situationsModified.emit("update", id)
                #self.rainfallModified.emit(id)
        
    def delete_situation(self):
        selected_row = self.situations_table.currentIndex().row()
        situation_id = self.situations_model.data(self.situations_model.index(selected_row, 0), 0)
        
        if selected_row >= 0:
            result = QMessageBox.question(self, "Delete Situation", "Deleting the situation will erase all the associated data of the analysis. Are you sure?", QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                # Attempt to remove the row from the model
                if not self.situations_model.removeRow(selected_row):
                    error_message = self.situations_model.lastError().text()
                    QMessageBox.critical(self, "Error", f"Failed to delete row: {error_message}")
                else:
                    # Submit the changes to the database
                    if not self.situations_model.submitAll():
                        error_message = self.situations_model.lastError().text()
                        QMessageBox.critical(self, "Error", f"Failed to submit changes to the database: {error_message}")
                    else:
                        self.situations_model.select()
                        self.situations_table.clearSelection()
                        
                        self.update_Situations()
                        self.situationsModified.emit("delete", situation_id)
                        #self.situationDeleted.emit(situation_id)
                        
    def update_combobox_items(self, configurations, scenarios, return_periods):
        
        #Update Situation Generator Lits:
        self.situation_config_combobox.clear()
        self.situation_scenario_combobox.clear()
        self.situation_return_period_list.clear()

        self.situation_config_combobox.addItems(configurations)
        self.situation_scenario_combobox.addItems(scenarios)
        self.situation_return_period_list.addItems(return_periods) 

    def get_situations(self):     
        if self.study_db.isValid() or not self.study_db.isOpen():
            situations_dataframe = M_OperateDatabases.fetch_table_from_database(self.study_db, "StudySituations")
            return situations_dataframe
    
    def situations_input_verify(self, name, config, scenario, return_period):
        #verify values
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
            elif not re.match(r'^[a-zA-Z0-9_()]+$', item) and key != "Return period":
                QMessageBox.critical(self, "Error", "Item contains invalid characters!")
                return
            # elif not re.match(r'^[0-9]+$', item) and key == "Return period":
            #     QMessageBox.critical(self, "Error", "Return must be integer!")
            #     return               
            if key == "Situation name":   # Verifies if the name does not exist in the 1st column of the table
                for row in range(self.situations_model.rowCount()):
                    if self.situations_model.data(self.situations_model.index(row, 1)) == name:
                        QMessageBox.critical(self, "Error", "Situation name already exists, please change!")
                        return
                    
        # Verifies that such situation is not already created
        for row in range(self.situations_model.rowCount()):
            if (
                self.situations_model.data(self.situations_model.index(row, 2)) == config
                and self.situations_model.data(self.situations_model.index(row, 3)) == scenario
                and self.situations_model.data(self.situations_model.index(row, 4)) == return_period
                ):
                QMessageBox.critical(self, "Error", "Situation already exists with the same configuration, scenario, and return period.")
                return     
        return True
                   
class EditSituationDialog(QDialog):
    def __init__(self, current_data, ListEditor: ListEditor):
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
        self.config_combo.addItems(ListEditor.config_list)
        self.config_combo.setCurrentText(config)

        scenario = current_data[2]
        scenario_label = QLabel("Scenario:")
        self.scenario_combo = QComboBox()
        self.scenario_combo.addItems(ListEditor.scenario_list)
        self.scenario_combo.setCurrentText(scenario)

        return_period = current_data[3]
        return_period_label = QLabel("Rainfall return period(s):")
        self.return_period_list = QListWidget()
        self.return_period_list.setSelectionMode(QListWidget.MultiSelection)
        self.return_period_list.addItems(ListEditor.return_period_list)
        for index in range(self.return_period_list.count()):
            item = self.return_period_list.item(index)
            if item.text() in return_period:
                item.setSelected(True)


        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(config_label)
        layout.addWidget(self.config_combo)
        layout.addWidget(scenario_label)
        layout.addWidget(self.scenario_combo)
        layout.addWidget(return_period_label)
        layout.addWidget(self.return_period_list)

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
        selected_RT = self.return_period_list.selectedItems()
        selected_RT_text = [item.text() for item in selected_RT]    
        return_period = "; ".join(selected_RT_text)
        return return_period

class Situation():

    def __init__(self):

        self.id = None
        self.name = None
        self.system_config = None
        self.timeframe = None
        self.rainfall = None 
        self.functional_index = 0
        self.performance_index = 0
        self.overall_index = 0
                
    def update_from_generator(self,
               SituationGenerator: SituationGenerator,
               Situation_ID: int):
        
        situations = SituationGenerator.get_situations()
        
        if Situation_ID == -1:
            self.id = None
            self.name = None
            self.system_config = None
            self.timeframe = None
            self.rainfall = None
        else:
            selected_situation = situations[situations['SituationID'] == Situation_ID].squeeze()
            self.id = selected_situation["SituationID"]
            self.name = selected_situation["SituationName"]
            self.system_config = selected_situation["SystemConfiguration"]
            self.timeframe = selected_situation["TimeFrame"]
            rainfall_values = selected_situation["Rainfall"].split("; ")
            self.rainfall = [int(value) for value in rainfall_values]  #list of Rainfall return periods as integers!
            

if __name__ == "__main__":
    app = QApplication([])
    
    list_layout = QVBoxLayout()
    generator_layout = QVBoxLayout()
    
    list_editor = ListEditor(list_layout)
    shared_table = SituationGenerator(generator_layout, list_editor)

    list_editor.lists_changed.connect(shared_table.update_combobox_items)

    main_layout = QVBoxLayout()
    main_layout.addLayout(list_layout)
    main_layout.addLayout(generator_layout)
    
    central_widget = QWidget()
    central_widget.setLayout(main_layout)

    main_window = QMainWindow()
    main_window.setCentralWidget(central_widget)
    main_window.setWindowTitle('Situation Editor')
    main_window.setGeometry(100, 100, 800, 600)

    main_window.show()
    app.exec()
