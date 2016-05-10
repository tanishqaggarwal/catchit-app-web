import webapp2
from google.appengine.ext import ndb

class ClearSightingsHandler(webapp2.RequestHandler):
	def get(self):
		ndb.delete_multi(dbmodel.Sighting.query().fetch(keys_only=True))