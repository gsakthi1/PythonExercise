import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,PolynomialFeatures


file_name = "kc_house_data_NaN.csv"
#file_name='https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/coursera/project/kc_house_data_NaN.csv'
df=pd.read_csv(file_name)

print(df.head())
df.drop('id', axis = 1, inplace=True)
df.drop('Unnamed: 0', axis = 1, inplace=True)

print("number of NaN values for the column bedrooms :", df['bedrooms'].isnull().sum())
print("number of NaN values for the column bathrooms :", df['bathrooms'].isnull().sum())

mean=df['bedrooms'].mean()
df['bedrooms'].replace(np.nan,mean, inplace=True)
mean=df['bathrooms'].mean()
df['bathrooms'].replace(np.nan,mean, inplace=True)
print("number of NaN values for the column bedrooms :", df['bedrooms'].isnull().sum())
print("number of NaN values for the column bathrooms :", df['bathrooms'].isnull().sum())


'''
Explore data
'''
floor_values = df['floors'].value_counts()
floor_values.to_frame()

sns.boxplot(x="waterfront", y="price", data=df) #Box plot for waterfront views data
plt.show()

sns.regplot(x="sqft_above", y="price", data=df)
plt.ylim(0,)
plt.show()
df[["sqft_above", "price"]].corr()  #Positive Correlation

#We can use the Pandas method corr() to find the feature other than price that is most correlated with price.
print(df.corr()['price'].sort_values())

'''
Model Creation
'''
from sklearn.linear_model import LinearRegression
X = df[['long']]
Y = df['price']
lm = LinearRegression()
lm.fit(X,Y)
lm.score(X, Y)   #R^2 value

'''
Multiple Linear Regression
'''
features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]   
x = df[features]
lm_mult = LinearRegression()
lm_mult.fit(x,df['price'])
print(lm_mult.intercept_ ,lm_mult.coef_)
lm_mult.score(df[features],df['price']) #R^2 value

'''
Standardization
'''
X = df[features]
Y = df[['price']]
pipe=Pipeline(Input)
pipe.fit(X,Y)
pipe.score(X,Y)

'''
Module 5: MODEL EVALUATION AND REFINEMENT
'''
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]    
X = df[features ]
Y = df['price']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=1)
print("number of test samples :", x_test.shape[0])
print("number of training samples:",x_train.shape[0])
Input=[('scale',StandardScaler()),('polynomial', PolynomialFeatures(include_bias=False)),('model',LinearRegression())]

'''
Ridge Regression
'''
from sklearn.linear_model import Ridge
RR = Ridge(alpha=0.1)
RR.fit(x_train, y_train)
#train_score = RR.score(x_train, y_train)
#RR.fit(x_test, y_test)
test_score = RR.score(x_test,y_test)
print(test_score)


