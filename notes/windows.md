### Powershell 
![powershell](https://github.com/cyberwr3nch/hackthebox/blob/master/scripts/files/powershell.png)
#### Get to know the current user, which you are logged in 

```powershell
# system_name\user_name
[System.Security.Principal.WindowsIdentity]::GetCurrent().Name

# user name & system name
$env:UserName
$env:UserDomain
```

#### Disable RealTimeProtection

```powershell
#disables real time protection
Set-MpPreference -DisableRealtimeMonitoring $true

#enables real time protection
Set-MpPreference -DisableRealtimeMonitoring $false
```

### CMD Commands

#### Normal CMD

```cmd
# get current username
whoami

# get system information
systeminfo

# grep() for os name
systeminfo | findstr /C:"OS Name"

# get the hostname
hostname

# know the priviledges we have
whoami /priv

# know all the users in the machine
net user 

# Obtain information about the specific user
net user <username>

# Obtain users belongs to a specific groups
net localgroup administrators / <group name>

# get to know network
ipconfig
ipconfig /all

# internal network services
netstat -ano 

```

#### CMD commands when wmic is available

```cmd
# updation list
wmic qfc get Caption,Description,HotFixID,InstalledOn

# list disks with wmic
wmic logicaldisk get caption,description,providenBane
```