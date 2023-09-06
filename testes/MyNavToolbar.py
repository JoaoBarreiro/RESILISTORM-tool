import sys
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MyNavToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)

        # Set the desired icon size (e.g., 24x24 pixels)
        icon_size = QSize(1, 1)

        # Find the buttons that you want to modify the icon size for
        buttons = [child for child in self.findChildren(QToolButton) if child.text() in ['Home', 'Zoom', 'Save']]


        # Set the icon size for each button
        for button in buttons:
            button.setIconSize(icon_size)
            
    #     # Hide all buttons
    #     self.hide_buttons()

    # def hide_buttons(self):
    #     # List of button names to show
    #     visible_buttons = ["Home", "Zoom", "Save"]

    #     # Find all QToolButton instances within the toolbar
    #     buttons = self.findChildren(QToolButton)

    #     # Iterate over each button and show/hide based on visibility list
    #     for button in buttons:
    #         if button.text() in visible_buttons:
    #             button.setVisible(True)
    #         else:
    #             button.setVisible(False)