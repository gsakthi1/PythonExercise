import pandas as pd
import numpy as np

np.random.seed(10)
df = pd.DataFrame({
    'normal': np.random.normal(10, 3, 1000),
    'chi': np.random.chisquare(4, 1000)
})

pd.cut(df['normal'], 8).head()

pd.cut(df['chi'], 8).head()

custom_bucket_array = np.linspace(0, 20, 9)

df['normal'] = pd.cut(df['normal'], custom_bucket_array)
df['chi'] = pd.cut(df['chi'], custom_bucket_array)
df.head()

import matplotlib.pyplot as plt

plt.style.use('ggplot')

a = df.groupby('normal').size()
b = df.groupby('chi').size()

categories = df['normal'].cat.categories
ind = np.array([x for x, _ in enumerate(categories)])
width = 0.35       
plt.bar(ind, a, width, label='Normal')
plt.bar(ind + width, b, width,
    label='Chi Square')

plt.xticks(ind + width / 2, categories)
plt.legend(loc='best')
plt.xticks(rotation = 90)
plt.show()

