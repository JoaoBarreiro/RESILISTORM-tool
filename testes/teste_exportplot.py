import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QWidget
from PySide6.QtGui import QAction
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plot Export Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a Figure and add a plot
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])

        # Create a FigureCanvas and set the Figure as its parent
        canvas = FigureCanvas(fig)

        # Set the FigureCanvas as the central widget
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(canvas)
        self.setCentralWidget(central_widget)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        # Create an "Export as Picture" action
        export_action = QAction("Export as Picture", self)
        export_action.triggered.connect(self.export_plot)

        # Add the action to the context menu
        context_menu.addAction(export_action)

        # Show the context menu at the position of the right-click event
        context_menu.exec_(self.mapToGlobal(event.pos()))

    def export_plot(self):
        # Code to save the plot as a picture
        # You can use matplotlib's savefig() function to save the plot as an image file
        # For example:
        # self.canvas.figure.savefig("plot.png")
        print("Plot exported!")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
