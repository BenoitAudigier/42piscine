import logreg_train as lt
import numpy as np
import csv

def predictFromCSV(fileName = None):
	# Get data
	X, X_1 = lt.getData(fileName, training = False)

	# get theta
	theta = lt.readTheta()

	# predict
	houseNumberConversionVect = np.vectorize(lt.houseNumberConversion)
	preds = houseNumberConversionVect(lt.predictMat(theta, X_1))

	# Adding the index
	preds = np.vstack((np.array(range(len(preds))), preds)).T

	# Write the csv
	with open("results.csv", "w") as output:
	    writer = csv.writer(output, lineterminator='\n')
	    writer.writerows([["Index", "Hogwarts House"]])
	    writer.writerows(preds)



predictFromCSV()