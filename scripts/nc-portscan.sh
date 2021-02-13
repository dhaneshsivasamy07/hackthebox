#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Pass the ip to scan for scan";
  echo "usage: nc-portscan <machine ip>";
  exit 1
fi

echo "looking for open ports in $1"
for i in $(seq 1 65535); do echo "Port: $i"; nc -zv $1 $i 2>&1 | grep open; do
