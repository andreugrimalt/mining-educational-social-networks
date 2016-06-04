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

#source db 
#mongod --dbpath /Users/chris/expts/praise/dataAnalysis/mongo/db --fork --syslog
#mongod --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/musiccircle
#cli = MongoClient("localhost:27017")
#db = cli.musiccircle

#target instance - intermediate representation
#mongod --port 27018 -dbpath /Users/chris/expts/praise/dataAnalysis/mongo/mus0IR --fork --syslog 
# mongod --port 27018 --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/processedclir = MongoClient("localhost:27018")
#clir = MongoClient("localhost:27026")
#ir = clir.research


json_data=open('histogramFeatureVectors.json')
featureListFromFile = json.load(json_data)


numerOfUsers=len(featureListFromFile['features'])

groundTruthCuster=[]
i=0
for actor in featureListFromFile['features']:
	for feature in actor['featureVectors']:
		groundTruthCuster.append(i)
	i=i+1

k_means = KMeans(n_clusters=numerOfUsers,init='random')

featureList=[]
for actor in featureListFromFile['features']:
	for feature in actor['featureVectors']:
		featureList.append(feature)

k_means.fit(featureList)

clusters={}
iterator=np.arange(0,numerOfUsers)
for i in iterator:
	clusters[str(i)]=[]

clusterListForHist=[]	

for actor in featureListFromFile['features']:
	for feature in actor['featureVectors']:
		cluster=k_means.predict(feature)
		for c in cluster:
			clusters[str(c)].append({'feature':feature,'actor_id':actor['actor_id']})
			clusterListForHist.append(c)

#plt.axis([0,s 4, 0, 800])

p.hist(groundTruthCuster,numerOfUsers,color='r')
plt.xlabel('clusters')
plt.ylabel('Number of feature vectors')
plt.show()
plt.savefig('histGroundTruth.png')
plt.clf()
p.hist(clusterListForHist,numerOfUsers,color='b')
plt.xlabel('clusters')
plt.ylabel('Number of feature vectors')
plt.show()
plt.savefig('histClusterGenerated.png')




