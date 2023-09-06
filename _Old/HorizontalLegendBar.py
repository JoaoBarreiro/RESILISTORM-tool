import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
import numpy as np


class HorizontalLegendBar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()     
        

    def initUI(self):
        self.fig = Figure(figsize=(6, 1))
        self.ax = self.fig.add_subplot(111)
        self.ax = self.fig.add_axes([0, 0, 1, 1])

        # Get the colors for the wedges
        self.cmap = cm.get_cmap('RdYlGn')
        self.norm = plt.Normalize(0, 1)

        sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
        sm.set_array([])

        colorbar = plt.colorbar(cax=self.ax, orientation='horizontal', cmap=self.cmap, norm=self.norm)
        colorbar.set_ticks([])
        colorbar.set_ticklabels([])
        
        # Set the custom tick positions and labels
        ticks = [0.15, 0.425, 0.65, 0.825, 0.95]
        ticklabels = ['Péssima', 'Insuficiente', 'Aceitável', 'Boa', 'Ótima']
        colorbar.set_ticks(ticks)
        colorbar.set_ticklabels(ticklabels)
        
        # Add the second set of ticks as minor ticks
        intervalticks = [0.0 , 0.3, 0.55, 0.75, 0.9, 1.0]
        colorbar.ax.set_xticks(intervalticks, minor=True)
        
        # Set the tick labels inside the colorbar
        colorbar.ax.xaxis.set_ticks_position('bottom')
        colorbar.ax.xaxis.set_label_position('bottom')
        colorbar.ax.tick_params(axis='x', pad=-0.5)
        
        # Create the canvas to display the plot
        self.canvas = FigureCanvas(self.fig)
        
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    value = 0.5
    widget = HorizontalLegendBar()
    widget.show()
    sys.exit(app.exec())

