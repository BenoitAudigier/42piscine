import itertools 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import itertools

# Load data using pandas
def load_raw_data(path = "dataset_train.csv"):
    dataset = pd.read_csv("resources/" + path)
    return(dataset)
   
# Preprocess data to get only numerical values
# raw_data : panda dataframe from the CSV file
# return panda dataframe with only numerical values, and removing the index column 
def select_numerical(raw_data):
    dataset_numeric = raw_data.replace('', np.nan)._get_numeric_data().drop('Index', 1)
    return(dataset_numeric)

# Display one plat for two features given the list of houses
# x : vector/list of the 1st feature to plot
# y : vector/list of the 2nd feature to plot
# xlabel : name of the 1st feature
# ylabel : name of the 2nd feature
# no return
def one_plot(x, y, house, xlabel, ylabel):
    for h in set(house):
        plt.plot(x[np.where(house == h)], y[np.where(house == h)], 'o', label = str(h))    
    plt.legend(house)
    plt.title("Comparison between " + str(xlabel) + " and " + str(ylabel))

# Display all plot calling the one plot function on each pair of features
def all_plots(dataset_numeric, house):
    cols = dataset_numeric.columns
    for (feat1, feat2) in itertools.combinations(cols, 2):
        plt.figure()
        x = dataset_numeric[feat1].values
        y = dataset_numeric[feat2].values
        one_plot(x, y, house, feat1, feat2)
        plt.show()
             
def main():
    raw_data = load_raw_data("dataset_train.csv")
    house = raw_data['Hogwarts House'].values
    dataset_numeric = select_numerical(raw_data)
    all_plots(dataset_numeric, house)
    
main()