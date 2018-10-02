from dataHandler import getDataSet
from computation import compute

def printSummaryForGivenDataset():
    # Reading file
    try:
        ds = getDataSet()
    except ValueError as e:
        print "Error: " + str(e)
        return None

    # for key in ds:
    #     print "key: %s \n\n, value: %s \n\n\n" % (key, len(ds[key]))


    # Computing required values
    print(ds)
    print("\n\n\n\n\n")
    info = compute(ds)
    print(info)

printSummaryForGivenDataset()
