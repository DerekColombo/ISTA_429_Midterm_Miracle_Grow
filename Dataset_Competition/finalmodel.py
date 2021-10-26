'''
Author: Colby Chambers, Ryan Rizzo, Derek Columbo, Cole Mckinley.
Description: This file takes in the numpy dataframe and runs it through
several different cleaning and reorganizing methods to then run it through the
model below.
'''

import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

'''
Average Direct Normal Irradiance (ADNI)
Average Precipitation (AP) 3
Average Relative Humidity (ARH)
Maximum Direct Normal Irradiance (MDNI) 2
Maximum Surface Temperature (MaxSur)
Minimum Surface Temperature (MinSur) 1
Average Surface Temperature (AvgSur)

Maturity Group (MG), Genotype ID, State, Year, and Location for each performance record.
'''

data = np.load('inputs_others_train.npy')

df = pd.DataFrame(data)


weather_data = np.load('inputs_weather_train.npy')

columns = ['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur']

newarr = weather_data.reshape(93028, 7*214)

df2 = pd.DataFrame(newarr)

#df2 = df2.iloc[: , :7] this line is used to trim the data to a managable size.

df_list = []
n=0
i=7
for sec in df2.columns:

    df_list.append(df2.iloc[: , n:i])
    n+=7
    i+=7

#df_list
len(df_list)

col = ['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur']

#df2.columns = col

df.columns = ['MG','Geno ID','State','Year','Location']

yield_data = np.load('yield_train.npy')

df3 = pd.DataFrame(yield_data)
#df3

df = df3.join(df)
#df

df.columns = ['CropY','MG','Geno ID','State','Year','Location']

#df

#df_merged = df2.join(df)
#df_merged

df_temp = df[['CropY','MG','Geno ID','State','Year','Location']]
#df_temp


i=0
for line in df_list:
    hell = line.join(df_temp)
    df_list[i] = hell
    #df_list[i].columns = ['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur','CropY','MG','Geno ID','State','Year','Location']
    i+=1
#df_list

df_list = df_list[0:214]

i=0
for line in df_list:
    df_list[i].columns=['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur','CropY','MG','Geno ID','State','Year','Location']
    i+=1

#df_merged.to_csv('rowbycolfull.csv')

i=0
for line in df_list:
    df_list[i] =line.groupby(['Geno ID']).mean()
    i+=1
DF = df_list

#DF.to_csv('groupedgenoid.csv')

testothers = np.load('inputs_others_test.npy')
testweather = np.load('inputs_weather_test.npy')

df_test = pd.DataFrame(testothers)
df_test.columns = ['MG','Geno ID','State','Year','Location']

newarr = testweather.reshape(10337, 7*214)
df_test2 = pd.DataFrame(newarr)

#df_test2 = df_test2.iloc[: , :7] #managable size file
df_list_test = []
n=0
i=7
for sec in df2.columns:

    df_list_test.append(df_test2.iloc[: , n:i])
    n+=7
    i+=7

df_list_test
len(df_list_test)

len(df_list_test[0])

df_temp2 = df_test[['MG','Geno ID','State','Year','Location']]
#df_temp2


i=0
for line in df_list_test:
    hell = line.join(df_temp2)
    df_list_test[i] = hell
    #df_list[i].columns = ['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur','CropY','MG','Geno ID','State','Year','Location']
    i+=1
#df_list_test

df_list_test = df_list_test[0:214]

i=0
for line in df_list_test:
    df_list_test[i].columns=['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur','MG','Geno ID','State','Year','Location']
    i+=1

df_list_test

i=0
for line in df_list_test:
    df_list_test[i] =line.groupby(['Geno ID']).mean()
    i+=1
DF_test = df_list_test

def calc_temp(colum, new_df):
    '''
    This function takes in  two parameters the column and the list
    of dataframes. It runs the training data through the model and
    and gets the inputs for the test formula, then runs the test
    data to return a list of 214 dataframes of crop yields.
    '''
    #print(new_df)
    yield_list_final = []
    x = new_df[colum]
    y = new_df['CropY']
    plt.plot(x, y, '.')
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b)
    cm = np.corrcoef(x, y)
    cxy = cm[0,1]
    r_squared = cxy**2
    #calc_list = slope()
    ####
    i=0
    for row in df_list_test:
        if i >=1:
            xyz=0
        else:
            for line in row[colum]:
                y = (m*line)+b
                yield_list_final.append(y)

    result = np.array(yield_list_final)
    return yield_list_final
    ####

'''
This loop is what collects all of the data and then writes the results
to a file.
'''
mean_list = []
for df in DF:
    ADNI = calc_temp("ADNI", df)
    AP = calc_temp("AP", df)
    ARH = calc_temp("ARH", df)
    MDNI = calc_temp("MDNI",df)
    MaxSur = calc_temp("MaxSur",df)
    MinSur = calc_temp("MinSur",df)
    AvgSur = calc_temp("AvgSur",df)

    combined_yield = [ADNI, AP, ARH, MDNI, MaxSur, MinSur, AvgSur]
    combined_df = pd.DataFrame(combined_yield)
    mean_list.append(combined_df)

mean_list

len(mean_list[0][0])

########n_train_hours = int(len(dataset)*0.80)

combined_df = mean_list

another_list = []
i = 0
for line in combined_df:
    final_df = combined_df[i].mean(axis=0)
    another_list.append(final_df)
    i+=1

another_list

numpy_result = final_df.to_numpy()

np.save("results.npy", numpy_result)
result = np.load('results.npy')


