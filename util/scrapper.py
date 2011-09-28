from urlopener import URLOpener
from BeautifulSoup import BeautifulSoup

from datetime import datetime

import calendar
import re
import urllib

_logon_url = 'https://cadetone.aafc.org.au/logon.php'
_logout_url = 'https://cadetone.aafc.org.au/logout.php'
_change_unit_url = 'https://cadetone.aafc.org.au/changeunit.php'
_act_details_url = 'https://cadetone.aafc.org.au/activities/viewactivity.php?'
_act_roll_url = 'https://cadetone.aafc.org.au/activities/nominalroll.php?'
_mbr_search_url = 'https://cadetone.aafc.org.au/searchmember.php?PageRef=memberdetails&Members=' # actually a post form
_mbr_profile_url = 'https://cadetone.aafc.org.au/personnel/memberdetails.php?'

def _parse_profile_for_age(page, start):
  soup = BeautifulSoup(page)

  curr = soup.find(text=re.compile('Date of Birth'))
  if not curr:
    return None

  dob = curr.parent.findNextSibling('td').contents[0].replace('&nbsp;', '')
  dob = datetime.strptime(dob, '%d %b %Y').date()

  try: # raised when birth date is February 29 and the current year is not a leap year
    birthday = dob.replace(year=start.year)
  except ValueError:
    birthday = dob.replace(year=start.year, day=born.day-1)

  days_after_bd = start-birthday

  if calendar.isleap(start.year):
    frac = days_after_bd.days / 366.0
  else:
    frac = days_after_bd.days / 365.0

  age = start.year - dob.year + frac

  return min(start.year - dob.year + frac, 18)

def _parse_mbr_search(page):
  soup = BeautifulSoup(page)

  if soup.find(text=re.compile('not authorised')):
    return None

  if soup.find(text=re.compile('No Members found')):
    return None

  # move curr to table containing search results
  curr = soup.body.table.findNextSibling('table').findNextSibling('table').tr.td.h2.findNextSibling('table')

  # 1st row of results (should only be 1)
  curr = curr.tr.findNextSibling('tr')

  # button to access member records
  curr = curr.input

  return curr['onclick'][curr['onclick'].find('ID=')+3:-1]

def _get_age(service_no, start, opener):
  param = urllib.urlencode({'LastNametxt':'', 'ServiceNotxt':service_no, 'Searchflag':'formsearch'})
  mid = _parse_mbr_search(opener.open(_mbr_search_url, data=param).content)
  param = urllib.urlencode({'PageRef':'searchmember', 'ID':'859'})
  return _parse_profile_for_age(opener.open(_mbr_profile_url, data=param).content, start)

def _parse_act_pages(pages):
  res = []
  for act, p in pages:
    soup = BeautifulSoup(p)
    if soup.find(text=re.compile('not authorised')):
      res.append({'act_id' : act, 'name':None})
      continue

    r = {}

    r['act_id'] = act

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

  return res


def _parse_roll_pages(pages, opener):
  res = []
  for p in pages:
    soup = BeautifulSoup(p)

    if soup.find(text=re.compile('not authorised')):
      continue

    curr = soup.body.table #1st table
    curr = curr.findNextSibling('table').findNextSibling('table') #3rd table
    curr = curr.table #1st sub table

    start = curr.find(text=re.compile('Start')).parent.parent.findNextSibling('td')
    start = start.contents[0].replace('&nbsp;', ' ')
    start = datetime.strptime(start, '%d %b %Y %H:%M').date()

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

        if i == 1 or i == 2:
          r['age'] = _get_age(r['service_no'], start, opener)
        else:
          r['age'] = 18

        res.append(r)
        row = row.findNextSibling('tr')
        return res

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
    pages.append((act, opener.open(_act_details_url + urllib.urlencode({'ActID': act})).content))

  return _parse_act_pages(pages)

def get_nominal_roll(act_ids, opener):
  pages = []
  for act in act_ids:
    pages.append(opener.open(_act_roll_url + urllib.urlencode({'ActID': act})).content)

  return _parse_roll_pages(pages, opener)
