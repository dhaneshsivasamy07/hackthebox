'''
##############################################################################################
 provide your htb user id, machine Id and machine name
 user id : https://www.hackthebox.eu/home/users/profile/220867, 220867 9s the profile id
 api key can be found in `hackthebox.eu/home/settings`
 enter the machine name and get snapped =)

required modules
1. requests - pip3 install requests
2. imgkit - pip3 install imgkit
wkhtmltopdf to be used by imgkit - sudo apt-get install wkhtmltopdf
3. coloroma - pip install colorama

ISSUE:
If you face error like: `requests.exceptions.SSLError: HTTPSConnectionPool`
please add `,verify= False)` in line 44

###############################################################################################
'''

import requests
import sys
from colorama import Fore, Back, Style
import json
import imgkit

BOLD = '\033[1m'
UNBOLD = "\033[0;0m"


def gen():
	#variables
	URL = 'https://www.hackthebox.eu/api/machines/get/all?api_token='
	api_ = input("Enter your API Key: ")
	URL += api_


	ach_ = 'https://www.hackthebox.eu/achievement/machine/'
	userId = input("Enter your htb id: ")
	macNam = ''

	HEADERS = { 'User-agent': 'Mozilla 5.0'}
	macId = ''
# process
	r = requests.get(url = URL, headers = HEADERS)
	if r.status_code == 200:
		machines = r.json()

		name = input("Machine name: ")
		macNam = name
		for machine in machines:
			if machine['name'].lower() == name.lower():
				macId = str(machine['id'])


	print("==================================================================")
	print("Capturing the " + macNam + " machine")
	print("==================================================================")


	dn = ach_ + userId + '/' + macId
	red = requests.get(url = dn, headers = HEADERS)
	#print(dn)

	if "Invalid" in red.text:
		print("Looks like, you Haven't completed the "+ macNam + "machine yet (>_<)")
	else:
		print("Congratulations on completing the box =D")
		print('Processing the snapshot...')
		imgkit.from_url( dn , macNam +'.jpg')



def logo():
    print(Fore.LIGHTGREEN_EX + """ 

    	                                                               .oooo.                         oooo        
                                                                    .dP""Y88b                        `888        
 .oooo.o ooo. .oo.    .oooo.   oo.ooooo.  oooo oooo    ooo oooo d8b       ]8P' ooo. .oo.    .ooooo.   888 .oo.   
d88(  "8 `888P"Y88b  `P  )88b   888' `88b  `88. `88.  .8'  `888""8P     <88b.  `888P"Y88b  d88' `"Y8  888P"Y88b  
`"Y88b.   888   888   .oP"888   888   888   `88..]88..8'    888          `88b.  888   888  888        888   888  
o.  )88b  888   888  d8(  888   888   888    `888'`888'     888     o.   .88P   888   888  888   .o8  888   888  
8""888P' o888o o888o `Y888""8o  888bod8P'     `8'  `8'     d888b    `8bd88P'   o888o o888o `Y8bod8P' o888o o888o 
                                888                                                                              
                               o888o          

                               """ + Fore.RESET)


if __name__ == "__main__":
    logo()
    print("Simple SnapShot tool by wr3nch")
    print(BOLD + 'Coded by a n00b: '+ Fore.BLUE + 'cyberwr3ch' + Fore.LIGHTBLACK_EX + '\nMember of TCSC' + Fore.RESET)
    print('With the help of my bros, AdithyanAK and Gokul' + UNBOLD)
    gen()
    print("\n Happy Hacking")
