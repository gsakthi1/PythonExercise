import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

path='https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/automobileEDA.csv'
#filename = 'auto.csv'

df = pd.read_csv(path)
print(df.head())
      
#Correlation for all columns
df.corr()

# Selecting specific columns for correlation
df[['bore','stroke' ,'compression-ratio','horsepower']].corr()

# Engine size as potential predictor variable of price
sns.regplot(x="engine-size", y="price", data=df)
plt.ylim(0,)
df[["engine-size", "price"]].corr()  #Positive correlation
plt.show()

sns.regplot(x="highway-mpg", y="price", data=df)
df[['highway-mpg', 'price']].corr()  #Neative correlation
plt.show()

sns.regplot(x="peak-rpm", y="price", data=df)
df[['peak-rpm','price']].corr()  #Weak correlation
plt.show()

sns.boxplot(x="body-style", y="price", data=df) #Box plot for categorical data
plt.show()

sns.boxplot(x="engine-location", y="price", data=df)
plt.show()

sns.boxplot(x="drive-wheels", y="price", data=df)
plt.show()

df['drive-wheels'].value_counts() # Counting of variable repeatability

drive_wheels_counts = df['drive-wheels'].value_counts().to_frame()  #Convert to data frame
drive_wheels_counts.rename(columns={'drive-wheels': 'value_counts'}, inplace=True)  #Change column name
drive_wheels_counts.index.name = 'drive-wheels'    #Change index column name

# engine-location as variable
engine_loc_counts = df['engine-location'].value_counts().to_frame()
engine_loc_counts.rename(columns={'engine-location': 'value_counts'}, inplace=True)
engine_loc_counts.index.name = 'engine-location'

#Grouping of data
df['drive-wheels'].unique()
df_group_one = df[['drive-wheels','body-style','price']]

#Mean of the group by driving wheels
df_group_one = df_group_one.groupby(['drive-wheels'],as_index=False).mean()

df_gptest = df[['drive-wheels','body-style','price']]
grouped_test1 = df_gptest.groupby(['drive-wheels','body-style'],as_index=False).mean()

#Pivot table for checking price w.r.t drive style ROW & Body Style COLUMNS
grouped_pivot = grouped_test1.pivot(index='drive-wheels',columns='body-style')
grouped_pivot = grouped_pivot.fillna(0) #fill missing values with 0
print(grouped_pivot)

#use the grouped results
plt.pcolor(grouped_pivot, cmap='RdBu')
plt.colorbar()
plt.show()

fig, ax = plt.subplots()
im = ax.pcolor(grouped_pivot, cmap='RdBu')

#label names
row_labels = grouped_pivot.columns.levels[1]
col_labels = grouped_pivot.index

#move ticks and labels to the center
ax.set_xticks(np.arange(grouped_pivot.shape[1]) + 0.5, minor=False)
ax.set_yticks(np.arange(grouped_pivot.shape[0]) + 0.5, minor=False)

#insert labels
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(col_labels, minor=False)

#rotate label if too long
plt.xticks(rotation=90)

fig.colorbar(im)
plt.show()

#Pearson Co-Efficient & Correlation between two columns
pearson_coef, p_value = stats.pearsonr(df['wheel-base'], df['price'])
print("The Pearson Correlation Coefficient is", pearson_coef, " with a P-value of P =", p_value)

#ANOVA: Analysis of Variance
grouped_test2=df_gptest[['drive-wheels', 'price']].groupby(['drive-wheels'])
grouped_test2.get_group('4wd')['price']  # Get price based on groups

f_val, p_val = stats.f_oneway(grouped_test2.get_group('fwd')['price'], grouped_test2.get_group('rwd')['price'], grouped_test2.get_group('4wd')['price'])  
print( "ANOVA results: F=", f_val, ", P =", p_val)
f_val, p_val = stats.f_oneway(grouped_test2.get_group('4wd')['price'], grouped_test2.get_group('fwd')['price'])  
print("ANOVA results: F=", f_val, ", P =", p_val)   
