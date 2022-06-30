# PRTS开发者日志

## Day0

    **准备了汇编以及OS的运行环境**

---

## Day1

### 1) 什么是二进制编辑器(十六进制编辑器)

> 一种直接编写二进制指令,使CPU直接执行的软件
> 
> 一般使用十六进制编写,再转换为16进制

## 2) .img文件的虚拟机运行环境

> 使用Nask进行编译,runbox运行
> 
> 使用complie.bat 自动编译运行

### 3) 初次体验汇编程序 (指令汇总在[Nasm.md](./Nasm.md)中)

#### 1.DB指令

        DB,Define Byte

        往 文件中 直接写入一个字节(或多个字节)

        语法为:DB %d....

```nasm
DB 0xff,0xfd
```

        这句语句的目的,就是往文件里分别依次写入0xff 0xfd

        附录:文件大小单位以及转换

| 名称:    | 位    (Bit) | 字节(Byte)   | 千字节(Kb)       | 兆字节(Mb)     | 千兆字节(GB)    | 千GB  (TB)   |
| ------ | ---------- | ---------- | ------------- | ----------- | ----------- | ----------- |
| **转换** | **/**      | **=8*Bit** | **=1024Byte** | **=1024Kb** | **=1024Mb** | **=1024GB** |

表1.1 数据单位的转换表

#### 2.RESB指令

        RESB,Reserve Byte

        从第一个未被填充的字节开始 ,一直填充0x00,重复指定的次数或者到指定的 文件中地址

        语法为 RESB %d / RESB %d-$

```nasm
RESB 100
```

        往文件中写入100个0x00

```nasm
RESB 0x1fe-$
```

        一直写入0x00,直到`0x1fe`的文件地址

#### 3.注释

        以`;` 开始 同C/C++中的`//`

#### 4.DW指令

        DW,Define Word

        写入2个字节的数据,16位数据

        语法为: DW ...

```nasm
DW 0xff
```

等于:

```nasm
DB 0x00,0xff
```

#### 5.DD指令

        DD,Define Doubleword

        写入4个字节的数据,32位数据

        语法为: DD ...

```nasm
DD 0xff
```

等于:

```nasm
DW 0x00,0xff
```

#### 6.DQ指令

        DQ,Define Quote

        写入4个字节的数据,32位数据

        语法为: DQ ...

```nasm
DQ 0xff
```

等于:

```nasm
DD 0x00,0xff
```

### 4) 专业名词解释

#### 1.TAB=4

        将TAB键的长度设为4个空格键,令源程序更加可读

#### 2.FAT12格式 (FAT32格式)

        这种格式兼容性好,所以我们的IPL也使用了这种格式.

#### 3.启动区

        磁盘的第一个扇区叫做启动区.那么什么是扇区呢?众所周知,计算机读取磁盘的时候,并不是一个字节一个字节读写的.所以他是按区块,也就是扇区读写的

---

## Day2

现在程序有些大的改动,在这里贴上来:

```nasm
; Primitive Rhodesisland Terminal System
; Version:0.0.2
; TAB = 4

        ORG        0x7c00            ; 指明程序的装载地址

; 以下这段是标准FAT12格式化软盘所要的代码

        JMP        entry
        DB         0x90
        DB         "PRTS_IPL"       ; 启动扇区 长度为8的字符串均可
        DW         512               ; 扇区大小 必须为512
        DB         1               ; 簇大小 必须为1个扇区
        DW         1              ; FAT的起始位置(一般为1)
        DB         2              ; FAT的个数(必须为2)
        DW         224               ; 根目录的大小(一般为224项)
        DW         2880           ; 该磁盘的大小(必须为2880个扇区)
        DB         0xf0           ; 该磁盘的种类(必须为0xf0)
        DW         9               ; FAT的长度(必须为9扇区)
        DW         18             ; 一个磁道有几个扇区(必须为18)
        DW         2                ; 磁头数字(必须为2)
        DD         0               ; 不使用的扇区个数(必须为0)
        DD         2880           ; 重写磁盘大小
        DB         0,0,0x29       ; damedane
        DD         0xffffffff     ; 卷标号码
        DB         "PRTS-DISK  "  ; 磁盘名称(11字节)
        DB         "FAT32   "     ; 磁盘格式名称(8字节)
        RESB       18               ; 空出18字节

; 程序核心

entry:
        MOV        AX,0            ; 初始化寄存器
        MOV        SS,AX
        MOV        SP,0x7c00
        MOV        DS,AX
        MOV        ES,AX

        MOV        SI,msg

putloop:
        MOV        AL,[SI]
        ADD        SI,1            ; 将SI+1
        CMP        AL,0
        JE         fin
        MOV        AH,0x0e            ; 显示一个文字
        MOV        BX,15            ; 指定其颜色
        INT        0x10            ; 调用显卡BIOS
        JMP        putloop

fin:
        HLT                        ; 让CPU停止
        JMP        fin                ; 无限循环

msg:
        DB        0x0a, 0x0a        ; 2个换行
        DB        "PRTS_Version:0.0.2"
        DB        0x0a            ; 换行
        DB        0

        RESB      0x7dfe-$        ; 填写0x00 直到0x07dfe的地址

        DB        0x55, 0xaa      ; 作为程序的标识符,只能是0x55,0xaa

; 启动区部分之外的输出

        DB        0xf0, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00
        RESB      4600
        DB        0xf0, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00
        RESB      1469432
```

这段程序里面又有许多新的指令 我们来看看

#### 7.ORG指令

        ORG,origin

        把机器语言装载到指定的内存位置,一般为```0x7c00```
