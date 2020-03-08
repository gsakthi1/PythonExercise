# import pandas as pd
# https://www.geeksforgeeks.org/python-pandas-dataframe/

import pandas as pd
 
# list of strings
lst = ['Geeks', 'For', 'Geeks', 'is', 'portal', 'for', 'Geeks']
 
# Calling DataFrame constructor on list
df = pd.DataFrame(lst)
print(df)

print("--------------")
# intialise data of lists.
data = {'Name':['Tom', 'nick', 'krish', 'jack'],
        'Age':[20, 21, 19, 18]}
 
# Create DataFrame
df = pd.DataFrame(data)
 
# Print the output.
print(df)

print("--------------")

# Define a dictionary containing employee data
data = {'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'],
        'Age':[27, 24, 22, 32],
        'Address':['Delhi', 'Kanpur', 'Allahabad', 'Kannauj'],
        'Qualification':['Msc', 'MA', 'MCA', 'Phd']}
 
# Convert the dictionary into DataFrame 
df = pd.DataFrame(data)

print(df[['Name','Qualification']])

# making data frame from csv file
data = pd.read_csv("nba.csv", index_col ="Name")
 
# retrieving row by loc method
first = data.loc["Avery Bradley"]
second = data.loc["R.J. Hunter"]
iloc_1 = data.iloc[0]
iloc_00 = data.iloc[0][0] 
iloc_11 = data.iloc[1][1]
iloc_12 = data.iloc[1][2]

print(first, "\n\n\n", second, "\n\n\n")
print("%%%%%%%%%%%%%%")
print("iloc - 0", iloc_1)
print("iloc -0", iloc_00)
print("iloc -11", iloc_11)
print("iloc -12", iloc_12)



