import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
import numpy as np

class CircularGraphWidget(QWidget):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.initUI()     
        
    def initUI(self):
        self.fig = Figure(constrained_layout=True)
        self.ax = self.fig.add_subplot(111)
        
        # Set the self.axis limits and remove the self.axis labels
        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.axis("off")
        self.ax.set_aspect('equal')
        
        # Set the background color with 50% transparency
        self.fig.patch.set_facecolor('white')
        self.fig.patch.set_alpha(0.0)   
        
        # Get the colors for the wedges
        self.cmap = cm.get_cmap('RdYlGn')
        self.norm = plt.Normalize(0, 1)
        empty_color = 'lightgrey'

        # Create the grey back wedge:
        wedge_empty = patches.Wedge(center = (0, 0), r = 1, theta1 = 0, theta2= 360, width=0.4, facecolor=empty_color, alpha = 0.2, edgecolor = 'black', linewidth = 0.5,)
        self.ax.add_patch(wedge_empty)

        # Create the filled part of the circular bar
        self.wedge_filled = patches.Wedge(center = (0, 0), r = 1, theta1 = 0, theta2= 360 * self.value, width=0.4, facecolor = self.cmap(self.norm(self.value)), edgecolor='black')
        self.ax.add_patch(self.wedge_filled)

        # Create a new axes for the text label
        self.text_ax = self.fig.add_axes([0, 0, 1, 1], zorder=1)
        self.text_ax.axis('off')
        self.text_label = self.text_ax.text(0.5, 0.5, f'{self.value}', ha='center', va='center', fontsize = 30)    
        
        # Create the canvas to display the plot
        self.canvas = FigureCanvas(self.fig)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
             

    def animateWedge(self):
        self.wedge_filled.set_theta2(0)
        self.wedge_filled.set_facecolor('None')
        self.text_label.set_fontsize(0)
        
        def update(frame):
            # Calculate the normalized value based on the frame
            norm_value = frame / 100
            #self.frames

            # Calculate the end angle for the filled part of the circular bar
            end_angle = 360 * norm_value

            # Update the theta2 value of the filled part of the circular bar
            self.wedge_filled.set_theta2(end_angle)
            self.wedge_filled.set_facecolor(self.cmap(self.norm(norm_value)))

        
            self.text_label.set_fontsize(norm_value * 30/self.value)

            if norm_value >= self.value:
                self.canvas.draw()
                self.animation.event_source.stop()
            else:
                self.canvas.draw()
       
        self.frames = 150  # Number of frames in the animation
        self.animation = FuncAnimation(self.fig, update, frames=self.frames, interval=0.2)
        self.canvas.draw_idle()   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    value = 0.5
    widget = CircularGraphWidget(value)
    widget.show()
    widget.animateWedge()  # Start the animation
    sys.exit(app.exec())
