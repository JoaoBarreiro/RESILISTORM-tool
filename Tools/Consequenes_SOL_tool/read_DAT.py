import numpy as np
from datetime import datetime

import glob
import os
from SOL_tool import read_2dm, calculate_mesh_areaweighted_timeseries, calculate_mesh_areaweighted_value

def read_DAT_data(filepath):
    settings = {}
    vertices_timeseries = []
    faces_timeseries = []
    timestamps = []

    with open(filepath, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            setting = line.split()

            if line.startswith("BEGSCL"):
                settings["data_type"] = "scalar"
            elif line.startswith("BEGVEC"):
                settings["data_type"] = "vector"
            elif line.startswith("ND"):
                settings["ND"] = int(setting[1])  # Nr of Vertices
            elif line.startswith("NC"):
                settings["NC"] = int(setting[1])  # Nr of Faces
            elif line.startswith("RT_JULIAN"):
                settings["start_date"] = float(setting[1])
            elif line.startswith("TIMEUNITS"):
                settings["time_units"] = setting[1]
            elif line.startswith("TS"):
                timestamps.append(float(setting[2]))  # Assuming the 3rd element is the timestamp
                i += 1  # Skip to the next line for vertices values
                current_vertices = []
                for _ in range(settings["ND"]):
                    vertice_value = float(lines[i].strip().split()[0])  # Assuming value is the first element in the line
                    current_vertices.append(vertice_value)
                    i += 1

                vertices_timeseries.append(current_vertices)

                current_faces = []
                for _ in range(settings["NC"]):
                    face_value = float(lines[i].strip().split()[0])  # Assuming value is the first element in the line
                    current_faces.append(face_value)
                    i += 1

                faces_timeseries.append(current_faces)

                continue  # Skip the increment at the end of the loop to handle the next line correctly
            elif line.startswith("ENDDS"):
                break  # Stop reading further as the time series data ends

            i += 1  # Move to the next line

    # Convert lists to numpy arrays
    vertices_timeseries = np.array(vertices_timeseries)
    faces_timeseries = np.array(faces_timeseries)
    timestamps = np.array(timestamps)

    return settings, vertices_timeseries, faces_timeseries, timestamps

def calculate_IHP_from_DAT(faces_area, faces_timeseries, timestamps, method = "Defra"):
    
    if method == "Defra":
        
        HR = faces_timeseries
        CV = [0.75, 1.25, 2]
        IHP = [1.0, 0.53, 0.21, 0.00]  #basically its a weight of each class

        # Initialize arrays to store results
        IHP_at_faces = np.zeros(HR.shape[1])  # Array to hold IHP for each face
        lowest_IHP_at_faces = np.zeros(HR.shape[1])  # Array to hold lowest IHP for each face
        faces_weight_series = []
        
        # Loop over each face's HR time series
        for i, face_hr_serie in enumerate(HR.T):
            # Initialize arrays for class and weight series for the current face
            face_hazardclass_serie = np.zeros_like(face_hr_serie)
            face_weight_serie = np.zeros_like(face_hr_serie)
            
             # Classify HR values and assign weights
            for j, hr_value in enumerate(face_hr_serie):
                if hr_value <= CV[0]:
                    face_hazardclass_serie[j] = 0  # Class index for CW[0]
                    face_weight_serie[j] = IHP[0] # Assign corresponding weight
                elif hr_value <= CV[1]:
                    face_hazardclass_serie[j] = 1  # Class index for CW[1]
                    face_weight_serie[j] = IHP[1]
                elif hr_value <= CV[2]:
                    face_hazardclass_serie[j] = 2  # Class index for CW[2]
                    face_weight_serie[j] = IHP[2]
                else:
                    face_hazardclass_serie[j] = 3  # Class index for CW[3]
                    face_weight_serie[j] = IHP[3]
                    
            # Store the weight series for the current face
            faces_weight_series.append(face_weight_serie)

            # Find the lowest IHP value for the current face
            lowest_IHP_at_faces[i] = np.min(face_weight_serie)
            
            #ASSUMING CONSTANT DT
            # Count occurrences in each class
            class_counts = np.bincount(face_hazardclass_serie.astype(int), minlength=len(IHP))
            # Calculate the proportions of time spent in each class
            proportions = class_counts / len(face_hr_serie)
            # Calculate IHP for the face by multiplying the proportion of time in each class with the corresponding class weight
            IHP_at_faces[i] = np.dot(proportions, IHP)
            
        #calculate the IHP as the weighted area with the area of each face in the 
        IHP = calculate_mesh_areaweighted_value(IHP_at_faces, faces_area)
        lowest_IHP = calculate_mesh_areaweighted_value(lowest_IHP_at_faces, faces_area)
    
    return IHP_at_faces, lowest_IHP_at_faces, IHP, lowest_IHP


# def find_worst_timestamp(faces_timeseries, faces_area):
#     # Calculate the total area of the mesh
#     total_area = np.sum(faces_area)
    
#     # Calculate weighted HR for each face at each time step
#     weighted_timeseries = faces_timeseries * faces_area[:, np.newaxis]

#     # Sum the weighted HR values for all faces at each time step to get the total weighted HR for the mesh
#     total_weighted_per_timestep = np.sum(weighted_timeseries, axis=0)

#     # Divide by total area to get the average weighted HR time series for the mesh
#     average_weighted_HR_per_timestep = total_weighted_per_timestep / total_area

#     # Find the time stamp with the highest average weighted HR
#     worst_time_index = np.argmax(average_weighted_HR_per_timestep)
    
#     return worst_time_index, np.max(average_weighted_HR_per_timestep)

def main ():
    
    #1. Get the .2dm file existent in the folder
    print(f'\n STARTING at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    
    def get_file(extension):
        file_path = glob.glob(extension)
        if file_path:
            return file_path[0]
        else:
            return None
        
    # Call the function to get the .2dm file
    two_dm_file = get_file("Tools/Consequenes_SOL_tool/*.2dm")
    if two_dm_file:
        print("Found .2dm file:", two_dm_file)
    else:
        print("No .2dm file found in the folder.")

    # Call the function to get the .dat file
    dat_file = get_file("Tools/Consequenes_SOL_tool/*.dat")
    if dat_file:
        print("Found .dat file:", dat_file)
    else:
        print("No .dat file found in the folder.")

    
    print("Reading .2dm file...")
    faces, nodes, faces_area, faces_centroids = read_2dm(two_dm_file)
    print("Reading .dat file...")
    settings, vertices_timeseries, faces_timeseries, timestamps = read_DAT_data(dat_file)

    print("Calculating IHP...")
    #from faces_timeseries and  timestamps use calculate_IHP_at_nodes()
    IHP_at_faces, lowest_IHP_at_faces, IHP, lowest_IHP = calculate_IHP_from_DAT(faces_area, faces_timeseries, timestamps, method = "Defra")
    
    # worst_time_index, worst_hr = find_worst_timestamp(faces_timeseries, faces_area)
    # find_worst_timestamp(faces_timeseries, faces_area)
    
    #get file name for input file directory using os
    inputfilename = os.path.basename(dat_file)

    #export IHP_at_faces and lowest_IHP_at_faces to DAT file
    print(f"\n SUCESS DATA READ FOR {inputfilename}")
    print(f"IHP: {IHP}")
    print(f"Worst IHP: {lowest_IHP}")
    print(f'\n FINISH at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')


if __name__ == "__main__":
    main()