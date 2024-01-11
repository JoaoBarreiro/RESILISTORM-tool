import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.integrate import trapezoid
from pyswmm import Output, Nodes, Links
from swmm.toolkit.shared_enum import NodeAttribute


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
        
        if SectionFound == False and CleanLine == (ReportSection): #verifies if interest section is found
            SectionFound = True
            SectionStart = index + LinesToData
            
        elif SectionFound == True and index >= SectionStart:
            if CleanLine == '':         #end of the section
                break
            else:
                Data = CleanLine.split()
                if len(Data) == len(output.columns) + 1:        #verifies if data matches the lenght od the table
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

def CalculateNodesResiliencePararameters(Nodes, Links, CrossSections, FloodAdmissibleDepth):

    #0. Get only nodes of JUNCTION Type
    NodesResilienceParameters = Nodes[Nodes["Type"] == "JUNCTION"].copy()
    
    #1. Iterate through each node
    for nodeID, nodeProp in NodesResilienceParameters.iterrows():
        NodeMaxDepth = NodesResilienceParameters.loc[nodeID, "MaxDepth"]
        
        #1.1. Find all the links of type CONDUIT connected to the node
        ConnectedLinks = Links.query("(FromNode == @nodeID | ToNode == @nodeID) & Type == 'CONDUIT' ")

        #1.2. Find the link with the greatest FullFlow linked to the node and respective section maximum height
        MaxFullFlow = 0
        LinkName = "ERRO"
        #MaxSection = 0
        #MaxFullDepth = 0

        for linkID, linkProp in ConnectedLinks.iterrows():
            
            FullFlow = CrossSections.loc[linkID, "FullFlow"]
            if FullFlow > MaxFullFlow:
                LinkName = linkID
                MaxFullDepth = CrossSections.loc[linkID, "FullDepth"]
                MaxFullFlow = CrossSections.loc[linkID, "FullFlow"]
                
        #1.3. Assign attributes to the node
        NodesResilienceParameters.loc[nodeID, "LinkName"] = LinkName
        NodesResilienceParameters.loc[nodeID, "MaxFullDepth"] = MaxFullDepth
        NodesResilienceParameters.loc[nodeID, "MaxFullFlow"] = MaxFullFlow
        NodesResilienceParameters.loc[nodeID, "SurchargePA"] = MaxFullDepth  / NodeMaxDepth             #TO UPADTE: Em rigor dever-se ia verificar se exist um offset e somar ao MaxFullDepth para coincidir com a verdadeira cota de coroa
        NodesResilienceParameters.loc[nodeID, "FloodPA"] = NodeMaxDepth  / (NodeMaxDepth + FloodAdmissibleDepth)
           
    #4. Calculate each node weight based on the respective linked MaxFullFlow -> W(i) = FullFlow(i) / (Soma(FullFlow(i:n))
    for nodeID, nodeProp in NodesResilienceParameters.iterrows():
        NodesResilienceParameters.loc[nodeID, "Weight"] = NodesResilienceParameters.loc[nodeID, "MaxFullFlow"] / NodesResilienceParameters["MaxFullFlow"].sum()
    
    NodesResilienceParameters = NodesResilienceParameters[["Weight", "MaxFullDepth", "MaxFullFlow", "SurchargePA", "FloodPA"]]
    
    #print(NodesResilienceParameters)
    
    #print(NodesResilienceParameters["Weight"].sum())
        
    return NodesResilienceParameters

def getNodeResults(Nodes, OutFilePath):
    
    #. Get only nodes of JUNCTION Type
    #Nodes = Nodes[Nodes["Type"] == "JUNCTION"].copy()
   
    with Output(OutFilePath) as out:
        NodeResults = pd.DataFrame(index = out.times)
        Data = {}
        for nodeID, nodeProp in Nodes.iterrows():
            node_depths = pd.DataFrame.from_dict(out.node_series(nodeID, NodeAttribute.INVERT_DEPTH, 0), columns = [nodeID], orient = "index")   #attr:`~INVERT_DEPTH`     water depth above invert    
            NodeResults = pd.concat([NodeResults, node_depths], axis = 1)

    return NodeResults


def CalculateNodesResiliencePerformance(Nodes, NodesResults, NodesResilienceParameters, FloodAdmissibleDepth):
    
    PlotCols = 8
    PlotRows = 10
    PlotFigure = PlotCols * PlotRows
    PlotTotal = len(NodesResilienceParameters)
    
    NrFigures = PlotTotal // PlotFigure
    
    if NrFigures == 0 or NrFigures % PlotTotal != 0:        #VERIFICAR SE NR DE FIGURAS BATE CERTO!
        NrFigures += 1 
              
    xValuesDates = NodesResults.index
    RainStartTime = xValuesDates[0]                             #TO UPDATE: Get from a file or user input
    AnalysisDuration = 4 * 2 * 3600                             #Define analysis duration to twice the rainfall duration, in seconds
    xValuesDates = xValuesDates[(xValuesDates >= RainStartTime) & (xValuesDates <= RainStartTime + datetime.timedelta(seconds=AnalysisDuration))]  #Clip time between the start of rainfal and analysis time. TO UPDATE: Make automatic
    
    xValues = (xValuesDates - xValuesDates[0]).total_seconds()  #Cumulative time in seconds, starting from zero
    xValues = xValues / xValues.max()                           #Normalize dates between 0 and 1
    
    Nodes = Nodes.query("Type == 'JUNCTION'").copy()
    
    
    # CALCULATE AND PLOT SURCHARGE RESILIENCE
    
    plotCounter = 0
    for k in range(1, NrFigures+1):
        fig = plt.figure(k, figsize=(11.69, 8.27))                  #A4 landscape size
        gs = fig.add_gridspec(nrows = PlotRows, ncols = PlotCols)
        axs = gs.subplots(sharex = True, sharey = True)

        axs[0,0].set_ylim(-0.1, 1.1)
        axs[0,0].set_xlim(-0.1, 1.1)
        #axs[0,0].invert_yaxis()
               
        for ax in axs.ravel():
            if plotCounter ==  PlotTotal: continue
            
            nodeID = Nodes.index[plotCounter]
                              
            MaxDepth = Nodes.loc[nodeID, "MaxDepth"]
            
            PA = 1 - NodesResilienceParameters.loc[nodeID, "SurchargePA"]
            
            #normalize depths between 0 and 1
            yValues = 1 - NodesResults[(NodesResults.index >= RainStartTime) & (NodesResults.index <= RainStartTime + datetime.timedelta(seconds=AnalysisDuration))][nodeID]/ MaxDepth #Clip time between the start of rainfal and analysis time.
            yValues = yValues.clip(lower = 0.0) #Define minimum possible value as zero (PF)

            #calculate integral between PA and Performance (normalized)
            yModified = (PA - yValues).clip(lower = 0.0)
            Integral = trapezoid(yModified, xValues)
            
            ResilienceZero = PA

            if ResilienceZero == 0:
                ResilienceZeroNorm = 1
                surcharges = (yValues == 0).any()
                
                if surcharges:
                    ResilienceLossNorm = 1
                else:
                    ResilienceLossNorm = 0
            else:
                Integral = trapezoid(yModified, xValues)
                
                ResilienceZeroNorm = ResilienceZero / ResilienceZero
                
                ResilienceLoss = Integral
                ResilienceLossNorm = ResilienceLoss / ResilienceZero
                
            Resilience = ResilienceZero - ResilienceLoss
            ResilienceNorm = Resilience / ResilienceZero
            
            NodesResilienceParameters.loc[nodeID, "Surcharge Resilience Zero"] = ResilienceZeroNorm
            NodesResilienceParameters.loc[nodeID, "Surcharge Resilience Loss"] = ResilienceLossNorm
            NodesResilienceParameters.loc[nodeID, "Surcharge Resilience"] = ResilienceNorm
               
            print(f'{nodeID}: \t\t\t Resilience Zero = {ResilienceZeroNorm:.2f}\t Resilience Loss = {ResilienceLossNorm:.2f}\t Resilience = {ResilienceNorm:.2f}')
            
            #Plot graph:
            ax.plot(xValues, yValues,                          
                    linewidth = 0.5,                    
                    color="black",                      
                    linestyle = "dashed")
            
            #Fill value between PA and PF=0
            filled_poly = ax.fill_between(xValues, yValues, PA, where=(yValues<=PA), color = 'lightsalmon', alpha = 0.6, interpolate = True)
            
            #Draw PA Line 
            ax.axhline(PA, color = 'orange', linewidth = 0.5)
            
            ax.set_title(nodeID, fontsize = 8)
            #ax.xaxis.set_major_locator(mdates.HourLocator(interval = 4))
            #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))  

            #Write the Resilience Loss value in the graph
            if Integral > 0:
                #Get the coordinates of the filled_poly and assign text in the mid point
                (x0, y0), (x1, y1) = filled_poly.get_paths()[0].get_extents().get_points()
                ax.text(x = (x0 + x1) / 2, y = y1 + 0.05, s = f'{ResilienceLossNorm:.2f}', fontsize = 6, color = 'red')

            plotCounter += 1
        
        fig.supxlabel("Time")
        fig.supylabel("Node Surcharge Performance")
        
        fig.tight_layout() 
        
    plt.show() 

    # CALCULATE AND PLOT FLOODING RESILIENCE
    
    plotCounter = 0
    for k in range(1, NrFigures+1):
        fig = plt.figure(k, figsize=(11.69, 8.27))                  #A4 landscape size
        gs = fig.add_gridspec(nrows = PlotRows, ncols = PlotCols)
        axs = gs.subplots(sharex = True, sharey = True)

        axs[0,0].set_ylim(-0.1, 1.1)
        axs[0,0].set_xlim(-0.1, 1.1)
        #axs[0,0].invert_yaxis()
               
        for ax in axs.ravel():
            if plotCounter ==  PlotTotal: continue
            
            nodeID = Nodes.index[plotCounter]
                              
            MaxDepth = Nodes.loc[nodeID, "MaxDepth"]
            
            PA = 1 - NodesResilienceParameters.loc[nodeID, "FloodPA"]
            
            #normalize depths between 0 and 1
            yValues = 1 - NodesResults[(NodesResults.index >= RainStartTime) & (NodesResults.index <= RainStartTime + datetime.timedelta(seconds=AnalysisDuration))][nodeID]/ (MaxDepth + FloodAdmissibleDepth) #Clip time between the start of rainfal and analysis time.
            yValues = yValues.clip(lower = 0.0) #Define minimum possible value as zero (PF)

            #calculate integral between PA and Performance (normalized)
            yModified = (PA - yValues).clip(lower = 0.0)
            Integral = trapezoid(yModified, xValues)
            
            ResilienceZero = PA

            if ResilienceZero == 0:
                ResilienceZeroNorm = 1
                surcharges = (yValues == 0).any()
                
                if surcharges:
                    ResilienceLossNorm = 1
                else:
                    ResilienceLossNorm = 0
            else:
                Integral = trapezoid(yModified, xValues)
                
                ResilienceZeroNorm = ResilienceZero / ResilienceZero
                
                ResilienceLoss = Integral
                ResilienceLossNorm = ResilienceLoss / ResilienceZero
                
            Resilience = ResilienceZero - ResilienceLoss
            ResilienceNorm = Resilience / ResilienceZero
            
            NodesResilienceParameters.loc[nodeID, "Flood Resilience Zero"] = ResilienceZeroNorm
            NodesResilienceParameters.loc[nodeID, "Flood Resilience Loss"] = ResilienceLossNorm
            NodesResilienceParameters.loc[nodeID, "Flood Resilience"] = ResilienceNorm
               
            print(f'{nodeID}: \t\t\t Resilience Zero = {ResilienceZeroNorm:.2f}\t Resilience Loss = {ResilienceLossNorm:.2f}\t Resilience = {ResilienceNorm:.2f}')
            
            #Plot graph:
            ax.plot(xValues, yValues,                          
                    linewidth = 0.5,                    
                    color="black",                      
                    linestyle = "dashed")
            
            #Fill value between PA and PF=0
            filled_poly = ax.fill_between(xValues, yValues, PA, where=(yValues<=PA), color = 'lightsalmon', alpha = 0.6, interpolate = True)
            
            #Draw PA Line 
            ax.axhline(PA, color = 'orange', linewidth = 0.5)
            
            ax.set_title(nodeID, fontsize = 8)
            #ax.xaxis.set_major_locator(mdates.HourLocator(interval = 4))
            #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))  

            #Write the Resilience Loss value in the graph
            if Integral > 0:
                #Get the coordinates of the filled_poly and assign text in the mid point
                (x0, y0), (x1, y1) = filled_poly.get_paths()[0].get_extents().get_points()
                ax.text(x = (x0 + x1) / 2, y = y1 + 0.05, s = f'{ResilienceLossNorm:.2f}', fontsize = 6, color = 'red')

            plotCounter += 1
        
        fig.supxlabel("Time")
        fig.supylabel("Node Flood Performance")
        
        fig.tight_layout() 
        
    plt.show() 
    
    
    
    return NodesResilienceParameters

def main():
    
    #InpFilePath = r"I:\O meu disco\PhD\Tese\REFUSS\SWMM_SCRIPT\TESTESWMM.inp"
    RptFilePath = r"I:\O meu disco\PhD\Tese\REFUSS\SWMM_SCRIPT\TESTESWMM.rpt"
    OutFilePath = r"I:\O meu disco\PhD\Tese\REFUSS\SWMM_SCRIPT\TESTESWMM.out"
    
    Start_Date = datetime.datetime(2023, 6, 28, 0, 0, 0)
    End_Date = datetime.datetime(2023, 6, 28, 6, 0, 0)

    FloodAdmissibleDepth = (0.2, 0.7) #Max. admissible flood depth to assign Failure Performance [m] on minor [0] and major system [1]
    
    
    Nodes = GetFromReport(RptFilePath, "Node Summary")
    Links = GetFromReport(RptFilePath, "Link Summary")
    CrossSections = GetFromReport(RptFilePath, "Cross Section Summary")

    #print(Nodes)
    #print(Links)
    #print(CrossSections)
    
    
    NodesResilienceParameters = CalculateNodesResiliencePararameters(Nodes, Links, CrossSections, FloodAdmissibleDepth[0])
    
    NodesResults = getNodeResults(NodesResilienceParameters, OutFilePath)
    
    NodesResilienceParameters = CalculateNodesResiliencePerformance(Nodes, NodesResults, NodesResilienceParameters, FloodAdmissibleDepth[0])   
     
    SystemSurchargeResilience = (NodesResilienceParameters["Surcharge Resilience"] * NodesResilienceParameters["Weight"]).sum()
    SystemFloodResilience = (NodesResilienceParameters["Flood Resilience"] * NodesResilienceParameters["Weight"]).sum()
      
    print(NodesResilienceParameters[["Surcharge Resilience Zero", "Surcharge Resilience Loss", "Surcharge Resilience", "Weight"]])
    print(NodesResilienceParameters[["Flood Resilience Zero", "Flood Resilience Loss", "Flood Resilience", "Weight"]])
    
    print("\n \n")
    print(f'********** System Surcharge Resilience = {SystemSurchargeResilience:.3f} **********')
    print(f'********** System Flood Resilience = {SystemFloodResilience:.3f} **************')
    print("\n \n")
    
    return

if __name__ == "__main__":
	main()
 
	os.system("pause")