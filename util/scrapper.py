from urlopener import URLOpener
from BeautifulSoup import BeautifulSoup

import re
import urllib

_logon_url = 'https://cadetone.aafc.org.au/logon.php'
_logout_url = 'https://cadetone.aafc.org.au/logout.php'
_change_unit_url = 'https://cadetone.aafc.org.au/changeunit.php'
_act_details_url = 'https://cadetone.aafc.org.au/activities/viewactivity.php?'
_act_roll_url = 'https://cadetone.aafc.org.au/activities/nominalroll.php?'

def _parse_act_pages(pages):
  res = []
  for p in pages:
    soup = BeautifulSoup(p)
    if soup.find(text=re.compile('not authorised')):
      continue

    r = {}

    curr = soup.find(text=re.compile('Name:'))
    if curr:
      r['name'] = curr.parent.findNextSibling('td').contents[0]

    curr = soup.find(text=re.compile('Location:'))
    if curr:
      r['loc'] = curr.parent.findNextSibling('td').contents[0]

    curr = soup.find(text=re.compile('Start'))
    if curr:
      r['start'] = curr.parent.findNextSibling('td').contents[0].replace('&nbsp;', ' ')

    curr = soup.find(text=re.compile('Finish'))
    if curr:
      r['finish'] = curr.parent.findNextSibling('td').contents[0].replace('&nbsp;', ' ')

    curr = soup.find(text=re.compile('Cadets:'))
    if curr:
      r['pax_no'] = int(curr.parent.findNextSibling('td').contents[0])

    curr = soup.find(text=re.compile('Staff:'))
    if curr:
      r['pax_no'] += int(curr.parent.findNextSibling('td').contents[0])

    res.append(r)

  print res
  return pages

def _parse_roll_pages(pages):
  for p in pages:
    soup = BeautifulSoup(p)

  return pages

def login(usr, pwd):
  opener = URLOpener()
  param = urllib.urlencode({
      'ServiceNo' : usr,
      'Password' : pwd})

  opener.open(_logon_url, data=param)

  # Change to 3WG appointment
###  param = urllib.urlencode({
###      'UnitDetId' : '3,0'})
###  opener.open(_change_unit_url)

  return opener

def logout(opener):
  opener.open(_logout_url)

def get_activity_info(act_ids, opener):
  pages = []

  for act in act_ids:
    pages.append(opener.open(_act_details_url + urllib.urlencode({'ActID': act})).content)

  return _parse_act_pages(pages)

def get_nominal_roll(act_ids, opener):
  pages = []
  for act in act_ids:
    pages.append(opener.open(_act_roll_url + urllib.urlencode({'ActID': act})).content)

  return _parse_roll_pages(pages)
