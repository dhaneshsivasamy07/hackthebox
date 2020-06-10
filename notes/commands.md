### DONT RELY ON MSF
##### Unless your only goal is to complete the box

#### NMAP Enumeration
- [ ] *nmap -sC -sV -oA output-Name Machine_Ip* - Scans Open ports and displays the versions<br />
- [ ] *nmap -T5 -p- machine_Ip* - Full TCP Scan <br />
- [ ] *nmap -sU -p- machine_Ip* - Full UDP Scan <br />


#### DIRECTORY Enumeration
- [ ] *gobuster dir -u http://machineIP -w ```$Wordlist``` -x html,php,json,aspx,txt -o gobuster-dirs.txt*
- [ ] *gobuster dir -u http://machineIP -w ```$Wordlist``` -x html,php,json,aspx,txt -o gobuster-common.txt*
- [ ] *wfuzz -u http://machineIP/FUZZ -w /usr/share/wordlists/dirb/common.txt --hc 404*


#### VHOST Enumeration
- [ ] *wfuzz -H 'HEAD: FUZZ.htb' -w ```$Wordlist``` -u http://machineIP --hw 0*
