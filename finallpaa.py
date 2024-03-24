# -*- coding: utf-8 -*-
"""FinalLPAA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WsPg-vkmwckgXxQ3YWHdPGOc1JPeRvpz
"""

import pandas as pd
import numpy as np

df = pd.read_csv('/content/Dados Históricos - Bitcoin.csv')
df = pd.read_csv('/content/Dados Históricos - Ethereum.csv')
df = pd.read_csv('/content/SPY - Histórico.csv')

dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='B')

btc_prices = np.random.normal(loc=50000, scale=500, size=len(dates))
eth_prices = np.random.normal(loc=3000, scale=300, size=len(dates))
ltc_prices = np.random.normal(loc=150, scale=15, size=len(dates))

df = pd.DataFrame({'Date': dates,
                   'BTC_Close': btc_prices,
                   'ETH_Close': eth_prices,
                   'LTC_Close': ltc_prices})

print(df.head())

df['BTC_Returns'] = df['BTC_Close'].pct_change()
df['ETH_Returns'] = df['ETH_Close'].pct_change()
df['LTC_Returns'] = df['LTC_Close'].pct_change()

df['BTC_Normalized'] = (df['BTC_Close'] / df['BTC_Close'].iloc[0]) * 100
df['ETH_Normalized'] = (df['ETH_Close'] / df['ETH_Close'].iloc[0]) * 100
df['LTC_Normalized'] = (df['LTC_Close'] / df['LTC_Close'].iloc[0]) * 100

print(df.head())

df['BTC_Returns'] = (df['BTC_Close'] / df['BTC_Close'].shift(1)) - 1
df['ETH_Returns'] = (df['ETH_Close'] / df['ETH_Close'].shift(1)) - 1
df['LTC_Returns'] = (df['LTC_Close'] / df['LTC_Close'].shift(1)) - 1

print(df.head())

annual_returns_mean = df[['BTC_Returns', 'ETH_Returns', 'LTC_Returns']].mean() * 252

annual_returns_var = df[['BTC_Returns', 'ETH_Returns', 'LTC_Returns']].var() * 252

annual_returns_std = df[['BTC_Returns', 'ETH_Returns', 'LTC_Returns']].std() * np.sqrt(252)

daily_range_amplitude = df[['BTC_Close', 'ETH_Close', 'LTC_Close']].max() - df[['BTC_Close', 'ETH_Close', 'LTC_Close']].min()
daily_range_amplitude_abs = daily_range_amplitude.abs()

annual_range_amplitude = df.groupby(df['Date'].dt.year)[['BTC_Close', 'ETH_Close', 'LTC_Close']].apply(lambda x: x.max() - x.min())
annual_range_amplitude_abs = annual_range_amplitude.abs()

daily_open_close_amplitude = (df[['BTC_Close', 'ETH_Close', 'LTC_Close']] - df[['BTC_Close', 'ETH_Close', 'LTC_Close']].shift(1)).abs().mean()
annual_open_close_amplitude = df.groupby(df['Date'].dt.year)[['BTC_Close', 'ETH_Close', 'LTC_Close']].apply(lambda x: (x - x.shift(1)).abs().mean())

total_cumulative_returns = (1 + df[['BTC_Returns', 'ETH_Returns', 'LTC_Returns']]).cumprod() - 1

rolling_12_month_returns = df[['BTC_Returns', 'ETH_Returns', 'LTC_Returns']].rolling(window=252).sum()

yearly_returns = df.groupby(df['Date'].dt.year)[['BTC_Returns', 'ETH_Returns', 'LTC_Returns']].sum()

correlation = df[['BTC_Returns', 'ETH_Returns', 'LTC_Returns']].corr()

rolling_correlation = df[['BTC_Returns', 'ETH_Returns', 'LTC_Returns']].rolling(window=45).corr()

print("Média de retornos anual:\n", annual_returns_mean)
print("\nVariância anual:\n", annual_returns_var)
print("\nDesvio padrão anual:\n", annual_returns_std)
print("\nMódulo da amplitude entre máxima e mínima diária:\n", daily_range_amplitude_abs)
print("\nMódulo da amplitude entre máxima e mínima anual:\n", annual_range_amplitude_abs)
print("\nMédia de variação entre abertura e fechamento diária:\n", daily_open_close_amplitude)
print("\nMédia de variação entre abertura e fechamento anual:\n", annual_open_close_amplitude)
print("\nRetorno acumulado total:\n", total_cumulative_returns)
print("\nRetorno acumulado nos últimos 12 meses:\n", rolling_12_month_returns)
print("\nRetorno ano a ano:\n", yearly_returns)
print("\nCorrelação entre os ativos:\n", correlation)
print("\nCorrelação com uma janela móvel de 45 dias:\n", rolling_correlation)

df['Gap'] = (df['BTC_Close'].shift(-1) - df['BTC_Close']) - (df['ETH_Close'].shift(-1) - df['ETH_Close']) - (df['LTC_Close'].shift(-1) - df['LTC_Close'])

df['Gap_Absolute'] = df['Gap'].abs()

annual_mean_gap = df.groupby(df['Date'].dt.year)['Gap_Absolute'].mean()

num_gaps = df[df['Gap'] != 0].shape[0]

print("Número total de gaps:", num_gaps)
print("\nMédia de gaps por ano:\n", annual_mean_gap)

df['Gap_Closed'] = ((df['Gap'] > 0) & (df['BTC_Close'].shift(-1) > df['BTC_Close'])) | ((df['Gap'] < 0) & (df['BTC_Close'].shift(-1) < df['BTC_Close']))

num_gap_closed = df[df['Gap_Closed'] == True].shape[0]

print("Número de vezes que houve fechamento de gap:", num_gap_closed)

import matplotlib.pyplot as plt

correlation_matrix = df[['BTC_Returns', 'ETH_Returns', 'LTC_Returns']].corr()

fig, ax = plt.subplots(figsize=(10, 8))

heatmap = ax.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')

ax.set_xticks(range(len(correlation_matrix.columns)))
ax.set_yticks(range(len(correlation_matrix.columns)))
ax.set_xticklabels(correlation_matrix.columns)
ax.set_yticklabels(correlation_matrix.columns)
ax.set_title('Matriz de Correlação entre Ativos')

plt.colorbar(heatmap)

plt.show()

df_normalized = df[['BTC_Close', 'ETH_Close', 'LTC_Close']].apply(lambda x: (x / x.iloc[0]) * 100)

df_drawdown = df[['BTC_Close', 'ETH_Close', 'LTC_Close']].apply(lambda x: (x / x.cummax() - 1) * 100)

fig, axs = plt.subplots(2, figsize=(12, 8), sharex=True)

df_normalized.plot(ax=axs[0], title='Preços de Fechamento Normalizados', xlabel='Data', ylabel='Preço', grid=True, linewidth=1)

df_drawdown.plot(ax=axs[1], title='Drawdown', xlabel='Data', ylabel='Drawdown (%)', grid=True, linewidth=1)

plt.tight_layout()

plt.show()

import matplotlib.pyplot as plt
import pandas as pd

data_btc = {
    'Data': pd.date_range(start='2018-01-01', end='2024-12-31', freq='Y'),
    'BTC_Close': [None, 30000, 31000, None, None, None, None]
}

data_eth = {
    'Data': pd.date_range(start='2018-01-01', end='2024-12-31', freq='Y'),
    'ETH_Close': [None, 1000, 1100, None, None, None, None]
}

data_ltc = {
    'Data': pd.date_range(start='2018-01-01', end='2024-12-31', freq='Y'),
    'LTC_Close': [None, 200, 250, None, None, None, None]
}

btc_df = pd.DataFrame(data_btc)
eth_df = pd.DataFrame(data_eth)
ltc_df = pd.DataFrame(data_ltc)

df = pd.merge(btc_df, eth_df, on='Data', how='outer')
df = pd.merge(df, ltc_df, on='Data', how='outer')

for column in ['BTC_Close', 'ETH_Close', 'LTC_Close']:
    df[f'{column}_Normalizado'] = df[column] - df[column].iloc[0]

fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 20))

df.plot(x='Data', y=['BTC_Close_Normalizado', 'ETH_Close_Normalizado', 'LTC_Close_Normalizado'], ax=axes[0])
axes[0].set_title('Preços Normalizados')
axes[0].set_ylabel('Preço')

def calculate_drawdown(prices):
    max_price = prices.cummax()
    drawdown = (prices - max_price) / max_price
    return drawdown

for i, column in enumerate(['BTC_Close', 'ETH_Close', 'LTC_Close']):
    drawdowns = calculate_drawdown(df[f'{column}_Normalizado'])
    axes[i+1].plot(df['Data'], drawdowns)
    axes[i+1].set_title(f'Drawdowns - {column}')
    axes[i+1].set_ylabel('Drawdown')

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import pandas as pd

data = {
    'Data': pd.date_range(start='2018-01-01', end='2024-12-31', freq='Y'),
    'BTC_Close': [30000, 31000, 32000, 33000, 34000, 35000, 36000],
    'ETH_Close': [1000, 1100, 1200, 1300, 1400, 1500, 1600],
    'LTC_Close': [200, 250, 300, 350, 400, 450, 500]
}

df = pd.DataFrame(data)

for column in ['BTC_Close', 'ETH_Close', 'LTC_Close']:
    df[f'{column}_Return'] = df[column].pct_change() * 100

plt.figure(figsize=(10, 6))
plt.hist([df['BTC_Close_Return'].dropna(), df['ETH_Close_Return'].dropna(), df['LTC_Close_Return'].dropna()], bins=20, label=['BTC', 'ETH', 'LTC'])
plt.title('Histograma dos Retornos dos Ativos')
plt.xlabel('Retorno (%)')
plt.ylabel('Frequência')
plt.legend()
plt.grid(True)
plt.show()

import pandas as pd

data = {
    'Ano': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'BTC_Max_Drawdown': [-5.0, -4.2, -3.5, -6.1, -4.9, -5.3, -3.8],
    'ETH_Max_Drawdown': [-6.5, -5.7, -4.8, -7.2, -6.0, -6.4, -4.7],
    'LTC_Max_Drawdown': [-7.2, -6.3, -5.4, -8.0, -6.8, -7.1, -5.3],
    'BTC_Retorno_Ano': [10.2, 9.5, 8.8, 11.0, 10.6, 10.8, 9.9],
    'ETH_Retorno_Ano': [9.8, 9.0, 8.3, 10.5, 10.1, 10.3, 9.5],
    'LTC_Retorno_Ano': [8.5, 7.8, 7.1, 9.3, 8.9, 9.1, 8.2],
    'BTC_Desvio_Padrao_Ano': [3.2, 3.0, 2.8, 3.5, 3.3, 3.4, 3.1],
    'ETH_Desvio_Padrao_Ano': [3.0, 2.8, 2.6, 3.3, 3.1, 3.2, 2.9],
    'LTC_Desvio_Padrao_Ano': [2.8, 2.6, 2.4, 3.1, 2.9, 3.0, 2.7],
    'BTC_Max_Drawdown_Historico': -10.0,
    'ETH_Max_Drawdown_Historico': -12.0,
    'LTC_Max_Drawdown_Historico': -11.0,
}

df = pd.DataFrame(data)

print(df)