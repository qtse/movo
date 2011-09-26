#
# Code roughly based on Scott Hillman's blog post
# http://everydayscripting.blogspot.com/2009/08/google-app-engine-cookie-handling-with.html
#

import Cookie
from google.appengine.api import urlfetch

class URLOpener:
  def __init__(self):
    self.cookie = Cookie.SimpleCookie()
                
  def open(self, url, data = None):
    if data is None:
      method = urlfetch.GET
    else:
      method = urlfetch.POST

    # This version doest not follow redirects at all.
    response = urlfetch.fetch(url=url,
                              payload=data,
                              method=method,
                              headers=self._getHeaders(self.cookie),
                              allow_truncated=False,
                              follow_redirects=False,
                              deadline=10
                              )
    self.cookie.load(response.headers.get('set-cookie', '')) # Load the cookies from the response

    return response

  def _getHeaders(self, cookie):
    headers = {
               'Cookie' : self._makeCookieHeader(cookie)
               }
    return headers

  def _makeCookieHeader(self, cookie):
    cookieHeader = ""
    for value in cookie.values():
      cookieHeader += "%s=%s; " % (value.key, value.value)
    return cookieHeader
