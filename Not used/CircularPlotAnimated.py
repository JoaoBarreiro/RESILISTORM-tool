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
        self.category = categorizeResilience(self.value)
        
        self.fontsize = int(self.width() / 40)

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
        self.fig.patch.set_facecolor("AliceBlue")
        self.fig.patch.set_alpha(0)   
        
        # Get the colors for the wedges
        self.cmap = cm.get_cmap('RdYlGn')
        self.norm = plt.Normalize(0, 1)
        
        self.WedgeRadius = 1
        self.WedgeWidth = 0.3
        
        # Create the grey back wedge:
        wedge_empty = patches.Wedge(center = (0, 0), r = self.WedgeRadius, theta1 = 0, theta2= 360, width = self.WedgeWidth, facecolor='lightgrey', alpha = 0.2, edgecolor = 'black', linewidth = 0.5)
        self.ax.add_patch(wedge_empty)

        # Create the filled part of the circular bar
        self.wedge_filled = patches.Wedge(center = (0, 0), r = self.WedgeRadius , theta1 = 0, theta2= 360 * self.value, width = self.WedgeWidth, facecolor = self.cmap(self.norm(self.value)), edgecolor='none')
        self.ax.add_patch(self.wedge_filled)

        # Create a new axes for the text label
        self.text_ax = self.fig.add_axes([0, 0, 1, 1], zorder=1)
        self.text_ax.axis('off')          
        
        self.text_label = self.text_ax.text(0.5, 0.5, f'{self.category}', ha='center', va='center', fontsize = self.fontsize)    
        
        # Create the canvas to display the plot
        self.canvas = FigureCanvas(self.fig)
        
        # Connect the mouse motion event
        #self.canvas.mpl_connect('motion_notify_event', self.on_bar_hover)
        
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        # Initialize text for on_bar_hover
        self.text_value = None

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

            self.text_label.set_fontsize(norm_value * self.fontsize/self.value)

            if norm_value >= self.value:
                #self.canvas.draw()
                self.animation.event_source.stop()
                # Connect the mouse motion event  
                self.canvas.mpl_connect('motion_notify_event', self.on_bar_hover)
            self.canvas.draw()
        
        self.frames = 150  # Number of frames in the animation
        self.canvas.draw_idle()   
        self.animation = FuncAnimation(self.fig, update, frames=self.frames, interval=0.2)

        # Initialize text for on_bar_hover
        self.text_value = None

    def on_bar_hover(self, event):

        if self.wedge_filled.contains(event)[0]:
            # Add a contour
            self.wedge_filled.set_edgecolor('darkblue')
            self.wedge_filled.set_linewidth(1)
            # Get the value of the hovered bar
            value = self.value
            
            # Remove the previous text element if it exists
            if self.text_value:
                self.text_value.remove()
            
            label = f"{(value):.2f}"
            
            # Calculate the angular position for the text label
            end_angle = 360 * value
            padding = self.WedgeWidth / 2  
            label_padding_angle = -10
            
            if end_angle <= 25:
                label_padding_angle = - label_padding_angle
            
            if end_angle <= 90:
                text_angle = end_angle - label_padding_angle - 90
            elif end_angle <= 180:
                text_angle = -(180 - end_angle - label_padding_angle) + 90
            elif end_angle <= 270:
                text_angle = -(180 - end_angle - label_padding_angle) - 90 
            else:
                text_angle = end_angle - label_padding_angle + 90
                       
           # Calculate the (x, y) coordinates for the text
            x = (self.WedgeRadius - padding) * np.cos(np.deg2rad(end_angle + label_padding_angle))
            y = (self.WedgeRadius - padding) * np.sin(np.deg2rad(end_angle + label_padding_angle))
                    
            # Add the text to the plot using the text method of the Axes object
            self.text_value = self.ax.text(x, y, label, rotation = text_angle, ha='center', va='center', size=self.fontsize/1.5, color='black')
        
        else:
            self.wedge_filled.set_edgecolor('none')
                
            if self.text_value:
                self.text_value.remove()
                self.text_value = None
        
        self.canvas.draw()
        
def categorizeResilience(value):

    categorization = {
        'Bad': (0.00, 0.30),
        'Insufficient': (0.30, 0.55),
        'Acceptable': (0.55, 0.75),
        'Good': (0.75, 0.90),
        'Great': (0.90, 1.00)
        } 
    
    if value == 1:
        return "Great"
    else:
        for category, (lower,upper) in categorization.items():
            if lower <= value < upper:
                resilienceClass = category
                return resilienceClass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    value = 0.65
    widget = CircularGraphWidget(value)
    widget.show()
    widget.animateWedge()  # Start the animation
    sys.exit(app.exec())
