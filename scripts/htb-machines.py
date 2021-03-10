import requests
import json
import sys
from pwn import *

if len(sys.argv[1:]) != 1:
	print("Usage: {} <htb-api key>".format(sys.argv[0]))
	sys.exit()

url = "https://www.hackthebox.eu/api/machines/get/all?api_token="
api_key = sys.argv[1]
url += api_key
print(url)
headers = {"User-agent": "Mozilla 5.0"}

re = requests.get(url=url, headers=headers)
if re.status_code == 200:
	machines = re.json()
	log.info("Total of {} Machines".format(len(machines)))

	try:
		for i in range(0, len(machines)+1):
			file_ = open("machines.txt", 'a')
			#print("- [ ] {} - {} - {} - {} : {} <br />\n<details>\n<summary>Techniques<\summary>\n - Yet to be completed \n<\details>".format(machines[i]['id'], machines[i]['name'], machines[i]['os'], machines[i]['ip'], machines[i]['rating']))
			lines = "- [ ] {} - {} - {} - {} : {} <br />\n<details>\n\t<summary> Summary of the box </summary>\n - Yet to be completed \n</details> \n\n".format(machines[i]['id'], machines[i]['name'], machines[i]['os'], machines[i]['ip'], machines[i]['rating'])
			file_.write(lines)
			file_.close()

	except IndexError:
		print("All Machines Logged")
		sys.exit()
	except KeyboardInterrupt:
		log.warning("Operation Ended by user")
		sys.exit()


