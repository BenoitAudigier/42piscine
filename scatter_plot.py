from histogram import distribute_per_house
from dataHandler import getDataSet

import matplotlib.pyplot as plt


#input : dictionnary per house 

# Display one plat for two features given the list of houses
# x : vector/list of the 1st feature to plot
# y : vector/list of the 2nd feature to plot
# xlabel : name of the 1st feature
# ylabel : name of the 2nd feature
# no return
def one_plot(x_name, y_name, dict_per_house):
	
	x_dict = dict_per_house[x_name]
	y_dict = dict_per_house[y_name]

	#then, for each house, we plot the distribution of values
	#we consider that we have values for every house for every "matiere scolaire" : TO TEST
	legend = []
	for house in x_dict : 
		print(house)
		#if (house in y_dict):
			# do have marks for this house for the y_values
		x_values = x_dict[house].copy()
		y_values = y_dict[house].copy()
		# we have to remove na values, if one value is na in x_values should also be removed from y_values
		print(len(x_values)==len(y_values))
		index_na_x = []
		index_na_y = []
		for i in range(len(x_values)):
			if(x_values[i]==''):
				index_na_x.append(i)
			if(y_values[i]==''):
				index_na_y.append(i)

		index_to_remove = index_na_x+index_na_y
		index_to_remove = list(set(index_to_remove))
		index_to_remove = sorted(index_to_remove)
		#remove dupplicate
		
		#print(index_to_remove)
		for j in range(len(index_to_remove)):
			index_to_remove[j]-=j
		print(index_to_remove)

		if index_to_remove != []:
			print(max(index_to_remove)>len(x_values))

		for j in index_to_remove:
			x_values.pop(j)
			y_values.pop(j)


		plt.plot(x_values,y_values,'o')
		legend.append(house)


	plt.title("Comparaison between "+x_name+" and "+y_name)
	plt.legend(legend)
	plt.xlabel(x_name)
	plt.ylabel(y_name)
	print("de")
	plt.show()
		





dict = getDataSet("dataset_train.csv")
dict = distribute_per_house(dict)

compt = 1
for k in dict : 
	for j in dict : 
			print(compt)
			print(k)
			print(j)
			if(k!=j and compt<10):
				print(k)
				print(j)
				#print(len(dict[k][h]))
				#print(len(dict[j][h]))
				one_plot(k,j,dict)
			compt +=1
			