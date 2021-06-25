# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 16:34:37 2021

@author: adamp
"""

import pandas as pd 
import dataframe_sql as sql
df = pd.read_csv(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\revenue.csv')
df = df[['Year','Net Profit','Total Operating Expense']]
df = df[(df['Year'] > 2007)]
df = df.reindex()
#df = df.set_index('Year')

# calc moving average with SQL
df_final = sql.query(
        """
        select
            Year
            ,"Net Profit" as Profit
            ,"Total Operating Expense" as Expense
            ,AVG("Net Profit") OVER( ORDER BY Year ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)  as mov2YrProfit
            ,AVG("Total Operating Expense") OVER( ORDER BY Year ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)  as mov2YrExpAvg
        from 
            df
        Group by Year,"Net Profit","Total Operating Expense" 
        """
    )

df_final.to_excel(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\exec_revenue.xlsx', index=False)



df = pd.read_excel(r'C:\Users\adamp\OneDrive\Desktop\a_vizes\Project\concat.xlsx')
df = df[['Year','Net Profit','Total Operating Expense']]
df = df[(df['Year'] > 2007)]
df = df.reindex()


