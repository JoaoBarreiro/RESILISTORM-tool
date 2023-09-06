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

class SingleBarGraphWidget(QWidget):
    def __init__(self, value, xmax):
        super().__init__()
        self.value = value
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
            #self.ax.set_xticklabels([f"{tick}%" for tick in range(0, 101, 25)])
        elif self.xmax == 1:
            self.ax.set_xticks(np.arange(0, 1.01, 0.25))
            #self.ax.set_xticklabels([f"{tick}" for tick in np.arange(0, 1.01, 0.25)])
        self.ax.set_xticklabels([])

        self.ax.xaxis.set_tick_params(labelsize = "small")
        self.ax.yaxis.set_tick_params(labelsize = "small")
        
        # Set the number of y values
        self.ax.set_yticks(range(1))
        self.ax.set_yticklabels(())
        
        # Hide the top and bottom axis lines
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        
        # Hide vertical gridlines
        self.ax.grid(False)
        
        # Set the background color with 50% transparency
        self.fig.patch.set_facecolor("AliceBlue")
        self.fig.patch.set_alpha(0)     
           
        # Set the facecolor to none
        self.ax.set_facecolor('none')
        
        # Create a colormap and normalize the values
        cmap = cm.get_cmap('RdYlGn')
        norm = plt.Normalize(0, self.xmax)
        
        #colors = [cmap(norm(value)) if value != '' else 'darkgrey' for value in self.values]
        
         # Create a values bar      
        self.bar = self.ax.barh(1, self.value, alpha= 1, color = cmap(norm(self.value)), zorder = 1)
        
        # Create a light grey bar as a background behind the data bars
        self.ax.barh(1, self.xmax, color='lightgrey', edgecolor = 'black', linewidth = 0.5, alpha = 0.2, zorder=0)

        # Create the canvas to display the plot
        self.canvas = FigureCanvas(self.fig)

        # Connect the mouse motion event
        self.canvas.mpl_connect('motion_notify_event', self.on_bar_hover)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        # Initialize the text element for the value inside the bars
        self.text = None    

    def animateBars(self):
        def update(frame):
            progress = frame / self.frames * self.xmax
            max_value = max(self.value)
            for bar, w in zip(self.bar, self.value):
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
            for bar in self.bar:
                if bar.contains(event)[0]:
                    # Add a contour
                    bar.set_edgecolor('darkblue')
                    bar.set_linewidth(1)
                    # Get the value of the hovered bar
                    value = self.value
                    
                    # Remove the previous text element if it exists
                    if self.text:
                        self.text.remove()
                    # Add the text for the value inside the bar
                    
                    normvalue = value / self.xmax
                    
                    labelpad = 0.025 * self.xmax
                    
                    if self.xmax == 1:
                        label = f"{(value):.2f}"
                    elif self.xmax == 100:
                        label = f"{str(value)}%"
                    
                    if normvalue <= 0.1:
                        self.text = self.ax.text(value + labelpad, 1, label , va='center', ha = "left")
                    else:
                        self.text = self.ax.text(value -labelpad, 1, label , va='center', ha = "right")    
                else:
                    bar.set_edgecolor('none')
                     
                    if self.text:
                        self.text.remove()
                        self.text = None
        else:
            for bar in self.bar:
                bar.set_edgecolor('none')
            if self.text:
                self.text.remove()
                self.text = None
        
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SingleBarGraphWidget(value = 0.12 , xmax = 1)
    widget.show()
    sys.exit(app.exec())
