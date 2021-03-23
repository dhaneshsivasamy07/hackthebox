import requests
from bs4 import BeautifulSoup
import hashlib

# session object
session = requests.session()

# variables
url = "http://138.68.171.242:30075/"

# get req
gr = session.get(url=url)
if gr.status_code == 200:
    print("[+] Parsing the contents")
    soup = BeautifulSoup(gr.text ,"html.parser")
    # print(soup)
    print("[+] Identifying the value needed to be hashed")
    val = soup.find_all("h3")[0].text
    # print(val)
    print(f"[+] {val} Needs to be MD5'ed")
    tmp = bytes(val.encode())
    md5val = hashlib.md5(tmp).hexdigest()
    print(f"[+] MD5ed value of {val} is {md5val}")
    print("[*] Sending the request")
    data = dict(hash=md5val)
    print(data)
    pr = session.post(url=url, data=data)
    #print(pr.text)
    if "HTB" in pr.text:
        print("*"*25)
        fg = BeautifulSoup(pr.text, 'html.parser')
        flag = fg.find_all('p')[0].text
        print(flag)
        print("*" * 25)