### Network Pivoting 

Scenario:
  We have compromised a web server(Machine A), the web server communicates within a machine(Machine B) inside the corporate netwrok. We cannot directly access the Machine B

Forwarding:
  - Local and Remote port forwarding forwards only a specified service
  - Dynamic Port Forwarding allows a full range of TCP communication across a range of ports

Tools Required:
  - Proxychains in linux

Procedure:

- machine_b's Ip = 10.10.1.1
- Web service hosting inside the machine_b's subnet(10.10.1.0/24) = 10.10.1.5 

```bash
# assume machine B has ssh running
ssh -f -N -D 9050 machine_b@10.10.1.1
# options
# -f = Background the ssh on successful connection
# -N = Dont execute any commands 
# -D = Dynamic port number, the port no., mentioned here should be as of the same value in /etc/proxychains.conf
# Dynamic port value = 9050
# add this in the end of the /etc/proxychains.conf = socks4 127.0.0.1 9050 
```

- Now the Dynamic port forwarding is successful
- If a web service is running on the machine_b_ip's subnet, we can access it from the linux machine with
```bash
proxychains firefox 10.10.1.5
```
 - Normally accessing the 10.10.1.5 will not be displayed. Since we make use of the `proxychains`, the request is sent through the configured dynamic port 9050 which is connected to the machine_b.
 - So the request for accessing 10.10.1.5 is first sent to the 10.10.1.1 through 9050 and is accessed. ( kali -> proxychains:9050 -> 10.10.1.1:9050 -> request for accessing from 10.10.1.1 -> 10.10.1.5:80)
