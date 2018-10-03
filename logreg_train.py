# Source: http://blog.datumbox.com/machine-learning-tutorial-the-multinomial-logistic-regression-softmax-regression/
import numpy as np
from logreg_functions import getData, predictMat, writeTheta, loss, gradLoss, calcAccuracy

# Main function, could've used an object but since no use of inheritance, and storage smaller if only the parameters are stored ..
def train(fileName = None, verbatim = True):

    # Getting data in nice way
    X, X_1, y_str, y_num = getData(fileName, training = True)

    # Defining variables used
    k = 4 # Number of categories
    n = X.shape[0] # Number of explicative variables
    m = X.shape[1] # Number of observations
    trainingPercentage = .8
    alpha = .01 # Learning rate
    iteration_number = 200 # Iteration number
    # iteration_number = 100 # Iteration number



    # Separation into train and validation set
    trainLength = int(trainingPercentage * m)
    testLength = m - trainingPercentage
    np.random.seed(0)
    indexTrain = np.sort(np.random.choice(range(m), trainLength, replace = False))
    indexVal = np.array(list(set(range(m)) - set(indexTrain)))

    X_train = X[:,indexTrain]
    X_train_1 = X_1[:,indexTrain]
    y_train_str = y_str[indexTrain]
    y_train_num = y_num[indexTrain]

    X_val = X[:,indexVal]
    X_val_1 = X_1[:,indexVal]
    y_val_str = y_str[indexVal]
    y_val_num = y_num[indexVal]

    # Initializing weights
    theta = np.zeros((n+1, k))

    for i in range(iteration_number):
        if(i % 25 == 0 and verbatim):
            print("\nIteration number " + str(i))
            print("Loss: " + str(loss(theta, X_train_1, y_train_num)))
            print("Training accuracy: " + str(calcAccuracy(predictMat(theta, X_train_1), y_train_num)))
            print("Validation accuracy: " + str(calcAccuracy(predictMat(theta, X_val_1), y_val_num)))

        for j in range(k):
            theta[:, j] = theta[:, j] - alpha * gradLoss(j, theta, X_train_1, y_train_num)

    # Saving stuff
    writeTheta(theta)





train()