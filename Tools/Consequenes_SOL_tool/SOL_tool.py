import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta

from astropy.time import Time

from PySide6.QtWidgets import (QMainWindow, QApplication, QFileDialog, QMessageBox)
from PySide6.QtCore import Signal

from netCDF4 import Dataset

import xarray as xr

import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.tri as tri
import matplotlib.collections as mcoll

from SOL_tool_GUI import Ui_MainWindow


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
        self.setWindowTitle("BASEMENT *.sol Performance Tool")
        
        self.ui.MeshFile_Search.clicked.connect(lambda: self.FindFile(type = "Mesh"))
        self.ui.DepthFile_Search.clicked.connect(lambda: self.FindFile(type = "Depth"))
        self.ui.VelocityFile_Search.clicked.connect(lambda: self.FindFile(type = "Velocity"))
        
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
        
        if type == "Depth":
            fileName, _ = QFileDialog.getOpenFileName(self, "Select Depth solution file", "", "(*.sol)")       
            self.ui.DepthFile_Filepath.setText(fileName)
            self.ui.VelocityFile_Filepath.setEnabled(True)
            self.ui.VelocityFile_Search.setEnabled(True)
            
            depth_file_lines = get_file_lines(fileName)
            _, _, _, start_date, end_date = get_timesettings(depth_file_lines)
                                
            self.ui.StartingDate.setDateTime(start_date)
            self.ui.StartingDate.setMinimumDateTime(start_date)
            self.ui.StartingDate.setMaximumDateTime(end_date)
            
            self.ui.EndDate.setDateTime(end_date)            
            self.ui.EndDate.setMinimumDateTime(start_date)
            self.ui.EndDate.setMaximumDateTime(end_date)
            
        elif type == "Velocity":
            fileName, _ = QFileDialog.getOpenFileName(self, "Select Velocity solution file", "", "(*.sol)")
            self.ui.VelocityFile_Filepath.setText(fileName)
            
        elif type == "Mesh":
            fileName, _ = QFileDialog.getOpenFileName(self, "Select 2D Mesh file", "", "(*.2dm)")
            self.ui.MeshFile_Filepath.setText(fileName)
        
    def verify_inputs(self):
        self.MeshFile = self.ui.MeshFile_Filepath.text()
        self.DepthFile= self.ui.DepthFile_Filepath.text()
        self.VelocityFile = self.ui.VelocityFile_Filepath.text()
        self.StartingDate = datetime(   self.ui.StartingDate.date().year(),
                                        self.ui.StartingDate.date().month(),
                                        self.ui.StartingDate.date().day(),
                                        self.ui.StartingDate.time().hour(),
                                        self.ui.StartingDate.time().minute(),
                                        self.ui.StartingDate.time().second())
                                    
        self.EndDate = datetime(self.ui.EndDate.date().year(),
                                self.ui.EndDate.date().month(),
                                self.ui.EndDate.date().day(),
                                self.ui.EndDate.time().hour(),
                                self.ui.EndDate.time().minute(),
                                self.ui.EndDate.time().second())
        
        self.MinorThresh = self.ui.MinorThreshold.value()
        self.MajorThresh = self.ui.MajorThreshold.value()
        
        if self.MeshFile == "":
            QMessageBox.warning(self, "Mesh Filepath", "Mesh filepath must be specified!")
            return False
        elif self.DepthFile == "":
            QMessageBox.warning(self, "Depth Filepath", "Depth filepath must be specified!")
            return False
        elif os.path.splitext(self.DepthFile)[1] != ".sol":
            QMessageBox.warning(self, "Depth File extension", "Depth File extension must be *.sol!")
            return False
        
        if self.VelocityFile == "":
            QMessageBox.warning(self, "Velocity Filepath", "Velocity filepath must be specified!")
            return False
        elif os.path.splitext(self.VelocityFile)[1] != ".sol":
            QMessageBox.warning(self, "Velocity File extension", "Velocity File extension must be *.sol!")
            return False
        
        if self.ui.StartingDate == self.ui.EndDate:
            QMessageBox.warning(self, "Analysis period", "Analysis period must be greater than 0!")
            return False
    
        if self.ui.SFP_checkBox.isChecked():
            self.SFP = True
        else:
            self.SFP = False
        
        if self.ui.IHP_checkBox.isChecked():
            self.IHP = True
        else:
            self.IHP = False
            
        if self.ui.IHV_checkBox.isChecked():
            self.IHV = True
        else:
            self.IHV = False
                        
        if self.ui.IHV_checkBox.isChecked():
            self.PrintLog = True
        else:
            self.PrintLog = False        
        
        self.Proceed.emit()
    
    def closeEvent(self, event):
        self.close()

def getData(file_lines: list):

    data_type, ND, NC = get_data_type(file_lines)
    
    time_units, time_steps, time_lines, start_date, end_date = get_timesettings(file_lines)

    data_series = get_data_results(file_lines, data_type, time_units, time_steps, time_lines, ND)

    return data_series, time_units, time_steps, ND, NC

def get_data_type(file_lines):
    data_type = None
    ND = NC = 0
    
    for i, line in enumerate(file_lines):
        if line.startswith("BEGSCL"):
            data_type = "scalar"
        elif line.startswith("BEGVEC"):
            data_type = "vector"
        elif line.startswith("ND"):
            ND = int(line.split()[1])
        elif line.startswith("NC"):
            NC = int(line.split()[1])
        if line.startswith("TS"):
            break
    if not data_type:
        raise ValueError("Data type not found in file.")
    
    return data_type, ND, NC

def get_timesettings(file_lines):
    
    time_units = None
    time_steps = []
    time_lines = []
    start_date = end_date = None
    
    time_options = {"seconds": ["seconds", "sec"],
                    "minutes": ["minutes", "min"],
                    "hours": ["hours", "hour"]}    
    
    for i, line in enumerate(file_lines):
        if line.startswith("RT_JULIAN"):
            julian_date = float(line.split()[1])
            start_date = julian_to_gregorian_astropy(julian_date)
        elif line.startswith("TIMEUNITS"):
            unit_text = line.split()[1].lower()
            for time_option, options in time_options.items():
                if unit_text in options:
                    time_units = time_option
                    break
        elif line.startswith("TS"):
            raw_time = line.split()[2]
            if raw_time == '0x0.000000000000p+0':
                timestep = float(0)
            else:
                timestep = float(raw_time)
            time_steps.append(timestep)
            time_lines.append(i)
    
    if time_steps:  
        end_date = start_date + timedelta(seconds=time_steps[-1])
    else:
        raise ValueError("No time steps found in file.")

    return time_units, time_steps, time_lines, start_date, end_date

def julian_to_gregorian_astropy(julian_date):
    # Use astropy to handle the conversion
    t = Time(julian_date, format='jd', scale='utc')
    return t.to_datetime()

def get_data_results(file_lines: list,
                     data_type: str,
                     time_units: str,
                     time_steps: list,
                     time_lines: list,
                     ND: int):
    
    # initialize result array with nr rows = nr time steps, nr cols = nr nodes
    result = np.zeros((len(time_steps), ND))

    # Initialize the index for time steps
    timestep_index = -1
    
    first_TS_line = time_lines[0]
    
    # time_lines = [x - time_lines[0] for x in time_lines]
    
    if data_type == "scalar":
        # Process each line in the file starting from the first time step line
        for i, line in enumerate(file_lines[time_lines[0]:], start=time_lines[0]):
            # New time step detection
            if "TS" in line:
                if timestep_index < len(time_steps) - 1:
                    timestep_index += 1
                continue

            # Skip non-data lines
            if not line.strip() or "ENDDS" in line:
                continue

            # Process data lines only after the first TS line has been encountered        
            if timestep_index >= 0:
                # Extract data value
                data_value = float(line.split()[0])

            # Assign data value to the result array
            # The element index is (i - time_lines[0] - 1) % ND because we need to account for the offset and loop back to 0 after ND
            element_index = (i - time_lines[timestep_index] - 1) % ND
            result[timestep_index, element_index] = data_value
        
    elif data_type == "vector":
        # Process each line in the file starting from the first time step line
        for i, line in enumerate(file_lines[time_lines[0]:], start=time_lines[0]):
            # New time step detection
            if "TS" in line:
                if timestep_index < len(time_steps) - 1:
                    timestep_index += 1
                continue

            # Skip non-data lines
            if not line.strip() or "ENDDS" in line:
                continue
            
            # Process data lines only after the first TS line has been encountered        
            if timestep_index >= 0:
                # Extract data value
                data_value = np.linalg.norm(np.array(line.split()[:2], dtype=float))

            # Assign data value to the result array
            # The element index is (i - time_lines[0] - 1) % ND because we need to account for the offset and loop back to 0 after ND
            element_index = (i - time_lines[timestep_index] - 1) % ND
            result[timestep_index, element_index] = data_value        

    return result    
    
    
    if data_type == "scalar":                   #more efficient, just checks the data_type once!
        for i, line in enumerate(file_lines[first_TS_line:-2]):
            if i in time_lines:
                element_id = 1
                timestep = time_steps[time_lines.index(i)]
                timestep_index = time_steps.index(timestep)
            else:
                result[timestep_index, element_id-1] = float(line.split()[0])
                element_id += 1
            
    elif data_type == "vector":
        for i, line in enumerate(file_lines[first_TS_line:-2]):
            if i in time_lines:
                element_id = 1
                timestep = time_steps[time_lines.index(i)]
                timestep_index = time_steps.index(timestep)
            else:
                x_value = float(line.split()[0])
                y_value = float(line.split()[1])
                modulus = np.sqrt(x_value**2 + y_value**2)
                result[timestep_index, element_id-1] = float(modulus)
                element_id += 1       
    
    # contains the data series for each element at each timestep
    # i.e. each column is a series and each row is a timestep
    # !!!! to iterate by node time series, use result.T !!!!
    return result

def calculate_result(line: str, data_type: str):
    if data_type == "scalar":            
        return float(line.split()[0])
    elif data_type == "vector":
        x_value = line.split()[0]
        y_value = line.split()[1]
        modulus = np.sqrt(x_value**2 + y_value**2)
        return float(modulus)

def get_file_lines(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    return lines

def calculate_depth_performance(timestamps,
                                nodes_depth_series: np.ndarray,
                                minor_threshold: float,
                                major_threshold: float):
    """
    Calculate the normalized resilience performance for each node based on the integral between the minor and major thresholds over time. 
    Args:
        timestamps: The timestamps associated with the depth series data.
        nodes_depth_series: An array containing the depth series data for each node.
        minor_threshold: The lower threshold value.
        major_threshold: The upper threshold value.
    Returns:
        mean_normalized_resilience: The mean normalized resilience performance across all nodes.
        nodes_normalized_resilience: An array of normalized resilience values for each node.
    """
    
    # Initialize lists to store the normalized resilience values at each node
    nodes_normalized_resilience = []
    # Initialize list to store the integrals
    integrals = []
    
    ResilienceZero = (major_threshold - minor_threshold) * (timestamps[-1] - timestamps[0])
    
    # Loop over each node depth time serie
    for i, depth_serie in enumerate(nodes_depth_series.T):

        # Calculate the integral between the thresholds for the node
        integral = calculate_integral_between_thresholds(timestamps, depth_serie, minor_threshold, major_threshold)
        integrals.append(integral)
        
        # Calculate the normalized resilience for the current node
        normalized_resilience = 1 - integral / ResilienceZero
        nodes_normalized_resilience.append(normalized_resilience)

     # Convert the list to a numpy array for easy handling and return
    nodes_normalized_resilience = np.array(nodes_normalized_resilience)
   
    # Assuming all nodes have the same weight
    # 1. Calculate the total integral (resilience loss)
    total_integral = np.sum(integrals)
    # 2. Get normalized resilience performance 
    mean_normalized_resilience = 1 - total_integral / (ResilienceZero * len(nodes_depth_series.T))   # can do this because R0 is the same for all series and weights are the same 
    
    return mean_normalized_resilience, nodes_normalized_resilience  

def calculate_integral_between_thresholds(times, serie, lower_threshold, upper_threshold):
    # Clip the series at the upper threshold
    upper_clipped_serie = np.clip(serie, a_min=None, a_max=upper_threshold)

    # Clip the series at the lower threshold
    lower_clipped_serie = np.clip(serie, a_min=None, a_max=lower_threshold)

    # Calculate the integral of the series clipped at the upper threshold
    upper_integral = np.trapz(upper_clipped_serie, times)

    # Calculate the integral of the series clipped at the lower threshold
    lower_integral = np.trapz(lower_clipped_serie, times)

    # The integral between the thresholds is the difference between the two
    integral_between_thresholds = upper_integral - lower_integral

    return integral_between_thresholds

def resample_timeseries(times, series_2d, dt=60):
    """
    Resample time series data to a fixed time step for a 2D array where each column is a time series.

    :param times: 1D array of original time stamps common to all series.
    :param series_2d: 2D array where each column is a time series.
    :param dt: Fixed time step in seconds.
    :return: Tuple of new times and 2D array of resampled values.
    """
    # Create a new time array with fixed intervals from the min to max of original times
    new_times = np.arange(np.min(times), np.max(times) + dt, dt)
    
    # Initialize an empty array to store the resampled values for each series
    new_series_2d = np.empty((len(new_times), series_2d.shape[1]))
    
    # Iterate over each series (column) to interpolate the values
    for i in range(series_2d.shape[1]):
        new_series_2d[:, i] = np.interp(new_times, times, series_2d[:, i])
    
    return new_times, new_series_2d

def calculate_IHP_at_nodes(nodes_depth_series: np.ndarray,
                                nodes_velocity_series: np.ndarray,
                                method = "Defra"):
               
    if method == "Defra":
        DF = np.where(nodes_depth_series <= 0.25, 0.5, 1)
        HR = nodes_depth_series * (nodes_velocity_series + 0.5) + DF
        
        CV = [0.75, 1.25, 2]
        IHP = [1.0, 0.53, 0.21, 0.00]  #basically its a weight of each class
        
        # Initialize an array to hold the hazard values for each node
        IHP_at_nodes = np.zeros(HR.shape[1])     
        nodes_IHP_series = [] 
        lowest_IHP_at_nodes = np.zeros(HR.shape[1])  # Array to hold lowest CW at each node

        # Loop over each node HR time serie
        for i, node_hr_serie in enumerate(HR.T):
            # Initialize an array for hazard classification
            node_hazardclass_serie = np.zeros_like(node_hr_serie)
            nodes_weight_serie = np.zeros_like(node_hr_serie)

            for j, hr_value in enumerate(node_hr_serie):
                if hr_value <= CV[0]:
                    node_hazardclass_serie[j] = 0  # Class index for CW[0]
                    nodes_weight_serie[j] = IHP[0] # Assign corresponding weight
                elif hr_value <= CV[1]:
                    node_hazardclass_serie[j] = 1  # Class index for CW[1]
                    nodes_weight_serie[j] = IHP[1]
                elif hr_value <= CV[2]:
                    node_hazardclass_serie[j] = 2  # Class index for CW[2]
                    nodes_weight_serie[j] = IHP[2]
                else:
                    node_hazardclass_serie[j] = 3  # Class index for CW[3]
                    nodes_weight_serie[j] = IHP[3]

            # Store the weight series for the current node
            nodes_IHP_series.append(nodes_weight_serie)       

            # Find the lowest CW value for the current node
            lowest_IHP_at_nodes[i] = min(nodes_weight_serie)
            
            # As dt is constant on the series: 
            # 1. Count occurrences in each class
            class_counts = np.bincount(node_hazardclass_serie.astype(int), minlength=len(IHP))
            # 2. Calculate the proportions of time spent in each class   
            proportions = class_counts / len(node_hr_serie)
            # 3. Calculate Indicator of Hazard to Pedestrians (IHP) for the node by multipling the proprotion of time in each class with the corresponding class indicator weight
            IHP_at_nodes[i] = np.dot(proportions, IHP)            
                                    
        #calulate the hazard indicator as the  mean of the values in the nodes (assuming all nodes have the same weight)
        mean_nodes_hazard_indicator = np.mean(IHP_at_nodes)        
        
        nodes_IHP_series = np.array(nodes_IHP_series)
        
    return mean_nodes_hazard_indicator, nodes_IHP_series.T, IHP_at_nodes, lowest_IHP_at_nodes

def calculate_IHV_at_nodes(nodes_depth_series: np.ndarray,
                              nodes_momentum_series: np.ndarray,
                              method = "Martinez"):
    

    if method == "Martinez":
        # Define threshold values and corresponding weights
        depth_threshold = 0.28
        momentum_thresholds = [0.40, 0.55]
        IHV = [1.0, 0.35, 0.0] 
        
        # Initialize an array to hold the hazard values for each time series
        IHV_at_nodes = np.zeros(nodes_depth_series.shape[1])
        nodes_IHV_series = [] 
        lowest_IHV_at_nodes = np.full(nodes_depth_series.shape[1], np.inf)
      
        # Loop over each time series
        for i in range(nodes_depth_series.shape[1]):
            # Get depth and momentum values for the current time series
            depth_serie = nodes_depth_series[:, i]
            momentum_serie = nodes_momentum_series[:, i]

            # Initialize an array for hazard classification
            node_hazardclass_serie = np.zeros_like(depth_serie, dtype=int)
            node_IHV_serie = np.zeros_like(depth_serie)
            
            # Classify each time step into a hazard class and IHV
            for j in range(len(depth_serie)):
                if depth_serie[j] <= depth_threshold:
                    if momentum_serie[j] <= momentum_thresholds[0]:
                        node_hazardclass_serie[j] = 0  # Class index for IHV[0]
                        node_IHV_serie[j] = IHV[0]
                    elif momentum_thresholds[0] < momentum_serie[j] <= momentum_thresholds[1]:
                        node_hazardclass_serie[j] = 1  # Class index for IHV[1]
                        node_IHV_serie[j] = IHV[1]
                else:
                    node_hazardclass_serie[j] = 2  # Class index for IHV[1]
                    node_IHV_serie[j] = IHV[2]
               
            # Store the weight series for the current node
            nodes_IHV_series.append(node_IHV_serie)  
            
            lowest_IHV_at_nodes[i] = np.min(node_IHV_serie)

            # As dt is constant on the series: 
            # 1. Count occurrences in each class
            class_counts = np.bincount(node_hazardclass_serie, minlength=len(IHV))
            # 2. Calculate the proportions of time spent in each class   
            proportions = class_counts / len(depth_serie)
            # 3. Calculate weighted hazard for the node: multiply by class weights
            IHV_at_nodes[i] = np.dot(proportions, IHV)
    
    # Calculate the overall hazard indicator as the mean of all hazard values
    mean_nodes_hazard_indicator = np.mean(IHV_at_nodes)

    #convert nodes_weight_series to numpy array
    nodes_IHV_series = np.array(nodes_IHV_series)
    
    return mean_nodes_hazard_indicator, nodes_IHV_series.T, IHV_at_nodes, lowest_IHV_at_nodes

def find_interpolated_crossing_time(t1, t2, value1, value2, threshold):
    """
    Linearly interpolates to find the time at which the HR crosses a given threshold between two timestamps.
    
    Parameters:
    t1, t2 : float
        The two timestamps between which we are interpolating.
    value1, value2 : float
        The HR values at timestamps t1 and t2, respectively.
    threshold : float
        The threshold HR value we are checking for a crossing.
        
    Returns:
    float
        The interpolated time at which the HR crosses the threshold.
    """
    # The slope of the line connecting the two HR points
    slope = (value2 - value1) / (t2 - t1)
    
    # The time at which the HR crosses the threshold can be found by solving
    # the equation of the line for the time (t): hr1 + slope * (t - t1) = threshold
    # Rearranging for t gives us the following formula:
    crossing_time = t1 + (threshold - value1) / slope
    
    return crossing_time

def interpolate_values(t1, t2, value1, value2, new_time):
    # Linear interpolation to find the value at new_time
    slope = (value2 - value1) / (t2 - t1)
    interpolated_value = value1 + slope * (new_time - t1)
    return interpolated_value

def write_dat_file(timestamps,
                   values,
                   ND: int,
                   NC: int,
                   Window: tool_GUI,
                   basename: str,
                   directory: str):
    
 
    with open(directory, 'w') as f:
        f.write(f'DATASET\n')
        f.write(f'OBJTYPE "mesh2d"\n')
        f.write(f'RT_JULIAN {2433282.500000}\n')
        f.write("BEGSCL")
        f.write(f'ND {int(ND)}\n')
        f.write(f'NC {int(NC)}\n')
        f.write(f'NAME "{basename}"\n')
        f.write(f'TIMEUNITS Seconds\n')
        for i, ts in enumerate(timestamps):
            f.write(f'TS 0  {ts}\n')
            f.writelines(f'{j}\n' for j in values.T[i])  #values has timeseries as columns, need to transpose
        f.write(f'ENDDS')
    
    return

def read_2dm(filepath):
    faces = {}  # Dicionário para armazenar elementos com os ID dos respetivos nós: {elemento_id: [v1, v2, v3]}
    nodes = {}  # Dicionário para armazenar nós com as respetivas coordenadas: {node_id: (x, y)}

    with open(filepath, 'r') as file:
        for line in file:
            props = line.split()

            if props[0] == 'E3T':
                # Armazenar informações do elemento
                face_id = int(props[1])
                face_vertices = [int(props[2]), int(props[3]), int(props[4])]
                faces[face_id] = face_vertices
            
            elif props[0] == 'ND':
                # Armazenar informações do nó
                node_id = int(props[1])
                x = float(props[2])
                y = float(props[3])
                nodes[node_id] = (x, y)
    
    faces_centroids = {}
    faces_area = {}

    for face_id, face_vertices in faces.items():
        vertices_coords = [nodes[v] for v in face_vertices]
        #calculate the centroid of the face
        faces_centroids[face_id] = np.mean(vertices_coords, axis=0)
        #calculate de area of the face
        x1, y1 = vertices_coords[0]
        x2, y2 = vertices_coords[1]
        x3, y3 = vertices_coords[2]
        faces_area[face_id] = 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
        
    return faces, nodes, faces_area, faces_centroids

def calcualte_vertices_idw_weights(faces: dict,
                         faces_centroids: dict,
                         nodes: dict):
    
    weights_idw = {}  # Dicionário para armazenar os pesos IDW para cada face {face_id: [peso1, peso2, peso3]}

    for face_id, centroid in faces_centroids.items():
        vertices = faces[face_id]  # IDs dos vértices do elemento atual
        weights = []  # Lista para armazenar os pesos IDW de cada vértice para o centróide
        for vertex_id in vertices:
            vertex_coords = np.array(nodes[vertex_id])  # Coordenadas do vértice
            distance = np.linalg.norm(vertex_coords - centroid)  # Distância do vértice ao centróide
            if distance == 0:
                peso = 1e9  # Atribui um peso alto se a distância for zero
            else:
                peso = 1 / distance  # Peso IDW
            weights.append(peso)
        
        # Normaliza os pesos
        weights = np.array(weights)
        weights /= weights.sum()
        
        weights_idw[face_id] = weights  # Armazena os pesos IDW para a face atual

    return weights_idw

def calculate_centroid_idw_values(faces: dict,
                   weights_idw: dict,
                   nodes_values: np.ndarray):

    # receives a np.ndarray with len(np.ndarray.shape) == 1 -> not a time series!
    # uses the weights_idw dictionary to calculate the centroid value
    
    centroid_values = np.zeros((len(faces)))
    
    # Iterate over each face to calculate the centroid value
    for face_id, vertices_id in faces.items():
        # Get the weights for the current face
        weights = weights_idw[face_id]

        # Check if the number of vertices and weights match
        if len(vertices_id) != len(weights):
            raise ValueError(f"Number of vertices and weights do not match for face {face_id}.")
 
        # Perform a weighted sum of the node series for the current face
        for vertex_id, weight in zip(vertices_id, weights):
            # Convert vertex_id to 0-based index for nodes_series beacuse series indexation starts at 0
            vertex_index = vertex_id - 1
            centroid_values[face_id - 1] += nodes_values[vertex_index] * weight

    return centroid_values

def calculate_centroid_idw_timeseries(faces: dict,
                    weights_idw: dict,
                    nodes_series: np.ndarray):
    """
    Calculate the centroid time series for each face based on the given faces, IDW weights, and node series.

    Parameters:
    - faces: A dictionary containing the vertices of each face.
    - weights_idw: A dictionary containing the IDW weights for each face.
    - nodes_series: A numpy array containing the time series data for the nodes.

    Returns:
    - centroid_series: A numpy array containing the centroid time series for each face. 
    """
        
    # Initialize an array to hold the time series data for the centroids
    centroid_series = np.zeros((nodes_series.shape[0], len(faces))) 
    
    # Iterate over each face to calculate the centroid series
    for i, (face_id, vertices_id) in enumerate(faces.items()):
        # Get the weights for the current face
        weights = weights_idw[face_id]

        # Check if the number of vertices and weights match
        if len(vertices_id) != len(weights):
            raise ValueError(f"Number of vertices and weights do not match for face {i+1}.")
 
        # Perform a weighted sum of the node series for the current face
        for vertex_id, weight in zip(vertices_id, weights):
            # Convert vertex_id to 0-based index for nodes_series beacuse series indexation starts at 0
            vertex_index = vertex_id - 1
            centroid_series[:, i] += nodes_series[:, vertex_index] * weight

    return centroid_series

def calculate_mesh_areaweighted_value(centroids_values: np.ndarray,
                                      Mesh_faces_area: dict[float]):
    
    if len(centroids_values.shape) > 1:
        raise ValueError(f"calculate_mesh_areaweighted_value: centroids_values > 1 ")
    
    # Sort the dictionary by keys and extract the values into an array
    areas = np.array([Mesh_faces_area[key] for key in sorted(Mesh_faces_area.keys())])
    
    # Calculate the sum of products
    mesh_areaweighted_value = np.sum(centroids_values * areas)
            
    return mesh_areaweighted_value/sum(Mesh_faces_area.values())  

def calculate_mesh_areaweighted_timeseries(centroid_series, faces_area):
    """
    Calculate the time series of a property for the entire mesh based on centroid series and faces area.
    Equivalent to system performance (weighted by the mesh elements area)

    Parameters:
    - centroid_series: array-like, the centroid series of the property for each timestep
    - faces_area: dict, the areas of the faces in the mesh

    Returns:
    - mesh_time_series: array, the time series of the property for the entire mesh
    """
    
    # Initialize an array for the time series of the property for the entire mesh
    mesh_time_series = np.zeros(centroid_series.shape[0])
 
    # Iterate through each timestep
    for t in range(centroid_series.shape[0]):
        # Initialize the weighted sum for this timestep
        weighted_sum = 0

        # Iterate through each face in the mesh
        for face_id, area in faces_area.items():
            # Get the timeseries value from the centroid of the face for this timestep
            centroid_value = centroid_series[t, face_id-1]  # -1 because IDs start at 1

            # Weight the contribution by the face's area and add to the total
            weighted_sum += centroid_value * area

        # Calculate the weighted average for this timestep and store in the mesh time series
        mesh_time_series[t] = weighted_sum / sum(faces_area.values())

    #calculate the proportion of time of that the mesh_time_series is 
    
    return mesh_time_series
   
def export_attributes_to_faces(Mesh_faces: dict,
                               Mesh_nodes: dict,
                               attributes_dict: dict,
                               outputfile_name: str):
    # Initialize an empty list to store each face's data
    data = []

    # Loop through each face to create a polygon and assign attributes
    for face_id, node_ids in Mesh_faces.items():
        # Get the coordinates for each node in the face
        polygon_vertices = [Mesh_nodes[node_id] for node_id in node_ids]

        # Create the polygon geometry
        polygon = Polygon(polygon_vertices)

        # Prepare the row with the geometry and attributes
        row = {'geometry': polygon, 'face_id': face_id}
        
        # Assign attributes based on the provided dictionary
        for attribute_name, attribute_values in attributes_dict.items():
            if face_id <= len(attribute_values):
                row[attribute_name] = attribute_values[face_id - 1]  # Adjusting for 0-based indexing if necessary

        # Append the row to the data list
        data.append(row)

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(data)

    # Export the GeoDataFrame to a GeoPackage or any other desired format
    output_filename = f"{outputfile_name}.gpkg"
    gdf.to_file(output_filename, driver="GPKG")

def convert_centroidseries_to_vector(Mesh_faces: dict,
                                     Mesh_nodes: dict,
                                     face_centroid_data: np.ndarray,
                                     time_steps: list or np.ndarray,
                                     output_filename: str):
    
    # Initialize an empty list to store each face's data
    data = []

    # Loop through each face to create a polygon and assign time-varying data
    for face_id, node_ids in Mesh_faces.items():
        # Get the coordinates for each node in the face
        polygon_vertices = [Mesh_nodes[node_id] for node_id in node_ids]
        
        # Create the polygon geometry
        polygon = Polygon(polygon_vertices)
        
        # Prepare the row with the geometry and time-varying attributes
        row = {'geometry': polygon, 'face_id': face_id}
        for timestep in range(face_centroid_data.shape[0]):
            row[f'timestep_{timestep}'] = face_centroid_data[timestep, face_id - 1]  # Adjusting for 0-based indexing if necessary

        # Append the row to the data list
        data.append(row)

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(data)    
    
    # #Export the GeoDataFrame to a GeoPackage
    # gdf.to_file(f"output_filename.gpkg", driver="GPKG")
    
    # Assuming `gdf` is your original GeoDataFrame with 'timestep_x' columns
    long_gdf = gdf.melt(id_vars=['geometry', 'face_id'], var_name='time', value_name='value')

    # Convert 'time' from 'timestep_x' to an actual time format or an integer representing the timestep
    # Example: converting 'timestep_0', 'timestep_1', ... to integers 0, 1, ...
    long_gdf['time'] = long_gdf['time'].str.extract('(\d+)$').astype(int)
    
    file_path = f"C:\\Users\\joaop\\OneDrive\\Documentos\\BASEMENT TEST\\{output_filename}.gpkg"
    long_gdf.to_file(file_path, driver="GPKG")
 
def interactive_mesh_plot(filename_geometry, filename_data):
    # Open the NetCDF files
    ds_geom = xr.open_dataset(filename_geometry)
    ds_data = xr.open_dataset(filename_data)

    # Extract mesh geometry
    vertex_x = ds_geom['vertex_x'].values
    vertex_y = ds_geom['vertex_y'].values
    face_vertices = ds_geom['face_vertices'].values  # This should be a 2D array (n_faces, vertices_per_face)

    # Setup the plot
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)  # Make space for the slider
    ax.set_title('Mesh Data over Time')
    ax.set_aspect('equal')

    # Prepare polygons for each face
    polygons = []
    for face in face_vertices:
        # Filter out invalid vertex indices (-1 for missing vertices in padded array)
        valid_vertices = face[face >= 0]
        polygons.append([(vertex_x[v], vertex_y[v]) for v in valid_vertices])

    # Determine global min and max values for face data across all time steps
    global_min = ds_data['face_data'].min().values
    global_max = ds_data['face_data'].max().values

    # Initial plot with the first time step's data
    face_data = ds_data['face_data'].isel(time=0).values
    collection = mcoll.PolyCollection(polygons, array=face_data, cmap='viridis', edgecolors='face')
    collection.set_clim([global_min, global_max])  # Set fixed color limits
    ax.add_collection(collection)
    ax.autoscale()

    # Add color bar
    cbar = plt.colorbar(collection, ax=ax)
    cbar.set_label('Face Data Value')

    # Slider setup
    slider_ax = plt.axes([0.2, 0.1, 0.65, 0.03])  # Position for the slider
    time_slider = Slider(
        ax=slider_ax, 
        label='Time Step', 
        valmin=0, 
        valmax=len(ds_data.time)-1,  # Ensure the max value matches the number of time steps
        valinit=0, 
        valfmt='%0.0f', 
        valstep=60)  # This makes the slider snap to discrete values


    # Update function for the slider
    def update(val):
        # Update the face data based on the slider's position (time step)
        step = int(time_slider.val)
        new_face_data = ds_data['face_data'].isel(time=step).values

        # Update the collection's face colors
        collection.set_array(new_face_data)
        fig.canvas.draw_idle()

    # Call the update function when the slider value is changed
    time_slider.on_changed(update)

    plt.show()

    # Close the datasets
    ds_geom.close()
    ds_data.close()

def create_geometry_netcdf(mesh_vertices, mesh_faces, output_filename):
    # Prepare data arrays
    vertex_x = [coords[0] for coords in mesh_vertices.values()]
    vertex_y = [coords[1] for coords in mesh_vertices.values()]

    # Ensure face_vertices have consistent dimensions
    nmax_face = 3  # Assuming always 3 vertices per face for a triangular mesh
    face_vertices_array = np.full((len(mesh_faces), nmax_face), -1, dtype=int)  # Initialize with -1

    for i, (face_id, vertex_ids) in enumerate(mesh_faces.items()):
        # Subtract one to convert from one-based to zero-based indexing
        face_vertices_array[i, :] = np.array(vertex_ids) - 1

    # Create xarray Dataset for mesh geometry
    geometry_ds = xr.Dataset(
        {
            "vertex_x": (("vertex",), vertex_x),
            "vertex_y": (("vertex",), vertex_y),
            "face_vertices": (("face", "nmax_face"), face_vertices_array),
        },
        coords={
            "vertex": np.arange(len(mesh_vertices)),
            "face": np.arange(len(mesh_faces)),
            "nmax_face": np.arange(nmax_face),
        }
    )

    # Set global attributes for the geometry dataset
    geometry_ds.attrs = {
        "Conventions": "UGRID-1.0",
        "title": "UGRID Geometry compliant NetCDF file",
        "institution": "IST",
        "source": "JB script",
        "references": "Barreiro (2024)",
        "history": "Created " + np.datetime_as_string(np.datetime64('now'), unit='m'),
        "mesh_type": "faces",
        "data_type": "vertices",
        "is_vector": "False",
    }

    # Optionally add CRS information
    geometry_ds["crs"] = xr.DataArray(1)  # Dummy variable for CRS
    geometry_ds["crs"].attrs = {
        "long_name": "WGS 84 / Pseudo-Mercator",
        "epsg_code": "EPSG:3857",
        # Add more CRS attributes as needed
    }

    # Save geometry to NetCDF file
    geometry_ds.to_netcdf(output_filename, format="NETCDF3_CLASSIC", engine="netcdf4")
    print(f'UGRID Geometry NetCDF file {output_filename} created successfully.')

def write_DAT_file(mesh_nodes, mesh_faces, datasets, filepath):
    
    with open(filepath, "w") as file:
        
        # Initial dataset information
        file.write("DATASET\n")
        file.write('OBJTYPE "mesh2d"\n')
        file.write("RT_JULIAN 2433282.500000\n")  # Example Julian date

        for dataset in datasets:
            dataset_name, data_series, timestamps = dataset['name'], dataset['data_series'], dataset['timestamps']

            # Write dataset header
            file.write("BEGSCL\n")
            file.write(f"ND {len(mesh_nodes)}\n")  # Number of vertices
            file.write(f"NC {len(mesh_faces)}\n")  # Number of faces
            file.write(f'NAME "{dataset_name}"\n')  # Dataset name
            file.write("TIMEUNITS Seconds\n")

            # Write data for each timestamp
            if len(timestamps) == 1:
                file.write(f"TS 0\t{timestamps[0]}\n")
                for node_data in data_series:
                    file.write(f"{node_data:.5f}\n")
            else:    
                for idx, ts in enumerate(timestamps):
                    file.write(f"TS 0\t{ts}\n")  # Write timestamp     
                    for node_data in data_series[idx]:
                        file.write(f"{node_data:.5f}\n")  # Write data for each node at this timestamp

            # Write end of dataset
            file.write("ENDDS\n")

    print(f"{filepath} file created successfully.")

def get_critical_nodes(file):
    with open(file, "r") as f:
        lines = f.readlines()
    
    clean_lines = [line.strip() for line in lines]
    return clean_lines

def main(Window: tool_GUI):
    print("\n\n\n START")
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    #critical_nodes = get_critical_nodes(r"C:\Users\joaop\OneDrive\Documentos\TESE_JL_BASEMENT_SIG\CRITICAL_NODES.txt")
    
    Mesh_faces, Mesh_nodes, Mesh_faces_area, Mesh_faces_centroids = read_2dm(Window.MeshFile)
    # Mesh_vertices_idw = calcualte_vertices_idw_weights(Mesh_faces, Mesh_faces_centroids, Mesh_nodes)

    #Mesh_nodes = {node_id: coords for node_id, coords in Mesh_nodes.items() if node_id in critical_nodes}
    
    depth_file = Window.DepthFile
    velocity_file = Window.VelocityFile

    element_based = "vertices"
    
    print("Reading depth file...")
    depth_file_contents = get_file_lines(depth_file)
    depth_results, depth_timeunits, depth_timeseries, ND, NC = getData(depth_file_contents)
    
    print("Reading velocity file...")
    velocity_file_contents = get_file_lines(velocity_file)
    velocity_results, velocity_timeunits, velocity_timeseries, _, _ = getData(velocity_file_contents)

    print("Resampling data file times...")
    # Resample time series to fixed dt (interpolating series)    
    #timestamps, nodes_depth_series = resample_timeseries(depth_timeseries, depth_results, dt=60) #assuming time units as secods
    #_, nodes_velocity_series = resample_timeseries(velocity_timeseries, velocity_results, dt=60)
    
    nodes_depth_series = depth_results
    nodes_velocity_series = velocity_results
    
    timestamps = depth_timeseries
    
    print("Calculating momentum...")
    nodes_momentum_series = nodes_depth_series * nodes_velocity_series

    base_name, extension = os.path.splitext(os.path.basename(Window.DepthFile))
    path = os.path.dirname(Window.DepthFile)

    datasets_to_write = [
        {"name": "my_Depth", "data_series": nodes_depth_series, "timestamps" : timestamps}            
    ]
    
    writing_path = os.path.join(path, f'{base_name}_my_Depth.DAT')
    
    write_DAT_file(Mesh_nodes,
                    Mesh_faces,
                    datasets_to_write,
                    filepath = writing_path)


    ''' 
    #create_basic_netcdf(Mesh_nodes, Mesh_faces, "Mesh_ugrid.nc")
   
    #convert_centroidseries_to_vector(Mesh_faces, Mesh_nodes, centroids_depth_series, timestamps, "Mesh_faces_depth_vector")
    
    # create_geometry_netcdf(Mesh_nodes, Mesh_faces, "mesh_faces.nc")
    # create_data_netcdf(centroids_depth_series, timestamps, "mesh_faces_depth.nc")   
    # interactive_mesh_plot("mesh_faces.nc", "mesh_faces_depth.nc")'''
   
    # print("Resampling series to mesh centroids...")
    # # centroids_depth_series = calculate_centroid_idw_timeseries(Mesh_faces, Mesh_vertices_idw, nodes_depth_series)
    # centroids_velocity_series = calculate_centroid_idw_timeseries(Mesh_faces, Mesh_vertices_idw, nodes_velocity_series)
    # centroids_momentum_series = calculate_centroid_idw_timeseries(Mesh_faces, Mesh_vertices_idw, nodes_momentum_series)    

    # #calculate the minimum and maximum momentum at each node
    # min_momentum = np.min(centroids_momentum_series, axis=0)
    # max_momentum = np.max(centroids_momentum_series, axis=0)
    
    # #find the time index of the max_momentum at each node
    # max_momentum_index = np.argmax(centroids_momentum_series, axis=0)
    # #get the respecrive node depth at that index
    # max_momentum_depth = centroids_depth_series[max_momentum_index]


    
    #get the depth file name , wihtout path
    GUI.ui.textEdit.append(f'Calculating indicators from {os.path.basename(depth_file)}...')
    if Window.SFP:
        print("Calculating SFP...")
                
        mean_node_SFP, nodes_SFP_values = calculate_depth_performance(timestamps, nodes_depth_series, Window.MinorThresh, Window.MajorThresh)
    
        datasets_to_write = [
            {"name": "nodes_SFP_values", "data_series": nodes_SFP_values, "timestamps" : [0]}            
        ]
        
        writing_path = os.path.join(path, f'{base_name}_MSF_nodes.DAT')
        
        write_DAT_file(Mesh_nodes,
                       Mesh_faces,
                       datasets_to_write,
                       filepath = writing_path)
        
        #mean_SFP, centroids_FP_values= calculate_depth_performance(timestamps, centroids_depth_series, Window.MinorThresh, Window.MajorThresh)
        #mesh_weighted_SFP = calculate_mesh_areaweighted_value(centroids_FP_values, Mesh_faces_area)
                
        #GUI.ui.textEdit.append(f'Surface flooding performance Resilience = {mesh_weighted_SFP:.3f}')

        #export_attributes_to_faces(Mesh_faces, Mesh_nodes, {"SFP": centroids_FP_values}, "Faces_SFP")
          
    if Window.IHP:
        print("Calculating IHP...")
        method = Window.ui.UHP_comboBox.currentText().split(",")[0]
        
        mean_node_IHP, nodes_IHP_series, nodes_IHP_weighted, nodes_IHP_worst = calculate_IHP_at_nodes(nodes_depth_series, nodes_velocity_series, method)

        datasets_to_write = [
            {"name": "nodes_IHP_series", "data_series": nodes_IHP_series, "timestamps" : timestamps},
            {"name": "nodes_IHP_weighted", "data_series": nodes_IHP_weighted, "timestamps" : [0]},
            {"name": "nodes_IHP_worst", "data_series": nodes_IHP_worst, "timestamps" : [0]}
        ]
        writing_path = os.path.join(path, f'{base_name}_IHP_nodes.DAT')
        write_DAT_file(Mesh_nodes,
                    Mesh_faces,
                    datasets_to_write,
                    filepath = writing_path)
        
        
        print("\n IHP files writen with success!")
        # mean_IHP, centroids_IHP_value, lowest_IHP_at_nodes = calculate_IHP_at_nodes(centroids_depth_series, centroids_velocity_series, method)
        # mesh_weighted_IHP = calculate_mesh_areaweighted_value(centroids_IHP_value, Mesh_faces_area)
        # lowest_weighted_IHP = calculate_mesh_areaweighted_value(lowest_IHP_at_nodes, Mesh_faces_area)
        
        # GUI.ui.textEdit.append(f'Indicator of Hazard to Pedestrians = {mesh_weighted_IHP:.3f}')
        # GUI.ui.textEdit.append(f'Lowest Indicator of Hazard to Pedestrians = {lowest_weighted_IHP:.3f}')

        #export_attributes_to_faces(Mesh_faces, Mesh_nodes, {"IHP": centroids_IHP_value, "WorstIHP": lowest_IHP_at_nodes}, "Faces_IHP")

    if Window.IHV:
        print("Calculating IHV...")
        
        mean_nodes_hazard_indicator, nodes_IHV_series, nodes_IHV_weighted, nodes_IHV_worst = calculate_IHV_at_nodes(nodes_depth_series, nodes_momentum_series)

        datasets_to_write = [
            {"name": "nodes_IHV_series", "data_series": nodes_IHV_series, "timestamps" : timestamps},
            {"name": "nodes_IHV_weighted", "data_series": nodes_IHV_weighted, "timestamps" : [0]},
            {"name": "nodes_IHV_worst", "data_series": nodes_IHV_worst, "timestamps" : [0]}
        ]
        writing_path = os.path.join(path, f'{base_name}_IHV_nodes.DAT')
        write_DAT_file(mesh_nodes = Mesh_nodes,
                       mesh_faces = Mesh_faces,
                       datasets =  datasets_to_write,
                       filepath = writing_path)
         
        # mesh_weighted_IHV = calculate_mesh_areaweighted_value(centroids_IHV_values, Mesh_faces_area)
        # lowest_weighted_IHV = calculate_mesh_areaweighted_value(lowest_IHV_at_nodes, Mesh_faces_area)
        
        # GUI.ui.textEdit.append(f'Indicator of Hazard to Vehicles = {mesh_weighted_IHV:.3f}')
        # GUI.ui.textEdit.append(f"Lowest Indicator of Hazard to Vehicles = {lowest_weighted_IHV:.3f}")

        # export_attributes_to_faces(Mesh_faces, Mesh_nodes, {"IHV": centroids_IHV_values, "WorstIHV": lowest_IHV_at_nodes}, "Faces_IHP")
        print("\n IHV files writen with success!")
        
    GUI.ui.textEdit.append(f'DONE!')   
    print("Run finished!")
    #PRINT time of finish
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    return 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    GUI = tool_GUI()
    GUI.Proceed.connect(lambda: main(GUI))
    
    GUI.show()
        
    sys.exit(app.exec())