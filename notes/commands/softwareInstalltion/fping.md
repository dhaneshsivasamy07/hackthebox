### fping

Command for performing ping sweep, (i.e., obtaining IP address of the machines which are accessable from the compromised machine)

#### Installation
```bash
sudo apt-get install fping
```

#### Obtain alive hosts information 
```bash
# Only the specific IP address (192.168.43.1) with the notation 
fping -g 192.168.43.1/32

# ip address from 192.168.43.0 - 192.168.43.255
fping -g 192.168.43.0/24 -q --alive

# ip address from 192.168.0.0 - 192.168.255.255
fping -g 192.168.0.0/16 -q --alive
```
