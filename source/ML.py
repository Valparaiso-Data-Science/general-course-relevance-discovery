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
    '''
    This process was moved from main.py into here since this process is only 
    necessary for machine learning. Please see the respective functions in 
    vectorize.py to know what they do. 
    
    There is a couple of line added in right before the return statement that 
    allows you to see the percentage of courses that were classified as data 
    science. This is important to check if your accuracy is as good as you think.
    For example, if 3% are data science courses then having a 97% accuracy is 
    pretty good, but you need to check if your confusion matrix shows that the 
    allgorithm straight guessed non-data-science courses thus yielding a 97% 
    accuracy. 
    
    UPDATE (as of 5/18/2021): 
        We needed to rebuild the random forest and we are now building/training
        it using only Smith and Valpo. From here we plan on splitting the data
        using the 10 stratified folds, and using 9 of those folds to build the 
        model. After the model is built we will then predict whether or not a 
        course is data science using the random forest model. The first 
        prediction will be done on the witheld fold, and the second round of 
        predictions will be done on all of Brown. 
        
        Adding in lines to subset AllSchools to only include Smith and Valpo. 
        Also creating a new variable that will be returned that will include 
        Brown's courses. 
    '''
    cleaned_df = pd.read_csv(const.CSV_DIR + "/" + const.ALL_CSV, encoding="ISO-8859-1")
    
    subset_df = cleaned_df.loc[cleaned_df['School'].isin(["Valpo","SmithSUPERTRIMMED"])]
    brown_df = cleaned_df.loc[cleaned_df['School']=='BrownSUPERTRIMMED']
    
    subset_df.to_csv(const.CSV_DIR + "/" + "ValpoAndSmith.csv", encoding="utf-8-sig")
    
    print("\tcleaned")
    vect_df = vectorizer(subset_df)
    print("\tvect")
    pruned_df = cleanVectorizer(vect_df)
    print("\tpruned")
    labeled_df = labelTargetsdf(pruned_df)
    print("\tfound targets")
    #%%
    features = labeled_df.drop("curricula relevance",axis = 1).astype("bool")
    labels = labeled_df["curricula relevance"]
    print(labeled_df.loc[labeled_df["curricula relevance"]==True])
    print('Percentage of classified data science courses: ' + str(sum(labels)/len(labels)))

    return features,labels,brown_df

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
    
    Basically everything that is commented out can be removed from the code. 
    We just never got around to doing this. We also, in case you cannot tell,
    tried using the same for-loop format in multiple places, so we just copied
    and pasted in here. 
    
    UPDATE (as of 5/18/2021): 
        We needed to rebuild the random forest and we are now building/training
        it using only Smith and Valpo. From here we plan on splitting the data
        using the 10 stratified folds, and using 9 of those folds to build the 
        model. After the model is built we will then predict whether or not a 
        course is data science using the random forest model. The first 
        prediction will be done on the witheld fold, and the second round of 
        predictions will be done on all of Brown. 
        
        Being changed are the saved indices. "fold_iterations" will only 
        include the last 9 folds as this is what the model is being built on. 
        The indices of the first fold will be saved in a new variable, 
        "pred_fold", named as such since it will be the fold that gets 
        predicted. Both will be saved so that the model can be built without 
        having to run this part everytime. The file for saving "fold_iterations" 
        will remain the same (recall that this will now only include the last 9 
        folds), and a new file to save "pred_fold" will be created.
        
        Random states were also changed so that they are the same. 
    '''

    skf = StratifiedKFold(n_splits=splits,shuffle=True, random_state = 2021)
    # skf.split(features,labels)
    # errors = []
    pred_fold = [0] #This was added to save the indices of the first fold
    fold_iterations = [0]*9 #Changed to 9 because the first fold is being witheld
    count=0
    print("Keys for features:" + str(features.keys()))
    print("Keys for labels:" + str(labels.keys()))
    #features = features.loc[features['School'].isin(["Valpo","SmithSUPERTRIMMED"])]
    #The line above is added to subset AllSchools.csv and only use Valpo and Smith
    #labels = labels.loc[labels['School'].isin(["Valpo","SmithSUPERTRIMMED"])]
    #The line above is added to subset AllSchools.csv and only use Valpo and Smith
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
        if count != 0: #Since the first fold is being witheld, this if statement
                       #is being added to only do the normal process on the other 
                       #9 folds
            fold_iterations[count-1]=indices #added the "-1" to account for the first fold being witheld
        else:
            pred_fold[count] = indices #The entire else statement has been added to save the first fold
        count+=1
    fold_iterations = asarray(fold_iterations)
    save('fold_iterations.npy',fold_iterations)
    pred_fold = asarray(pred_fold)
    save('pred_fold.npy',pred_fold)
    print(fold_iterations)

def randForest(features,labels,extra_df):
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

    If you end up using this code be sure to save the results to the txt file. 
    The txt file is there to allow for the code to be ran on a computer overnight
    and finish running at any time, while still allowing you to see your results.
    
    UPDATE (as of 5/18/2021): 
        We needed to rebuild the random forest and we are now building/training
        it using only Smith and Valpo. From here we plan on splitting the data
        using the 10 stratified folds, and using 9 of those folds to build the 
        model. After the model is built we will then predict whether or not a 
        course is data science using the random forest model. The first 
        prediction will be done on the witheld fold, and the second round of 
        predictions will be done on all of Brown. 
        
        Changing here is the for loop which will no longer be used. Instead a 
        new for loop will be created to concatenate the 9 folds. Test/Train 
        splits in those folds are being ignored. Then the random forest is 
        being built on those 9 folds. Then, the witheld fold will be predicted 
        on using the random forest. Then the random forest will make 
        predictions on the courses from Brown. The results will be saved to a 
        text file.  
        
        Random states were also changed so that they are the same. 
    '''
    # brown_feat = features.loc[features["School"]=="BrownSUPERTRIMMED"]
    # brown_label = labels.loc[labels["School"]=="BrownSUPERTRIMMED"]
    # #The lines above get the features and labels for Brown
    # features = features.loc[features["School"].isin(["Valpo","SmithSUPERTRIMMED"])]
    # #The line above is added to subset AllSchools.csv and only use Valpo and Smith
    # labels = labels.loc[labels["School"].isin(["Valpo","SmithSUPERTRIMMED"])]
    #The line above is added to subset AllSchools.csv and only use Valpo and Smith
    features.reset_index(inplace=True)
    #labels.reset_index(inplace=True)
    fold_iterations = load('fold_iterations.npy',allow_pickle=True)
    pred_fold = load('pred_fold.npy',allow_pickle=True)
    accs = [0]*len(fold_iterations) #This is to be used with the original for loop
    rf = RandomForestClassifier(n_estimators = 100, random_state = 2021)
    train_x = [] #Created to hold all train data from the 9 folds
    train_y = [] #Created to hold all train data from the 9 folds
    count = 0 #Used with the original for loop
    fold_0 = []
    fold_1 = []
    for fold in fold_iterations:
        ###Below is the original for loop#####
    #     print(fold[0].tolist())
    #     print('Max of fold[0]: '+ str(max(fold[0].tolist())))
    #     print()
    #     print(fold[1].tolist())
    #     print('Max of fold[1]: '+ str(max(fold[1].tolist())))
    #     print('len of features: '+ str(len(features)))
    #     print('len of labels: ' + str(len(labels)))
    #     X_train = features.iloc[fold[0].tolist()]
    #     y_train = labels.iloc[fold[0].tolist()]
    #     X_test = features.iloc[fold[1].tolist()]
    #     y_test = labels.iloc[fold[1].tolist()]
    #     rf.fit(X_train, y_train)
    #     preds = rf.predict(X_test)
    #     #errors.append(round(np.mean(abs(preds - y_test)),2))
    #     forAc = rf.score(X_test,y_test)
    #     accs[count] = forAc
    #     print('Mean Accuracy for forest #' + str(count) +': ' + str(forAc))
    #     print(confusion_matrix(y_test, preds))
    #     count += 1
    # avgAcc = sum(accs)/len(accs)
    # print('Average Model Accuracy: '+ str(avgAcc))
        ###END OF ORIGINAL LOOP#####
        
        # train_x.append(features.iloc[fold[0].tolist()]) 
        # train_y.append(labels.iloc[fold[0].tolist()])
        # train_x.append(features.iloc[fold[1].tolist()])
        # train_y.append(labels.iloc[fold[1].tolist()])
        fold_0.append(fold[0])
        fold_1.append(fold[1])
        #The lines above append all 9 folds together 
    train_x = features.iloc[fold_0]
    train_x.append(labels.iloc[fold_0])
    train_y = features.iloc[fold_1]
    train_y.append(labels.iloc[fold_1])
    print("Train X:")
    print(train_x)
    print("Train Y:")
    print(train_y)
    rf.fit(train_x,train_y) #Fits the model using the 9 folds
    
    test_x = features.iloc[pred_fold[0].tolist()] #test set from witheld fold
    test_y = labels.iloc[pred_fold[1].tolist()] #test set from witheld fold
    fold_prediction = rf.predict(test_x) #Make the model predict using the witheld fold
    fold_conf_matrix = confusion_matrix(test_y,fold_prediction) #See how the model did on that fold
    fold_accuracy = rf.score(test_x,test_y) #Accuracy of the witheld fold
    
    # brown_feat = extra_df.drop("curricula relevance",axis = 1).astype("bool")
    # brown_label = extra_df["curricula relevance"]
    
    # brown_prediction = rf.predict(brown_feat) #Make the model predict using Brown
    # brown_conf_matrix = confusion_matrix(brown_label,brown_prediction) #See how the model did on Brown
    # brown_accuracy = rf.score(brown_feat,brown_label) #Accuracy of Brown
    
    results = open('../source/RandForestResult.txt','w')
    results.write("THE WITHELD FOLD: \n")
    results.write("\t CONFUSION MATRIX: \n")
    results.write("\t \t" + str(fold_conf_matrix) + "\n")
    results.write("\t ACCURACY: \n")
    results.write("\t \t" + str(fold_accuracy) + "\n\n")
    # results.write("BROWN:\n")
    # results.write("\t CONFUSION MATRIX: \n")
    # results.write("\t \t" + str(brown_conf_matrix) + "\n")
    # results.write("\t ACCURACY: \n")
    # results.write("\t \t" + str(brown_accuracy) + "\n\n")
    results.close()
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
    test-train splits made by the k-fold function. So, in theory this function
    when reformatted should easily be ran using the saved indices.

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

def OldrandForest(features,labels,splits=10):
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
    This is an old version of the random forest code that does not seperate
    out the process of data splitting+undersampling from the random forest. 
    This version works, unlike the other version, but it takes a very long time
    to run. 
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
        X_train,y_train = Oldundersample(X_train,y_train)
        rf = RandomForestClassifier(n_estimators = 100, random_state = 42)
        rf.fit(X_train, y_train)
        preds = rf.predict(X_test)
        #errors.append(round(np.mean(abs(preds - y_test)),2))
        # i=0
        # for pred in preds:
        #     if pred == y_test[i]:
        #         accs[count]+=1
        #     i +=1
        # accs[count] = (accs[count]/len(preds))*100
        forAc = rf.score(X_test,y_test)
        accs[count] = forAc
        count += 1
        print('Mean Accuracy: ' + str(forAc))
        print(confusion_matrix(y_test, preds))
        #vizRFTrees(rf, 5, features)
    count = 0
    modelAc= sum(accs)/len(accs)
    print("Average Model Accuracy: "+ str(modelAc))
    results = open('../source/RandForestResult.txt','w')
    r = results.write("Average Model Accuracy: "+ str(modelAc))
    results.close()

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

def Oldundersample(features, labels, split=0.5):
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
    newLabels : list
        The new set of labels after running near miss.
    
    newFeatures: list
        See above.
        
    Notes
    -----
    This is an old version of the undersample code. Again, it takes a while to 
    run given that it calculates distances for many points in a multidimensional
    space, but it works. Print statements were added for debugging. Feel free 
    to take them out or comment them out. There is also the line commented out 
    for random under sampling. If you wish to use this you must change nmus to 
    rus where it says .fit_resample()
    '''
    #rus = RandomUnderSampler(sampling_strategy=split, random_state=19)
    nmus = NearMiss(version=3,sampling_strategy={0:sum(labels),1:sum(labels)})
    newFeatures, newLabels = nmus.fit_resample(features, labels)
    print(len(newLabels))
    print(sum(newLabels))
    print(newFeatures)
    return newFeatures, newLabels

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
        1. Random Forest code doesn't even work yet.
        2. Because of the point above, we are not sure if this function works. 

    '''
    outfile='randFor_Tree'+ntree+'.dot'
    export_graphviz(rf.estimators_[ntree],outfile = outfile,feature_names=list(features.columns),
                    filled=True)
    call(['dot', '-Tpng', outfile, '-o', 'tree.png', '-Gdpi=600'])
    Image(filename='tree.png')
'''
decisionTree and visTree were from the summer before ours (ie nathan wrote it)
    
Random forest was made to upgrade decision tree
    
vizRFTrees was made to replace visTree
'''
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

