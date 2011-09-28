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
import os
import sys

###os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

###from google.appengine.dist import use_library
###use_library('django', '1.2')

sys.path.insert(0, 'simplejson.zip')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

import urllib

from util.urlopener import URLOpener

###from pytz.gae import pytz
###from pytz import timezone
###from datetime import datetime

###from views import views
from views import jsonfmt as fmt
import simplejson as json

def parse_date(s):
  return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.Z")

class MainHandler(webapp.RequestHandler):
  def get(self, obj_type, arg=''):
    arg = arg.strip()
    if len(arg) > 0 and arg[-1] == '/':
      arg = arg[:-1]
    args = arg.strip().split('/')
    res = None

    self.response.out.write(json.dumps(res, default=fmt.json_handler))

  def post(self, obj_type, arg=''):
    pass

  def put(self, obj_type, arg=''):
    self.response.out.write(json.dumps(res, default=fmt.json_handler))

  def delete(self, obj_type, arg=''):
    pass

def main():
  application = webapp.WSGIApplication([
                                        (r'/(.*?)/(.*)', MainHandler),
                                        (r'/(.*)', MainHandler),
                                       ], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
