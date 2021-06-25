# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 16:02:48 2021

@author: adamp
"""

import pandas as pd
import numpy as np

#https://www.nhtsa.gov/content/nhtsa-ftp/280561
# initial dataset to show car crashes across the US
df = pd.read_csv(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\Week9_10\VehicleData\Vehicle2018.csv',encoding="ISO-8859-1")
df = df[['STATENAME','BUS_USE','DEATHS']]
df.to_excel(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\Week9_10\p_auto_deaths_state_df.xlsx', index=False)


# begin timeline
df = pd.read_csv(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\Week9_10\VehicleData\Vehicle2018.csv',encoding="ISO-8859-1")
df = df[['STATENAME','DEATHS','DAY','MONTH']]
df['YEAR'] = 2018
df['date'] = pd.to_datetime(df[['YEAR', 'MONTH','DAY']].assign(DAY=1))
df = df.groupby(['STATENAME','date'], as_index=False)["DEATHS"].sum()

# function to clean the vehicle data source
def vehicle_crash_clean(year):
    df = pd.read_csv(f'C:\\Users\\adamp\\OneDrive\\Desktop\\a_vizes\\Project\\Week9_10\\VehicleData\\Vehicle{year}.csv',encoding="ISO-8859-1")
    df = df[['STATENAME','DEATHS','MONTH']]
    df['YEAR'] = year
    df['date'] = pd.to_datetime(df[['YEAR','MONTH']].assign(DAY=1))
    df = df.groupby(['STATENAME','date'], as_index=False)["DEATHS"].sum()
    return df


year_list = [2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1996,1995]
length = len(year_list)
i = 0

df = pd.DataFrame({'DEATHS': pd.Series([], dtype='int'),
                   'date': pd.Series([], dtype='d'),
                   'STATENAME': pd.Series([], dtype='str')
                   })
    
    
# Iterating using while loop
# Using enumerate()
try:
    for i, val in enumerate(year_list):
        df = df.append(vehicle_crash_clean(val))
        print(i)
        print(val)
except Exception as e:
    print(e)

df['type'] = 'car'        
df = df.reset_index(drop=True)
df.to_excel(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\Week11_12\p_car_timeline.xlsx')


#import plane data
df_plane = pd.read_excel(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\Week9_10\PlaneData\concat.xlsx',encoding="ISO-8859-1")
df_plane['date'] = df_plane['Date'].values.astype('datetime64[M]')
df_plane = df_plane[['Operator','date','Fatalities']]

# only include the top 20 airlines according to passengers 
to_keep = ['Aeromexico', 'Alaska Airlines','American Airlines','Delta Air Lines','Frontier Air','Southwest Airlines','United Air Lines']
df_plane = df_plane.query("Operator in @to_keep")

df_plane = df_plane.groupby(['date'], as_index=False)["Fatalities"].sum()

df_plane['DEATHS'] = df_plane['Fatalities']
df_plane = df_plane[['DEATHS','date']]
df_plane['type'] = 'plane'

df = df.append(df_plane)
    

df.to_excel(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\Week9_10\p_joined_plane_car_timeline.xlsx')





