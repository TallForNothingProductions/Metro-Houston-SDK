#Written By Nile Dixon
#Description: This is a library for receiving data from the Metro Houston API 
#Dependencies: requests, json

import requests
import json

class MetroArrival:
	def __init__(self, data):
		self.localArrivalTime = data['LocalArrivalTime']
		self.localTripStartTime = data['LocalTripStartTime']
		self.status = data['Status']
		self.confidenceLevel = data['ConfidenceLevel']
		self.delaySeconds = data['DelaySeconds']
		self.arrivalId = data['ArrivalId']
		self.frequency = data['Frequency']
		self.localTripEndTime = data['LocalTripEndTime']
		self.direction = data['Direction']
		self.destinationStopId = data['DestinationStopId']
		self.stopSequence = data['StopSequence']
		self.stopId = data['StopId']
		self.routeName = data['RouteName']
		self.stopName = data['StopName']
		self.tripId = data['TripId']
		self.localDepartureTime = data['LocalDepartureTime']
		self.arrivalTime = data['ArrivalTime']
		self.isRealTime = data['IsRealTime']
		self.destinationName = data['DestinationName']
		self.routeId = data['RouteId']
		self.serviceDate = data['ServiceDate']
		self.destinationStopName = data['DestinationStopName']
		self.vehicleId = data['VehicleID']
		self.scheduledTime = data['ScheduledTime']
		self.utcDepartureTime = data['UtcDepartureTime']
		self.utcArrivalTime = data['UtcArrivalTime']
		self.routeType = data['RouteType']


#This is a class to hold and access data on each Metro Vehicle
class MetroVehicle:
	def __init__(self, data):
		self.block = data['Block']
		self.tripStartTimeUTC = data['TripStartTimeUTC']
		self.tripId = str(data['TripId'])
		self.vehicleId = str(data['VehicleId'])
		self.agencyId = str(data['AgencyId'])
		self.vehicleReportTime = str(data['VehicleReportTime'])
		self.routeName = str(data['RouteName'])
		self.destinationName = str(data['DestinationName'])
		self.routeId = str(data['RouteId'])
		self.latitude = float(data['Latitude'])
		self.directionName = str(data['DirectionName'])
		self.longitude = str(data['Longitude'])
		self.delaySeconds = int(data['Delayseconds'])
		self.tripStartTimeLocal = str(data['TripStartTimeLocal'])
		self.tripEndTimeLocal = str(data['TripEndTimeLocal'])
		self.isMonitored = data['IsMonitored']
		self.tripEndTimeUTC = data['TripEndTimeUTC']

#This is a class to hold and access data on each Metro Incident
class MetroIncident:
	def __init__(self, data):
		self.status = data['Status']
		self.emergencyText = data['EmergencyText']
		self.delay = data['Delay']
		self.duration = data['Duration']
		self.affectedTo = data['AffectedTo']
		self.affectedFrom = data['AffectedFrom']
		self.type = data['Type']
		self.id = data['Id']
		self.description = data['Description']

class MetroRoute:
	def __init__(self, data):
		self.name = str(data['RouteName'])
		self.id = str(data['RouteId'])
		self.longName = str(data['LongName'])
		self.type = str(data['RouteType'])

class MetroItinerary:
	def __init__(self, data):
		self.id = str(data['ItineraryId'])
		self.created = data['Created']
		self.startTime = data['StartTime']
		self.endTime = data['EndTime']
		self.adjustedStartTime = data['AdjustedStartTime']
		self.adjustedEndTime = data['AdjustedEndTime']
		self.startStopName = str(data['StartStopName'])
		self.endStopName = str(data['EndStopName'])
		self.startStopId = str(data['StartStopId'])
		self.endStopId = str(data['EndStopId'])
		self.startAddress = str(data['StartAddress'])
		self.endAddress = str(data['EndAddress'])
		self.transferCount = int(data['TransferCount'])
		self.travelTypes = str(data['TravelTypes']).split(",")
		self.walkDistance = float(data['WalkDistance'])
		self.startLon = float(data['StartLon'])
		self.startLat = float(data['StartLat'])
		self.endLon = float(data['EndLon'])
		self.endLat = float(data['EndLat'])
		self.legs = []
		for leg in data['Legs']['results']:
			self.legs.append(MetroLeg(leg))

#This class is to hold te data of each leg in an itinerary
class MetroLeg:
	def __init__(self, data):
		self.itineraryLegId = str(data['ItineraryLegId'])
		self.created = str(data['Created'])
		self.stopName = str(data['StopName'])
		self.stopId = str(data['StopId'])
		self.routeId = str(data['RouteId'])
		self.routeName = str(data['RouteName'])
		self.directionId = str(data['DirectionId'])
		self.directionName = str(data['DirectionName'])
		self.startTime = str(data['StartTime'])
		self.adjustedStartTime = str(data['AdjustedStartTime'])
		self.duration = int(data['Duration'])
		self.length = float(data['Length'])
		self.address = str(data['Address'])
		self.transportType = str(data['TransportType'])
		self.itineraryId = str(data['ItineraryId'])
		self.lat = float(data['Lat'])
		self.lon = float(data['Lon'])
		self.tripId = str(data['TripId'])

class MetroStop:
	def __init__(self, data):
		self.name = str(data['Name'])
		self.lon = float(data['Lon'])
		self.lat = float(data['Lat'])
		self.stopId = str(data['StopId'])
		self.stopCode = str(data['StopCode'])


class Metro:
	#This is the initialization function that sets the API key for future requests
	def __init__(self, api_key):
		self.api_key = api_key

	#This function is the main function to help users 
	def get(self, route, data = {}):
		route_list = {
			'Calculate Itinerary Arriving At' : 'getItineraryArrivingAt',
			'Incidents' : 'getIncidents',
			'Routes' : 'getRoutes',
			'Routes ID' : 'getRoutesId',
			'Routes ID Arrivals' : 'getRoutesIdArrivals',
			'Routes ID Stops' : 'getRoutesStops',
			'Stops' : 'getStops',
			'Stops ID' : 'getStopsId',
			'Stops ID Arrivals' : 'getStopsArrivals',
			'Stops ID Routes' : 'getStopsRoutes',
			'Vehicles' : 'getVehicles'
		}

		return getattr(self, route_list[route])(data)

	#This function returns thr itineraries given two points
	def getItineraryArrivingAt(self, data = {}):
		url = "https://api.ridemetro.org/data/CalculateItineraryArrivingAt?$format=json&$expand=Legs&subscription-key="+ self.api_key
		for key in data.keys():
			url = url + "&" + str(key) + "=" + str(data[key])
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroItinerary(x))
		return metroObjects

	#This function returns the itineraries given two points
	def getItineraryByPoints(self, data = {}):
		url = "https://api.ridemetro.org/data/CalculateItineraryByPoints?$expand=Legs&$format=json&subscription-key="+ self.api_key
		for key in data.keys():
			url = url + "&" + str(key) + "=" + str(data[key])
		r = requests.get(url)
		resp = r.json()
		print str(resp)
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroItinerary(x))
		return metroObjects

	#This function returns a list of incidents
	def getIncidents(self, data = {}):
		url = "https://api.ridemetro.org/data/Incidents?$format=json&subscription-key="+ self.api_key
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroIncident(x))
		return metroObjects

	#This function returns a list of Routes
	def getRoutes(self, data = {}):
		url = "https://api.ridemetro.org/data/Routes?$format=json&subscription-key="+ self.api_key
		for key in data.keys():
			url = url + "&" + str(key) + "=" + str(data[key])
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroRoute(x))
		return metroObjects

	#This function returns a list of routes given an ID
	def getRoutesId(self, data = {}):
		url = "https://api.ridemetro.org/data/Routes('" + data['id'] + "')?$format=json&subscription-key="+ self.api_key
		for key in data.keys():
			if key != "id":
				url = url + "&" + key + "=" + data[key]
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroRoute(x))
		return metroObjects

	#This function returns a list of routes' arrivals given an ID
	def getRoutesIdArrivals(self, data = {}):
		url = "https://api.ridemetro.org/data/Routes('" + data['id'] + "')/Arrivals?$format=json&subscription-key="+ self.api_key
		for key in data.keys():
			if key != "id":
				url = url + "&" + str(key) + "=" + str(data[key])
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroArrival(x))
		return metroObjects

	#This function returns the stops for a given route
	def getRoutesStops(self, data = {}):
		url = "https://api.ridemetro.org/data/Routes('" + data['id'] + "')/Stops?$format=json&subscription-key="+ self.api_key
		r = requests.get(url)
		for key in data.keys():
			if key != "id":
				url = url + "&" + str(key) + "=" + str(data[key])
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroStop(x))
		return metroObjects

	def getStops(self, data = {}):
		url = "https://api.ridemetro.org/data/Stops?$format=json&subscription-key="+ self.api_key
		for key in data.keys():
			url = url + "&" + str(key) + "=" + str(data[key])
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroStop(x))
		return metroObjects

	def getStopsId(self, data = {}):
		url = "https://api.ridemetro.org/data/Stops('" + data['id'] + "')?$format=json&subscription-key="+ self.api_key
		for key in data.keys():
			if key != "id":
				url = url + "&" + str(key) + "=" + str(data[key])
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroStop(x))
		return metroObjects

	def getStopsArrivals(self, data = {}):
		url = "https://api.ridemetro.org/data/Stops('" + data['id'] + "')/Arrivals?$format=json&subscription-key="+ self.api_key
		for key in data.keys():
			if key != "id":
				url = url + "&" + str(key) + "=" + str(data[key])
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroArrival(x))
		return metroObjects

	def getStopsRoutes(self, data = {}):
		url = "https://api.ridemetro.org/data/Stops('" + data['id'] + "')/Routes?$format=json&subscription-key="+ self.api_key
		for key in data.keys():
			if key != "id":
				url = url + "&" + str(key) + "=" + str(data[key])
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroRoute(x))
		return metroObjects

	#This function returns all of the active 
	def getVehicles(self, data = {}):
		url = "https://api.ridemetro.org/data/Vehicles?$format=json&subscription-key=" + self.api_key
		r = requests.get(url)
		resp = r.json()
		metroObjects = []
		for x in resp['d']['results']:
			metroObjects.append(MetroVehicle(x))
		return metroObjects