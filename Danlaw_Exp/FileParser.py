import os

Input = "24130.txt"
Output = "24130MemoryUsage.txt"

Input_1 = "24130current_mem_info.txt"   
Output_1 = "24130ProcessDetails.txt"

if os.path.exists(Output):
    os.remove(Output)
if os.path.exists(Output_1):
    os.remove(Output_1)

file_op = open(Output,"a")

with open (Input,'rt') as myfile:
    for myline in myfile:
        if(myline.find('UTC') >= 0):
           myline = myline.rstrip()
           file_op.write(myline)
           file_op.write('  ')
           continue       
        if(myline.find('RAM Usage') >= 0):
            myline = myline.rstrip()
            file_op.write(myline)
            file_op.write('  ')
            continue
        if(myline.find('CACHE Usage') >= 0):
            file_op.write(myline)

file_op.close()

file_op_1 = open(Output_1,"a")
with open (Input_1,'rt') as myfile:
    for myline in myfile:
        if(myline.find('PID') >= 0):
           myline = myline.rstrip()
           file_op_1.write(myline)
           file_op_1.write('  ')
           continue       
        if(myline.find('COMMAND') >= 0):
            myline = myline.rstrip()
            file_op_1.write(myline)
            file_op_1.write('  ')
            continue
        if(myline.find('PSS_MEMORY') >= 0):
            myline = myline.rstrip()
            file_op_1.write(myline)
            file_op_1.write('  ')
            continue
        if(myline.find('RSS_MEMORY') >= 0):
            file_op_1.write(myline)

file_op_1.close()
print('Output file created')
