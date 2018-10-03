from dataHandler import getDataSet
from computation import isNumericColumn
import numpy as np

def tryToConvToNum(s):
    try:
        return(float(s))
    except ValueError:
        return(None) # will result in nan



# Return matrix of values and vector of labels
def getData(fileName = None):
    # Reading file
    try:
        ds = getDataSet(fileName)
    except ValueError as e:
        print("Error: " + str(e))
        return(None)

    # Isolate numeric columns
    dsNum = {}
    for key in ds:
        values = ds[key]
        if(isNumericColumn(key, values)):
            dsNum[key]= values

    # Turning into matrix
    dsMat = np.array([dsNum[i] for i in dsNum])
    # Replacing NA by None and converting to float
    X = np.vectorize(tryToConvToNum)(dsMat)

    # Centering/Scaling varaibles
    for i in range(X.shape[0]):
        row = X[i, :]
        # Computing for the row the mean and std deviation
        # stdev = np.std(row[np.invert(np.isnan(row))])
        # m = np.mean(row[np.invert(np.isnan(row))])
        stdev = np.nanstd(row)
        m = np.nanmean(row)
        # Applying
        for j in range(len(row)):
            if(np.isnan(row[j])):
                row[j] = 0 # mean of the new array
            else:
                row[j] = (row[j] - m)/stdev
        X[i, :] = row


    X_1 = np.concatenate((np.array(np.ones((1, X.shape[1]))), X))

    y_str = np.array(ds["Hogwarts House"])
    y_num = np.array([houseNumberConversion(y_i) for y_i in y_str])

    return X, X_1, y_str, y_num

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
    X, X_1, y_str, y_num = getData(fileName)

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
        if(i % 25 == 0):
            print("\nIteration number" + str(i))
            print("Loss: " + str(loss(theta, X_1, y_num, m)))

        for j in range(k):
            theta[:, j] = theta[:, j] - alpha * gradLoss(j, theta, X_1, y_num, m, k)

    print("Train prediction:")
    for i in range(50):
        print("Dude number " + str(i))
        predict(theta, X_1[:, i])
        print('Reality: ' + y_str[i])
        print("\n")


# Computes loss for given parameters
def loss(theta, X_1, y_num, m):
    J = 0
    for i in range(m):

        x_i = X_1[:, i]
        theta_j = theta[:,y_num[i]] # Extracting the theta corresponding to the class of x_i

        # Adding the loss of the individual
        J += np.log(hypoFun(theta_j, theta, x_i))
    # Averaging and inverting sign
    J = -J/m
    return J

# computes the hypothesis function
def hypoFun(theta_j, theta, x_i):
        return(
            (np.exp(np.dot(x_i, theta_j)))
            /
            sum(np.exp(np.dot(theta.T, x_i)))
        )


def gradLoss(j, theta, X_1, y_num, m, k):
    theta_j = theta[:, j]
    DJ = 0
    for i in range(m):
        x_i = X_1[:, i]
        # Adding the gradient loss of the individual
        DJ += x_i*(abs(j==y_num[i]) - hypoFun(theta_j, theta, x_i))
    # Averaging and inverting sign
    DJ = -DJ/m
    return DJ



# X_test must be of shape (13, n) like the original data X
def predict(theta, x_i_1):
    for house in range(4):
        print(houseNumberConversion(house))
        print(hypoFun(theta[:, house], theta, x_i_1))

    # return(res, np.array([houseNumberConversion(y_i) for y_i in res]))

# main(fileName = "dataset_train.csv")
#TODO clean up that shit, add separation train and test, compute prediction, be better on missing values, comment
# Source: http://blog.datumbox.com/machine-learning-tutorial-the-multinomial-logistic-regression-softmax-regression/
