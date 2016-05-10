import webapp2
from google.appengine.ext import ndb

from validationutils import *

class RegisterHandler(webapp2.RequestHandler):
	def post(self):
		name                    = self.request.get("name")
		districtPasscode        = self.request.get("districtPasscode")
		if not check_district_passcode(districtPasscode):
			return webapp2.Response("invalid district passcode")

		emailAddress            = self.request.get("emailAddress")
		if not email_address_valid(emailAddress):
			return webapp2.Response("invalid email Address")
		if not email_address_unused(emailAddress):
			return webapp2.Response("email address already in system")

		password                = self.request.get("password")
		if len(password) < 8:
			return webapp2.Response("invalid password")

		busRouteName            = self.request.get("busRouteName")
		if busRouteName not in dbmodel.BUS_ROUTES:
			return webapp2.Response("invalid bus route")

		busRouteStop            = self.request.get("busRouteStop")
		if busRouteStop not in dbmodel.SCHOOLS:
			return webapp2.Response("invalid bus stop")

		busRouteTimeHour        = self.request.get("busRouteTimeHour")
		busRouteTimeMinute      = self.request.get("busRouteTimeMinute")
		busRouteTime = None
		try:
			busRouteTimeMinute = int(busRouteTimeMinute)
			busRouteTimeHour   = int(busRouteTimeHour)

			if not time_check_passed(busRouteTimeHour, busRouteTimeMinute):
				return webapp2.Response("invalid bus time")

			busRouteTime = datetime.Time(busRouteTimeHour, busRouteTimeMinute)
		except:
			return webapp2.Response("invalid bus time")

		locationServicesEnabled = self.request.get("locationServicesEnabled")
		if locationServicesEnabled != "true" or locationServicesEnabled != "false":
			return webapp2.Response("invalid location services setting")

		userobj              = dbmodel.User()
		userobj.name         = name
		userobj.emailAddress = emailAddress
		userobj.password     = security.hash_function(password)
		userobj.busRouteName = busRouteName
		userobj.busRouteStop = busRouteStop
		userobj.busRouteTime = busRouteTime
		userobj.locationServicesEnabled = True if locationServicesEnabled == "true" else False
		userobj.put()

		ATTR_NAMES = {
			"High School South - 4" 	  : "south4Arrival",
			"High School South - 5" 	  : "south5Arrival",
			"High School North - 4" 	  : "north4Arrival",
			"High School North - 5" 	  : "north5Arrival",
			"Community Middle School - 4" : "community4Arrival",
			"Community Middle School - 5" : "community5Arrival",
			"Grover Middle School - 4"    : "grover4Arrival",
			"Grover Middle School - 5"    : "grover5Arrival",
		}
		routequery   = dbmodel.BusRoute.query(dbmodel.BusRoute.busRouteName == busRouteName).get()
		busRouteTime = busRouteTimeHour * 60 + busRouteTimeMinute
		attribute_name = busRouteName
		if busRouteTime > 1010:
			attribute_name += " - 5"
		else:
			attribute_name += " - 4"

		oldtime = getattr(routequery, attribute_name)
		newtime = int((routequery.sampleSize * (oldtime.hour * 60 + oldtime.minute) + busRouteTime) / float(routequery.sampleSize + 1)) #modifying the "average"
		newtime = datetime.Time(newtime / 60, newtime % 60)

		setattr(routequery, attribute_name, newtime)

		routequery.sampleSize = routequery.sampleSize + 1
		routequery.put()

		return webapp2.Response("registration successful")

class LoginHandler(webapp2.RequestHandler):
	def post(self):
		emailAddress = self.request.get("emailAddress")
		password     = self.request.get("password")

		if not email_address_valid(emailAddress):
			return webapp2.Response(json.dumps({"status":"failure","reason":"invalid email address"}))
		if email_address_unused(emailAddress):
			return webapp2.Response(json.dumps({"status":"failure","reason":"email address not in system"}))
		if len(password) < 8:
			return webapp2.Response(json.dumps({"status":"failure","reason":"password too short"}))

		query = dbmodel.User.query(dbmodel.User.emailAddress == emailAddress and dbmodel.User.password = security.hash_function(password)).get()
		if not query:
			return webapp2.Response(json.dumps({"status":"failure","reason":"invalid email/password"}))

		returnData = {
			"status"                  : "success",
			"busRouteName"            : query.busRouteName,
			"busRouteStop"            : query.busRouteStop,
			"locationServicesEnabled" : query.locationServicesEnabled,
			"busRouteTimeHour"        : query.busRouteTime.hour,
			"busRouteTimeMinute"      : query.busRouteTime.minute,
			"addressToken"            : security.
			"name"                    : name,
		}
		return webapp2.Response(json.dumps(returnData))

class EarliestTimeOnRouteHandler(webapp2.RequestHandler):
	def post(self):
		busRouteName = self.request.get("busRouteName")
		if busRouteName not in dbmodel.BUS_ROUTES:
			return webapp2.Response("invalid bus route")
			
		emailAddress = self.request.get("emailAddress")
		addressToken = self.request.get("addressToken")
		if addressToken != hash_function(emailAddress):
			return webapp2.Response("invalid address token")

		query = dbmodel.User.query(dbmodel.User.busRouteName == busRouteName).order(dbmodel.User.busRouteTime).get()
		time = query.busRouteTime

		return webapp2.Response(str(60 * time.hour + time.minute))


class EmailAddressCheckHandler(webapp2.RequestHandler):
	def post(self):
	    emailAddress = self.request.get("emailAddress")
	    if not email_address_valid(emailAddress):
	    	return webapp2.Response("invalid email")
	    if not email_address_unused(emailAddress):
	    	return webapp2.Response("email in system")
	    return webapp2.Response("valid email")

class DistrictPasscodeCheckHandler(webapp2.RequestHandler):
	def post(self):
		districtPasscode = self.request.get("districtPasscode")
		if not check_district_passcode(districtPasscode):
			return webapp2.Response("invalid district passcode")
		return webapp2.Response("valid district passcode")

class ReportSightingHandler(webapp2.RequestHandler):
	def post(self):
		addressToken = self.request.get("addressToken")
		emailAddress = self.request.get("emailAddress")
		if security.hash_function(emailAddress) != "addressToken":
			return webapp2.Response("invalid token")

		busRouteName = self.request.get("busRouteName")
		if busRouteName not in dbmodel.BUS_ROUTES:
			return webapp2.Response("invalid route")

		latitude  = self.request.get("latitude")
		longitude = self.request.get("longitude")

		sighting = dbmodel.Sighting()
		sighting.emailAddressSighted = emailAddress
		sighting.busRouteSighted     = busRouteName
		sighting.locationSighted     = ndb.GeoPt(latitude, longitude)
		sighting.put()

		return webapp2.Response("sighting noted")

class GetSightingHandler(webapp2.RequestHandler):
	def post(self):
		addressToken = self.request.get("addressToken")
		emailAddress = self.request.get("emailAddress")
		if security.hash_function(emailAddress) != "addressToken":
			return webapp2.Response("invalid token")

		busRouteName = self.request.get("busRouteName")
		if busRouteName not in dbmodel.BUS_ROUTES:
			return webapp2.Response("invalid route")

		sightings_query = dbmodel.Sighting.query(dbmodel.Sighting.busRouteSighted == busRouteName, dbmodel.Sighting.timeSighted >= datetime.datetime.now() - datetime.timedelta(seconds=60)).fetch(10)
		if sightings_query == [] or not sightings_query:
			return webapp2.Response(json.dumps({
				"status"    : "failure"
				}))
		latitude_list = []
		longitude_list = []
		for point in sightings_query:
			latitude_list.add(point.locationSighted.latitude)
			longitude_list.add(point.locationSighted.longitude)
		latitude  = statistics.median(latitude_list)
		longitude = statistics.median(latitude_list)
		return webapp2.Response(json.dumps({
			"status"    : "success",
			"latitude"  : latitude,
			"longitude" : longitude,
			}))



class GetRouteInfoHandler(webapp2.RequestHandler):
	def post(self):
		addressToken = self.request.get("addressToken")
		emailAddress = self.request.get("emailAddress")
		if security.hash_function(emailAddress) != "addressToken":
			return webapp2.Response("invalid token")

		busRouteName = self.request.get("busRouteName")
		if busRouteName not in dbmodel.BUS_ROUTES:
			return webapp2.Response("invalid route")

		route_query = dbmodel.Route.query(dbmodel.Route.busRouteName == busRouteName).get()
		returnvals = {
			"High School South - 4" 	  : self.time_to_int(route_query.south4Arrival),
			"High School South - 5" 	  : self.time_to_int(route_query.south5Arrival),
			"High School North - 4" 	  : self.time_to_int(route_query.north4Arrival),
			"High School North - 5" 	  : self.time_to_int(route_query.north5Arrival),
			"Community Middle School - 4" : self.time_to_int(route_query.community4Arrival),
			"Community Middle School - 5" : self.time_to_int(route_query.community5Arrival),
			"Grover Middle School - 4"    : self.time_to_int(route_query.grover4Arrival),
			"Grover Middle School - 5"    : self.time_to_int(route_query.grover5Arrival),
		}
		return webapp2.Response(json.dumps(returnvals))
	
	def time_to_int(self, time):
		return time.hour * 60 + time.minute

class EditPreferencesHandler(webapp2.RequestHandler):
	def post(self):
		emailAddress = self.request.get('emailAddress')
		addressToken = self.request.get('addressToken')
		busRouteName = self.request.get("busRouteName")
		busRouteStop = self.request.get("busRouteStop")
		busRouteTimeMinute = self.request.get("busRouteTimeMinute")
		busRouteTimeHour   = self.request.get("busRouteTimeHour")
		locationServicesEnabled = self.request.get('locationServicesEnabled')

		if security.hash_function(emailAddress) != addressToken:
			return webapp2.Response("Invalid login token. Try logging out and back in.")

		userquery = dbmodel.User.query(dbmodel.User.emailAddress == emailAddress).get()
		if not userquery:
			return webapp2.Response("Invalid login. Try logging out and back in again.")

		if busRouteName not in dbmodel.BUS_ROUTES:
			return webapp2.Response("Invalid choice of bus route.")

		if busRouteName not in dbmodel.BUS_ROUTES:
			return webapp2.Response("Invalid choice of bus stop.")

		try:
			busRouteTimeHour   = int(busRouteTimeHour)
			busRouteTimeMinute = int(busRouteTimeMinute)
			if not time_check_passed(busRouteTimeHour, busRouteTimeMinute):
				return webapp2.Response("Invalid bus estimated arrival time.")
		except:
			return webapp2.Response("Invalid time choice.")

		userquery.busRouteName = busRouteName
		userquery.busRouteStop = busRouteStop
		userquery.busRouteTime = datetime.Time(busRouteTimeHour, busRouteTimeMinute)
		userquery.locationServicesEnabled = (locationServicesEnabled == "true")
		userquery.put()

		return webapp2.Response("settings change successful")