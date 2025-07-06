import pandas as pd

bios = pd.read_csv('./olympic-data/bios.csv')
bios_new = bios.copy() # creates a copy of the dataframe

bios_new['first_name'] = bios_new['name'].str.split(' ').str[0] # string operations
bios_new['born_datetime'] = pd.to_datetime(bios_new['born_date']) # allows us to set the column to a date object column, you can also format the data as well
bios_new['born_year'] = bios_new['born_datetime'].dt.year # we can do date operations based now that the 'born_datetime' column is a date object column

print(bios_new.head())