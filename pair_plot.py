import matplotlib.pyplot as plt


from histogram import plot_hist
from preprocess_visual import distribute_per_house
from scatter_plot import plot_scatter

from dataHandler import getDataSet


#function that displays the pair plot 
#takes as input : dict = the whole dataset
# return the pair plot (histograms + scatter_plot)


def display_pair_plot(fileName=None):

	#consider two versions of the data : 
	#dict the whole dataset with keys = columns names, values = list columns values
	#dict_per_house with only columns of interest (with marks), keys = column name, val = dict with key = house, values = columns values for this house
	dict = getDataSet(fileName)
	dict_per_house = distribute_per_house(dict)


	#n_rows is the number of key ie the number of courses
	n_rows = len(dict_per_house)

	#we define a big structure for the plot
	f,ax = plt.subplots(n_rows,n_rows,figsize=(50,75))

	list_keys = list(dict_per_house.keys())

	#we scan all keys 
	for i in range(n_rows) : 
		for j in range(n_rows) :
			#x_name is the name of the course x
			#y_name is the name of the course y 
			x_name = list_keys[i]
			y_name = list_keys[j] 

			#if different, we plot a scatter plot
			if(x_name!=y_name):
				plot_scatter(ax[i,j],x_name,y_name,dict_per_house)
			#if identical, we plot an histogram
			if(x_name==y_name):
				plot_hist(ax[i,j],x_name,dict,dict_per_house,50)
	plt.tight_layout()
	#we save the final plot in a .png file
	f.savefig("pair_plot.png")

display_pair_plot()
	

