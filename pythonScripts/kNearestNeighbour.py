from numpy import genfromtxt
from bson import *
from pymongo import *
import time
from datetime import timedelta
import numpy as np
import sys
import json
from pymongo.errors import InvalidOperation
import operator
import matplotlib.pyplot as plt
import pylab as p
import math
import random as random
import os
from sklearn.cluster import KMeans
from sklearn import datasets, linear_model
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier

clir = MongoClient("localhost:27026")
ir = clir.research

featureListFromFile = json.load(open('featureMatrix.json'))

outfile=open("kNeighbourScore.json", "w")


# Train data
def makeTrainData():
	trainData=[]
	while(len(trainData)<int(0.9*len(featureListFromFile['featureMatrix']))):
		random.seed(time.time())
		index=random.randint(0, len(featureListFromFile['featureMatrix'])-1)
		if featureListFromFile['featureMatrix'][index] not in trainData:
			trainData.append(featureListFromFile['featureMatrix'][index])
	return trainData

# Test data
def makeTestData():
	testData=[]
	for featureVector in featureListFromFile['featureMatrix']:
		if featureVector not in trainData:
			testData.append(featureVector)
	return testData



# k neighbours classifier
# build feaure vectors and classes for train
def buildFeatureVectorsAndClassesForTrain():
	featureVectorsTrain=[]
	classesTrain=[]
	for user in trainData:
		
		grade=user['grade']
		if grade is not None:
			if grade<50:
				classesTrain.append(1)
			if grade>=50 and grade<70:
				classesTrain.append(2)
			if grade>=70:
				classesTrain.append(3)

			featureVectorsTrain.append(user['featureVector'])
	return [featureVectorsTrain,classesTrain]

# build feaure vectors and classes for test
def buildFeatureVectorsAndClassesForTest():
	featureVectorsTest=[]
	classesTest=[]
	for user in testData:
		grade=user['grade']
		if grade is not None:
			if grade<50:
				classesTest.append(1)
			if grade>=50 and grade<70:
				classesTest.append(2)
			if grade>=70:
				classesTest.append(3)
			featureVectorsTest.append(user['featureVector'])
	return [featureVectorsTest,classesTest]

iterator=np.arange(0,100)
iterator2=np.arange(2,80)
kVsAccuracy=[]

for j in iterator2:
	print j
	temp=[]
	del temp[:]
	for i in iterator:
		trainData=makeTrainData()
		testData=makeTestData()
		print 'train set = ',len(trainData)
		print 'train test = ',len(testData)
		featureVectorsTrain_=buildFeatureVectorsAndClassesForTrain()[0]
		classesTrain_=buildFeatureVectorsAndClassesForTrain()[1]
		print 'trainV=',len(featureVectorsTrain_)
		print 'trainC=',len(classesTrain_)	

		featureVectorsTest_=buildFeatureVectorsAndClassesForTest()[0]
		classesTest_=buildFeatureVectorsAndClassesForTest()[1]

		print 'testV=',len(featureVectorsTest_)
		print 'testC=',len(classesTest_)

		classifier=KNeighborsClassifier(n_neighbors=j)
		classifier.fit(featureVectorsTrain_,classesTrain_)
		score=classifier.score(featureVectorsTest_,classesTest_)
		temp.append(score)
		print score

	maxVal=max(temp)
	minVal=min(temp)
	kVsAccuracy.append([j,maxVal,minVal])

json.dump({'score':kVsAccuracy}, outfile, indent=4)
outfile.close()
