### Directory Enumeration

- Gobuster
- Wfuzz
- rustbuster

#### Gobuster
```bash
# find files with SecLists worlist
gobuster dir -u http://10.10.*.*/some_dir -w /opt/SecLists/Discovery/Web-Content/raft-small-words.txt -o gobuster-admin_dir-raft-small -x txt,php -b 404
# if proxy needed
add `-p <proxy address>` in the dir mode and vhost mode
```

#### Wfuzz
```bash
wfuzz -c -v -u http://10.10.*.*/FUZZ  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hc 404
# if proxy needed
add `-p <proxy address>` in the dir mode and vhost mode
```

#### rustbuster
```bash
# hide status codes with 404 and add extensions php and txt
rustbuster dir -u http://10.10.*.*/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -S 404 -e php,txt -o rustbuster-medium.txt
```

### VHost enumeration

#### Gobuster
```bash
# If the website resolves to a domain name like something.htb, specify it
gobuster vhost -u http://something.htb/ -w /opt/Seclists/Discovery/DNS/subdomains-top1million-5000.txt
# if proxy needed
add `-p <proxy address>` in the dir mode and vhost mode
```

#### Wfuzz
```bash
Wfuzz -c -v -w /opt/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -u http://10.10.*.*/ -H 'Host: FUZZ.<hostname>.htb'
# if proxy needed
add `-p <proxy address>` in the dir mode and vhost mode
```

#### rustbuster
```bash
# -u specifies the url, -w wordlists, -d resolving name, -x ignore this string
rustbuster vhost -u http://10.10.*.*/ -w custom.txt -d <hostname>.htb -x 'redirect'
```
