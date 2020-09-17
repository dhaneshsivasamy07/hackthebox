- [ ] Navigate to the IP when ```HTTP``` port is found
- [ ] If the IP is resolved into ```machine.htb```, add it to **/etc/hosts** and look for vhosts
*Wordlist for vhost bruteforce may be crafted(cewl) / default ones*
- [ ] enumerate the dirs
- [ ] look for fishy directories (dev/, backup/, etc..,)
- [ ] if ```uploads``` directory is present make a note of it
- [ ] when open shell is found with code execution and redirection ```2>&1``` in the source code upload a reverse shell in the uploads dir
- [ ] when you encounter a cms ```(like wordpress, bludit, openemr)``` bruteforce for directories and look for exploits
- [ ] use `msfvenom` to generate reverse shells if you are confused to get the perfect shell
