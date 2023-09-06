import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
import pandas as pd
from matplotlib.font_manager import FontProperties
import time
import numpy as np

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    categories = ['A', 'B', 'C']
    values = [0.3, 0.5, 1]
    df = pd.DataFrame(values, index=categories)
    widget = ResilienceBarGraphWidget(df, xmax = 1)
    widget.show()
    sys.exit(app.exec())
