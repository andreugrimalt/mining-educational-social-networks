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
#%pylab inline
#from IPython import display


#source db 
#mongod --dbpath /Users/chris/expts/praise/dataAnalysis/mongo/db --fork --syslog
#mongod --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/musiccircle
#cli = MongoClient("localhost:27017")
#db = cli.musiccircle

#target instance - intermediate representation
#mongod --port 27018 -dbpath /Users/chris/expts/praise/dataAnalysis/mongo/mus0IR --fork --syslog 
# mongod --port 27018 --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/processedclir = MongoClient("localhost:27018")
clir = MongoClient("localhost:27026")
ir = clir.research


json_data=open('featureMatrix.json')
featureMatrix = json.load(json_data)


distFile=open('distanceMatrix.json','w')


def calculateDistance(vector1,vector2):
    iterator=np.arange(0,len(vector1))
    sum=0
    for i in iterator:
        sum=sum+math.pow(vector1[i]-vector2[i],2)
    return math.sqrt(sum)


featureMatrixDimension=len(featureMatrix['featureMatrix'])
print featureMatrixDimension
iterator1=np.arange(0,featureMatrixDimension)
distanceMatrix=[]
tempDistance=[]
for i in iterator1:
    print featureMatrixDimension-i, 'left'
    iterator2=np.arange(0,featureMatrixDimension)
    tempDistance=[]
    del tempDistance[:]
    for j in iterator2:
        tempDistance.append(calculateDistance(featureMatrix['featureMatrix'][i],featureMatrix['featureMatrix'][j]))
        if(i==j):
            print calculateDistance(featureMatrix['featureMatrix'][i],featureMatrix['featureMatrix'][j])

    distanceMatrix.append(tempDistance)
json.dump({'distanceMatrix':distanceMatrix}, distFile, indent=4)
distFile.close()

