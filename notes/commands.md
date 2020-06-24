### DONT RELY ON MSF
##### Unless your only goal is to complete the box

#### NMAP Enumeration<br />
- [ ] *nmap -sC -sV -oA output-Name Machine_Ip* - Scans Open ports and displays the versions<br />
- [ ] *nmap -T5 -p- machine_Ip* - Full TCP Scan <br />
- [ ] *nmap -sU -p- machine_Ip* - Full UDP Scan <br />


#### DIRECTORY Enumeration<br />
- [ ] *gobuster dir -u http://machineIP -w ```$Wordlist``` -x html,php,json,aspx,txt -o gobuster-dirs.txt*<br />
- [ ] *gobuster dir -u http://machineIP -w ```$Wordlist``` -x html,php,json,aspx,txt -o gobuster-common.txt*<br />
- [ ] *wfuzz -u http://machineIP/FUZZ -w /usr/share/wordlists/dirb/common.txt --hc 404*<br />


#### VHOST Enumeration<br />
- [ ] *wfuzz -H 'HEAD: FUZZ.htb' -w ```$Wordlist``` -u http://machineIP --hw 0*<br />

#### FILE Upload<br />
- [ ] *curl --user "{user}:{creds}" --upload-file=<file> "http://machineIP/upload_location"*<br />
  
#### SQL Injection<br />
- [ ] *sqlmap -r <request-file> --level=5 --risk=3 --batch*<br />
  
  
  
  
#### References<br />
  - ##### File Upload Via *[CURL](https://medium.com/@petehouston/upload-files-with-curl-93064dcccc76)*<br />
  - ##### File Upload Via *[CURL & WGET](https://www.ostechnix.com/easy-fast-way-share-files-internet-command-line/)*<br />
