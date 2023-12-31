import numpy as np
import pandas as pd 
from src.backtesting_hj import *
from src.data_loader_hj import *
from src.strategy import *



temp = ['rsi','macd','envelope','bollinger','stochastic']


def big_strategy2(df):
    temp = ['rsi','macd','envelope','bollinger','stochastic']
    result = {}
    for i in temp:
        exec(f"df['{i}_position'] = {i}_strategy(df)")
        wow = backtest(df,f'{i}_position')
        result[i] = wow.res
    test_list = [[i, result[i]['CAGR']] for i in result ]
    a=0
    for i in range(len(test_list)):
        for j in range(len(test_list)):
            if test_list[i][1]>test_list[j][1]:
                a=test_list[i]
                test_list[i] = test_list[j]
                test_list[j] = a
    print(test_list)

    df = test(df,test_list[0][0],test_list[1][0])        
    return backtest(df,'position',True)


