from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsTextItem, QGraphicsScene, QGraphicsView
from PySide6.QtGui import QFont, QColor, Qt, QPainter
from PySide6.QtCharts import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent

class SingleBarGraphWidget(QWidget):
    def __init__(self, value, xmax):
        super().__init__()
        self.value = value
        self.xmax = xmax
        self.initUI()

    def initUI(self):
        # Create a chart and set the chart view
        self.chart = QChart()
    
        # Create a bar set
        bar_set = QBarSet("Value")
        bar_set.append([self.value])

        # Set the color of the bar series
        bar_set.setBrush(QColor("green"))

        # Create a series and add the bar set
        series = QHorizontalBarSeries()
        series.append(bar_set)

        # Add the series to the chart
        self.chart.addSeries(series)

        # Set y-axis categories label
        categories = ["Value"]
        # Create and set the y-axis
        axisY = QBarCategoryAxis()
        axisY.append(categories)
        self.chart.addAxis(axisY, Qt.AlignLeft)
        
        series.attachAxis(axisY)
        
        
        axisX = QValueAxis()
        self.chart.addAxis(axisX, Qt.AlignBottom)    
        series.attachAxis(axisX)
            
        # Set the range and tick intervals for the value axis
        axisX.setRange(0, self.xmax)
        axisX.setTickCount(5)
        axisX.setLabelsVisible(True)
        axisX.setLabelFormat("%.2f")
        axisX.setLabelsFont(QFont("Arial", 8))        
        
        # Set the background color and transparency
        self.chart.setBackgroundBrush(QColor("AliceBlue"))
        self.chart.setBackgroundRoundness(0)

        # Set the chart as the scene for the QGraphicsView
        self.chart_view = CustomChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setSceneRect(self.chart.rect())

        
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

class CustomChartView(QChartView):
    def __init__(self, chart):
        super().__init__(chart)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event: QMouseEvent):
        # Get the position of the mouse cursor
        pos = event.pos()

        # Map the position to the chart view coordinate system
        chart_pos = self.chart().mapFromScene(self.mapToScene(pos))

        # Get the chart elements at the mouse position
        elements = self.items(chart_pos)

        # Check if any of the items are QBarSet
        for element in elements:
            if isinstance(element, QBarSet):
                # Get the value of the bar at the current index
                index = element.indexOf(chart_pos.x())
                if index >= 0:
                    bar_value = element.at(index)
                    bar_rect = element.barRect(index)

                    # Check if the mouse is inside the bar's rectangle
                    if bar_rect.contains(chart_pos):
                        # Show tooltip label
                        self.tooltip.setPlainText(f"Value: {bar_value}")
                        tooltip_pos = self.mapToScene(bar_rect.center())
                        tooltip_rect = self.tooltip.boundingRect()
                        tooltip_pos.setX(tooltip_pos.x() - tooltip_rect.width() / 2)
                        tooltip_pos.setY(tooltip_pos.y() - tooltip_rect.height())
                        self.tooltip.setPos(tooltip_pos)
                        self.tooltip.setVisible(True)
                        return

                    
        # If the mouse is not over any bar, hide the tooltip
        self.tooltip.setVisible(False)

        # Call the base class implementation
        super().mouseMoveEvent(event)
        
    # def resizeEvent(self, event):
    #     # Resize the tooltip scene to match the size of the chart view
    #     self.tooltip_scene.setSceneRect(self.chart().scene().sceneRect())


if __name__ == "__main__":
    app = QApplication([])
    widget = SingleBarGraphWidget(value=0.12, xmax=1)
    widget.show()
    app.exec()
