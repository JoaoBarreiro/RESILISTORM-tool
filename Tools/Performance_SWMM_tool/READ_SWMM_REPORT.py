import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def getFileLines(InputFile):
    
    with open(InputFile, "r") as File:
        list = File.readlines()
    
    return list

def getNodesSummary(list):
    
    Nodes = pd.DataFrame(columns = ["Name", "Type", "InvertElev", "MaxDepth", "PondedArea", "ExternalInflow"])
    
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
                if len(CleanLine) == 5:
                    Nodes.loc[len(Nodes)] = CleanLine + ["No"]
                elif len(CleanLine) == 6:
                    Nodes.loc[len(Nodes)] = CleanLine
                
    Nodes = Nodes.astype({"Name": "string", "Type": "string", "InvertElev": "float", "MaxDepth": "float" , "PondedArea": "float", "ExternalInflow": "string"})

    return Nodes

def getLinksSummary(list):
    
    Links = pd.DataFrame(columns = ["Name", "FromNode", "ToNode", "Type", "Length", "Slope", "Roughness"])
    
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
                if len(CleanLine) == len(Links.columns):
                    Links.loc[len(Links)] = CleanLine
                if len(CleanLine) < 7:
                    Links.loc[len(Links)] = CleanLine + ["nan"]*(len(Links.columns)-len(CleanLine))
                    
    Links = Links.astype({"Name": "string", "FromNode": "string", "ToNode": "string", "Type": "string", "Length": "float", "Slope": "float", "Roughness": "float"})

    return Links

def getCrossSectionsSummary(list):
    
    CrossSections = pd.DataFrame(columns = ["Conduit", "Shape", "FullDepth", "FullArea", "HydRad", "MaxWidth", "NoBarrels", "FullFlow"])
    
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
                if len(CleanLine) == len(CrossSections.columns):
                    CrossSections.loc[len(CrossSections)] = CleanLine
                if len(CleanLine) < 7:
                    CrossSections.loc[len(CrossSections)] = CleanLine + ["nan"]*(len(CrossSections.columns)-len(CleanLine))
                    
    CrossSections = CrossSections.astype({"Conduit": "string", "Shape": "string", "FullDepth": "float", "FullArea": "float", "HydRad": "float", "MaxWidth": "float", "NoBarrels": "int", "FullFlow": "float"})
    
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
    for i, node in NodesResilienceParameters.iterrows():
        ConnectedLinks = Links.query("(FromNode == @node['Name'] | ToNode == @node['Name']) & Type == 'CONDUIT' ")

    #2. find the greatest cross section linked to the node and respective section maximum height
        MaxSection = 0
        MaxFullDepth = 0
        LinkName = "ERRO"
        for j, link in ConnectedLinks.iterrows():
            
            Section = CrossSections.query('Conduit == @link["Name"]')["FullArea"].item()
            if Section > MaxSection:
                LinkName = link["Name"]
                MaxSection = Section
                MaxFullDepth = CrossSections.query('Conduit == @link["Name"]')["FullDepth"].item()
                
    #3. attribute that MaxFullDepth to the node
        NodesResilienceParameters.loc[i, "LinkName"] = LinkName
        NodesResilienceParameters.loc[i, "MaxFullDepth"] = MaxFullDepth
        NodesResilienceParameters.loc[i, "PA"] = MaxFullDepth  / NodesResilienceParameters.loc[i, "MaxDepth"]
        
        #print(NodesResilienceParameters.loc[i])
        
    #4. calculate the node weight based on that MaxFullDepth -> W(i) = Deq(i) / Soma(i:n) Deq(i)
    for i, node in NodesResilienceParameters.iterrows():
        NodesResilienceParameters.loc[i, "Weight"] = node["MaxFullDepth"] / NodesResilienceParameters["MaxFullDepth"].sum()
    
    NodesResilienceParameters = NodesResilienceParameters[["Name", "MaxFullDepth", "Weight", "PA"]]
    
    print(NodesResilienceParameters)
    
    print(NodesResilienceParameters["Weight"].sum())
        
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
    
    PlotCols = 5
    PlotTotal = len(NodesResilienceParameters)
    
    PlotRows = PlotTotal // PlotCols
    
    if PlotTotal % PlotCols != 0:
        PlotRows += 1
        
    PlotPosition = range(1, PlotTotal + 1)
    
    
    xValues = []
    
    for index, row in enumerate(list(NodesResults.items())[0][1]["Date"]):
        xValues.append(datetime.datetime.combine(list(NodesResults.items())[0][1]["Date"][index], list(NodesResults.items())[0][1]["Time"][index]))
    
    xValues = pd.DataFrame(xValues, columns = ["DataTime"])["DataTime"].values       
    
    Nodes = 
    
    
    fig = plt.figure(1)
    
    for k in range(PlotTotal):
    
        ax = fig.add_subplot(PlotRows, PlotCols, PlotPosition[k])
        ax.
    
    #fig, ax1 = plt.subplots(ncols = numbercolumns, sharex = True, sharey = True)
     

    
    for n, ax in enumerate(ax1.flatten()):
        for i in NodesResults.keys():
            if Nodes[Nodes["Name"] == i]["Type"].values[0] == "JUNCTION":
                
                MaxDepth = Nodes[Nodes["Name"] == i]["MaxDepth"].values[0]
                
                PA = NodesResilienceParameters.query("Name == @i")["PA"].values[0]
                
                yValues = NodesResults[i]["Depth"] / MaxDepth
                
                ax.plot(xValues, yValues,                           
                        #NodesResults[i]["Depth"],            
                        #NodesResults[i]["Depth"] / MaxDepth,
                        label = i,                          
                        linewidth = 0.5,                    
                        color="black",                      
                        linestyle = "dashed")
                
                ax.fill_between(xValues, yValues, PA)
                ax.axhline(PA)
                ax.set_title(i)
        
        # for ax in ax1.flat:
            ax.set(xlabel = "Time", ylabel = "Node Performance")
            ax.label_outer()
        
    #ax1.set_xlabel("Date")
    #ax1.set_ylabel("Node depth / Node max depth")
    
    #fig.autofmt_xdate()
    fig.tight_layout() 
    plt.show() 
    
    return


def main():
    
    InputFile = r"C:\Users\joaop\OneDrive\Documentos\SINERGEA\SWMM-Land_Cenarios\SWMM-Land\SWMM\FullReport.rpt"
    
    ReportLines = getFileLines(InputFile)
    
    Nodes = getNodesSummary(ReportLines)
    # print(Nodes)
    Links = getLinksSummary(ReportLines)
    # print(Links)
    CrossSections = getCrossSectionsSummary(ReportLines)
    # print(CrossSections)

    NodesResilienceParameters = calculateNodesResPar(Nodes, Links, CrossSections)
    
    NodesResults = getNodeResults(ReportLines)
    # print(NodeResults.keys())
    
    # LinkResults = getLinkResults(ReportLines)
    # print(LinkResults.keys())
       
    #plotNodesRelativeDepth(Nodes, NodesResults)
    
    plotNodesPerformance(Nodes, NodesResults, NodesResilienceParameters)
    
    return



if __name__ == "__main__":
	main()
	os.system("pause")