from urlopener import URLOpener
from BeautifulSoup import BeautifulSoup

from datetime import datetime

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
      r['start'] = datetime.strptime(r['start'], '%d %b %Y %H:%M').date()

    curr = soup.find(text=re.compile('Finish'))
    if curr:
      r['finish'] = curr.parent.findNextSibling('td').contents[0].replace('&nbsp;', ' ')
      r['finish'] = datetime.strptime(r['finish'], '%d %b %Y %H:%M').date()

    curr = soup.find(text=re.compile('Cadets:'))
    if curr:
      r['pax_no'] = int(curr.parent.findNextSibling('td').contents[0])

    curr = soup.find(text=re.compile('Staff:'))
    if curr:
      r['pax_no'] += int(curr.parent.findNextSibling('td').contents[0])

    res.append(r)


def _parse_roll_pages(pages):
  res = []
  for p in pages:
    soup = BeautifulSoup(p)

    if soup.find(text=re.compile('not authorised')):
      continue

    curr = soup.body.table #1st table
    curr = curr.findNextSibling('table').findNextSibling('table') #3rd table
    curr = curr.table #1st sub table

    for i in range(1, 5):
      curr = curr.findNextSibling('table')

      row = curr.tr.findNextSibling('tr').findNextSibling('tr') # ignore 1st 2 header rows

      while row is not None:
        if row.find(text=re.compile('No records found')):
          break

        r = {}
        cell = row.td
        r['rank'] = cell.contents[0]
        cell = cell.findNextSibling('td')
        r['first_name'] = cell.contents[0]
        cell = cell.findNextSibling('td')
        r['last_name'] = cell.contents[0]
        cell = cell.findNextSibling('td')
        r['service_no'] = cell.contents[0]
        cell = cell.findNextSibling('td')
        r['unit'] = cell.contents[0]
        cell = cell.findNextSibling('td')

        res.append(r)
        row = row.findNextSibling('tr')

  return res

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
