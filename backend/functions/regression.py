import os
import numpy as np
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')  # Set Matplotlib to use the Agg backend
import matplotlib.pyplot as pyplot

def regression(indicator, startDate, endDate):

    df = yf.download(indicator, start=startDate, end=endDate, interval="1mo")

    df['Time'] = np.arange(len(df.index))
    df = df[['Time', 'Adj Close']]

    x = df.loc[:, ['Time']]  # features
    y = df.loc[:, 'Adj Close']  # target

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = pd.Series(model.predict(x), index=x.index)

    std = df['Adj Close'].std()
    print(std)

    upper_bound = y_pred + 0.68 * std
    lower_bound = y_pred - 0.68 * std

    std68Up = pd.Series(upper_bound, index=x.index)
    std68Dn = pd.Series(lower_bound, index=x.index)

    pyplot.plot(std68Dn, linestyle='dashed', label='68%', color='red')
    pyplot.plot(std68Up, linestyle='dashed', label='68%', color='red')

    upper_bound = y_pred + 0.95 * std
    lower_bound = y_pred - 0.95 * std

    std68Up = pd.Series(upper_bound, index=x.index)
    std68Dn = pd.Series(lower_bound, index=x.index)

    pyplot.plot(std68Dn, linestyle='dashed', label='95%', color='blue')
    pyplot.plot(std68Up, linestyle='dashed', label='95%', color='blue')

    upper_bound = y_pred + 0.99 * std
    lower_bound = y_pred - 0.99 * std

    std68Up = pd.Series(upper_bound, index=x.index)
    std68Dn = pd.Series(lower_bound, index=x.index)

    pyplot.plot(std68Dn, linestyle='dashed', label='99%', color='green')
    pyplot.plot(std68Up, linestyle='dashed', label='99%', color='green')

    # Store the fitted values as a time series with the same time index as
    # the training data
    pyplot.plot(y_pred)
    pyplot.plot(df.index, df['Adj Close'])

    pyplot.legend()


    directory_path = "./static"

    # File path
    file_path = os.path.join(directory_path, "reg.png")

    # Check if the directory exists, and if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Check if the file already exists
    if os.path.exists(file_path):
        # If it exists, remove the file
        os.remove(file_path)

    # Save the plot and close it without displaying
    pyplot.savefig(file_path, bbox_inches='tight')
    pyplot.close()

    return file_path
