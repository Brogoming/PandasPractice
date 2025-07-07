import pandas as pd

results_numpy = pd.read_csv('./data/results.csv')
results_arrow = pd.read_csv('./data/results.csv', engine='pyarrow', dtype_backend='pyarrow')

print(results_numpy.info(), '\n')
print(results_arrow.info()) # This method explicitly assigns the data closer to its actual data type compared to the default way. Nothing fundamentally changes but if for example you want to mess with strings in the dataframe pyarrow is faster (better optimized)