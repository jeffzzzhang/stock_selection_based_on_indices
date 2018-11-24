# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 11:20:39 2017

@author: talen
"""
# select stocks based on indices and attributes
import pandas as pd
import numpy as np
import os,time,math

start_time = time.time()
os.chdir('C:\\Users\\LH\\Desktop\\工作日志\\2017年4月第2周')
stock_data = pd.read_excel('stock_data.xls')
print('loading time is',time.time()-start_time,'s')
corporates_number = len(stock_data.iloc[:,1])
ownership = '国有非央企' #企业性质
location = '北上深' #省份
quantile = 0.8 # x:总市值的最高的1-x,
PE = 25 # price earning ratio
turnover_ratio = 1
volatility_ratio = 1.5
elimination_gap = 3 # in unit of year
# eliminate the public corporates: less than 3 years
from datetime import datetime
now = datetime.now()
keep_after_eli_index = np.zeros(corporates_number)
for i in range(corporates_number):
    IPO_date = stock_data.ix[i,'首发上市日期'].to_period('D')
    if IPO_date.year < now.year - elimination_gap:
        keep_after_eli_index[i] = 1
    elif IPO_date.year == now.year - elimination_gap and IPO_date.month <= now.month and IPO_date.day <= now.day:
        keep_after_eli_index[i] = 1
del i,IPO_date
#
ownership_index = np.zeros(corporates_number)
if ownership == '国有非央企':
    for i in range(corporates_number):
        if '央' in str(stock_data.loc[i,['企业性质']]) or '民' in str(stock_data.loc[i,['企业性质']]) or '外资' in str(stock_data.loc[i,['企业性质']]):
            continue
        else:
            ownership_index[i] = 1
del i

location_index = np.zeros(corporates_number)
if location == '北上深':
    for j in range(corporates_number):
        if '上海' in str(stock_data.loc[j,['省份']]) or '北京' in str(stock_data.loc[j,['省份']]):
            location_index[j] = 1
        elif '深圳' in str(stock_data.loc[j,['地级市']]):
            location_index[j] = 1
        else:
            continue
del j
#
PE_index = np.zeros(corporates_number)
for i in range(corporates_number):
    if type(stock_data.ix[i,'市盈率']) == float:
        if stock_data.ix[i,'市盈率'] <= PE:
            PE_index[i] = 1
del i
#
turnover_index = np.zeros(corporates_number)
for i in range(corporates_number):
    if type(stock_data.ix[i,'换手率']) == float:
        if stock_data.ix[i,'换手率'] >= turnover_ratio:
            turnover_index[i] = 1
del i
#
volatility_index = np.zeros(corporates_number)
for i in range(corporates_number):
    if type(stock_data.ix[i,'波动率']) == float:
        if stock_data.ix[i,'波动率'] >= volatility_ratio:
            volatility_index[i] = 1
del i
#
tmp = stock_data.总市值.tolist()
tmp.sort()
quantile_point = tmp[math.floor(len(tmp)*quantile)]
market_value_index = np.zeros(corporates_number)
for k in range(corporates_number):
    if float(stock_data.loc[k,['总市值']]) >= quantile_point:
        market_value_index[k] = 1
    else:
        continue
del k

select_index = volatility_index*turnover_index*PE_index*keep_after_eli_index*location_index*market_value_index*ownership_index
tmp = []
for i in range(len(select_index)):
    if select_index[i] > 0.5:
        tmp.append(i)
selected_stocks = stock_data.iloc[tmp,:]
print('total running time is',time.time()-start_time,'s')
del start_time
