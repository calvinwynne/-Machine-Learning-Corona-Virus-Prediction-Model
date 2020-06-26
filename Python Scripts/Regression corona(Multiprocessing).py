#!/usr/bin/env python
# coding: utf-8

# In[5]:


from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn import linear_model 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
from multiprocessing import Process


# In[6]:


def read_dict():
    global country_list, path, dict_files
    path = "E:\\Python Projects\Corona virus\\Source Files\\cleaned\\Python files\\"
    
    
    pickle_in = open(path + "[Main] Confirmed_Corona","rb")
    confirmed_dict = pickle.load(pickle_in)
    pickle_in.close()
    print("[Success] Read Confirmed_Corona")
    
    pickle_in = open(path + "[Main] Deaths_Corona","rb")
    deaths_dict = pickle.load(pickle_in)
    pickle_in.close()
    print("[Success] Read Deaths_Corona")
    
    pickle_in = open(path + "[Main] Recovered_Corona","rb")
    recovered_dict = pickle.load(pickle_in)
    pickle_in.close()
    print("[Success] Read Recovered_Corona")
   
    pickle_in = open(path + "[list] Country","rb")
    country_list = pickle.load(pickle_in)
    pickle_in.close()
    print("[Success] Read Country_list")
    
    dict_files = ((confirmed_dict, "Confirmed_Corona"),  (deaths_dict, "Deaths_Corona"), (recovered_dict, "Recovered_Corona"))

# In[7]:


def write_dict(dataframe, filename, accuracy):
    path = "E:\\Python Projects\Corona virus\\Source Files\\cleaned\\Python files\\"
    f = open(path + "[Predicted] " + filename,"wb")
    pickle.dump(dataframe,f)
    f.close()
    
    print("\n[Writing] Predicted " +  filename + "to memory")
    
    f = open(path +  "[Accuracy] " +  filename ,"wb")
    pickle.dump(accuracy,f)
    f.close()
    
    print("[Writing] Accuracy " + filename + " to memory")
    print()

# In[8]:


def Train_Predict(country_dict, filename, country_list):
    accuracy_dict = {}
    for country in country_list:
        df = country_dict[country].dropna().reset_index(drop =True)
        x = df.drop("Forecast", axis=1)
        y = df["Forecast"]
        regressor =  linear_model.LinearRegression()
        accuracy = 0
        training_count = 0
        print("[ " + country + " ] Training on " + filename + " data: ",end='')
        while  accuracy <= 90:
            x_train, x_test, y_train, y_test = train_test_split(x , y, test_size=0.33)
            regressor.fit(x_train, y_train)
            accuracy = regressor.score(x_test, y_test)
            accuracy = round(accuracy*100,2)
            print(".",end='')
            training_count = training_count + 1
            if training_count > 10:
                print("\nModel went into an infinite loop")
                print("Model has been trained " + str(training_count) + " times" )
                break
        print("Training Completed")
        print("Model Accuracy on " + country + ": " + str(accuracy) +" %")
        print("Predicting data for next 5 days")
        prediction_list= []
        for i in range(df.shape[0],df.shape[0]+5):
            prediction_list.append([i, int(df.iloc[i-5][2]) ])
        result = regressor.predict(prediction_list)
        print("Prediction completed")
        print("Appending predicted values to the appropriate dictionary")
        last_val = prediction_list[-1][0]
        for i,vals in enumerate(result,1):
            prediction_list.append([last_val+i, int(vals),0])
        df2 = pd.DataFrame(data=prediction_list, columns=df.columns)
        df = df.append(df2, ignore_index=True)
        df.fillna(0, inplace=True)
        country_dict[country] = df
        accuracy_dict.update({country : accuracy})
        print()
    write_dict(country_dict, filename, accuracy_dict)


# In[9]:




if __name__ == "__main__":
    print("Initializing Training Process...")
    print("Reading saved dictionary files")
    read_dict()
    for dataframe, filename in dict_files:
        p1 = Process(target=Train_Predict, args=((dataframe, filename, country_list)))
        p1.start()
    print("Training Completed.")

# In[ ]:




