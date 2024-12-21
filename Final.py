import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import numpy as np
pd.options.display.float_format = '{:.2f}'.format

# initialize df1
df1 = pd.read_csv('NCHS1.csv')
df1 = df1.rename(columns = {'113 Cause Name':'Category'})
# initialize df2
df2 = pd.read_csv('NCHS2.csv')
df2 = df2.drop(columns = 'Estimates Base')
df2 = df2.drop(index=[0,1,2,3,4,56]) #See previous assignment comments
df2['Geographic Area'] = df2['Geographic Area'].str.replace('.','')

# Cleaning data of commas to be mathematically pliable and creating population variable
names = df2.columns.tolist()
names.pop(0)
names.pop(0)
population = []
for col in df2.columns:
    df2[col] = df2[col].str.replace(',','')
    try:
        df2[col] = df2[col].astype(int)
        population.append(int(df2[col].iloc[0]))
    except:
        pass
population.pop(0)
population.pop(-1)
population.pop(-1)

# Reformatting DataFrame 1 to meger with DataFrame 2
deaths = pd.DataFrame(df1.groupby('Year')[['Deaths']].agg('sum'))
deaths = deaths.drop(index=[1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009])
deaths.insert(1,"Population", population, True)
deaths['Deaths per Capita'] = deaths['Deaths']/deaths['Population']

# Formatting new data and concatonating with old data
YR2010 = pd.read_csv('YR2010.csv'); YR2011 = pd.read_csv('YR2011.csv'); YR2012 = pd.read_csv('YR2012.csv'); YR2013 = pd.read_csv('YR2013.csv'); YR2014 = pd.read_csv('YR2014.csv'); YR2015 = pd.read_csv('YR2015.csv'); YR2016 = pd.read_csv('YR2016.csv')
years = [YR2010, YR2011, YR2012, YR2013, YR2014, YR2015, YR2016]
means = []
medians = []
for YR in years:
    for col in YR.columns:
        YR[col] = YR[col].str.replace("%","")
        YR[col] = YR[col].str.replace(",","")
    YR['Estimate'] = pd.to_numeric(YR['United States!!Households!!Estimate'], errors = 'coerce') + pd.to_numeric(YR['United States!!Nonfamily households!!Estimate'], errors = 'coerce')
    YR = YR.rename(columns = {'Label (Grouping)': 'Stat'})
    YR = YR.loc[11:12, ['Stat', 'Estimate']]
    medians.append(int(YR.iat[0,1]))
    means.append(int(YR.iat[1,1]))    

stats = {'Median Income': medians, 'Mean Income': means}
incomes = pd.DataFrame(data = stats, index = [2010, 2011, 2012, 2013, 2014, 2015, 2016])
incomes.index.name = 'Year'
info = pd.concat([deaths, incomes], axis = 1)
print(info)

corr1 = info.corr(numeric_only=True)['Deaths per Capita']['Median Income']
corr2 = info.corr(numeric_only=True)['Deaths per Capita']['Mean Income']

print(corr1)
print(corr2)

fig, ax = plt.subplots()
ax.set_title("Comparing Deaths per Capita to Median Income")
ax.bar(info.index, info['Median Income'], width = 0.5, label= 'Median Inc.', color = 'darkorange')
ax2 = ax.twinx()
ax2.bar(info.index, info['Deaths per Capita'], width = 0.3, label = 'Deaths per Capita', color = 'teal')
ax.set_ylim(75000, 95000)
ax2.set_ylim(1.8, 2)
ax.legend(loc="upper left")
ax2.legend(loc="upper center")
plt.show()

info['CPI'] = [218.1, 224.9, 229.6, 233.0, 236.7, 237.0, 240.0]
multipliers = []
for i in info['CPI']:
    multiplier = info.iat[0,5]/i
    multipliers.append(multiplier)

info['Multiplier'] = multipliers
info['Mean Adjusted'] = info['Mean Income'] * info['Multiplier']; info['Median Adjusted'] = info['Median Income'] * info['Multiplier']
info['Mean Adjusted'] = info['Mean Adjusted'].round(0).astype(int); info['Median Adjusted'] = info['Median Adjusted'].round(0).astype(int) 
#print(info)

corr3 = info.corr(numeric_only=True)['Deaths per Capita']['Median Adjusted']
corr4 = info.corr(numeric_only=True)['Deaths per Capita']['Mean Adjusted']

print(corr3)
print(corr4)


fig, ax = plt.subplots()
ax.set_title("Comparing Deaths per Capita to Median Real Income")
ax.bar(info.index, info['Median Adjusted'], width = 0.5, label= 'Median Inc.', color = 'darkorange')
ax2 = ax.twinx()
ax2.bar(info.index, info['Deaths per Capita'], width = 0.3, label = 'Deaths per Capita', color = 'teal')
ax.set_ylim(75000, 85000)
ax2.set_ylim(1.8, 2)
ax.legend(loc="upper left")
ax2.legend(loc="upper center")
plt.show()