# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 09:24:08 2020

@author: adamp
"""

import pandas as pd
import re

df_d = pd.read_csv(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\Airplane_Crashes_and_Fatalities_Since_1908_20190820105639.csv')

# get only needed columns
df_d = df_d[['Date','Aboard','Fatalities','Operator']]
df_d = df_d[df_d['Operator'].notna()]
df_d['Date'] = pd.to_datetime(df_d['Date'])

# convert date to date format and add period format
df_d['Date'] = pd.to_datetime(df_d['Date'])
df_d['period'] = df_d['Date'].dt.strftime('%Y%m')

# grab only dates that are greater than 1984
df_d = df_d[(df_d['period'] > '198412')]

# remove special chars and whitespace
# upper case all values
#df_d['Operator'] = df_d['Operator'].str.replace('\W', '')
#df_d['Operator'] = df_d['Operator'].apply(lambda x: x.upper())

df = pd.read_excel(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\airlinedata.xlsx')


df['fatalities_85_99_per_seat'] = ((df['fatalities_85_99']/df['avail_seat_km_per_week'])*100)
df['incidents_85_99_per_seat'] = ((df['incidents_85_99']/df['avail_seat_km_per_week'])*100)

df['fatalities_00_14_per_seat'] = ((df['fatalities_00_14']/df['avail_seat_km_per_week'])*100)
df['incidents_00_14_per_seat'] = ((df['incidents_00_14']/df['avail_seat_km_per_week'])*100)

df_melt = df.melt(id_vars="airline", 
        var_name="metricName", 
        value_name="Value")

#df['airline'] = df['airline'].str.replace('\W', '')
#df['airline'] = df['airline'].apply(lambda x: x.upper())

#df_concat = df_d.merge(df, left_on=['Operator'], right_on=['airline'],
#                   how='inner')
df.to_excel(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\airlinedata_update.xlsx', index=False)

df = df[['Month','Year','Number Fatalities']]
df['Month'] = df.Month.astype(int)
df['Year'] = df.Year.astype(int)

df['MonthYear']=pd.to_datetime([['Year','Month']]).dt.strftime('%m-%Y')

# traffic accidents 
df = pd.read_csv(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\ardd_fatal_crashes.csv')

