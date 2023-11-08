import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def questão_4_lookback():
    n = 252
    T = 1
    S = 100
    r = 0.05
    standard_vol = 0.2
    standard_m = 10000
    standard_e = 100
    e_values = list(np.arange(90, 130 + 1))
    m_values = [valor for valor in range(100, 15000, 100) if valor <= 15000]
    vol_values = [round(i, 2) for i in list(np.linspace(0.05, 0.8, num=16))]
    
    def princing(n, T, M, S, sigma, r, E):
        dt = T/n
        St = np.exp((sigma**2/2)*dt + sigma*np.random.normal(0,np.sqrt(dt), size=(M,n)).T)
        St = np.vstack([np.ones(M), St])
        df_St = pd.DataFrame(S*St.cumprod(axis=0).T)
        max_St = list(df_St.max(axis=1))
        payoff = [np.maximum(0, elemento - E) for elemento in max_St]
        media_payoff = np.mean(payoff)
        price = media_payoff * np.exp(-r)
        
        return price
    
    #Variando a Vol
    vol_prices = list()
    for i in vol_values:
        sigma = i
        E = standard_e
        M = standard_m
        price = princing(n, T, M, S, sigma, r, E)
        vol_prices.append(price)
    df_vol = pd.DataFrame(vol_prices)
    df_vol.index = vol_values

    #Variando o número de simulações
    sim_prices = list()
    for i in m_values:
        M = i
        E = standard_e
        sigma = standard_vol
        price = princing(n, T, M, S, sigma, r, E)
        sim_prices.append(price)
    df_sim = pd.DataFrame(sim_prices)
    df_sim.index = m_values
    
    #Variando o Strike
    strike_prices = list()
    for i in e_values:
        E = i
        M = standard_m
        sigma = standard_vol
        price = princing(n, T, M, S, sigma, r, E)
        strike_prices.append(price)
    df_strike = pd.DataFrame(strike_prices)
    df_strike.index = e_values
    
    fig = plt.figure(figsize=(18, 5))

    plt.subplot(1, 3, 1)
    plt.plot(df_vol)
    plt.xlabel('Volatility')
    plt.ylabel('Lookback Call Price')
    plt.grid(True)
    
    plt.subplot(1, 3, 2)
    plt.plot(df_sim)
    plt.xlabel('Simulations')
    plt.ylabel('Lookback Call Price')
    plt.grid(True)
    
    plt.subplot(1, 3, 3)
    plt.plot(df_strike)
    plt.xlabel('Strikes')
    plt.ylabel('Lookback Call Price')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

questão_4_lookback()