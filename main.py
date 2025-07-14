import matplotlib.pyplot as plt

labels = ['A', 'B', 'C']
values = [1,4,2]

bars = plt.bar(labels, values) # creates a bar graph by passing in our x (labels) and y (values). Both have to be 1D Arrays

patterns = ['/', 'O', '*']
for bar in bars:
	bar.set_hatch(patterns.pop(0)) # Set the hatch style (for fills)

plt.show()