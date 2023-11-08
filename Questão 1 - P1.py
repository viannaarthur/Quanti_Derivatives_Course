import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def principal_questao_1():
    S = 100
    r = 0.05
    E = 100
    T = 1
    standard_n = 252
    standard_vol = 0.2
    n_values = list(np.arange(4, 50 + 1))
    vol_values = [round(i, 2) for i in list(np.linspace(0.05, 0.8, num=16))]

    def pricing(S, r, E, T, n, sigma):
        delta_t = T / n
        u = np.exp(sigma * np.sqrt(delta_t))
        d = 1 / u
        p = (np.exp(r * delta_t) - d) / (u - d)
        q = 1 - p

        option_price = np.maximum(0, S - E)

        for i in range(n):
            option_price = np.exp(-r * delta_t) * (p * option_price + q * np.maximum(S * u - E, 0))

        return option_price

    #Variando a Vol
    vol_prices = list()
    for i in vol_values:
        sigma = i
        n = standard_n
        option_price = pricing(S, r, E, T, n, sigma)
        vol_prices.append(option_price)
    df_vol = pd.DataFrame(vol_prices)
    df_vol.index = vol_values

    #Variando o N_steps
    n_prices = list()
    for i in n_values:
        n = i
        sigma = standard_vol
        option_price = pricing(S, r, E, T, n, sigma)
        n_prices.append(option_price)
    df_n = pd.DataFrame(n_prices)
    df_n.index = n_values

    #Variando ambos
    df_prices = pd.DataFrame()
    for i in vol_values:
        prices = list()
        sigma = i
        for j in n_values:
            n = j
            option_price = pricing(S, r, E, T, n, sigma)
            prices.append(option_price)
        prices = pd.DataFrame(prices)
        df_prices = pd.concat([df_prices, prices], axis=1)
    df_prices.columns = vol_values
    df_prices.index = n_values

    fig = plt.figure(figsize=(18, 5))

    plt.subplot(1, 3, 1)
    plt.plot(df_vol)
    plt.xlabel('Volatility')
    plt.ylabel('European Call Price')
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(df_n)
    plt.xlabel('# time steps')
    plt.ylabel('European Call Price')
    plt.grid(True)

    ax = fig.add_subplot(1, 3, 3, projection='3d')
    x = df_prices.columns
    y = df_prices.index
    X, Y = np.meshgrid(x, y)
    Z = df_prices.values
    surface = ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('Volatility')
    ax.set_ylabel('# time steps')
    ax.set_zlabel('European Call Price')

    plt.tight_layout()
    plt.show()

principal_questao_1()