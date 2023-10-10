import sys
import pandas as pd
import numpy as np

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QMenu, QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties

class MultiHorizontalBarGraphWidget(QWidget):
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

        self.ax.xaxis.set_tick_params(labelsize = "small")
        self.ax.yaxis.set_tick_params(labelsize = "small")
        
        # Set the number of y values
        self.ax.set_yticks(range(len(self.categories)))
        self.ax.set_yticklabels(self.categories, weight ='bold')
        
        # Hide the top and bottom axis lines
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        
        # Hide vertical gridlines
        self.ax.grid(False)
        
        # Set the background color with 50% transparency
        self.fig.patch.set_facecolor("AliceBlue")
        self.fig.patch.set_alpha(1)     
           
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
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

class SingleHorizontalBarGraphWidget(QWidget):
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

class ResilienceHorizontalBarGraphWidget(QWidget):
    def __init__(self, dataframe: pd.DataFrame, xmax: int):
        super().__init__()
        self.df = dataframe.copy()
        self.xmax = xmax
        self.series_names = dataframe.index.tolist()
        self.num_series = len(self.series_names)
        self.series_values = dataframe.values.flatten().tolist()
        
        # Create a colormap and normalize the values
        cmap = cm.get_cmap('RdYlGn')
        norm = plt.Normalize(0, self.xmax)   
        
        self.df["Color"] = pd.Series()
        for index, row in self.df.iterrows():
            self.df.at[index, "Color"] = cmap(norm(self.df.at[index, "PerRes"]))
        
        self.emptyplot()

    def emptyplot(self):
        self.LinesToKeep = []
        
        # Create a figure and axes
        self.fig = Figure(constrained_layout=True)
        self.ax = self.fig.add_subplot(111)

        # Fix the X values between 0 and 100%
        self.ax.set_xlim(0, self.xmax)

        # Set the x-axis for the main ticjs and hide them
        x_ticks = [0, 0.3, 0.55, 0.75, 0.9, 1]
        self.ax.set_xticks(x_ticks)
        self.ax.set_xticklabels([])
        # Hide the minor x-tick marks
        self.ax.tick_params(which='major', length=0)

        # Set the x-axis ticks the labels to show
        x_labels_ticks = [0.15, 0.425, 0.65, 0.825, 0.95]
        x_labels = ['Bad', 'Insufficient', 'Acceptable', 'Good', 'Great']
        self.ax.set_xticks(x_labels_ticks, minor=True)
        self.ax.set_xticklabels(x_labels, minor=True)
        
        xLabelsFont = FontProperties(family='Segoe UI', style='normal', weight='bold', size=8)
        self.ax.tick_params(which='minor', length=0)
        
        for tick in self.ax.xaxis.get_minor_ticks():
            tick.label.set_fontproperties(xLabelsFont)

        # Display vertical lines on major x-ticks
        for tick in x_ticks:
            vline = self.ax.axvline(tick, color='lightgray', linewidth = 0.5, linestyle='--', zorder = 0)
            self.LinesToKeep.append(vline)

        # Set the number of y values
        self.ax.set_yticks([])
        self.ax.set_yticklabels([])

        # Hide the top and bottom axis lines
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)

        # Set the background color
        self.fig.patch.set_facecolor("AliceBlue")
        self.fig.patch.set_alpha(1)

        # Set the facecolor to none
        self.ax.set_facecolor('none')
        
        # Create the canvas to display the plot
        self.canvas = FigureCanvas(self.fig)

        # Set the layout for the main plot
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Initialize the text element for the value inside the bars
        self.text = None
        
        # Initizalir the baseline scenario for comparisons
        self.baseline_scenario = None
        
        # Initialize current series ploted names controler
        self.PlotedSeries = []
        
        #Initialize plot bars container
        self.bars = None
        self.greybars = None
        
    def set_baseline_scenario(self, baseline_scenario):
        self.baseline_scenario = baseline_scenario

    def update_series_visibility(self, series_name: str, Status: bool):
        
        if Status:
            if series_name not in self.PlotedSeries:
                self.PlotedSeries.append(series_name)
        else:
           if series_name in self.PlotedSeries:
                self.PlotedSeries.remove(series_name)            
              
        # Set the number of y values
        self.ax.set_yticks(range(len(self.PlotedSeries)))
        yLabelsFont = FontProperties(family='Segoe UI', style='normal', weight='bold', size=10)
        self.ax.set_yticklabels(self.PlotedSeries, fontproperties = yLabelsFont)
        
        if not self.PlotedSeries:
            self.ax.set_ylim(0, 1)
        else:
            self.ax.set_ylim(range(len(self.PlotedSeries))[0] - 0.5, range(len(self.PlotedSeries))[-1] + 0.5)

        # Filter the DataFrame based on the updated series_names in self.PlotedSeries
        df_Plot = self.df[self.df.index.isin(self.PlotedSeries)]
        
        # Clear the existing bars from the plot
        if self.bars:
            for bar in self.bars:
                bar.remove()      
        
        if self.greybars:
            for bar in self.greybars:
                bar.remove()              
        
        # Plot the bars from the filtered dataframe based on the series_names on self.PlotedSeries
        self.bars = self.ax.barh(range(len(self.PlotedSeries)), df_Plot["PerRes"], height = 0.3, alpha= 1, color = df_Plot["Color"], zorder = 2)
        
        # Create a light grey bar as a background behind the data bars
        self.greybars = self.ax.barh(range(len(self.PlotedSeries)), self.xmax, color='lightgrey', edgecolor = 'black', linewidth = 0.5, height = 0.3, alpha = 0.2, zorder = 1)

        self.canvas.draw()
        
        # Connect the mouse motion event
        self.canvas.mpl_connect('motion_notify_event', self.on_bar_hover)
        
        # Initialize the text element for the value inside the bars
        self.text = None

    def animateBars(self):

        def update(frame):
            progress = frame / self.frames * self.xmax
            max_value = max(self.series_values)
            for bar, w in zip(self.bars, self.series_values):
                width = min(progress , w)
                bar.set_width(width)

            self.canvas.draw()

            if progress >= max_value:
                self.animation.event_source.stop()

        self.frames = 150
        self.animation = animation.FuncAnimation(self.fig, update, frames = self.frames, interval= 0.2)
        self.canvas.draw_idle()

    def on_bar_hover(self, event):
        if event.inaxes == self.ax:
            for i, bar in enumerate(self.bars):
                if bar.contains(event)[0]:
                    # Add a contour
                    bar.set_edgecolor('darkblue')
                    bar.set_linewidth(1)

                    # Get the value of the hovered bar
                    value = self.series_values[i]

                    # Remove the previous text element if it exists
                    if self.text:
                        self.text.remove()

                    normvalue = value / self.xmax
                    labelpad = 0.025 * self.xmax

                    # Add the text for the value inside the bar
                    if self.xmax == 1:
                        label = f"{(value):.2f}"
                    elif self.xmax == 100:
                        label = f"{str(value)}%"

                    if normvalue <= 0.1:
                        self.text = self.ax.text(value + labelpad, i, label , va='center', ha = "left")
                    else:
                        self.text = self.ax.text(value - labelpad, i, label , va='center', ha = "right")

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
        else:
            if self.text:
                self.text.remove()
                self.text = None

        self.canvas.draw()
    
    def clearSelected_lines_and_text(self):
        # Remove the lines and text associated with the selected series
        for line in self.ax.lines:
            if line not in self.LinesToKeep:
                line.remove()

        for text in self.ax.texts:
            text.remove()

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
        self.animation = animation.FuncAnimation(self.fig, update, frames=self.frames, interval=0.2)

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

class ScatterPlotWidget(QWidget):
    def __init__(self, dataframe: pd.DataFrame(), xmax: int):
        super().__init__()
        self.df = dataframe.copy()
        self.xmax = xmax
        self.initUI()

    def initUI(self):
        
        self.LinesToKeep = []
        
        # Create a figure and axes
        self.fig = Figure(constrained_layout=True)
        self.ax = self.fig.add_subplot(111)

        self.ax.xaxis.set_tick_params(labelsize = "small")
        self.ax.yaxis.set_tick_params(labelsize = "small")

        # Set initial plot limits based on the data range
        min_value = self.df.iloc[:, :].astype(float).min().min()
        max_value = self.df.iloc[:, :].astype(float).max().max()

        self.ax.set_xlim(max(0, round(min_value - 0.1, 1)), min(1, round(max_value + 0.1), 1))
        
        #self.ax.set_xlim(0, self.xmax)
        #self.ax.set_xticks(np.arange(0, 1.01, 0.25))
        #self.ax.set_xticklabels([f"{tick}" for tick in np.arange(0, 1.01, 0.25)])

        # Get the categories (indicators) from the DataFrame columns
        self.categories = self.df.columns
        
        # Set the number of y values
        self.ax.set_yticks(range(len(self.categories)))
        self.ax.set_yticklabels(self.categories, weight='bold')
        
        self.ax.set_ylim(range(len(self.categories))[0] - 0.5, range(len(self.categories))[-1] + 0.5)

        # Hide the top and bottom axis lines
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)

        # Hide vertical gridlines
        self.ax.grid(False)

        # Set the background color with 50% transparency
        self.fig.patch.set_facecolor('AliceBlue')
        self.fig.patch.set_alpha(0)
        
        # Set the facecolor for the plot area within the axes
        self.ax.set_facecolor('AliceBlue')
        self.ax.patch.set_alpha(1)
        
        # Create a colormap with unique colors for each row (scenario) name
        self.cmap = cm.get_cmap('tab10', len(self.df.index))
        self.unique_row_names = self.df.index.unique()
        self.row_name_to_int = {name: i for i, name in enumerate(self.unique_row_names)}
        
        #Set a fixed color for each series_name
        self.df["Color"] = pd.Series()
        for index, row in self.df.iterrows():
            self.df.at[index, "Color"] = self.cmap(self.row_name_to_int[index])
        
        self.legend_entries = list(self.unique_row_names)

        self.marker_size = 60  # Set the marker size here -> unit is area


        # Initialize variables that will be used to control the data series visibility and plot legends
        self.data_series_visibility = {}
        for index in self.df.index.tolist():
            self.data_series_visibility[index] = False
            
        self.scatter_objects = []
        
        self.legend = None

        for i, category in enumerate(self.categories):
            values = self.df[category].tolist()  # Get the values for the category

            for j, value in enumerate(values):
                if value != None:
                    value = float(value)
                    scenario_name = self.df.index[j]
                    scatter = self.ax.scatter(value, i, marker='o', color = self.df.at[self.df.index[j], "Color"], s=self.marker_size, label=scenario_name, alpha = 0, zorder = 10)
                    self.scatter_objects.append(scatter)

        # Plot a horizontal light grey line between 0 and 1 for each category
        for i, _ in enumerate(self.categories):
           hline = self.ax.axhline(y=i, color='lightgrey', linestyle='--', linewidth=0.5, zorder = 0)
           self.LinesToKeep.append(hline)       
        
        self.canvas = FigureCanvas(self.fig)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Enable right-click context menu
        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas.customContextMenuRequested.connect(self.show_context_menu)

        self.baseline_scenario = None
        
        # Add lists to store texts
        self.texts = {}
        self.InteractiveElements = {}   # dict to save the created hlines and texts when legend is clicked. Key is series name
        
    def show_context_menu(self, pos):
        # Create a context menu at the specified position
        context_menu = QMenu(self)
        save_action = QAction("Save Figure As...", self)
        save_action.triggered.connect(self.save_figure)
        context_menu.addAction(save_action)
        context_menu.exec_(self.canvas.mapToGlobal(pos))

    def save_figure(self):
        # Prompt the user to save the figure
        file_path, _ = QFileDialog.getSaveFileName(None, "Save Figure As...", "", "PNG (*.png)")
        if file_path:
            self.canvas.figure.savefig(file_path, dpi = 300)
            
    def set_baseline_scenario(self, baseline_scenario):
        self.baseline_scenario = baseline_scenario

    def update_series_visibility(self, data_series_name, visible):

        # for scatter in self.scatter_objects:
        #     if scatter.get_label() == data_series_name:
        #         scatter.set_alpha(1 if visible else 0)

        if visible:
            self.data_series_visibility[data_series_name] = True
        else:
            self.data_series_visibility[data_series_name] = False

        # If legend exist, remove it from the plot
        # if self.legend is not None:
        #     self.legend.remove()

        # Get the handles for the visible entries

        for scatter in self.scatter_objects:
            scatter_series_name = scatter.get_label()
            if scatter_series_name == data_series_name:
                    scatter.set_alpha(1 if visible else 0)

        # Get the labels of the series set as Visible
        visible_labels = [series_name for series_name in self.data_series_visibility if self.data_series_visibility[series_name] == True]
        self.visible_scatters = [scatter for scatter in self.scatter_objects if scatter.get_label() in visible_labels]
        
        # Check if there are visible handles before creating the legend
        if self.visible_scatters:
            self.legend = self.ax.legend(handles = self.visible_scatters, labels = visible_labels, 
                                         fontsize="small", loc='center', bbox_to_anchor=(0.5, -0.2),
                                         ncol=min(3, len(visible_labels)), 
                                         labelspacing = 0.2, handletextpad=0.1)
            self.legend.set_visible(True)  # Make sure the legend is visible
            self.legend.set_picker(True) # Enable picking on the legend
            self.legend.figure.canvas.mpl_connect('pick_event', self.on_legend_pick)

        # self.legend.figure.canvas.mpl_connect('pick_event', self.on_legend_pick)
        self.SelectedSeries = None
        self.canvas.draw()
        
    def on_legend_pick(self, event):
        
        legend_label = None
        
        if event.mouseevent.button == 1:  # Left mouse button clicked
            legend_artist = event.artist
            legend_handles = legend_artist.legendHandles
            
            if not legend_label:            
                for handle in legend_handles:
                    contains, _ = handle.contains(event.mouseevent)
                    if contains:
                        legend_label = handle.get_label()
                        #print("Clicked on legend symbol:", legend_label)  
                        break

            if not legend_label:
                for text in legend_artist.get_texts():
                    if text.contains(event.mouseevent)[0]:
                        legend_label = text.get_text()
                        #print("Clicked on legend label:", legend_label)

            if self.SelectedSeries == legend_label:
                # Clear the selected series and remove the lines and text
                self.clearSelected_lines_and_text()
                self.SelectedSeries = None
            else:
                if self.ax.lines is not None:
                    self.clearSelected_lines_and_text()
                self.plotPercentualDif(legend_label)
                self.SelectedSeries = legend_label

            # Redraw the canvas to reflect the changes
            event.canvas.draw()

    def get_series_index(self, legend_label):
        for i, label in enumerate(self.series_labels):
            if label == legend_label:
                return i
        return -1  # Return -1 if the legend label is not found in the list of series labels
    
    def plotPercentualDif(self, legend_label):
        
        if legend_label != self.baseline_scenario:
            
            self.InteractiveElements[legend_label] = []
            
            for i, category in enumerate(self.categories):
                
                # Get the baseline scatter point values
                baseline_value = self.df.loc[self.df.index == self.baseline_scenario, category].astype(float).to_list()[0]
                
                # Get the values of the clicked series
                value = self.df.loc[self.df.index == legend_label, category].astype(float).to_list()[0]
                
                if baseline_value != 0:
                    percentage_change = (value - baseline_value) / baseline_value * 100
                else:
                    percentage_change = value * 100

                # Calculate the midpoint between the baseline scatter and the other scatter
                x_baseline = baseline_value
                x_other = value
                y = i
                x_midpoint = (x_baseline + x_other) / 2
                y_midpoint = y

                # Determine the line style and color based on the percentage change
                line_style = '-'
                line_color = 'green' if percentage_change > 0 else 'red'

                # Draw the line between the two points
                hline = self.ax.plot([x_baseline, x_other], [y, y], color=line_color, linewidth=1.5, linestyle=line_style, zorder=2)
                self.InteractiveElements[legend_label].append(hline)

                # Set the position of the text slightly above the midpoint
                text_x = x_midpoint
                text_y = y_midpoint +  0.05 * (len(self.categories) - 1 ) 

                # Add the text for the percentage change with "+" sign for positive values
                if percentage_change > 0:
                    text = self.ax.text(text_x, text_y, f'+{int(percentage_change)}%', ha='center', va='center', fontsize='x-small', weight='bold', color=line_color, zorder = 3)
                    self.InteractiveElements[legend_label].append(text)
                else:
                    text = self.ax.text(text_x, text_y, f'{int(percentage_change)}%', ha='center', va='center', fontsize='x-small', weight='bold', color=line_color, zorder = 3)
                    self.InteractiveElements[legend_label].append(text)

            # Set alpha and zorder for scatter points of non-selected scenarios
            for scatter in self.visible_scatters:
                    if scatter.get_label() != legend_label and scatter.get_label() != self.baseline_scenario:
                    #if scatter.get_label() != legend_label and scatter.get_label() in self.visible_labels and scatter.get_label() != self.baseline_scenario:
                        scatter.set_alpha(0.1)
                        scatter.set_zorder(0)
        else:
            for scatter in self.visible_scatters:
                if scatter.get_label() != legend_label:
                #if scatter.get_label() != legend_label and scatter.get_label() in self.visible_labels:
                    scatter.set_alpha(0.1)
                    scatter.set_zorder(0)           
                          
        for i, category in enumerate(self.categories):
            # Plot a vertical line for the selected scenario with respective average value
            values = self.df.loc[self.df.index == legend_label].iloc[0, :-1].astype(float).tolist()
            avg_value = sum(values) / len(values)
            #color = self.cmap(self.row_name_to_int[legend_label])  # Assign a color to each scenario
            
            self.ax.axvline(avg_value, color= self.df.at[self.df.index[i], "Color"], linestyle=':', linewidth = 0.66, alpha = 1, zorder = 0)
            self.ax.text(avg_value, 0.33, f"avg = {avg_value:.2f}", color='black', rotation = 90, ha='right', va='bottom', fontsize='small')
            
        # Redraw the canvas to reflect the changes
        self.ax.figure.canvas.draw()

    def clearSelected_lines_and_text(self):
        # Remove the lines and texts
        for line in self.ax.lines:
            if line not in self.LinesToKeep:
                line.remove()

        for text in self.ax.texts:
            text.remove()
            
        for scatter in self.visible_scatters:
            scatter.set_alpha(1)
            scatter.set_zorder(1)

        # Redraw the canvas to reflect the changes
        self.ax.figure.canvas.draw()   
        
    def clear_hlines_and_texts(self, data_series_name):
        
        for key, elements in self.InteractiveElements.items():
            if key == data_series_name:
                for element in elements:
                    element.remove()
                    
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    #TEST MultiBarGraphWidget
    widget = MultiHorizontalBarGraphWidget(categories = ['1', '2', '3'], values = [0.3, 0.5, 1], xmax = 1)
    widget.show()
    
    #TEST SingleBarGraphWidget
    widget = SingleHorizontalBarGraphWidget(value = 0.12 , xmax = 1)
    widget.show()
    
    #TEST ResilienceHorizontalBarGraphWidget
    categories = ['A', 'B', 'C']
    values = [0.3, 0.5, 1]
    df = pd.DataFrame(values, index=categories)
    widget = ResilienceHorizontalBarGraphWidget(df, xmax = 1)
    widget.show()
    
    #TEST CircularGraphWidget
    value = 0.65
    widget = CircularGraphWidget(value)
    widget.show()
    widget.animateWedge()  # Start the animation    

    #TEST ScatterPlotWidget
    data = {
        'ScenarioName': ['Atual', 'Futuro BAU', 'Futuro ST01'],
        'I1': [0.9, 0.7, 0.92],
        'I2': [0.92, 0.75, 0.98],
        'I3': [0.8, 0.75, 0.9]}

    df = pd.DataFrame(data)

    widget = ScatterPlotWidget(df, xmax=1)
    widget.show()
    
    
    sys.exit(app.exec())
