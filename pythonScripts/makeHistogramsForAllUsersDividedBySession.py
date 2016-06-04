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


#source db 
#mongod --dbpath /Users/chris/expts/praise/dataAnalysis/mongo/db --fork --syslog
#mongod --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/musiccircle
cli = MongoClient("localhost:27017")
db = cli.musiccircle

#target instance - intermediate representation
#mongod --port 27018 -dbpath /Users/chris/expts/praise/dataAnalysis/mongo/mus0IR --fork --syslog 
# mongod --port 27018 --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/processedclir = MongoClient("localhost:27018")
clir = MongoClient("localhost:27026")
ir = clir.research

# get actors that hve uploaded and have log activities
actors=ir.Actors.find({"$and":[{"activities.at":{"$eq":0}},{"activities.at":{"$eq":6}}]},timeout=False)
totalActors=actors.count()

print totalActors

def sortActors():
	actorsList=[]
	n=0
	# make a list of actors so we can sort it
	for actor in actors:
		n=n+1
		print totalActors-n," left"
		actorsList.append(actor)
	actorsList.sort(key=operator.itemgetter('uploadsAndLogActivities'))
	return actorsList



# check if a key is in a dictionary
def checkForKey(key,dictionary):
	if key in dictionary:
		return True
	else:
		return False

def makeSessionObjectList(actor):
# make an object that will store session start and end timestamp
	sessionsObjectList=[]
	iterator=np.arange(0,len(actor['sessions'])-1)

	for i in iterator:
		tempSession={}
		tempSession['sessionStart']=actor['sessions'][i]['sessionStart']
		tempSession['nextSession']=actor['sessions'][i+1]['sessionStart']
		sessionsObjectList.append(tempSession)
		#print tempSession
	return sessionsObjectList

def makeActivitiesList(actor):
	# we put the activities in a list so we can sort by timestamp
	activitiesList=[]

	for activity in actor['activities']:
		if activity['at']==0: 
			activitiesList.append(activity)
		if activity['at']==6:
			# get the 'click'
			if checkForKey('logtype',activity) and activity['logtype']!='playing' and checkForKey('type',activity) and activity['type']=='click':
				activitiesList.append(activity)
			
	activitiesList.sort(key=operator.itemgetter('ts'))

	return activitiesList

def makeActivityChunks(sessionsObjectList,activitiesList):
	# we want to devide the activities list respect to the sessions
	activitiesSet=[]

	for session in sessionsObjectList:
		#print session['sessionStart']
		tempAct=[]
		del tempAct[:]
		
		for activity in activitiesList:

			if activity['ts']>=session['sessionStart'] and activity['ts']<session['nextSession']:
				tempAct.append(activity)
				#print activity
		if len(tempAct)!=0:
			activitiesSet.append(tempAct)

	return activitiesSet

def checkForString(dictionary,key,check):
	if key in dictionary and dictionary[key]==check:
		return True
	else:
		return False

def makeHistogram(nActor,activitiesSet):
	n=0
	print len(activitiesSet)
	for activitySet in activitiesSet:
		n=n+1

		theHistogram=[]
		del theHistogram[:]
		for activity in activitySet:
			if activity['at']==0:
				theHistogram.append(0)
			if checkForString(activity,'logtype','region_block'):
				theHistogram.append(1)
			if checkForString(activity,'logtype','my_track_nav_item'):
				theHistogram.append(2)
			if checkForString(activity,'logtype','community_media_nav_item'):
				theHistogram.append(3)
			if checkForString(activity,'logtype','play'):
				theHistogram.append(4)
		if 0 not in theHistogram:
			theHistogram.append(0)
		if 1 not in theHistogram:
			theHistogram.append(1)
		if 2 not in theHistogram:
			theHistogram.append(2)	
		if 3 not in theHistogram:
			theHistogram.append(3)
		if 4 not in theHistogram:
			theHistogram.append(4)
		
		plt.axis([0, 4, 0, 3500])
		p.hist(theHistogram,5)
		#display.clear_output(wait=True)
		#display.display(plt.gcf())
		#time.sleep(0.01)

		if not os.path.exists('./user_'+str(nActor)+'_featureVectors/'):
			os.makedirs('./user_'+str(nActor)+'_featureVectors/')
		plt.savefig('./user_'+str(nActor)+'_featureVectors/'+str(n)+'_.png')
		plt.clf()


actorsList=sortActors()
nActor=0
for actor in actorsList:
	activitiesSet=makeActivityChunks(makeSessionObjectList(actor),makeActivitiesList(actor))
	print len(activitiesSet)
	makeHistogram(nActor,activitiesSet)
	nActor=nActor+1



