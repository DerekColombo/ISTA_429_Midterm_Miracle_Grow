import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt

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
#df

weather_data = np.load('inputs_weather_train.npy')

columns = ['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur']

newarr = weather_data.reshape(93028, 7*214)

df2 = pd.DataFrame(newarr)

#df2 = df2.iloc[: , :7]

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




complete_df = pd.concat(df_list)


#len(complete_df)

complete_df.columns = ['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur','CropY','MG','Geno ID','State','Year','Location']

#df_merged.to_csv('rowbycolfull.csv')

#df_merged

DF = complete_df.groupby(['Geno ID']).mean()
#DF
#DF.to_csv('groupedgenoid.csv')

'''
*****This is a sample cell of what the function does*****

x = DF['MDNI']
y = DF['CropY']
plt.plot(x, y, '.')

m, b = np.polyfit(x, y, 1)


plt.plot(x, m*x + b)

*****This is a sample cell of what the function does*****
'''

'''
*****This is a sample cell of what the function does*****

cm = np.corrcoef(x, y)
cxy = cm[0,1]
r_squared = cxy**2
r_squared

*****This is a sample cell of what the function does*****
'''

testothers = np.load('inputs_others_test.npy')
testweather = np.load('inputs_weather_test.npy')

df_test = pd.DataFrame(testothers)
df_test.columns = ['MG','Geno ID','State','Year','Location']

newarr = testweather.reshape(10337, 7*214)
df_test2 = pd.DataFrame(newarr)

#df_test2 = df_test2.iloc[: , :7] #don't uncomment
df_list_test = []
n=0
i=7
for sec in df2.columns:
    
    df_list_test.append(df_test2.iloc[: , n:i])
    n+=7
    i+=7
    
df_list_test
len(df_list_test)

df_temp2 = df_test[['MG','Geno ID','State','Year','Location']]
#df_temp2


i=0
for line in df_list_test:
    hell = line.join(df_temp2)
    df_list_test[i] = hell
    #df_list[i].columns = ['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur','CropY','MG','Geno ID','State','Year','Location']
    i+=1
#df_list_test

complete_test = pd.concat(df_list)

complete_test.columns = ['ADNI','AP','ARH','MDNI','MaxSur','MinSur','AvgSur','MG','Geno ID','State','Year','Location']

#df_test = df_test.join(df_test2)

df_test = complete_test

'''
*****This is a sample cell of what the function below does*****

yield_list = []

for row in df_test['ADNI']:
    y = (m*row)+b
    yield_list.append(y)
    
result = np.array(yield_list)
m

*****This is a sample cell of what the function does*****
'''

'''
def list_func():
    yield_list = []

    for row in df_test['ADNI']:
        y = (m*row)+b
        yield_list.append(y)
    
    result = np.array(yield_list)
'''


def calc_temp(colum):
    yield_list_final = []
    x = DF[colum]
    y = DF['CropY']
    plt.plot(x, y, '.')
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b)
    cm = np.corrcoef(x, y)
    cxy = cm[0,1]
    r_squared = cxy**2
    print(r_squared)
    #calc_list = slope()
    #### 
    for row in df_test[colum]:
        y = (m*row)+b
        yield_list_final.append(y)
    
    result = np.array(yield_list_final)
    return yield_list_final
    ####

ADNI = calc_temp("ADNI")
AP = calc_temp("AP")
ARH = calc_temp("ARH")
MDNI = calc_temp("MDNI")
MaxSur = calc_temp("MaxSur")
MinSur = calc_temp("MinSur")
AvgSur = calc_temp("AvgSur")

combined_yield = [ADNI, AP, ARH, MDNI, MaxSur, MinSur, AvgSur]
combined_df = pd.DataFrame(combined_yield)

final_df = combined_df.mean(axis=0)
#final_df

numpy_result = final_df.to_numpy()

len(numpy_result)

np.save("results.npy", numpy_result)
result = np.load('results.npy')

print(result)

len(result)

