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


json_data=open('featureMatrix.json')
featureList = json.load(json_data)


k_means = KMeans(n_clusters=2,init='random')
k_means.fit(featureList['featureMatrix']) 
clusters=[]
for feature in featureList['featureMatrix']:
    cluster=k_means.predict(feature)
    for c in cluster:
    	clusters.append(c)
    
    

#plt.axis([0, 4, 0, 800])
p.hist(clusters)
plt.show()





