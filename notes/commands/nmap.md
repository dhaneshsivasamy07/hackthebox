#### Nmap
```bash
# quick nmap with awk, awk -F 'field seperator' ORS 'displays the multi line output with ,'
nmap -oA nmap/machine 10.10.*.* | grep open | awk -F/ '{print $1}' ORS=','
```