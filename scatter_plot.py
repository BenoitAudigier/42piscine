from histogram import distribute_per_house
from dataHandler import getDataSet

import matplotlib.pyplot as plt


#FUNCTION displaying a scatter plot for two features
#input : ax : axes, needed when calling displaying functions
#	x_name  = name of the 1st feature to plot
#	y_name = name of the 2nd feature to plot
#	dict_per_house = dict of the data with house granularity
#return : the scatter plot


def plot_scatter(ax,x_name, y_name, dict_per_house):	

	# retrieve the data 
	x_dict = dict_per_house[x_name]
	y_dict = dict_per_house[y_name]

	#on a global figure, we will have 4 differents plots : one per house
	#for each house, we plot the distribution of values
	legend = []

	# looping on the house
	for house in x_dict : 
		x_values = x_dict[house].copy()
		y_values = y_dict[house].copy()
		# we have to remove na values, if one value is na in x_values should also be removed from y_values
		index_na_x = []
		index_na_y = []
		for i in range(len(x_values)):
			if(x_values[i]==''):
				index_na_x.append(i)
			if(y_values[i]==''):
				index_na_y.append(i)

		#create a list of the index to remove, we remove dupplicates and sort the list
		index_to_remove = index_na_x+index_na_y
		index_to_remove = list(set(index_to_remove))
		index_to_remove = sorted(index_to_remove)

		#when removing a value, the index to remove the following one decreases by 1
		for j in range(len(index_to_remove)):
			index_to_remove[j]-=j

		for j in index_to_remove:
			x_values.pop(j)
			y_values.pop(j)


		#we plot the distribution
		ax.plot(x_values,y_values,'o')
		legend.append(house)


	#we don't put title for lisibility for the pair_plot functions.
	#ax.set_title("Comparaison between "+x_name+" and "+y_name)
	ax.legend(legend)
	ax.set_xlabel(x_name)
	ax.set_ylabel(y_name)
	return(ax)


#FUNCTION to display one scatter plot

def display_scatter(x_name,y_name,dict_per_house):
	f,ax = plt.subplots()
	plot_scatter(ax,x_name,y_name,dict_per_house)
	plt.show()
		


#FUNCTION to display the n first scatter_plot
#input : n = the number of plots we want to display
# output : the n plots

def display_all_scatter(n,fileName=None):
	dict = getDataSet(fileName)
	dict_per_house = distribute_per_house(dict)
	c=1
	for k in dict_per_house : 
		for j in dict_per_house : 
			if (k!=j and c<=n):
				display_scatter(k,j,dict_per_house)
				c+=1




display_all_scatter(5)

			