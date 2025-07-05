import pandas as pd

coffee = pd.read_csv('./warmup-data/coffee.csv')

print(coffee.sort_values("Units Sold", ascending=False)) # you can sort by one or more columns (["Units Sold", "Coffee Type"]) and with ascending you can determine what direction each specific column is sorted [0, 1] (0 is for descending)