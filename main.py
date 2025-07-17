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