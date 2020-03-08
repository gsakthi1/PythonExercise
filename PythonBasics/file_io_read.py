#File IO operations


#Open and print characters
file = open("sample.txt",'r')
data = file.read(1)
print(data)
data = file.read(4)
print(data)
data = file.read(8)
print(data)
data = file.read(12)
print(data)
file.close()
print("======1111======")
#Print line by line
file = open("sample.txt",'r')
data = file.readline()
print(data)
data = file.readline()
print(data)
data = file.readline()
print(data)
data = file.readline()
print(data)
file.close()
print("=====2222=======")
#Print Entire content
file = open("sample.txt",'r')
data = file.read()
print(data)
print("=====3333=======")
# Open file using with
example1 = "sample.txt"
with open(example1, "r") as file1:
    FileContent = file1.read()
    print(FileContent)
print("=====444=======")
# Open file using with & looping
with open(example1,"r") as file2:
    i=0
    for line in file2:
#        fileContent = file2.readline()
        i = i+1
        print("Line -",i,"Content - ",line)
print("=====555=======")
with open(example1, "r") as file1:
    FileasList = file1.readlines()
    print(FileasList)
