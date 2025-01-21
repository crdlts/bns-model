import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma
import os


def realized_variance(returns):
    return np.sum(returns ** 2)


def bipower_variation(returns, m):
    mu = np.sqrt(2 / np.pi)
    return mu ** (-2) * (m / (m - 1)) * np.sum(np.abs(returns[1:]) * np.abs(returns[:-1]))


def relative_jump(rv, bv):
    return (rv - bv) / rv


def tripower_quarticity(returns, m):
    mu43 = (2 ** (2/3)) * gamma(7/6) * gamma(1/2)
    return mu43 ** (-3) * (m ** 2 / (m - 2)) * np.sum((np.abs(returns[1:-2]) ** (4/3)) * (np.abs(returns[2:-1]) ** (4/3)) * (np.abs(returns[:-3]) ** (4/3)))


def z_statistic(bv, rj, tp, m):
    vqq = 2
    vbb = (np.pi / 2) ** 2 + np.pi - 3
    return rj / np.sqrt((vbb-vqq) * 1 / m * max(1, tp / (bv ** 2)))


file_path = 'Yandex.csv'

data = pd.read_csv(file_path, delimiter=',', decimal=',', quotechar='"')
data.columns = ['Date', 'Price', 'Open.', 'Max.', 'Min.', 'Volume', 'Shift']

data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%Y')

date_of_month = data['Date'].dt.to_period('M').unique()
date_of_month = [str(date) for date in date_of_month]

data['Price'] = data['Price'].str.replace('.', '', regex=False)
data['Price'] = data['Price'].str.replace(',', '.', regex=False)
data['Price'] = pd.to_numeric(data['Price'], errors='raise')

monthly_data_list = []
for year in range(2014, 2024):
    for month in range(1, 13):
        start_date = f'{year}-{month:02d}-01'
        if month == 12:
            end_date = f'{year + 1}-01-01'
        else:
            end_date = f'{year}-{month + 1:02d}-01'

        filtered_data = data[(data['Date'] >= start_date) & (data['Date'] < end_date)].copy()

        if not filtered_data.empty:
            monthly_data_list.append(filtered_data)

n = len(monthly_data_list)

M = []
for i in range(n):
    monthly_data_list[i]['Returns'] = monthly_data_list[i]['Price'].pct_change(fill_method=None)
    M.append(len(monthly_data_list[i]['Returns']))

RV = [realized_variance(monthly_data_list[i]['Returns']) for i in range(n)]
BV = [bipower_variation(monthly_data_list[i]['Returns'], M[i]) for i in range(n)]
RJ = [relative_jump(RV[i], BV[i]) for i in range(n)]
TP = [tripower_quarticity(monthly_data_list[i]['Returns'], M[i]) for i in range(n)]
Z = [z_statistic(BV[i], RJ[i], TP[i], M[i]) for i in range(len(M))]

combined_returns = pd.concat(monthly_data_list, ignore_index=True)
years = [date[:4] for date in date_of_month]
stock_name = os.path.splitext(os.path.basename(file_path))[0]

plt.figure(figsize=(12, 8))
plt.plot(date_of_month, Z, color='blue', linewidth = 0.5)
plt.title(stock_name)
plt.xlabel('Time')
plt.ylabel('Z - statistic')
plt.xticks(ticks=range(0, len(date_of_month), 12), labels=years[::12])
plt.grid(True)

plt.show()