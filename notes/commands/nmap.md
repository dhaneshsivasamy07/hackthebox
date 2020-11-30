#### Nmap
```bash
# normal nmap scan enumerates only open ports
nmap -Pn -vv -sC -sV -oN wr3nch.nmap 10.10.10.10

# nmap full ports scan TCP
nmap -p- -vv -sC -sV -oN wr3nch.nmap 10.10.10.10

# nmap UDP scan
nmap -sU -p- -oN wr3nch.nmap 10.10.10.10

# namp query shown by htb for port enumeratuion
ports=$(nmap -p- --min-rate=1000 -T4 10.10.10.10 | grep ^[0-9] | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)
nmap -p$ports -sC -sV -oN wr3nch.nmap 10.10.10.10

# quick nmap with awk, awk -F 'field seperator' ORS 'displays the multi line output with ,'
nmap -oA nmap/machine 10.10.10.10 | grep open | awk -F/ '{print $1}' ORS=','
```

| Flags | Performance |
| ----- | ----------- |
| -sT   | Performs TCP Scan |
| -sU   | Performs UDP Scan |
| -p-   | Scans All Ports   |
| -v    | Verbosity         |
| -oA   | Output in xml, nmap, gnmap formats |
| -oN   | Output in Nmap Format |
| -oG   | Output in GNmap Format |
| -oX   | Output in xml Format |
| -oS   | Output in ScriptKiddie Format |
