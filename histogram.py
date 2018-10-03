import matplotlib.pyplot as plt

from computation import compute, isNumericColumn
from dataHandler import getDataSet

# FUNCTION : create new dictionnary with the quantitative data + house granularity
#input :  dict with all columns (quantitative or not), key = column name, values = column values
#output : dict with only quantitative columns,
#key = column name,values = another dict with key = house, v = values of the marks for this house

def distribute_per_house(dict):
    res = {}

    houses = dict['Hogwarts House']
    for key in dict :
        #1.check if the column is a quantitative one, meaning it contains marks
        if isNumericColumn(key,dict[key]):
            values_per_house = {}
            #2. We scan the list dict[key] to build a new dict, key = house and values = values
            for i in range(len(dict[key])):
                #3. We retrieve the house for the i-th value
                current_house = houses[i]
                if current_house in values_per_house:
                    values_per_house[current_house].append(dict[key][i])
                else :
                    values_per_house[current_house]=[dict[key][i]]

            #4. add the new dict to the final result
            res[key]=values_per_house
    return(res)


#FUNCTION : intermediate function : given a list of float values, returns a list of length k
# Count the number of values in each of the k intervals, k intervals are computed by dividing equally the distance between min and max by k 
# be careful, min and max as arguments are not necessary the min and max of the values_list
# indeed, values_list may be the values for a course for a house, while min and max are the min/max considering all houses
def count(values_list,min,max,k):

    #1.create a count list, output of the algo
    count = [0]*k
    
    #2. We remote na values
    values_list = [i for i in values_list if i!='']

    #3. Scan the list to count the number of values in each interval
    for i in values_list:
        if i==max:
            count[-1]+=1
        else:
            index = int((i-min)/(max-min)*k)
            count[index]+=1
    return count

#FUNCTION : intermediate functions to plot the hist
#to plot the hist, we have to plot rectangles and have to need to dupplicate points on x axis
def coord_x_axis(min,max,k):
    res = [min]
    #the limits of the intervals are computed by dividing the distance between min and max in k equal intervals
    for i in range(1,k):
        #to plot rectangles, we need to have two points per abscisses
        res.append(int(min+(max-min)/k*i))
        res.append(int(min+(max-min)/k*i))
    res.append(max)
    return res


#to plot the hist, we have to plot rectangles and dupplicate points, for a same abs x, we have two values : 
# one of the value of the count of values in the interval ending by x
# one of the value of the count of values in the interval beginning by x
#as a result, we just have to dupplicate the count list 
def coord_y_axis(values_list,min,max,k):
    c = count(values_list,min,max,k)
    res = []
    for i in c:
        res.append(i)
        res.append(i)
    return res


#FUNCTION : return the histogram plot
#input : ax : axes, needed when calling displaying functions
#   x_name  = name of the feature to plot
#   dict = dict of the whole data with the course granularity
#   dict_per_house = dict of the data with course/house granularity
#   k : bin of the histogramme

#output : plots of the histogram for the "name" course, with 4 distributions : one per house
def plot_hist(ax,name,dict,dict_per_house,k):
    #we compute the summary from the dictionnary, as we need the min and max info to compute the histogram
    per_house = dict_per_house
    summary = compute(dict)

    #we filter the data only for the course that we are looking for : with the var "name"
    per_house_values = per_house[name]
    min_global = summary[name]["Min"]
    max_global = summary[name]["Max"]

    #compute the coord for the x axis
    x=coord_x_axis(min_global,max_global,k)
    legend = []
    #now, we add a line per house
    for house in per_house_values :
        y=coord_y_axis(per_house_values[house],min_global,max_global,k)
        ax.plot(x,y)
        legend.append(house)
    #ax.set_title(name)
    ax.legend(legend)
    ax.set_xlabel(name)
    ax.set_xlim(min_global,max_global)
    return(ax)



#FUNCTION to display one histogram

def display_hist(x_name,dict,dict_per_house,k):
    f,ax = plt.subplots()
    plot_hist(ax,x_name,dict,dict_per_house,k)
    plt.show()
        


#FUNCTION to display the n first histograms
#input : n = the number of plots we want to display
#       k = bin of the histogram
# output : the n plots

def display_all_hist(n,k,fileName = None):
    dict = getDataSet(fileName)
    dict_per_house = distribute_per_house(dict)
    #init a counter
    c=1
    for key in dict_per_house : 
        if (c<=n):
            display_hist(key,dict,dict_per_house,k)
            c+=1




display_all_hist(5,50)



    
