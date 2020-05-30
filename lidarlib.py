


# Input: Address in a single line string that can be geocoded
# Returns: Dictionary of the info about the address
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
	return geocode_dictionary


# Input: extent bounding box of the search for an availible pointcloud 
# Returns: Output is a dictionary listing the posible datasets that can be downloaded
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
	dataset_lists_dictionary = json.loads(response.text)
	return dataset_lists_dictionary