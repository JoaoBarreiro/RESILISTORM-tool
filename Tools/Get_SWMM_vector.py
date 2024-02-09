from pyswmm import Output
from swmm.toolkit.shared_enum import NodeAttribute, LinkAttribute
import numpy as np
import swmmio
import geopandas as gpd
from shapely.geometry import Point, LineString
from datetime import datetime



#1. Extract Data from the SWMM Output File

# Specify your output file and the time index you're interested in
# Time index needs to be in the range of the simulation times
output_file = r"F:\IST\PhD\Case Studies\JL\MODELOS\ATUAL\SWMM\100anos.out"

node_flooding = {}
conduit_capacity = {}

time = datetime(2014, 9, 22, 2, 30) 

with Output(output_file) as out:
    # Get the index for flooding and capacity
    nodes_flooding = out.node_attribute(NodeAttribute.FLOODING_LOSSES, time)
    links_capacity = out.link_attribute(LinkAttribute.CAPACITY, time)


#2 . Read the SWMM Input File for Geospatial Data
model = swmmio.Model(r"F:\IST\PhD\Case Studies\JL\MODELOS\ATUAL\SWMM\100anos.INP")
nodes_df = model.inp.coordinates
conduits_df = model.inp.conduits

#3. Merge Simulation Results with Geospatial Data
nodes_df['Flooding'] = nodes_df['InvertElev'].map(node_flooding)  # Use a unique identifier, like InvertElev, if node IDs are not directly available
conduits_df['Capacity'] = conduits_df['Geom1'].map(conduit_capacity)  # Use a unique identifier, like Geom1, if conduit IDs are not directly available

#4.  Convert DataFrames to GeoDataFrames and Export to GPKG

# Convert node DataFrame to GeoDataFrame
gdf_nodes = gpd.GeoDataFrame(nodes_df, geometry=gpd.points_from_xy(nodes_df.XCoord, nodes_df.YCoord))

# For conduits, create LineStrings from the start and end node coordinates
gdf_conduits = gpd.GeoDataFrame(conduits_df)
gdf_conduits['geometry'] = gdf_conduits.apply(lambda row: LineString([
    (nodes_df.loc[row['InletNode'], 'XCoord'], nodes_df.loc[row['InletNode'], 'YCoord']),
    (nodes_df.loc[row['OutletNode'], 'XCoord'], nodes_df.loc[row['OutletNode'], 'YCoord'])
]), axis=1)

# Export to GPKG
gdf_nodes.to_file("swmm_results.gpkg", layer='nodes', driver="GPKG")
gdf_conduits.to_file("swmm_results.gpkg", layer='conduits', driver="GPKG", mode='a')  # Use mode='a' to append to the same file
