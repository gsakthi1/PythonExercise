# List - Can do everything []
a = ["sakthi","srishti","shanthi"]
print(a)

print(a[2])

print(a[0:3])

for x in a:
    print('Looping : ',x)

a.append("shakthi")
print(len(a))

if 'shakthi' in a:
    print("shakthi present")
else:
    print("shakthi Not present")

#Tuple - Cannot remove an item, can add items. ()
thistuple = ("apple", "banana", "cherry")
print(thistuple)

thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[2:5])

tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)
tuple3 = tuple1 + tuple2
print(tuple3) 

#Sets - Unordered, Unindexed {} items
thisset = {"Set_apple", "Set_banana", "Set_cherry"}
#Order of print will vary as the items are unordered
for x in thisset:
  print(x) 
thisset.add("orange")
thisset.update(["up1",'up2','up3'])

set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}
set3 = set1.union(set2)
print(set3)

#Dictonaries - Unordered, Unindexed {} items (Key - Value Pairs)
thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict["model"])
print(thisdict.get("brand"))
thisdict["year"] = 2018

#Print keys
for x in thisdict:
    print("Keys :" ,x)

#Print values
for x in thisdict:
    print("Values 1:" ,thisdict[x])
for x in thisdict.values():
    print("Values 2:" ,x)
for x, y in thisdict.items():
  print("Both:", x, y)

#Nested dictionaries
child1 = {
  "name" : "Emil",
  "year" : 2004
}
child2 = {
  "name" : "Tobias",
  "year" : 2007
}
child3 = {
  "name" : "Linus",
  "year" : 2011
}

myfamily = {
  "child1" : child1,
  "child2" : child2,
  "child3" : child3
}
print(myfamily)

child4 = child3
print(child4)
child4["year"] = 2019
print(myfamily)

childy = child2.copy()
childy["year"] = 2020
