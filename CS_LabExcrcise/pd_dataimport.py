import pandas as pd

file = "input.csv"
output = "output.csv"

df = pd.read_csv(file, header = None)
print(df.head(3))
print(df.tail(3))

headers = ['Epoch','Serial','SW_Version','Error_code','Location']
print(headers)
df.columns = headers
df.head(5)

df.to_csv(output)

print(df.describe())  #Statistical summary only numeric
print(df.describe(include = 'all')) # Including objects
print(df.info()) # List top 30 & bottom 30 rows

Serial = df.Serial.unique()
print(len(Serial))
