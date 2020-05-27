import math
import laspy
import scipy
import scipy.spatial
import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg as LA
from math import radians, cos, sin, asin, sqrt
import networkx as nx

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def dist(x1, y1, x2, y2):
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def preparePointCloud(extent, bbox, las_File_Path, latlng, radius):
	print("Reading in file...")
	inFile = laspy.file.File(las_File_Path)
	scale = np.array(inFile.header.scale)
	max = np.array(inFile.header.max)
	min = np.array(inFile.header.min)
	diff = np.subtract(max, min)
	diff = np.array([truncate(diff[0]), truncate(diff[1]), diff[2]])

	extent_diff_x = truncate(extent['xmax'] - extent['xmin'], 7)
	extent_diff_y = truncate(extent['ymax'] - extent['ymin'], 7)

	bbox_diff_x = truncate(bbox["maxX"] - bbox["minX"], 7)
	bbox_diff_y = truncate(bbox["maxY"] - bbox["minY"], 7)

	bbox_transpose = np.array([bbox_diff_x, bbox_diff_y, 1])
	bbox_transpose_zero = np.array([bbox_diff_x, bbox_diff_y, 0])
	translate_lat_lng = np.array([bbox["minX"], bbox["minY"], 0])

	x_pos = truncate(bbox["maxX"] - latlng["X"], 7)
	y_pos = truncate(bbox["maxY"] - latlng["Y"], 7)

	x_ratio = x_pos / bbox_diff_x
	y_ratio = y_pos / bbox_diff_y

	x_translated_point = x_ratio * diff[0]
	y_translated_point = y_ratio * diff[1]

	dataset = np.vstack([inFile.X, inFile.Y, inFile.Z]).transpose()
	point = np.array([latlng["X"], latlng["Y"], 0])

	filtered_Points = []
	for x in dataset:
		x = np.multiply(x, scale)
		x = np.subtract(x, min)
		d = dist(x[0], x[1], x_translated_point, y_translated_point)
		if d < radius:
			filtered_Points.append(x)
	return np.vstack(filtered_Points)






latlng = {
"X": -80.77858560661295,
"Y": 35.03540636135962
}

bbox = {
"minX": -80.7875583,
"maxX": -80.7704832,
"minY": 35.0281416,
"maxY": 35.042186
}

extent = {
'xmin': -80.7799555, 
'ymin': 35.03434400000001, 
'xmax': -80.77795549999999, 
'ymax': 35.03634400000001
}

las_File_Path = "./home.las"
radius = 100
points = preparePointCloud(extent, bbox, las_File_Path, latlng, radius)

listed_points = points.transpose()

# 2D graph of nodes
# plt.scatter(listed_points[0], listed_points[1], s=5, c=listed_points[2])
# plt.show()
class Point:
	def __init__(point, dist):
		self.X = point[0]
		self.Y = point[1]
		self.Z = point[2]
		self.distance = dist
		

graph = nx.Graph()

for x in listed_points:
	graph.add_node(x)

nn = nx.k_nearest_neighbors(graph)
print(nn)

# if x[0] == 0:
# 			print()
# 			x = np.divide(np.array([0, bbox_diff_y, 1]), x)
# 		elif x[1] == 0:
# 			x = np.divide(np.array([bbox_diff_x, 0, 1]), x)
# 		elif x[2] == 0:
# 			x = np.divide(np.array([bbox_diff_x, bbox_diff_y, 0]), x)
# 		x = np.divide(bbox_transpose, x)
# 		x = np.add(x, translate_lat_lng)
# 		filtered_Points = np.vstack(filtered_Points)




