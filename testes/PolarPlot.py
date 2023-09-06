import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QMenu, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.cm as cm

class PolarPlotWidget(QWidget):
    def __init__(self, dataframe: pd.DataFrame, xmax: int):
        super().__init__()
        self.df = dataframe
        self.xmax = xmax
        self.series_names = dataframe.index.tolist()
        self.num_series = len(self.series_names)
        self.series_values = dataframe.tolist()
        self.initUI()
        
    def initUI(self):
        angles = np.linspace(0, 2 * np.pi, self.num_series, endpoint=False)
        radii = np.array(self.series_values)

        fig = Figure(constrained_layout = False)
        ax = fig.add_subplot(111, projection='polar')

        # Set the background color with 50% transparency
        fig.patch.set_facecolor("AliceBlue")
        fig.patch.set_alpha(0)     

        # Set the radial axis of value 1 (maximum)
        ax.set_ylim(0, self.xmax)      
        
        # Set the custom radial tick values
        tick_values = [0.3, 0.55, 0.75, 0.9, 1]
        ax.yaxis.grid(color='gray', linestyle='-', alpha=0, linewidth=0.5, zorder=1)
        ax.set_yticks(tick_values)
        ax.set_yticklabels(())

        # Plot the radial grid lines and tick labels
        ax.xaxis.grid(color='gray', linestyle='-', alpha=1, linewidth=0.5, zorder=1)
        # Set the series axis and labels in between the bars
        ax.set_xticks(angles + (np.pi / self.num_series))
        ax.set_xticklabels([])

        # Create a colormap with unique colors for each row (scenario) name
        self.cmap = cm.get_cmap('tab10', len(self.series_names))
        self.unique_row_names = self.series_names
        self.row_name_to_int = {name: i for i, name in enumerate(self.unique_row_names)}

        # Create custom colors for filling the radial plot area
        resilience_colors = ['#D34C4C', '#DB944C', '#FFFF4C', '#76CA4C', 'green']
            
        # Fill the polar plot background with colored radial segments in reverse order
        for i in range(len(tick_values), 0, -1):
            theta = np.linspace(0, 2 * np.pi, 100)
            r = np.full_like(theta, tick_values[i-1])
            ax.fill(theta, r, color=resilience_colors[i-1], alpha=0.7, zorder = 0)
           
        # Plot the series as polar pie slices
        for i in range(self.num_series):
            width = radii[i] * 2 * np.pi / self.num_series
            scenario_name = self.series_names[i]
            color = self.cmap(self.row_name_to_int[scenario_name])  # Assign a color to each scenario
            ax.bar(angles[i], radii[i], width=width,
                color=color, alpha=1, edgecolor='black', linewidth=2, zorder=5, fill=True)
       
        # Create a legend with the colors and series names
        legend_labels = [plt.Rectangle((0, 0), 1, 1, color=color, alpha=1) for color in self.cmap.colors]
        series_legend = ax.legend(legend_labels, self.series_names, loc='lower center', bbox_to_anchor=(0.5, 1.1), ncol=self.num_series)
       
        # # Create a second legend for the colors used to fill the radial plot area
        # resilience_legend_fill = [plt.Rectangle((0, 0), 1, 1, color=color, alpha = 0.7) for color in resilience_colors]
        # legend_labels_texts = ['Bad', 'Insufficient', 'Acceptable', 'Good', 'Great']
        # ax.legend(resilience_legend_fill, legend_labels_texts, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)           

        #ax.add_artist(series_legend)
        
        self.canvas = FigureCanvas(fig)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    series_names = ['SerieA', 'SerieB', 'SerieC']
    series_values = [0.5, 0.75, 0.94]

    testedf = pd.DataFrame({'': series_values}, index=series_names)

    polar_plot = PolarPlotWidget(testedf, 1)
    polar_plot.show()
    sys.exit(app.exec())   
