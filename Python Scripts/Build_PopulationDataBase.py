#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import requests
import datetime


# In[14]:


def request_webpage():
    url = 'https://www.worldometers.info/world-population/population-by-country/'
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
    page = requests.get(url, headers=header)
    return page


# In[15]:


def Build_Population():
    date_today = datetime.date.today()
    date_today = date_today.strftime("%d-%b-%Y")
    path = "E:\\Python Projects\\Corona virus\\Source Files\\cleaned"
    print("Downloading World Population data...")
    page = request_webpage()
    population_df = pd.read_html(page.text)
    population_df = population_df[0]
    print("Building world population database...")
    population_df.set_index(keys='Country (or dependency)', inplace=True)
    population_df.drop("#", axis=1, inplace=True)
    population_df.to_csv(path+"\\Population_database.csv")
    print("Success: Population Database built\n\n")
    print(population_df)


# In[16]:


Build_Population()


# In[ ]:




