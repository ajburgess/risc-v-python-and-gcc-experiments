X0 = ZERO = 0
X1 = RA = 1
X2 = 2
X3 = 3
X4 = 4
X5 = 5
X6 = 6
X7 = 7
X8 = 8
X9 = 9
X10 = 10
X11 = 11
X12 = 12
X13 = 13
X14 = 14
X15 = 15

memory = []
pc = 0
registers = [0x00000000] * 15

def bit(value, index):
    return (value >> index) & 1 == 1

def shift(value, from_index, down_to_index):
    width = from_index - down_to_index + 1
    result = 0
    for i in range(0, width):
        b = bit(value, i)
        result = result | (b << down_to_index + i)
    return result

def instruction(parts):
    result = 0
    for part in parts:
        result = result | shift(part[0], part[1], part[2])
    return result

def i_format(imm12, rs1, func3, rd, opcode):
    return instruction([(imm12, 31, 20), (rs1, 19, 15), (func3, 14, 12), (rd, 11, 7), (opcode, 6, 0)])

def shift_i_format(is_arithmetic, shamt, rs1, func3, rd, opcode):
    extra = 0x20 if is_arithmetic else 0x00
    return instruction([(extra, 31, 25), (shamt, 24, 20), (rs1, 19, 15), (func3, 14, 12), (rd, 11, 7), (opcode, 6, 0)])

def u_format(imm20, rd, opcode_high, opcode_low):
    return instruction([(imm20, 31, 12), (rd, 11, 7), (opcode_high, 6, 2), (opcode_low, 1, 0)])

def b_format(rs1, rs2, imm13_even_only, function3, opcode_high, opcode_low):
    imm_bit_12 = extract(imm13_even_only, 12, 12)
    imm_bit_11 = extract(imm13_even_only, 11, 11)
    imm_bits_10_to_5 = extract(imm13_even_only, 10, 5)
    imm_bits_4_to_1 = extract(imm13_even_only, 4, 1)
    return instruction([(imm_bit_12, 31, 31), (imm_bits_10_to_5, 30, 25), (rs2, 24, 20), (rs1, 19, 15), (function3, 14, 12), (imm_bits_4_to_1, 11, 8), (imm_bit_11, 7, 7), (opcode_high, 6, 2), (opcode_low, 1, 0)])

def beq(rs1, rs2, offset13_even_only):
    return b_format(rs1, rs2, offset13_even_only, 0x00, 0x18, 0x03)

def bne(rs1, rs2, offset13_even_only):
    return b_format(rs1, rs2, offset13_even_only, 0x01, 0x18, 0x03)

def blt(rs1, rs2, offset13_even_only):
    return b_format(rs1, rs2, offset13_even_only, 0x04, 0x18, 0x03)

def bge(rs1, rs2, offset13_even_only):
    return b_format(rs1, rs2, offset13_even_only, 0x05, 0x18, 0x03)

def bltu(rs1, rs2, offset13_even_only):
    return b_format(rs1, rs2, offset13_even_only, 0x06, 0x18, 0x03)

def bgeu(rs1, rs2, offset13_even_only):
    return b_format(rs1, rs2, offset13_even_only, 0x07, 0x18, 0x03)

def addi(rd, rs1, imm12):
    return i_format(imm12, rs1, 0x00, rd, 0x13)

def slti(rd, rs1, imm12):
    return i_format(imm12, rs1, 0x02, rd, 0x13)

def sltiu(rd, rs1, imm12):
    return i_format(imm12, rs1, 0x03, rd, 0x13)

def xori(rd, rs1, imm12):
    return i_format(imm12, rs1, 0x04, rd, 0x13)

def ori(rd, rs1, imm12):
    return i_format(imm12, rs1, 0x06, rd, 0x13)

def andi(rd, rs1, imm12):
    return i_format(imm12, rs1, 0x07, rd, 0x13)

def slli(rd, rs1, shamt):
    return shift_i_format(False, shamt, rs1, 0x01, rd, 0x13)

def srli(rd, rs1, shamt):
    return shift_i_format(False, shamt, rs1, 0x05, rd, 0x13)

def srai(rd, rs1, shamt):
    return shift_i_format(True, shamt, rs1, 0x05, rd, 0x13)

def lui(rd, imm20):
    return u_format(imm20, rd, 0x0D, 0x03)

def auipc(rd, imm20):
    return u_format(imm20, rd, 0x05, 0x03)

def demo1():
    global memory
    memory = [
        # addi(X5, X0, 1000),
        # addi(X6, X0, 2000),
        # addi(X7, X6, 500),
        # addi(X8, X6, -1),
        # addi(X9, ZERO, 0x7ff),
        # lui(X9, 0xDEADC),
        # addi(X9, X9, 0xEEF),
        # auipc(X10, 0x7ffff),
        # auipc(X10, -16),
        addi(X5, ZERO, -122),  #0000
        addi(X6, ZERO, 123),   #0004
        bltu(X5, X6, 8),       #0008
        addi(X7, ZERO, 1),     #000C
        addi(X7, ZERO, 2),     #0010
        0x00000000]
    run()

def run():
    global pc, registers
    pc = 0
    for n in range(len(registers)):
        registers[n] = 0x00000000

    print()

    while True:
        pc_before = pc
        instruction = memory[int(pc / 4)]
        
        if instruction == 0:
            break
        
        description = decode_and_execute(instruction)        

        print(f"PC  = {hex32(pc_before)} {description}\n")
        print_registers()
        print()
        input("Enter to continue...")

def to_signed(value, width):
    raw_value = extract(value, width - 1, 0)
    if bit(value, width - 1) == 1:
        return raw_value - 2 ** width
    else:
        return raw_value

def to_unsigned(value, width):
    raw_value = extract(value, width - 1, 0)
    return raw_value

def extract(instruction, from_bit, down_to_bit):
    width = from_bit - down_to_bit + 1
    mask = 2 ** width - 1
    value = instruction >> down_to_bit & mask
    return value

def decode_and_execute(instruction):
    global pc
    opcode_low = extract(instruction, 1, 0)
    opcode_high = extract(instruction, 6, 2)
    func3 = extract(instruction, 14, 12)
    rd = extract(instruction, 11, 7)
    rs1 = extract(instruction, 19, 15)
    if opcode_low == 0x03:
        if opcode_high == 0x04:
            imm = extract(instruction, 31, 20)
            signed_value = to_signed(imm, 12)
            if func3 == 0x00:
                description = f"addi x{rd},x{rs1},{signed_value}"
                registers[rd] = registers[rs1] + signed_value
                pc = pc + 4
            elif func3 == 0x02:
                description = f"slti x{rd},x{rs1},{signed_value}"
                raise Exception("Instruction SLTI not implemented yet")
                pc = pc + 4
            elif func3 == 0x03:
                description = f"sltiu x{rd},x{rs1},{signed_value}"
                raise Exception("Instruction SLTIU not implemented yet")
                pc = pc + 4
            elif func3 == 0x04:
                description = f"xori x{rd},x{rs1},{signed_value}"
                raise Exception("Instruction XORI not implemented yet")
                pc = pc + 4
            elif func3 == 0x06:
                description = f"ori x{rd},x{rs1},{signed_value}"
                raise Exception("Instruction ORI not implemented yet")
                pc = pc + 4
            elif func3 == 0x07:
                description = f"andi x{rd},x{rs1},{signed_value}"
                raise Exception("Instruction ANDI not implemented yet")
                pc = pc + 4
        elif opcode_high == 0x0D:
            imm20 = extract(instruction, 31, 12)
            effective_value = imm20 << 12
            description = f"lui x{rd},{imm20} # {hex32(effective_value)}"
            registers[rd] = effective_value
            pc = pc + 4
        elif opcode_high == 0x05:
            imm20 = extract(instruction, 31, 12)
            signed_value = to_signed(imm20)
            description = f"auipc x{rd},{signed_value}"
            registers[rd] = pc + signed_value
            pc = pc + 4
        elif opcode_high == 0x18:
            rs2 = extract(instruction, 24, 20)
            imm_bit_12 = extract(instruction, 31, 31)
            imm_bits_10_to_5 = extract(instruction, 30, 25)
            imm_bits_4_to_1 = extract(instruction, 11, 8)
            imm_bit_11 = extract(instruction, 7, 7)
            imm13 = imm_bit_12 << 12 | imm_bit_11 << 11 | imm_bits_10_to_5 << 5 | imm_bits_4_to_1 << 1
            signed_offset = to_signed(imm13, 13)
            rs1_unsigned_value = to_unsigned(registers[rs1], 32)
            rs2_unsigned_value = to_unsigned(registers[rs2], 32)
            rs1_signed_value = to_signed(registers[rs1], 32)
            rs2_signed_value = to_signed(registers[rs2], 32)
            branch_address = pc + signed_offset
            if func3 == 0x00:
                description = f"beq x{rs1},x{rs2},{signed_offset} # {hex32(branch_address)}"
                if rs1_signed_value == rs2_signed_value:
                    pc = branch_address
                else:
                    pc = pc + 4
            elif func3 == 0x01:
                description = f"bne x{rs1},x{rs2},{signed_offset} # {hex32(branch_address)}"
                if rs1_signed_value != rs2_signed_value:
                    pc = branch_address
                else:
                    pc = pc + 4
            elif func3 == 0x04:
                description = f"blt x{rs1},x{rs2},{signed_offset} # {hex32(branch_address)}"
                if rs1_signed_value < rs2_signed_value:
                    pc = branch_address
                else:
                    pc = pc + 4
            elif func3 == 0x05:
                description = f"bge x{rs1},x{rs2},{signed_offset} # {hex32(branch_address)}"
                if rs1_signed_value >= rs2_signed_value:
                    pc = branch_address
                else:
                    pc = pc + 4
            elif func3 == 0x06:
                description = f"bltu x{rs1},x{rs2},{signed_offset} # {hex32(branch_address)}"
                if rs1_unsigned_value < rs2_unsigned_value:
                    pc = branch_address
                else:
                    pc = pc + 4
            elif func3 == 0x07:
                description = f"bgeu x{rs1},x{rs2},{signed_offset} # {hex32(branch_address)}"
                if rs1_unsigned_value >= rs2_unsigned_value:
                    pc = branch_address
                else:
                    pc = pc + 4

    if description is None:
        raise Exception(f"Instruction {hex32(instruction)} not recognised")

    registers[0] = 0
    return description

def hex32(value):
    return f"0x{tohex(value, 32).zfill(8)}"

def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))[2:]

def print_registers():
    for r in range(len(registers)):
        value = registers[r]
        print(f"X{str(r).ljust(2)} = {hex32(value)} ({value})")

def bin_chopped(value, sizes):
    initial_text = bin(value)[2:].zfill(32)
    chopped_text = ""
    pos = 0
    for size in sizes:
        chopped_text = chopped_text + initial_text[pos:pos + size]
        chopped_text = chopped_text + " "
        pos = pos + size
    return chopped_text

if __name__ == "__main__":
    demo1()
    # instr = srai(15, 1, 15)
    # print(bin_chopped(instr, [12, 5, 3, 5, 7]))
