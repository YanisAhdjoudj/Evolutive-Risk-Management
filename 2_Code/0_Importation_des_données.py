# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 21:40:02 2021

@author: yanis
"""

import pandas as pd
from typing import Union
import yfinance as yf


# Nous devons choisir 20 actions pour notre projet
#
# Nous décidons de prendre uniquement des actions américaines car cela nous évite 
# d'avoir à géré le risque de change (en nous considérant comme des investisseurs
# américains) de plus elles sont plus nombreuses et diversifiées ce qui nous offre
# une plus grande liberté de choix
#
# Afin d'avoir un portefeuille diversifié nous décidons de choisir des actions
# de différents secteurs :
#    
#
# Information Technology : Google(GOOGL), Facebook (FB), Apple(AAPL), Amazon(AMZN)
#
# Retail : Walmart(WMT), Costco (COST)
#
# Food : The Coca-Cola Company (KO), McDonald's(MCD)
#
# Financials : BlackRock(BLK), JPMorgan Chase & Co(JPM), Berkshire Hathaway(BRK.A)
#
# Industrials : Builders FirstSource Inc (BLDR), General Motors(GM), Tesla(TSLA),
#               Union Pacific(UNP)
#
# Healthcare and Biotech: Pfizer(PFE), Heron Therapeutics(HRTX)
#   
# Energy : ExxonMobil(XOM), Chevron(CVX), Plug Power(PLUG)


# On commence par initialiser la liste des tickers
ticker_list=["GOOGL","FB","AAPL","AMZN","WMT","COST","KO","MCD","BLK","JPM",
             "BRK-A","BLDR","GM","TSLA","UNP","PFE","HRTX","XOM","CVX","PLUG"]

# On choisi les dates pour définir les données a récupérées
start_date= "2017-01-01"
end_date="2021-01-01"


# On défini les fonctions qui vont nous permettre de prendre les données 

########################################################################################

def get_stock(stock, start, end , value: Union[str , list], index_as_date=True):
    """
    Parameters
    ----------
    stock : str
        Stock abreviation
    start : str
        Start date in format yyyy-mm-dd
    end : str
        End date in format yyyy-mm-dd
    value : Union[str , list]
        Open, High, Low, Close, Adj Close or Volume
    index_as_date : bool
        Set True if you want dates as index and False if you don't want dates.

    Returns
    -------
    pd.DataFrame
        Dataframe with requested data.
    """
    
    serie = yf.download(stock , start = start , end = end)
    
    if index_as_date == True:
        serie = serie[value]
        serie.index = serie.index.to_period('d')
    else:
        serie = serie[value].reset_index(drop=True)
    

    return serie 

########################################################################################

def get_multiple_stock(tickers, start, end, value: Union[str , list], index_as_date=True):
    """

    Parameters
    ----------
    tickers : list
        The list with the stocks wanted (as strings)
    start : str
        Start date in format yyyy-mm-dd
    end : str
        End date in format yyyy-mm-dd
    value : Union[str , list]
        Open, High, Low, Close, Adj Close or Volume
    index_as_date : str, optional
        dafaut True if you want dates as index and False if you don't want dates.

    Returns
    -------
    stocks_df : pd.Dataframe
        Dataframe with requested data.

    """
    list_stock=[]
    
    for ticker in tickers:
        stock_serie = get_stock(stock=ticker, start=start, end=end,  value=value, index_as_date=index_as_date)
        list_stock.append(stock_serie)
    
    stocks_df=pd.concat(list_stock, axis=1)
    stocks_df.columns = tickers
    
    return stocks_df

#########################################################################################

def get_returns(df_stocks):
    """
    
    Parameters
    ----------
    df_stocks : pd.DataFrame
        Dataframe with stocks value

    Returns
    -------
    returns_df : pd.DataFrame
        Dataframe with stocks returns

    """

    list_returns=[]
    
    for ticker in df_stocks.columns:
        
        serie_return= df_stocks[ticker].pct_change()
        list_returns.append(serie_return)
    
    returns_df=pd.concat(list_returns, axis=1)
    returns_df.columns = df_stocks.columns
    
    returns_df = returns_df.iloc[1: , :]
    
    return returns_df

#########################################################################################


# Application pour les valeurs

df_stocks=get_multiple_stock(tickers=ticker_list,start=start_date, end=end_date , value = 'Open',index_as_date=True)

# Exportation des valeurs

df_stocks.to_csv(r"C:\Users\yanis\01 Projets\01 Python Projects\Projet_RiskManagment\Projet_RiskManagement\3_Données\stocks_data.csv",sep=';',header=True,index=True)



# Calcul des rendements

df_returns=get_returns(df_stocks)

# Exportation des rendements

df_returns.to_csv(r"C:\Users\yanis\01 Projets\01 Python Projects\Projet_RiskManagment\Projet_RiskManagement\3_Données\stocks_returns_data.csv",sep=';',header=True,index=True)



