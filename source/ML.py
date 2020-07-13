# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 13:50:39 2019

@author: nrandle
"""
import os
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

def randForest(features,labels,splits=10):
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
    '''

    skf = StratifiedKFold(n_splits=splits,shuffle=True, random_state = 19)
    # skf.split(features,labels)
    # errors = []
    accs = [0]*splits
    fold_iterations = [0]*10
    count=0
    # features.reset_index(inplace=True)
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
        ds_i = features.index[labels == 1]
        train_index = np.append(maj_train_index,ds_i)
        indices[0]=train_index
        fold_iterations[count]=indices
        count+=1
    print(fold_iterations)    
    # rf = RandomForestClassifier(n_estimators = 100, random_state = 42)
    #     rf.fit(X_train, y_train)
    #     preds = rf.predict(X_test)
    #     #errors.append(round(np.mean(abs(preds - y_test)),2))
    #     i=0
    #     for pred in preds:
    #         if pred == y_test[i]:
    #             accs[count]+=1
    #         i +=1
    #     accs[count] = (accs[count]/len(preds))*100
    #     count += 1
    #     forAc = rf.score(X_test,y_test)
    #     accs.append(forAc)
    #     print('Mean Accuracy: ' + str(forAc))
    #     print(confusion_matrix(y_test, preds))
    #     #vizRFTrees(rf, 5, features)
    ####################################################
    # count = 0
    # modelAc= sum(accs)/len(accs)
    # print("Average Model Accuracy: "+ str(modelAc*100))
    # results = open('../source/RandForestResult.txt','w')
    # r = results.write("Average Model Accuracy: "+ str(modelAc*100))
    # results.close()
def svm(features,labels,splits):
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
    #rus = RandomUnderSampler(sampling_strategy=split, random_state=19)
    nmus = NearMiss(version=3,sampling_strategy={0:sum(labels),1:sum(labels)})
    nmus.fit_resample(features, labels)
    newLabels = nmus.sample_indices_
    print(len(newLabels))
    #print(sum(newLabels))
    # print(newFeatures)
    return newLabels

def vizRFTrees(rf, ntree,features):
    outfile='randFor_Tree'+ntree+'.dot'
    export_graphviz(rf.estimators_[ntree],outfile = outfile,feature_names=list(features.columns),
                    filled=True)
    call(['dot', '-Tpng', outfile, '-o', 'tree.png', '-Gdpi=600'])
    Image(filename='tree.png')

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
