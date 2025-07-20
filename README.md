# PandasPractice

## Libraries
- [pandas](https://pandas.pydata.org/docs/)
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/doc/stable/)

## Terms
- Dataframe - Essentially a data table that has extra functionality
- Aggregate - Formed or calculated by the combination of many separate units or items
 
## Pandas Functions

### Accessing Data

**.head(), .tail(), .sample(), .toList(), .describe(), .nunique(), .shape(), .DataFrame()**
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

**.read_parquet(), .read_csv(), .read_excel()**

```python
import pandas as pd

coffee = pd.read_csv(
    './warmup-data/coffee.csv')  # reads the csv file given, you can also replace it with a url of the data.

results = pd.read_parquet('./data/results.parquet')

olympicsData = pd.read_excel('./data/olympics-data.xlsx', sheet_name="results")  # if the xlsx file has multiple sheets you can pick one to get data from
```

**.loc, .sort_values()**
```python
import pandas as pd

coffee = pd.read_csv('./warmup-data/coffee.csv')

coffee.loc[0, "Units Sold"] = 10 # We can edit data in our dataframe, this includes a whole row, a whole column, a specific cell, etc.... You can use .at[] or .iat[] for more specific results
print(coffee.loc[0:, ["Day", "Units Sold"]]) # allows us to filter out by rows and columns [Rows, Columns]. Rows and columns can be a single value, list of values, slice syntax
print(coffee.Day) # you can access specific columns by calling their name or putting it in square brackets
print(coffee.sort_values("Units Sold", ascending=False)) # you can sort by one or more columns (["Units Sold", "Coffee Type"]) and with ascending you can determine what direction each specific column is sorted [0, 1] (0 is for descending)
coffee.index = coffee.Day # reassigns our index column
```
- You can also iterate with every row with **df.iterrows()** but that would make viewing the data much slower.

### Filtering Data

**.query()**
```python
import pandas as pd

bios = pd.read_csv('./data/bios.csv')

print(bios.loc[bios['height_cm'] > 215, ["name", "height_cm"]])  # grabs all athletes taller than 215cm
print(bios[bios['height_cm'] > 215][["name", "height_cm"]])  # this also works
print(bios[(bios['height_cm'] > 215) & (bios['born_country'] == 'USA')])  # You can also do multiple filters
print(bios[bios['name'].str.contains('keith|patrick',case=False)])  # you can filter by data type value, in this case we only want the values that have either keith or patrick as the name (works with regex as by default the regex argument is True)
print(bios.query(
    'born_country == "USA" and born_city == "Seattle"'))  # we can query our data, but it has to be in single quotes
```

### Editing Columns

**.drop(), .rename()**
```python
import pandas as pd
import numpy as np

coffee = pd.read_csv('./warmup-data/coffee.csv')

# Add
coffee['price'] = 4.99 # Creates a new column called price where the default value is 4.99
coffee['new_price'] = np.where(coffee['Coffee Type']=='Espresso', 3.99, 5.99) # we use a numpy where function to add in our new column. The 1st arg is the condition, the 2nd is if the condition is true and the 3rd is if it is false
coffee['revenue'] = coffee['Units Sold'] * coffee['new_price'] # basic math operations
coffee['abbreviation'] = coffee['Coffee Type'].str[0:3] # string operations

# Delete
coffee.drop(columns=['price'], inplace=True) # To drop, not delete, a column you have to specify the columns param. If you only pass in a number it will drop, not delete, the index (row). Setting inplace=True will actually delete the column (or row depending on the param)

# Edit
coffee.rename(columns={'new_price': 'price'}, inplace=True) # allows us to rename the columns

print(coffee.head())
```
- A caveat is if we want to make a new dataframe based on the one we have already created by editing the new dataframe it will also edit the older one. The new dataframe is essentially just pointing to the same dataframe as the old one. If you want to actually copy a dataframe you have to use **.copy()** function.`new_df = org_df.copy()`

**.copy(), .to_datetime(), .apply()**

```python
import pandas as pd

bios = pd.read_csv('./data/bios.csv')
bios_new = bios.copy()  # creates a copy of the dataframe

# Add
bios_new['first_name'] = bios_new['name'].str.split(' ').str[0]  # string operations
bios_new['born_datetime'] = pd.to_datetime(bios_new['born_date'])  # allows us to set the column to a date object column
bios_new['born_year'] = bios_new['born_datetime'].dt.year  # we can do date operations based now that the 'born_datetime' column is a date object column
bios_new['height_category'] = bios['height_cm'].apply(lambda x: 'Short' if x < 165 else ('Average' if x < 185 else 'Tall'))  # you can use lambdas to apply to columns


def categorize_athlete(row):  # we can create custom functions
    if row['height_cm'] < 175 and row['weight_kg'] < 70:
        return 'Lightweight'
    elif row['height_cm'] < 185 and row['weight_kg'] <= 80:
        return 'Middleweight'
    else:
        return 'Heavyweight'


bios['Category'] = bios.apply(categorize_athlete, axis=1)  # we can use custom functions to apply data to our column

print(bios_new.head())
```
- We can also save the dataframe with `bios_new.to_csv('./olympic-data/bios_new.csv', index=False)`. By default, it will save the data with an extra index column so that is why we set index to False in this case

### Merging and Concatenating

**.merge(), .concat()**
```python
import pandas as pd

bios = pd.read_csv('./data/bios.csv')
nocs = pd.read_csv('./data/noc_regions.csv')
results = pd.read_parquet('./data/results.parquet')

bios_new = pd.merge(bios, nocs, left_on='born_country', right_on='NOC', how='left')  # merges to dataframes by the column
combined_df = pd.merge(results, bios, on='athlete_id', how='left')

usa = bios[bios['born_country'] == 'USA'].copy()
gbr = bios[bios['born_country'] == 'GBR'].copy()

new_df = pd.concat([usa, gbr])  # combines 2 dataframes together
```
- If both dataframes have the same column name for you to merge you can just use `on='column name'`. By default, how is inner. If multiple columns have the sameish name you can change the suffixes to make them more clear

### Handling Nulls

**.isna(), .sum(), .fillna(), .interpolate(), .dropna()**
```python
import pandas as pd
import numpy as np

coffee = pd.read_csv('./warmup-data/coffee.csv')
coffee.loc[[0,1], 'Units Sold'] = np.nan # makes the Units Sold column for the 2 rows NaN
print(coffee.isna().sum()) # shows the number of NaNs in each column, if we want non NaNs we can use .notna()

coffee = coffee.fillna(coffee['Units Sold'].mean()) # Fills in the NaN values with the arg given, in this case the mean of all Units Sold values

coffee.loc[[2,3], 'Units Sold'] = np.nan
coffee['Units Sold'] = coffee['Units Sold'].interpolate() # Fills in the NaN values, in this case it's the interpolation of all Units Sold values

coffee.loc[[4,5], 'Units Sold'] = np.nan
coffee.dropna(subset=['Units Sold'], inplace=True) # Drops all the rows that have NaN in them if not specified

print(coffee)
```

### Aggregate Data

**.value_counts, .count(), .reset_index(), .sort_values(), .groupby()**

```python
import pandas as pd

bios = pd.read_csv('./data/bios.csv')
print(bios['born_city'].value_counts())  # returns an aggregated list of cities by how many times they occurred
print(
    bios[bios['born_country'] == 'USA']['born_region'].value_counts())  # we only want those born in the US in this case

bios['born_date'] = pd.to_datetime(bios['born_date'])
print(bios.groupby(bios['born_date'].dt.year)['name'].count().reset_index().sort_values('name', ascending=False))  # .groupby() combined with datetime operations
```

**.pivot()**
```python
import pandas as pd
import numpy as np

coffee = pd.read_csv('./warmup-data/coffee.csv')
coffee['price'] = np.where(coffee['Coffee Type']=='Espresso', 3.99, 5.99)
coffee['revenue'] = coffee['Units Sold'] * coffee['price']

print(coffee.groupby(['Coffee Type'])['Units Sold'].sum()) # groups all the coffe types and combine the Units Sold for the same types
print(coffee.groupby(['Coffee Type']).agg({'Units Sold': 'sum', 'price': 'mean'})) # allows us to specify multiple columns to group by

pivot = coffee.pivot(columns='Coffee Type', index='Day', values='revenue') # We pivot the coffee table where the coffee types are the headers and day is our index to see the revenue we generate each day
print(pivot) # our new dataframe that is a pivot of coffee
print(pivot.loc["Monday", "Latte"]) # we can get Monday's latte count
```

### Advanced Functionality

**.shift()**
```python
import pandas as pd
import numpy as np

coffee = pd.read_csv('./warmup-data/coffee.csv')
coffee['price'] = np.where(coffee['Coffee Type']=='Espresso', 3.99, 5.99)
coffee['revenue'] = coffee['Units Sold'] * coffee['price']
coffee['yesterday_revenue'] = coffee['revenue'].shift(2) # Shifts the values from the revenue column by 2 for the yesterday_revenue column, you can also shift backwards
coffee['precent_change'] = coffee['revenue']/coffee['yesterday_revenue'] * 100

print(coffee)
```

**.rank()**

```python
import pandas as pd

bios = pd.read_csv('./data/bios.csv')
bios['height_rank'] = bios['height_cm'].rank()  # gets the rank of each row by the column value of a row, in this case 'height_cm'
bios['height_rank'].sort_values(ascending=False)

print(bios.sort_values(['height_rank'], ascending=False))
```

**.cumsum(), .rolling()**
```python
import pandas as pd
import numpy as np

coffee = pd.read_csv('./warmup-data/coffee.csv')
coffee['price'] = np.where(coffee['Coffee Type']=='Espresso', 3.99, 5.99)
coffee['revenue'] = coffee['Units Sold'] * coffee['price']

print(coffee.select_dtypes('float').cumsum()) # shows the cumulative sum of the float types as it goes through each row

coffee['cumulative_revenue'] = coffee['revenue'].cumsum() # adds the results together as it goes through the rows
print(coffee.loc[0: ,['revenue', 'cumulative_revenue']])

latte = coffee[coffee['Coffee Type'] == "Latte"].copy()
print(latte['Units Sold'].rolling(3).sum()) # grabs the last 3 rows and gets the sum of those rows
```

### Extra Bits

**pyarrow**
```python
import pandas as pd

results_numpy = pd.read_csv('./data/results.csv')
results_arrow = pd.read_csv('./data/results.csv', engine='pyarrow', dtype_backend='pyarrow')

print(results_numpy.info(), '\n')
print(results_arrow.info()) # This method explicitly assigns the data closer to its actual data type compared to the default way. Nothing fundamentally changes but if for example you want to mess with strings in the dataframe pyarrow is faster (better optimized)
```

## matplotlib Functions

### Basic Graphs
#### Line Graph

**.plot(), .show(), .title(), .xlabel(), .ylabel(), .figure(), .xticks(), .yticks(), .legend(), .savefig(), .show()**
```python
import matplotlib.pyplot as plt
import numpy as np

x = [0,1,2,3,4]
y = [0,2,4,6,8]
x2 = np.arange(0, 4.5, 0.5)

plt.figure(figsize=(5,4), dpi=150) # Resize the graph (dpi = pixels per inch)

# Plotting the data
plt.plot(x, y, label='2x', color='red', marker='.', linestyle='dashed', linewidth='2', markersize=12) # x (independent data) and y (dependent data) need to be 1D arrays
plt.plot(x2[:6], x2[:6]**2, 'gv-', label='x^2') # another way of styling the graph
plt.plot(x2[5:], x2[5:]**2, 'b^:', label='x^2') # The data can be split as long as it is still a 1D array

# Title and labels
plt.title('My First Graph', fontdict={'fontname': 'Comic Sans MS', 'fontsize': 20}) # Sets the title of the graph
plt.xlabel('Independent', fontdict={'fontname': 'Times New Roman'}) # Sets the label of the x-axis
plt.ylabel('Dependent') # Sets the label of the y-axis

# Tick marks
plt.xticks(range(0,10)) # Manually set the x-axis ticks
plt.yticks(range(0,10)) # Manually set the y-axis ticks

# Setting the legend, saving the graph, and showing the graph
plt.legend() # gives us a legend that lists all the labels and their corresponding data
plt.savefig('mygraph.png', dpi=300) # saves the graph as a png image
plt.show() # This is what shows the graph, without it, we can't see the data
```

#### Bar Chart

**.bar(), .set_hatch()**
```python
import matplotlib.pyplot as plt

labels = ['A', 'B', 'C']
values = [1,4,2]

bars = plt.bar(labels, values) # creates a bar graph by passing in our x (labels) and y (values). Both have to be 1D Arrays

patterns = ['/', 'O', '*']
for bar in bars:
	bar.set_hatch(patterns.pop(0)) # Set the hatch style (for fills)

plt.show()
```

### Examples
#### Line Graph (gas prices)

```python
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
```

#### Histogram (fifa)
```python
import matplotlib.pyplot as plt
import pandas as pd

fifa = pd.read_csv('./data/fifa_data.csv')

plt.figure(figsize=(8,5))
bins = range(40,100,10)
plt.hist(fifa["Overall"], bins=bins, color='#ff00dd') # histogram that shows the number of players that have an overall score between the bins
plt.xticks(bins)

plt.title('Distribution of Player Skills in FIFA 2018')
plt.xlabel('Skill Level')
plt.ylabel('Number of Players')

plt.show()
```

#### Pie Chart (fifa)
```python
import matplotlib.pyplot as plt
import pandas as pd

fifa = pd.read_csv('./data/fifa_data.csv')

left = fifa.loc[fifa['Preferred Foot'] == 'Left'].count().iloc[0]
right = fifa.loc[fifa['Preferred Foot'] == 'Right'].count().iloc[0]

plt.pie([left, right], labels=['Left', 'Right'], colors=['#ff0000', '#00ffff'], autopct='%.2f %%')
# Pass in a list of numeric values, labels of each category, colors of each category, and a string of how to format the percentages

plt.title('Foot Preference of FIFA Players')

plt.show()
```

```python
import matplotlib.pyplot as plt
import pandas as pd

fifa = pd.read_csv('./data/fifa_data.csv')

plt.style.use('bmh') # default styles to use https://matplotlib.org/3.1.0/gallery/style_sheets/style_sheets_reference.html

fifa["Weight"] = [int(x.strip('lbs')) if type(x)==str else x for x in fifa["Weight"]]

light = fifa.loc[fifa["Weight"] < 125].count().iloc[0]
light_medium = fifa.loc[(fifa["Weight"] >= 125) & (fifa["Weight"] < 150)].count().iloc[0]
medium = fifa.loc[(fifa["Weight"] >= 150) & (fifa["Weight"] < 175)].count().iloc[0]
heavy_medium = fifa.loc[(fifa["Weight"] >= 175) & (fifa["Weight"] < 200)].count().iloc[0]
heavy = fifa.loc[fifa["Weight"] >= 200].count().iloc[0]

weights = [light, light_medium, medium, heavy_medium, heavy]
labels = ['Light', 'Light Medium', 'Medium', 'Heavy Medium', 'Heavy']
explode = (.4,.1,0,0,.4)

plt.pie(weights, labels=labels, autopct='%.2f %%', pctdistance=0.8, explode=explode) # pctdistance = percentage distance, explode = spaces out the sections
plt.title('Player Weights (in lbs) by Category')
plt.show()
```

#### Box and Whiskers (fifa)
```python
import matplotlib.pyplot as plt
import pandas as pd

fifa = pd.read_csv('./data/fifa_data.csv')

barcelona = fifa.loc[fifa["Club"] == 'FC Barcelona']['Overall']
madrid = fifa.loc[fifa["Club"] == 'Real Madrid']['Overall']
revs = fifa.loc[fifa["Club"] == 'New England Revolution']['Overall']
labels = ['FC Barcelona', 'Real Madrid', 'New England Revolution']

boxes = plt.boxplot([barcelona, madrid, revs], tick_labels=labels, patch_artist=True, medianprops={'linewidth': 2}) # x needs to be a list of integer lists
for box in boxes['boxes']:
	box.set(color='#4286f4', linewidth=2) # set edge color
	box.set(facecolor='#e0e0e0') # change the inside of the box

plt.title('Overall Club Scores')
plt.ylabel('FIFA Team Comparison')

plt.show()
```