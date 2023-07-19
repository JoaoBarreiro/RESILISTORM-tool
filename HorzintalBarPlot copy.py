import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Data for the bar plot
categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4']
values = [10, 20, 15, 25]

class BarGraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a figure and axes
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Create the horizontal bar plot
        self.bars = self.ax.barh(categories, values, alpha=0.8)

        # Create the canvas to display the plot
        self.canvas = FigureCanvas(self.fig)

        # Connect the mouse motion event
        self.canvas.mpl_connect('motion_notify_event', self.on_bar_hover)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # Initialize the text element for the value inside the bars
        self.text = None
        
    def on_bar_hover(self, event):
        if event.inaxes == self.ax:
            for i, bar in enumerate(self.bars):
                if bar.contains(event)[0]:
                    # Set the transparency of the hovered bar to 1.0
                    bar.set_alpha(1)
                    # Add a contour
                    bar.set_edgecolor('darkblue')
                    bar.set_linewidth(1)
                    
                    # Get the value of the hovered bar
                    value = values[i] 
                    
                    # Remove the previous text element if it exists
                    if self.text:
                        self.text.remove()

                    # Add the text for the value inside the bar
                    self.text = self.ax.text(value, i, str(value), va='center')
                    
                else:
                    # Set the transparency of non-hovered bars to 0.5
                    bar.set_alpha(0.8)
                    bar.set_edgecolor('none')

            self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = BarGraphWidget()
    widget.show()
    sys.exit(app.exec())
