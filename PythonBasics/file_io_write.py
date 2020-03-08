#Write operations

file1 = open("example2.txt","w")
file1.write("This is write operation")
file1.close()


with open("example2.txt","a") as file2:
    file2.write("This is appending")

    
with open("example2.txt","r") as file3:
    content = file3.readlines()
    print(content)


with open("sample.txt","r") as file4:
    with open("example2.txt","a") as file5:
        for line in file4:
            file5.write(line)

with open("example2.txt","r") as final:
    content_f = final.readlines()
    print(content_f)
