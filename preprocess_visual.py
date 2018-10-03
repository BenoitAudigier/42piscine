
from computation import isNumericColumn


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
