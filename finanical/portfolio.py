import yfinance as yf
import pandas_datareader as pdr
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


class finanical_data():
    def __init__(self,stocklist,quantity,start,end):
        self.stocklist=stocklist
        self.quantity=quantity
        self.start=datetime.datetime.strptime(start,"%Y-%m-%d").date()
        self.end=datetime.datetime.strptime(end,"%Y-%m-%d").date()
        self.df=None
        self.df_pass=None
        self.quantity_dictionary=None
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
    def convert_quantity_to_dictionary(self):
        portfolio={}
        for i in range(0,len(stocklist)):
            portfolio[self.stocklist[i]]=self.quantity[i]
        self.quantity_dictionary=portfolio
    def get_data(self):
        self.latest_trading_day()
        self.convert_quantity_to_dictionary()
        self.df= yf.download(" ".join(self.stocklist),  start=self.start, end=self.end)
        self.df=self.df["Close"]
        self.df=self.df.iloc[[-1]].T
        self.df.columns=["price"]
        self.df["quantity"]=self.df.index.map(self.quantity_dictionary)
        self.df["value"]=self.df["price"]*self.df["quantity"]
        self.df["% port"]=(self.df["value"]/self.df["value"].sum())*100
        self.df=self.df.round(2)
    def porfolio_vale(self):
        portfolio_value=round(self.df["value"].sum(),2)
        print(self.df)
        print(f"The portfolio value is : {portfolio_value}")
    def previous_price(self):
        portfolio_value=0
        self.latest_trading_day()
        self.convert_quantity_to_dictionary()
        self.df_pass= yf.download(" ".join(self.stocklist),  start=self.start, end=self.end)
        self.df_pass=self.df_pass["Close"]
        for i in self.df_pass.columns:
            portfolio_value+=self.df_pass[i]*self.quantity_dictionary[i]
        portfolio_value.fillna(method='ffill',inplace=True)
        self.df_pass["portfolio_value"]=portfolio_value
        self.df_pass=self.df_pass.round(2)
    def all_function(self):
        self.latest_trading_day()
        self.get_data()
        self.porfolio_vale()
    def plot_return_against_QQQ(self):
        plt.plot(self.df_pass["portfolio_value"].pct_change()*100,label="portfolio")
        plt.plot(self.df_pass["QQQ"].pct_change()*100,label="QQQ")
        plt.xticks(rotation=90)
        plt.legend();

        
def check_currency(stocklist):
    """
    This takes a long time to run, should only be using if you are not confident on the currency of the stock, but this can also extract all company info of the company
    """
    cur={}
    for i in stocklist:
        cur[i]=tickers.tickers[i].info["currency"]
    return cur