; CopyRight (c) 2022-present, The Vexah Team. All rights reserved.
; Author: The Vexah Team, DrAlfred
; Version: 0.2.0
; Date: 2022-07-28
; License: MIT

		ORG		0x7c00			; 这个程序会被读入哪里

; 以下是标准FAT12格式软盘的记述

		JMP		entry
		DB		0x90
		DB		"Vexah-OS"		; 可以自由写引导扇区的名称（8字节）
		DW		512				; 1个扇区的大小（必须为512）
		DB		1				; 群集大小（必须为一个扇区）
		DW		1				; FAT从哪里开始（一般从第一个扇区开始）
		DB		2				; FAT个数（必须为2）
		DW		224				; 根目录区域的大小（通常为224个条目）
		DW		2880			; 此驱动器的大小（必须为2880个扇区）
		DB		0xf0			; 介质类型（必须为0xf0）
		DW		9				; FAT区域长度（必须为9个扇区）
		DW		18				; 一个磁道有多少个扇区（必须是18）
		DW		2				; 头数（必须为2）
		DD		0				; 因为没有使用分区，所以这里一定是0
		DD		2880			; 再写一次这个驱动器的大小
		DB		0,0,0x29		; 虽然不太清楚，但是这个价格就好了
		DD		0xffffffff		; 可能是卷序列号
		DB		"Vexah      "	; 磁盘名称（11字节）
		DB		"FAT12   "		; 格式名称（8字节）
		RESB	18				; 先打18个字节

; 程序主体

entry:
		MOV		AX,0			; 寄存器初始化
		MOV		SS,AX
		MOV		SP,0x7c00
		MOV		DS,AX

; 读磁盘

		MOV		AX,0x0820
		MOV		ES,AX
		MOV		CH,0			; 气缸0
		MOV		DH,0			; 头部0
		MOV		CL,2			; 扇区2

		MOV		AH,0x02			; AH=0x02:磁盘读取
		MOV		AL,1			; 一个扇区
		MOV		BX,0
		MOV		DL,0x00			; A驱动器
		INT		0x13			; 磁盘BIOS调用
		JC		error

; 虽然读完了，但总之没什么要做的，所以睡觉

fin:
		HLT						; 停止处理器直到出现问题
		JMP		fin				; 无限循环

error:
		MOV		SI,msg
putloop:
		MOV		AL,[SI]
		ADD		SI,1			; SI加1
		CMP		AL,0
		JE		fin
		MOV		AH,0x0e			; 单字显示功能
		MOV		BX,15			; 彩色编码
		INT		0x10			; 视频BIOS调用
		JMP		putloop
msg:
		DB		0x0a, 0x0a		; 两个换行符
		DB		"load error"
		DB		0x0a			; 改行
		DB		0

		RESB	0x7dfe-$		; 用0x00填满0x7dfe的命令

		DB		0x55, 0xaa
