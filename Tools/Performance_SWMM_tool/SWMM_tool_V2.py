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
from matplotlib.collections import PathCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.integrate import trapezoid
from pyswmm import Output, Nodes, Links
from swmm.toolkit.shared_enum import NodeAttribute

from PySide6.QtWidgets import (QStyledItemDelegate, QWidget, QHBoxLayout, QLineEdit, QMainWindow, QApplication, QFileDialog, QMessageBox, QPushButton, QTableWidgetItem)
from PySide6.QtCore import Qt, Signal

from SWMM_tool_GUI_V2 import Ui_MainWindow


class FileDialogDelegate(QStyledItemDelegate):
    simulationReportData= Signal(object, datetime.time, bool)
    
    def __init__(self, parent=None, fileType='RPT'):
        super().__init__(parent)
        self.fileType = fileType

    def createEditor(self, parent, option, index):
        
        # Create a widget to hold the line edit and button
        editor = QWidget(parent)
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create the line edit
        self.lineEdit = QLineEdit(editor)
        layout.addWidget(self.lineEdit)

        # Create the browse button
        self.button = QPushButton("...", editor)
        self.button.clicked.connect(lambda: self.openFileDialog(index.row()))
        layout.addWidget(self.button)

        editor.setLayout(layout)
        return editor

    def setEditorData(self, editor, index):
        # Set the editor data from the model item
        value = index.model().data(index, Qt.EditRole)
        self.lineEdit.setText(value)

    def setModelData(self, editor, model, index):
        # Set the model data from the editor
        model.setData(index, self.lineEdit.text(), Qt.EditRole)

    def openFileDialog(self, rowPosition:int):
        if self.fileType == "RPT":
            fileName, _ = QFileDialog.getOpenFileName(None, "Select RPT File", "", "RPT Files (*.rpt)")
            self.lineEdit.setText(fileName)
            self.lineEdit.setCompleter(None)

            if rowPosition == 0:
                #Get simulation start and end dates and set them in the GUI
                SimulationDates, RPT_TimeStep, AllowPonding = self.getSimulationOptions()
                
                self.simulationReportData.emit(SimulationDates, RPT_TimeStep, AllowPonding)
                
        elif self.fileType == "OUT":
            fileName, _ = QFileDialog.getOpenFileName(None, "Select OUT File", "", "(*.out)")
            self.lineEdit.setText(fileName)
            #make a tab to exit the line edit
            self.lineEdit.setCompleter(None)
        
    def getSimulationOptions(self):
        """
        Retrieves the simulation start and end dates from the given report file.

        Parameters:
        - None

        Returns:
        - A tuple containing the simulation start date and the simulation end date.
          The start and end dates are both instances of the datetime.datetime class.
        """
        
        ReportLines = getFileLines(self.lineEdit.text())

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

        # Create delegate instances for RPT and OUT columns and connect signals
        rptDelegate = FileDialogDelegate(self.ui.Input_table, fileType='RPT')
        outDelegate = FileDialogDelegate(self.ui.Input_table, fileType='OUT')
        
        self.ui.Input_table.setItemDelegateForColumn(1, rptDelegate)
        self.ui.Input_table.setItemDelegateForColumn(2, outDelegate)
        
        # Connect the delegate's signal to the slot method in the tool_GUI class
        rptDelegate.simulationReportData.connect(self.getDatesfromRPT)
        
        # Connect buttons for adding and deleting rows
        self.ui.addRow_button.clicked.connect(self.addRow)
        self.ui.delRow_button.clicked.connect(self.delRow)
        
        self.ui.NodeList_Search.clicked.connect(lambda: self.FindFile(type = "NodeList"))
        
        self.ui.runButton.clicked.connect(self.verify_inputs)
        self.ui.closeButton.clicked.connect(self.close)
    
    def addRow(self):
        rowPosition = self.ui.Input_table.rowCount()
        self.ui.Input_table.insertRow(rowPosition)      

        # # Create a button for the RPT File column
        # RPT_button = QPushButton('...')
        # RPT_button.clicked.connect(lambda: self.GetFile('RPT', rowPosition))
        # self.ui.Input_table.setCellWidget(rowPosition, 1, RPT_button)  # Assuming column 1 is for RPT File
        
        # OUT_button = QPushButton('...')
        # OUT_button.clicked.connect(lambda: self.GetFile('OUT', rowPosition))
        # self.ui.Input_table.setCellWidget(rowPosition, 2, OUT_button)  # Assuming column 1 is for RPT File
                
    def delRow(self):
        #Remove selected row from self.ui.Input_table
        self.ui.Input_table.removeRow(self.ui.Input_table.currentRow())            
    
    def getDatesfromRPT(self,SimulationDates, RPT_TimeStep, AllowPonding):
        self.SimulationDates = SimulationDates
        self.RPT_TimeStep = RPT_TimeStep
        self.AllowPonding = AllowPonding 
            
        self.ui.StartingDate.setDateTime(self.SimulationDates[0])
        # self.ui.StartingDate.setMinimumDateTime(self.SimulationDates[0])
        # self.ui.StartingDate.setMaximumDateTime(self.SimulationDates[1])
        
        self.ui.EndDate.setDateTime(self.SimulationDates[1])            
        # self.ui.EndDate.setMinimumDateTime(self.SimulationDates[0])
        # self.ui.EndDate.setMaximumDateTime(self.SimulationDates[1])
    
    def FindFile(self, type: str) :
        """
        Finds a file based on the specified type.

        Args:
            type (str): The type of file to find. Valid values are "RPT", "OUT", and "NodeList".

        Returns:
            None
        """
        
        if type == "NodeList":
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
        
        ReportLines = getFileLines(self.ui.Input_table.item(0, 1).text())

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
        self.Situations = {}
    
        rowCount = self.ui.Input_table.rowCount()

        for row in range(rowCount):
            if self.ui.Input_table.item(row, 0).text() == "":
                QMessageBox.warning(self, "ID label missing!", "ID label missing...")
                return False
            else:
                ID_label = self.ui.Input_table.item(row, 0).text()
                self.Situations[ID_label] = {}
                if self.ui.Input_table.item(row, 1).text() != "":
                    self.Situations[ID_label]["RPT"] = self.ui.Input_table.item(row, 1).text()
                else: 
                    QMessageBox.warning(self, "RPT Filepath", "RPT Filepath missing...")
                    return False
                if self.ui.Input_table.item(row, 2).text() != "":
                    self.Situations[ID_label]["OUT"] = self.ui.Input_table.item(row, 2).text()
                else:
                    QMessageBox.warning(self, "OUT Filepath", "OUT Filepath missing...")
                    return False
            
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
        output = output[output["Length"]!='PUMP']
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

def getNodesWithResults(OUT_File: str):
    # Get timeseries from OUT file
    with Output(OUT_File) as out:
        NodesWithResults =  out.nodes.keys()
    
    return NodesWithResults    

def FilterAnalysisNodes(Nodes: pd.DataFrame, Window: tool_GUI):    
    if Window.FilterNodes:
    #Filter analysis nodes with the Node List File
        AnalysisNodes = getFileLines(Window.ui.NodeList_Filepath.text())
        AnalysisNodes = [node.strip() for node in AnalysisNodes if not node.strip().startswith("!")]
        Nodes = Nodes[Nodes.index.isin(AnalysisNodes)]
    
    #Filter nodes with errors
    #1. For some reason node has no depth -> mistake in building INP / "lost node"
    Nodes = Nodes[Nodes["MaxDepth"] != 0]
    
    return Nodes

def getNodeResults(Nodes: pd.DataFrame, Window: tool_GUI, OUT_File: str):
    
    # Get timeseries from OUT file
    with Output(OUT_File) as out:      
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
                print(f"\n alert node resilience zero - {nodeid}")
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
                NodesResilience[Type].at[nodeID, f"ResilienceBeforeFlood"] = ResilienceNorm
                NodesResilience[Type].at[nodeID, f"Resilience"] = ResilienceNorm * (1 - Flooding_VolumeRatio)
                
                #get the nodes where Resilience is lower than 1, i.e, flooding nodes:
                BadNodes = NodesResilience[Type][NodesResilience[Type]["Resilience"] < 0.99990]

            NodesResilience[Type].at[nodeID, "Worst Performance"] = min((PerformanceNormalizedValues).clip(lower = 0, upper = 1).values)
                                     
    if len(BadNodes) > 0:
        print(BadNodes)
                  
    return NodesResilience, NodesPerformanceCurves

def CalculateSystemResilience(Types: list,
                              Window: tool_GUI,                              
                              NodesParameters: pd.DataFrame,
                              NodesResilience: Dict[str, pd.DataFrame],
                              NodesPerformanceCurves: Dict[str, pd.DataFrame]):

    SystemResilience = {}
    SystemPerformanceCurves = {}
    
    #order all used dataframes by index to be sure that they are in the same order and scatters are correct
    NodesParameters = NodesParameters.sort_index()
    for dataframe in NodesResilience:
        NodesResilience[dataframe] = NodesResilience[dataframe].sort_index()
    for dataframe in NodesPerformanceCurves:
        NodesPerformanceCurves[dataframe] = NodesPerformanceCurves[dataframe].sort_index()    
    
    for Type in Types:
        SystemResilience[Type] = {}
        #Calculate System Weighted Performance Curve
        weighted_performance = NodesPerformanceCurves[Type].mul(NodesParameters['Weight'], axis=1)    
        SystemPerformanceCurves[Type] = weighted_performance.sum(axis=1)
        
        # if Type == "Flooding" and Window.UseFloodVolume:
        #     Resilience = ((NodesResilience[Type]["Resilience"] * (1-NodesResilience[Type]["Flooding Ratio"])) * NodesParameters["Weight"]).sum()
            
        # else:
        Resilience = (NodesResilience[Type]["Resilience"] * NodesParameters["Weight"]).sum()
        ResilienceLoss = 1 - Resilience
        WorstPerforamnce = (NodesResilience[Type]["Worst Performance"] * NodesParameters["Weight"]).sum()
        
        SystemResilience[Type]["Resilience"] = Resilience
        SystemResilience[Type]["Resilience Loss"] = ResilienceLoss
        SystemResilience[Type]["Worst Performance"] = WorstPerforamnce
        
    return SystemResilience, SystemPerformanceCurves

def PlotNodesPerformance(Types: str,        #type of analysis: 'Surcharge' or 'Flooding'
                         Window: tool_GUI,
                         NodesParameters: pd.DataFrame,
                         NodesResilience: Dict[str, pd.DataFrame],
                         NodesPerformanceCurves: Dict[str, pd.DataFrame]):
    
    #PLOT SHEETS OF NODES PERFORMANCE
    num_plots = len(NodesParameters)
    num_columns = 5        #number of columns in one Figure
    num_rows = 10          #number of rows in one Figure
    plots_per_figure = num_columns * num_rows       #number of plots in one Figure
    num_figures = (num_plots - 1) // plots_per_figure + 1   #number of needed Figures
    
    #Order NodesParameters in descending order of Weight
    #OrderedOrderedNodesParameters = NodesParameters.sort_values(by = "Weight", ascending = False)

    # OrderedNodesResilience = NodesResilience[Type].sort_values(by = "Resilience Loss", ascending = False)
    # OrderedNodesResilience = OrderedNodesResilience.join(NodesParameters["Weight"])
    
    for Type in Types:
        OrderedNodesResilience = NodesResilience[Type].sort_values(by = "Resilience Loss", ascending = False)
        OrderedNodesResilience = OrderedNodesResilience.join(NodesParameters["Weight"])               
        
        for figure_num in range(num_figures):
            fig, axes = plt.subplots(nrows = min(num_rows, max(1, num_plots // num_rows)),
                                    ncols = min(num_columns, num_plots - figure_num * plots_per_figure),
                                    sharex = True, 
                                    sharey = True,
                                    figsize=(11.69, 8.27))
            
            axes = axes.flatten()  # Flatten the NumPy array of axes
            
            start_index = figure_num * plots_per_figure
            end_index = min(num_plots, (figure_num + 1) * plots_per_figure)
            
            for i, (nodeID, nodeProp) in enumerate(OrderedNodesResilience.iloc[start_index:end_index].iterrows()):
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
                        ResilienceLoss_text = ResilienceLoss_text + '\n' + r'$Flood_r$' + f' = {NodesResilience[Type].at[nodeID, "Flooding Ratio"]:.3f}'
                
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
    
        # for nodeID in NodesPerformanceCurves[Type].columns:
        #     color = new_cmap(norm(NodesParameters.at[nodeID, 'Weight']))
        #     ax.plot(NodesPerformanceCurves[Type][nodeID], color=color, label='_nolegend_', linewidth=0.25)
        
        # Plot System Weighted Performance
        
        min_performance_time = SystemPerformanceCurves[Type].idxmin()
        values_at_min_performance = NodesPerformanceCurves[Type].loc[min_performance_time]
        ax.plot(SystemPerformanceCurves[Type].index, SystemPerformanceCurves[Type], color='black', linewidth=2, label='System Weighted Performance')
        ax.scatter(min_performance_time,SystemPerformanceCurves[Type].min(), color='red', zorder=3)   
        
        boxplot_data = [values_at_min_performance.values.flatten()]  # Coloca os dados em uma lista como esperado pela função boxplot
        ax.boxplot(boxplot_data, positions=[min_performance_time], widths=0.05, patch_artist=True, boxprops=dict(facecolor='orange', alpha=0.5))

            
        #Dray y = 0 Line
        ax.axhline(0, color = 'black', linewidth = 0.5, linestyle = "dashed")
        ax.axhline(1, color = 'black', linewidth = 0.5, linestyle = "dashed")

        ax.tick_params(axis='x', width = 0.25, bottom=True, top=False, labelbottom=True)
        # Set axis limits
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)

        fig.tight_layout()  
    
    plt.tight_layout()  
    plt.show()  
     
def cm_to_inches(cm):
    return cm / 2.54  # Converte centímetros para polegadas
   
def PlotNodesWeightVsNodesResilience(Types: list,
                                     Situations: dict):
 
    for Type in Types:
        fig_width_cm = 10
        fig_height_cm = 10
        fig_size_inches = (cm_to_inches(fig_width_cm), cm_to_inches(fig_height_cm))
       
        
        # Initialize the JointGrid with dummy data to set up the grid
        g = sns.JointGrid(x=[0], y=[0], space = 0.1/2.5, height = cm_to_inches(fig_height_cm))

        # Define a color palette with enough colors for all your series
        palette = sns.color_palette("husl", len(Situations))

        for i, (ID, Results) in enumerate(Situations.items()):
            raw_node_resilience = Results["NodesResilience"][Type]["Resilience"]
            node_weights = Results["NodesParameters"]["Weight"]
            SR = Results["SystemResilience"][Type]["Resilience"]

            raw_node_resilience = raw_node_resilience.sort_index()
            node_weights = node_weights.sort_index()
                    
            # Use the color from the palette for this series
            color = palette[i]
    
            # Plot each scatter series on the joint plot area
            # g.ax_joint.scatter(node_weights, raw_node_resilience, label=f'{ID}', color=color, edgecolor='white', s=10, linewidths=0.5)
            g.ax_joint.scatter(node_weights, raw_node_resilience, label=f'{ID}', color=color, edgecolor='white', s=10, linewidths=0.5)
            
            g.ax_joint.axhline(SR, color=color, linewidth = 1, linestyle='--', label=f'$R_{{{ID}}}$ = {SR:.3f}')  
                  
            # Plot KDE for each series on the margins
            sns.kdeplot(x=node_weights, ax=g.ax_marg_x, color=color, fill=True, lw = 1.5)
            sns.kdeplot(y=raw_node_resilience, ax=g.ax_marg_y, color=color, fill=True, lw = 1.5, bw_adjust=2)       
            
        # Definindo os tamanhos dos rótulos dos ticks para 8 pontos
        for label in g.ax_joint.get_xticklabels():
            label.set_size(8)
        for label in g.ax_joint.get_yticklabels():
            label.set_size(8)
            
        #add axis labels
        g.ax_joint.set_xlabel('Node Weight', fontsize = 8, fontweight='bold')
        g.ax_joint.set_ylabel(f'Node {Type} Resilience', fontsize = 8, fontweight='bold')

        g.ax_joint.set_ylim(0, 1.10)  # Ajuste esses valores conforme necessário

        
        # Supondo que 'g' é seu JointGrid sns
        handles, labels = g.ax_joint.get_legend_handles_labels()

        # Filtra os handles para pontos e linhas
        scatter_handles = [h for h, l in zip(handles, labels) if isinstance(h, PathCollection)]
        line_handles = [h for h, l in zip(handles, labels) if isinstance(h, plt.Line2D)]

        # Faça o mesmo para os labels
        scatter_labels = [l for h, l in zip(handles, labels) if isinstance(h, PathCollection)]
        line_labels = [l for h, l in zip(handles, labels) if isinstance(h, plt.Line2D)]

        # Recria a ordem dos handles e labels para a legenda
        ordered_handles = scatter_handles + line_handles
        ordered_labels = scatter_labels + line_labels

        # Crie a legenda com os handles e labels ordenados
        g.ax_joint.legend(ordered_handles, ordered_labels, ncol=1, fontsize=8, loc='lower right')

        # Create a custom legend with the updated labels
        # g.ax_joint.legend(ncol = 2, fontsize = 8)
        
        g.fig.tight_layout()
        
        plt.show()
 
    return

"""def PlotNodesWorstPerformance(Types: list, Situations: dict): _ FORGET THIS FUNCTION_
    
    NodesWorstMoment = {}
    ConjugatedWorstPerformances = {}
 
    for Type in Types:   
        fig_width_cm = 10
        fig_height_cm = 10
        fig_size_inches = (cm_to_inches(fig_width_cm), cm_to_inches(fig_height_cm))
       
        # Initialize the JointGrid with dummy data to set up the grid
        g = sns.JointGrid(x=[0], y=[0], space = 0.1/2.5, height = cm_to_inches(fig_height_cm))

        # Define a color palette with enough colors for all your series
        palette = sns.color_palette("husl", len(Situations))
        
        NodesWorstMoment[Type] = {}
        ConjugatedWorstPerformances[Type] = {}
        
        for i, (ID, Results) in enumerate(Situations.items()):         
            min_value = Results["NodesPerformanceCurves"][Type].min()
            min_value_time = Results["NodesPerformanceCurves"][Type].idxmin()
            NodesWorstMoment[Type] = pd.DataFrame({
            "Worst Performance": min_value,
            "Worst Performance Time": min_value_time})        

            ConjugatedWorstPerformances[Type] = (NodesWorstMoment[Type]["Worst Performance"] * Results["NodesParameters"]["Weight"]).sum()       
                                
            # Use the color from the palette for this series
            color = palette[i]
    
            # Plot each scatter series on the joint plot area
            g.ax_joint.scatter(NodesWorstMoment[Type]["Worst Performance Time"],
                               NodesWorstMoment[Type]["Worst Perforamnce"], label = f'{ID}', color=color, edgecolor='white', s=10, linewidths=0.5)
            
            g.ax_joint.axhline(ConjugatedWorstPerformances[Type], color=color, linewidth = 1, linestyle='--', label=f'${ID}$ = {ConjugatedWorstPerformances[Type]:.3f}')  
                  
            # Plot KDE for each series on the margins
            sns.kdeplot(x=NodesWorstMoment[Type]["Worst Performance Time"], ax=g.ax_marg_x, color=color, fill=True, lw = 1.5)
            sns.kdeplot(y=NodesWorstMoment[Type]["Worst Perforamnce"], ax=g.ax_marg_y, color=color, fill=True, lw = 1.5, bw_adjust=2)       
            
        # Definindo os tamanhos dos rótulos dos ticks para 8 pontos
        for label in g.ax_joint.get_xticklabels():
            label.set_size(8)
        for label in g.ax_joint.get_yticklabels():
            label.set_size(8)
            
        #add axis labels
        g.ax_joint.set_xlabel('Time', fontsize = 8, fontweight='bold')
        g.ax_joint.set_ylabel(f'Node worst {Type} Resilience', fontsize = 8, fontweight='bold')

        g.ax_joint.set_ylim(0, 1.10)  # Ajuste esses valores conforme necessário

        
        # Supondo que 'g' é seu JointGrid sns
        handles, labels = g.ax_joint.get_legend_handles_labels()

        # Filtra os handles para pontos e linhas
        scatter_handles = [h for h, l in zip(handles, labels) if isinstance(h, PathCollection)]
        line_handles = [h for h, l in zip(handles, labels) if isinstance(h, plt.Line2D)]

        # Faça o mesmo para os labels
        scatter_labels = [l for h, l in zip(handles, labels) if isinstance(h, PathCollection)]
        line_labels = [l for h, l in zip(handles, labels) if isinstance(h, plt.Line2D)]

        # Recria a ordem dos handles e labels para a legenda
        ordered_handles = scatter_handles + line_handles
        ordered_labels = scatter_labels + line_labels

        # Crie a legenda com os handles e labels ordenados
        g.ax_joint.legend(ordered_handles, ordered_labels, ncol=2, fontsize=8)

        # Create a custom legend with the updated labels
        # g.ax_joint.legend(ncol = 2, fontsize = 8)
        
        g.fig.tight_layout()
        
        plt.show()
 
    return

     """
def main(Window: tool_GUI):
    
    # Indicators to calculate
    Types = ["Surcharge", "Flooding"]
       
    # Clear GUI
    Window.ui.textEdit.clear()   
    
    Situation_Outputs = {}
    
    for ID, Files in Window.Situations.items():
        Situation_Outputs[ID] = {}
        
        # Get nodes with output results (reported nodes in SWMM)
        NodesWithResults = getNodesWithResults(Files["OUT"]) 

        # Get data from RPT file -> all elements of the simulation
        Nodes = GetFromReport(Files["RPT"], "Node Summary")
        Links = GetFromReport(Files["RPT"], "Link Summary")
        CrossSections = GetFromReport(Files["RPT"], "Cross Section Summary")
        
        # print(Nodes)
        # print(Links)
        # print(CrossSections)
        
        # Filter Nodes with NodesWithResults
        Nodes = Nodes[Nodes.index.isin(NodesWithResults)]
            
        # Filter Nodes with Input List and INP Errors
        Nodes = FilterAnalysisNodes(Nodes, Window)
        
        # Calculate nodes parameters 
        NodesParameters = CalculateNodesPararameters(Nodes, Links, CrossSections, Window.AllowPonding)
        Situation_Outputs[ID]["NodesParameters"] = NodesParameters
        
        # Get nodes results from out file
        NodesResults = getNodeResults(NodesParameters, Window, Files["OUT"])
        Situation_Outputs[ID]["NodesResults"] = NodesResults
    
        # Calculate nodes resilience and performance curves
        NodesResilience, NodesPerformanceCurves = CalculateNodesResilience(Types, Window, Nodes, NodesResults, NodesParameters)
        Situation_Outputs[ID]["NodesResilience"] = NodesResilience
        Situation_Outputs[ID]["NodesPerformanceCurves"] = NodesPerformanceCurves

        #Calculate system resilience and performance curves
        SystemResilience, SystemPerformanceCurves = CalculateSystemResilience(Types, Window, NodesParameters, NodesResilience, NodesPerformanceCurves)
        Situation_Outputs[ID]["SystemResilience"] = SystemResilience
        Situation_Outputs[ID]["SystemPerformanceCurves"] = SystemPerformanceCurves

        # Print nodes resilience in terminal - DEBUG
        # print(f'\n Situation {ID} debug outputs:')
        # print(f'\n {NodesParameters}')
        # print(f'\n {NodesResilience}')
        # print(f'\n {SystemResilience}')

        # Print system resilience in GUI log
        GUI.ui.textEdit.append(f'Successfull run for Situation {ID}!')                    
        for Type in Types:
            GUI.ui.textEdit.append(f'Minor system {Type} Resilience = {SystemResilience[Type]["Resilience"]:.3f}')
    
        # Print system resilience in terminal
        print("\n")
        print(f"*** Situation {ID} ***")
        for Type in Types:
            print(f'Minor system {Type} Resilience = {SystemResilience[Type]["Resilience"]:.3f}')
            print(f'Minor system {Type} WORST Performance = {SystemResilience[Type]["Worst Performance"]:.3f}')
        print("\n")

    if Window.PlotAllNodes:
        # Plot nodes resilience performance curves
        for ID, Files in Window.Situations.items():
            PlotNodesPerformance(Types = Types,
                                 Window = Window,
                                 NodesParameters = Situation_Outputs[ID]["NodesParameters"],
                                 NodesResilience = Situation_Outputs[ID]["NodesResilience"],
                                 NodesPerformanceCurves = Situation_Outputs[ID]["NodesPerformanceCurves"])
    if Window.PlotWeightedPerformance:
        for ID, Files in Window.Situations.items():
            PlotSystemPerformance(Types = Types,
                                  NodesParameters = Situation_Outputs[ID]["NodesParameters"],
                                  NodesPerformanceCurves = Situation_Outputs[ID]["NodesPerformanceCurves"],
                                  SystemResilience = Situation_Outputs[ID]["SystemResilience"],
                                  SystemPerformanceCurves = Situation_Outputs[ID]["SystemPerformanceCurves"])
    if Window.PlotWeightsResilience:
        PlotNodesWeightVsNodesResilience(Types = Types,
                                         Situations = Situation_Outputs)
    
    
    return

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    GUI = tool_GUI()
    GUI.Proceed.connect(lambda: main(GUI))
    
    GUI.show()
        
    sys.exit(app.exec())
