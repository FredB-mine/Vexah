# Make VexahOS

default : 
	make run

ipl.bin : ipl.nas Makefile
	../z_tools/nask.exe ipl.nas ipl.bin ipl.lst

VexahOS.img : ipl.bin Makefile
	..\z_tools\edimg.exe   imgin:../z_tools/fdimg0at.tek   wbinimg src:ipl.bin len:512 from:0 to:0   imgout:VexahOS.img

img : 
	make -r VexahOS.img

asm :
	make -r ipl.bin

run : 
	make img
	copy VexahOS.img ..\z_tools\qemu\fdimage0.bin
	make -C ..\z_tools\qemu

install :
	make img
	..\z_tools\imgtol.com w a: VexahOS.img

clean : 
	-del ipl.bin
	-del ipl.lst

src_only : 
	make clean
	-del VexahOS.img