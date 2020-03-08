import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures

path = 'automobileEDA.csv'
df = pd.read_csv(path)
#print(df.head())

'''
Linear Regression (Yhat = a+bX)
a - intercept (default value when X is 0)
b - Slope  (rate at which Y changes based on X)
'''

from sklearn.linear_model import LinearRegression

#Create a liner regression object : Highway - mpg
lm = LinearRegression()

X = df[['highway-mpg']]  # Predictor variable
Y = df[['price']]   # Response
lm.fit(X,Y)     # Training the linear model
Yhat=lm.predict(X)
#print(Yhat[0:5])
print("Intercept -", lm.intercept_ ,"\n","Slope - ",lm.coef_ )

#Create a liner regression object : Engine Size
lm_obj = LinearRegression()
a = df[['engine-size']]
b = df[['price']]
lm_obj.fit(a,b)
Yhat_obj=lm_obj.predict(a)
print(Yhat_obj[0:5])
print("Intercept -", lm_obj.intercept_ ,"\n","Slope - ",lm_obj.coef_ )

'''
Multiple liner regression model
Y = b0+b1X1+b2X2+b3X3+b4X4
'''
lm2 = LinearRegression()
Z=df[['horsepower','curb-weight','engine-size','highway-mpg']]
lm2.fit(Z,df['price'])
print("Multi Coeff : ",lm2.coef_,"\nMulti Slope",lm2.intercept_)

'''
Data Visualization
'''
width = 8
height = 8
plt.figure(figsize=(width, height))
sns.regplot(x="highway-mpg", y="price", data=df)
plt.ylim(0,)
plt.show()

plt.figure(figsize=(width, height))
sns.regplot(x="peak-rpm", y="price", data=df)
plt.ylim(0,)
plt.show()

#correlation to show map the plots "highway-mpg" strong correlation compared to "peak-rpm"
print(df[['highway-mpg','peak-rpm','price']].corr())

#Residual plot
'''
Random spread indicates linear model is good
If a pattern is visible then linear model is not good for prediction
'''
width = 8
height = 8
plt.figure(figsize=(width, height))
sns.residplot(df['highway-mpg'], df['price'])
plt.show()

sns.residplot(df['peak-rpm'], df['price'])
plt.show()

'''
Multiple Linear Regress - Distribution plot to show actual vs predicted value
'''
Y_hat = lm2.predict(Z)
ax1 = sns.distplot(df['price'], hist=False, color="r", label="Actual Value")
sns.distplot(Yhat, hist=False, color="b", label="Fitted Values" , ax=ax1)

plt.title('Actual vs Fitted Values for Price')
plt.xlabel('Price (in dollars)')
plt.ylabel('Proportion of Cars')
plt.show()

'''
Polynomial Regresssion
𝑌=𝑎+𝑏1𝑋2+𝑏2𝑋2+𝑏3𝑋3....
'''
def PlotPolly(model, independent_variable, dependent_variabble, Name):
    x_new = np.linspace(15, 55, 100)
    y_new = model(x_new)

    plt.plot(independent_variable, dependent_variabble, '.', x_new, y_new, '-')
    plt.title('Polynomial Fit with Matplotlib for Price ~ Length')
    ax = plt.gca()
    ax.set_facecolor((0.898, 0.898, 0.898))
    fig = plt.gcf()
    plt.xlabel(Name)
    plt.ylabel('Price of Cars')

    plt.show()
    plt.close()

x = df['highway-mpg']
y = df['price']
# Here we use a polynomial of the 3rd order (cubic) 
f = np.polyfit(x, y, 3)
p = np.poly1d(f)
print(p)
PlotPolly(p, x, y, 'highway-mpg')
np.polyfit(x, y, 3)

#Polynomial Features
pr=PolynomialFeatures(degree=2)
Z_pr=pr.fit_transform(Z)
print("Polynomial Change", Z.shape, "\n", Z_pr.shape)

#Data Pipeline with standard scalar
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
Input=[('scale',StandardScaler()), ('polynomial', PolynomialFeatures(include_bias=False)), ('model',LinearRegression())]
pipe=Pipeline(Input)
pipe.fit(Z,y)
ypipe=pipe.predict(Z)
print(ypipe[0:4])

Input=[('scale',StandardScaler()),('model',LinearRegression())]
pipe=Pipeline(Input)
pipe.fit(Z,y)
ypipe=pipe.predict(Z)
print(ypipe[0:10])

'''
Model evaluation based on R Square  / Mean Squared Error (MSE)
When comparing models, the model with the higher R-squared value is a better fit for the data.
When comparing models, the model with the smallest MSE value is a better fit for the data.
'''
#highway_mpg_fit
lm.fit(X, Y)
# Find the R^2
print('The R-square is: ', lm.score(X, Y))
Yhat=lm.predict(X)
print('The output of the first four predicted value is: ', Yhat[0:4])

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(df['price'], Yhat)
print('The mean square error of price and predicted value is: ', mse)

# fit the model 
lm2.fit(Z, df['price'])
# Find the R^2
print('The R-square is: ', lm2.score(Z, df['price']))
Y_predict_multifit = lm2.predict(Z)
print('The mean square error of price and predicted value using multifit is: ', \
      mean_squared_error(df['price'], Y_predict_multifit))

from sklearn.metrics import r2_score
r_squared = r2_score(y, p(x))
print('The R-square value is: ', r_squared)
print(mean_squared_error(df['price'], p(x)))

#Predicting for new input
import matplotlib.pyplot as plt
import numpy as np
new_input=np.arange(1, 100, 1).reshape(-1, 1)
lm.fit(X, Y)
yhat=lm.predict(new_input)
print(yhat[0:5])
plt.plot(new_input, yhat)
plt.show()

