import pandas as pd
import seaborn as sns
import numpy as np
import sys
import os
import datetime
from typing import Dict
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.colorbar import ColorbarBase
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.integrate import trapezoid
from pyswmm import Output, Nodes, Links
from swmm.toolkit.shared_enum import NodeAttribute

from PySide6.QtWidgets import (QMainWindow, QApplication, QFileDialog, QMessageBox)
from PySide6.QtCore import Signal

from Tools.Performance_SWMM_tool._Old.SWMM_tool_GUI import Ui_MainWindow

class tool_GUI(QMainWindow):
    Proceed  = Signal()
    
    def __init__(self):
        """
        Initializes the MainWindow class.

        This function initializes the MainWindow class by calling the constructor of its superclass and setting up the user interface

        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("SWMM Performance Tool")

        self.ui.RPT_Search.clicked.connect(lambda: self.FindFile(type = "RPT"))
        self.ui.OUT_Search.clicked.connect(lambda: self.FindFile(type = "OUT"))
        self.ui.NodeList_Search.clicked.connect(lambda: self.FindFile(type = "NodeList"))
        
        self.ui.runButton.clicked.connect(self.verify_inputs)
        self.ui.closeButton.clicked.connect(self.close)
            
    def FindFile(self, type: str):
        """
        Finds a file based on the specified type.

        Args:
            type (str): The type of file to find. Valid values are "RPT", "OUT", and "NodeList".

        Returns:
            None
        """
        
        if type == "RPT":
            fileName, _ = QFileDialog.getOpenFileName(self, "Select RPT File", "", "(*.rpt)")       
            self.ui.RPT_Filepath.setText(fileName)
            
            #Get simulation start and end dates and set them in the GUI
            self.SimulationDates, self.RPT_TimeStep, self.AllowPonding = self.getSimulationOptions()
                    
            self.ui.StartingDate.setDateTime(self.SimulationDates[0])
            self.ui.StartingDate.setMinimumDateTime(self.SimulationDates[0])
            self.ui.StartingDate.setMaximumDateTime(self.SimulationDates[1])
            
            self.ui.EndDate.setDateTime(self.SimulationDates[1])            
            self.ui.EndDate.setMinimumDateTime(self.SimulationDates[0])
            self.ui.EndDate.setMaximumDateTime(self.SimulationDates[1])
            
        elif type == "OUT":
            fileName, _ = QFileDialog.getOpenFileName(self, "Select OUT File", "", "(*.out)")
            self.ui.OUT_Filepath.setText(fileName)
        
        elif type == "NodeList":
            fileName, _ = QFileDialog.getOpenFileName(self, "Select Node List File", "", "(*.txt)")     
            self.ui.NodeList_Filepath.setText(fileName)
    
    def getSimulationOptions(self):
        """
        Retrieves the simulation start and end dates from the given report file.

        Parameters:
        - None

        Returns:
        - A tuple containing the simulation start date and the simulation end date.
          The start and end dates are both instances of the datetime.datetime class.
        """
        
        ReportLines = getFileLines(self.ui.RPT_Filepath.text())

        for line in ReportLines:
            if "Starting Date" in line:
                SimulationStartDate = datetime.datetime.strptime(line.split(". ")[1].strip(), "%m/%d/%Y %H:%M:%S")
            elif "Ending Date" in line:
                SimulationEndDate = datetime.datetime.strptime(line.split(". ")[1].strip(), "%m/%d/%Y %H:%M:%S")
            elif "Report Time Step" in line:
                Report_TimeStep = datetime.datetime.strptime(line.split(". ")[1].strip(), "%H:%M:%S").time()
                break
            elif "Ponding Allowed" in line:
                Ponding = line.split(". ")[1]
                if Ponding == "YES":
                    AllowPonding = True
                else:
                    AllowPonding = False

        return (SimulationStartDate, SimulationEndDate), Report_TimeStep, AllowPonding
     
    def verify_inputs(self):
        self.RPT = self.ui.RPT_Filepath.text()
        self.OUT = self.ui.OUT_Filepath.text()
        self.StartingDate = datetime.datetime(self.ui.StartingDate.date().year(),
                                              self.ui.StartingDate.date().month(),
                                              self.ui.StartingDate.date().day(),
                                              self.ui.StartingDate.time().hour(),
                                              self.ui.StartingDate.time().minute(),
                                              self.ui.StartingDate.time().second())
                                               
        self.EndDate = datetime.datetime(self.ui.EndDate.date().year(),
                                         self.ui.EndDate.date().month(),
                                         self.ui.EndDate.date().day(),
                                         self.ui.EndDate.time().hour(),
                                         self.ui.EndDate.time().minute(),
                                         self.ui.EndDate.time().second())
        
        self.MinorThresh = self.ui.MinorThreshold.value()
        
        if self.RPT == "":
            QMessageBox.warning(self, "RPT Filepath", "RPT Filepath must be specified!")
            return False
        elif os.path.splitext(self.RPT)[1] != ".rpt":
            QMessageBox.warning(self, "RPT File extension", "RPT File extension must be *.rpt!")
            return False
        
        if self.OUT == "":
            QMessageBox.warning(self, "OUT Filepath", "OUT Filepath must be specified!")
            return False
        elif os.path.splitext(self.OUT)[1] != ".out":
            QMessageBox.warning(self, "OUT File extension", "OUT File extension must be *.out!")
            return False
        
        if self.ui.StartingDate == self.ui.EndDate:
            QMessageBox.warning(self, "Analysis period", "Analysis period must be greater than 0!")
            return False
    
        if self.ui.FloodVolume_checkbox.isChecked():
            self.UseFloodVolume = True
        else:
            self.UseFloodVolume = False
        
        if self.ui.NodeList_checkBox.isChecked():
            self.FilterNodes = True
            if self.ui.NodeList_Filepath.text() == "":
                #Show message saying "Node List Filepath must be specified!"
                QMessageBox.warning(self, "Node List Filepath", "Node List Filepath must be specified!")
                return False
        else:
            self.FilterNodes = False
            
        if self.ui.logBox.isChecked():
            self.PrintLog = True
        else:
            self.PrintLog = False        
        
        if self.ui.AllNodesPlot_checkBox.isChecked():
            self.PlotAllNodes = True
        else:
            self.PlotAllNodes = False
        
        if self.ui.WeightedSystemPlot_checkBox.isChecked():
            self.PlotWeightedPerformance = True
        else:
            self.PlotWeightedPerformance = False
            
        if self.ui.WeightNodesResilience_checkBox.isChecked():
            self.PlotWeightsResilience = True
        else:
            self.PlotWeightsResilience = False
        
        self.Proceed.emit()
    
    def closeEvent(self, event):
        self.close()

def getFileLines(FilePath):
    with open(FilePath, "r") as File:
        list = File.readlines()
    return list

def GetFromReport(RptFilePath, ReportSection):
    
    ReportLines = getFileLines(RptFilePath)
    
    if ReportSection == "Subcatchment Summary":
        pass
    elif ReportSection == "Node Summary":
        output = pd.DataFrame(columns = ["Type", "InvertElev", "MaxDepth", "PondedArea", "ExternalInflow"])
        LinesToData = 5
    elif ReportSection == "Link Summary":
        output = pd.DataFrame(columns = ["FromNode", "ToNode", "Type", "Length", "Slope", "Roughness"])
        LinesToData = 4
    elif ReportSection == "Cross Section Summary":
        output = pd.DataFrame(columns = ["Shape", "FullDepth", "FullArea", "HydRad", "MaxWidth", "NoBarrels", "FullFlow"])
        LinesToData = 5

    SectionFound = False
    SectionStart = 0
    
    for index, line in enumerate(ReportLines):      #iterate through report lines
        CleanLine = line.strip()    
        
        if SectionFound == False and CleanLine == ReportSection: #verifies if interest section is found
            SectionFound = True
            SectionStart = index + LinesToData
            
        elif SectionFound == True and index >= SectionStart:
            if CleanLine == '':         #end of the section
                break
            else:
                Data = CleanLine.split()
                if len(Data) == len(output.columns) + 1:        #verifies if data matches the lenght of the table
                    output.loc[Data[0]] = Data[1:]
                if len(Data) < len(output.columns) + 1:         #if not, ads Nan to empty fields
                    output.loc[Data[0]] = Data[1:] + [np.nan]*(len(output.columns) + 1 - len(Data))
    
    if ReportSection == "Subcatchment Summary":
        pass
    elif ReportSection == "Node Summary":
        output = output.astype({"Type": "string", "InvertElev": "float", "MaxDepth": "float" , "PondedArea": "float", "ExternalInflow": "string"})
    elif ReportSection == "Link Summary":
        output = output.astype({"FromNode": "string", "ToNode": "string", "Type": "string", "Length": "float", "Slope": "float", "Roughness": "float"})
    elif ReportSection == "Cross Section Summary":
        output = output.astype({"Shape": "string", "FullDepth": "float", "FullArea": "float", "HydRad": "float", "MaxWidth": "float", "NoBarrels": "int", "FullFlow": "float"})
    
    return output

def CalculateNodesPararameters(Nodes: pd.DataFrame,
                               Links: pd.DataFrame,
                               CrossSections: pd.DataFrame, 
                               AllowPonding: bool):

    #0. Get only nodes of JUNCTION Type
    NodesParameters = Nodes[Nodes["Type"] == "JUNCTION"].copy()
    
    #1. Iterate through each node
    for nodeID, _ in NodesParameters.iterrows():
        
        #1.1. Find all the links of type CONDUIT connected to the node
        ConnectedLinks = Links.query("(FromNode == @nodeID | ToNode == @nodeID) & Type == 'CONDUIT' ")

        #1.2. Find the link with the greatest FullFlow linked to the node and respective section maximum height
        MaxFullFlow = 0
        MaxFullDepth = 0
        LinkName = "ERRO"

        for linkID, linkProp in ConnectedLinks.iterrows():
            FullFlow = CrossSections.loc[linkID, "FullFlow"]
            if FullFlow > MaxFullFlow:
                LinkName = linkID
                MaxFullDepth = CrossSections.loc[linkID, "FullDepth"]
                MaxFullFlow = CrossSections.loc[linkID, "FullFlow"]
        
        #1.3. Verify if node has PondedArea
        if AllowPonding:
            if Nodes.at[nodeID, "PondedArea"] == 0:
                FloodingNode = False
            else:
                FloodingNode = True
        else:
            FloodingNode = True
        
        if LinkName == 'ERRO' or MaxFullFlow == 0 or MaxFullDepth == 0:
            # Remove node from NodesParameters
            NodesParameters = NodesParameters.drop(nodeID)
        else:
            # Assign attributes to the node
            NodesParameters.loc[nodeID, "LinkName"] = LinkName
            NodesParameters.loc[nodeID, "MaxFullDepth"] = MaxFullDepth
            NodesParameters.loc[nodeID, "MaxFullFlow"] = MaxFullFlow
            NodesParameters.loc[nodeID, "FloodingNode"] = FloodingNode
           
    #4. Calculate each node weight based on the respective linked MaxFullFlow -> W(i) = FullFlow(i) / (Soma(FullFlow(i:n))
    for nodeID, _ in NodesParameters.iterrows():
        NodesParameters.loc[nodeID, "Weight"] = NodesParameters.loc[nodeID, "MaxFullFlow"] / NodesParameters["MaxFullFlow"].sum()
    
    NodesParameters = NodesParameters[["LinkName", "MaxDepth", "MaxFullDepth", "MaxFullFlow", "Weight", "FloodingNode"]]
            
    return NodesParameters

def getNodesWithResults(Window: tool_GUI):
    # Get timeseries from OUT file
    with Output(Window.OUT) as out:
        NodesWithResults =  out.nodes.keys()
    
    return NodesWithResults    

def FilterAnalysisNodes(Nodes: pd.DataFrame, Window: tool_GUI):    
    if Window.FilterNodes:
    #Filter analysis nodes with the Node List File
        AnalysisNodes = getFileLines(Window.ui.NodeList_Filepath.text())
        AnalysisNodes = [node.strip() for node in AnalysisNodes]
        Nodes = Nodes[Nodes.index.isin(AnalysisNodes)]
    
    #Filter nodes with errors
    #1. For some reason node has no depth -> mistake in building INP / "lost node"
    Nodes = Nodes[Nodes["MaxDepth"] != 0]
    
    
    return Nodes

def getNodeResults(Nodes: pd.DataFrame, Window: tool_GUI):
    
    # Get timeseries from OUT file
    with Output(Window.OUT) as out:      
        times = out.times
        NodeResults = {"Depth": pd.DataFrame(index = times),
                       "InflowRate": pd.DataFrame(index = times),
                       "FloodingRate": pd.DataFrame(index = times)}
        
        for nodeID, _ in Nodes.iterrows():
            node_depths = pd.Series(out.node_series(nodeID, NodeAttribute.INVERT_DEPTH), name = nodeID)
            node_inflow = pd.Series(out.node_series(nodeID, NodeAttribute.TOTAL_INFLOW), name = nodeID)
            node_flooding = pd.Series(out.node_series(nodeID, NodeAttribute.FLOODING_LOSSES), name = nodeID)
            
            NodeResults["Depth"] = pd.concat([NodeResults["Depth"], node_depths], axis = 1)
            NodeResults["InflowRate"] = pd.concat([NodeResults["InflowRate"], node_inflow], axis = 1)
            NodeResults["FloodingRate"] = pd.concat([NodeResults["FloodingRate"], node_flooding], axis = 1)
            
    timestep = datetime.timedelta(hours = Window.RPT_TimeStep.hour,
                                  minutes = Window.RPT_TimeStep.minute,
                                  seconds = Window.RPT_TimeStep.second)   
   
    #Calculate start and end analysis timesteps based on analysis period given by user
    if Window.StartingDate == Window.SimulationDates[0]:
        start_date = Window.SimulationDates[0] + timestep   # SWMM does not report time 0, so firt time is start date + timestep
    else:
        start_date = Window.StartingDate
    if Window.EndDate == Window.SimulationDates[1]:
        end_date = Window.SimulationDates[1] - timestep     # SWMM does not report last time step, so last time is end date - timestep
    else:
        end_date = Window.EndDate
    
    # filter time series with start_date and end_date
    for result in NodeResults:
        NodeResults[result] = NodeResults[result][(NodeResults[result].index >= start_date) & (NodeResults[result].index <= end_date)]
            
    return NodeResults

def CalculateNodesResilience(Types: list,        #type of analysis: 'Surcharge' and 'Flooding'
                             Window: tool_GUI,
                             Nodes: pd.DataFrame,
                             NodesResults: Dict[str, pd.DataFrame],
                             NodesParameters: pd.DataFrame):
    
    AnalysisDuration = Window.EndDate - Window.StartingDate    
    
    xValues_Dates = NodesResults["Depth"].index
    xValues = (xValues_Dates - xValues_Dates[0]).total_seconds()  # Cumulative time in seconds, starting from zero
    
    # Normalize dates between 0 and 1:
    xNormValues = xValues / xValues.max()              
    
    resilience_raw_dataframe = pd.DataFrame(index = NodesParameters.index)
    performance_raw_dataframe = pd.DataFrame(index = xNormValues, columns = NodesParameters.index) 
    
    NodesResilience = {"Surcharge": resilience_raw_dataframe.copy(),
                       "Flooding": resilience_raw_dataframe.copy()}
    
    NodesPerformanceCurves = {"Surcharge": performance_raw_dataframe.copy(),
                              "Flooding": performance_raw_dataframe.copy()}
    
    for nodeID, nodeParameter in NodesParameters.iterrows(): # 1st loop by node is more efficient!
        nodeMaxDepth = Nodes.loc[nodeID, "MaxDepth"]      # Node depth (m)
        
        for Type in Types:
            if Type == "Surcharge":
                AD = nodeParameter["MaxFullDepth"]      #AD = Admissile Depth
                normalizer = nodeMaxDepth               #TO UPDATE LATER: Em rigor dever-se ia verificar se exist um offset e somar ao MaxFullDepth para coincidir com a verdadeira cota de coroa
            elif Type == "Flooding": 
                AD = nodeParameter["MaxDepth"]
                normalizer = nodeMaxDepth + Window.MinorThresh
                
            # Set Performance Curve: normalize depths between 0 and 1 by dividing by normalizer
            PerformanceNormalizedValues = (1 - NodesResults["Depth"][nodeID] / normalizer)      # Allow negative values (i.e. lower than PF = 0). Only clip afterwards when calculating the integral
            NodesPerformanceCurves[Type][nodeID] = PerformanceNormalizedValues.values
            
            PA = 1.0 - AD  / normalizer
            ResilienceZero = PA
            
            """if resiliencezero == 0 or np.isnan(resiliencezero) or np.isinf(resiliencezero):
                print(f"\nalert node resilience zero - {nodeid}")
                pass"""
            
            Threshold = 0.0001
            if Type == "Surcharge" and PA == 0:
                # if nodeMaxFullDepth(sewer) is equal to the respective surcharge depth(nodeMaxDepth)
                # # In that case, Resilience is "1D" and Resilience Loss is the proportion of time where values are equal or higher than the node MaxFullDepth-Threshold (a "safe" threshold is considered)
                ResilienceZero = 1
                # Calculate the proportion of time steps where the value is equal or lower than the threshold. -> surcharged node
                ResilienceLoss = (PerformanceNormalizedValues.values <= Threshold).sum() / len(PerformanceNormalizedValues.values)  
                """surcharges = (PerformanceNormalizedValues <= 0).any()         #verifies if node surcharges _OLD_
                if surcharges:
                    ResilienceLoss = (PerformanceNormalizedValues.values / normalizer <= 0.0001).sum() / len(PerformanceNormalizedValues.values)
                else:
                    ResilienceLoss = 0   """    
            else:                       
                if (Type == "Flooding" and Window.AllowPonding == False) or (Type == "Flooding" and Window.AllowPonding == True and nodeParameter["FloodingNode"] == False):
                    # if the node can't flood in SWMM
                    # # In that case, Resilience is "1D" and Resilience Loss is the proportion of time where values are equal or higher than the node MaxDepth-Threshold (a "safe" threshold is considered)
                    ResilienceZero = 1
                    # Calculate the proportion of time steps where the value is equal or lower than the threshold. -> flooded node
                    # Need to subtract MinorThresh/normalizer because the "real" AD is MaxDepth because the node can't flood in SWMM
                    ResilienceLoss = (PerformanceNormalizedValues.values - Window.MinorThresh / normalizer <= Threshold).sum() / len(PerformanceNormalizedValues.values)    # Calculate the proportion of time values are equal or lower than the threshold.
                    ResilienceLossNorm = ResilienceLoss
                else:               # "normal cases"
                    yModified = (PA - PerformanceNormalizedValues).clip(lower = 0.0, upper = PA)      # get values of Performance when they are <= than PA 
                    ResilienceLoss = trapezoid(yModified, xNormValues)                                # calculate integral between PA and P(t)
                    ResilienceLossNorm = ResilienceLoss / ResilienceZero                              # normalize between 0 and 1        
            
            Resilience = ResilienceZero - ResilienceLoss
            ResilienceNorm = Resilience / ResilienceZero
            
            NodesResilience[Type].at[nodeID, "PA"] = PA
            NodesResilience[Type].at[nodeID, "Resilience Loss"] = ResilienceLossNorm
            NodesResilience[Type].at[nodeID, "Resilience"] = ResilienceNorm
            
            if Type == "Flooding":
                # .index.to_series().diff().dt.total_seconds() calculates the time differences between consecutive timestamps in the Series index, converts them to seconds, and returns a new Series containing the time differences.
                inflow_volume = (NodesResults["InflowRate"][nodeID] * NodesResults["InflowRate"].index.to_series().diff().dt.total_seconds()).sum()
                flooding_volume = (NodesResults["FloodingRate"][nodeID] * NodesResults["FloodingRate"].index.to_series().diff().dt.total_seconds()).sum()
                if inflow_volume > 0:
                    Flooding_VolumeRatio = flooding_volume / inflow_volume
                else:
                    Flooding_VolumeRatio = 0
                NodesResilience[Type].at[nodeID, f"Flooding Ratio"] = Flooding_VolumeRatio
                
    return NodesResilience, NodesPerformanceCurves

def CalculateSystemResilience(Types: list,
                              Window: tool_GUI,                              
                              NodesParameters: pd.DataFrame,
                              NodesResilience: Dict[str, pd.DataFrame],
                              NodesPerformanceCurves: Dict[str, pd.DataFrame]):

    SystemResilience = {"Surcharge": {}, "Flooding": {}}
    SystemPerformanceCurves = {"Surcharge": {}, "Flooding": {}}
    
    #order all used dataframes by index to be sure that they are in the same order and scatters are correct
    NodesParameters = NodesParameters.sort_index()
    for dataframe in NodesResilience:
        NodesResilience[dataframe] = NodesResilience[dataframe].sort_index()
    for dataframe in NodesPerformanceCurves:
        NodesPerformanceCurves[dataframe] = NodesPerformanceCurves[dataframe].sort_index()    
    
    for Type in Types:
        #Calculate System Weighted Performance Curve
        weighted_performance = NodesPerformanceCurves[Type].mul(NodesParameters['Weight'], axis=1)    
        SystemPerformanceCurves[Type] = weighted_performance.sum(axis=1)
        
        if Type == "Flooding" and Window.UseFloodVolume:
            Resilience = ((NodesResilience[Type]["Resilience"] * (1-NodesResilience[Type]["Flooding Ratio"]))* NodesParameters["Weight"]).sum()
            
        else:
            Resilience = (NodesResilience[Type]["Resilience"] * NodesParameters["Weight"]).sum()
        ResilienceLoss = 1 - Resilience
        
        SystemResilience[Type]["Resilience"] = Resilience
        SystemResilience[Type]["Resilience Loss"] = ResilienceLoss
        
    return SystemResilience, SystemPerformanceCurves

def PlotNodesPerformance(Types: str,        #type of analysis: 'Surcharge' or 'Flooding'
                         Window: tool_GUI,
                         NodesParameters: pd.DataFrame,
                         NodesResilience: Dict[str, pd.DataFrame],
                         NodesPerformanceCurves: Dict[str, pd.DataFrame]):
    
    #PLOT SHEETS OF NODES PERFORMANCE
    num_plots = len(NodesParameters)
    num_columns = 8        #number of columns in one Figure
    num_rows = 10          #number of rows in one Figure
    plots_per_figure = num_columns * num_rows       #number of plots in one Figure
    num_figures = (num_plots - 1) // plots_per_figure + 1   #number of needed Figures
    
    #Order NodesParameters in descending order of Weight
    OrderedNodesParameters = NodesParameters.sort_values(by = "Weight", ascending = False)
    for Type in Types:        
        for figure_num in range(num_figures):
            fig, axes = plt.subplots(nrows = min(num_rows, max(1, num_plots // num_rows)),
                                    ncols = min(num_columns, num_plots - figure_num * plots_per_figure),
                                    sharex = True, 
                                    sharey = True,
                                    figsize=(11.69, 8.27))
            
            axes = axes.flatten()  # Flatten the NumPy array of axes
            
            start_index = figure_num * plots_per_figure
            end_index = min(num_plots, (figure_num + 1) * plots_per_figure)
            
            for i, (nodeID, nodeProp) in enumerate(OrderedNodesParameters.iloc[start_index:end_index].iterrows()):
                # plot_index = figure_num * plots_per_figure + i
                # if plot_index >= num_plots:
                #     break
                
                xValues = NodesPerformanceCurves[Type].index
                yValues = NodesPerformanceCurves[Type][nodeID].values
                
                PA = NodesResilience[Type].at[nodeID, "PA"]
                Loss = NodesResilience[Type].at[nodeID, "Resilience Loss"]
                Resilience = NodesResilience[Type].at[nodeID, "Resilience"]
                
                #Plot graph:
                axes[i].set_title(f'{nodeID} (w={nodeProp["Weight"]:.2e})', fontsize=7, fontdict={'fontsize': 4})
                axes[i].set_ylim(-0.1, 1.1)
                axes[i].set_xlim(-0.1, 1.1)
                
                axes[i].plot(xValues, yValues,                          
                        linewidth = 0.5,                    
                        color="black",                      
                        linestyle = "solid")
                        
                #Fill Resilience Loss
                axes[i].fill_between(xValues, np.maximum(yValues, 0), PA, where = yValues <= PA, color = 'lightsalmon', alpha = 0.6, interpolate = True)
                #fill values below PF (0)
                axes[i].fill_between(xValues, np.minimum(yValues, 0), 0, where=(yValues <= 0), color='red', alpha=0.6, interpolate=False)
                
                #Draw PA Line 
                axes[i].axhline(PA, color = 'orange', linewidth = 0.5)
                
                #Dray y = 0 and y = 1 Line
                axes[i].axhline(0, color = 'black', linewidth = 0.5, linestyle = "dashed")
                axes[i].axhline(1, color = 'black', linewidth = 0.5, linestyle = "dashed")
                            
                Resilience_text = f'R = {Resilience:.2f}'
                axes[i].annotate(Resilience_text, xy=(1.1, 1.1), xytext=(-1, -2), textcoords='offset points', fontsize=6, color='green', ha='right', va='top')
                
                ResilienceLoss_text = r'$R_L$' + f' = {Loss:.2f}'
                
                if Type == "Flooding" and Window.UseFloodVolume:
                    if NodesResilience[Type].at[nodeID, "Flooding Ratio"] > 0:
                        ResilienceLoss_text = ResilienceLoss_text + '\n' + r'$F_r$' + f' = {NodesResilience[Type].at[nodeID, "Flooding Ratio"]:.3f}'
                
                axes[i].annotate(ResilienceLoss_text, xy=(1.1, 0.0), xytext=(-1, 1), textcoords='offset points', fontsize=6, color='red', ha='right', va='bottom')
            
            fig.supxlabel("Time")
            fig.supylabel(f"Node {Type} Performance")

            fig.tight_layout()        
    plt.tight_layout()     
    plt.show()
            
def PlotSystemPerformance(Types: list,
                          NodesParameters: pd.DataFrame,
                          NodesPerformanceCurves: Dict[str, pd.DataFrame],
                          SystemResilience: dict[dict],
                          SystemPerformanceCurves: dict[dict]):
    
    #PLOT FIGURE OF SYSTEM AVERAGED PERFORMANCE  -> CAREFULL ANALYSIS!!!
    
    #order all used dataframes by index to be sure that they are in the same order and scatters are correct
    NodesParameters = NodesParameters.sort_index()
    for dataframe in NodesPerformanceCurves:
        NodesPerformanceCurves[dataframe] = NodesPerformanceCurves[dataframe].sort_index()
    
    
    fig, axes = plt.subplots(nrows = len(Types),
                             ncols = 1,
                             sharex = 'col')

    # axes = axes.flatten()  # Flatten the NumPy array of axes
    for i, Type in enumerate(Types):
        ax = axes[i]
        ax.set_xlabel(r'$Time_N$')
        ax.set_ylabel(f'{Type} Resilience')
                
        # Plot all nodes time series with colormap
        cmap = cm.Blues
        cmap_colors = cmap(np.arange(0.25, 1, 0.01))
        new_cmap = ListedColormap(cmap_colors)
        norm = Normalize(NodesParameters['Weight'].min(), NodesParameters['Weight'].max())
    
        for nodeID in NodesPerformanceCurves[Type].columns:
            color = new_cmap(norm(NodesParameters.at[nodeID, 'Weight']))
            ax.plot(NodesPerformanceCurves[Type][nodeID], color=color, label='_nolegend_', linewidth=0.25)
        
        # Plot System Weighted Performance
        ax.plot(SystemPerformanceCurves[Type], color='black', linewidth=2, label='System Weighted Performance')

        #Dray y = 0 Line
        ax.axhline(0, color = 'black', linewidth = 0.5, linestyle = "dashed")
        ax.axhline(1, color = 'black', linewidth = 0.5, linestyle = "dashed")

        # Set axis limits
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)

        fig.tight_layout()  
    
    plt.tight_layout()  
    plt.show()  
    
"""def PlotNodesWeightVsNodesResilience(Types: list, _ OLD
                                     NodesParameters: pd.DataFrame,
                                     NodesResilience: Dict[str, pd.DataFrame],
                                     SystemResilience: dict):
    #PLOT FIGURE OF NODES WEIGHT VS RESILIENCE 
    
    #order all used dataframes by index to be sure that they are in the same order and scatters are correct
    NodesParameters = NodesParameters.sort_index()
    for dataframe in NodesResilience:
        NodesResilience[dataframe] = NodesResilience[dataframe].sort_index()
    
    xmax = max(NodesParameters['Weight'])*(1.05)
    
    fig, axes = plt.subplots(ncols = len(Types),
                             nrows = 1,
                             sharex = False, 
                             sharey = True)
    
    axes = axes.flatten()  # Flatten the NumPy array of axes
    
    for i, Type in enumerate(Types):
        axes[i].scatter(NodesParameters['Weight'], NodesResilience[Type]['Resilience'], marker='x', s = 10, linewidths=0.5)
        axes[i].set_xlabel('Node Weight')
        axes[i].set_ylabel(f'Node {Type} Resilience')
        
        SR = SystemResilience[Type]["Resilience"]
        axes[i].axhline(SR, color = 'green', linewidth = 1)
        axes[i].annotate(f'R = {SR:.3f}', xy=(xmax, SR), xytext=(-1, -2), textcoords='offset points', fontsize=8, color='green', ha='right', va='top')
        axes[i].axhline(1, color = 'black', linewidth = 0.5, linestyle = "dashed")
        axes[i].axhline(0, color = 'black', linewidth = 0.5, linestyle = "dashed")
        # Set axis limits
        axes[i].set_xlim(0, xmax)
        axes[i].set_ylim(-0.1, 1.1)
    
    # Adjust layout
    fig.tight_layout()
    
    # Show the plot
    plt.tight_layout()
    plt.show()"""
   
def PlotNodesWeightVsNodesResilience(Types: list,
                               NodesParameters: pd.DataFrame,
                               NodesResilience: Dict[str, pd.DataFrame],
                               SystemResilience: dict):
 
    #order all used dataframes by index to be sure that they are in the same order and scatters are correct
    NodesParameters = NodesParameters.sort_index()
    for dataframe in NodesResilience:
        NodesResilience[dataframe] = NodesResilience[dataframe].sort_index()
    
    fig, axes = plt.subplots(ncols = len(Types),
                             nrows = 1,
                             sharex = False, 
                             sharey = True)
    
    axes = axes.flatten()  # Flatten the NumPy array of axes
    
    #xmax = max(NodesParameters['Weight'])*(1.05)
    
    node_weights = NodesParameters["Weight"]
 
    for i, Type in enumerate(Types):
        raw_node_resilience = NodesResilience[Type]["Resilience"]
        SR = SystemResilience[Type]["Resilience"]

        # Create a new figure for each JointGrid
        g = sns.JointGrid(x=node_weights, y=raw_node_resilience)

        # Plot a scatter plot in the center
        g.plot_joint(plt.scatter, color='blue', edgecolor='white', marker='x', s=10, linewidths=0.5)

        # Plot KDE plots in the margins
        g.plot_marginals(sns.kdeplot, color='blue', fill=True)
        
        # Retrieve the current x-axis limits
        xmin, xmax = g.ax_joint.get_xlim()

        # Add horizonta line at SR and value annotation        
        g.ax_joint.axhline(SR, color = 'green', linewidth = 1)
        g.ax_joint.annotate(f'R = {SR:.3f}', xy=(xmax, SR), xytext=(-1, -2), textcoords='offset points', fontsize=8, color='green', ha='right', va='top')
        
        #add axis labels
        g.ax_joint.set_xlabel('Node Weight')
        g.ax_joint.set_ylabel(f'Node {Type} Resilience')
        
        # Create a joint plot with hexbins
        #sns.jointplot(x=raw_node_resilience, y=node_weights, kind='hex', gridsize=20, cmap='Blues')

        # Alternatively, create a joint plot with a 2D density estimate
        #sns.jointplot(x=node_weights, y=raw_node_resilience, kind='kde', cmap='Blues')
        
    plt.tight_layout()
    plt.show()

    
    return
     
def main(Window: tool_GUI):
    
    # Indicators to calculate
    Types = ["Surcharge", "Flooding"]
       
    # Clear GUI
    Window.ui.textEdit.clear()   
    
    # Get nodes with output results (reported nodes in SWMM)
    NodesWithResults = getNodesWithResults(Window) 

    # Get data from RPT file -> all elements of the simulation
    Nodes = GetFromReport(Window.RPT, "Node Summary")
    Links = GetFromReport(Window.RPT, "Link Summary")
    CrossSections = GetFromReport(Window.RPT, "Cross Section Summary")
    
    # print(Nodes)
    # print(Links)
    # print(CrossSections)
    
    # Filter Nodes with NodesWithResults
    Nodes = Nodes[Nodes.index.isin(NodesWithResults)]
        
    # Filter Nodes with Input List and INP Errors
    Nodes = FilterAnalysisNodes(Nodes, Window)
    
    # Calculate nodes parameters 
    NodesParameters = CalculateNodesPararameters(Nodes, Links, CrossSections, Window.AllowPonding)
    
    # Get nodes results from out file
    NodesResults = getNodeResults(NodesParameters, Window)
    
    # Calculate nodes resilience and performance curves
    NodesResilience, NodesPerformanceCurves = CalculateNodesResilience(Types, Window, Nodes, NodesResults, NodesParameters)

    #Calculate system resilience and performance curves
    SystemResilience, SystemPerformanceCurves = CalculateSystemResilience(Types, Window, NodesParameters, NodesResilience, NodesPerformanceCurves)	

    # Print nodes resilience in terminal
    print(f'\n {NodesParameters}')
    print(f'\n {NodesResilience}')
    print(f'\n {SystemResilience}')

    # Print system resilience in GUI log
    GUI.ui.textEdit.append(f'Successfull run!')                    
    for Type in Types:
        GUI.ui.textEdit.append(f'Minor system {Type} Resilience = {SystemResilience[Type]["Resilience"]:.3f}')
    
    # Print system resilience in terminal
    print("\n")
    for Type in Types:
        print(f'*** Minor system {Type} Resilience = {SystemResilience[Type]["Resilience"]:.3f} **')
    print("\n")

    plotNodesResilienceViolins(Types, NodesParameters, NodesResilience, SystemResilience)

    if Window.PlotAllNodes:
        # Plot nodes resilience performance curves
        PlotNodesPerformance(Types, Window, NodesParameters, NodesResilience, NodesPerformanceCurves)
    if Window.PlotWeightedPerformance:
        PlotSystemPerformance(Types, NodesParameters, NodesPerformanceCurves, SystemResilience, SystemPerformanceCurves)
    if Window.PlotWeightsResilience:
        PlotNodesWeightVsNodesResilience(Types, NodesParameters, NodesResilience, SystemResilience)
    
    return

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    GUI = tool_GUI()
    GUI.Proceed.connect(lambda: main(GUI))
    
    GUI.show()
        
    sys.exit(app.exec())
