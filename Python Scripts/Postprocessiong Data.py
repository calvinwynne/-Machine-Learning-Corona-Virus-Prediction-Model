#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pickle


# In[2]:


def read_files(filename, population=False):
    path = "E:\\Python Projects\Corona virus\\Source Files\\cleaned\\"
    
    try: 
        dataframe = pd.read_csv(path + filename + ".csv")
        print("[Success] Reading: "  + filename)
    except:
        print("[ Error ] Reading: "  + filename)
    
    try:
        popl_filename = "Population_database.csv"
        population_df  = pd.read_csv(path + popl_filename)
        print("[Success] Reading: "  + popl_filename)
        
    except:
        print("[ Error ] Reading: " + popl_filename)        
    print()
    return (dataframe, (popl_filename, population_df))


# In[14]:


def read_dict(filename, read_listCountry = False):
    path = "E:\\Python Projects\Corona virus\\Source Files\\cleaned\\Python files\\"
    
    pickle_in = open(path + "[Predicted] " + filename,"rb")
    main = pickle.load(pickle_in)
    pickle_in.close()
 
    pickle_in = open(path + "[Accuracy] " + filename,"rb")
    accuracy = pickle.load(pickle_in)
    pickle_in.close()
    
    pickle_in = open(path + "[DaySince] " + filename,"rb")
    daysince = pickle.load(pickle_in)
    pickle_in.close()
    
    pickle_in = open(path + "[list] Country","rb")
    country_list = pickle.load(pickle_in)
    pickle_in.close()
    return (main, accuracy, daysince, country_list)


# In[23]:


def PostProcess(filename, dataframe, main, accuracy, daysince, country_list):
    path = "E:\\Python Projects\Corona virus\\Source Files\\cleaned\\"
    df = dataframe
    df.drop(df.columns[1:-2], axis=1,inplace =True)
    df["Case"] = filename[:-7]
    for i in range(1,6):
        df["Predicted Day: " + str(i)] = 0
    df.set_index("Country/Region", inplace=True)
    for country in country_list:
        df.loc[country, "Accuracy"] = accuracy[country]
        temp = main[country]
        temp = temp[country].to_list()
        temp = temp[-5:]
        for i in range(1,6):
            df.loc[country, "Predicted Day: " + str(i)] = temp[i-1]
    df = df[["Case", "Accuracy", df.columns[1], df.columns[0], df.columns[3], df.columns[4], df.columns[5], df.columns[6], df.columns[7]]]
    df.to_csv(path[:-8] + "Prediction Output\\Predicted " + filename + ".csv")
    print(df)


# In[24]:


filenames = ("Confirmed_Corona", "Deaths_Corona", "Recovered_Corona")
for filename in filenames:
    dataframe, population = read_files(filename)
    main, accuracy, daysince, country_list = read_dict(filename, True)
    PostProcess(filename, dataframe, main, accuracy, daysince, country_list)
    


# In[ ]:




