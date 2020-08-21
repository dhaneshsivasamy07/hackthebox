#!/bin/python3

import os
import time
import sys
from colorama import Fore, Back, Style

BOLD = '\033[1m'

machine_ = input(str("Enter machine name: "))
ip_ = input(str("Enter machine IP: "))
http_ = ""
https_ = ""
hport_ = int(80)
hsport_ = "443"


def nmap():
    print(BOLD + Fore.BLUE + " \n \n[+]NMAP Enumeration Started \n" + Fore.WHITE)
    nmap_ = 'sudo nmap -Pn -vv -sC -sV -oN {}.nmap {}'.format(machine_, ip_)
    os.system(nmap_)
    print(BOLD + Fore.RED + "[+] NMAP Enumeration Ended \n" + Fore.WHITE)
    print(BOLD + Fore.CYAN + "[+] LOOKING FOR PORTS [+]" + Fore.WHITE)
    ports("{}.nmap".format(machine_))


def ports(scanOutput):
    with open(scanOutput) as outPut:
        if "http" in outPut.read():
            por_ = "grep -w 'http' %s.nmap | cut -d '/' -f 1 | awk 'NR==1{print $1}' | cut -c1-5" % machine_
            print(Fore.LIGHTBLUE_EX + "HTTP Port found in: ")
            global hport_
            hports_ = os.popen(por_).read()
            hport_ = int(hports_)
            print(hport_)
            global http_
            http_ = 1
            direnumeration()

        elif 'https' in outPut.read():
            por_ = "grep -w 'http' %s.nmap | cut -d '/' -f 1 | awk 'NR==1{print $1}' | cut -c1-5" % machine_
            print(Fore.LIGHTBLUE_EX + "HTTP Port found in: ")
            global hsport_
            hports_ = os.popen(por_).read()
            hsport_ = int(hports_)
            print(hsport_)
            global https_
            https_ = 1
            direnumeration()
            
        else:
            print(BOLD + Fore.RED + "HTTP / HTTPS ports are not found")
            print(BOLD + Fore.YELLOW + "Enumerating UDP ports")
            nmapUDP = 'sudo nmap -sU {}'.format(ip_)
            os.system(nmapUDP)



def direnumeration():
    print(BOLD + Fore.MAGENTA + "[+] Directory Enumeration" + Fore.WHITE)
    while http_ :
        gobuster_ ="gobuster dir -u http://{}:{} -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -b 401,402,403,404,502 -x php,html,json,text -t 5 -o go-http.txt".format(ip_, hport_)
        os.system(gobuster_)
        print(BOLD + Fore.RED + '[+] Root Directory Enumerated')
        print(BOLD + Fore.GREEN + "[+]VHost LookUp[+]" + Fore.WHITE)
        vhost()
    
    while https_:
        gobuster_ ="gobuster dir -u http://{}:{} -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -b 401,402,403,404,502 -x php,html,json,text -t 5 -o go-http.txt".format(ip_, hport_)
        os.system(gobuster_)
        print('[+] Root Directory Enumerated')
    print(Fore.BLUE + "[+] Directory enumerated")



def vhost():
    print(BOLD + Fore.YELLOW + "[+] VHOST Checking" + Fore.WHITE)
    vhst = "ffuf -u http://FUZZ/{}:{} -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -sf -fc 401,402,403,404 -of vhost-ffuf.json".format(ip_,hport_)
    os.system(vhst)
    user_ = 'whoami'
    print(BOLD + Fore.RED + "[+] VHOST Enumeration Completed")
    print(BOLD + Fore.LIGHTCYAN_EX + "Every Process is done" + Fore.RESET)
    print(BOLD + Fore.GREEN + "{+} Everthing is done, Meet you soon :")
    os.system(user_)
    sys.exit()



def logo():
    print(Fore.LIGHTGREEN_EX + """                               
                   ____        _                
        __ __ ___ |__ /_ _  __| |_    _ __ _  _ 
        \ V  V / '_|_ \ ' \/ _| ' \ _| '_ \ || |
         \_/\_/|_||___/_||_\__|_||_(_) .__/\_, |
                                     |_|   |__/ 
                        """ + Fore.RESET)



if __name__ == "__main__":
    logo()
    print("Test Version 2.0")
    print(BOLD + 'Coded by a n00b: '+ Fore.BLUE + 'cyberwr3ch' + Fore.LIGHTBLACK_EX + '\nMember of TCSC')
    print(Fore.YELLOW + "Script that scans ports and enumerate dirs for CTF's")
    time.sleep(3)
    nmap()
