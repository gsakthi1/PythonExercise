
FILE = "test.bin"

def main():
    index = 0
    Length = 0
    contents = []
    f=open(FILE, "r")
    if f.mode == 'r':
       contents =f.read().splitlines()
       Length = len(contents)
    while index < Length:
            print("Item index :", index, "Content:", contents[index])
            index += 1
            

    
if __name__== "__main__":
  main()
