; CopyRight (c) 2022-present, The Vexah Team. All rights reserved.
; Author: The Vexah Team, DrAlfred
; Version: 0.2.0
; Date: 2022-07-28
; License: MIT

		ORG		0x7c00			; 指明程序的装载地址

; 以下这段是标准FAT12格式化软盘所要的代码

		JMP		entry
		DB		0x90
		DB 	    "VexahIPL"	   ; 启动扇区 长度为8的字符串均可
		DW 	    512			   ; 扇区大小 必须为512
		DB 	    1			   ; 簇大小 必须为1个扇区
		DW   	1              ; FAT的起始位置(一般为1)
		DB 	    2              ; FAT的个数(必须为2)
		DW 	    224			   ; 根目录的大小(一般为224项)
		DW 	    2880		   ; 该磁盘的大小(必须为2880个扇区)
		DB 	    0xf0		   ; 该磁盘的种类(必须为0xf0)
		DW	    9			   ; FAT的长度(必须为9扇区)
		DW      18             ; 一个磁道有几个扇区(必须为18)
		DW      2 			   ; 磁头数字(必须为2)
		DD	    0			   ; 不使用的扇区个数(必须为0)
		DD 	    2880           ; 重写磁盘大小
		DB 	    0,0,0x29	   ; damedane
		DD      0xffffffff     ; 卷标号码
		DB      "Vexah-OS   "  ; 磁盘名称(11字节)
		DB      "FAT32   "     ; 磁盘格式名称(8字节)
		RESB    18			   ; 空出18字节

; 程序核心

entry:
		MOV		AX,0			; 初始化寄存器
		MOV		SS,AX
		MOV		SP,0x7c00
		MOV		DS,AX
		MOV		ES,AX

		MOV		SI,msg
putloop:
		MOV		AL,[SI]
		ADD		SI,1			; 将SI+1
		CMP		AL,0
		JE		fin
		MOV		AH,0x0e			; 显示一个文字
		MOV		BX,15			; 指定其颜色
		INT		0x10			; 调用显卡BIOS
		JMP		putloop
fin:
		HLT						; 让CPU停止
		JMP		fin				; 无限循环

msg:
		DB		0x0a, 0x0a		; 2个换行
		DB		"Hello Vexah"
		DB		0x0a			; 换行
		DB		0

		RESB	0x7dfe-$		; 填写0x00 直到0x07dfe的地址

		DB		0x55, 0xaa
        