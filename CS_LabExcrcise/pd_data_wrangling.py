import pandas as pd
import matplotlib.pylab as plt
import numpy as np

#filename = "https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/auto.csv"
filename = "auto.csv"

headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]

df = pd.read_csv(filename,names = headers)

print(df.head())

df.replace("?",np.nan,inplace=True)
print(df.head())

missing_data_0 = df.isnull()
print(missing_data_0.head())

missing_data_1 = df.notnull()
print(missing_data_1.head())

#Identify the missing data in each column
for column in missing_data_0.columns.values.tolist():
    print(column)
    print (missing_data_0[column].value_counts())
    print("")    

#Replace the missing contents by mean
avg_norm_loss = df["normalized-losses"].astype("float").mean(axis=0)
print("Average of normalized-losses:", avg_norm_loss)
df["normalized-losses"].replace(np.nan,avg_norm_loss,inplace=True)

avg_bore = df["bore"].astype("float").mean(axis=0)
print("Avg bore",avg_bore)
df["bore"].replace(np.nan,avg_bore,inplace=True)

avg_stroke = df["stroke"].astype("float").mean(axis=0)
print("Avg bore",avg_stroke)
df["stroke"].replace(np.nan,avg_stroke,inplace=True)

avg_horsepower = df['horsepower'].astype('float').mean(axis=0)
print("Average horsepower:", avg_horsepower)
df['horsepower'].replace(np.nan, avg_horsepower, inplace=True)

avg_peakrpm=df['peak-rpm'].astype('float').mean(axis=0)
print("Average peak rpm:", avg_peakrpm)
df['peak-rpm'].replace(np.nan, avg_peakrpm, inplace=True)

#Replace the missing contents by frequency
print(df['num-of-doors'].value_counts())      #Values present in particular column
print(df['num-of-doors'].value_counts().idxmax())   #Most common type
df["num-of-doors"].replace(np.nan, "four", inplace=True)

#Delete the entire row
df.dropna(subset=["price"], axis=0, inplace=True)
# reset index, because we droped two rows
df.reset_index(drop=True, inplace=True)

#Checking for missing values after cleaning data
print(df.isnull())
print(df.dtypes) # List all data types of data frame

#Convert to proper data type
df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
df[["price"]] = df[["price"]].astype("float")
df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")

# Convert mpg to L/100km by mathematical operation (235 divided by mpg)
df['city-L/100km'] = 235/df["city-mpg"]
# transform mpg to L/100km by mathematical operation (235 divided by mpg)
df["highway-mpg"] = 235/df["highway-mpg"]

# rename column name from "highway-mpg" to "highway-L/100km"
df.rename(columns={'"highway-mpg"':'highway-L/100km'}, inplace=True)

#Normalization
# replace (original value) by (original value)/(maximum value)
df['length'] = df['length']/df['length'].max()
df['width'] = df['width']/df['width'].max()
df["height"]=df["height"]/df["height"].max()

#Binning
df["horsepower"]=df["horsepower"].astype(int, copy=True)  #Change format to int

import matplotlib as plt
from matplotlib import pyplot
plt.pyplot.hist(df["horsepower"])

# set x/y labels and plot title
plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")

bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]), 4)
print(bins)

group_names = ['Low', 'Medium', 'High']
df['horsepower-binned'] = pd.cut(df['horsepower'], bins, labels=group_names, include_lowest=True )
df[['horsepower','horsepower-binned']].head(20)

print(df["horsepower-binned"].value_counts())

import matplotlib as plt
from matplotlib import pyplot
pyplot.bar(group_names, df["horsepower-binned"].value_counts())

# set x/y labels and plot title
plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")

#Indicator variables to help any future regression models
dummy_variable_1 = pd.get_dummies(df["fuel-type"])
print(dummy_variable_1.head())
dummy_variable_1.rename(columns={'fuel-type-gas':'gas', 'fuel-type-diesel':'diesel'}, inplace=True)
print(dummy_variable_1.head())

# merge data frame "df" and "dummy_variable_1" 
df = pd.concat([df, dummy_variable_1], axis=1)

# drop original column "fuel-type" from "df"
df.drop("fuel-type", axis = 1, inplace=True)

dummy_variable_2 = pd.get_dummies(df["aspiration"])
dummy_variable_2.rename(columns={'std':'aspiration-std', 'turbo':'aspiration-turbo'}, inplace=True)
dummy_variable_2.head()

#merge the new dataframe to the original datafram
df = pd.concat([df, dummy_variable_2], axis=1)
# drop original column "aspiration" from "df"
df.drop('aspiration', axis = 1, inplace=True)


df.to_csv('clean_df.csv')

