### DONT RELY ON MSF
##### Unless your only goal is to complete the box

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


##### Commands:

###### Network monitoring:

```bash
#network modules info and IPs
ifconfig
ipaddr
#shows the tcp connection
netstat -antp     
ss -antp          
```
