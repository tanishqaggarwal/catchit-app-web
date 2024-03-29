#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from jinja2 import Environment, PackageLoader
import api

env = Environment(loader=PackageLoader('catchit-app', 'html'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(env.get_template("index.html").render())

app = webapp2.WSGIApplication([
    ('/'                               		 , MainHandler),
    ("/api/register"                   		 , api.RegisterHandler),
    ("/api/login"                      		 , api.AppLoginHandler),
    ("/api/utils/get_earliest_time_on_route" , api.EarliestTimeOnRouteHandler),
    ("/api/utils/check_email_address"        , api.EmailAddressCheckHandler),
    ("/api/utils/check_district_passcode"    , api.DistrictPasscodeCheckHandler),
    ("/api/sightings/report"           		 , api.ReportSightingHandler),
    ("/api/sightings/get"              		 , api.GetSightingHandler),
    ("/api/route_info"              		 , api.GetRouteInfoHandler),
    ("/api/edit_preferences"           		 , api.EditPreferencesHandler),
    ("/tasks/clear_sightings"          		 , cron.ClearSightingsHandler),
], debug=True)