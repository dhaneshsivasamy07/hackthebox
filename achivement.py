'''
##############################################################################################
 provide your htb user id, machine Id and machine name
 user id : https://www.hackthebox.eu/home/users/profile/220867, 220867 9s the profile id
 machine id: https://www.hackthebox.eu/home/machines/profile/233, 223 is the machine id

required modules
1. requests - pip3 install requests
2. imgkit - pip3 install imgkit


###############################################################################################
'''

import requests
import imgkit

# variables
url_ = "https://www.hackthebox.eu/achievement/machine/"
header = {'User-agent': 'Mozilla/5.0'}

#inputs
userId = input('Enter HackTheBox User ID: ')
macId = input('Enter machine ID: ')
macNam = input("Enter machine name: ")

#processing
dn = url_ + userId + '/' + macId 
r = requests.get (url = dn, headers = header)
if "Invalid" in r.text:
	print("The machine ID seems to be invalid / you havent finished it yet")
else:
	print('Processing the snapshot...')
	imgkit.from_url( dn , macNam +'.jpg')


