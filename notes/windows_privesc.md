### Windows PrivEsc

- [ ] once you get the revershell, look for `current user` and `system informations`
- [ ] Look for open vulns with `kbid` with the command `wmic qfc` 
> WE CANT EXPECT IT TO WORK ON ALL BOXES
- [ ] Check for password files stored in clear text, `findstr /si password *.txt *.ini *.config *.xml`
- [ ] Always look for `unattended.xml`