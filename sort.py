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

class SortPage(webapp.RequestHandler):
    def get(self):
        index = self.request.get("tag")
        user = users.get_current_user()  
        islog={}
        if user:
            islog['url'] = users.create_logout_url(self.request.uri)
            islog['tell'] = 'Logout'
            islog['name'] = user.nickname()
        else:
            self.redirect(users.create_login_url(self.request.uri))
            return 0

        istag = db.GqlQuery("SELECT * FROM Notes WHERE tag=:1 LIMIT 20",index)
        isauthor = db.GqlQuery("SELECT * FROM Authors WHERE nick=:1 LIMIT 20",index)
        mytags = db.GqlQuery("SELECT * FROM Tags ORDER BY counter DESC LIMIT 20")

        archi = db.GqlQuery("SELECT * FROM Archives ORDER BY date DESC LIMIT 1000")
        if istag.count():
            mynotes = istag
            isauthor = db.GqlQuery("SELECT * FROM Authors ORDER BY counter DESC LIMIT 20")
        else:
            if isauthor.count():
                mynotes = db.GqlQuery("SELECT * FROM Notes WHERE author=:1 ORDER BY date DESC LIMIT 1000",isauthor[0].author)
            else:
                self.redirect('/')
                return 0

        template_values ={
		    'mynotes':mynotes,
		    'tags':mytags,
            'log':islog,
            'authors':isauthor,
            'archi':archi
	    }
        path = os.path.join(os.path.dirname(__file__),'main.html')
        self.response.out.write(template.render(path,template_values))

application = webapp.WSGIApplication([
            ('.*', SortPage)
            ], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
