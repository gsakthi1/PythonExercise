import pandas as pd

df = pd.read_csv("Serial.csv")
df.head()
print(df.head())
print("-------")
print(df['Serial'])
print("-------")
print(df.loc[0])
print("-------")
print(df.iloc[1,2])
print(df.iloc[0:3,0:3])
print('**************')
print(df[['Serial','Date']])
