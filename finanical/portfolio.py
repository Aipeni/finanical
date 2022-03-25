import yfinance as yf
import pandas_datareader as pdr
import pandas as pd
import datetime


class finanical_data():
    def __init__(self,stocklist,quantity,start,end):
        self.stocklist=stocklist
        self.quantity=quantity
        self.start=datetime.datetime.strptime(start,"%Y-%m-%d").date()
        self.end=datetime.datetime.strptime(end,"%Y-%m-%d").date()
        self.df=None
    def latest_trading_day(self):
        holiday=["2022-01-17","2022-02-21","2022-04-15","2022-05-30","2022-06-20","2022-07-04","2022-09-05","2022-11-24","2022-12-26"]
        non_trading_date=[]
        for i in holiday:
            non_trading_date.append(datetime.datetime.strptime(i,"%Y-%m-%d").date())
        if self.start in non_trading_date:
            self.start=self.start-datetime.timedelta(days=1)
        if self.start.weekday()==5:
            self.start=self.start-datetime.timedelta(days=1)
        elif self.start.weekday()==6:
            self.start=self.start-datetime.timedelta(days=2)
    def get_data(self):
        self.latest_trading_day()
        portfolio={}
        for i in range(0,len(stocklist)):
            portfolio[self.stocklist[i]]=self.quantity[i]
        self.df= yf.download(" ".join(self.stocklist),  start=self.start, end=self.end)
        self.df=self.df["Close"]
        self.df=self.df.iloc[[-1]].T
        self.df.columns=["price"]
        self.df["quantity"]=self.df.index.map(portfolio)
        self.df["value"]=self.df["price"]*self.df["quantity"]
    def porfolio_vale(self):
        portfolio_value=self.df["value"].sum()
        print(self.df)
        print(f"The portfolio value is : {portfolio_value}")
    def all_function(self):
        self.latest_trading_day()
        self.get_data()
        self.porfolio_vale()

