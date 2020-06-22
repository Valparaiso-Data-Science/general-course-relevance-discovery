import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from adaline_logistic import AdalineLogistic


def main(argv):

    plt.figure(figsize=(12, 8))

    df = pd.read_csv("wordgain_analysis.csv")

    print(df.keys())

    match_ratio = np.log(df["matches"].values/df["total words"].values)
    avg_word_gain = df["average word gain"].values

    plt.scatter(match_ratio, avg_word_gain, c=df["bad spacing"].values)

    for i in range(len(df)):
        plt.annotate(df["school"][i], (match_ratio[i], avg_word_gain[i]))

    features = np.asarray((match_ratio, avg_word_gain)).T
    y = df["bad spacing"].values.astype(int)

    # plt.show()

    net = AdalineLogistic(n_epochs=500)
    loss, acc = net.fit(features, y)

    print(net.wts)

    x = np.linspace(match_ratio.min(), match_ratio.max(), 50, endpoint=False)
    y = (-net.wts[1]*x - net.wts[0])/net.wts[2]

    plt.plot(x, y)
    plt.xlabel("log of match ratio")
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
