from dataHandler import getDataSet
from computation import isNumericColumn
import numpy as np
import pickle

# For preformating the numbers (cause of Na's)
def tryToConvToNum(s):
    try:
        return(float(s))
    except ValueError:
        return(None) # will result in nan
# Scaling (using old or new values if training or not)
def scalingData(X, training):
    # Centering/Scaling variables
    # Storing/Retrieving means std devs
    if training:
        ms = []
        stdevs = []
    else:
        ms, stdevs = readScalingParams() # Might throw exception
    # Applying the rescaling
    for i in range(X.shape[0]):
        row = X[i, :]
        if training: # Compute and keeping the scaling
            # Computing for the row the mean and std deviation
            # stdev = np.std(row[np.invert(np.isnan(row))])
            # m = np.mean(row[np.invert(np.isnan(row))])
            stdev = np.nanstd(row)
            m = np.nanmean(row)
            ms += [m]
            stdevs += [stdev]
        else: # Read the scaling
            m = ms[i]
            stdev = stdevs[i]
        # Applying
        for j in range(len(row)):
            if(np.isnan(row[j])):
                row[j] = 0 # mean of the new array
            else:
                row[j] = (row[j] - m)/stdev
        X[i, :] = row
    # Saving the parameters
    writeScalingParams(ms, stdevs)
    return(X)



# Return matrix of values without and with one for biais and vector of labels
def getData(fileName = None, training = True):


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



    # Scaling
    X = scalingData(X, training)


    # Adding ones for biais
    X_1 = np.concatenate((np.array(np.ones((1, X.shape[1]))), X))

    if training:
        # Dealing with labels
        y_str = np.array(ds["Hogwarts House"])
        y_num = np.array([houseNumberConversion(y_i) for y_i in y_str])
        return X, X_1, y_str, y_num
    else:
        return X, X_1
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



# Computes loss for given parameters
def loss(theta, X_1, y_num):
    J = 0
    local_m = X_1.shape[1]
    for i in range(local_m):

        x_i = X_1[:, i]
        theta_j = theta[:,y_num[i]] # Extracting the theta corresponding to the class of x_i

        # Adding the loss of the individual
        J += np.log(hypoFun(theta_j, theta, x_i))
    # Averaging and inverting sign
    J = -J/local_m
    return J
# Computes the gradient of the loss function
def gradLoss(j, theta, X_1, y_num):
    theta_j = theta[:, j]
    DJ = 0
    local_m = X_1.shape[1]
    for i in range(local_m):
        x_i = X_1[:, i]
        # Adding the gradient loss of the individual
        DJ += x_i*(abs(j==y_num[i]) - hypoFun(theta_j, theta, x_i))
    # Averaging and inverting sign
    DJ = -DJ/local_m
    return DJ
# computes the hypothesis function
def hypoFun(theta_j, theta, x_i):
        return(
            (np.exp(np.dot(x_i, theta_j)))
            /
            sum(np.exp(np.dot(theta.T, x_i)))
        )



# Predict for one guy
def predict(theta, x_i_1):
    prob = -1
    housePred = -1
    for house in range(4):
        current_prob = hypoFun(theta[:, house], theta, x_i_1)
        if(current_prob > prob):
            prob = current_prob
            housePred = house
    return(housePred)
# X_topred_1 must be of shape (13 + 1, n) like the original data X
def predictMat(theta, X_topred_1):
    preds = np.array([predict(theta, X_topred_1[:, i]) for i in range(X_topred_1.shape[1])])
    return(preds)
# Percentage of right guesses, throws exception if mismatched vectors
def calcAccuracy(y_pred, y_real):
    if(len(y_pred) != len(y_real)):
        raise ValueError("Trying to compute accuracy of unmatching size vectors (real vs prediction)")
    return(sum(y_real == y_pred)/len(y_pred))



# pickling a dict
def writeTheta(theta):
    with open("params/theta.P", "wb") as fp:
        pickle.dump(theta, fp)
# unpickling a dict
def readTheta():
    with open("params/theta.P", "rb") as fp: # Pickling
        theta = pickle.load(fp)
    return(theta)
# pickling a dict
def writeScalingParams(ms, stds):
    tmp = {"ms":ms, "stds":stds}
    with open("params/scales.P", "wb") as fp:
        pickle.dump(tmp, fp)
# unpickling a dict
def readScalingParams():
    with open("params/scales.P", "rb") as fp: # Pickling
        tmp = pickle.load(fp)
    try:
        ms = tmp["ms"]
        stds = tmp["stds"]
        return ms, stds
    except:
        print('Impossible to retrieve the saved value from last training.')
        return(False)


    # return(res, np.array([houseNumberConversion(y_i) for y_i in res]))



