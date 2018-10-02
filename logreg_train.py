from dataHandler import getDataSet
from computation import isNumericColumn
import numpy as np

# def main():

# Return matrix of values and vector of labels
def getData(fileName = None):
    # Reading file
    try:
        ds = getDataSet(fileName)
    except ValueError as e:
        print "Error: " + str(e)
        return None

    # Isolate numeric columns
    dsNum = {}
    for key in ds:
        values = ds[key]
        if(isNumericColumn(key, values)):
            dsNum[key]= values

    # Turning into matrix
    dsMat = np.array([dsNum[i] for i in dsNum])





    for i in range(dsMat.shape[0]):
        row = dsMat[i, :]
        stdev = np.std(np.array(row[row!=""], dtype = "float")) # Removing missing values
        for j in range(len(row)):
            if(row[j] != ""):
                row[j] = float(row[j])/stdev
        dsMat[i, :] = row

    return dsMat, ds["Hogwarts House"]

# Both ways, raises exception if unknown
def houseNumberConversion(toConv):
    houseToNum = {"Gryffindor":0, "Slytherin":1, "Ravenclaw":2, "Hufflepuff":3}
    numToHouse = {0:"Gryffindor", 1:"Slytherin", 2:"Ravenclaw", 3:"Hufflepuff"}
    try:
        house = numToHouse[toConv]
        return(house)
    except:
        pass
    try:
        num = houseToNum[toConv]
        return(num)
    except:
        pass
    raise ValueError("Unknown house or number given to houseNumberConversion")

def main(fileName = None):
    # Getting data in nice way
    X, y_str = getData(fileName)
    y_num = np.array([houseNumberConversion(y_i) for y_i in y_str])

    # Defining variables
    k = 4 # Number of categories
    n = X.shape[0] # Number of explicative variables
    m = X.shape[1] # Number of observations
    alpha = .01 # Learning rate
    iteration_number = 200 # Iteration number
    # iteration_number = 100 # Iteration number

    # Initializing weights
    theta = np.zeros((n+1, k))

    for i in range(iteration_number):
        if(i % 5 == 0):
            print("\nIteration number" + str(i))
            print("Loss: " + str(loss(theta, X, y_num, m)))

        for j in range(k):
            theta[:, j] = theta[:, j] - alpha * gradLoss(j, theta, X, y_num, m, k)




def loss(theta, X, y_num, m):
    J = 0
    for i in range(m):
        x_i = np.append(1, X[:, i]) # adding one for the biais
        theta_j = theta[:,y_num[i]] # Extracting the theta corresponding to the class of x_i

        # Let's first consider only the individuals without missing values TODO change
        try:
            x_i = np.array(x_i, dtype = "float")
        except:
            continue

        # Adding the loss of the individual
        J += np.log(hypoFun(theta_j, theta, x_i))
    # Averaging and inverting sign
    J = -J/m
    return J


def hypoFun(theta_j, theta, x_i):
        return(
            (np.exp(np.dot(x_i, theta_j)))
            /
            sum(np.exp(np.dot(theta.T, x_i)))
        )

def gradLoss(j, theta, X, y_num, m, k):
    theta_j = theta[:, j]
    DJ = 0
    for i in range(m):
        x_i = np.append(1, X[:, i]) # adding one for the biais

        # Let's first consider only the individuals without missing values TODO change
        try:
            x_i = np.array(x_i, dtype = "float")
        except:
            continue

        # Adding the gradient loss of the individual
        DJ += x_i*(abs(j==y_num[i]) - hypoFun(theta_j, theta, x_i))
    # Averaging and inverting sign
    DJ = -DJ/m
    return DJ








main(fileName = "dataset_train.csv")
