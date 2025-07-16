import matplotlib.pyplot as plt
import pandas as pd

fifa = pd.read_csv('./data/fifa_data.csv')

plt.figure(figsize=(8,5))

left = fifa.loc[fifa['Preferred Foot'] == 'Left'].count()[0]
right = fifa.loc[fifa['Preferred Foot'] == 'Right'].count()[0]

plt.pie([left, right], labels=['Left', 'Right'], colors=['#ff0000', '#00ffff'], autopct='%.2f %%')
# Pass in a list of numeric values, labels of each category, colors of each category, and a string of how to format the percentages

plt.title('Foot Preference of FIFA Players')

plt.show()