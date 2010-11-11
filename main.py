#!/usr/bin/env python -t
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
import cgi
import os
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

from google.appengine.ext.webapp import template 
from google.appengine.ext.webapp.util import run_wsgi_app

from data import *           

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        islog = {} 
        mynotes = db.GqlQuery("SELECT * FROM Notes ORDER BY date DESC LIMIT 20")
        mytags = db.GqlQuery("SELECT * FROM Tags ORDER BY counter DESC LIMIT 100")
        myauthors = db.GqlQuery("SELECT * FROM Authors ORDER BY counter DESC LIMIT 20")
        archi = db.GqlQuery("SELECT * FROM Archives ORDER BY date DESC LIMIT 1000")
        if user:
            islog['url'] = users.create_logout_url(self.request.uri)
            islog['tell'] = 'Logout'
            islog['name'] = user.nickname()
        else:
            islog['url'] = (users.create_login_url(self.request.uri))
            islog['tell'] = 'Login'
            islog['name'] = 'Guest' 

        template_values ={
		        'mynotes':mynotes,
		        'tags':mytags,
                'log':islog,
                'authors':myauthors,
                'archi':archi,
        }
        path = os.path.join(os.path.dirname(__file__),'main.html')
        self.response.out.write(template.render(path,template_values))

application = webapp.WSGIApplication([
            ('/', MainPage)
            ], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
