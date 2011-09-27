from urlopen import URLOpener

import urllib

_logon_url = 'https://cadetone.aafc.org.au/logon.php'
_logout_url = 'https://cadetone.aafc.org.au/logout.php'
_act_details_url = 'https://cadetone.aafc.org.au/activities/viewactivity.php?ActID='
_act_roll_url = 'https://cadetone.aafc.org.au/activities/nominalroll.php?ActID='

def _parse_act_pages(pages):
  return pages

def _parse_roll_pages(pages):
  return pages

def login(usr, pwd):
  opener = URLOpener()
  param = urllib.urlencode({
      'ServiceNo' : usr,
      'Password' : pwd})

  return opener.open(_logon_url, data=param)

def _logout(opener):
  opener.open(_logout_url)

def get_activity_info(act_ids, opener):
  pages = []

  for act in act_ids:
    pages.append(opener.open(_act_details_url + urllib.urlencode(act)).content)

  return _parse_act_pages(pages)

def get_nominal_roll(act_ids, opener):
  pages = []
  for act in act_ids:
    pages.append(opener.open(_act_roll_url + urllib.urlencode(act)).content)

  return _parse_roll_pages(pages)
