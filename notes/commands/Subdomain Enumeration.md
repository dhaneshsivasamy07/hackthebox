### Subdomain Enumeration

- Gobuster
- Wfuzz
- rustbuster

#### Gobuster
```bash
# If the website resolves to a domain name like something.htb, specify it
gobuster vhost -u http://something.htb/ -w /opt/Seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

#### Wfuzz
```bash
Wfuzz -c -v -w /opt/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -u http://10.10.*.*/ -H 'Host: FUZZ.<hostname>.htb'
```

#### rustbuster
```bash
# -u specifies the url, -w wordlists, -d resolving name, -x ignore this string
rustbuster vhost -u http://10.10.*.*/ -w custom.txt -d <hostname>.htb -x 'redirect'
```
