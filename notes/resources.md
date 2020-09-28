### CMS Exploits
- [Bludit Code Execution](https://github.com/bludit/bludit/issues/1081)
- [Tomcat Exploitation](https://www.hackingarticles.in/multiple-ways-to-exploit-tomcat-manager/)
- [Litecart Exploitation](https://www.exploit-db.com/exploits/45267)
- [GYM management System](https://www.exploit-db.com/exploits/48506)


### CVE's And PoC's

#### Windows
- Windows 10 IoT [exploit](https://www.zdnet.com/article/new-exploit-lets-attackers-take-control-of-windows-iot-core-devices/) and its [PoC](https://github.com/SafeBreach-Labs/SirepRAT)

#### Apache Tomcat
- Apache Tomcat Verison 7.x [RCE](https://www.redtimmy.com/apache-tomcat-rce-by-deserialization-cve-2020-9484-write-up-and-exploit/) and its [PoC](https://github.com/masahiro331/CVE-2020-9484)

#### PrivEsc Articles
- PrivEsc when [USBCreator](https://unit42.paloaltonetworks.com/usbcreator-d-bus-privilege-escalation-in-ubuntu-desktop/) is provided with SUID and running with the root privileges
- Compromising system with [mysql](https://recipeforroot.com/mysql-to-system-root/)
- PrivEsc via Splunk [detailed-article](https://medium.com/@airman604/splunk-universal-forwarder-hijacking-5899c3e0e6b2) and [discussion](https://www.securityfocus.com/bid/101664/discuss) what will be happening if the exploit is leveraged, [PoC](https://github.com/cnotin/SplunkWhisperer2)

#### Docker Security
- What happens if [docker.sock](https://dejandayoff.com/the-danger-of-exposing-docker.sock/) is explosed.
- Docker.sock exposure [medium](https://medium.com/better-programming/about-var-run-docker-sock-3bfd276e12fd) post by [Luc Juggery](https://medium.com/@lucjuggery)
- Multiple Docker Security [articles](https://securityboulevard.com/2019/02/abusing-docker-api-socket/)
- LXD privEsc, happens when the user belongs to the [lxd](https://www.hackingarticles.in/lxd-privilege-escalation/) group.

### Useful Things
- File Upload Via *[CURL](https://medium.com/@petehouston/upload-files-with-curl-93064dcccc76)*<br />
- File Upload Via *[CURL & WGET](https://www.ostechnix.com/easy-fast-way-share-files-internet-command-line/)*<br />
- Obtaining Network Statistics when netstat is [not available](https://staaldraad.github.io/2017/12/20/netstat-without-netstat/)<br />
- Get a *[TTY Shell](https://netsec.ws/?p=337)* <br />
- Get <b>pip</b> installed in oneliner:
	```python
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py; python get-pip.py
	```
- Bypass php [disabled_functions](https://packetstormsecurity.com/files/154728/PHP-7.3-disable_functions-Bypass.html) from PHP verison 7.x - 7.3
