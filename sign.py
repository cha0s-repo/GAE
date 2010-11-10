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
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
             
from data import *
import re

class dumpNote(webapp.RequestHandler):
    def post(self):
        mynote = Notes()

        content = self.request.get('content')
        tag = self.request.get('tag')

		 
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return 0

        if len(content):
            mynote.content = content
            mynote.tag = tag
            mynote.author = user
            mynote.put()

# Check if user is already in Authors database    
            nickname  = user.nickname()
            getauthor = db.GqlQuery("SELECT * FROM Authors WHERE name=:1 ORDER BY counter DESC LIMIT 10",nickname)
            if getauthor.count():
                update_author = Authors.get_by_key_name(nickname)
                update_author.counter += 1
                update_author.put()
                """
                split = re.search('([\w.-]+)@([\w.-]+)',nickname)
                if split:
                    getauthor.nick = split.group(1)

                    getauthor.name = nickname
                else:
                    getauthor.nick = nickname
                    getauthor.name = nickname+"@gmail.com"
                """
            else:
                newauthor = Authors(key_name=nickname)
                newauthor.author = user

                # Some user may not login with an email address
                split = re.search('([\w.-]+)@([\w.-]+)',nickname)
                if split:
                    newauthor.nick = split.group(1)

                    newauthor.name = nickname
                else:
                    newauthor.nick = nickname
                    newauthor.name = nickname
                newauthor.counter = 1
                newauthor.put()
            
            # Update current tag counter
            gettag = Tags.get_by_key_name(tag)
            if gettag:
                gettag.counter +=1
            else:
                self.redirect('/config')
			
            gettag.put()

        self.redirect('/')
               	
application = webapp.WSGIApplication([
            ('/sign', dumpNote)
            ], debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
