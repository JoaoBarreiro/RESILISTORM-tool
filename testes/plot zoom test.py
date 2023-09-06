import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a matplotlib figure and canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)

        # Create and plot your data (you can use your own plotting logic here)
        self.plot_data()

    def plot_data(self):
        # Implement your plotting logic here using the self.figure and self.canvas objects
        # For example:
        ax = self.figure.add_subplot(111)
        ax.plot([1, 2, 3, 4], [10, 5, 8, 2])

        # Call the draw method to update the canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
