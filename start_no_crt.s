_start:
  .global _start

  /* set all registers to zero */
  mv  x1, x0
  mv  x2, x1
  mv  x3, x1
  mv  x4, x1
  mv  x5, x1
  mv  x6, x1
  mv  x7, x1
  mv  x8, x1
  mv  x9, x1
  mv x10, x1
  mv x11, x1
  mv x12, x1
  mv x13, x1
  mv x14, x1
  mv x15, x1

  /* stack initilization */
  la   x2, _stack_start

  /* clear BSS */
  la x14, _bss_start
  la x15, _bss_end

  bge x14, x15, zero_loop_end

zero_loop:
  sw x0, 0(x14)
  addi x14, x14, 4
  ble x14, x15, zero_loop
zero_loop_end:

main_entry:
  /* jump to main program entry point (argc = argv = 0) */
  addi x10, x0, 0
  addi x11, x0, 0
  jal x1, main

