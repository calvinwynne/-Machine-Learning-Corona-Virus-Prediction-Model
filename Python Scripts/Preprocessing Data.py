#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import pickle


# In[11]:


def read_files():
    global path, populaion_df, conf_df, deth_df, recv_df, conf_filename, deth_filename, recv_filename, files
    path = "E:\\Python Projects\Corona virus\\Source Files\\cleaned\\"
    
    try: 
        conf_filename = "Confirmed_Corona.csv"
        conf_df     = pd.read_csv(path + conf_filename)
        print("[Success] Reading: "  + conf_filename)
    except:
        print("[ Error ] Reading: " + conf_filename)
    
    try: 
        deth_filename = "Deaths_Corona.csv"
        deth_df       = pd.read_csv(path + deth_filename)
        print("[Success] Reading: "  + deth_filename)
    except:
        print("[ Error ] Reading: " + deth_filename)
        
    try:
        recv_filename = "Recovered_Corona.csv"
        recv_df       = pd.read_csv(path + recv_filename)
        print("[Success] Reading: "  + recv_filename)
    except:
        print("[ Error ] Reading: " + recv_filename)
        
    try:
        popl_filename = "Population_database.csv"
        populaion_df  = pd.read_csv(path + popl_filename)
        print("[Success] Reading: "  + popl_filename)
    except:
        print("[ Error ] Reading: " + popl_filename)
    files = ((deth_df, deth_filename),  (recv_df, recv_filename), (conf_df, conf_filename))
    print()


# In[24]:


def preprocess(dataframe):
    df = dataframe
    temp_df = df[["Country/Region", "DaySince"]].set_index("Country/Region")
    DaySince_dict = temp_df.to_dict()["DaySince"]
    df.drop("DaySince",axis=1,inplace=True)
    df.set_index("Country/Region", inplace=True)
    df = df.transpose()
    df["Day"] = range(1, df.shape[0]+1)
    country_list = []
    country_dict = {}
    for no,countries in enumerate(df.columns):
        country_list.append(countries)
        df["Forecast"] = df[countries].shift(-5)
        temp_df = df[["Day", countries, "Forecast"]]
        country_dict.update({countries : temp_df})
    country_list.remove("Day")
    del country_dict["Day"]
    for no,countries in enumerate(df.columns):
            plt.plot(df["Day"], df[countries], label=df.columns[no])
    print()
    return (country_dict, country_list, DaySince_dict)


# In[29]:

def write_dict(filename, dataframe, country_list, DaySince_dict):
    f = open(path+ "Python files\\[Main] " +filename[:-4],"wb")
    pickle.dump(dataframe,f)
    f.close()
    print("[Writing] "+ filename[:-4] + " to memory")

    f = open(path+"Python files\\" +"[list] Country","wb")
    pickle.dump(country_list,f)
    f.close()
    print("[Writing] Country_list to memory")
    
    f = open(path+ "Python files\\" +"[DaySince] " + filename[:-4],"wb")
    pickle.dump(DaySince_dict,f)
    f.close()
    print("[Writing] Days_Since to memory")

# In[30]:


read_files()
for dataframe, filename in files:
    dataframe, country_list, DaySince_dict = preprocess(dataframe)
    write_dict(filename, dataframe, country_list, DaySince_dict)


# In[ ]:




