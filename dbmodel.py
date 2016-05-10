from google.appengine.ext import ndb

BUS_ROUTES = [
        "Late Bus A",
        "Late Bus B",
        "Late Bus C",
        "Late Bus D",
        "Late Bus D / Canal Pointe/Meadow Road EXPRESS",
        "Late Bus D / Estates at Princeton Junction EXPRESS",
        "Late Bus E",
        "Late Bus E / Ravens Crest EXPRESS",
        "Late Bus F",
        "Late Bus G",
        "Late Bus H",
        "Late Bus H / Walker Gordon Farm EXPRESS",
        "Late Bus I",
        "Late Bus J",
        "Late Bus K",
        "Late Bus L"
]
SCHOOLS = [
"High School South",
"High School North",
"Grover Middle School",
"Community Middle School"]

class User(ndb.Model):
	datetimeRegistered 		= ndb.DateTimeProperty(auto_now_add = True)
	name 					= ndb.StringProperty(required = True)
	emailAddress 			= ndb.StringProperty(required = True)
	password                = ndb.StringProperty(required = True)
	busRouteName 			= ndb.StringProperty(required = True, choices = BUS_ROUTES)
	busRouteStop		    = ndb.StringProperty(required = True, choices = SCHOOLS)
	busRouteTime 			= ndb.TimeProperty(required = True)
	locationServicesEnabled = ndb.BooleanProperty(default = True)

class BusSighting(ndb.Model):
	timeSighted         = ndb.DateTimeProperty(auto_now_add = True)
	emailAddressSighted = ndb.StringProperty(required = True)
	busRouteSighted     = ndb.StringProperty(required = True, choices = BUS_ROUTES)
	locationSighted     = ndb.GeoPtProperty(required = True)

class Route(ndb.Model):
	busRouteName = ndb.StringProperty(required = True)
	#the following are all "average" arrival times computed daily
	south4Arrival     = ndb.TimeProperty(required = True)
	north4Arrival     = ndb.TimeProperty(default = )
	community4Arrival = ndb.TimeProperty(required = True)
	grover4Arrival    = ndb.TimeProperty(required = True)
	south5Arrival     = ndb.TimeProperty(required = True)
	north5Arrival     = ndb.TimeProperty(default = )
	community5Arrival = ndb.TimeProperty(required = True)
	grover5Arrival    = ndb.TimeProperty(required = True)
	sampleSize        = ndb.IntegerProperty(default = 0)