import sys
import pandas as pd
from PySide6.QtGui import QAction, QMouseEvent
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QMenu, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.legend
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math

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
