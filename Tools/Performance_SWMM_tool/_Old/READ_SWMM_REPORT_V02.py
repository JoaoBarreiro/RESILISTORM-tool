import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.integrate import trapezoid
import sympy as sy

def getFileLines(InputFile):
    
    with open(InputFile, "r") as File:
        list = File.readlines()
    
    return list

def getNodesSummary(list):
    
    Nodes = pd.DataFrame(columns = ["Type", "InvertElev", "MaxDepth", "PondedArea", "ExternalInflow"])
    
    SectionFound = False
    SectionStart = 0
    
    for index, line in enumerate(list):
        CleanLine = line.rstrip().split()
        
        if SectionFound == False and line.startswith("  Node Summary"):
            SectionFound = True
            SectionStart = index + 5
            
        elif SectionFound == True and index >= SectionStart:
            if CleanLine == []:
                break
            else:
                if len(CleanLine) == len(Nodes.columns) + 1:
                    Nodes.loc[CleanLine[0]] = CleanLine[1:]
                elif len(CleanLine) < len(Nodes.columns) + 1:
                    Nodes.loc[CleanLine[0]] = CleanLine[1:] + [np.nan]*(len(Nodes.columns) + 1 -len(CleanLine))
                
    Nodes = Nodes.astype({"Type": "string", "InvertElev": "float", "MaxDepth": "float" , "PondedArea": "float", "ExternalInflow": "string"})

    return Nodes

def getLinksSummary(list):
    
    Links = pd.DataFrame(columns = ["FromNode", "ToNode", "Type", "Length", "Slope", "Roughness"])
    
    SectionFound = False
    SectionStart = 0
    
    for index, line in enumerate(list):
        CleanLine = line.rstrip().split()
        
        if SectionFound == False and line.startswith("  Link Summary"):
            SectionFound = True
            SectionStart = index + 4
            
        elif SectionFound == True and index >= SectionStart:
            if CleanLine == []:
                break
            else:
                if len(CleanLine) == len(Links.columns) + 1:
                    Links.loc[CleanLine[0]] = CleanLine[1:]
                if len(CleanLine) < len(Links.columns) + 1:
                    Links.loc[CleanLine[0]] = CleanLine[1:] + [np.nan]*(len(Links.columns) + 1 -len(CleanLine))
                    
    Links = Links.astype({"FromNode": "string", "ToNode": "string", "Type": "string", "Length": "float", "Slope": "float", "Roughness": "float"})

    return Links

def getCrossSectionsSummary(list):
    
    CrossSections = pd.DataFrame(columns = ["Shape", "FullDepth", "FullArea", "HydRad", "MaxWidth", "NoBarrels", "FullFlow"])
    
    SectionFound = False
    SectionStart = 0
    
    for index, line in enumerate(list):
        CleanLine = line.rstrip().split()
        
        if SectionFound == False and line.startswith("  Cross Section Summary"):
            SectionFound = True
            SectionStart = index + 5
            
        elif SectionFound == True and index >= SectionStart:
            if CleanLine == []:
                break
            else:
                if len(CleanLine) == len(CrossSections.columns) + 1 :
                    CrossSections.loc[CleanLine[0]] = CleanLine[1:]
                if len(CleanLine) < len(CrossSections.columns) + 1:
                    CrossSections.loc[CleanLine[0]] = CleanLine[1:] + [np.nan]*(len(CrossSections.columns) + 1 -len(CleanLine))
                    
    CrossSections = CrossSections.astype({"Shape": "string", "FullDepth": "float", "FullArea": "float", "HydRad": "float", "MaxWidth": "float", "NoBarrels": "int", "FullFlow": "float"})
    
    return CrossSections

def getNodeResults(list):
    
    AllNodeResults = {}
    
    SectionFound = False
    SectionStart = 0
    
    for index, line in enumerate(list):
        CleanLine = line.rstrip().split()
      
        if SectionFound == False and line.startswith("  Node Results"):
            SectionFound = True
            SectionStart = index
            
            NodeFound = False
            NodeStart = 0
        
        elif SectionFound == True and index >= SectionStart:
            if index < SectionStart + 3:
                continue
            elif line.startswith("  *"):
                break
            
            elif line.startswith("  <<<"):
                NodeName = CleanLine[2]
                if NodeName.endswith("_OF"):
                    continue
                NodeFound = True
                NodeStart = index + 5
                NodeResults = pd.DataFrame(columns = ["Date", "Time", "Inflow", "Flooding", "Depth", "Head"])
                
            elif NodeFound == True:    
                if index < NodeStart:
                    continue
                elif CleanLine == []:
                    NodeFound = False
                    NodeStart = 0
                    AllNodeResults[NodeName] = NodeResults
                else:
                    DateString = CleanLine[0].split("/")
                    Year = int(DateString[2])
                    Month = int(DateString[0])
                    Day = int(DateString[1])
                    Date = datetime.date(Year, Month, Day)
                    
                    TimeString = CleanLine[1].split(":")
                    Hour = int(TimeString[0])
                    Minute = int(TimeString[1])
                    Second = int(TimeString[2])
                    Time = datetime.time(Hour, Minute, Second)
                    
                    Inflow = float(CleanLine[2])
                    Flooding = float(CleanLine[3])
                    Depth = float(CleanLine[4])
                    Head = float(CleanLine[5])
                    
                    NodeResults.loc[len(NodeResults)] = [Date, Time, Inflow, Flooding, Depth, Head]
    
    return AllNodeResults

def getLinkResults(list):
    
    AllLinkResults = {}
    
    SectionFound = False
    SectionStart = 0
    
    for index, line in enumerate(list):
        CleanLine = line.rstrip().split()
      
        if SectionFound == False and line.startswith("  Link Results"):
            SectionFound = True
            SectionStart = index
            
            LinkFound = False
            LinkStart = 0
        
        elif SectionFound == True and index >= SectionStart:
            if index < SectionStart + 3:
                continue
            elif line.startswith("  *"):
                break
            
            elif line.startswith("  <<<"):
                LinkName = CleanLine[2]
                # if LinkName.endswith("_OL"):
                #     continue
                LinkFound = True
                LinkStart = index + 5
                LinkResults = pd.DataFrame(columns = ["Date", "Time", "Flow", "Velocity", "Depth", "Capacity"])
                
            elif LinkFound == True:    
                if index < LinkStart:
                    continue
                elif CleanLine == []:
                    LinkFound = False
                    LinkStart = 0
                    AllLinkResults[LinkName] = LinkResults
                else:
                    DateString = CleanLine[0].split("/")
                    Year = int(DateString[2])
                    Month = int(DateString[0])
                    Day = int(DateString[1])
                    Date = datetime.date(Year, Month, Day)
                    
                    TimeString = CleanLine[1].split(":")
                    Hour = int(TimeString[0])
                    Minute = int(TimeString[1])
                    Second = int(TimeString[2])
                    Time = datetime.time(Hour, Minute, Second)
                    
                    Flow = float(CleanLine[2])
                    Velocity = float(CleanLine[3])
                    Depth = float(CleanLine[4])
                    Capacity = float(CleanLine[5])
                    
                    LinkResults.loc[len(LinkResults)] = [Date, Time, Flow, Velocity, Depth, Capacity]
    
    return AllLinkResults

def calculateNodesResPar(Nodes, Links, CrossSections):
    
#NodesResilienceParameters = pd.DataFrame(columns = ["Name", "LinkName","MaxFullDepth", "Weight"])

    NodesResilienceParameters = Nodes[Nodes["Type"] == "JUNCTION"].copy()
    
    #1. find all the links connected to the node
    for nodeID, nodeProp in NodesResilienceParameters.iterrows():
        ConnectedLinks = Links.query("(FromNode == @nodeID | ToNode == @nodeID) & Type == 'CONDUIT' ")

    #2. find the greatest cross section linked to the node and respective section maximum height
        MaxSection = 0
        MaxFullDepth = 0
        LinkName = "ERRO"
        for linkID, linkProp in ConnectedLinks.iterrows():
            
            Section = CrossSections.loc[linkID, "FullArea"]
            if Section > MaxSection:
                LinkName = linkID
                MaxSection = Section
                MaxFullDepth = CrossSections.loc[linkID, "FullDepth"]
                
    #3. attribute that MaxFullDepth to the node
        NodesResilienceParameters.loc[nodeID, "LinkName"] = LinkName
        NodesResilienceParameters.loc[nodeID, "MaxFullDepth"] = MaxFullDepth
        NodesResilienceParameters.loc[nodeID, "PA"] = MaxFullDepth  / NodesResilienceParameters.loc[nodeID, "MaxDepth"]
        
        #print(NodesResilienceParameters.loc[i])
        
    #4. calculate the node weight based on that MaxFullDepth -> W(i) = Deq(i) / Soma(i:n) Deq(i)
    for nodeID, nodeProp in NodesResilienceParameters.iterrows():
        NodesResilienceParameters.loc[nodeID, "Weight"] = nodeProp["MaxFullDepth"] / NodesResilienceParameters["MaxFullDepth"].sum()
    
    NodesResilienceParameters = NodesResilienceParameters[["MaxFullDepth", "Weight", "PA"]]
    
    print(NodesResilienceParameters)
    
    #print(NodesResilienceParameters["Weight"].sum())
        
    return NodesResilienceParameters

def plotNodesRelativeDepth(Nodes, NodeResults):
    
    fig, ax1 = plt.subplots()
    
    
    xValues = []
    
    for index, row in enumerate(list(NodeResults.items())[0][1]["Date"]):
        xValues.append(datetime.datetime.combine(list(NodeResults.items())[0][1]["Date"][index], list(NodeResults.items())[0][1]["Time"][index]))
    
    
    for i in NodeResults.keys():
        if Nodes[Nodes["Name"] == i]["Type"].values[0] == "JUNCTION":
            
            MaxDepth = Nodes[Nodes["Name"] == i]["MaxDepth"].values[0]
            
            ax1.plot(xValues,                           
                    #NodeResults[i]["Depth"],            
                    NodeResults[i]["Depth"] / MaxDepth,  
                    label = i,                          
                    linewidth = 0.5,                    
                    color="black",                      
                    linestyle = "dashed")
    
    
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Node depth / Node max depth")
    
    #fig.autofmt_xdate()
    fig.tight_layout() 
    plt.show() 
    
    return


def plotNodesPerformance(Nodes, NodesResults, NodesResilienceParameters):
    
    PlotCols = 8
    PlotRows = 10
    PlotTotal = len(NodesResilienceParameters)
    
    NrFigures = PlotTotal // (PlotCols*PlotRows)
    if NrFigures % PlotTotal != 0:                      #VERIFICAR SE NR DE FIGURAS BATE CERTO!
         NrFigures += 1 
           
    xValues = []
    
    for node, row in enumerate(list(NodesResults.items())[0][1]["Date"]):
        xValues.append(datetime.datetime.combine(list(NodesResults.items())[0][1]["Date"][node], list(NodesResults.items())[0][1]["Time"][node]))
    
    xValues = pd.DataFrame(xValues, columns = ["DataTime"])      
    
    Nodes = Nodes.query("Type == 'JUNCTION'").copy()
    
    plotCounter = 0
    
    for k in range(1, NrFigures+1):
        fig = plt.figure(k, figsize=(11.69, 8.27))   #A4 landscape size
        gs = fig.add_gridspec(nrows = PlotRows, ncols = PlotCols)
        axs = gs.subplots(sharex = True, sharey = True)

        axs[0,0].set_ylim(-0.1, 1.1)
        axs[0,0].invert_yaxis()
               
        for ax in axs.ravel():
            if plotCounter ==  PlotTotal: continue
            
            nodeID = Nodes.index[plotCounter]
                              
            MaxDepth = Nodes.loc[nodeID, "MaxDepth"]
            
            PA = NodesResilienceParameters.loc[nodeID, "PA"]
            
            yValues = NodesResults[nodeID]["Depth"] / MaxDepth
            
            yValues = yValues.clip(upper = 1.0)
                    
            ax.plot(xValues["DataTime"].values, yValues,                          
                    linewidth = 0.5,                    
                    color="black",                      
                    linestyle = "dashed")
            
            filled_poly = ax.fill_between(xValues["DataTime"].values, yValues, PA, where=(yValues>=PA), color = 'lightsalmon', alpha = 0.6, interpolate = True)
            
            ax.axhline(PA, color = 'orange', linewidth = 0.5)
            
            ax.set_title(nodeID, fontsize = 8)
            ax.xaxis.set_major_locator(mdates.HourLocator(interval = 4))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))  
                                
            #calculate integral above PA
            xModified = xValues["DataTime"].reset_index()['DataTime'].diff().dt.total_seconds().fillna(0).cumsum().values
            yModified = (yValues - PA).clip(lower = 0)
            Integral = trapezoid(yModified, xModified)
            
            
            NodesResilienceParameters.loc[nodeID, "Integral"] = Integral
            
            Severity = 1/PA * 1 /(xModified.max()-xModified.min()) * Integral
            
            NodesResilienceParameters.loc[nodeID, "Resilience"] = 1 - Severity
            print(f'{nodeID}: \t\t\t Integral = {Integral:.1f}\t Severity = {Severity:.1f}\t Resilience = {1 - Severity:.1f}')
            
            if Integral > 0:
                (x0, y0), (x1, y1) = filled_poly.get_paths()[0].get_extents().get_points()
                ax.text(x = (x0 + x1) / 2, y = y1 + 0.05, s = f'{Integral:.1f}', fontsize = 6, color = 'red', )

            plotCounter += 1
        
        fig.supxlabel("Time")
        fig.supylabel("Node Performance")
        
        fig.tight_layout() 
        
        plt.show() 
        
    return NodesResilienceParameters


def main():
    
    InputFile = r"C:\Users\joaop\OneDrive\Documentos\SINERGEA\SWMM-Land_Cenarios\SWMM-Land\SWMM\FullReport.rpt"
    
    ReportLines = getFileLines(InputFile)
    
    Nodes = getNodesSummary(ReportLines)
    # print(Nodes)
    Links = getLinksSummary(ReportLines)
    #print(Links)
    CrossSections = getCrossSectionsSummary(ReportLines)
    #print(CrossSections)

    NodesResilienceParameters = calculateNodesResPar(Nodes, Links, CrossSections)
    
    NodesResults = getNodeResults(ReportLines)
    # print(NodeResults.keys())
    
    # LinkResults = getLinkResults(ReportLines)
    # print(LinkResults.keys())
       
    #plotNodesRelativeDepth(Nodes, NodesResults)
    
    NodesResilienceParameters = plotNodesPerformance(Nodes, NodesResults, NodesResilienceParameters)
    
    PRT = (NodesResilienceParameters["Resilience"] * NodesResilienceParameters["Weight"]).sum()
    print(f'PRT = {PRT:.3f}')
    
    return



if __name__ == "__main__":
	main()
	os.system("pause")