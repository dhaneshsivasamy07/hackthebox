# Reversing

## Debuggers
- [IDA Hex Rays](https://www.hex-rays.com/products/ida/support/download_freeware/)
- [Ghidra](https://ghidra-sre.org/)
- [Radare2](https://rada.re/n/radare2.html)
- [Cutter](https://cutter.re/)
- [GDB](https://www.gnu.org/software/gdb/)
- [pwntools](https://github.com/Gallopsled/pwntools)

## Commands

- [GDB](#gdb)
- [Radare2](#r2)
- [Misc](#misc)

### gdb <a name='gdb'></a>
```bash
# gdb
# load the binary
gdb ./binary

# gather information about the available functions in the binary
info functions

# disassemble a function
disassemble {function-name}  # disassemble main

# change disassemble method from AT&T format to INTEL format
set disassembly-flavor intel # views instructions in intel format
set disassembly-flavor att   # views instructions in AT&T format

# set a breakpoint at a specific address
break *{memory-adddress}     # break *0x000011c6

# run the progam until it reaches the breakpoint
r

# move to next instruction
n

# step to next instruction
s

# gather information about the contents of the registers
info registers

# gather information on flags
p $eflags

# view the contents of the stack
# prints 20 bytes of hexdata from the memory address held by esp
x/20x $esp # esp is referenced since it changes value on pushing and popping things in/out of the stack
```

### radare2 / r2 <a name='r2'></a>
```bash
# r2
# open the files in disassemble mode
r2 -d ./binary

# analyze all the available symbols, datas etc..,
aaa

# list the available functions in the binary
afl

# move to a function
s {function-name}            # s main

# print the disassmbled function
pdf

# disassemble a function with function name
pdf @{function-name}        # pdf @sym.vuln

# create a breakpoint                                                    ------------
db {memory-address}         # db 0x5662a1ef                                           |
                                                                                      |
# run until breakpoint is reached                                                     |
dc                                                                                    |
                                                                                      |
# run until a call instruction is reached                                             |===============> debugger Commands 
dcc                                                                                   |
                                                                                      |
# run until a ret instruction is reached                                              |
dcr                                                                                   |
                                                                                      |
# move to next instruction                                               ------------
ds


# switch to visual mode
## Visual mode commands are specified with ## prefix
V  # gives stack view of the program

## switch to interactive mode where stack, registers, disassembly are shown
!

## split the panes
| # vertical split
- # horizontal split

## add new section
# wide options will be shown like breakpoints, hexdumps, functions etc..,
<ctrl> + "   

## execute commands in visual mode
: {debugger-command} # :dcc

## restart the execution with same breakpoints
: ood

## Quit the visual mode
q

# quit r2 without confirmation
Q
```

### Misc <a name='misc'></a>
```bash
# know the security implementaions on the binary
checksec --file ./binary

# know the functions in the binary
readelf --syms ./binary

# obtain spectif section's data
readelf -sj {section-name} ./binary # readelf -sj .rodata ./binary

# otain the crash message
dmesg
```