; CopyRight (c) 2022-present, The Vexah Team. All rights reserved.
; Author: The Vexah Team, DrAlfred
; Version: 0.1.2
; Date: 2022-07-28
; License: MIT

; The code to initialize FAT32 Disk

    DB  0xeb, 0x4e, 0x90
    DB  "VexahIPL"          ; The name of the IPL(Initial Program Loader)   IPL名称
    DW  512                 ; The size of Each Sector(must be 512B)         每个扇区的大小(必须是512B)
    DB  1                   ; The number of Sectors per Cluster(must be 1)  每个簇的扇区数(必须是1)
    DW  1                   ; The start of FAT(Normally be 1)               FAT的起始位置(通常是1)
    DB  2                   ; The number of FAT(must be 2)                  FAT的数量(必须是2)
    DW  224                 ; The size of Root Directory(normally be 224)   根目录的大小(通常是224)
    DW  2880                ; The size of The disk(normally be 2880)        磁盘的大小(通常是2880)
    DB  0xf0                ; The media type(normally be 0xf0)              磁盘的媒体类型(通常是0xf0)
    DW  9                   ; The length(sector) of FAT(must be 9)          FAT的长度(必须是9)
    DW  18                  ; How much Sectors in each track(must be 18)    每个磁道的扇区数(必须是18)
    DW  2                   ; The number of heads(must be 2)                磁头的数量(必须是2)
    DD  0                   ; The number of hidden sectors(must be 0)       隐藏的扇区数(必须是0)
    DD  2880                ; Rewrite the length of the disk                重写磁盘的长度
    DB  0, 0, 0x29          ; Reserve
    DD  0xffffffff          ; The signature of the disk(must be 0xffffffff) 磁盘的号码(必须是0xffffffff)
    DB  "Vexah-OS   "       ; The name of the disk(Is Vexah-OS)             磁盘的名称(是Vexah-OS)
    DB  "FAT32   "          ; The type of the disk(Is FAT32)                磁盘的类型(是FAT32)
    RESB    18

; The code to initialize FAT32 Disk End

; The main function of the IPL

    DB  0xb8, 0x00, 0x00, 0x8e, 0xd0, 0xbc, 0x00, 0x7c
    DB  0x8e, 0xd8, 0x8e, 0xc0, 0xbe, 0x74, 0x7c, 0x8a
    DB  0x04, 0x83, 0xc6, 0x01, 0x3c, 0x00, 0x74, 0x09
    DB  0xb4, 0x0e, 0xbb, 0x0f, 0x00, 0xcd, 0x10, 0xeb
    DB  0xee, 0xf4, 0xeb, 0xfd

; The main function of the IPL End

; The info-show function 

    DB  0x0a, 0x0a              ; 2 \n s
    DB  "Hello,Vexah"           ; The info to show
    DB  0x0a                    ; 2 \n s
    DB  0

    RESB   0x1fe-$            ; fill 0x00 until 0x001fe
    DB  0x55, 0xaa              

; The info-show function End

; The output outside of the IPL

    DB  0xf0, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00
    RESB    4600
    DB  0xf0, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00
    RESB    1469432
