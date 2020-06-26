#!/usr/bin/env python
# coding: utf-8

# In[72]:

import datetime
import requests 
import numpy as np
import pandas as pd
from multiprocessing import Process
# In[73]:

Coordinates = True
date_today = datetime.date.today()
date_today = date_today.strftime("%d-%b-%Y")
path = "E:\\Python Projects\Corona virus\\Source Files\\"
base_url = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_"


# In[117]:


conf_filename = "Confirmed_Corona" + " " + date_today + ".csv"
deth_filename = "Deaths_Corona"    + " " + date_today + ".csv"
recv_filename = "Recovered_Corona" + " " + date_today + ".csv"


# In[118]:


conf_url = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
deth_url = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv"
recv_url = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv"

url_lib = {
    conf_filename : conf_url,
    deth_filename : deth_url,
    recv_filename : recv_url
}


# In[119]:


def file_download(file_name):
    url = url_lib[file_name]
    r = requests.get(url, stream = True) 
    with open(path + file_name,"wb") as csv: 
        for chunk in r.iter_content(chunk_size=1024): 
             if chunk: 
                 csv.write(chunk)
        print("Downloaded: " + file_name)


# In[120]:


def column_Sorter(date_list):
    date_dict = {}
    for date in date_list:
        if date[3] == '/':
            temp = int(date[0]+ '0' + date[2])
        else:
            temp = int(date[0]+date[2:4])
        date_dict.update({date:temp })
    vat = sorted(date_dict.items(), key=lambda item: item[1])
    returnable_list = []
    for i in vat:
        returnable_list.append(i[0])
    return returnable_list


# In[121]:


def DaySince(df, file_name):
    d = df.mask(df == 0)
    d.columns = np.arange(len(df.columns))
    df = df.assign(
        Days_since=d.apply(pd.Series.first_valid_index, 1)
    )
    df["Days_since"] = df["Days_since"].apply(lambda row : df.shape[1] - row)
    df.rename({"Days_since" : "DaySince"}, axis=1, inplace=True)
    return df
    


# In[122]:


def data_formater(file_name, gen_cord=False):
    try :
        global Coordinates
        df = pd.read_csv(path + file_name)
        if gen_cord == True:
            cordinates_df = df[["Country/Region","Lat", "Long"]]
            cordinates_df.set_index("Country/Region", inplace=True)
            print("Formated: "+ "Coordinates_database.csv")
            cordinates_df.to_csv(path+"cleaned\\"+"Coordinates_database.csv")
            Coordinates = False
        df = df.drop(["Province/State", "Lat", "Long"], axis=1)
        df = pd.pivot_table(df, index=["Country/Region"],aggfunc='sum')
        date_list = df.columns
        date_list = column_Sorter(date_list)
        df = df[date_list]
        df.sort_values(by= df.columns[-1], ascending=False, inplace=True)
        df.sort_values(by= df.columns[-1], ascending=False, inplace=True)
        df = DaySince(df, file_name)
        file_name = file_name[:-16]+".csv"
        df.to_csv(path+"cleaned\\"+file_name)
        print("Formated: "+ file_name)
    except:
        print("Something went wrong: " + file_name) 
        


# In[123]:


parallel_list = ((conf_filename, True), (deth_filename, False), (recv_filename, False))


# In[88]:


if __name__ == "__main__":
    print("Initializing Download...")
    for file, cord in parallel_list:
        p1 = Process(target=file_download, args=((file,)))
        p1.start()
    p1.join()
    print("Download Completed.")
    print("\nInitializing Preprocessing...")
    for file, cord in parallel_list:
        p2 = Process(target=data_formater, args=((file, cord)))
        p2.start()
    p2.join()
    print("\nPreprocessing Completed")   