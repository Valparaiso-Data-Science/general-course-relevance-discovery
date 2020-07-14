"""
    Train the parameters of the simple ADALINE classifier for determining if file has spacing issues.
"""

import sys
import adaline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def train_adaline(source_filename="diagnostic_results.csv", plots=False, parameter_filename="adaline_wts.npy"):
    """
    Train ADALINE classifier to be able to determine if XML files have broken spacing.

    :param source_filename: CSV file that contains the features and manual labels for "good" and "bad" XML files
    :param plots: whether or not to show plots of the data points and the ADALINE classification boundary
    :param parameter_filename: name of the file where ADALINE weights are stored
    """

    train_df = pd.read_csv(source_filename)
    schools = train_df["school"].values

    # 1st feature: log of the ratio between long word (>=17 chars) matches and total number of words
    log_match_ratio = np.log(train_df["matches"].values / train_df["total words"].values)

    # 2nd feature: average word gain
    avg_word_gain = train_df["average word gain"].values

    # concatenate
    features = np.vstack((log_match_ratio, avg_word_gain)).T

    y = train_df["bad spacing"].values

    # fit classifier to the 2 features and the y (category: ok or bad word spacing)
    spacing_classifier = adaline.AdalineLogistic(n_epochs=500)
    spacing_classifier.fit(features, y)

    if plots:
        # plot results 1. prepare figure
        plt.figure(figsize=(8, 6))
        plt.rcParams.update({'font.size': 6})

        # plot results 2. format school names, the 2 feature columns, and the y into one table
        plottable = np.hstack((features, y.reshape((len(y), 1))))
        plottable = np.hstack((schools.reshape((len(schools), 1)), plottable))

        # plot results 3. plot the observations in the feature space color-coded by y
        plt.scatter(plottable[:, 1][plottable[:, 3] == 1], plottable[:, 2][plottable[:, 3] == 1], label="bad spacing",
                    color="red")
        plt.scatter(plottable[:, 1][plottable[:, 3] == 0], plottable[:, 2][plottable[:, 3] == 0], label="good spacing",
                    color="green")
        # annotate each data point with the source catalog name
        for i in range(len(plottable)):
            row = plottable[i]
            plt.annotate(str(row[0]), (row[1], row[2]))

        # plot results 4. plot adaline decision boundary
        adaline_wts = spacing_classifier.wts  # boundary coefficients a.k.a. adaline weights
        boundary_x = np.linspace(plottable[:, 1].min(), plottable[:, 1].max(), 3)
        boundary_y = (-boundary_x * adaline_wts[1] - adaline_wts[0]) / adaline_wts[2]
        plt.plot(boundary_x, boundary_y, label="classifier decision boundary")

        # plot results: show
        plt.legend()
        plt.title("Catalogs classified by spacing errors")
        plt.xlabel("log (num long word / total number of words)")
        plt.ylabel("average word gain")
        plt.show()

    # save the learned classifier parameters
    np.save(parameter_filename, spacing_classifier.wts)


def main(argv):

    train_adaline(plots=True)


if __name__ == "__main__":
    main(sys.argv)
