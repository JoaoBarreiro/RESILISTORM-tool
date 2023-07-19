import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties
import time
import numpy as np

class BarGraphWidget(QWidget):
    def __init__(self, categories, values, xmax):
        super().__init__()
        self.categories = categories
        self.values = values
        self.xmax = xmax
        self.initUI()

    def initUI(self):
        # Create a figure and axes
        self.fig = Figure(constrained_layout=True)
        self.ax = self.fig.add_subplot(111)

        # Fix the X values between 0 and 100%
        self.ax.set_xlim(0, self.xmax)

        # Set the x-axis tick intervals to 25 and show % sign
        if self.xmax == 100:
            self.ax.set_xticks(range(0, 101, 25))
            self.ax.set_xticklabels([f"{tick}%" for tick in range(0, 101, 25)])
        elif self.xmax == 1:
            self.ax.set_xticks(np.arange(0, 1.01, 0.25))
            self.ax.set_xticklabels([f"{tick}" for tick in np.arange(0, 1.01, 0.25)])
        
        # Set the number of y values
        self.ax.set_yticks(range(len(self.categories)))
        self.ax.set_yticklabels(self.categories, weight ='bold')
        
        # Hide the top and bottom axis lines
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        
        # Hide vertical gridlines
        self.ax.grid(False)
        
        # Set the background color with 50% transparency
        self.fig.patch.set_facecolor('white')
        self.fig.patch.set_alpha(0.0)     
           
        # Set the facecolor to none
        self.ax.set_facecolor('none')
        
        # Create a colormap and normalize the values
        cmap = cm.get_cmap('RdYlGn')
        norm = plt.Normalize(0, self.xmax)
        
        #colors = [cmap(norm(value)) if value != '' else 'darkgrey' for value in self.values]
        
         # Create a values bar      
        self.bars = self.ax.barh(self.categories, self.values, height = 0.3, alpha= 1, color = cmap(norm(self.values)), zorder = 1)
        
        # Create a light grey bar as a background behind the data bars
        self.ax.barh(self.categories, self.xmax, color='lightgrey', edgecolor = 'black', linewidth = 0.5, height = 0.3, alpha = 0.2, zorder=0)

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

    def animateBars(self):
        
        def update(frame):
            progress = frame / self.frames * self.xmax
            max_value = max(self.values)
            for bar, w in zip(self.bars, self.values):
                width = min(progress , w)
                bar.set_width(width)

            self.canvas.draw()
            
            if progress >= max_value:
                self.animation.event_source.stop()

        self.frames = 100
        self.animation = animation.FuncAnimation(self.fig, update, frames = self.frames, interval= 0.2)
        self.canvas.draw_idle()
    
    def on_bar_hover(self, event):
        if event.inaxes == self.ax:
            for i, bar in enumerate(self.bars):
                if bar.contains(event)[0]:
                    # Set the transparency of the hovered bar to 1.0
                    #bar.set_alpha(1)
                    # Add a contour
                    bar.set_edgecolor('darkblue')
                    bar.set_linewidth(1)
                    
                    # Get the value of the hovered bar
                    value = self.values[i] 
                    
                    # Remove the previous text element if it exists
                    if self.text:
                        self.text.remove()
                   
                    # Add the text for the value inside the bar
                    if self.xmax == 100:
                        self.text = self.ax.text(value + 1, i, f"{str(value)}%", va='center')
                    elif self.xmax == 1:
                        self.text = self.ax.text(value + 0.01, i, f"{str(value)}", va='center')
                    
                else:
                    # Set the transparency of non-hovered bars to 0.5
                    bar.set_alpha(0.5)
                    bar.set_edgecolor('none')
                    
            # Remove the text element if it exists and the mouse is not over any bar
            if not any(bar.contains(event)[0] for bar in self.bars):
                for i, bar in enumerate(self.bars):
                    bar.set_alpha(1)
                if self.text:
                    self.text.remove()
                    self.text = None

            self.canvas.draw()
            
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = BarGraphWidget(categories = ['1', '2', '3'], values = [0.3, 0.5, 1], xmax = 1)
    widget.show()
    sys.exit(app.exec())
