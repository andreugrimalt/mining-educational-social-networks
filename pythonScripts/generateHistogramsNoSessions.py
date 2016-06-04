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

# get first of very active users
#tenVeryActiveUsers=ir.Actors.find({"$and":[{"$where":"this.activities.length >49000"},{"activities.at":{"$eq":6}}]})
tenVeryActiveUsers=ir.Actors.find({"$and":[{"$where":"this.activities.length >100"},{"activities.at":{"$eq":6}},{"activities.at":{"$eq":0}}]},timeout=False)

# this finds feedback triggers (clicks)
feedbackTriggers=[]
#fig = plt.figure()
theHistogram=[]
#plt.ion()
#plt.show()
nUser=0
numberOfUsers=tenVeryActiveUsers.count()
for user in tenVeryActiveUsers:
    feedbackTriggers=[]
    theHistogram=[]
    del feedbackTriggers[:]
    del theHistogram[:]
    nUser=nUser+1
    print numberOfUsers-nUser," left"

    for activity in user["activities"]:
            if activity['at']==0:
                theHistogram.append(0)
            # get click events ignore playing logs
            if 'type' in activity.keys() and activity['type']=='click' and activity["logtype"]!="playing":
                    feedbackTriggers.append(activity)
    print "feedbackTriggers has length = ",len(feedbackTriggers)
    # sort feedbackTriggers array by time
    feedbackTriggers.sort(key=operator.itemgetter('ts'))
    iterator=np.arange(0,len(feedbackTriggers)-1)

    
    for i in iterator:
        if feedbackTriggers[i+1]['ts']-feedbackTriggers[i]['ts']>datetime.timedelta(milliseconds=200):
            #print feedbackTriggers[i]
            if feedbackTriggers[i]['logtype']=='region_block':
                theHistogram.append(1)
            if feedbackTriggers[i]['logtype']=='my_track_nav_item':
                theHistogram.append(2)
            if feedbackTriggers[i]['logtype']=='community_title_nav_item':
                theHistogram.append(3)
            if feedbackTriggers[i]['logtype']=='play':
                theHistogram.append(4)
                #feedbackTriggersFiltered.append(feedbackTriggers[i])
    #fig = plt.figure()
    if 0 in theHistogram and 1 in theHistogram and 2 in theHistogram and 3 in theHistogram and 4 in theHistogram: 
        plt.axis([0, 4, 0, 500])
        p.hist(theHistogram,5)
        #display.clear_output(wait=True)
        #display.display(plt.gcf())
        #time.sleep(0.01)
        plt.savefig('./png/'+str(nUser)+'_'+str(int(time.time()))+'.png')
        plt.clf()
    
#print "feedbackTriggers has ", len(feedbackTriggers)," elements"