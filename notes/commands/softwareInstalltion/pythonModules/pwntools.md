### pwntools
<p align="center">
  <img src="https://github.com/arthaud/python3-pwntools/blob/master/docs/source/logo.png" >
</p>

- Whether you’re using it to write exploits, or as part of another software project will dictate how you use it.
- Historically pwntools was used as a sort of exploit-writing DSL. Simply doing from pwn import * in a previous version of pwntools would bring all sorts of nice side-effects.
- When redesigning pwntools for 2.0, we noticed two contrary goals:
- We would like to have a “normal” python module structure, to allow other people to familiarize themselves with pwntools quickly.
- We would like to have even more side-effects, especially by putting the terminal in raw-mode.
- To make this possible, we decided to have two different modules. pwnlib would be our nice, clean Python module, while pwn would be used during CTFs.

### Installation

> Pip3 installation can be found [here](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/softwareInstalltion/python-pip.md#pip3-installation)

```bash
git clone https://github.com/arthaud/python3-pwntools
cd python3-pwntools
pip3 install -e .
```
