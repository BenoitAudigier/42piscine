import matplotlib.pyplot as plt

from computation import compute, isNumericColumn
from dataHandler import getDataSet


#input :  pre_processed dict with all columns (quantitative or not), key = column name, values = column values
#output : dict with only quantitative columns,
#key = column name,values = dict with key = house, v = values of the marks for this house

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
                
#TEST ON GARDE TOUTES LES VALEURS, MEME LES NA, IL FAUT LES ENLEVER JUSTE AU MOMENT DE PLOT
                if current_house in values_per_house:
                    values_per_house[current_house].append(dict[key][i])
                else :
                    values_per_house[current_house]=[dict[key][i]]

            #4. add the new dict to the final result
            res[key]=values_per_house
    return(res)


#given a list of values, create a count list of length k
#it s a list of the frequencies between min and max, with k intervals
#be careful, the min and max when displaying the results are the min and max of the whole data and not per house

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

#to plot the hist, we have to plot rectangles and have to need to dupplicate points on x axis
def coord_x_axis(min,max,k):
    res = [min]
    for i in range(1,k):
        #to plot rectangles, we need to have two points per abscisses
        res.append(int(min+(max-min)/k*i))
        res.append(int(min+(max-min)/k*i))
    res.append(max)
    return res


#to plot the hist, we have to plot rectangles and dupplicate points
def coord_y_axis(values_list,min,max,k):

    c = count(values_list,min,max,k)
    res = []
    for i in c:
        res.append(i)
        res.append(i)
    return res



#input : dict with all (needed for the summary)
#output : plots of one hist per field, with 4 lines on each : one per house
def display_hist(name,dict,k):
    per_house = distribute_per_house(dict)
    summary = compute(dict)

    #per 'matiere scolaire', we compute a plot
    per_house_values = per_house[name]
    min_global = summary[name]["Min"]
    max_global = summary[name]["Max"]

    x=coord_x_axis(min_global,max_global,k)
    legend = []
    #per house per matiere scolaire, we add a line on the plot
    for house in per_house_values :
        y=coord_y_axis(per_house_values[house],min_global,max_global,k)
        plt.plot(x,y)
        legend.append(house)
    plt.title(name)
    plt.legend(legend)

    plt.xlim(min_global,max_global)
    plt.show()






#input : dict with all (needed for the summary)
#output : plots of one hist per field, with 4 lines on each : one per house
def display_hist_all(dict,k):
    #dict with the house distribution of the quantitative values
    per_house = distribute_per_house(dict)
    summary = compute(dict)

    #per 'matiere scolaire', we compute a plot
    for key in per_house:
        per_house_values = per_house[key]
        min_global = summary[key]["Min"]
        max_global = summary[key]["Max"]

        x=coord_x_axis(min_global,max_global,k)
        legend = []
        #per house per matiere scolaire, we add a line on the plot
        for house in per_house_values :
            y=coord_y_axis(per_house_values[house],min_global,max_global,k)
            plt.plot(x,y)
            legend.append(house)
        plt.title(key)
        plt.legend(legend)

        plt.xlim(min_global,max_global)
        plt.show()



dict = getDataSet("dataset_train.csv")
#dict = distribute_per_house(dict)

compt = 1
for k in dict : 
    if(k!="Index" and isNumericColumn(k, dict[k])):
        print(compt)
        print(k)
        if(compt<10):
            display_hist(k,dict,16)
        compt +=1
    
