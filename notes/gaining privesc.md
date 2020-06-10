### DONT RELY ON MSF
##### Unless your only goal is to complete the box

- [ ] when ```www-data``` shell is obtained upload a linenum scripts and run it
- [ ] look for <br />
        1. Files with unwanted permissions <br />
        2. Files with SETUID binaries ```find / -perm -4000``` <br />
        3. Look for Cron Jobs <br />
- [ ] always look for the users in the ```/home``` dirs, the passwords that found during the enumeartion phase will be the same password for the user as well
- [ ] ```sudo -l``` should be checked must
