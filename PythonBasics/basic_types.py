#Python Basics

x = y = z = 5
z = x+y+z
print(z)

def mul_func():
    global a
    b = 25
    a = x*y*z
    print("Inside Scope:", a)

mul_func()
print("Outside scope: ", a)

# b cannot be accessed outside function
#print("Non Global var:", b)

import random
print(random.randrange(2,6))

"""
Multiple line comments can be added like this
as string literals
"""
c = """
Multiple line string literals
"""
print(c)

#String can be accessed as arrays
print(c[10],c[5],c[2])
print(c[1:6])
print(len(c))
print(c[-31:-15])
#Remove white spaces in beginning/end
print(c.strip())
#Case change
print(c.lower())
print(c.upper())

age = 36
txt = "My name is John, and I am {}"
print(txt.format(age))

quantity = 3
itemno = 567
price = 49.95
myorder = "I want {} pieces of item {} for {} dollars."
print(myorder.format(quantity, itemno, price))

quantity = 3
itemno = 567
price = 49.95
myorder = "I want to pay {2} dollars for {0} pieces of item {1}."
print(myorder.format(quantity, itemno, price))
