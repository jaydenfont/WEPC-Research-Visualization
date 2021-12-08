#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import os
import math

data = pd.read_csv("bullying_viz_data.csv")
data


# In[19]:


def reformat_to_pct_change(data):
    
    # fill Nan with zeros
    data.fillna(0)
    
    # convert dates to datetime
    data['date'] = pd.to_datetime(data['date'])
    
    # pivot by state, so we can compare across time
    pivot_data = data.pivot(index='state', columns = 'date')
    
    # break data into the different bullying types and calculate pct change across each type
    data_subsets = set()
    for col in pivot_data.columns:
        data_subsets.add(col[0])
    
    for bullying_type in data_subsets:
        pivot_data[bullying_type] = 100*pivot_data[bullying_type].astype(float).pct_change(axis=1)
        
    # drop first col of all Nan
    pivot_data = pivot_data.drop(columns=pivot_data.columns[0])
    
    return pivot_data


# In[20]:


pct_changed = reformat_to_pct_change(data)
pct_changed


# In[21]:


pct_changed.to_csv("data_pct_change.csv")


# In[ ]:




