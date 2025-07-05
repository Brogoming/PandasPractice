# PandasPractice

## Terms
 Dataframe - Essentially a data table that has extra functionality
 
## Functions

### Accessing Data
```python
import pandas as pd

df = pd.DataFrame([[1,2,3], [4,5,6], [7,8,9]], columns=["A", "B", "C"], index=["X", "Y", "Z"]) # Creates a data frame

print(df) # prints all the rows in the dataframe
print(df.head()) # returns the first 5 rows by default, you can also put a number in the () for a specific number of rows
print(df.tail()) # returns the last 5 rows by default, you can also put a number in the () for a specific number of rows
print(df.sample()) # returns random samples of data
print(df.columns.tolist()) # returns the headers
print(df.index.tolist()) # returns the indexes

df.info() # prints the information about the data frame
print(df.describe()) # returns a bunch of useful information about our table like number of items in each column, min of each column, etc...
print(df.nunique()) # returns the number of unique values in each column
print(df.shape) # returns the shape of the dataframe in this case it is a 3 by 3 table
```
```python
import pandas as pd
coffee = pd.read_csv('./warmup-data/coffee.csv') # reads the csv file given, you can also replace it with a url of the data.

results = pd.read_parquet('./olympic-data/results.parquet')

olympicsData = pd.read_excel('./olympic-data/olympics-data.xlsx', sheet_name="results") # if the xlsx file has multiple sheets you can pick one to get data from
```
```python
import pandas as pd

coffee = pd.read_csv('./warmup-data/coffee.csv')

coffee.loc[0, "Units Sold"] = 10 # We can edit data in our dataframe, this includes a whole row, a whole column, a specific cell, etc.... You can use .at[] or .iat[] for more specific results
print(coffee.loc[0:, ["Day", "Units Sold"]]) # allows us to filter out by rows and columns [Rows, Columns]. Rows and columns can be a single value, list of values, slice syntax
print(coffee.Day) # you can access specific columns by calling their name or putting it in square brackets
print(coffee.sort_values("Units Sold", ascending=False)) # you can sort by one or more columns (["Units Sold", "Coffee Type"]) and with ascending you can determine what direction each specific column is sorted [0, 1] (0 is for descending)
coffee.index = coffee.Day # reassigns our index column
```