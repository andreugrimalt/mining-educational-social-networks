# Build feature vectors and store them in a json file

from bson import *
from pymongo import *
import time
from datetime import timedelta
import numpy as np
import json
import operator
import os

# Connect to the research database
clir = MongoClient("localhost:27026")
ir = clir.research

# get actors that have uploaded and have log activities
actors=ir.Actors.find({"$and":[{"activities.at":{"$eq":0}},{"activities.at":{"$eq":6}}]},timeout=False)
totalActors=actors.count()

print totalActors

# Sort the actors by their number of activities
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

# Check if a key is in a dictionary
def checkForKey(key,dictionary):
	if key in dictionary:
		return True
	else:
		return False
´
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

def makeFeatureVectors(activitiesSet):
	n=0

	#print len(activitiesSet)

	featureVectors=[]
	del featureVectors[:]
	for activitySet in activitiesSet:
		n=n+1
		upload=0
		region_block=0
		my_track_nav_item=0
		community_media_nav_item=0
		play=0
		tempVector=[]
		for activity in activitySet:
			if activity['at']==0:
				upload=upload+1
			if checkForString(activity,'logtype','region_block'):
				region_block=region_block+1
			if checkForString(activity,'logtype','my_track_nav_item'):
				my_track_nav_item=my_track_nav_item+1
			if checkForString(activity,'logtype','community_media_nav_item'):
				community_media_nav_item=community_media_nav_item+1
			if checkForString(activity,'logtype','play'):
				play=play+1

		tempVector.append(upload)
		tempVector.append(region_block)
		tempVector.append(my_track_nav_item)
		tempVector.append(community_media_nav_item)
		tempVector.append(play)
		featureVectors.append(tempVector)
	
	return featureVectors


actorsList=sortActors()

outfile=open("histogramFeatureVectors.json", "w")

featureList=[]
for actor in actorsList:
	featureObject={}
	activitiesSet=makeActivityChunks(makeSessionObjectList(actor),makeActivitiesList(actor))
	#print len(activitiesSet)
	featureObject['actor_id']=str(actor['_id'])
	featureObject['featureVectors']=makeFeatureVectors(activitiesSet)
	featureList.append(featureObject)

json.dump({'features':featureList}, outfile, indent=4)
outfile.close()




