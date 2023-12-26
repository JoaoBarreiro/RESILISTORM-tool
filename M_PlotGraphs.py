import M_GraphClasses

import pandas as pd

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# def _OLD_plotSceariosResilience(DataFrame: pd.DataFrame, xScale: int, DestinyWidget: QWidget):

#     PerformanceResiliencePlot = M_GraphClasses.ResilienceHorizontalBarGraphWidget(DataFrame, xScale)

#     layout = DestinyWidget.layout()
    
#     if layout is None:
#         layout = QVBoxLayout()
#     else:
#         # Remove any existing widget in the DestinyWidget
#         while layout.count():
#             item = layout.takeAt(0)
#             widget = item.widget()
#             if widget is not None:
#                 widget.setParent(None)

#     layout.addWidget(PerformanceResiliencePlot)
#     layout.setContentsMargins(0, 0, 0, 0)
#     layout.setSpacing(0)
#     DestinyWidget.setLayout(layout)

#     return PerformanceResiliencePlot

# def _OLD_plotHorizontalBars(DataFrame: pd.DataFrame, labelColumn: str, dataColumn: str, xScale: int, DestinyWidget: QWidget, MultiBar: bool, yPrefix: str = "Crit. "):
#     #int = 100 ou 1
    
#     layout = DestinyWidget.layout()
#     if layout is not None:
#         # Remove all widgets from the layout
#         while layout.count():
#             item = layout.takeAt(0)
#             widget = item.widget()
#             if widget is not None:
#                 widget.setParent(None)
#                 widget.deleteLater()
#     else:
#         layout = QVBoxLayout()
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#     DestinyWidget.setLayout(layout)

#     if xScale == 100:
#         Values = round(DataFrame[dataColumn], 0).astype(int).tolist()
#     elif xScale == 1:
#         Values = round(DataFrame[dataColumn].astype(float), 2).tolist()
    
#     if not MultiBar:
#         for index, row in DataFrame.iterrows():
#             label = QLabel(f"{DataFrame.at[index, labelColumn]}")
#             label.setAlignment(Qt.AlignCenter)
#             label.setFont(QFont("Segoe UI", weight=QFont.Bold))
#             label.setStyleSheet("QLabel { padding-top: 5px; }")
#             layout.addWidget(label)
            
#             layout.addWidget(M_GraphClasses.SingleHorizontalBarGraphWidget(Values[index], xScale))
#     else:            
#         Categories = DataFrame.iloc[:, 0].tolist()
#         Categories = [yPrefix + element for element in Categories]
#         MultiBarPlot = M_GraphClasses.MultiHorizontalBarGraphWidget(Categories, Values, xScale)
#         layout.addWidget(MultiBarPlot)
        
def plotHorizontalFunctionalBars(DataFrame: pd.DataFrame,
                        labelColumn: str,
                        DestinyWidget: QWidget,
                        Type: str,
                        yPrefix: str = "Crit. "):
    #int = 100 ou 1
    
    layout = DestinyWidget.layout()
    if layout is not None:
        # Remove all widgets from the layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
    else:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    DestinyWidget.setLayout(layout)
    
    if DataFrame is not None:
        for index, row in DataFrame.iterrows():
            label = QLabel(f"{DataFrame.at[index, labelColumn]}")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Segoe UI", weight=QFont.Bold))
            label.setStyleSheet("QLabel { padding-top: 5px; }")
            layout.addWidget(label)
            if Type == "Completness":
                xScale = 100
                layout.addWidget(M_GraphClasses.SingleHorizontalBarGraph(
                    data = row[["Completness", "Missing"]],
                    colors = ["","#808080"],
                    xmax = xScale))
            elif Type == "Rating":
                xScale = 1
                layout.addWidget(M_GraphClasses.SingleHorizontalBarGraph(
                    data = row[["Rating", "Space", "Missing"]],
                    colors = ["","#D6DBDF", "#808080"],
                    xmax = xScale))
        

def plotResilienceCircle(DataFrame, DestinyWidget: QWidget):

    layout = DestinyWidget.layout()

    if layout is None:
        layout = QVBoxLayout()
        DestinyWidget.setLayout(layout)
    else:
        if layout.itemAt(0):
            layout.itemAt(0).widget().deleteLater()
                
    if DataFrame != 0:
        if isinstance(DataFrame, pd.DataFrame):
            Res_plotter = M_GraphClasses.CircularGraphWidget(
                data = DataFrame.loc['1', ["Rating", "Space","Missing"]],
                colors = ["", "#D6DBDF", "#808080"])
        else:
            data = pd.DataFrame(index = ['2'], columns = ["Rating", "Space"])
            data.at["2", "Rating"] = DataFrame
            data.at["2", "Space"]  = 1 - DataFrame
            Res_plotter = M_GraphClasses.CircularGraphWidget(
                data = data.loc['2', ["Rating", "Space"]],
                colors = ["", "#D6DBDF"])
            
        Res_plotter.animateWedge()

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(Res_plotter)
    
def plotPerformances(DataFrame: pd.DataFrame, Legend: pd.DataFrame, DestinyWidget: QWidget):
    
    layout = DestinyWidget.layout()
    if layout is None:
        layout = QVBoxLayout()
    else:
        # Remove any existing widget in the DestinyWidget
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:  
                    widget.setParent(None)   
                    
    if DataFrame is not None:
        if len(DataFrame.index) > 1:
            PerformancePlot = M_GraphClasses.ScatterPerformancePlotWidget(DataFrame, Legend)
        elif len(DataFrame.index) == 1:
            PerformancePlot = M_GraphClasses.BarPerformancePlotWidget(DataFrame, Legend)

        layout.addWidget(PerformancePlot)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        DestinyWidget.setLayout(layout)