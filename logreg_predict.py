from logreg_functions import getData, readTheta, houseNumberConversion, predictMat
import numpy as np
import csv

def predictFromCSV(fileName = None):
	# Get data
	X, X_1 = getData(fileName, training = False)

	# get theta
	theta = readTheta()

	# predict
	houseNumberConversionVect = np.vectorize(houseNumberConversion)
	preds = houseNumberConversionVect(predictMat(theta, X_1))

	# Adding the index
	preds = np.vstack((np.array(range(len(preds))), preds)).T

	# Write the csv
	with open("results.csv", "w") as output:
	    writer = csv.writer(output, lineterminator='\n')
	    writer.writerows([["Index", "Hogwarts House"]])
	    writer.writerows(preds)



predictFromCSV()