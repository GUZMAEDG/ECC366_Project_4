print("Project 4 MIPS Simulator")
print("----------")
mem_space = 4096



def simulate(Instr, Hex_Instr):
    print("***** Simulation Start ******\n")
    DIC = 0
    Reg = [0,0,0,0,0,0,0,0]
    PC = 0
    Memory = [0 for i in range(mem_space)]
    
    finished = False
    Cycle = 0
    threeCycles = 0
    fourCycles = 0
    fiveCycles = 0
    
    while(not(finished)):
        line = Instr[PC]
        DIC += 1
        
        if(line[0:32] == '00010000000000001111111111111111'):
            print("PC = " + str(PC*4) + " Instruction: 0x" +  Hex_Instr[PC])
            print("Deadloop. Ending program")
            Cycle += 3
            threeCycles += 1
            finished = True
            
        elif(line[0:6] == '000000' and line[26:32] == '100000'): # ADD
            rd = str(int(line[16:21],2))
            rs = str(int(line[6:11],2))
            rt = str(int(line[11:16],2)) 
            print("Instruction: 0x" +  Hex_Instr[PC])
            print("add $%s, $%s, $%s" %(rd, rs, rt))
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Reg[int(line[16:21],2)] = Reg[int(line[6:11],2)] + Reg[int(line[11:16],2)]

        elif(line[0:6] == '000000' and line[26:32] == '100010'): # SUB
            rd = str(int(line[16:21],2))
            rs = str(int(line[6:11],2))
            rt = str(int(line[11:16],2)) 
            print("Instruction: 0x" +  Hex_Instr[PC])
            print("sub $%s, $%s, $%s" %(rd, rs, rt))
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Reg[int(line[16:21],2)] = Reg[int(line[6:11],2)] - Reg[int(line[11:16],2)]

        elif(line[0:6] == '000000' and line[26:32] == '100110'): # XOR
            rd = str(int(line[16:21],2))
            rs = str(int(line[6:11],2))
            rt = str(int(line[11:16],2)) 
            print("Instruction: 0x" +  Hex_Instr[PC])
            print("xor $%s, $%s, $%s" %(rd, rs, rt))
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Reg[int(rd)] = Reg[int(rs)] ^ Reg[int(rt)]

        
        elif(line[0:6] == '001000'): # ADDI
            rs = str(int(line[6:11],2))
            rt = str(int(line[11:16],2))
            imm = int(line[16:32],2) if line[16]=='0' else -(65535 -int(line[16:32],2)+1)
            print("Instruction: 0x" +  Hex_Instr[PC])
            print("addi $%s, $%s, %s" %(rt, rs, imm))
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Reg[int(rt)] = Reg[int(rs)] + imm

        elif(line[0:6] == '000100'): # BEQ
            rs = str(int(line[6:11],2))
            rt = str(int(line[11:16],2))
            imm = int(line[16:32],2) if line[16]=='0' else -(65535 -int(line[16:32],2)+1)
            print("Instruction: 0x" +  Hex_Instr[PC])
            print("beq $%s, $%s, %s" %(rt, rs, imm))
            print("Taking 3 cycles \n")
            PC += 1
            Cycle += 3
            threeCycles += 1
            PC = PC + imm if (Reg[int(rs)] == Reg[int(rt)]) else PC

        elif(line[0:6] == '000101'): # BNE
            rs = str(int(line[6:11],2))
            rt = str(int(line[11:16],2))
            imm = int(line[16:32],2) if line[16]=='0' else -(65535 -int(line[16:32],2)+1)
            print("Instruction: 0x" +  Hex_Instr[PC])
            print("bne $%s, $%s, %s" %(rt, rs, imm))
            print("Taking 3 cycles \n")
            PC += 1
            Cycle += 3
            threeCycles += 1
            PC = PC + imm if (Reg[int(rs)] != Reg[int(rt)]) else PC

        elif(line[0:6] == '000000' and line[26:32] == '101010'): # SLT
            rd = str(int(line[16:21],2))
            rs = str(int(line[6:11],2))
            rt = str(int(line[11:16],2)) 
            print("Instruction: 0x" +  Hex_Instr[PC])
            print("slt $%s, $%s, $%s" %(rd, rs, rt))
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Reg[int(rd)] = 1 if Reg[int(rs)] < Reg[int(rt)] else 0

        elif(line[0:6] == '100011'):                               # LW
            #Sanity check for word-addressing 
            if (int(line[30:32])%4 != 0 ):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(line,2)))
                exit()
            imm = int(line[16:32],2)
            rs = str(int(line[6:11],2))
            rt = str(int(line[11:16],2))
            print("Instruction: 0x" +  Hex_Instr[PC])
            print("lw $%s, %s($%s)" %(rt, imm, rs))
            print("Taking 5 cycles \n")
            PC += 1
            Cycle += 5
            fiveCycles += 1
            Reg[int(rt)] = Memory[imm + Reg[int(rs)] - 8192] # Load memory into register
 
        elif(line[0:6] == '101011'):                               # SW
            #Sanity check for word-addressing 
            if (int(line[30:32])%4 != 0 ):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(line,2)))
                exit()
            imm = int(line[16:32],2)
            rs = str(int(line[6:11],2))
            rt = str(int(line[11:16],2))
            print("Instruction: 0x" +  Hex_Instr[PC])
            print("sw $%s, %s($%s)" %(rt, imm, rs))
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Memory[imm + Reg[int(rs)] - 8192] = Reg[int(rt)]# Load memory into register
        
        

    print("******** Simulation finished *********\n")
    print("Dynamic Instr Count: ",DIC)
    print("Registers $0-$7: ",Reg)
    print("Total # of Cycles: %s. Break down:" % Cycle)
    print("                    " + str(threeCycles) + " instructions take 3 cycles" )
    print("                    " + str(fourCycles) + " instructions take 4 cycles" )
    print("                    " + str(fiveCycles) + " instructions take 5 cycles" )



def main():
        instr_file = open("i_mem.txt", "r")
        Instruction = []
        Hex_Instruction = []
        
        
        for line in instr_file:
            if(line == "\n" or line[0] == '#'):
                continue
            line = line.replace("\n","")
            Hex_Instruction.append(line)
            line = format(int(line,16),"032b")
            Instruction.append(line)
        
        simulate(Instruction, Hex_Instruction)

        instr_file.close()

if __name__ == "__main__":
    main()
