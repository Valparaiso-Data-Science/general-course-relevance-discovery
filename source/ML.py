# -*- coding: utf-8 -*-
"""
--Do we need this file?--


Created on Mon Jul 22 13:50:39 2019

@author: nrandle
@co-author: Frankie & Sasha
"""
import os
import sys
import const
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn import tree,metrics
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from io import StringIO
from IPython.display import Image
import pydotplus
import graphviz
from subprocess import call
from imblearn.under_sampling import RandomUnderSampler, NearMiss
import numpy as np
from numpy import asarray, save, load
import pandas as pd

from vectorize import newClean, vectorizer, cleanVectorizer, labelTargetsdf

def preProcess():
    cleaned_df = pd.read_csv(const.CSV_DIR + "/" + const.ALL_CSV, encoding="ISO-8859-1")

    print("\tcleaned")
    vect_df = vectorizer(cleaned_df)
    print("\tvect")
    pruned_df = cleanVectorizer(vect_df)
    print("\tpruned")
    labeled_df = labelTargetsdf(pruned_df)
    print("\tfound targets")
    #%%
    features = labeled_df.drop("curricula relevance",axis = 1).astype("bool")
    labels = labeled_df["curricula relevance"]

    return features,labels

def stratKFold(features,labels,splits=10):
    '''
    Parameters
    ----------
    features : list
        Array of feature data.
    labels : list
        Array of labels.
    splits : int
        Number of splits to use in the stratified k-fold.

    Returns
    -------
    None.
    It does, however, save the indices to a file that can be used at a later point.

    Notes
    -----
    Saving the indices is done to save time. This block of code takes a pretty
    long time to run. Therefore it is possible to run the random forest using
    the already saved indices. This function should only be called if the data
    is altered and the algorithm needs to be retrained.

    The current implementation uses a random undersampler. This is not ideal.
    The goal is to convert to using a near miss algorithm to conduct the
    undersampling. The switch to random undersampling was done to save time
    when debugging the saving of the indices.
    '''

    skf = StratifiedKFold(n_splits=splits,shuffle=True, random_state = 19)
    # skf.split(features,labels)
    # errors = []
    fold_iterations = [0]*10
    count=0
    features.reset_index(inplace=True)
    for train_index, test_index in skf.split(features, labels):
        indices = [0]*2
        indices[1]=test_index
        print("TRAIN:", train_index, "TEST:", test_index)
        # X_train = [features.iloc[i] for i in train_index]
        # X_test=[features.iloc[i] for i in test_index]
        X_train = features.iloc[train_index]
        # X_test = features.iloc[test_index]
        y_train = labels.iloc[train_index]
        # y_test = labels.iloc[test_index]
        maj_train_index = undersample(X_train,y_train)
        #features = features.reset_index()

        ds_i = features.index[labels == 1]

        train_index = np.append(maj_train_index,ds_i)
        print("NEW TRAIN: ", train_index)
        indices[0]=train_index
        fold_iterations[count]=indices
        count+=1
    fold_iterations = asarray(fold_iterations)
    save('fold_iterations.npy',fold_iterations)
    print(fold_iterations)

def randForest(features,labels):
    '''
    Parameters
    ----------
    features : list
        Array of feature data.
    labels : list
        Array of labels.

    Returns
    -------
    None.

    Notes
    -----
    Prints out the average for each cross-validation iteration, as well as the
    overall average (Computed by taking the average of the averages) of the
    random forest.

    It also loads in fold_iterations.npy which is a file that stores the indices
    for each test-train split computed by the stratified k-fold function. The
    point of seperating the two was to save time. There should be no need to
    run stratKFold() unless changes are made directly to it.

    There is currently an index out of bounds error that is in the process of 
    being debugged. The good news is that fold_iterations loads in. 


    '''
    fold_iterations = load('fold_iterations.npy',allow_pickle=True)
    accs = [0]*len(fold_iterations)
    rf = RandomForestClassifier(n_estimators = 100, random_state = 42)
    count = 0
    for fold in fold_iterations:
        X_train = features.iloc[fold[0].tolist()]
        y_train = labels.iloc[fold[0].tolist()]
        X_test = features.iloc[fold[1].tolist()]
        y_test = labels.iloc[fold[1].tolist()]
        rf.fit(X_train, y_train)
        preds = rf.predict(X_test)
        #errors.append(round(np.mean(abs(preds - y_test)),2))
        forAc = rf.score(X_test,y_test)
        accs[count] = forAc
        print('Mean Accuracy for forest #' + str(count) +': ' + str(forAc))
        print(confusion_matrix(y_test, preds))
        count += 1
    avgAcc = sum(accs)/len(accs)
    print('Average Model Accuracy: '+ str(avgAcc))
        #vizRFTrees(rf, 5, features)
    ####################################################
    # count = 0
    # modelAc= sum(accs)/len(accs)
    # print("Average Model Accuracy: "+ str(modelAc*100))
    # results = open('../source/RandForestResult.txt','w')
    # r = results.write("Average Model Accuracy: "+ str(modelAc*100))
    # results.close()
def svm(features,labels,splits):
    '''
    Parameters
    ----------
    features : list
        Array of feature data.
    labels : list
        Array of labels.
    splits : int
        Number of splits to use in the stratified k-fold.

    Returns
    -------
    None.

    Notes
    -----
    This is not in a working state currently. This function is using an old
    code structure. Looking at the randForest() function, it does not do any
    of the stratified k-fold, but instead loads a file of saved indices. If
    this code is looking to be used, one must first change the format to look
    more like randForest(). Another reason we save the indices was to allow us
    to be able to do different machine-learning algorithms using the same
    test-train splits made by the k-fold function.

    '''
    skf = StratifiedKFold(n_splits=splits,shuffle=True, random_state = 19)
    # skf.split(features,labels)
    # errors = []
    accs = [0]*splits
    count=0
    for train_index, test_index in skf.split(features, labels):
        print("TRAIN:", train_index, "TEST:", test_index)
        # X_train = [features.iloc[i] for i in train_index]
        # X_test=[features.iloc[i] for i in test_index]
        X_train = features.iloc[train_index]
        X_test = features.iloc[test_index]
        y_train = labels.iloc[train_index]
        y_test = labels.iloc[test_index]
        svm = SVC(kernel='poly')
        svm.fit(X_train,y_train)
        preds = svm.predict(X_test)
        i=0
        for pred in preds:
            if pred == y_test[i]:
                accs[count]+=1
            i +=1
        accs[count] = (accs[count]/len(preds))*100
        count += 1
        #print('Accuracy: ' + str(accuracy_score(X_test,y_test)))
        print(confusion_matrix(y_test, preds))
    count = 0
    for acc in accs:
        #print("Mean Absolute Error for Forest #" + str(count) + ": " + str(error) + ' degrees.')
        print("Accuracy for SVM #"+ str(count)+ ": " + str(acc) + " percent")
        count += 1


def undersample(features, labels, split=0.5):
    '''
    Parameters
    ----------
    features : list
        Array of feature data.
    labels : list
        Array of labels.
    split : float, optional
        This is the ratio of minority class samples to
        the resampled majority class samples. The default is 0.5. Currently
        only used when we use random undersampling. It can, however, be used
        for near miss.

    Returns
    -------
    newLabels : numpy array
        The indices of the resampled majority class samples determined by the
        undersampling method.
        
    Notes
    -----
    The current implementation uses random undersampling for time purposes. 
    It runs quicker and allowed us to test our code faster. This should not be
    used in the final implementation. Using a near miss algorithm would be much
    better. We recommend near miss 3. 

    '''
    rus = RandomUnderSampler(sampling_strategy=split, random_state=19)
    # nmus = NearMiss(version=3,sampling_strategy={0:sum(labels),1:sum(labels)})
    # nmus.fit_resample(features, labels)
    # newLabels = nmus.sample_indices_
    rus.fit_resample(features,labels)
    newLabels = rus.sample_indices_
    print(len(newLabels))
    #print(sum(newLabels))
    # print(newFeatures)
    return newLabels

def vizRFTrees(rf, ntree,features):
    '''
    Parameters
    ----------
    rf : random forest
        The final fit to all data random forest.
    ntree : int
        The number of trees you wish to display.
    features : list
        Array of feature data.

    Returns
    -------
    None.
    
    Should theoretically print out the decision trees from the random forest.
    
    Notes
    -----
    This is not ready to be used for multiple reasons:
        1. Random Forest code doesn't even work yet
        2. Because of the point above, we are not sure this works. 

    '''
    outfile='randFor_Tree'+ntree+'.dot'
    export_graphviz(rf.estimators_[ntree],outfile = outfile,feature_names=list(features.columns),
                    filled=True)
    call(['dot', '-Tpng', outfile, '-o', 'tree.png', '-Gdpi=600'])
    Image(filename='tree.png')

# decisionTree and visTree were from the summer before ours (ie nathan wrote it)
# Random forest was made to upgrade decision tree
# vizRFTrees was made to replace visTree
def decisionTree(feature_train,answer_train,depth):

    #forestClassifier = RandomForestClassifier(n_estimators=depth)
#    forestClassifier.fit(feature_train,answer_train)

    treeClassifier = tree.DecisionTreeClassifier(max_depth=depth)
    treeClassifier = treeClassifier.fit(feature_train,answer_train)
    return treeClassifier

def visTree(dTree):
    dot_data = tree.export_graphviz(dTree, out_file=None)
    graph = graphviz.Source(dot_data)
    return graph
# This allows for the code to be ran from the command line using the make file
if __name__ == "__main__":

    run_dir = sys.argv[1]
    csv_file = sys.argv[2]
    ml_selection = sys.argv[3]

    valid_ml_selections = [ "svm", "stratKfold", "randForest" ]

    if run_dir is None:
        print("Invalid directory given as input. Exiting...")
        os.quit()
    if not csv_file.__contains__("csv"):
        print("Invalid csv file was given as input. Exiting...")
        os.quit()
    if ml_selection not in valid_ml_selections:
        print("Valid machine learning choices:")
        for i in valid_ml_selections:
            print(i)
        print("Invalid machine learning selection. Exiting...")
        os.quit()

    os.chdir(run_dir)

    features, labels = preProcess()

    if ml_selection == "svm":
        svm(features, labels, 10) # need to change this magic value
    if ml_selection == "stratKfold":
        stratKFold(features, labels)
    if ml_selection == "randForest":
        randForest(features, labels)

