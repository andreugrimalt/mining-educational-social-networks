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



clir = MongoClient("localhost:27026")
ir = clir.research

# get users

tenVeryActiveUsers=ir.Actors.find({"$and":[{"activities.at":{"$eq":0}},{"activities.at":{"$eq":6}}]},timeout=False)

totalUsers=tenVeryActiveUsers.count()

feedbackTriggers=[]
featureMatrix=[]
featureVector=[]
nUsers=0

outfile=open("featureMatrix.json", "w")

for user in tenVeryActiveUsers:

    uploads=0
    region_block=0
    my_track_nav_item=0
    community_title_nav_item=0
    play=0
    comments=0
    nUsers=nUsers+1

    featureVector=[]
    del featureVector[:]
    feedbackTriggers=[]
    del feedbackTriggers[:]
    
    for activity in user["activities"]:
            # get click events ignore playing logs
        if 'type' in activity.keys() and activity['type']=='click' and activity["logtype"]!="playing":
            feedbackTriggers.append(activity)

        if activity['at']==0:
            uploads=uploads+1
        if activity['at']==2:
            comments=comments+1
    print "feedbackTriggers has length = ",len(feedbackTriggers)
    # sort feedbackTriggers array by time
    feedbackTriggers.sort(key=operator.itemgetter('ts'))
    iterator=np.arange(0,len(feedbackTriggers)-1)

    for i in iterator:
        if feedbackTriggers[i+1]['ts']-feedbackTriggers[i]['ts']>datetime.timedelta(milliseconds=200):
            #print feedbackTriggers[i]
            if feedbackTriggers[i]['logtype']=='region_block':
                region_block=region_block+1
            if feedbackTriggers[i]['logtype']=='my_track_nav_item':
                my_track_nav_item=my_track_nav_item+1
            if feedbackTriggers[i]['logtype']=='community_title_nav_item':
                community_title_nav_item=community_title_nav_item+1
            if feedbackTriggers[i]['logtype']=='play':
                play=play+1
                #feedbackTriggersFiltered.append(feedbackTriggers[i])
    featureVector.append(uploads)
    featureVector.append(region_block)
    featureVector.append(my_track_nav_item)
    featureVector.append(community_title_nav_item)
    featureVector.append(play)
    featureVector.append(comments)
    
    norm = [float(i)/sum(featureVector) for i in featureVector]
    grade=ir.ActorsGrade.find_one({'id':user['_id']})
    if grade is None:
        grade=None
    else:
        grade=grade['grade'][0]
    featureMatrix.append({'id':str(user['_id']), 'grade':grade,'featureVector':norm})

    print nUsers


json.dump({'featureMatrix':featureMatrix}, outfile, indent=4)
outfile.close()
print "feature matrix has ",len(featureMatrix)," vectors"



    
#print "feedbackTriggers has ", len(feedbackTriggers)," elements"