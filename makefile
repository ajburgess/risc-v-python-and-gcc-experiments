CROSS_COMPILE=riscv32-unknown-elf-

AS = $(CROSS_COMPILE)as
CC = $(CROSS_COMPILE)gcc
LD = $(CROSS_COMPILE)ld
AR = $(CROSS_COMPILE)ar
GDB = $(CROSS_COMPILE)gdb
OBJCOPY = $(CROSS_COMPILE)objcopy
OBJDUMP = $(CROSS_COMPILE)objdump

.PHONY: clean all dump

CFLAGS = -O0 -march=rv32e -mabi=ilp32e

PROG=main

all: $(PROG).bin

$(PROG).bin: $(PROG).elf
	$(OBJCOPY) -v -O binary $^ $@

main.elf : main.o start_no_crt.o
	$(CC) $(CFLAGS) -nostdlib -T simple.lds $^ -o $@

hello.elf : hello.c
	$(CC) $(CFLAGS) -T simple-with-crt.lds $^ -o $@

main.o : main.c
	$(CC) $(CFLAGS) -c $^ -o $@

start_no_crt.o : start_no_crt.s
	$(CC) $(CFLAGS) -c $^ -o $@

clean:
	rm -f *.a
	rm -f *.o 
	rm -f *.elf
	rm -f *.v
	rm -f *.bin
	rm -f *.md5
	rm -f *.hex
	rm -f *.dmp

# Show the disassembly
dump: $(PROG).elf
	$(OBJDUMP) -d -Mnumeric,no-aliases $(PROG).elf

