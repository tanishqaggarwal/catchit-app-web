import re
from google.appengine.ext import ndb

def time_check_passed(hour, minute):
	busRouteTime = minute + 60 * hour

	if busRouteTime > 1470 or busRouteTime < 930:
		return False
	else:
		return True

def email_address_unused(emailAddress):
	query = dbmodel.User(dbmodel.User.emailAddress == emailAddress).get()
	if not query:
		return True
	else:
		return False

def email_address_valid(emailAddress):
	if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify) == None:
		return False
	else:
		return True	

def check_district_passcode(passcode):
	if passcode == "wholechildeverychild":
		return True
	return False