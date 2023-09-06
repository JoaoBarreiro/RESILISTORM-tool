from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog, QSpacerItem, QSizePolicy, QDialog, QLabel, QScrollArea, QMessageBox, QFrame, QFormLayout, QLineEdit
from PySide6.QtCore import Qt
import re

class ExpandableElement(QWidget):
    def __init__(self, parent=None, default_label=""):
        super().__init__(parent)
        self.setup_ui(default_label)
        self.expanded = False

    def setup_ui(self, default_label):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create a frame for the header labels and a simple horizontal line
        header_frame = QFrame(self)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Create a horizontal layout for the header labels (self.label, self.edit_label, self.expand_label)
        header_labels_layout = QHBoxLayout()

        # Create a label for the element's text (self.label)
        self.label = QLabel(default_label, self)

        # Create a horizontal spacer to push self.label to the left
        label_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # label_spacer = QWidget(self)
        # label_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Create a label for the ✏️ button (self.edit_label)
        self.edit_label = QLabel("✏️", self)
        self.edit_label.setAlignment(Qt.AlignCenter)
        self.edit_label.setCursor(Qt.PointingHandCursor)
        self.edit_label.mousePressEvent = self.edit_label_text

        # Create a label for the expand/collapse arrow (self.expand_label)
        self.expand_label = QLabel("▼", self)  # Use ▼ for down arrow and ▲ for up arrow
        self.expand_label.setAlignment(Qt.AlignCenter)
        self.expand_label.setCursor(Qt.PointingHandCursor)
        self.expand_label.mousePressEvent = self.toggle_properties

        # Add the labels to the header_labels_layout
        header_labels_layout.addWidget(self.label)
        header_labels_layout.addItem(label_spacer)
        header_labels_layout.addWidget(self.edit_label)
        header_labels_layout.addWidget(self.expand_label)

        header_layout.addLayout(header_labels_layout)

        # Create a simple horizontal line
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        header_layout.addWidget(line)

        self.layout.addWidget(header_frame)

        # Create a widget for the expandable properties (e.g., labels and input fields)
        self.properties_widget = QWidget(self)
        self.properties_layout = QFormLayout(self.properties_widget)

        # Add labels and input fields for the form
        labels = ["Rainfall:", "System configuration:", "Outfall conditions:", "Comments:"]
        self.form_fields = {}

        for label_text in labels:
            label = QLabel(label_text, self)
            input_field = QLineEdit(self)
            self.form_fields[label_text] = input_field
            self.properties_layout.addRow(label, input_field)

        self.properties_layout.setVerticalSpacing(5)  # Adjust vertical spacing as needed
        self.properties_widget.hide()
        
        header_layout.addWidget(self.properties_widget)

        # Create a delete button for the element (only visible when expanded)
        self.delete_button = QPushButton("❌ Delete scenario", self)  # Symbol ❌ added
        self.delete_button.clicked.connect(self.delete_element)
        self.delete_button.hide()

        # Create a layout for the delete button and spacer
        header_button_layout = QHBoxLayout()
        header_button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        header_button_layout.addWidget(self.delete_button)

        header_layout.addLayout(header_button_layout)

        self.layout.addWidget(header_frame)

        
    def toggle_properties(self, event):
        self.expanded = not self.expanded
        self.properties_widget.setVisible(self.expanded)
        if self.expanded:
            self.expand_label.setText("▲")  # Change to up arrow when expanded
            self.delete_button.show()
        else:
            self.expand_label.setText("▼")  # Change to down arrow when collapsed
            self.delete_button.hide()

    def edit_label_text(self, event):
        while True:
            new_label, ok = QInputDialog.getText(self, "Edit scenario name", "Enter new scenario name:")
            if ok:
                if new_label.strip() and re.match(r'^[a-zA-Z0-9_]+$', new_label.strip()):
                    self.label.setText(new_label)
                    break         
                elif not new_label.strip():  # Input is empty or whitespace
                    warning_dialog = WarningDialog('Scenario name must not be empty!', self)
                    warning_dialog.exec()
                elif not re.match(r'^[a-zA-Z0-9_]+$', new_label.strip()):
                    warning_dialog = WarningDialog('Scenario name must not have special characters!', self)
                    warning_dialog.exec()
            else:
                break

    def delete_element(self):
        # Show a confirmation dialog
        confirmation = QMessageBox.question(
            self,
            "Delete scenario",
            f"Are you sure you want to delete the scenario '{self.label.text()}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        # If the user confirms the deletion, remove the element
        if confirmation == QMessageBox.Yes:
            self.deleteLater()

class WarningDialog(QDialog):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Warning")
        layout = QVBoxLayout(self)
        label = QLabel(f"{text}", self)
        layout.addWidget(label)

        button_container = QWidget(self)  # Create a container for the button
        button_layout = QHBoxLayout(button_container)  # Create a layout for the button container

        ok_button = QPushButton("OK", self)
        ok_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set size policy for the button
        ok_button.clicked.connect(self.accept)

        button_layout.addWidget(ok_button)
        layout.addWidget(button_container)  # Add the button container to the main layout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Scenario set-up")
        
        # Create a central widget to hold the content
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a layout for the central widget
        self.layout = QVBoxLayout(central_widget)
        
        # Create a layout for the button
        button_layout = QHBoxLayout()
        
        # Add Element button to respective layout   
        add_element_button = QPushButton("➕ Add new scenario", central_widget)
        add_element_button.clicked.connect(self.add_element)
        button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(add_element_button)
        button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)
        
        # Define the layout for the scenarios (expandable elements)
        scenarios_container = QWidget()
        self.scenarios_layout = QVBoxLayout(scenarios_container)
        self.scenarios_layout.setSpacing(0)  # Adjust the spacing between elements
        
        # Create a scroll area for scenarios
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidget(scenarios_container)
 
        # Add the scroll area to the layout
        self.layout.addWidget(scroll_area)
        

    def add_element(self):
        while True:
            new_label, ok = QInputDialog.getText(self, "Add scenario", "New scenario name:")
            
            if ok:
                if  new_label.strip() and re.match(r'^[a-zA-Z0-9_]+$', new_label.strip()):  # Check if the input is not empty or whitespace and if has no strange characters
                    expandable_element = ExpandableElement(default_label=new_label)
                    # Remove any existing vertical spacer (if present) before adding the new element
                    if self.scenarios_layout.count() >= 1:
                        item = self.scenarios_layout.itemAt(self.scenarios_layout.count() - 1)
                        self.scenarios_layout.removeItem(item)
                    
                    self.scenarios_layout.addWidget(expandable_element)
                    
                    # Add vertical spacer below the last added element
                    self.scenarios_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
                    
                    break  # Exit the loop if a valid input is provided
                elif not new_label.strip():  # Input is empty or whitespace
                    warning_dialog = WarningDialog('Scenario name must not be empty!', self)
                    warning_dialog.exec()
                elif not re.match(r'^[a-zA-Z0-9_]+$', new_label.strip()):
                    warning_dialog = WarningDialog('Scenario name must not have special characters!', self)
                    warning_dialog.exec()                    
            else:
                break

if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.setFixedSize(400, 500)
    main_window.show()
    app.exec()