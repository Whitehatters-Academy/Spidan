#!/usr/bin/env python

import sys
import requests
import socket

# Add some colouring for printing packets later
YELLOW = '\033[93m'
GREEN = '\033[92m'
END = '\033[0m'
RED = '\033[91m'

def get_host(target):
  r = requests.get(target)
  if r.status_code != 200:
    print RED + 'Error: URL is not alive' + END
  else:
    print GREEN + '[+] Printing out Server Information....' + END
    print YELLOW + '[-] Host Name: %s' %target + END
    if 'http://' in target:
      host = target[7:]
    if 'https://' in target:
      host = target[8:]
    print YELLOW + '[-] IP Address: %s' %(socket.gethostbyname(host)) + END
    if 'server' in r.headers:
      print YELLOW + '[-] Server: %s' %(r.headers['server']) + END
    if 'x-powered-by' in r.headers:
      print YELLOW + '[-] Powered By: %s' %(r.headers['x-powered-by']) + END
    print YELLOW + '[-] Cookies: %s' %(requests.utils.dict_from_cookiejar(r.cookies)) + END

def get_robots(target):
  robot = target + '/robots.txt'
  r = requests.get(robot)
  if r.status_code != 200:
    print GREEN + '[+] Printing out robots.txt file....' + END
    print r.text
  else:
    print RED + 'No robots.txt found' + END

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print RED + 'Usage: ./spidan.py http://www.example.com' + END
    sys.exit(1)

  target = sys.argv[1]
  get_host(target)
  get_robots(target)
