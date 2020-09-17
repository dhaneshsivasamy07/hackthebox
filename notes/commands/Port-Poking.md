### Notes to look after:
- [DNS Stuffs](#dns)
- [302 Stuffs](#302)
- [Burp Stuffs](#burp)
- [Mysql Stuffs](#mysql)
- [Passwd Stuffs](#passwd)


#### DNS Things:<a name='dns'></a>
- When DNS port is open on TCP, high chances of `zone transfer`

#### 302 Things:<a name='302'></a>
{BANK}
- When the status code is `302` which is redirect and has a size more than `1kb` then its fishy
- When `302` is found in the response heade, browser looks for the `location` header in the response and redirects there
- When the response form the server is intercepted and 302 is changed to `200 OK`
- The altered response processes and shows a new result than before


#### Burp Things:<a name='burp'></a>
- Automatically find and replace the response code with burp:
   - options -> Match and Replace -> Response Header -> Match: 30[12] FOUND; Replace: 200 OK -> ☑️ Regex match -> ok 
   - This replaces 301 FOUND / 302 FOUND with 200 OK in the response header


#### MySQL Things:<a name='mysql'></a>
- When the creds for mysql is obtained, try to login 
  - `mysql -u <user> -p`
- After logging into mysql `\! /bin/sh` pops a shell (nice to give it a try)

#### Passwd Things:<a name='passwd'></a>
- When `write` permission for the passwd file is found
- Genereate a `crypt` passwd, which is standard unix algorithm
- In the passwd file, `root:x:0:0:root:/root:/bin/bash` replace the `x` with the openssl generated hash
- And su as root
