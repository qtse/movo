from urlopener import URLOpener

import urllib

_logon_url = 'https://cadetone.aafc.org.au/logon.php'
_logout_url = 'https://cadetone.aafc.org.au/logout.php'
_change_unit_url = 'https://cadetone.aafc.org.au/changeunit.php'
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

  opener.open(_logon_url, data=param)

  # Change to 3WG appointment
  param = urllib.urlencode({
      'UnitDetId' : '3,0'})
  opener.open(_change_unit_url)

  return opener

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
