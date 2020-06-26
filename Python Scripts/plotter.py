import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

plt.style.use("seaborn-dark")
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey

fig, ax = plt.subplots()
fig = plt.gcf()
fig.set_size_inches(9, 5)


def Predicted_Files():
    global confirmed, deaths, recovered
    print("\nReading predicted files")
    path = "E:\\Python Projects\\Corona virus\\Source Files\\Prediction Output\\"
    confirmed = pd.read_csv(path + "Predicted Confirmed_Corona.csv")
    print("[Success] Read Predicted Confirmed_Corona.csv")
    deaths    = pd.read_csv(path + "Predicted Deaths_Corona.csv")
    print("[Success] Read Predicted Death_Corona.csv")
    recovered = pd.read_csv(path + "Predicted Recovered_Corona.csv")
    print("[Success] Read Predicted Recovered_Corona.csv")
    
    
def Clean_Files():
    global clean_confirmed, clean_deaths, clean_recovered
    path = "E:\\Python Projects\Corona virus\\Source Files\\cleaned\\"
    print("\nReading Preprocessed files")
    clean_confirmed = pd.read_csv(path + "Confirmed_Corona" + ".csv")
    print("[Success] Read Confirmed_Corona.csv")
    clean_deaths    = pd.read_csv(path + "Deaths_Corona" + ".csv")
    print("[Success] Read Deathas_Corona.csv")
    clean_recovered = pd.read_csv(path + "Recovered_Corona" + ".csv")
    print("[Success] Read Recovered_Corona.csv")


def df_combiner(df1, df2, case_name):
    print("\nCombining data from predicted and preprocessed file")
    df1.drop("Accuracy", axis=1, inplace=True)
    df1.drop(df1.columns[3], axis=1, inplace=True)
    df1.drop("DaySince", axis=1, inplace=True)
    df = pd.merge(df2, df1, how='inner', on="Country/Region", left_on=None, right_on=None,
             left_index=False, right_index=False, sort=True,
             suffixes=('_x', '_y'), copy=True, indicator=False,
             validate=None)
    cols = df.columns.to_list()[-12:]
    cols.remove('DaySince')
    cols.remove('Case')
    front_cols = ['Country/Region', 'Case',  'DaySince']
    front_cols.extend(cols)
    df = df[front_cols]
    print("[Success] Combined file: " + case_name)
    return df


def sorter(df, start):
    df.sort_values(by="Country/Region", inplace=True)
    df["New Index"] = [i for i in range(start, df.shape[0]*3+1, 3)]
    df.set_index("New Index", inplace=True)
    return df


def master_combiner():
    global confirmed, deaths, recovered, clean_confirmed, clean_deaths, clean_recovered
    confirmed = df_combiner(confirmed, clean_confirmed, "Confirmed Cases")
    deaths    = df_combiner(deaths, clean_deaths, "Deaths")
    recovered = df_combiner(recovered, clean_recovered, "Recovered Cases")
    confirmed = sorter(confirmed, 1)
    deaths    = sorter(deaths, 2)
    recovered = sorter(recovered, 3)
    df = confirmed.append(deaths)
    df = df.append(recovered)
    df.sort_index(axis=0, inplace=True)
    return df


def get_country(df):
    index = 1
    country = input("\n \nPlease enter the Coutry name: ")
    df = df.loc[df["Country/Region"]==country]
    df.set_index("Case", inplace=True)
    df = df.iloc[0:,2:]
    df = df.transpose()
    return df



def plotter(df):
    ax.grid(color='#2A3459')  
    colors = [
        '#08F7FE',  # teal/cyan
        '#FE53BB',  # pink
        '#F5D300',  # yellow
        '#00ff41', # matrix green
    ]
    df.plot(marker='o', ax=ax, color=colors)
    n_lines = 10
    diff_linewidth = 1.05
    alpha_value = 0.03
    for n in range(1, n_lines+1):
        df.plot(marker='o', linewidth=2+(diff_linewidth*n), alpha=alpha_value, legend=False, ax=ax, color=colors)
    for column, color in zip(df, colors):
        ax.fill_between(x=df.index, y1=df[column].values, y2=[0] * len(df), color=color, alpha=0.1)

    ax.set_xlim([ax.get_xlim()[0] - 0.2, ax.get_xlim()[1] + 0.2])  # to not have the markers cut off
    ax.set_ylim(0)
    plt.xticks(rotation=35)
    plt.show()


while True:
    Clean_Files()
    Predicted_Files()
    df = master_combiner()
    country = get_country(df)
    plotter(country)


