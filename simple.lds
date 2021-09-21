OUTPUT_ARCH(RISCV)
ENTRY(_start)
SECTIONS
{
    . = 0x0000;
    . = ALIGN(4);

    .text : {
        start_no_crt.o (.text)
	*(.text)
    }

    .rodata : {
        *(.rodata.*)
    }

    _bss_start = .;
    .bss : {
        *(.bss)
    }
    _bss_end = .;
    _stack_start = 0x10000;
}
