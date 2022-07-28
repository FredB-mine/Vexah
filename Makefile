# Make the os

ipl.bin : ipl.nas Makefile
	../z_tools/nask.exe ipl.nas ipl.bin ipl.lst

VexahOS.img : ipl.bin Makefile
	..\z_tools\edimg.exe   imgin:../z_tools/fdimg0at.tek   wbinimg src:ipl.bin len:512 from:0 to:0   imgout:VexahOS.img

img : 
	..\z_tools\make.exe -r VexahOS.img

asm :
	..\z_tools\make.exe -r ipl.bin

run : 
	..\z_tools\make.exe img
	copy VexahOS.img ..\z_tools\qemu\fdimage0.bin
	..\z_tools\make.exe -C ..\z_tools\qemu

install :
	..\z_tools\make.exe img
	..\z_tools\imgtol.com w a: VexahOS.img