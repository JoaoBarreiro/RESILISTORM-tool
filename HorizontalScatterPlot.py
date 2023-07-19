import sys
import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.legend
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math

class ScatterPlotWidget(QWidget):
    def __init__(self, dataframe=pd.DataFrame(), xmax=1):
        super().__init__()
        self.df = dataframe
        self.xmax = xmax
        self.initUI()

    def initUI(self):
        # Create a figure and axes
        self.fig = Figure(constrained_layout=True)
        self.ax = self.fig.add_subplot(111)


        self.ax.xaxis.set_tick_params(labelsize = "small")
        self.ax.yaxis.set_tick_params(labelsize = "small")

        # Set initial plot limits based on the data range
        min_value = self.df.iloc[:, 1:].astype(float).min().min()
        max_value = self.df.iloc[:, 1:].astype(float).max().max()
        self.ax.set_xlim(max(0, min_value - 0.1), min(1, max_value + 0.1))

        #self.ax.set_xlim(0, self.xmax)
        #self.ax.set_xticks(np.arange(0, 1.01, 0.25))
        #self.ax.set_xticklabels([f"{tick}" for tick in np.arange(0, 1.01, 0.25)])

        # Get the categories (indicators) from the DataFrame columns
        self.categories = self.df.columns[1:]

        # Set the number of y values
        self.ax.set_yticks(range(len(self.categories)))
        self.ax.set_yticklabels(self.categories, weight='bold')

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

        # Create a colormap with unique colors for each scenario name
        self.cmap = cm.get_cmap('tab10', len(self.df['ScenarioName']))
        self.unique_scenario_names = self.df['ScenarioName'].unique()
        self.scenario_name_to_int = {name: i for i, name in enumerate(self.unique_scenario_names)}

        self.legend_entries = list(self.unique_scenario_names)

        self.marker_size = 100  # Set the marker size here -> unit is area

        self.data_series_visibility = {}
        self.scatter_objects = []

        for i, category in enumerate(self.categories):
            values = self.df[category].tolist()  # Get the values for the category

            for j, value in enumerate(values):
                value = float(value)
                scenario_name = self.df['ScenarioName'][j]
                color = self.cmap(self.scenario_name_to_int[scenario_name])  # Assign a color to each scenario
                scatter = self.ax.scatter(value, i, marker='o', color=color, s=self.marker_size, label=scenario_name, alpha = 0, zorder = 1)
                self.scatter_objects.append(scatter)

        self.legend = None
        self.canvas = FigureCanvas(self.fig)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


        self.baseline_scenario = None
        # Add lists to store hlines and texts
        self.hlines = {}
        self.texts = {}

        # Initialize the text element for the value inside the bars
        self.text = None
        #self.legend.figure.canvas.mpl_connect('pick_event', self.on_legend_pick)

        # Connect the mouse motion event
        #self.canvas.mpl_connect('motion_notify_event', self.on_scatter_hover)

    def set_baseline_scenario(self, baseline_scenario):
        self.baseline_scenario = baseline_scenario

    def update_series_visibility(self, data_series_name, visible):

        for scatter in self.scatter_objects:
            if scatter.get_label() == data_series_name:
                scatter.set_alpha(1 if visible else 0)

        if visible and data_series_name not in self.data_series_visibility:
            self.data_series_visibility[data_series_name] = True

        # Check if the series should be hidden (visible=False) and remove the corresponding legend item
        if not visible and data_series_name in self.data_series_visibility:
            self.visible_labels.remove(data_series_name)
            if self.legend is not None:
                self.legend.remove()

        # Get the handles and labels for the visible entries
        visible_handles = []
        self.visible_labels = []
        for scatter in self.scatter_objects:
            if scatter.get_alpha() == 1 and scatter.get_label() not in self.visible_labels:  # Check if scatter is visible
                visible_handles.append(scatter)
                self.visible_labels.append(scatter.get_label())

        # Check if there are visible handles before creating the legend
        if visible_handles:
            self.legend = self.ax.legend(handles=visible_handles, labels=self.visible_labels, fontsize="x-small",
                                         loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(self.visible_labels),
                                         labelspacing = 0.2, handletextpad=0.1)
            self.legend.set_visible(True)  # Make sure the legend is visible
            self.legend.set_picker(True) # Enable picking on the legend
            self.legend.figure.canvas.mpl_connect('pick_event', self.on_legend_pick)

        self.legend.figure.canvas.mpl_connect('pick_event', self.on_legend_pick)
        self.SelectedSeries = None
        self.canvas.draw()


    def clear_hlines_and_texts(self, data_series_name=None):
        if data_series_name is None:
            # Clear all hlines and texts
            for hline in self.hlines.values():
                hline.remove()

            for text in self.texts.values():
                text.remove()

            self.hlines.clear()
            self.texts.clear()

        else:
            # Clear hlines and texts for a specific series
            if data_series_name in self.hlines:
                for hline in self.hlines[data_series_name]:
                    hline.remove()
                del self.hlines[data_series_name]

            if data_series_name in self.texts:
                for text in self.texts[data_series_name]:
                    text.remove()
                del self.texts[data_series_name]

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

                        if self.SelectedSeries == legend_label:
                            # Clear the selected series and remove the lines and text
                            self.remove_lines_and_text()
                            self.SelectedSeries = None
                        else:
                            if self.ax.lines is not None or self.ax.lines is not None:
                                self.remove_lines_and_text()
                            self.plotPercentualDif(legend_label)
                            self.SelectedSeries = legend_label

            if not legend_label:
                for text in legend_artist.get_texts():
                    if text.contains(event.mouseevent)[0]:
                        legend_label = text.get_text()
                        print("Clicked on legend label:", legend_label)
                        # Update the plot based on the clicked legend item


            # Redraw the canvas to reflect the changes
            event.canvas.draw()

    def get_series_index(self, legend_label):
        for i, label in enumerate(self.series_labels):
            if label == legend_label:
                return i
        return -1  # Return -1 if the legend label is not found in the list of series labels
    
    def plotPercentualDif(self, legend_label):
        
        if legend_label != self.baseline_scenario:
            for i, category in enumerate(self.categories):

                # Get the baseline scatter point values
                baseline_value = self.df.loc[self.df['ScenarioName'] == self.baseline_scenario, category].astype(float).to_list()[0]
                
                # Get the values of the clicked series
                value = self.df.loc[self.df['ScenarioName'] == legend_label, category].astype(float).to_list()[0]
                
                percentage_change = (value - baseline_value) / baseline_value * 100

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
                self.ax.plot([x_baseline, x_other], [y, y], color=line_color, linewidth=1.5, linestyle=line_style, zorder=0)

                # Set the position of the text slightly above the midpoint
                text_x = x_midpoint
                text_y = y_midpoint + 0.05

                # Add the text for the percentage change with "+" sign for positive values
                if percentage_change > 0:
                    self.ax.text(text_x, text_y, f'+{int(percentage_change)}%', ha='center', va='center', fontsize='x-small', weight='bold', color=line_color, zorder = 1)
                else:
                    self.ax.text(text_x, text_y, f'{int(percentage_change)}%', ha='center', va='center', fontsize='x-small', weight='bold', color=line_color, zorder = 1)

            # Set alpha and zorder for scatter points of non-selected scenarios
            for scatter in self.ax.collections:
                    if scatter.get_label() != legend_label and scatter.get_label() in self.visible_labels and scatter.get_label() != self.baseline_scenario:
                        scatter.set_alpha(0.3)
                        scatter.set_zorder(0)
        else:
            for scatter in self.ax.collections:
                if scatter.get_label() != legend_label and scatter.get_label() in self.visible_labels:
                    scatter.set_alpha(0.3)
                    scatter.set_zorder(0)           
                          
        for i, category in enumerate(self.categories):
            # Plot a vertical line for the selected scenario with respective average value
            values = self.df.loc[self.df['ScenarioName'] == legend_label].iloc[0, 1:].astype(float).tolist()
            avg_value = sum(values) / len(values)
            color = self.cmap(self.scenario_name_to_int[legend_label])  # Assign a color to each scenario
            
            self.ax.axvline(avg_value, color=color, linestyle='dashed', linewidth = 1, alpha = 1, zorder = 0)
            self.ax.text(avg_value, 0.5, f"avg = {avg_value:.2f}", color='black', rotation=90, ha='right', va='bottom', fontsize='small')
            
        # Redraw the canvas to reflect the changes
        self.ax.figure.canvas.draw()

    def remove_lines_and_text(self):
        # Remove the lines and text associated with the selected series
        for line in self.ax.lines:
          line.remove()

        for text in self.ax.texts:
            text.remove()
            
        for scatter in self.ax.collections:
            if scatter.get_label() in self.visible_labels:
                scatter.set_alpha(1)
                scatter.set_zorder(1)

        # Redraw the canvas to reflect the changes
        self.ax.figure.canvas.draw()   

def main():
    app = QApplication(sys.argv)

    data = {
        'ScenarioName': ['Atual', 'Futuro BAU', 'Futuro ST01'],
        'I1': [0.9, 0.7, 0.92],
        'I2': [0.92, 0.75, 0.98],
        'I3': [0.8, 0.75, 0.9]
    }

    df = pd.DataFrame(data)

    widget = ScatterPlotWidget(df, xmax=1)
    widget.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
