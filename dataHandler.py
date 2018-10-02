# HOW TO USE
# import dataHandler
# getDataSet()


################################################################################


import sys # read argument
import re # regex fo csv file
import os.path # check existence of file
import csv # to read the csv

# Retrieves data set name from argument given
# Throws exception if bad call from command line
def getDataSetPath():

    # More than one file - could be a feature, todo
    if(len(sys.argv) != 2):
        raise ValueError('Incorrect call of program')

    fileName = sys.argv[1]

    # checking if csv
    if(re.match(r'.*.csv', fileName) is None):
        raise ValueError('Incorrect file name given')

    # checking if it exists
    if(not os.path.isfile('resources/' + fileName)):
        raise ValueError('Incorrect file name given: file does not exists. Please make sure the file is in the folder ressources/')

    return 'resources/' + fileName

# returns a dictionnary with headers as key and list of values for value; path is the path to the csv (must be a csv)
# Trows exception if bad call from command line
def getDataSet():
    path = getDataSetPath()
    return readCSV(path)

# Reads a correctly formed csv
def readCSV(path):
    res = dict() # Storing the res with key = colomn name and val = list of values
    colNames = dict() # Storing the index of each colomn names to remember the order when parcouring the text file
    with open(path) as csv_file: # Should be already a valid file. Few improvements could be made (checking the length of rows and such) but let's suppose we have a valid data set
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader: # Reading the lines
            if line_count == 0: # Treating the headers
                for i in range(len(row)):
                    colNames[i] = row[i]
                    res[row[i]] = []
                line_count += 1
            else:
                for i in range(len(row)): # adding the values to each column
                    res[colNames[i]] += [to_number_or_str(row[i])]
                # line_count += 1
    return res

# Give back str or float following the str given as argument
def to_number_or_str(s):
    try:
        s = float(s)
        return s
    except ValueError:
        return s
