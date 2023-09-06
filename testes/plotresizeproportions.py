import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet

# Create the application
app = QApplication(sys.argv)

# Create the main window
window = QMainWindow()
window.setWindowTitle("Responsive Plot")

# Create the central widget
central_widget = QWidget(window)
window.setCentralWidget(central_widget)

# Create the layout
layout = QVBoxLayout(central_widget)

# Create the chart view
chart_view = QChartView()
layout.addWidget(chart_view)

# Create the chart and series
chart = QChart()
series = QBarSeries()

# Add data to the series
data = [(0, 10), (1, 20), (2, 15), (3, 25)]
for x, y in data:
    bar_set = QBarSet(str(x))
    bar_set.append(y)
    series.append(bar_set)

# Add the series to the chart
chart.addSeries(series)

# Set the chart title
chart.setTitle("Responsive Plot")

# Set the font size for the chart title
title_font = chart.titleFont()
title_font.setPointSize(title_font.pointSize() + 5)  # Increase the font size by 5 points
chart.setTitleFont(title_font)

# Set the font size for the axis labels
axis_font = chart.axisX().setLabelsFont()
axis_font.setPointSize(axis_font.pointSize() + 2)  # Increase the font size by 2 points
chart.axisX().setLabelFont(axis_font)

axis_font = chart.axisY().setLabelsFont()
axis_font.setPointSize(axis_font.pointSize() + 2)  # Increase the font size by 2 points
chart.axisY().setLabelFont(axis_font)

# Set the chart view to display the chart
chart_view.setChart(chart)

# Show the main window
window.show()

# Run the application
sys.exit(app.exec())
