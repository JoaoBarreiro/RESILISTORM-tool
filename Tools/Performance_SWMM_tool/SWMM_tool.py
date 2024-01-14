import winsound
import pandas as pd
import numpy as np
import sys
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.integrate import trapezoid
from pyswmm import Output, Nodes, Links
from swmm.toolkit.shared_enum import NodeAttribute

from PySide6.QtWidgets import (QMainWindow, QApplication, QFileDialog, QMessageBox)
from PySide6.QtCore import Signal

from SWMM_tool_GUI import Ui_MainWindow

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

        if self.ui.logBox.isChecked():
            self.PrintLog = True
        else:
            self.PrintLog = False
        
        if self.ui.NodeList_checkBox.isChecked():
            self.FilterNodes = True
            if self.ui.NodeList_Filepath.text() == "":
                #Show message saying "Node List Filepath must be specified!"
                QMessageBox.warning(self, "Node List Filepath", "Node List Filepath must be specified!")
                return False
        else:
            self.FilterNodes = False
        
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
        
        #1.4. Assign attributes to the node
        NodesParameters.loc[nodeID, "LinkName"] = LinkName
        NodesParameters.loc[nodeID, "MaxFullDepth"] = MaxFullDepth
        NodesParameters.loc[nodeID, "MaxFullFlow"] = MaxFullFlow
        NodesParameters.loc[nodeID, "FloodingNode"] = FloodingNode
           
    #4. Calculate each node weight based on the respective linked MaxFullFlow -> W(i) = FullFlow(i) / (Soma(FullFlow(i:n))
    for nodeID, _ in NodesParameters.iterrows():
        NodesParameters.loc[nodeID, "Weight"] = NodesParameters.loc[nodeID, "MaxFullFlow"] / NodesParameters["MaxFullFlow"].sum()
    
    NodesParameters = NodesParameters[["LinkName", "MaxDepth", "MaxFullDepth", "MaxFullFlow", "Weight", "FloodingNode"]]

    #print(NodesParameters)
            
    return NodesParameters

def getNodesWithResults(Window: tool_GUI):
    # Get timeseries from OUT file
    with Output(Window.OUT) as out:
        NodesWithResults =  out.nodes.keys()
    
    return NodesWithResults    

def FilterAnalysisNodes(Nodes: pd.DataFrame, Window: tool_GUI):
    AnalysisNodes = getFileLines(Window.ui.NodeList_Filepath.text())
    
    AnalysisNodes = [node.strip() for node in AnalysisNodes]
    
    Nodes = Nodes[Nodes.index.isin(AnalysisNodes)]
    return Nodes

def getNodeResults(Nodes: pd.DataFrame, Window: tool_GUI):
    
    # Get timeseries from OUT file
    with Output(Window.OUT) as out:
        NodeResults = pd.DataFrame(index = out.times)
        
        for nodeID, _ in Nodes.iterrows():
            node_depths = pd.DataFrame.from_dict(out.node_series(nodeID, NodeAttribute.INVERT_DEPTH),
                                                 columns = [nodeID],
                                                 orient = "index")   #attr:`~INVERT_DEPTH`     water depth above invert    
            NodeResults = pd.concat([NodeResults, node_depths], axis = 1)
   
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
    NodeResults = NodeResults[(NodeResults.index >= start_date) & (NodeResults.index <= end_date)]
            
    return NodeResults

def CalculatePerformanceCurve(Type: str,        #type of analysis: 'Surcharge' or 'Flooding'
                              Window: tool_GUI,
                              Nodes: pd.DataFrame,
                              NodesResults: pd.DataFrame,
                              NodesParameters: pd.DataFrame):
    
    AnalysisDuration = Window.EndDate - Window.StartingDate    
    
    xValues_Dates = NodesResults.index
    xValues = (xValues_Dates - xValues_Dates[0]).total_seconds()  # Cumulative time in seconds, starting from zero
    
    # Normalize dates between 0 and 1:
    xNormValues = xValues / xValues.max()              
    
    PerformanceCurves = pd.DataFrame(index = xNormValues, columns = NodesParameters.index) 

    for nodeID, nodeParameter in NodesParameters.iterrows():
        nodeMaxDepth = Nodes.loc[nodeID, "MaxDepth"]      # Node depth (m)
        
        if Type == "Surcharge":
            AD = nodeParameter["MaxFullDepth"]      #AD = Admissile depth
            normalizer = nodeMaxDepth           #TO UPADTE LATER: Em rigor dever-se ia verificar se exist um offset e somar ao MaxFullDepth para coincidir com a verdadeira cota de coroa
        elif Type == "Flooding": 
            AD = nodeParameter["MaxDepth"]
            normalizer = nodeMaxDepth + Window.MinorThresh

        # Set Performance Curve: normalize depths between 0 and 1 by dividing by MaxDepth
        PerformanceNormalizedValues = (1 - NodesResults[nodeID] / normalizer)      # Allow negative values (i.e. lower than PF = 0) only clip afterwards when calculating the integral
        PerformanceCurves[nodeID] = PerformanceNormalizedValues.values
        
        PA = 1 - AD  / normalizer   
        ResilienceZero = PA
        ResilienceZeroNorm = ResilienceZero / ResilienceZero
        
        if Type == "Surcharge" and ResilienceZero == 0:     # if nodeMaxDepth is equal to the respective surcharge depth
            surcharges = (PerformanceNormalizedValues <= 0).any()   
            if surcharges:
                ResilienceLoss = ResilienceZero
            else:
                ResilienceLoss = 0
            ResilienceLossNorm = ResilienceLoss / ResilienceZero                              # normalize between 0 and 1
        else:                       
            if (Type == "Flooding" and Window.AllowPonding == False) or (Type == "Flooding" and Window.AllowPonding == True and nodeParameter["FloodingNode"] == False):
                ResilienceZero = 1
                ResilienceZeroNorm = 1
                # Calculate the proportion of time values are equal or lower than the threshold.
                # Need to subtract MinorThresh/normalizer because the "real" AD is MaxDepth because the node can't flood in SWMM
                ResilienceLoss = (PerformanceNormalizedValues.values - Window.MinorThresh / normalizer <= 0.0001).sum() / len(PerformanceNormalizedValues.values)    
                ResilienceLossNorm = ResilienceLoss
            else:               # "normal cases"
                yModified = (PA - PerformanceNormalizedValues).clip(lower = 0.0, upper = PA)      # get values of Performance when they are <= than PA 
                ResilienceLoss = trapezoid(yModified, xNormValues)                                # calculate integral between PA and P(t)
                ResilienceLossNorm = ResilienceLoss / ResilienceZero                              # normalize between 0 and 1        
        
        Resilience = ResilienceZero - ResilienceLoss
        ResilienceNorm = Resilience / ResilienceZero
        
        NodesParameters.at[nodeID, f"{Type} PA"] = PA
        NodesParameters.at[nodeID, f"{Type} Resilience Loss"] = ResilienceLossNorm
        NodesParameters.at[nodeID, f"{Type} Resilience"] = ResilienceNorm
    
    return NodesParameters, PerformanceCurves

def PlotResiliencePerformance(Type: str,        #type of analysis: 'Surcharge' or 'Flooding'
                              Window: tool_GUI,
                              NodesParameters: pd.DataFrame,
                              PerformanceCurve: pd.DataFrame):
    
    # Normalize dates between 0 and 1:
    num_plots = len(NodesParameters)
    
    num_columns = 8        #number of columns in one Figure
    num_rows = 10          #number of rows in one Figure
    plots_per_figure = num_columns * num_rows       #number of plots in one Figure
    num_figures = (num_plots - 1) // plots_per_figure + 1   #number of needed Figures
    

    for figure_num in range(num_figures):
        fig, axes = plt.subplots(nrows = min(num_rows, max(1, num_plots // num_rows)),
                                 ncols = min(num_columns, num_plots - figure_num * plots_per_figure),
                                 sharex = True, 
                                 sharey = True,
                                 figsize=(11.69, 8.27))
        
        fig.supxlabel("Time")
        fig.supylabel(f"Node {Type} Performance")
                
        for i, (nodeID, nodeProp) in enumerate(NodesParameters.iterrows()):
            plot_index = figure_num * plots_per_figure + i
            if plot_index >= num_plots:
                break
            
            xValues = PerformanceCurve.index
            yValues = PerformanceCurve[nodeID].values
            PA = NodesParameters.at[nodeID, f"{Type} PA"]
            Loss = NodesParameters.at[nodeID, f"{Type} Resilience Loss"]
                        
            #Plot graph:
            axes[i].set_title(nodeID, fontsize = 8)
            axes[i].set_ylim(-0.1, 1.1)
            axes[i].set_xlim(-0.1, 1.1)
            
            axes[i].plot(xValues, yValues,                          
                    linewidth = 0.5,                    
                    color="black",                      
                    linestyle = "solid")
                       
            #Fill Resilience Loss
            filled_poly = axes[i].fill_between(xValues, np.maximum(yValues, 0), PA, where = yValues <= PA, color = 'lightsalmon', alpha = 0.6, interpolate = True)
            
            axes[i].fill_between(xValues, np.minimum(yValues, 0), 0, where=(yValues < 0), color='red', alpha=0.6, interpolate=True)
            
            
            #Draw PA Line 
            axes[i].axhline(PA, color = 'orange', linewidth = 0.5)
            
            #Dray y = 0 Line
            axes[i].axhline(0, color = 'black', linewidth = 0.5, linestyle = "dashed")
            
            
            #Write the Resilience Loss value in the graph
            # if Loss > 0:
            #Get the coordinates of the filled_poly and assign text in the mid point
                #(x0, y0), (x1, y1) = filled_poly.get_paths()[0].get_extents().get_points()
            
            axes[i].annotate(f'R = {1-Loss:.2f}', xy=(1.1, 1.1), xytext=(-1, -1), textcoords='offset points', fontsize=6, color='green', ha='right', va='top')
            axes[i].annotate(r'$R_L$' + f' = {Loss:.2f}', xy=(1.1, -0.1), xytext=(-1, 1), textcoords='offset points', fontsize=6, color='red', ha='right', va='bottom')
        
        fig.supxlabel("Time")
        fig.supylabel(f"Node {Type} Performance")

        fig.tight_layout()        
        fig.show()

def main(Window: tool_GUI):
        
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
        
    # Filter Nodes with Node Analysis List, if necessary
    if Window.FilterNodes:
        Nodes = FilterAnalysisNodes(Nodes, Window)
    
    # Calculate nodes parameters 
    NodesParameters = CalculateNodesPararameters(Nodes, Links, CrossSections, Window.AllowPonding)
    
    # Get nodes results from out file
    NodesResults = getNodeResults(NodesParameters, Window)
    
    # Calculate resilience performance curves
    NodesParameters, SurchargePerforamnceCurves = CalculatePerformanceCurve("Surcharge", Window, Nodes, NodesResults, NodesParameters)
    NodesParameters, FloodingPerforamnceCurves = CalculatePerformanceCurve("Flooding", Window, Nodes, NodesResults, NodesParameters)
    
    # Plot resilience performance curves
    PlotResiliencePerformance("Surcharge", Window, NodesParameters, SurchargePerforamnceCurves)   
    PlotResiliencePerformance("Flooding", Window, NodesParameters, FloodingPerforamnceCurves)
     
    # Calculate system resilience
    SystemSurchargeResilience = (NodesParameters["Surcharge Resilience"] * NodesParameters["Weight"]).sum()
    SystemFloodResilience = (NodesParameters["Flooding Resilience"] * NodesParameters["Weight"]).sum()
    
    # Print nodes resilience in terminal
    print(NodesParameters[["Weight", "Surcharge Resilience Loss", "Surcharge Resilience", "Flooding Resilience Loss", "Flooding Resilience"]])
    
    # Print system resilience in GUI log
    GUI.ui.textEdit.append(f'Successfull run!')
    GUI.ui.textEdit.append(f'Minor system Surcharge Resilience = {SystemSurchargeResilience:.3f}')
    GUI.ui.textEdit.append(f'Minor system Flooding Resilience = {SystemFloodResilience:.3f}')
    
    # Print system resilience in terminal
    print("\n")
    print(f'********** Minor system Surcharge Resilience = {SystemSurchargeResilience:.3f} **********')
    print(f'********** Minor system Surcharge Resilience = {SystemFloodResilience:.3f} **************')
    print("\n")
    
    return

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    GUI = tool_GUI()
    GUI.Proceed.connect(lambda: main(GUI))
    
    GUI.show()
        
    sys.exit(app.exec())
