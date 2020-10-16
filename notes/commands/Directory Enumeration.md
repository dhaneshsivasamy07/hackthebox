### Directory Enumeration

- Gobuster
- Wfuzz
- rustbuster

#### Gobuster
```bash
# find files with SecLists worlist
gobuster dir -u http://10.10.*.*/some_dir -w /opt/SecLists/Discovery/Web-Content/raft-small-words.txt -o gobuster-admin_dir-raft-small -x txt,php -b 404
```

#### Wfuzz
```bash
wfuzz -c -v -u http://10.10.*.*/FUZZ  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hc 404
```

#### rustbuster
```bash
# hide status codes with 404 and add extensions php and txt
rustbuster dir -u http://10.10.*.*/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -S 404 -e php,txt -o rustbuster-medium.txt
```
