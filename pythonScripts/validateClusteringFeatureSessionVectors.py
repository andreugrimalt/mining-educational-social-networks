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
import os
from sklearn.cluster import KMeans
import random
from collections import *
from sklearn import metrics


json_data=open('histogramFeatureVectors.json')
featureListFromFile = json.load(json_data)


numerOfUsers=len(featureListFromFile['features'])

k_means = KMeans(n_clusters=numerOfUsers,init='random')

featureList=[]
for actor in featureListFromFile['features']:
	for feature in actor['featureVectors']:
		featureList.append(feature)

k_means.fit(featureList)

groundTruthCuster=[]
i=0
for actor in featureListFromFile['features']:
	for feature in actor['featureVectors']:
		groundTruthCuster.append(i)
	i=i+1

modelCluster=[]	

for actor in featureListFromFile['features']:
	for feature in actor['featureVectors']:
		cluster=k_means.predict(feature)
		for c in cluster:
			modelCluster.append(c)

print "adjusted random index (different from assigning random classes?)= ",metrics.adjusted_rand_score(groundTruthCuster,modelCluster)
print "adjusted mutual Information based scores (tends to increase with number of clusters)= ",metrics.adjusted_mutual_info_score(groundTruthCuster,modelCluster)
print "homogenity, completeness, v-measure scores = ",metrics.homogeneity_completeness_v_measure(groundTruthCuster,modelCluster)







