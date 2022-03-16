import yfinance as yf
import pandas_datareader as pdr
import pandas as pd

class Financial_ratio():
    def __init__(self,stocklist):
        self.stocklist=stocklist
        self.df=None

    def get_data(self):
        tickers = yf.Tickers(" ".join(self.stocklist))
        data_list=[]
        for i in self.stocklist:
            info=tickers.tickers[i.upper()].info
            data_list.append(info)
            process=int(((self.stocklist.index(i)+1)/len(self.stocklist))*100)
            print(f"Processing: {process}%")
        self.df=pd.DataFrame(data_list)
