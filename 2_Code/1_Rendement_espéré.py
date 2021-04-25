# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 16:18:41 2021

@author: yanis
"""

import pandas as pd
import numpy as np
from scipy import stats

# Importation des données 

df_stocks=pd.read_csv(r"C:\Users\yanis\01 Projets\01 Python Projects\Projet_RiskManagment\Projet_RiskManagement\3_Données\stocks_data.csv",sep=';',index_col=0)

df_returns=pd.read_csv(r"C:\Users\yanis\01 Projets\01 Python Projects\Projet_RiskManagment\Projet_RiskManagement\3_Données\stocks_returns_data.csv",sep=';',index_col=0)

#########################################################################################

# Calcul des paramètres du moouvement brownien

def get_mu_and_sigma(df):
    '''
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with the series of interest
    Returns
    -------
    df_param : pd.DataFrame
        A DataFrame with the mean et the standard deviation of all the columns

    '''
    
    list_mu=[]
    list_sigma=[]
    
    for i in df:
        
        mu=df[i].mean()
        sigma=df[i].std()
        
        list_mu.append(mu)
        list_sigma.append(sigma)
    
    list_param=list(zip(list_mu, list_sigma))
    df_param=pd.DataFrame(list_param).T
    df_param.columns = df.columns
        
    return df_param

#########################################################################################

# Test de student sur les paramètres

def get_t_stats(df):
    '''
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with shape (2,n) 
        mean on the first row
        std on the second row

    Returns
    -------
    df_tstats : pd.DataFrame
        A dataFrame with the tstat and the pvalue associated 

    '''
    
    tstats_list=[]
    Pvalue_list=[]
        
    for i in range(0,len(df.T)):
            
        tstats=(df.iloc[0,i])/(df.iloc[1,i])
        tstats_list.append(tstats)
         
        
    for p in range(0,len(tstats_list)):
        Pvalue=2*(stats.norm(0, 1).sf(abs(tstats_list[p])))
        Pvalue_list.append(Pvalue)
            
    list_tstat_pval=list(zip(tstats_list,Pvalue_list))
    df_tstats=pd.DataFrame(list_tstat_pval).T
    df_tstats.columns = df.columns
        
    return df_tstats
            
        
        

#########################################################################################

# Application 

df_param=get_mu_and_sigma(df_returns.columns)

df_tstats=get_t_stats(df_param)
