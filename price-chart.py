import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = 'Yandex.csv'

data = pd.read_csv(file_path, delimiter=',', decimal=',', quotechar='"')
data.columns = ['Date', 'Price', 'Open.', 'Max.', 'Min.', 'Volume', 'Shift']

data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%Y')
data.sort_values('Date', inplace=True)

data['Price'] = data['Price'].str.replace('.', '', regex=False)
data['Price'] = data['Price'].str.replace(',', '.', regex=False)
data['Price'] = pd.to_numeric(data['Price'], errors='raise')

stock_name = os.path.splitext(os.path.basename(file_path))[0]

plt.figure(figsize=(12, 8))
plt.plot(data['Date'], data['Price'], color='blue', linewidth = 0.5)

plt.title(stock_name)
plt.xlabel('Time')
plt.ylabel('Price')
plt.grid(True)

plt.show()

file_path_yandex = 'C:/Users/nikit/OneDrive/Рабочий стол/BN-S model/Yandex.csv'
