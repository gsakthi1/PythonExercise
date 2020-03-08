#!/usr/bin/env python
# coding: utf-8

# In[87]:


import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt 


# In[88]:


filename = "Topic_Survey_Assignment.csv"


# In[89]:


df_survey = pd.read_csv(filename,index_col=[0])


# In[90]:


df_survey.head()


# In[91]:


df_survey.sort_values(['Very interested'], ascending=False, axis=0, inplace=True)


# In[92]:


df_survey.head()


# In[93]:


total_rsp = 2233
df_survey_percnt = df_survey
df_survey_percnt.head()


# In[94]:


df_survey_percnt['Very interested'] = df_survey['Very interested']/total_rsp
df_survey_percnt['Somewhat interested'] = df_survey['Somewhat interested']/total_rsp
df_survey_percnt['Not interested'] = df_survey['Not interested']/total_rsp


# In[95]:


df_survey_percnt


# In[101]:


ax = df_survey_percnt.plot(kind='bar', width=0.8, figsize=(20, 8), color = ('#5cb85c', '#5bc0de', '#d9534f'),fontsize = 14)
ax.set_title('Percentage of Respondents Interest in Data Science',fontsize = 16)
ax.legend(fontsize=14)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_yaxis().set_visible(False)
for p in ax.patches:
    ax.annotate("{:.2%}".format(p.get_height()),
                xy=(p.get_x()+0.02, p.get_height()+0.01))


# In[8]:


sfo_filename = "SFO_2016.csv"
df_sfo = pd.read_csv(sfo_filename)
#df_sfo.head()
df_sfo.describe()
df_sfo.shape


# In[102]:




# get the frequency of occurence of values in PdDistrict column in a list
dataTemp = df_sfo['PdDistrict'].value_counts()
# Convert to a dataframe
df2 = pd.DataFrame(data = dataTemp)
# set index:
df2 = df2.reset_index()
# rename columns
df2.rename(columns={'index':'Neighberhood', 'PdDistrict':'Count'}, inplace=True)
# display dataframe
df2.head(11)


# In[11]:


df_sfo_neigh = df_sfo.PdDistrict.unique()
df_sfo_neigh


# In[125]:


type(df_sfo_neigh)


# In[12]:


df_sfo_neigh_cnt = df_sfo['PdDistrict'].value_counts()
type(df_sfo_neigh_cnt)


# In[13]:


print(df_sfo_neigh)
print(df_sfo_neigh_cnt)


# In[14]:


df_sfo_neigh_cnt.to_frame()
df_sfo_neigh_cnt.reset_index()


# In[15]:


df_sfo_neigh_cnt.rename(columns = {"index":"Nhood", 'PdDistrict':'Count'})


# In[17]:


df_group_sfo = df_sfo.groupby(['PdDistrict']).count()


# In[21]:


type(df_group_sfo)


# In[19]:


df_group_sfo.head()


# In[23]:


df_sel = df_group_sfo
df_sel.reset_index()
df_sel.columns


# In[175]:


df_sel.columns


# In[180]:


#df_sel.drop(['Address','Location','PdId'],axis=1,inplace=True)
df_sel.head()


# In[181]:


df_sel.reset_index()


# In[24]:


df_sel.columns


# In[185]:


df_sel.rename(columns = {'IncidntNum':'Counts'},inplace=True)
df_sel.columns


# In[187]:


df_sel.reset_index()


# In[49]:


import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library
#!conda install -c conda-forge folium=0.5.0 --yes
import folium
print('Folium installed and imported!')


# In[79]:


X = 37.7749
Y = -122.4194
# define the world map
world_map = folium.Map(location=[X, Y], zoom_start=8)
# download countries geojson file
#!wget --quiet https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/world_countries.json -O world_countries.json
#!wget --quiet https://cocl.us/sanfran_geojson.geojson    
#print('GeoJSON file downloaded!')    
SF_geo = 'sanfran.geojson' # geojson file
# create a plain world map
SF_map = folium.Map(location=[37.77, -122.42], zoom_start=11.5)


# In[81]:


crimedata = pd.DataFrame(df_sfo['PdDistrict'].value_counts().astype(float))
crimedata.to_json('crimeagg.json')
crimedata = crimedata.reset_index()
crimedata.columns = ['Nieighborhood', 'Count']
SF_COORDINATES = (37.76, -122.45)
crimedata.head()


# In[82]:


# generate choropleth map using the total crime numbers per district for SF
SF_map.choropleth(
    geo_data=SF_geo,
    data=crimedata,
    columns=['Nieighborhood', 'Count'],
    key_on='feature.properties.DISTRICT',
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Crime Rate in San Francisco'
)
folium.LayerControl().add_to(SF_map)
# display map
SF_map


# In[ ]:




