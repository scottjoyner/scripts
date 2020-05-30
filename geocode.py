import requests, json
from requests.exceptions import HTTPError
import math
import logging
from matplotlib import pyplot as plt
import http.client as http_client
import urllib

# urllib.urlretrieve('ftp://server/path/to/file', 'file')


# def downloadFile(url):
# 	urllib.urlretrieve(url)
# url = "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/LPC/projects/NC_MecklenburgCo_2007/las/tiled/NC_MecklenburgCo_2007_000603.zip"

# downloadFile(url)
# http_client.HTTPConnection.debuglevel = 0

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?SingleLine=5317%20Addington%20Ct%20Charlotte%20NC&locationType=rooftop&sourceCountry=USA&maxLocations=1&outFields=*&f=pjson

# https://viewer.nationalmap.gov/tnmaccess/api/products?datasets=Lidar+Point+Cloud+%28LPC%29&bbox=-80.7800815%2C35.034299%2C-80.7780815%2C35.036299&q=&dateType=dateCreated&start=&end=&polyCode=&polyType=&offset=&max=&outputFormat=JSON&version=1&_csrf=793285aa-e367-451e-9703-41514effa09e
def geocode(address, locations=1):
	payload = {
        'SingleLine': address,
        'locationType': 'rooftop',
        'sourceCountry': 'USA',
        'maxLocations': locations,
        'outFields':'*',
        'f':'pjson',
    }
	response = requests.get('https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?', params=payload)
	geocode_dictionary = json.loads(response.text)
	print(geocode_dictionary['candidates'][0]['address'])
	print(geocode_dictionary['candidates'][0]['extent'])
	return geocode_dictionary



def findPointCloud(extent, format='LAS,LAZ'):
	payload = {
		'datasets': 'Lidar Point Cloud (LPC)',
		'bbox': str(extent['xmin']) + ',' + str(extent['ymin']) + ',' + str(extent['xmax']) + ',' + str(extent['ymax']),
		'q': '',
		'prodFormats': format,
		'prodExtents': '',
		'dateType': 'dateCreated',
		'start': '',
		'end': '',
		'polyCode': '',
		'polyType': '',
		'offset': '',
		'max': '',
		'outputFormat': 'JSON',
		'version': '1',
		'_csrf': '95af3dcf-8483-4fd0-942f-e1499457515a',
	}
	print(payload['bbox'])
	try:
		response = requests.get('https://viewer.nationalmap.gov/tnmaccess/api/products?', params=payload)
	except HTTPError as e:
		print("Something went wrong")
	print(response.status_code)
	dataset_lists_dictionary = json.loads(response.text)
	# print(dataset_lists_dictionary)
	return dataset_lists_dictionary

def url(extent):

	url = "https://viewer.nationalmap.gov/tnmaccess/api/products?datasets=Lidar+Point+Cloud+%28LPC%29&bbox=-80.7800815%2C35.034299%2C-80.7780815%2C35.036299&q=&dateType=dateCreated&start=&end=&polyCode=&polyType=&offset=&max=&outputFormat=JSON&version=1&_csrf=1fabdb22-6872-42ea-b909-8078f6aaeeff"

# def listDir():
# 	response = requests.get('rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/LPC/projects/')
# 	print(response.text)

# geocode_dictionary = geocode('5317 addington Ct charlotte NC')
# pointcloud_dictionary = findPointCloud(geocode_dictionary['candidates'][0]['extent'])

# print(pointcloud_dictionary["messages"])
# for item in pointcloud_dictionary['items']:
# 	print(item['title'] + ": " + item['downloadURL'])



def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


import laspy
import scipy
import scipy.spatial
#from scipy.spatial.kdtree import KDTree
import numpy as np

# Open a file in read mode:
inFile = laspy.file.File("./home.las")
print(inFile.header.point_return_count)
print(inFile.header.scale)
print(inFile.header.global_encoding)
print(inFile.header.offset)
print(inFile.header.data_record_length)
min = np.array(inFile.header.min)
# Grab a numpy dataset of our clustering dimensions:
x = inFile.X - inFile.header.min[0]
y = inFile.Y - inFile.header.min[1]
color = inFile.Z - inFile.header.min[2]
print(color)
print(len(x))
print(len(y))
dataset = np.vstack([inFile.X, inFile.Y, inFile.Z]).transpose()
for x in dataset:
	x = np.subtract(x, min)

plt.scatter(x, y, s=5, c=color)

plt.show()
#translated_dataset = np.subtract(dataset, np.array(inFile.header.min))
# print(dataset)
# dataset.transpose()
# print(dataset)
# Build the KD Tree
# tree = scipy.spatial.kdtree(dataset[0], 5)
# This should do the same as the FLANN example above, though it might
# be a little slower.
# tree.query(dataset[100,], k = 5)
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

def preparePointCloud(extent, bbox, las_File_Path):
	inFile = laspy.file.File(las_File_Path)
	max = np.array(inFile.header.max)
	min = np.array(inFile.header.min)
	print(max)
	print(min)
	diff = np.subtract(max, min)
	diff = np.array([truncate(diff[0]), truncate(diff[1]), diff[2]])
	print(diff)
	extent_diff_x = truncate(extent['xmax'] - extent['xmin'], 7)
	extent_diff_y = truncate(extent['ymax'] - extent['ymin'], 7)
	bbox_diff_x = truncate(bbox["maxX"] - bbox["minX"], 7)
	bbox_diff_y = truncate(bbox["maxY"] - bbox["minY"], 7)
	print(extent_diff_x, extent_diff_y)
	print(extent_diff_x / diff[0])
	print(extent_diff_y / diff[1])
	print(bbox_diff_x, bbox_diff_y)
	print(bbox_diff_x / diff[0])
	print(bbox_diff_y / diff[1])
	return 0
# preparePointCloud(extent, bbox, las_File_Path)

def translatePoints():
	return 0



# Prevous version....
# def preparePointCloud(extent, bbox, las_File_Path):
# 	inFile = laspy.file.File(las_File_Path)
# 	max = np.array(inFile.header.max)
# 	min = np.array(inFile.header.min)
# 	print(max)
# 	print(min)
# 	diff = np.subtract(max, min)
# 	diff = np.array([truncate(diff[0]), truncate(diff[1]), diff[2]])
# 	print(diff)
# 	extent_diff_x = truncate(extent['xmax'] - extent['xmin'], 7)
# 	extent_diff_y = truncate(extent['ymax'] - extent['ymin'], 7)
# 	print(extent_diff_x, extent_diff_y)
# 	print(extent_diff_x / diff[0])
# 	print(extent_diff_y / diff[1])
# 	return 0
# class User:
# 	def __init__:
# 		# TODO


'''{
 "spatialReference": {
  "wkid": 4326,
  "latestWkid": 4326
 },
 "candidates": [
  {
   "address": "5317 Addington Ct, Charlotte, North Carolina, 28277",
   "location": {
    "x": -80.778955499999995,
    "y": 35.035344000000009
   },
   "score": 100,
   "attributes": {
    "Loc_name": "World",
    "Status": "M",
    "Score": 100,
    "Match_addr": "5317 Addington Ct, Charlotte, North Carolina, 28277",
    "LongLabel": "5317 Addington Ct, Charlotte, NC, 28277, USA",
    "ShortLabel": "5317 Addington Ct",
    "Addr_type": "PointAddress",
    "Type": "",
    "PlaceName": "",
    "Place_addr": "5317 Addington Ct, Charlotte, North Carolina, 28277",
    "Phone": "",
    "URL": "",
    "Rank": 20,
    "AddBldg": "",
    "AddNum": "5317",
    "AddNumFrom": "",
    "AddNumTo": "",
    "AddRange": "",
    "Side": "",
    "StPreDir": "",
    "StPreType": "",
    "StName": "Addington",
    "StType": "Ct",
    "StDir": "",
    "BldgType": "",
    "BldgName": "",
    "LevelType": "",
    "LevelName": "",
    "UnitType": "",
    "UnitName": "",
    "SubAddr": "",
    "StAddr": "5317 Addington Ct",
    "Block": "",
    "Sector": "",
    "Nbrhd": "",
    "District": "",
    "City": "Charlotte",
    "MetroArea": "",
    "Subregion": "Mecklenburg County",
    "Region": "North Carolina",
    "RegionAbbr": "NC",
    "Territory": "",
    "Zone": "",
    "Postal": "28277",
    "PostalExt": "3208",
    "Country": "USA",
    "LangCode": "ENG",
    "Distance": 0,
    "X": -80.77858560661295,
    "Y": 35.03540636135962,
    "DisplayX": -80.778955499999995,
    "DisplayY": 35.035344000000009,
    "Xmin": -80.7799555,
    "Xmax": -80.77795549999999,
    "Ymin": 35.034344000000011,
    "Ymax": 35.036344000000007,
    "ExInfo": ""
   },
   "extent": {
    "xmin": -80.7799555,
    "ymin": 35.034344000000011,
    "xmax": -80.77795549999999,
    "ymax": 35.036344000000007
   }
  }
 ]
}'''

'''
{
    "total": 5,
    "messages":
    [
        "Retrieved 5 item(s) (1 through 5)"
    ],
    "errors": [],
    "items":
    [
        {
            "title": "USGS Lidar Point Cloud (LPC) NC_MecklenburgCo_2007_000603 2014-09-16 LAS",
            "sourceId": "5826fe08e4b01fad86f1ec28",
            "sourceName": "ScienceBase",
            "sourceOriginId": "9786665",
            "sourceOriginName": "gda",
            "metaUrl": "https://www.sciencebase.gov/catalog/item/5826fe08e4b01fad86f1ec28",
            "publicationDate": "2014-09-16",
            "lastUpdated": "2018-10-05",
            "dateCreated": "2016-11-12",
            "sizeInBytes": 12137860,
            "extent": "Varies",
            "format": "LAS/LAZ",
            "downloadURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/LPC/projects/NC_MecklenburgCo_2007/las/tiled/NC_MecklenburgCo_2007_000603.zip",
            "previewGraphicURL": "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/LPC/browse/NC_MecklenburgCo_2007_000603.jpg",
            "downloadLazURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/NC_MecklenburgCo_2007/laz/NC_MecklenburgCo_2007_000603.laz",
            "datasets":
            [
                "Lidar Point Cloud (LPC)"
            ],
            "boundingBox":
            {
                "minX": -80.7875583,
                "maxX": -80.7704832,
                "minY": 35.0281416,
                "maxY": 35.042186
            },
            "bestFitIndex": 0.016679903946836567,
            "prettyFileSize": "11.58 MB"
        },
        {
            "title": "USGS Lidar Point Cloud NC Phase4 Mecklenburg 2016 LA 37 10446715 LAS 2019",
            "sourceId": "5d31fa96e4b01d82ce86ece1",
            "sourceName": "ScienceBase",
            "sourceOriginId": "13629214",
            "sourceOriginName": "gda",
            "metaUrl": "https://www.sciencebase.gov/catalog/item/5d31fa96e4b01d82ce86ece1",
            "publicationDate": "2019-07-15",
            "lastUpdated": "2019-07-19",
            "dateCreated": "2019-07-19",
            "sizeInBytes": 99430430,
            "extent": "Varies",
            "format": "LAZ",
            "downloadURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Mecklenburg_2016_LAS_2019/laz/USGS_LPC_NC_Phase4_Mecklenburg_2016_LA_37_10446715__LAS_2019.laz",
            "previewGraphicURL": "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Mecklenburg_2016_LAS_2019/browse/USGS_LPC_NC_Phase4_Mecklenburg_2016_LA_37_10446715__LAS_2019_thumb.jpg",
            "downloadLazURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Mecklenburg_2016_LAS_2019/laz/USGS_LPC_NC_Phase4_Mecklenburg_2016_LA_37_10446715__LAS_2019.laz",
            "datasets":
            [
                "Lidar Point Cloud (LPC)"
            ],
            "boundingBox":
            {
                "minX": -80.787527172,
                "maxX": -80.77902636,
                "minY": 35.0351694148,
                "maxY": 35.0419142532
            },
            "bestFitIndex": 0.006193928816048281,
            "prettyFileSize": "94.82 MB"
        },
        {
            "title": "USGS Lidar Point Cloud NC Phase4 Mecklenburg 2016 LA 37 10446716 LAS 2019",
            "sourceId": "5d31fa96e4b01d82ce86ece3",
            "sourceName": "ScienceBase",
            "sourceOriginId": "13629212",
            "sourceOriginName": "gda",
            "metaUrl": "https://www.sciencebase.gov/catalog/item/5d31fa96e4b01d82ce86ece3",
            "publicationDate": "2019-07-15",
            "lastUpdated": "2019-07-19",
            "dateCreated": "2019-07-19",
            "sizeInBytes": 112639761,
            "extent": "Varies",
            "format": "LAZ",
            "downloadURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Mecklenburg_2016_LAS_2019/laz/USGS_LPC_NC_Phase4_Mecklenburg_2016_LA_37_10446716__LAS_2019.laz",
            "previewGraphicURL": "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Mecklenburg_2016_LAS_2019/browse/USGS_LPC_NC_Phase4_Mecklenburg_2016_LA_37_10446716__LAS_2019_thumb.jpg",
            "downloadLazURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Mecklenburg_2016_LAS_2019/laz/USGS_LPC_NC_Phase4_Mecklenburg_2016_LA_37_10446716__LAS_2019.laz",
            "datasets":
            [
                "Lidar Point Cloud (LPC)"
            ],
            "boundingBox":
            {
                "minX": -80.7791760375,
                "maxX": -80.7706758992,
                "minY": 35.035292228,
                "maxY": 35.0420376516
            },
            "bestFitIndex": 0.0052945412627712195,
            "prettyFileSize": "107.42 MB"
        },
        {
            "title": "USGS Lidar Point Cloud NC Phase4 Union 2016 10446719 LAS 2019",
            "sourceId": "5d69bb6ce4b0c4f70cf2fe18",
            "sourceName": "ScienceBase",
            "sourceOriginId": "13727858",
            "sourceOriginName": "gda",
            "metaUrl": "https://www.sciencebase.gov/catalog/item/5d69bb6ce4b0c4f70cf2fe18",
            "publicationDate": "2019-07-25",
            "lastUpdated": "2019-08-30",
            "dateCreated": "2019-08-30",
            "sizeInBytes": 112805279,
            "extent": "Varies",
            "format": "LAZ",
            "downloadURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Union_2016_LAS_2019/laz/USGS_LPC_NC_Phase4_Union_2016_10446719_LAS_2019.laz",
            "previewGraphicURL": "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Union_2016_LAS_2019/browse/USGS_LPC_NC_Phase4_Union_2016_10446719_LAS_2019_thumb.jpg",
            "downloadLazURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Union_2016_LAS_2019/laz/USGS_LPC_NC_Phase4_Union_2016_10446719_LAS_2019.laz",
            "datasets":
            [
                "Lidar Point Cloud (LPC)"
            ],
            "boundingBox":
            {
                "minX": -80.7873767923,
                "maxX": -80.7788767077,
                "minY": 35.0283011732,
                "maxY": 35.0350460267
            },
            "bestFitIndex": 0.00353216395912153,
            "prettyFileSize": "107.58 MB"
        },
        {
            "title": "USGS Lidar Point Cloud NC Phase4 Union 2016 10446720 LAS 2019",
            "sourceId": "5d69bb6ce4b0c4f70cf2fe1b",
            "sourceName": "ScienceBase",
            "sourceOriginId": "13727861",
            "sourceOriginName": "gda",
            "metaUrl": "https://www.sciencebase.gov/catalog/item/5d69bb6ce4b0c4f70cf2fe1b",
            "publicationDate": "2019-07-25",
            "lastUpdated": "2019-08-30",
            "dateCreated": "2019-08-30",
            "sizeInBytes": 145795031,
            "extent": "Varies",
            "format": "LAZ",
            "downloadURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Union_2016_LAS_2019/laz/USGS_LPC_NC_Phase4_Union_2016_10446720_LAS_2019.laz",
            "previewGraphicURL": "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Union_2016_LAS_2019/browse/USGS_LPC_NC_Phase4_Union_2016_10446720_LAS_2019_thumb.jpg",
            "downloadLazURL": "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/USGS_LPC_NC_Phase4_Union_2016_LAS_2019/laz/USGS_LPC_NC_Phase4_Union_2016_10446720_LAS_2019.laz",
            "datasets":
            [
                "Lidar Point Cloud (LPC)"
            ],
            "boundingBox":
            {
                "minX": -80.7790263566,
                "maxX": -80.770526949,
                "minY": 35.0284239733,
                "maxY": 35.0351694121
            },
            "bestFitIndex": 0.0029493260512802066,
            "prettyFileSize": "139.04 MB"
        }
    ]
}
'''
