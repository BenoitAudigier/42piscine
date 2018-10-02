import numpy as np

def partition(current_list,g,d):

    #g correspond a l'index gauche
    #d correspond a l'index droit
    #on partitionne la liste entre g et d autour d'un pivot
    #par defaut, le pivot est choisi comme etant egal a current_list[g]
    p=g
    pivot = current_list[g]
    for k in range(g+1,d):
        if current_list[k]<pivot:
            p+=1
            current_list[p],current_list[k] = current_list[k],current_list[p]
    current_list[p], current_list[g] = current_list[g],current_list[p]
    return p

def quicksort(current_list,g,d):
    # le tri rapide marche alors par recursivite
    # on partionne la liste suivant le pivot choisi
    #puis, on re-trie la liste entre l'index gauche et le pivot
    # et entre l'index droit et le pivot
    if g<d:
        p =partition(current_list,g,d)
        quicksort(current_list,g,p)
        quicksort(current_list,p+1,d)


#calculation calcule toutes les informations du describe()
# input : une colonne d'un dataset en liste
# output : dictionnaire res avec toutes les informations

# Comptute required values for one line
def calculation(l):
    print("Going for:" + str(l[0:10]))

    #prend en argument une liste
    l = list(l)
    n = len(l)

    res=[]

    #pour calculer la mediane et les quantiles, on a besoin d'une liste triee
    # quicksort(l,0,n)
    l = sorted(l)

    #definition de variables pour calculer moyenne, std, min et max
    sum = 0
    sum_carre = 0
    min = 0
    max = 0
    #en parcourant la liste, on calcule mean,std,min et max
    for i in l:
        # si i n'est pas un entier, on ne le prend pas en compte dans les calculs
        ## TODO: rajouter un warning
        if(i==np.nan or i == ''):
            continue
        sum = sum + i
        sum_carre = sum_carre + i**2
        if(i<min):
            mon = i
        if(i>max):
            max = i


    #on cree le dictionnaire res avec toutes les informations voulues

    # res["mean"]=sum/n
    # res["count"] = sum
    # res["std"] = sum_carre/n - (sum/n)**2
    # res["min"] = min
    # res["max"]=max
    # res["25%"]=l[int(n/4)]
    # res["50%"]=l[int(n/2)]
    # res["75%"]=l[int(n*3/4)]

    res = [n,sum/n,(sum_carre/n - (sum/n)**2),min,l[int(n/4)],l[int(n/2)],l[int(n*3/4)],max]
    return(res)


#compute function
# input : dictionnaire avec en cles les noms des colonnes et en valeurs, la colonne sous forme de liste
# output : dictiionnaire avec en cles les noms des colonnes quantitatives, et en valeurs, les informations summary sous forme de liste

# Takes a dictionary and returns another one with the info on the numeric lists inside
def compute(dict):
    #dict est un dictionnaire avec les noms des columns en cles
    # et une liste des valeurs en argument

    res = {}
    for key in dict:
        values = dict[key] #todo consider only the 5 firsts, or the first one as long as not ''
        if(isNumericColumn(values)):
            res[key]= calculation(values)
    return res

# We consider that if we have a numeric value in first five values, then the column is numeric.
# The value 5 and not one is to make sure the NA do not disturb the result.
def isNumericColumn(column):
    for c in column[0:5]:
        if(type(c) == float or type(c) == int):
            return(True)
    return(False)



# dict = {}
# dict['a'] = [0,14,5,7,8]
# dict["b"] = ["f","fe","g","ge","d"]
# dict["c"]=[0,45,1,2,4]
# print(compute(dict))
