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
#cli = MongoClient("localhost:27017")
#db = cli.musiccircle

#target instance - intermediate representation
#mongod --port 27018 -dbpath /Users/chris/expts/praise/dataAnalysis/mongo/mus0IR --fork --syslog 
# mongod --port 27018 --dbpath /Users/matthew/Documents/PRAISE_local/data/musiccircle_latest/processedclir = MongoClient("localhost:27018")
clir = MongoClient("localhost:27026")
ir = clir.research

# get actors that have uploaded and have log activities
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



def putEventsInVector(activitiesSet):
	# sort by activity type
	uploads=[]
	del uploads[:]
	region_block=[]
	del region_block[:]
	my_track_nav_item=[]
	del my_track_nav_item[:]
	community_media_nav_item=[]
	del community_media_nav_item[:]
	play=[]
	del play[:]

	for activitySet in activitiesSet:
		for activity in activitySet:
			if activity['at']==0:
				uploads.append(activity)
			if checkForString(activity,'logtype','region_block'):
				region_block.append(activity)
			if checkForString(activity,'logtype','my_track_nav_item'):
				my_track_nav_item.append(activity)
			if checkForString(activity,'logtype','community_media_nav_item'):
				community_media_nav_item.append(activity)
			if checkForString(activity,'logtype','play'):
				play.append(activity)
	sortedByActivityArray = [uploads,region_block,my_track_nav_item,community_media_nav_item,play]

	return sortedByActivityArray


# array with all the actors and their activities quantised
def quantise(actorsList):
	data=[]
	for actor in actorsList:

		actorActivities=[]
		del actorActivities[:]

		activitiesSet=makeActivityChunks(makeSessionObjectList(actor),makeActivitiesList(actor))
		for activities in putEventsInVector(activitiesSet):	
			tempActivities=[]
			del tempActivities[:]
			for event in activities:
				# quantise to 50 ms
				mod=(event['ts'].microsecond/1000.0)%50
				if mod<50:
					new=int((event['ts'].microsecond/1000.0)-mod)*1000
					event['ts']=event['ts'].replace(event['ts'].year,event['ts'].month,event['ts'].day,event['ts'].hour,event['ts'].minute,event['ts'].second,new) 
					tempActivities.append(event)

				elif mod>=50:
					new=int((event['ts'].microsecond/1000.0)+(10-mod))*1000
					event['ts']=event['ts'].replace(event['ts'].year,event['ts'].month,event['ts'].day,event['ts'].hour,event['ts'].minute,event['ts'].second,new)
					tempActivities.append(event)
				#print event['ts']
			actorActivities.append(tempActivities)
		
		data.append(actorActivities)
	return data
				

# generate a list of dates
def dateListGenerator(start, end, delta):
    result=[]
    curr = start
    while curr < end:
        curr += delta
        result.append(curr)
        
    return result

dateList=dateListGenerator(datetime.datetime(2014, 6, 30, 00, 00, 00, 00),datetime.datetime(2014, 8, 30, 00, 00, 00, 00),timedelta(microseconds=50000))

print len(dateList)

activitiesList=quantise(sortActors())

#checking uploads
for date in dateList:
	print date









