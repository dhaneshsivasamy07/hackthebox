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
