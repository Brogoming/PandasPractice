import matplotlib.pyplot as plt
import pandas as pd

gas = pd.read_csv('./data/gas_prices.csv')

plt.figure(figsize=(8,5))

plt.plot(gas['Year'], gas['USA'], 'r.-', label='USA')
plt.plot(gas['Year'], gas['Canada'], 'b.-', label='Canada')
plt.plot(gas['Year'], gas['South Korea'], 'g.-', label='South Korea')
plt.plot(gas['Year'], gas['Australia'], 'y.-', label='Australia')

plt.title('Gas Prices Over Time')
plt.xlabel('Years')
plt.ylabel('Dollars/Gallon')

plt.legend()

plt.xticks(gas['Year'][::3].tolist()+[2011]) # Gets every 3rd year and ends at 2011
plt.show()