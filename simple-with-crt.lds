OUTPUT_ARCH(RISCV)
ENTRY(_start)
SECTIONS
{
    __global_pointer$ = 0x00000000;
    _edata = 0x00000000;
    _end = 0x00000000;

    . = 0x0000;
    . = ALIGN(4);

    .text : {
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
