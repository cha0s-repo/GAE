#!/usr/bin/env python -t

from google.appengine.ext import db
                
class Notes(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    tag = db.StringProperty(multiline=False)

class Authors(db.Model):
    author = db.UserProperty()
    name = db.StringProperty(multiline=False)
    nick = db.StringProperty(multiline=False)
    counter = db.IntegerProperty()

class Tags(db.Model):
	name = db.StringProperty(multiline=False)
	counter = db.IntegerProperty()

