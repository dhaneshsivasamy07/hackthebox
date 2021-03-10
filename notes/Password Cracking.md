### Password Cracking

- hashcat 
- John

```bash
# get the mode of cracking with hashcat
hashcat --example-hashes | grep -B4 'hash_starting'

# crack the hashes with the specified mode
hashcat -m xxxx hashes.txt /usr/share/wordlists/rockyou.txt

# view the cracked password when hashcat is done cracking
hashcat -m xxxx hashes.txt --show
```

```bash
# crack hashes with John
john -w=/usr/share/wordlists/rockyou.txt hashes.txt
```

```bash
# crack the password protected zip file
zip2john \<zipfile\> \> zipfile.hash
john  --format=zip zipfile.hash --wordlist=/usr/share/wordlists/rockyou.txt
```
