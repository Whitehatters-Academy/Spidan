#!/usr/bin/env python

import sys
import requests
import socket
import shodan

# Add some colouring for printing packets later
YELLOW = '\033[93m'
GREEN = '\033[92m'
END = '\033[0m'
RED = '\033[91m'

def get_host(target):
  try:
    print GREEN + '[*] Trying to connect to: %s' %target
    r = requests.get(target)
    if 'http://' in target:
      host = target[7:]
    if 'https://' in target:
      host = target[8:]
    ipaddr = socket.gethostbyname(host)
    if r.status_code != 200:
      print RED + 'Error: URL is not alive' + END
    else:
      print GREEN + '[+] Printing out Server Information....' + END
      print YELLOW + '[-] Host Name: %s' %target + END
      print YELLOW + '[-] IP Address: %s' %ipaddr + END
      if 'server' in r.headers:
        print YELLOW + '[-] Server: %s' %(r.headers['server']) + END
      if 'x-powered-by' in r.headers:
        print YELLOW + '[-] Powered By: %s' %(r.headers['x-powered-by']) + END
      print YELLOW + '[-] Cookies: %s' %(requests.utils.dict_from_cookiejar(r.cookies)) + END
    shodan_search(ipaddr)
  except Exception as e:
    print RED + '[!] Error encountered - %s' %(str(e)) + END
    sys.exit(1)

def get_robots(target):
  robot = target + '/robots.txt'
  try:
    print GREEN + '[*] Looking for robots.txt file at %s' %robot + END
    r = requests.get(robot)
    if r.status_code == 302:
      print RED + '[!] Sneaky redirect, no robots.txt here..' + END
    if r.status_code == 200:
      print GREEN + '[+] Printing out robots.txt file....' + END
      print YELLOW + r.text + END
    else:
      print RED + '[!] No robots.txt found' + END
  except Exception, e:
    print RED + '[!] Whoops that didnt work...' + END

def shodan_search(host):
  api = shodan.Shodan(apikey)
  print GREEN + '[*] Connecting to Shodan, looking for %s' %host + END
  try:
    results = api.host(host)
    print YELLOW + '[-] Latitude: %s\n[-] Longitude: %s' %(results.get('latitude', 'n/a'), results.get('longitude', 'n/a')) + END
    google_map = 'https://maps.google.co.uk/maps?z=20&q=%s,%s' %(results.get('latitude', 'n/a'), results.get('longitude', 'n/a')) + END
    print YELLOW + '[-] Google Map URL: %s' %google_map
  except shodan.APIError, e:
    print 'Error: %s' % e

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print RED + 'Usage: ./spidan.py http://www.example.com 6abb3602b5755089e9e4e27050ec506a' + END
    print RED + 'Example: ./spidan.py [URL] [Shodan API Key]'
    sys.exit(1)
  target = sys.argv[1]
  apikey = sys.argv[2]
  get_host(target)
  get_robots(target)
