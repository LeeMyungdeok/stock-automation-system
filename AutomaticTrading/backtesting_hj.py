import numpy as np
import pandas as pd


# 모델링용

# def __get_period(df):
#     df.dropna(inplace=True)
#     end_date = df['Datetime'][df['Datetime'].index[-1]]
#     start_date = df['Datetime'][df['Datetime'].index[0]]
#     days_between = (end_date - start_date).days
#     return abs(days_between)
# def __annualize(rate, period):
#     if period < 360:
#         rate = ((rate-1) / period * 365) + 1
#     elif period > 365:
#         rate = rate ** (365 / period)
#     else:
#         rate = rate
#     return round(rate, 4)


# def __get_sharpe_ratio(df, rf_rate):
#     '''
#     Calculate sharpe ratio
#     :param df:
#     :param rf_rate:
#     :return: Sharpe ratio
#     '''
#     period = __get_period(df)
#     rf_rate_daily = rf_rate / 365 + 1
#     df['exs_rtn_daily'] = df['daily_rtn'] - rf_rate_daily
#     exs_rtn_annual = (__annualize(df['acc_rtn'][-1:], period) - 1) - rf_rate
#     exs_rtn_vol_annual = df['exs_rtn_daily'].std() * np.sqrt(365)
#     sharpe_ratio = exs_rtn_annual / exs_rtn_vol_annual if exs_rtn_vol_annual>0 else 0
#     return round(sharpe_ratio, 4)
# def evaluate(df, cost=.001):
#     '''
#     Calculate daily returns and MDDs of portfolio
#     :param df: The dataframe containing trading position
#     :param cost: Transaction cost when sell
#     :return: Returns, MDD
#     '''
#     df['signal_price'] = np.nan
#     df['signal_price'].mask(df['position']==1, df['Adj Close'], inplace=True)
#     df['signal_price'].mask(df['position']==2, df['Adj Close'], inplace=True)
#     record = df[['position','signal_price']].dropna()
#     record['rtn'] = 1
#     record['rtn'].mask(record['position']==2, (record['signal_price']*(1-cost))/record['signal_price'].shift(1), inplace=True)
#     record['acc_rtn'] = record['rtn'].cumprod()

#     df['signal_price'].mask(df['position']==0, df['Adj Close'], inplace=True)
#     df['rtn'] = record['rtn']
#     df['rtn'].fillna(1, inplace=True)
   
#     df['daily_rtn'] = 1
#     df['daily_rtn'].mask(df['position'] == 0, df['signal_price'] / df['signal_price'].shift(1), inplace=True)
#     df['daily_rtn'].mask(df['position'] == 2, (df['signal_price']*(1-cost)) / df['signal_price'].shift(1), inplace=True)
#     df['daily_rtn'].fillna(1, inplace=True)
#     df['acc_rtn'] = df['daily_rtn'].cumprod()
#     df['acc_rtn_dp'] = ((df['acc_rtn']-1)*100).round(2)
#     df['mdd'] = (df['acc_rtn'] / df['acc_rtn'].cummax()).round(4)
#     df['bm_mdd'] = (df['Adj Close'] / df['Adj Close'].cummax()).round(4)
#     df.drop(columns='signal_price', inplace=True)
#     return df


# def performance(df, rf_rate=.01):
#     '''
#     Calculate additional information of portfolio
#     :param df: The dataframe with daily returns
#     :param rf_rate: Risk free interest rate
#     :return: Number of trades, Number of wins, Hit ratio, Sharpe ratio, ...
#     '''
#     rst = {}
#     rst['no_trades'] = (df['position']==1).sum()
#     rst['no_win'] = (df['rtn']>1).sum()
#     rst['acc_rtn'] = df['acc_rtn'][-1:].round(4)
#     rst['hit_ratio'] = round((df['rtn']>1).sum() / rst['no_trades'], 4) if rst['no_trades']>0 else 0
#     rst['avg_rtn'] = round(df[df['rtn']!=1]['rtn'].mean(), 4)
#     rst['period'] = __get_period(df)
#     rst['annual_rtn'] = __annualize(rst['acc_rtn'], rst['period'])
#     rst['bm_rtn'] = round(df.iloc[-1,5]/df.iloc[0,5], 4)
#     rst['sharpe_ratio'] = __get_sharpe_ratio(df, rf_rate)
#     rst['mdd'] = df['mdd'].min()
#     rst['bm_mdd'] = df['bm_mdd'].min()

#     print('CAGR: ',(rst['annual_rtn'].values[0] - 1))
#     print('Accumulated return:',(rst['acc_rtn'].values[0] - 1))
#     print('Average return: ',(rst['avg_rtn'] - 1))
#     print('Benchmark return :',(rst['bm_rtn']-1))
#     print('Number of trades: ',(rst['no_trades']))
#     print('Number of win:',(rst['no_win']))
#     print('Hit ratio:',(rst['hit_ratio']))
#     print('Investment period:',(rst['period']/365),'yrs')
#     print('Sharpe ratio:',(rst['sharpe_ratio'].values[0]))
#     print('MDD:',(rst['mdd']-1))
#     print('Benchmark MDD:',(rst['bm_mdd']-1))




# 백테스팅용 
class backtest:
    def __init__(self, df ,position, result_show =False):
        self.df =df
        self.position = position
        self.result_show = result_show
        self.df = self.evaluate(self.df, cost=.001)
        self.performance(self.df)


    def __get_period(self, df):

        df.dropna(inplace=True)
        end_date = df['Datetime'][df['Datetime'].index[-1]]
        start_date = df['Datetime'][df['Datetime'].index[0]]
        days_between = (end_date - start_date).days
        return abs(days_between)
    def __annualize(self, rate, period):
        df = self.df
        if period < 360:
            rate = ((rate-1) / period * 365) + 1
        elif period > 365:
            rate = rate ** (365 / period)
        else:
            rate = rate
        return round(rate, 4)


    def __get_sharpe_ratio(self, df, rf_rate):
        '''
        Calculate sharpe ratio
        :param df:
        :param rf_rate:
        :return: Sharpe ratio
        '''
        df = self.df
        period = self.__get_period(df)
        rf_rate_daily = rf_rate / 365 + 1
        df['exs_rtn_daily'] = df['daily_rtn'] - rf_rate_daily
        exs_rtn_annual = (self.__annualize(df['acc_rtn'][-1:], period) - 1) - rf_rate
        exs_rtn_vol_annual = df['exs_rtn_daily'].std() * np.sqrt(365)
        sharpe_ratio = exs_rtn_annual / exs_rtn_vol_annual if exs_rtn_vol_annual>0 else 0
        return round(sharpe_ratio, 4)
    def evaluate(self, df, cost=.001):
        '''
        Calculate daily returns and MDDs of portfolio
        :param df: The dataframe containing trading position
        :param cost: Transaction cost when sell
        :return: Returns, MDD
        '''
        df['signal_price'] = np.nan
        df['signal_price'].mask(df[self.position]==1, df['Adj Close'], inplace=True)
        df['signal_price'].mask(df[self.position]==-1, df['Adj Close'], inplace=True)
        record = df[[self.position,'signal_price']].dropna()
        record['rtn'] = 1
        record['rtn'].mask(record[self.position]==-1, (record['signal_price']*(1-cost))/record['signal_price'].shift(1), inplace=True)
        record['acc_rtn'] = record['rtn'].cumprod()

        df['signal_price'].mask(df[self.position]==0, df['Adj Close'], inplace=True)
        df['rtn'] = record['rtn']
        df['rtn'].fillna(1, inplace=True)

        df['daily_rtn'] = 1
        df['daily_rtn'].mask(df[self.position] == 0, df['signal_price'] / df['signal_price'].shift(1), inplace=True)
        df['daily_rtn'].mask(df[self.position] == -1, (df['signal_price']*(1-cost)) / df['signal_price'].shift(1), inplace=True)
        df['daily_rtn'].fillna(1, inplace=True)
        df['acc_rtn'] = df['daily_rtn'].cumprod()
        df['acc_rtn_dp'] = ((df['acc_rtn']-1)*100).round(2)
        df['mdd'] = (df['acc_rtn'] / df['acc_rtn'].cummax()).round(4)
        df['bm_mdd'] = (df['Adj Close'] / df['Adj Close'].cummax()).round(4)
        df.drop(columns='signal_price', inplace=True)
        return df


    def performance(self, df, rf_rate=.01):
        '''
        Calculate additional information of portfolio
        :param df: The dataframe with daily returns
        :param rf_rate: Risk free interest rate
        :return: Number of trades, Number of wins, Hit ratio, Sharpe ratio, ...
        '''

        rst = {}
        rst['no_trades'] = (df[self.position]==1).sum()
        rst['no_win'] = (df['rtn']>1).sum()
        rst['acc_rtn'] = df['acc_rtn'][-1:].round(4)
        rst['hit_ratio'] = round((df['rtn']>1.0).sum() / rst['no_trades'], 4) if rst['no_trades']>0 else 0
        rst['avg_rtn'] = round(df[df['rtn']!=1.0]['rtn'].mean(), 4)
        rst['period'] = self.__get_period(df)
        rst['annual_rtn'] = self.__annualize(rst['acc_rtn'], rst['period'])
        rst['bm_rtn'] = round(df.iloc[-1,5]/df.iloc[0,5], 4)
        rst['sharpe_ratio'] = self.__get_sharpe_ratio(df, rf_rate)
        rst['mdd'] = df['mdd'].min()
        rst['bm_mdd'] = df['bm_mdd'].min()
        if self.result_show ==True:
            print('CAGR: ',(rst['annual_rtn'].values[0] - 1)*100)
            print('Accumulated return:',(rst['acc_rtn'].values[0] - 1)*100)
            print('Average return: ',(rst['avg_rtn'] - 1)*100)
            print('Benchmark return :',(rst['bm_rtn']-1)*100)
            print('Number of trades: ',(rst['no_trades']))
            print('Number of win:',(rst['no_win']))
            print('Hit ratio:',(rst['hit_ratio']))
            print('Investment period:',(rst['period']/365),'yrs')
            print('Sharpe ratio:',(rst['sharpe_ratio'].values[0]))
            print('MDD:',(rst['mdd']-1)*100)
            print('Benchmark MDD:',(rst['bm_mdd']-1)*100)
            self.res = {'CAGR':(rst['annual_rtn'].values[0] - 1)*100,'Accumulated return':(rst['acc_rtn'].values[0] - 1)*100,'Average return': (rst['avg_rtn'] - 1)*100,'MDD':(rst['mdd']-1)*100}
        else:
            self.res = {'CAGR':(rst['annual_rtn'].values[0] - 1)*100,'Accumulated return':(rst['acc_rtn'].values[0] - 1)*100,'Average return': (rst['avg_rtn'] - 1)*100,'MDD':(rst['mdd']-1)*100}
            print('백테스팅 성공')
        