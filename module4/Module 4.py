#!/usr/bin/env python
# coding: utf-8

# 
# ## Module 4
# 
# Build a dash app for a arborist studying the health of various tree species (as defined by the variable ‘spc_common’) across each borough (defined by the variable ‘borough’). This arborist would like to answer the following two questions for each species and in each borough.
# 
# Link to app.py: https://github.com/olga0503/DATA-608/blob/master/app.py
# 

# In[257]:


import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
from plotly import tools


# In[258]:


url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
trees.head(10)


# ## 1.What proportion of trees are in good, fair, or poor health according to the ‘health’   variable?

# In[176]:


for x in range(0, max_row, offset):
    #print('x is ' + str(x))
    url_1 = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=1000&$offset=' + str(x) +        '&$select=borocode,spc_common,health,steward,count(block_id)' +        '&$group=borocode,spc_common,health,steward').replace(' ', '%20')
    trees = pd.read_json(url_1)
    if(x==0):
        df = pd.DataFrame(columns=list(trees.columns.values))
    df = df.append(trees)

df = df.dropna(axis=0, how='any')


# In[259]:


print(df)


# In[261]:


df.head(5)


# In[262]:


df_totals = df.groupby(['borocode', 'spc_common'])['count_block_id'].sum()
df_totals = df_totals.reset_index(drop=False)
df_totals.columns = ['borocode', 'spc_common', 'total_spc_common']


# In[263]:



df_totals.head(5)


# In[264]:


df_total_by_borocode_specie_health = df.groupby(['borocode', 'spc_common', 'health'])['count_block_id'].sum()
df_total_by_borocode_specie_health = df_total_by_borocode_specie_health.reset_index(drop=False)
df_total_by_borocode_specie_health.columns = ['borocode', 'spc_common', 'health', 'total']


# In[265]:


df_total_by_borocode_specie_health.head(5)


# In[268]:


tree_ratio = pd.merge(df_total_by_borocode_specie_health, df_totals, on=['borocode', 'spc_common'])


# In[269]:


tree_ratio.head(5)


# In[271]:


tree_ratio['ratio'] = tree_ratio['total']/ tree_ratio['total_spc_common']
tree_ratio.head(10)


# In[272]:


df_health = tree_proportions.groupby(['health'])['total'].sum()
df_health = df_health.reset_index(drop=False)
df_health.head()


# In[273]:


df_health1 = tree_proportions.groupby(['health'])['total_for_specie_in_borough'].sum()
df_health1 = df_health1.reset_index(drop=False)
df_health1.head()


# In[274]:


tot_health = pd.merge(df_health, df_health1, on=['health'])
tot_health.head()


# In[275]:


tot_health['ratio'] = tot_health['total']/ tot_health['total_for_specie_in_borough']
tot_health.head(10)


# In[212]:


import matplotlib.pyplot as plt
import numpy as np

x = tot_health['health']
y = tot_health['ratio']

plt.bar(x,y)
plt.show()


# ## 2. Are stewards (steward activity measured by the ‘steward’ variable) having an impact on the health of trees?

# In[276]:


list(df['steward'].unique())


# In[286]:


df.head()


# In[327]:


df_total_by_steward = df.groupby(['borocode', 'spc_common', 'steward'])['count_block_id'].sum()
df_total_by_steward = df_total_by_steward.reset_index(drop=False)
df_total_by_steward.columns = ['borocode', 'spc_common', 'steward', 'steward_total']
df_total_by_steward.head(10)


# In[328]:




df_steward = pd.merge(df, df_total_by_steward, on=['borocode', 'spc_common', 'steward'])
df_steward.head(10)


# In[329]:


df_steward['health_index'] = df_steward['steward_total']/ df_steward['count_block_id']
df_steward.head(10)


# In[331]:


df_steward_1 = df_steward.groupby(['health', 'steward'])['health_index'].sum()
df_steward_1 = df_steward_1.reset_index(drop=False)
df_steward_1.columns = ['health', 'steward', 'health_index']
df_steward_1.head(10)


# In[332]:


groups = df_steward_1.groupby('health' )
fig = go.Figure()
for g in groups.groups:
    group = groups.get_group(g)
    fig.add_trace(go.Bar(x=group['steward'], y=group['health_index'], name=str(g)))
fig.layout.update({'height':600})
fig.layout.update({'width':1500})
fig.show()


# In[ ]:




